import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <section className="hero-page">
      <h1>Welcome to the Student Portal</h1>
      <p>Track your courses, grades, and notifications all in one place.</p>
      <Link to="/courses" className="cta-link">Explore Courses</Link>
    </section>
  );
}

export default HomePage;
