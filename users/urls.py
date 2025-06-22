from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import RegisterView, LogoutView, CourseViewSet, SubjectViewSet, TeacherViewSet, StudentViewSet, \
    UserViewSet, ProfileViewSet, get_user_info

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')
router.register(r'subject',SubjectViewSet,basename='subject')
router.register(r'teacher',TeacherViewSet,basename='teacher')
router.register(r'student',StudentViewSet,basename='student')
router.register(r'users',UserViewSet,basename='users')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileViewSet.as_view()),
    path('userinfo/', get_user_info),
    path('', include(router.urls)),

]