import { Routes } from '@angular/router';
import { CourseList } from './course-list/course-list';
import { StudentProfile } from './student-profile/student-profile';

export const routes: Routes = [
  { path: '', component: CourseList },
  { path: 'profile', component: StudentProfile },
];
