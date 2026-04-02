import mysql.connector # type: ignore
from sqlmodel import SQLModel, create_engine, Session
from sqlmodel import Column, SQLModel, Field, String, Text
from typing import Optional
from datetime import datetime

database_url = "mysql+pymysql://root:root@localhost/amana_db"
engine = create_engine(database_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session

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
# ...existing code...

# --- Fonctions CRUD complètes ---

# ===== USERS =====
def create_user(session: Session, email: str, password_hash: str, role: str, full_name: str) -> User:
    user = User(email=email, password_hash=password_hash, role=role, full_name=full_name)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    return session.query(User).filter(User.email == email).first()

def get_user_by_id(session: Session, user_id: int) -> Optional[User]:
    return session.query(User).filter(User.id == user_id).first()

def get_all_users(session: Session) -> list[User]:
    return session.query(User).all()

def update_user(session: Session, user_id: int, **kwargs) -> Optional[User]:
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in kwargs.items():
            setattr(user, key, value)
        session.commit()
        session.refresh(user)
    return user

def delete_user(session: Session, user_id: int) -> bool:
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
        return True
    return False

# ===== STUDENTS =====
def create_student(session: Session, nom: str, prenom: str, email: str, classe: str) -> Student:
    student = Student(nom=nom, prenom=prenom, email=email, classe=classe)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

def get_student_by_id(session: Session, student_id: int) -> Optional[Student]:
    return session.query(Student).filter(Student.id == student_id).first()

def get_student_by_email(session: Session, email: str) -> Optional[Student]:
    return session.query(Student).filter(Student.email == email).first()

def get_all_students(session: Session) -> list[Student]:
    return session.query(Student).all()

def get_students_by_class(session: Session, classe: str) -> list[Student]:
    return session.query(Student).filter(Student.classe == classe).all()

def update_student(session: Session, student_id: int, **kwargs) -> Optional[Student]:
    student = session.query(Student).filter(Student.id == student_id).first()
    if student:
        for key, value in kwargs.items():
            setattr(student, key, value)
        session.commit()
        session.refresh(student)
    return student

def delete_student(session: Session, student_id: int) -> bool:
    student = session.query(Student).filter(Student.id == student_id).first()
    if student:
        session.delete(student)
        session.commit()
        return True
    return False

# ===== ACTS =====
def create_act(session: Session, titre: str, description: str, type_action: str, student_id: int) -> Act:
    act = Act(titre=titre, description=description, type_action=type_action, student_id=student_id)
    session.add(act)
    session.commit()
    session.refresh(act)
    return act

def get_act_by_id(session: Session, act_id: int) -> Optional[Act]:
    return session.query(Act).filter(Act.id == act_id).first()

def get_acts_by_student(session: Session, student_id: int) -> list[Act]:
    return session.query(Act).filter(Act.student_id == student_id).all()

def get_all_acts(session: Session) -> list[Act]:
    return session.query(Act).all()

def get_acts_by_type(session: Session, type_action: str) -> list[Act]:
    return session.query(Act).filter(Act.type_action == type_action).all()

def update_act(session: Session, act_id: int, **kwargs) -> Optional[Act]:
    act = session.query(Act).filter(Act.id == act_id).first()
    if act:
        for key, value in kwargs.items():
            setattr(act, key, value)
        session.commit()
        session.refresh(act)
    return act

def delete_act(session: Session, act_id: int) -> bool:
    act = session.query(Act).filter(Act.id == act_id).first()
    if act:
        session.delete(act)
        session.commit()
        return True
    return False