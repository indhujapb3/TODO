from getpass import getpass

from database import SessionLocal
from models.user import User
from models.task import Task
from security.password import hash_password

def create_admin():
    db = SessionLocal()

    try:
        # Check whether an admin already exists
        existing_admin = (
            db.query(User)
            .filter(User.role == "admin")
            .first()
        )

        if existing_admin:
            print("Admin user already exists.")
            return

        # Get admin credentials
        username = input("Enter admin username: ")
        password = getpass("Enter admin password: ")

        # Check whether username already exists
        existing_user = (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

        if existing_user:
            print("Username already exists.")
            return

        # Hash password
        hashed_password = hash_password(password)

        # Create admin user
        admin = User(
            username=username,
            password=hashed_password,
            role="admin"
        )

        # Save to database
        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("Admin user created successfully.")
        print(f"Admin username: {admin.username}")

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()