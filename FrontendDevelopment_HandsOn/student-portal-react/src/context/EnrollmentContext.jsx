import { createContext, useState } from 'react';

export const EnrollmentContext = createContext(null);

export function EnrollmentProvider({ children }) {
  const [enrolledCourses, setEnrolledCourses] = useState([]);

  function enroll(course) {
    setEnrolledCourses((prev) =>
      prev.some((c) => c.id === course.id) ? prev : [...prev, course]
    );
  }

  function remove(courseId) {
    setEnrolledCourses((prev) => prev.filter((c) => c.id !== courseId));
  }

  return (
    <EnrollmentContext.Provider value={{ enrolledCourses, enroll, remove }}>
      {children}
    </EnrollmentContext.Provider>
  );
}
