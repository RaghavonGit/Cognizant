import { useState } from 'react';

function StudentProfile() {
  const [profile, setProfile] = useState({ name: '', email: '', semester: '' });

  function handleChange(event) {
    const { name, value } = event.target;
    setProfile((prev) => ({ ...prev, [name]: value }));
  }

  return (
    <section className="profile-form">
      <h2>Student Profile</h2>
      <form>
        <label>
          Name
          <input type="text" name="name" value={profile.name} onChange={handleChange} />
        </label>
        <label>
          Email
          <input type="email" name="email" value={profile.email} onChange={handleChange} />
        </label>
        <label>
          Semester
          <input type="number" name="semester" value={profile.semester} onChange={handleChange} />
        </label>
      </form>
      <p className="profile-preview">
        {profile.name || 'Name'} · {profile.email || 'email@example.com'} · Semester {profile.semester || '-'}
      </p>
    </section>
  );
}

export default StudentProfile;
