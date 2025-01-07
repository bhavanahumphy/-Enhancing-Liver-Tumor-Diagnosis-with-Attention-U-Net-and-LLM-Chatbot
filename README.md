# -Enhancing-Liver-Tumor-Diagnosis-with-Attention-U-Net-and-LLM-Chatbot

# Abstract
This project focuses on enhancing liver tumor segmentation and patient interaction through a hybrid U-Net model with attention mechanisms and a Large Language Model (LLM)-powered chatbot. The proposed solution integrates transformer blocks into the U-Net architecture to improve segmentation precision in liver CT scans, addressing challenges such as tumor variability and class imbalance. The web application provides an intuitive interface for uploading CT images, visualizing segmentation outputs, and interacting with the LLM chatbot for personalized and empathetic healthcare guidance. Results demonstrate the system's high accuracy (99.12%) and user engagement effectiveness, paving the way for AI-driven advancements in diagnostic healthcare. Future work includes expanding to multimodal imaging, 3D convolution, and clinical system integration.

# Installation Documentation

Dataset Link:

Part-1: https://www.kaggle.com/datasets/andrewmvd/liver-tumor-segmentation

Here download all the files i.e segmentation files and volume files 

Part-2: https://www.kaggle.com/datasets/andrewmvd/liver-tumor-segmentation-part-2

Here also download all the files i.e volume-pt-6 and volume-pt-8

For Frontend File with name Frontend 

Install these necessary Python packages:
pip install Flask Flask-SQLAlchemy Flask-Bcrypt matplotlib Pillow numpy tensorflow

Place the unet_model_weights.weights.h5 in the root directory.

### Set environment variable
export FLASK_APP=app.py

### Start the application
flask run

Visit http://localhost:5000 to access the app after starting the server.


For LLM file that is with the name liver_tumor_ai

Here’s a detail for `liver_tumor_ai`. This guides users through the setup, including creating a virtual environment, installing dependencies, setting up the `.env` file for the Google API key, and starting the FastAPI app.
### liver_tumor_ai
This project leverages FastAPI and AI models to assist in analyzing liver tumor data. It integrates with Google API services for AI processing and provides an interactive web interface.

### Setup Guide
Follow the steps below to set up the project on your local machine.

### 1. Clone the repository
First, clone the repository to your local machine:

```bash
Extract the zip_folder
cd liver_tumor_ai
```
### 2. Create a Virtual Environment
Create a virtual environment to isolate the project dependencies:

#### On Windows:
```bash
python -m venv venv
```

#### On macOS/Linux:
```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment
Activate the virtual environment.

#### On Windows:
```bash
.\venv\Scripts\activate
```

#### On macOS/Linux:
```bash
source venv/bin/activate
```
Once activated, your prompt should change, indicating that you're now working inside the virtual environment.

### 4. Install Dependencies
With the virtual environment activated, install the required dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```
### 5. Set Up the `.env` File
This project requires the Google API key to function. To obtain the Google API key, follow these steps:
1. Go to the [Google Cloud Console](https://aistudio.google.com/).
2. Login with your Google Account
3. Click on **Get API Key**
4. Go to the **Credentials** tab and create an API key.
5. Copy the API key.
Next, create a `.env` file in the root directory of the project (`liver_tumor_ai/`) and add the API key like this:
```env
GOOGLE_API_KEY=your-google-api-key-here
```
Replace `your-google-api-key-here` with the actual API key you obtained.

### 6. Start the FastAPI App
Once all dependencies are installed and the `.env` file is properly configured, you can start the FastAPI app using **Uvicorn**:

```bash
uvicorn app:app --reload
```

- `app` refers to the Python file (`app.py`) where your FastAPI app is defined.
- `app` is the FastAPI instance created in your `app.py`.
- The `--reload` flag enables auto-reloading during development, so any changes to the code will automatically be reflected.

### 7. Check the Output

Once the server is running, open your browser and navigate to:
```
http://127.0.0.1:8000
```
You should see the FastAPI application running. If you see the FastAPI interface or any other expected output, the setup is complete.


