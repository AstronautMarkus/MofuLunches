from . import dashboard
from flask import render_template

@dashboard.route('/dashboard')
def dashboard_home():
    return render_template('dashboard/admin.html')