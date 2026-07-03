from flask import Flask, render_template, request, redirect, url_for, session
from models.database import users_collection
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)

app.secret_key = "expensewise_secret_key"

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', firstname=session['firstname'])


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


@app.route('/add-expense')
def add_expense():
    return render_template('add_expense.html')


@app.route('/expenses')
def expenses():
    return "<h1>Expense History Page</h1>"


@app.route('/budget')
def budget():
    return render_template('budgets.html')


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
    return render_template('expense_history.html')



if __name__ == "__main__":
    app.run(debug=True)