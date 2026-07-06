from fastapi import FastAPI, Depends, HTTPException, status, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional, List
from jose import JWTError

from database import get_db, create_tables
from models import Course, Department, Student, Enrollment, User
from schemas import (CourseCreate, CourseUpdate, CourseResponse,
                     DepartmentCreate, DepartmentResponse,
                     StudentCreate, StudentResponse,
                     EnrollmentCreate, EnrollmentResponse,
                     UserCreate, UserResponse, Token)
from security import get_password_hash, verify_password, create_access_token, decode_token

# API versioning: URL versioning (/v1/) is simple and visible.
# Alternative: header-based versioning (Accept: application/vnd.api+json;version=1)
# keeps URLs clean but is harder to test in a browser.

app = FastAPI(
    title="Course Management API",
    description="A RESTful API for managing courses, students and enrollments",
    version="1.0",
    contact={"name": "Raghav", "email": "raghavnagalingaayyanar@gmail.com"}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/")
bearer_scheme = HTTPBearer()

@app.on_event("startup")
def startup():
    create_tables()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme), db: Session = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

def send_confirmation_email(student_email: str):
    print(f"Sending confirmation to {student_email}")

# ── Root ──────────────────────────────────────────────────────────────────────
@app.get("/")
def root():
    return {"message": "API running"}

# ── Courses ───────────────────────────────────────────────────────────────────
@app.get("/api/v1/courses/", response_model=List[CourseResponse], tags=["Courses"],
         summary="List all courses", response_description="Paginated list of courses")
def get_courses(skip: int = 0, limit: int = 10,
                department_id: Optional[int] = None,
                search: Optional[str] = None,
                db: Session = Depends(get_db)):
    query = db.query(Course)
    if department_id:
        query = query.filter(Course.department_id == department_id)
    if search:
        query = query.filter(
            (Course.name.ilike(f"%{search}%")) | (Course.code.ilike(f"%{search}%"))
        )
    total = query.count()
    results = query.offset(skip).limit(limit).all()
    return results

@app.post("/api/v1/courses/", response_model=CourseResponse,
          status_code=status.HTTP_201_CREATED, tags=["Courses"],
          summary="Create a new course")
def create_course(course: CourseCreate, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course

@app.get("/api/v1/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail={"error": {"code": "NOT_FOUND", "message": f"Course with id {course_id} does not exist", "field": None}})
    return course

@app.put("/api/v1/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
def update_course(course_id: int, course_data: CourseCreate,
                  db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in course_data.model_dump().items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course

@app.patch("/api/v1/courses/{course_id}", response_model=CourseResponse, tags=["Courses"])
def partial_update_course(course_id: int, course_data: CourseUpdate,
                           db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    for key, value in course_data.model_dump(exclude_unset=True).items():
        setattr(course, key, value)
    db.commit()
    db.refresh(course)
    return course

@app.delete("/api/v1/courses/{course_id}",
            status_code=status.HTTP_204_NO_CONTENT, tags=["Courses"])
def delete_course(course_id: int, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    db.delete(course)
    db.commit()

@app.get("/api/v1/courses/{course_id}/students/",
         response_model=List[StudentResponse], tags=["Courses"])
def get_course_students(course_id: int, db: Session = Depends(get_db)):
    enrollments = db.query(Enrollment).filter(Enrollment.course_id == course_id).all()
    return [e.student for e in enrollments]

# ── Students ──────────────────────────────────────────────────────────────────
@app.get("/api/v1/students/", response_model=List[StudentResponse], tags=["Students"])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@app.post("/api/v1/students/", response_model=StudentResponse,
          status_code=status.HTTP_201_CREATED, tags=["Students"])
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

# ── Enrollments ───────────────────────────────────────────────────────────────
@app.post("/api/v1/enrollments/", response_model=EnrollmentResponse,
          status_code=status.HTTP_201_CREATED, tags=["Enrollments"])
def create_enrollment(enrollment: EnrollmentCreate,
                      background_tasks: BackgroundTasks,
                      db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == enrollment.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    db_enrollment = Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    background_tasks.add_task(send_confirmation_email, student.email)
    return db_enrollment

# ── Auth ──────────────────────────────────────────────────────────────────────
@app.post("/api/v1/auth/register/", response_model=UserResponse,
          status_code=status.HTTP_201_CREATED, tags=["Auth"])
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")
    hashed = get_password_hash(user.password)
    db_user = User(email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/v1/auth/login/", response_model=Token, tags=["Auth"])
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}
