from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, status ,viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User, Course, Subject, Teacher, Student, AttendanceRecord, Attendance, ExamType,\
    MarkRecord, Marks
from users.serializers import RegisterSerializer, CourseSerializer, SubjectSerializer, TeacherSerializer, \
    StudentSerializer, UserSerializer, AttendanceRecordSerializer, AttendanceSerializer, ExamSerializer, \
    GradeSerializer, GradeRecordSerializer, AttendanceCalendarSerializer, ChangePasswordSerializer


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

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        if hasattr(user, 'is_student') and user.is_student:
            try:
                student = Student.objects.get(user_id=user.id)
                course = student.course
                return Response({
                    "type": "student",
                    "id": student.id,
                    "user_id": user.id,
                    "email": user.email,
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "phone": student.phone,
                    "address": student.address,
                    "course_details" : {
                        "id" : course.id,
                        "course" : course.course,
                        "code" : course.code
                    }
                })
            except Student.DoesNotExist:
                return Response({"error": "Student profile not found"}, status=404)

        elif hasattr(user, 'is_teacher') and user.is_teacher:
            try:
                teacher = Teacher.objects.get(user_id=user.id)
                subject = teacher.subject
                return Response({
                    "type": "teacher",
                    "id": teacher.id,
                    "user_id": user.id,
                    "email": user.email,
                    "first_name": teacher.first_name,
                    "last_name": teacher.last_name,
                    "phone": teacher.phone,
                    "address": teacher.address,
                    "qualification": teacher.qualification,
                    "subject_details":{
                        "id": subject.id,
                        "subject" : subject.subject
                    }
                })
            except Teacher.DoesNotExist:
                return Response({"error": "Teacher profile not found"}, status=404)

        else:
            return Response({"error": "User role not recognized"}, status=400)

    def put(self, request):
        user = request.user

        if hasattr(user, 'is_student') and user.is_student:
            try:
                student = Student.objects.get(user_id=user.id)
                serializer = StudentSerializer(student, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Student.DoesNotExist:
                return Response({"error": "Student profile not found"}, status=404)

        elif hasattr(user, 'is_teacher') and user.is_teacher:
            try:
                teacher = Teacher.objects.get(user_id=user.id)
                serializer = TeacherSerializer(teacher, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Teacher.DoesNotExist:
                return Response({"error": "Teacher profile not found"}, status=404)

        else:
            return Response({"error": "User role not recognized"}, status=400)


class SubjectFilter(APIView):
    def get(self, request, id):
        subjects = Subject.objects.filter(course_id=id)
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

class AttendanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceSerializer
    queryset = Attendance.objects.all()

class AttendanceRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceRecordSerializer
    queryset = AttendanceRecord.objects.all()

    def create(self, request, *args, **kwargs):
        is_bulk = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_bulk)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class StudentFilter(APIView):
    def get(self, request, id):
        subjects = Student.objects.filter(course_id=id)
        serializer = StudentSerializer(subjects, many=True)
        return Response(serializer.data)


class AttendanceFilter(APIView):
    def get(self, request, id):
        teacher = Teacher.objects.get(user_id=request.user.id)

        course_id = request.GET.get('course')
        subject_id = request.GET.get('subject')
        date = request.GET.get('date')
        status = request.GET.get('status')

        if id == 0:

            attendance_qs = Attendance.objects.filter(teacher_id=teacher.id)

            if course_id:
                attendance_qs = attendance_qs.filter(course_id=course_id)
            if subject_id:
                attendance_qs = attendance_qs.filter(subject_id=subject_id)
            if date:
                attendance_qs = attendance_qs.filter(date=date)

            all_records = []

            for attendance in attendance_qs:
                records = AttendanceRecord.objects.filter(attendance_id=attendance.id)
                if status:
                    records = records.filter(status=status)
                all_records.extend(records)

        else:
            records = AttendanceRecord.objects.filter(attendance_id=id)
            if status:
                records = records.filter(status=status)
            all_records = list(records)

        serializer = AttendanceRecordSerializer(all_records, many=True)
        return Response(serializer.data)


class ExamViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ExamSerializer
    queryset = ExamType.objects.all()

class GradeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GradeSerializer
    queryset = Marks.objects.all()

class GradeRecordViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = GradeRecordSerializer
    queryset = MarkRecord.objects.all()

    def create(self, request, *args, **kwargs):
        is_bulk = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=is_bulk)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class GradeListing(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        teacher = get_object_or_404(Teacher, user=request.user)

        course = request.GET.get('course')
        exam_type = request.GET.get('exam_type')

        if id == 0:
            filters = {"record__subject": teacher.subject}
            if course:
                filters["record__course_id"] = course
            if exam_type:
                filters["record__exam_type_id"] = exam_type

            all_records = MarkRecord.objects.filter(**filters).select_related('record', 'record__subject', 'student')
        else:
            all_records = MarkRecord.objects.filter(record_id=id).select_related('record', 'record__subject', 'student')

        serializer = GradeRecordSerializer(all_records, many=True)
        return Response(serializer.data)

class SubjectWiseAttendance(APIView):
    def get(self, request, id):

        if id==0:
            attendance_data = (
                AttendanceRecord.objects
                .all()
                .values('attendance__subject__id','attendance__subject__subject', 'status')
                .annotate(count=Count('id'))
            )
        else:
            attendance_data = (
                AttendanceRecord.objects
                .filter(student_id=id)
                .values('attendance__subject__id','attendance__subject__subject', 'status')
                .annotate(count=Count('id'))
            )

        result = {}
        for entry in attendance_data:
            subject_id = entry['attendance__subject__id']
            subject_name = entry['attendance__subject__subject']
            status = entry['status']
            count = entry['count']

            if subject_name not in result:
                result[subject_name] = {'subject': subject_name,'subject_id':subject_id, 'Present': 0, 'Absent': 0}
            result[subject_name][status] = count

        return Response(list(result.values()))

class ExamWiseMarksView(APIView):
    def get(self, request, id):

        records = (
            MarkRecord.objects
            .filter(student_id=id)
            .select_related('record__exam_type', 'record__subject')
        )

        exam_data = {}  # key: exam_id, value: dict with exam name and subjects
        for rec in records:
            exam_type = rec.record.exam_type
            exam_id = exam_type.id
            subject_name = rec.record.subject.subject

            if exam_id not in exam_data:
                exam_data[exam_id] = {
                    "exam": exam_type.exam,
                    "exam_id": exam_id,
                    "subjects": []
                }

            exam_data[exam_id]["subjects"].append({
                "name": subject_name,
                "value": rec.mark
            })

        result = list(exam_data.values())
        return Response(result)

class StudentMarkListView(APIView):
    def get(self, request,id):
        student = Student.objects.get(user_id=request.user.id)
        records = (
            MarkRecord.objects
            .filter(record__exam_type__id=id, student=student)
            .select_related('record__subject', 'record__exam_type')
        )

        if not records.exists():
            return Response({"exam": "Unknown", "subjects": []})

        exam_name = records[0].record.exam_type.exam

        data = {
            "exam": exam_name,
            "subjects": []
        }

        for rec in records:
            data["subjects"].append({
                "name": rec.record.subject.subject,
                "mark": rec.mark,
                "grade": rec.grade
            })

        return Response(data)

class StudentCountAPIView(APIView):
    def get(self, request):
        data = (
            Student.objects
            .values('course__course')
            .annotate(count=Count('id'))
            .order_by('course__course')
        )

        result = [{"course": entry["course__course"], "count": entry["count"]} for entry in data]
        return Response(result)

class AttendanceCalenderView(APIView):
    def get(self, request, id):
        subject = get_object_or_404(Subject, id=id)
        try:
            student = Student.objects.get(user_id=request.user.id)
        except:
            return Response({"detail": "Student profile not found."}, status=404)

        records = AttendanceRecord.objects.filter(
            student=student,
            attendance__subject=subject
        ).select_related('attendance').order_by('attendance__date')

        attendance_list = [
            {"date": record.attendance.date, "status": record.status}
            for record in records
        ]

        serializer = AttendanceCalendarSerializer(attendance_list, many=True)
        return Response(serializer.data)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            if not user.check_password(old_password):
                return Response({"old_password": ["Incorrect old password."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
