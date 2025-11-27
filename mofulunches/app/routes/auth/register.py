from . import auth
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from app import db
from app.models.models import User, Role

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')

        employee_role = Role.query.filter_by(slug='employee').first()
        if not employee_role:
            flash('Rol de empleado no encontrado.', 'danger')
            return render_template('auth/register.html')

        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=generate_password_hash(password),
            role=employee_role
        )
        db.session.add(user)
        db.session.commit()
        flash('Usuario registrado exitosamente.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

