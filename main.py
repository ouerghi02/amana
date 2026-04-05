from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, select
from database import engine, get_session
from models import User, Student, Act
import hashlib

app = FastAPI(title="Amana API", version="1.0.0")

# ✅ FIX 1: Add CORS so the frontend browser can call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # In production, replace "*" with your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ FIX 2: Create tables on startup (runs once when server starts)
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


# ─────────────────────────────────────────
#  USERS
# ─────────────────────────────────────────

@app.post("/users", response_model=User, tags=["Users"])
def create_user(user: User, session: Session = Depends(get_session)):
    # ✅ FIX 3: Hash the password before saving (never store plain text)
    user.password_hash = hashlib.sha256(user.password_hash.encode()).hexdigest()
    session.add(user)
    try:
        session.commit()
        session.refresh(user)
        return user
    except Exception:
        session.rollback()
        raise HTTPException(status_code=400, detail="Email already exists or invalid data")

@app.get("/users", tags=["Users"])
def read_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()


# ─────────────────────────────────────────
#  STUDENTS
# ─────────────────────────────────────────

# ✅ FIX 4: Only ONE definition of each route (removed duplicates)
@app.post("/students", response_model=Student, tags=["Students"])
def create_student(student: Student, session: Session = Depends(get_session)):
    session.add(student)
    try:
        session.commit()
        session.refresh(student)
        return student
    except Exception:
        session.rollback()
        raise HTTPException(status_code=400, detail="Could not create student. Email may already exist.")

@app.get("/students", tags=["Students"])
def read_students(session: Session = Depends(get_session)):
    # ✅ FIX 5: Use session.exec() consistently (not session.query())
    return session.exec(select(Student)).all()

@app.get("/students/{student_id}", tags=["Students"])
def read_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@app.put("/students/{student_id}", tags=["Students"])
def update_student(student_id: int, new_data: Student, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.nom = new_data.nom
    student.prenom = new_data.prenom
    student.email = new_data.email
    student.classe = new_data.classe
    session.add(student)
    session.commit()
    session.refresh(student)
    return student

@app.delete("/students/{student_id}", tags=["Students"])
def delete_student(student_id: int, session: Session = Depends(get_session)):
    student = session.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    session.delete(student)
    session.commit()
    return {"message": "Student deleted successfully"}


# ─────────────────────────────────────────
#  ACTS (Activities)
# ─────────────────────────────────────────

@app.post("/acts", response_model=Act, tags=["Acts"])
def create_act(act: Act, session: Session = Depends(get_session)):
    # Verify student exists before creating the act
    if act.student_id:
        student = session.get(Student, act.student_id)
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")
    session.add(act)
    try:
        session.commit()
        session.refresh(act)
        return act
    except Exception:
        session.rollback()
        raise HTTPException(status_code=500, detail="Could not create activity")

@app.get("/acts", tags=["Acts"])
def read_acts(session: Session = Depends(get_session)):
    return session.exec(select(Act)).all()

@app.get("/acts/{act_id}", tags=["Acts"])
def read_act(act_id: int, session: Session = Depends(get_session)):
    act = session.get(Act, act_id)
    if not act:
        raise HTTPException(status_code=404, detail="Act not found")
    return act

# ✅ FIX 6: Added missing GET acts by student (was using old session.query API)
@app.get("/students/{student_id}/acts", response_model=list[Act], tags=["Acts"])
def get_acts_by_student(student_id: int, session: Session = Depends(get_session)):
    acts = session.exec(select(Act).where(Act.student_id == student_id)).all()
    return acts

@app.put("/acts/{act_id}", tags=["Acts"])
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

@app.delete("/acts/{act_id}", tags=["Acts"])
def delete_act(act_id: int, session: Session = Depends(get_session)):
    act = session.get(Act, act_id)
    if not act:
        raise HTTPException(status_code=404, detail="Act not found")
    session.delete(act)
    session.commit()
    return {"message": "Act deleted successfully"}