from rest_framework import serializers
from .models import User, Course, Subject, Teacher, Student, Attendance, AttendanceRecord, ExamType, MarkRecord, \
    Marks


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


class AttendanceSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), write_only=True
    )
    teacher_details = TeacherSerializer(source='teacher', read_only=True)

    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), write_only=True
    )
    course_details = CourseSerializer(source='course', read_only=True)

    subject = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), write_only=True
    )
    subject_details = SubjectSerializer(source='subject', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id','course','course_details','subject','subject_details','teacher','teacher_details','date']


class AttendanceRecordSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(),write_only=True
    )
    student_details = StudentSerializer(source='student',read_only=True)
    attendance = serializers.PrimaryKeyRelatedField(
        queryset=Attendance.objects.all(),write_only=True
    )
    attendance_details = AttendanceSerializer(source='attendance',read_only=True)

    class Meta:
        model = AttendanceRecord
        fields = ['id' ,'attendance','attendance_details','student','student_details','status']

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = ['id','exam']

class GradeSerializer(serializers.ModelSerializer):
    subject = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(), write_only=True
    )
    subject_details = SubjectSerializer(source='subject', read_only=True)
    exam_type = serializers.PrimaryKeyRelatedField(
        queryset=ExamType.objects.all(), write_only=True
    )
    exam_details = ExamSerializer(source='exam_type', read_only=True)
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all(), write_only=True
    )
    course_details = CourseSerializer(source='course', read_only=True)

    class Meta:
        model = Marks
        fields = ['id','subject','subject_details','exam_type','exam_details','max_mark','course','course_details']

class GradeRecordSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(
        queryset=Student.objects.all(), write_only=True
    )
    student_details = StudentSerializer(source='student', read_only=True)
    record = serializers.PrimaryKeyRelatedField(
        queryset=Marks.objects.all(),write_only=True
    )
    record_details = GradeSerializer(source='record',read_only=True)

    class Meta:
        model = MarkRecord
        fields = ['id','record','record_details','student','student_details','mark','grade']

class AttendanceCalendarSerializer(serializers.Serializer):
    date = serializers.DateField()
    status = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    con_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['con_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data

