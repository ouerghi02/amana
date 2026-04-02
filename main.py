from fastapi import FastAPI, Depends # type: ignore
from database import get_session # pyright: ignore[reportMissingImports]
from sqlmodel import SQLModel, Session
from models import  User, Student, Act # type: ignore
from fastapi import HTTPException, Depends
from sqlmodel import select
app = FastAPI()
@app.post("/users", response_model=User)
def create_user(user: User, session: Session = Depends(get_session)):
    # Note: En production, il faudra hacher le mot de passe ici
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
@app.post("/students", response_model=Student)
def create_student(student: Student, session: Session = Depends(get_session)):
    session.add(student)
    session.commit()
    session.refresh(student)
    return student
@app.post("/acts", response_model=Act)
def create_act(act: Act, session: Session = Depends(get_session)):
    # Optionnel: Vérifier si l'étudiant existe avant de créer l'acte
    session.add(act)
    session.commit()
    session.refresh(act)
    return act
@app.get("/students/{student_id}/acts", response_model=list[Act])
def get_acts_by_student(student_id: int, session: Session = Depends(get_session)):
    acts = session.query(Act).filter(Act.student_id == student_id).all()
    return acts
@app.get("/students")
def read_students(session: Session = Depends(get_session)):
    students = session.query(Student).all()
    return students


# CREATE
@app.post("/students", response_model=Student)
def create_student(student: Student, session: Session = Depends(get_session)):
    session.add(student)
    try:
        session.commit()
        session.refresh(student)
        return student
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Impossible d'ajouter l'étudiant")

# READ ALL
@app.get("/students")
def read_students(session: Session = Depends(get_session)):
    return session.exec(select(Student)).all()

# READ ONE
@app.get("/students/{student_id}")
def read_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# DELETE
@app.delete("/students/{student_id}")
def delete_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    session.delete(student)
    session.commit()
    return {"message": "Student deleted"}
# CREATE
@app.post("/acts", response_model=Act)
def create_act(act: Act, session: Session = Depends(get_session)):
    session.add(act)
    try:
        session.commit()
        session.refresh(act)
        return act
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Erreur lors de la création de l'activité")

# READ ALL
@app.get("/acts")
def read_acts(session: Session = Depends(get_session)):
    return session.exec(select(Act)).all()

# UPDATE
@app.put("/acts/{act_id}")
def update_act(act_id: int, new_data: Act, session: Session = Depends(get_session)):
    act = session.get(Act, act_id)
    if not act:
        raise HTTPException(status_code=404, detail="Act not found")
    
    act.titre = new_data.titre
    act.description = new_data.description
    act.type_action = new_data.type_action
    
    session.add(act)
    session.commit()
    session.refresh(act)
    return act