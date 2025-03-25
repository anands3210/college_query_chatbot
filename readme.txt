# FAQ Chatbot System
Developed by Anand Srivastava

A Flask-based FAQ chatbot system that uses fuzzy matching to answer questions from a database of frequently asked questions.

## Key Features

- Interactive Q&A chatbot interface
- Admin panel for FAQ management
- CSV file upload support
- Fuzzy matching algorithm for intelligent responses
- Responsive design for all devices

## Technical Stack

- Flask (Web Framework)
- SQLite (Database)
- FuzzyWuzzy (Text Matching)
- HTML/CSS (Frontend)

## Detailed Setup Guide

### 1. Set Up Development Environment

1. Install Python (3.8 or higher):
   ```
   https://www.python.org/downloads/
   ```

### 2. Transfer Files to New Device

1. Create a new directory on the target device
2. Copy all project files to the new directory:
   - app.py
   - requirements.txt
   - templates/ folder
   - static/ folder (if exists)
   - Any other project files

You can transfer files using:
- USB drive
- Network file sharing
- Cloud storage (Dropbox, Google Drive, etc.)
- Direct file transfer tools (like FileZilla)

### 3. Set Up Virtual Environment

1. Open terminal/command prompt
2. Navigate to project directory:
   ```
   cd path/to/your/project
   ```
3. Create virtual environment:
   ```
   python -m venv venv
   ```
4. Activate virtual environment:
   - Windows:
     ```
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```
     source venv/bin/activate
     ```

### 4. Install Dependencies

1. Install required packages:
   ```
   pip install -r requirements.txt
   ```

### 5. Initialize Application

1. Create uploads directory:
   ```
   mkdir uploads
   ```
2. Run the application:
   ```
   flask run
   ```
3. Access the application:
   ```
   http://localhost:5000
   ```

## Usage

### User Interface
- Visit the homepage to interact with the chatbot
- Type your question and receive relevant answers
- System uses fuzzy matching to find the best response

### Admin Interface
- Login with admin credentials:
  - Username: anand_srivastava (password: anand123)
  - Username: mohini_khattri (password: mohini123)
- Add, edit, or delete FAQ entries
- Upload FAQ data through CSV files
- Manage the knowledge base

## Project Structure

- app.py: Main application file
- templates/: HTML templates
- static/: CSS and JavaScript files
- uploads/: Directory for CSV uploads
- faq.db: SQLite database file

## Dependencies

All required dependencies are listed in requirements.txt including:
- Flask==2.3.3
- Flask-SQLAlchemy==3.1.1
- FuzzyWuzzy==0.18.0
- Python-Levenshtein==0.21.1
- Additional supporting libraries

## Troubleshooting

Common issues and solutions:
1. Database errors: Delete faq.db and restart Flask
2. Package conflicts: Create fresh virtual environment
3. Port in use: Change port using flask run --port xxxx
4. File permissions: Ensure proper read/write access to project directory

## Developer Contact

For any queries or support, please contact:
Anand Srivastava




