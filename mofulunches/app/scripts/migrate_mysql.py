"""
Script to initialize the MySQL database with Flask-SQLAlchemy.
This script creates the necessary tables.
"""

import os
import sys

project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from app import create_app
from app.models.models import db

def init_database():
    """Initialize the database by creating tables."""
    
    app = create_app()
    
    with app.app_context():
        print("Creating tables...")
        db.create_all()
        print("Tables created successfully")
        print("Database initialized completely")

def create_roles():
    """Create default roles in the database."""
    from app.models.models import Role
    from app.models.models import db

    roles = [
        {"name": "Administrador", "slug": "admin", "description": "Administradores del sistema, encargados de la gestión completa y supervisión de todas las operaciones."},
        {"name": "Cocineros", "slug": "cook", "description": "Responsables de la preparación de los almuerzos y la gestión de los menús diarios."},
        {"name": "Empleado", "slug": "employee", "description": "Empleados de la empresa que utilizarán el sistema para gestionar sus almeuerzos y datos relacionados."}
    ]

    for role_data in roles:
        existing_role = Role.query.filter_by(name=role_data["name"]).first()
        if not existing_role:
            role = Role(
                name=role_data["name"],
                slug=role_data["slug"],
                description=role_data["description"]
            )
            db.session.add(role)
    
    db.session.commit()
    print("Default roles created")

def reset_database(auto_confirm=False):
    """Delete all tables and recreate them."""
    
    app = create_app()
    
    with app.app_context():
        print("WARNING: This will delete all existing tables and data.")
        if auto_confirm:
            confirm = "yes"
        else:
            confirm = input("Are you sure? (yes/no): ")
        
        if confirm.lower() in ['yes', 'y', 'sí', 'si']:
            print("Deleting tables...")
            db.drop_all()
            print("Tables deleted")
            init_database()
            create_roles()
        else:
            print("Operation cancelled")

if __name__ == "__main__":
    valid_flags = ["--reset", "--fresh"]
    if len(sys.argv) > 1:
        flag = sys.argv[1]
        if flag == "--reset":
            reset_database()
        elif flag == "--fresh":
            reset_database(auto_confirm=True)
        else:
            print(f"Invalid flag: {flag}")
            print("Valid flags are:")
            for f in valid_flags:
                print(f"  {f}")
            print("No action was performed.")
    else:
        init_database()