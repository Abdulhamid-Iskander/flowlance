# Flowlance - Freelance Platform

## How to Run the Project 
1. **Create and Activate Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:

pip install -r requirements.txt

Set Environment Variables:

Copy the .env.example file and rename it to .env.

cp .env.example .env

Run Migrations (if database is not included):

python manage.py migrate

Run the Server:

python manage.py runserver

Open http://127.0.0.1:8000 in your browser.