from django.urls import path, include
from .views import hello_view
from .views import CourseListView, CourseDetailView, CourseViewSet, StudentViewSet, EnrollmentViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('courses',CourseViewSet)
router.register('students', StudentViewSet)
router.register('enrollments', EnrollmentViewSet)
urlpatterns = [
    path('api/hello/', hello_view, name='hello'),
    path('api/', include(router.urls)),
]
    


