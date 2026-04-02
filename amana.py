import mysql.connector # type: ignore
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel import Column, SQLModel, Field, String, Text
from typing import Optional
from datetime import datetime

# Correction 1: Variable DATABASE_URL (était DATABASE_URL au lieu de database_url)
database_url = "mysql+pymysql://root:root@localhost/amana_db"
engine = create_engine(database_url, echo=True)

# Correction 2: Indentation de get_session
def get_session():
    with Session(engine) as session:
        yield session

# Correction 3: Classe users → User (convention PascalCase)
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(sa_column=Column(String(255), unique=True))  # String(25) → String(255)
    password_hash: str = Field(sa_column=Column(String(255)))  # String(50) → String(255)
    role: str = Field(sa_column=Column(String(20)))
    full_name: str = Field(sa_column=Column(String(100)))
    
    def __repr__(self):
        return f"User(id={self.id}, email='{self.email}', role='{self.role}', full_name='{self.full_name}')"

# --- Table des Étudiants ---
class Student(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str = Field(sa_column=Column(String(100), nullable=False))
    prenom: str = Field(sa_column=Column(String(100), nullable=False))
    email: str = Field(sa_column=Column(String(150), unique=True, index=True))
    classe: Optional[str] = Field(default=None, sa_column=Column(String(50)))

# --- Table des Activités (Acts) ---
class Act(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titre: str = Field(sa_column=Column(String(100), nullable=False))
    description: Optional[str] = Field(default=None, sa_column=Column(Text))
    type_action: str = Field(sa_column=Column(String(50)))
    date_publication: datetime = Field(default_factory=datetime.utcnow)
    student_id: Optional[int] = Field(default=None, foreign_key="student.id")

# --- Fonctions CRUD manquantes ---
def create_user(session: Session, email: str, password_hash: str, role: str, full_name: str) -> User:
    user = User(email=email, password_hash=password_hash, role=role, full_name=full_name)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.query(User).filter(User.email == email).first()

def create_student(session: Session, nom: str, prenom: str, email: str, classe: str) -> Student:
    student = Student(nom=nom, prenom=prenom, email=email, classe=classe)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

def get_student_by_id(session: Session, student_id: int) -> Optional[Student]:
    return session.query(Student).filter(Student.id == student_id).first()

def create_act(session: Session, titre: str, description: str, type_action: str, student_id: int) -> Act:
    act = Act(titre=titre, description=description, type_action=type_action, student_id=student_id)
    session.add(act)
    session.commit()
    session.refresh(act)
    return act

def get_acts_by_student(session: Session, student_id: int) -> list[Act]:
    return session.query(Act).filter(Act.student_id == student_id).all()