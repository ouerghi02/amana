from sqlmodel import SQLModel, Column, Field, String, Text
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column(String(255), unique=True))  
    password_hash: str = Field(sa_column=Column(String(255)))  
    role: str = Field(sa_column=Column(String(20)))
    full_name: str = Field(sa_column=Column(String(100)))
    
    def __repr__(self):
        return f"User(id={self.id}, email='{self.email}', role='{self.role}', full_name='{self.full_name}')"


class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str = Field(sa_column=Column(String(100), nullable=False))
    prenom: str = Field(sa_column=Column(String(100), nullable=False))
    email: str = Field(sa_column=Column(String(150), unique=True, index=True))
    classe: Optional[str] = Field(default=None, sa_column=Column(String(50)))


class Act(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titre: str = Field(sa_column=Column(String(100), nullable=False))
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    type_action: str = Field(sa_column=Column(String(50)))
    date_publication: datetime = Field(default_factory=datetime.utcnow)
    student_id: Optional[int] = Field(default=None, foreign_key="student.id")
