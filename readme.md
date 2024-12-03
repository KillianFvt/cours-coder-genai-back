# Project Installation Guide

## Prerequisites

Ensure you have the following installed on your system:
- Python (v3.8 or higher)
- pip (v20 or higher)

## Installation Steps

1. **Clone the repository:**
   ```sh
   git clone https://github.com/KillianFvt/cours-coder-genai-back.git
   cd cours-coder-genai-back
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Run the development server:**
   ```sh
   python manage.py runserver
   ```
   _Note : The **database** is in the repository, you can use it to test the project._
   _It's a SQLite database, filename is `db.sqlite3`_


4. **Run tests:**
   ```sh
   python manage.py test
   ```

## Additional Scripts

- **Make migrations:**
  ```sh
   python manage.py makemigrations
  ```

- **Apply migrations:**
  ```sh
   python manage.py migrate
  ```

## Project Structure

- `shopping/` - Shopping app, used for managing products and orders
- `cours_coder_genai/` - Project settings and configuration
- `cookie_token/` - Custom JWT authentication backend
- `tests/` - Test files
- `manage.py` - Django management script
- `requirements.txt` - Project dependencies