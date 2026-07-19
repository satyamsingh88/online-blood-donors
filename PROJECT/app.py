from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import re

app = Flask(__name__)
app.secret_key = "blood_donation_secret"

# MySQL Configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'SA88@kumar'
app.config['MYSQL_DB'] = 'blood_donor_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# ---------------- HOME ----------------
@app.route('/')
def index():
    return render_template('index.html')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':

        name = request.form['name']
        age = request.form['age']
        phone = request.form['phone']
        email = request.form['email']
        address = request.form['address']

        # ✅ NAME (only letters)
        if not re.match(r'^[A-Za-z\s]{3,}$', name):
            flash("Name must contain only letters ❌")
            return redirect(url_for('register'))

        # ✅ AGE
        if not age.isdigit() or int(age) < 18 or int(age) > 65:
            flash("Age must be between 18 and 65 ❌")
            return redirect(url_for('register'))

        # ✅ PHONE
        if not phone.isdigit() or len(phone) != 10:
            flash("Phone must be 10 digits ❌")
            return redirect(url_for('register'))

        # ✅ EMAIL
        if not re.match(r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$', email):
            flash("Invalid Email ❌")
            return redirect(url_for('register'))

        # ✅ ADDRESS (ULTRA STRICT)
        # Format: Flat 12, Area, City 411001
        if not re.match(r'^.*\d{1,5}.*[A-Za-z]+.*\d{6}$', address):
            flash("Enter full address like: Flat 12, MG Road, Pune 411001 ❌")
            return redirect(url_for('register'))

        if len(address) < 15:
            flash("Address too short ❌")
            return redirect(url_for('register'))

        cur = mysql.connection.cursor()

        # ✅ Duplicate phone check
        cur.execute("SELECT * FROM donors WHERE phone=%s", [phone])
        if cur.fetchone():
            flash("Phone already registered ❌")
            return redirect(url_for('register'))

        # ✅ INSERT
        cur.execute("""
            INSERT INTO donors(name, age, gender, blood_group, phone, email, address)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            name,
            age,
            request.form['gender'],
            request.form['blood_group'],
            phone,
            email,
            address
        ))

        mysql.connection.commit()
        flash("Registration Successful! ✅")
        return redirect(url_for('index'))

    return render_template('register.html')

# ---------------- SEARCH ----------------
@app.route('/search', methods=['GET', 'POST'])
def search():
    donors = []
    if request.method == 'POST':
        bg = request.form['blood_group']
        loc = request.form['location']
        cur = mysql.connection.cursor()
        cur.execute(
            "SELECT * FROM donors WHERE blood_group LIKE %s AND address LIKE %s",
            ('%' + bg + '%', '%' + loc + '%')
        )
        donors = cur.fetchall()
    return render_template('search.html', donors=donors)

# ---------------- REQUEST BLOOD ----------------
@app.route('/request_blood', methods=['GET', 'POST'])
def request_blood():
    if request.method == 'POST':

        name = request.form['patient_name']
        location = request.form['location']
        contact = request.form['contact']

        # ✅ NAME
        if not re.match(r'^[A-Za-z\s]{3,}$', name):
            flash("Invalid Name ❌")
            return redirect(url_for('request_blood'))

        # ✅ ADDRESS (ULTRA STRICT)
        if not re.match(r'^.*\d{1,5}.*[A-Za-z]+.*\d{6}$', location):
            flash("Enter full address like: Flat 12, MG Road, Pune 411001 ❌")
            return redirect(url_for('request_blood'))

        if len(location) < 15:
            flash("Address too short ❌")
            return redirect(url_for('request_blood'))

        # ✅ CONTACT
        if not contact.isdigit() or len(contact) != 10:
            flash("Invalid phone number ❌")
            return redirect(url_for('request_blood'))

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO requests(patient_name, blood_group, location, contact, needed_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            name,
            request.form['blood_group'],
            location,
            contact,
            request.form['needed_date']
        ))

        mysql.connection.commit()
        flash("Blood request posted successfully ✅")
        return redirect(url_for('index'))

    return render_template('request.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (user, pw))
        admin = cur.fetchone()

        if admin:
            session['logged_in'] = True
            return redirect(url_for('admin'))

        flash("Invalid Credentials ❌")

    return render_template('login.html')

# ---------------- ADMIN ----------------
@app.route('/admin')
def admin():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM donors")
    donors = cur.fetchall()

    cur.execute("SELECT * FROM requests")
    requests = cur.fetchall()

    return render_template('admin.html', donors=donors, requests=requests)

# ---------------- DELETE ----------------
@app.route('/delete_donor/<int:id>')
def delete_donor(id):
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM donors WHERE id=%s", [id])
    mysql.connection.commit()

    return redirect(url_for('admin'))

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)