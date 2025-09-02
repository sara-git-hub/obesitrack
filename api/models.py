from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import String, Text, JSON, ForeignKey, func
import uuid


class Base(DeclarativeBase):
    pass


def uuid4_str():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid4_str)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[str] = mapped_column(server_default=func.now())

    predictions: Mapped[list["Prediction"]] = relationship(back_populates="user")


class Prediction(Base):
    __tablename__ = "predictions"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=uuid4_str)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id"))
    payload_json: Mapped[dict] = mapped_column(JSON)
    predicted_class: Mapped[str] = mapped_column(String(100))
    proba: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[str] = mapped_column(server_default=func.now())

    user: Mapped[User] = relationship(back_populates="predictions")