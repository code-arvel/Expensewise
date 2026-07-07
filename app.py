from flask import Flask, render_template, request, redirect, url_for, session
from models.database import users_collection, expenses_collection, budgets_collection
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from bson.objectid import ObjectId

app = Flask(__name__)

app.secret_key = "expensewise_secret_key"

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_id = session['user_id']

    budget = budgets_collection.find_one({ 'user_id': user_id })

    budget_amount = (budget['budget_amount'] if budget else 0)

    expenses = list(expenses_collection.find({ 'user_id': user_id }))
    category_totals = {}
    for expense in expenses:
        category = expense['category']
        amount = expense['amount']

        if category not in category_totals:
            category_totals[category] = 0

        category_totals[category] += amount


    total_expenses = sum(expense['amount'] for expense in expenses)


    remaining_balance = (budget_amount - total_expenses)

    total_transactions = len(expenses)

    recent_expenses = list(expenses_collection.find({'user_id': user_id }).sort('_id', -1).limit(5))
    
    return render_template(
        'dashboard.html',
        budget_amount=budget_amount,
        total_expenses=total_expenses,
        remaining_balance=remaining_balance,
        total_transactions=total_transactions,
        recent_expenses=recent_expenses,
        category_totals=category_totals,

        firstname=session['firstname']
    )


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        email = request.form['email']

        existing_user = users_collection.find_one({"email": email})
        
        if existing_user:
            return "Email already exists"
        
        user = {
            'firstname': request.form['firstname'],
            'lastname': request.form['lastname'],
            'email': request.form['email'],
            'password': generate_password_hash(request.form['password']),
            'reg_number': request.form['regnumber']
        }

        users_collection.insert_one(user)

        return redirect(url_for('login'))
    

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users_collection.find_one({"email": email})

        if user and check_password_hash(user['password'], password):
            session['user_id'] = str(user['_id'])
            session['firstname'] = user['firstname']

            return redirect(url_for('dashboard'))
        
        return 'Invalid email or password'
    
    return render_template('login.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/profile')
def profile():
    user = {
        "firstname": "Jack",
        "lastname": "Darzel",
        "email": "jack@example.com",
        "reg_number": "MOUAU/CMP/22/116558"
    }

    return render_template(
        'profile.html',
        user=user
    )


@app.route('/add-expense', methods=['GET', 'POST'])
def add_expense():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        expense = {
            'user_id': session['user_id'],
            'amount': float(
                request.form['amount']
            ),
            'category': request.form['category'],
            'description': request.form['description'],
            'expense_date': request.form['expense_date'],
            'created_at': datetime.utcnow()
        }

        expenses_collection.insert_one(expense)
        return redirect(url_for('expense_history'))
    
    return render_template('add_expense.html')

@app.route('/delete-expense/<expense_id>')
def delete_expense(expense_id):

    expenses_collection.delete_one({ '_id': ObjectId(expense_id) })

    return redirect(url_for('expense_history'))


@app.route('/budget', methods=['GET', 'POST'])
def budget():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        budget_amount = float(request.form['budget_amount'])
        budgets_collection.update_one(
            {'user_id': session['user_id']},
            {'$set': {
                'budget_amount': budget_amount
            }},
            upsert=True
        )

        return redirect(url_for('budget'))
    
    budget = budgets_collection.find_one({'user_id': session['user_id']})
   
    expenses = list(expenses_collection.find({'user_id': session["user_id"]}))
    
    total_expenses = sum(
        expense['amount']
        for expense in expenses
    )

    budget_amount = (
        budget['budget_amount']
        if budget
        else 0
    )
   
    remaining_balance = (
        budget_amount - total_expenses
    )

        #for progress bar
    if budget_amount > 0:
        usage_percentage = (total_expenses / budget_amount) * 100
    else:
        usage_percentage = 0

    usage_percentage = min(usage_percentage, 100)

    if usage_percentage >= 90:
        progress_class = "danger"
    elif usage_percentage >= 70:
        progress_class = "warning"
    else:
        progress_class = ""


    return render_template(
        'budgets.html',
        budget_amount=budget_amount,
        total_expenses = total_expenses,
        remaining_balance=remaining_balance,
        usage_percentage = usage_percentage,
        progress_class=progress_class,
    )

@app.route('/expense')
def expenses():
    return render_template('expenses.html')

@app.route('/reports')
def reports():
    return render_template('reports.html')


@app.route('/logout')
def logout():
    session.clear()

    return redirect(
        url_for('login')
    )


@app.route('/expense history')
def expense_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    expenses = list(
        expenses_collection.find({
            'user_id': session['user_id']
        }).sort('_id', -1)
    )


    return render_template('expense_history.html', expenses=expenses)



if __name__ == "__main__":
    app.run(debug=True)