from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, UpSampling2D, concatenate, LayerNormalization, MultiHeadAttention, Dense
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/outputs'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    gender = db.Column(db.Enum('M', 'F', 'O'), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def load_and_preprocess_image(image_path, target_size=(128, 128)):
    img = Image.open(image_path).convert('RGB')
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)


def transformer_block(x, num_heads=2, ff_dim=32):
    attn_output = tf.keras.layers.MultiHeadAttention(num_heads=num_heads, key_dim=x.shape[-1])(x, x)
    attn_output = tf.keras.layers.LayerNormalization(epsilon=1e-6)(attn_output + x)
    ff_output = tf.keras.layers.Dense(ff_dim, activation="relu")(attn_output)
    ff_output = tf.keras.layers.Dense(x.shape[-1])(ff_output)
    return tf.keras.layers.LayerNormalization(epsilon=1e-6)(ff_output + attn_output)

def unet_with_attention(input_layer):
    conv1 = Conv2D(64, (3, 3), activation='relu', padding='same')(input_layer)
    pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
    pool1 = transformer_block(pool1)
    conv2 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool1)
    pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
    conv3 = Conv2D(128, (3, 3), activation='relu', padding='same')(pool2)
    up1 = UpSampling2D((2, 2))(conv3)
    concat1 = concatenate([conv2, up1], axis=-1)
    concat1 = transformer_block(concat1)
    conv4 = Conv2D(64, (3, 3), activation='relu', padding='same')(concat1)
    up2 = UpSampling2D((2, 2))(conv4)
    concat2 = concatenate([conv1, up2], axis=-1)
    outputs = Conv2D(1, (1, 1), activation='sigmoid')(concat2)
    model = Model(inputs=input_layer, outputs=outputs)
    return model


# Function to make predictions
def predict_image(model, image_path):
    processed_image = load_and_preprocess_image(image_path)  # Load and preprocess the image
    prediction = model.predict(processed_image)  # Make prediction
    prediction = np.squeeze(prediction)  # Remove batch dimension
    return prediction

input_layer = Input(shape=(128, 128, 3))
unet_model = unet_with_attention(input_layer)
#unet_model.compile(optimizer=Adam(learning_rate=1e-4), loss='binary_crossentropy', metrics=['accuracy'])


try:
    unet_model.load_weights('unet_model_weights.weights.h5')
except Exception as e:
    print("Error loading weights:", e)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['user_id'] = user.id  # Store user ID in session
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')   # Updated from 'username' to 'name'
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        age = request.form.get('age')
        gender = request.form.get('gender')
        mobile = request.form.get('mobile')

        # Validate mobile number
        if len(mobile) != 10 or not mobile.isdigit():
            flash('Mobile number must be exactly 10 digits.', 'danger')
            return render_template('login.html')

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash('Email address already in use. Please choose a different one.', 'danger')
            return render_template('login.html')

        # Check if name (username) already exists
        if User.query.filter_by(name=name).first():
            flash('Name is already taken. Please choose a different one.', 'danger')
            return render_template('login.html')

        # Validate password
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('login.html')

        if len(password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            return render_template('login.html')

        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password)

        # Create a new user instance
        new_user = User(
            name=name,
            email=email,
            password=hashed_password,
            age=age,
            gender=gender,
            mobile=mobile
        )

        # Add and commit the new user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/prediction', methods=['GET', 'POST'])
def prediction():
    if request.method == 'POST':
        file = request.files.get('image')
        if not file or file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if allowed_file(file.filename):
            filename = file.filename
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)
            prediction = predict_image(unet_model, image_path)
            segmented_image_path = os.path.join(app.config['OUTPUT_FOLDER'], 'segmented_' + filename)
            plt.imsave(segmented_image_path, prediction, cmap='gray')
            result = {
                'image_filename': 'uploads/' + filename,
                'segmented_filename': 'outputs/segmented_' + filename,
                #'comparison_filename': 'outputs/comparison_' + filename
            }
            return render_template('prediction.html', result=result)
    return render_template('prediction.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Remove user ID from session
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)



