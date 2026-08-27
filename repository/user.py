from sqlalchemy.orm import Session

from app.models.user import User


def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_id(
    db: Session,
    user_id: int
) -> User | None:

    return (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )


def get_user_by_username(
    db: Session,
    username: str
) -> User | None:

    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )


def get_all_users(
    db: Session
) -> list[User]:

    return db.query(User).all()