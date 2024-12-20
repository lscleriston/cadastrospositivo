# Flask Web Application

This project is a simple web application built using Flask, designed for employee authentication through a login screen.

## Project Structure

```
flask-web-app
├── app
│   ├── __init__.py          # Initializes the Flask application
│   ├── forms.py             # Contains the LoginForm class
│   ├── routes.py            # Defines application routes
│   ├── templates            # Directory for HTML templates
│   │   └── login.html       # Login screen HTML
│   └── static               # Directory for static files (CSS, JS, images)
├── config.py                # Configuration settings for the application
├── run.py                   # Entry point to run the Flask application
└── README.md                # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd flask-web-app
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

5. **Run the application:**
   ```
   python run.py
   ```

## Overview

This application provides a login screen for employees to authenticate themselves. It includes form validation to ensure that users enter a valid email and password. The application is structured to separate concerns, making it easy to maintain and extend in the future.