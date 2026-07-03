from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/login')
def login():
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
    return 'hello world'


@app.route('/expense history')
def expense_history():
    return render_template('expense_history.html')



if __name__ == "__main__":
    app.run(debug=True)