import os
from werkzeug.security import generate_password_hash
from utils.extensions import db
from models.user import User
from main import app

def seed_admin():
    email = os.environ.get("ADMIN_EMAIL")
    password = os.environ.get("ADMIN_PASSWORD")
    name = os.environ.get("ADMIN_NAME", "Admin")

    if not email or not password:
        print("ADMIN_EMAIL / ADMIN_PASSWORD not set. Skipping admin seed.")
        return

    with app.app_context():
        existing = db.session.scalar(db.select(User).where(User.email == email))
        if existing:
            # Zorg dat hij admin is (handig als user al bestaat)
            if hasattr(existing, "is_admin") and not getattr(existing, "is_admin"):
                setattr(existing, "is_admin", True)
                db.session.commit()
            print("Admin already exists. Skipping.")
            return

        admin = User(
            name=name,
            email=email,
            password=generate_password_hash(password, method="pbkdf2:sha256", salt_length=8),
        )
        if hasattr(admin, "is_admin"):
            admin.is_admin = True

        db.session.add(admin)
        db.session.commit()
        print("Admin created.")

if __name__ == "__main__":
    seed_admin()
