from django.core.paginator import PageNotAnInteger
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View
from pure_pagination import Paginator

from course.models import Course
from operation.models import UserFavorite


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        # 热门课程推荐
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_course = all_courses.order_by('-students')
            if sort == 'hot':
                all_course = all_courses.order_by('-click_nums')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 2, request=request)
        course = p.page(page)
        return render(request, 'course-list.html', {'all_course': all_courses,
                                                    'sort': sort,
                                                    'hot_courses': hot_courses})


class CourseDetailView(View):
    """课程详情"""

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 课程的点击数加1
        course.click_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        # 必须时用户已登录我们才需要判断
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # 课程标签
        # 通过当前标签，查找数据库中的课程
        tag = course.tag
        if tag:
            # 需要从1开始不然会推荐自己
            relate_courses = Course.objects.filter(tag=tag)[:3]
        else:
            relate_courses = []
        return render(request, 'course-detail.html', {'course': course,
                                                      'relate_courses': relate_courses,
                                                      'has_fav_course': has_fav_course,
                                                      'has_fav_org': has_fav_orgs})
