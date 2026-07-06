from django.contrib import admin

from .models import Course, Department, Enrollment, Student
    

# Register your models here.
admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Enrollment)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department', 'credits')
    search_fields = ('name', 'code')
    list_filter = ('department',)

admin.site.register(Course, CourseAdmin)
