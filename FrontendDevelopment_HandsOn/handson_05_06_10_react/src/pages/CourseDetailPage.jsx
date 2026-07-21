import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { enroll } from '../features/enrollmentSlice';
import { getCourseById } from '../api/courseApi';

function CourseDetailPage() {
  const { courseId } = useParams();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!courseId) return;

    setLoading(true);
    getCourseById(courseId).then((data) => {
      setCourse(data);
      setLoading(false);
    });
  }, [courseId]);

  function handleEnroll() {
    dispatch(enroll(course));
    navigate('/profile');
  }

  if (loading) return <p className="status-msg">Loading course...</p>;
  if (!course) return <p className="status-msg error">Course not found.</p>;

  return (
    <section className="course-detail">
      <h2>{course.name}</h2>
      <p>{course.code} · {course.credits} credits</p>
      <p className="course-body">{course.body}</p>
      <button className="enroll-btn" onClick={handleEnroll}>Enroll</button>
    </section>
  );
}

export default CourseDetailPage;
