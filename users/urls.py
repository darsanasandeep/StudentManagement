from os.path import basename

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.serializers import ChangePasswordSerializer
from users.views import RegisterView, LogoutView, CourseViewSet, SubjectViewSet, TeacherViewSet, StudentViewSet, \
    UserViewSet, get_user_info, ProfileView, AttendanceViewSet, SubjectFilter, StudentFilter, AttendanceRecordViewSet, \
    AttendanceFilter, ExamViewSet, GradeViewSet, GradeRecordViewSet, GradeListing, SubjectWiseAttendance, \
    ExamWiseMarksView, StudentMarkListView, StudentCountAPIView, AttendanceCalenderView, ChangePasswordView

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')
router.register(r'subject',SubjectViewSet,basename='subject')
router.register(r'teacher',TeacherViewSet,basename='teacher')
router.register(r'student',StudentViewSet,basename='student')
router.register(r'users',UserViewSet,basename='users')
router.register(r'attendance',AttendanceViewSet,basename='attendance')
router.register(r'record',AttendanceRecordViewSet,basename='record')
router.register(r'exam',ExamViewSet,basename='exam')
router.register(r'grade',GradeViewSet,basename='grade')
router.register(r'graderecord',GradeRecordViewSet,basename='graderecord')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view()),
    path('userinfo/', get_user_info),
    path('subjectfilter/<int:id>',SubjectFilter.as_view()),
    path('studentfilter/<int:id>',StudentFilter.as_view()),
    path('attendancelist/<int:id>',AttendanceFilter.as_view()),
    path('gradelist/<int:id>',GradeListing.as_view()),
    path('attendancechart/<int:id>',SubjectWiseAttendance.as_view()),
    path('gradechart/<int:id>',ExamWiseMarksView.as_view()),
    path('marklist/<int:id>',StudentMarkListView.as_view()),
    path('studentcount/',StudentCountAPIView.as_view()),
    path('calender/<int:id>',AttendanceCalenderView.as_view()),
    path('changepassword/',ChangePasswordView.as_view()),
    path('', include(router.urls)),

]