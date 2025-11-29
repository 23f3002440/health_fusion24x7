from main import app
from flask import render_template, request, session, flash, redirect, url_for
from controller.models import User, Role
from controller.database import db


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'user_email' in session:
            return redirect(url_for('home'))
        return render_template('Login.html')

    # POST
    email = request.form.get('email', None)
    password = request.form.get('password', None)

    if not email or not password:
        flash("Email and Password are required")
        return render_template('Login.html')

    if '@' not in email:
        flash("Invalid email address")
        return render_template('Login.html')

    user = User.query.filter_by(user_email=email).first()
    if not user:
        flash("User does not exist")
        return render_template('Login.html')

    if not user.check_password(password):
        flash("Incorrect password")
        return render_template('Login.html')

    session['user_email'] = user.user_email
    session['user_role'] = [role.name for role in user.roles]

    flash("Login successful")
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    if 'user_email' not in session:
        flash("You are not logged in")
        return redirect(url_for('login'))

    session.pop('user_email', None)
    session.pop('user_role', None)

    flash("You are logged out successfully")
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    # POST
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    confirm_password = request.form.get('confirm_password', None)
    user_name = request.form.get('user_name', None)
    role = request.form.get('role', None)

    # data validation
    if not email or not password or not confirm_password or not user_name or not role:
        flash("All fields are required")
        return render_template('register.html')

    if '@' not in email:
        flash("Invalid email address")
        return render_template('register.html')

    if password != confirm_password:
        flash("Passwords do not match")
        return render_template('register.html')

    if len(password) < 8:
        flash("Password must be at least 8 characters long")
        return render_template('register.html')

    user = User.query.filter_by(user_email=email).first()
    if user:
        flash("User already exists")
        return render_template('register.html')

    role_obj = Role.query.filter_by(name=role).first()
    if not role_obj:
        flash("Invalid role selected")
        return render_template('register.html')

    # create user
    user = User(
        user_email=email,
        password=password,
        user_name=user_name
    )

    db.session.add(user)
    db.session.commit()

    # attach role
    user.roles.append(role_obj)
    db.session.commit()

    flash("Registration successful. Please log in.")
    return redirect(url_for('login'))

