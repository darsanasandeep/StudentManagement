from rest_framework import serializers
from .models import User, Course, Subject, Teacher, Student


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'is_student', 'is_teacher']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id','course','code']


class SubjectSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), write_only=True
    )
    course_detail = CourseSerializer(source='course', read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'subject', 'course', 'course_detail']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','username']

class TeacherSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    user_details = UserSerializer(source='user', read_only=True)

    subject = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),write_only=True
    )
    subject_details = SubjectSerializer(source='subject',read_only=True)

    class Meta:
        model = Teacher
        fields =['id', 'user','user_details','first_name', 'last_name', 'phone', 'address', 'qualification','subject','subject_details']

class StudentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    user_details = UserSerializer(source='user', read_only=True)
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), write_only=True
    )
    course_details = CourseSerializer(source='course',read_only=True)
    class Meta:
        model = Student
        fields = ['id', 'user','user_details','first_name', 'last_name', 'phone', 'address','course','course_details']

class ProfileSerializer(serializers.Serializer):
    role = serializers.CharField()
    data = serializers.SerializerMethodField()

    def get_data(self,obj):
        if obj['role'] == 'teacher':
            teacher = Teacher.objects.get(user=obj['user'])
            return TeacherSerializer(teacher).data
        elif obj['role'] == 'student':
            student = Student.objects.get(user=obj['user'])
            return StudentSerializer(student).data
        return None