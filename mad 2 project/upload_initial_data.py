
from main import app
from application.sec import datastore
from application.model import db, Role
from flask_security import hash_password
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()
    
    # Create roles if they don't exist
    if not datastore.find_role("admin"):
        datastore.create_role(name="admin", description="User is an admin")
    
    db.session.commit()
    
    # Create users if they don't exist
    if not datastore.find_user(email="admin@email.com"):
        datastore.create_user(username="lakshya",Name = "Lakshya",
            email="lakshya@email.com", password=generate_password_hash("admin"), roles=["admin"]
        )
    db.session.commit()
