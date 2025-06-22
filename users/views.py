from django.core.serializers import serialize
from django.shortcuts import render
from rest_framework import generics, status ,viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Course, Subject, Teacher, Student
from users.serializers import RegisterSerializer, CourseSerializer, SubjectSerializer, TeacherSerializer, \
    StudentSerializer, UserSerializer, ProfileSerializer


# Create your views here.


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class CourseViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

class SubjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SubjectSerializer
    queryset = Subject.objects.all()

class TeacherViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = TeacherSerializer
    queryset = Teacher.objects.all()

class StudentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentSerializer
    queryset = Student.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    def get_queryset(self):
        user_type = self.request.query_params.get('type')

        if user_type == 'teacher':
            return User.objects.filter(is_teacher=True)
        elif user_type == 'student':
            return User.objects.filter(is_student=True)
        return User.objects.none()

class ProfileViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        user = request.user

        if user.is_teacher:
            role = 'teacher'
            data = TeacherSerializer(user.teacher).data
        elif user.is_student:
            role = 'student'
            data = StudentSerializer(user.student).data
        else:
            return Response({'detail': 'Profile not found'}, status=404)

        return Response({
            'role': role,
            'data': data
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_teacher": user.is_teacher,
        "is_student": user.is_student,
    })
