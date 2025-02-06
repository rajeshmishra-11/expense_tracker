# Expense Tracker

An **Expense Tracker** web application built using **Flask, MySQL, and Bootstrap** that allows users to manage their expenses efficiently.

## Features
- **User Authentication**: Secure login and registration with hashed passwords.
- **Expense Management**: Add, view, update, and delete expenses.
- **Graphical Insights**: Visual representation of expenses using bar charts and pie charts.
- **Category-wise Tracking**: View total expenses and category-wise breakdown.
- **Multi-Device Support**: Access your expenses from different devices using a MySQL database.
- **Modern UI**: Responsive design using Bootstrap for a smooth experience.
- **Success/Error Messages**: User-friendly notifications for actions like login, registration, and expense management.

## Technologies Used
- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, Bootstrap
- **Database**: MySQL
- **Charting**: Chart.js for visualizing expenses

## Installation & Setup
### Prerequisites
- Python 3.x installed
- MySQL installed and running
- Virtual environment (optional but recommended)

### Steps
1. **Clone the repository**:
   ```sh
   git clone https://github.com/rajeshmishra-11/expense-tracker.git
   cd expense-tracker
   ```

2. **Create a virtual environment** (optional but recommended):
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up the database**:
   - Create a MySQL database (e.g., `expense_tracker_db`).
   - Import the provided SQL schema.
   - Configure database credentials in `config.py`.

5. **Run the application**:
   ```sh
   python app.py
   ```

6. **Access the app**:
   Open your browser and go to `http://127.0.0.1:5000`

## API Routes
| Route              | Method | Description              |
|--------------------|--------|--------------------------|
| `/login`          | POST   | User login               |
| `/register`       | POST   | User registration        |
| `/add_expense`    | POST   | Add a new expense        |
| `/update_expense` | PUT    | Update an expense        |
| `/delete_expense` | DELETE | Delete an expense        |
| `/get_expenses`   | GET    | Retrieve all expenses    |


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss the changes.

## Contact
For any inquiries or support, reach out to [rajeshmishra847410@gmail.com].

