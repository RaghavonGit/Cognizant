import { Component, OnInit, signal, computed } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { CourseCard } from '../course-card/course-card';
import { CourseService, CourseData } from '../course';

@Component({
  selector: 'app-course-list',
  imports: [FormsModule, CourseCard],
  templateUrl: './course-list.html',
  styleUrl: './course-list.css',
})
export class CourseList implements OnInit {
  courses = signal<CourseData[]>([]);
  searchTerm = signal('');
  loading = signal(false);

  filteredCourses = computed(() => {
    const term = this.searchTerm().toLowerCase();
    return this.courses().filter((course) => course.name.toLowerCase().includes(term));
  });

  constructor(private courseService: CourseService) {}

  ngOnInit(): void {
    this.loading.set(true);
    this.courseService.getCourses().subscribe((posts) => {
      this.courses.set(
        posts.map((post, index) => ({
          id: post.id,
          name: post.title.slice(0, 28),
          code: `CS10${index + 1}`,
          credits: 3 + (index % 2),
          grade: ['A', 'A-', 'B+', 'B', 'A'][index],
        }))
      );
      this.loading.set(false);
    });
  }

  onSearchInput(value: string): void {
    this.searchTerm.set(value);
  }
}
