import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormGroup, FormControl, Validators } from '@angular/forms';

@Component({
  selector: 'app-student-profile',
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './student-profile.html',
  styleUrl: './student-profile.css',
})
export class StudentProfile {
  profileForm = new FormGroup({
    name: new FormControl('', Validators.required),
    email: new FormControl('', [Validators.required, Validators.email]),
    semester: new FormControl('', [Validators.required, Validators.min(1), Validators.max(8)]),
  });

  submitted = false;

  onSubmit(): void {
    this.submitted = true;
    console.log(this.profileForm.value);
  }
}
