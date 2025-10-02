Expense Tracker API

A RESTful backend API built with FastAPI and MySQL for secure management of incomes and expenses, providing insights and optional currency conversion.

Technologies Used

* Backend: FastAPI (Python)
* Database: MySQL
* Authentication: JWT
* Currency Conversion: Forex-Python
* API Documentation: Swagger UI (/docs)

Key Features

* User Authentication: JWT-based login and registration.
* Income & Expense Management: Create, read, update, and delete records.
* Filtering & Analytics: Filter by category, source, month, and year; view monthly insights.
* Currency Conversion: Convert amounts between different currencies in real-time using Forex-Python.
* Secure & User-Specific: Each user can only access their own data.

Setup / Run Locally

1. Clone the repository:
   git clone https://github.com/GunnamDeekshitha/expense-tracker-api.git
   cd expense-tracker-api
2. Install dependencies:
   pip install -r requirements.txt
3. Configure MySQL database
   *  Replace "replace_your_password" in app/database.py with your MySQL password.
4. Run the FastAPI server:
   uvicorn app.main:app --reload
5. Access API documentation in your browser:
   http://127.0.0.1:8000/docs
