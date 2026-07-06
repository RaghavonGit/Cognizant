from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status           # HTTP status codes like 200, 201, 404
from .models import Course, Student, Enrollment  # Our Course, Student, and Enrollment database models
from .serializers import CourseSerializer, StudentSerializer, EnrollmentSerializer   # Converts objects to/from JSON
from rest_framework.response import Response  # DRF's response object (returns JSON automatically)
from rest_framework.views import APIView   # Base class that handles HTTP methods for us
from rest_framework.decorators import action  # Allows us to add custom actions to viewsets
from rest_framework import viewsets

def hello_view(request):
    return HttpResponse("Course Manager API is working!")

class CourseListView(APIView):
    # Handles GET /api/courses/ — returns all courses
    def get(self, request):
        courses = Course.objects.all()                      # Fetch every course from the database
        serializer = CourseSerializer(courses, many=True)   # Convert list of objects to JSON (many=True for lists)
        return Response(serializer.data)                    # Send JSON response with 200 OK

    # Handles POST /api/courses/ — creates a new course
    def post(self, request):
        serializer = CourseSerializer(data=request.data)    # Load incoming JSON into serializer
        if serializer.is_valid():                           # Validate the data against model rules
            serializer.save()                               # Save valid data to the database
            return Response(serializer.data, status=status.HTTP_201_CREATED)        # Return created object with 201
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)      # Return errors with 400
    
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        course = self.get_object()
        enrollments = Enrollment.objects.filter(course=course)
        students = [e.student for e in enrollments]
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


class CourseDetailView(APIView):
    # Handles GET /api/courses/<pk>/ — returns one course
    def get(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)          # Fetch course by primary key
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)   # Return 404 if not found

        serializer = CourseSerializer(course)           # Convert single object to JSON (no many=True needed)
        return Response(serializer.data)

    # Handles PUT /api/courses/<pk>/ — updates a course
    def put(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course, data=request.data)    # Pass existing object + new data to serializer
        if serializer.is_valid():
            serializer.save()                           # Update the record in the database
            return Response(serializer.data)            # Return updated object with 200
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handles DELETE /api/courses/<pk>/ — deletes a course
    def delete(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        course.delete()                                         # Remove from database
        return Response(status=status.HTTP_204_NO_CONTENT)     # 204 = success but no content to return
    
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer