function CourseCard({ name, code, credits, grade }) {
  return (
    <article className="course-card">
      <h3>{name}</h3>
      <p>{code}</p>
      <span>{credits} credits{grade ? ` · Grade: ${grade}` : ''}</span>
    </article>
  );
}

export default CourseCard;
