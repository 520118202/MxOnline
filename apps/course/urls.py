from django.urls import path, re_path

# 要写上app的名字
from course.views import CourseListView, CourseDetailView

app_name = "course"

urlpatterns = [
    path('list/', CourseListView.as_view(), name='course_list'),
    re_path('course/(?P<course_id>\d+)/', CourseDetailView.as_view(), name='course_detail'),
]
