import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { getAllCourses } from '../api/courseApi';

export const fetchAllCourses = createAsyncThunk('courses/fetchAll', async () => {
  return await getAllCourses();
});

const enrollmentSlice = createSlice({
  name: 'enrollment',
  initialState: {
    enrolledCourses: [],
    courses: [],
    coursesLoading: false,
    coursesError: null,
  },
  reducers: {
    enroll(state, action) {
      const alreadyEnrolled = state.enrolledCourses.some((c) => c.id === action.payload.id);
      if (!alreadyEnrolled) {
        state.enrolledCourses.push(action.payload);
      }
    },
    unenroll(state, action) {
      state.enrolledCourses = state.enrolledCourses.filter((c) => c.id !== action.payload);
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchAllCourses.pending, (state) => {
        state.coursesLoading = true;
        state.coursesError = null;
      })
      .addCase(fetchAllCourses.fulfilled, (state, action) => {
        state.courses = action.payload;
        state.coursesLoading = false;
      })
      .addCase(fetchAllCourses.rejected, (state, action) => {
        state.coursesError = action.error.message;
        state.coursesLoading = false;
      });
  },
});

export const { enroll, unenroll } = enrollmentSlice.actions;

// Selectors — components read state through these, never the raw store shape
export const selectCourses = (state) => state.enrollment.courses;
export const selectCoursesLoading = (state) => state.enrollment.coursesLoading;
export const selectCoursesError = (state) => state.enrollment.coursesError;
export const selectEnrolledCourses = (state) => state.enrollment.enrolledCourses;

export default enrollmentSlice.reducer;
