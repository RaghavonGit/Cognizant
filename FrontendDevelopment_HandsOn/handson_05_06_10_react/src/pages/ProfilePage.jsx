import { useSelector, useDispatch } from 'react-redux';
import { unenroll, selectEnrolledCourses } from '../features/enrollmentSlice';
import StudentProfile from '../components/StudentProfile';

function ProfilePage() {
  const enrolledCourses = useSelector(selectEnrolledCourses);
  const dispatch = useDispatch();

  return (
    <>
      <StudentProfile />

      <section className="enrolled-list">
        <h2>Enrolled Courses ({enrolledCourses.length})</h2>
        {enrolledCourses.length === 0 && <p className="status-msg">No courses enrolled yet.</p>}
        <div className="course-grid">
          {enrolledCourses.map((course) => (
            <article className="course-card" key={course.id}>
              <h3>{course.name}</h3>
              <p>{course.code}</p>
              <span>{course.credits} credits</span>
              <button className="remove-btn" onClick={() => dispatch(unenroll(course.id))}>Remove</button>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}

export default ProfilePage;
