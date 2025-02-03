from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_db_connection
import datetime

app = Flask(__name__)
app.secret_key = 'rajesh@11'  


@app.route('/')
def home():
    return render_template('home.html')


# User Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()

        if existing_user:
            flash("Username or Email already taken!", "error")
            return render_template("register.html")

        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", 
                       (username, email, hashed_password))
        db.commit()
        db.close()

        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')  # Use .get() to safely access the form data
        password = request.form.get('password')

        if not email or not password:
            flash("Email and password are required!", "error")
            return render_template('login.html')

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        db.close()

        if user and check_password_hash(user[3], password):  # user[3] refers to the hashed password in DB
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash("Login successful!", "success")
            return redirect(url_for('dashboard'))

        flash("Invalid credentials! Please try again.", "error")

    return render_template('login.html')


# User Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("Logout successful!", "success")
    return redirect(url_for('login'))

#Dashboard
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # Check if the user is logged in
    if 'user_id' not in session:
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for('login'))

    # Establish database connection
    db = get_db_connection()
    cursor = db.cursor()

    # Fetch the username based on the logged-in user
    cursor.execute("SELECT username FROM users WHERE id = %s", (session['user_id'],))
    user = cursor.fetchone()
    username = user[0] if user else 'Guest'

    # Get the selected month and year from the request
    month = request.args.get('month')
    year = request.args.get('year')

    # Fetch expenses for the selected month and year (if provided)
    if month and year:
        cursor.execute("""
            SELECT * FROM expenses 
            WHERE user_id = %s AND MONTH(date) = %s AND YEAR(date) = %s
        """, (session['user_id'], month, year))
    else:
        cursor.execute("SELECT * FROM expenses WHERE user_id = %s", (session['user_id'],))

    expenses = cursor.fetchall()

    # Get the category-wise sum of expenses
    if month and year:
        cursor.execute("""
            SELECT category, SUM(amount) 
            FROM expenses 
            WHERE user_id = %s AND MONTH(date) = %s AND YEAR(date) = %s
            GROUP BY category
        """, (session['user_id'], month, year))
    else:
        cursor.execute("""
            SELECT category, SUM(amount) 
            FROM expenses 
            WHERE user_id = %s
            GROUP BY category
        """, (session['user_id'],))

    category_sums = cursor.fetchall()

    # Close the database connection
    db.close()

    # Separate categories and amounts for the template
    categories = [row[0] for row in category_sums]
    amounts = [row[1] for row in category_sums]
    total_expense = sum(amounts)

    # Render the template, passing the username and other data
    return render_template('dashboard.html', 
                           expenses=expenses, 
                           categories=categories, 
                           amounts=amounts, 
                           total_expense=total_expense, 
                           month=month, 
                           year=year,
                           username=username)  # Pass username to the template

# Add Expense
@app.route('/add_expense', methods=['GET', 'POST'])
def add_expense():
    if 'user_id' not in session:
        flash("Please log in to add an expense.", "error")
        return redirect(url_for('login'))

    if request.method == 'POST':
        category = request.form['category']
        amount = request.form['amount']
        description = request.form['description']
        date = request.form['date']

        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("""
            INSERT INTO expenses (user_id, category, amount, description, date) 
            VALUES (%s, %s, %s, %s, %s)
        """, (session['user_id'], category, amount, description, date))
        db.commit()
        db.close()

        flash("Expense added successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('add_expense.html')


# Update Expense
@app.route('/update_expense/<int:expense_id>', methods=['GET', 'POST'])
def update_expense(expense_id):
    if 'user_id' not in session:
        flash("Please log in to update expenses.", "error")
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor()

    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = float(request.form['amount'])
        description = request.form['description']

        cursor.execute("""
            UPDATE expenses 
            SET date = %s, category = %s, amount = %s, description = %s 
            WHERE id = %s AND user_id = %s
        """, (date, category, amount, description, expense_id, session['user_id']))
        db.commit()
        db.close()

        flash("Expense updated successfully!", "success")
        return redirect(url_for('dashboard'))

    cursor.execute("SELECT * FROM expenses WHERE id = %s AND user_id = %s", 
                   (expense_id, session['user_id']))
    expense = cursor.fetchone()
    db.close()
    return render_template('update_expense.html', expense=expense)


# Delete Expense
@app.route('/delete_expense/<int:expense_id>')
def delete_expense(expense_id):
    if 'user_id' not in session:
        flash("Please log in to delete expenses.", "error")
        return redirect(url_for('login'))

    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM expenses WHERE id = %s AND user_id = %s", 
                   (expense_id, session['user_id']))
    db.commit()
    db.close()

    flash("Expense deleted successfully!", "success")
    return redirect(url_for('dashboard'))

#comapare
@app.route('/compare_expenses', methods=['GET', 'POST'])
def compare_expenses():
    if 'user_id' not in session:
        flash("Please log in to compare expenses.", "error")
        return redirect(url_for('login'))

    labels = []
    data1 = []
    data2 = []
    month1 = month2 = None  # Initialize months

    if request.method == 'POST':
        month1_full = request.form.get('month1')  # Example: "2024-01"
        month2_full = request.form.get('month2')  # Example: "2024-02"

        if not month1_full or not month2_full:
            flash("Please select two months.", "error")
            return redirect(url_for('compare_expenses'))

        # Extract year and month separately
        year1, month1 = month1_full.split('-')
        year2, month2 = month2_full.split('-')

        db = get_db_connection()
        cursor = db.cursor()

        # Fetch category-wise expense sums for first selected month
        cursor.execute("""
            SELECT category, SUM(amount) 
            FROM expenses 
            WHERE user_id = %s AND MONTH(date) = %s AND YEAR(date) = %s
            GROUP BY category
        """, (session['user_id'], month1, year1))
        expenses1 = cursor.fetchall()

        # Fetch category-wise expense sums for second selected month
        cursor.execute("""
            SELECT category, SUM(amount) 
            FROM expenses 
            WHERE user_id = %s AND MONTH(date) = %s AND YEAR(date) = %s
            GROUP BY category
        """, (session['user_id'], month2, year2))
        expenses2 = cursor.fetchall()

        db.close()

        # Prepare data for chart
        category_dict = {}

        for category, amount in expenses1:
            category_dict[category] = [amount, 0]  # First month amount, second month default 0

        for category, amount in expenses2:
            if category in category_dict:
                category_dict[category][1] = amount  # Update second month amount
            else:
                category_dict[category] = [0, amount]  # First month default 0, second month amount

        # Extract labels and values
        labels = list(category_dict.keys())
        data1 = [values[0] for values in category_dict.values()]
        data2 = [values[1] for values in category_dict.values()]

    return render_template('compare_expenses.html', labels=labels, data1=data1, data2=data2, month1=month1, month2=month2)




if __name__ == '__main__':
    app.run(debug=True)













