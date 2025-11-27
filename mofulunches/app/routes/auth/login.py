from . import auth
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import check_password_hash
from app.models.models import User

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('dashboard.dashboard_home'))
        else:
            flash('Correo electrónico o contraseña inválidos.', 'danger')
    return render_template('auth/login.html')
