import { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import CourseCard from '../components/CourseCard';
import { enroll, fetchAllCourses, selectCourses, selectCoursesLoading, selectCoursesError } from '../features/enrollmentSlice';

function CoursesPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const dispatch = useDispatch();
  const navigate = useNavigate();

  const courses = useSelector(selectCourses);
  const loading = useSelector(selectCoursesLoading);
  const error = useSelector(selectCoursesError);

  useEffect(() => {
    dispatch(fetchAllCourses());
  }, [dispatch]);

  function handleEnroll(course) {
    dispatch(enroll(course));
    navigate('/profile');
  }

  const filteredCourses = courses.filter((course) =>
    course.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <section id="courses">
      <h2>Course Catalogue</h2>

      <input
        type="text"
        className="search-input"
        placeholder="Search courses..."
        value={searchTerm}
        onChange={(event) => setSearchTerm(event.target.value)}
      />

      {loading && <p className="status-msg">Loading...</p>}
      {error && <p className="status-msg error">Error: {error}</p>}

      <div className="course-grid">
        {filteredCourses.map((course) => (
          <div key={course.id}>
            <Link to={`/courses/${course.id}`} className="card-link">
              <CourseCard name={course.name} code={course.code} credits={course.credits} grade={course.grade} />
            </Link>
            <button className="enroll-btn" onClick={() => handleEnroll(course)}>
              Enroll
            </button>
          </div>
        ))}
      </div>
    </section>
  );
}

export default CoursesPage;
