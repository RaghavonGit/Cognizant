import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-course-card',
  imports: [],
  templateUrl: './course-card.html',
  styleUrl: './course-card.css',
})
export class CourseCard {
  @Input() name = '';
  @Input() code = '';
  @Input() credits = 0;
  @Input() grade = '';
}
