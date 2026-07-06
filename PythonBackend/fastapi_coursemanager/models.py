from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint, Boolean
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Department(Base):
    __tablename__ = 'departments'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    head_of_dept = Column(String)
    budget = Column(Float)
    courses = relationship('Course', back_populates='department')

class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, nullable=False)
    credits = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.id'))
    department = relationship('Department', back_populates='courses')
    enrollments = relationship('Enrollment', back_populates='course')

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    enrollment_year = Column(Integer)
    department_id = Column(Integer, ForeignKey('departments.id'))
    enrollments = relationship('Enrollment', back_populates='student')

class Enrollment(Base):
    __tablename__ = 'enrollments'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    grade = Column(String(2), nullable=True)
    student = relationship('Student', back_populates='enrollments')
    course = relationship('Course', back_populates='enrollments')
    __table_args__ = (UniqueConstraint('student_id', 'course_id'),)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
