from sqlmodel import SQLModel, Column, Field, String, Text
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    # ✅ FIX: "user" is a reserved word in MySQL — set an explicit table name
    __tablename__ = "amana_user"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column(String(255), unique=True, nullable=False))
    password_hash: str = Field(sa_column=Column(String(255), nullable=False))
    role: str = Field(sa_column=Column(String(20), nullable=False))
    full_name: str = Field(sa_column=Column(String(100), nullable=False))

    def __repr__(self):
        return f"User(id={self.id}, email='{self.email}', role='{self.role}')"


class Student(SQLModel, table=True):
    __tablename__ = "student"

    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str = Field(sa_column=Column(String(100), nullable=False))
    prenom: str = Field(sa_column=Column(String(100), nullable=False))
    email: str = Field(sa_column=Column(String(150), unique=True, index=True, nullable=False))
    classe: Optional[str] = Field(default=None, sa_column=Column(String(50)))

    def __repr__(self):
        return f"Student(id={self.id}, nom='{self.nom}', prenom='{self.prenom}')"


class Act(SQLModel, table=True):
    __tablename__ = "act"

    id: Optional[int] = Field(default=None, primary_key=True)
    titre: str = Field(sa_column=Column(String(100), nullable=False))
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    type_action: str = Field(sa_column=Column(String(50), nullable=False))
    # ✅ FIX: Use timezone-aware UTC now for new Python versions
    date_publication: datetime = Field(default_factory=datetime.utcnow)
    student_id: Optional[int] = Field(default=None, foreign_key="student.id")

    def __repr__(self):
        return f"Act(id={self.id}, titre='{self.titre}', type='{self.type_action}')"