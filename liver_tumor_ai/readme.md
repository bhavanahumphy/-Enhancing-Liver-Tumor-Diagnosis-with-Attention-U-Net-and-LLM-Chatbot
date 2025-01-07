Here’s a detailed `README.md` file for your project `liver_tumor_ai`. It guides users through the setup, including creating a virtual environment, installing dependencies, setting up the `.env` file for the Google API key, and starting the FastAPI app.

---

# liver_tumor_ai

This project leverages FastAPI and AI models to assist in analyzing liver tumor data. It integrates with Google API services for AI processing and provides an interactive web interface.

## Setup Guide

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

### 8. Access the API Documentation

FastAPI automatically generates interactive API documentation. You can access it by navigating to:

```
http://127.0.0.1:8000/docs
```

You can interact with the API directly from this interface to send requests and view responses.

---
