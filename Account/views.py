from django.shortcuts import render
from rest_framework.views import APIView
from CleverDoctor.Authentication import CsrfExemptSessionAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib import auth
from django.contrib.auth.hashers import check_password
from CleverDoctor.settings import STATUS_CODE
from .serializers import AccountRegisterSerializer, AccountLoginSerializer, AccountCertifiedSerializer, \
    BriefInfoSerializer, DetailInfoSerializer, ChangeSerializer, DiagnosisSerializer, DetailDiagnosisSerializer
from .models import Account, DiagnosticRecords
from django.db.models import Q
from CleverDoctor.utils import My_page


# Create your views here.
class CreateUser(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,)
    permission_classes = (AllowAny,)

    def post(self, request):
        register = AccountRegisterSerializer(data=request.data)
        if register.is_valid():
            token_key = register.save()
            if token_key == "fail":
                return Response({"code": STATUS_CODE["fail"], "msg": "邮箱已注册!"})
            else:
                return Response({"code": STATUS_CODE["success"], "msg": "注册成功!", "token": token_key})
        else:
            return Response(register.errors)


class Login(APIView):
    authentication_classes = [CsrfExemptSessionAuthentication]
    permission_classes = (AllowAny,)

    def post(self, request):
        login = AccountLoginSerializer(data=request.data)
        if login.is_valid():
            try:
                user = Account.objects.get(username=login.validated_data["username"])
                if check_password(login.validated_data["password"], user.password):
                    auth.login(request, user)
                    try:
                        token = Token.objects.get(user=user).key
                    except:
                        token = Token.objects.create(user=user).key
                    return Response({"code": STATUS_CODE["success"], "msg": "登录成功！", "token": token,
                                     "data": BriefInfoSerializer(user).data})
                else:
                    return Response({"code": STATUS_CODE["fail"], "msg": "账号或密码错误！"})
            except:
                return Response({"code": STATUS_CODE["fail"], "msg": "账号或密码错误！"})
        return Response({"code": STATUS_CODE["fail"], "msg": "邮箱格式错误！"})


class Logout(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        auth.logout(request=request)
        return Response({'code': STATUS_CODE["success"], "msg": "注销成功！"})


class CertifiedDoctor(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        try:
            message = AccountCertifiedSerializer(instance=user, data=request.data)
            message.update(instance=user, validated_data=request.data)
            user.avatar = request.FILES.get("avatar")
            user.save()
            return Response(
                {"code": STATUS_CODE["success"], "msg": "认证成功！",
                 "detail_data": DetailInfoSerializer(user).data})
        except:
            return Response({"code": STATUS_CODE["fail"], "msg": "该电话号码已经被使用！"})


class DetailPerson(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        doctor_id = request.query_params.get("id")
        doctor = Account.objects.get(id=doctor_id)
        info = DetailInfoSerializer(doctor).data
        return Response({"code": STATUS_CODE["success"], "msg": info})


class AllDoctor(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = My_page()
        doctors = Account.objects.filter(Q(role='d') & Q(is_active=1))
        page_list = page.paginate_queryset(doctors, request, view=self)
        return Response(
            {'code': STATUS_CODE['success'],
             'info': [DetailInfoSerializer(doctor, context={"request": request}, many=False).data for doctor in
                      page_list if
                      doctor.is_active]})


class EditDoctor(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            doctor_id = request.query_params.get("id")
            doctor = Account.objects.get(id=doctor_id)
            message = AccountCertifiedSerializer(instance=doctor, data=request.data)
            message.update(instance=doctor, validated_data=request.data)
            doctor.avatar = request.FILES.get("avatar")
            doctor.save()
            return Response(
                {"code": STATUS_CODE["success"], "msg": "编辑成功！",
                 "detail_data": DetailInfoSerializer(doctor).data})
        except:
            return Response({"code": STATUS_CODE["fail"], "msg": "该电话号码已经被使用！"})


class DeleteDoctor(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAdminUser]

    def delete(self, request):
        try:
            doctor_id = request.query_params.get("id")
            doctor = Account.objects.get(id=doctor_id)
            if doctor.is_active:
                doctor.is_active = 0
                doctor.save()
                return Response({"code": STATUS_CODE["success"], "msg": "删除成功！"})
            else:
                return Response({"code": STATUS_CODE["fail"], "msg": "错误删除！该医生早已被删除"})
        except:
            return Response({"code": STATUS_CODE["fail"], "msg": "错误删除！该医生不存在"})


class ChangeInformation(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        message = ChangeSerializer(user, request.data)
        message.update(user, request.data)

        return Response(
            {"code": STATUS_CODE["success"], "msg": "信息更改成功", "detail_info": BriefInfoSerializer(user).data})


class Diagnose(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        doctor = request.user
        if doctor.role != 'd':
            return Response({"code": STATUS_CODE["fail"], "msg": "你不是医生，无权限使用该功能！"})
        patient_id = request.query_params.get("patient_id")
        message = DiagnosisSerializer(data=request.data)
        if message.is_valid():
            diagnosis = DiagnosticRecords.objects.create(attending_doctor=doctor,
                                                         patient=Account.objects.get(id=patient_id),
                                                         diagnostic_department=doctor.department.first(),
                                                         symptom=message.data["symptom"],
                                                         therapeutic_method=message.data["therapeutic_method"])
            return Response({"code": STATUS_CODE["success"], "msg": DetailDiagnosisSerializer(diagnosis).data})


class AllMyDiagnose(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        page = My_page()
        if user.role == 'd':
            diagnosis = user.doc_diag.all()
        else:
            diagnosis = user.pat_diag.all()
        page_list = page.paginate_queryset(diagnosis, request, view=self)
        return Response(
            {"code": STATUS_CODE["success"], "personal_msg": BriefInfoSerializer(user).data,
             "diag_msg": [DetailDiagnosisSerializer(diag, context={"request": request}, many=False).data for diag in
                          page_list]})


class UploadPicture(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]

    #
    # def get(self, request):
    #     user = request.user
    #     serializer = UserSerializer(user)
    #     return Response(serializer.data)

    def post(self, request):
        user = request.user
        user.avatar = request.FILES.get('avatar')
        user.save()
        serializer = DetailInfoSerializer(user)
        return Response({"code": STATUS_CODE["success"], "msg": "上传成功!", "detail_info": serializer.data})
