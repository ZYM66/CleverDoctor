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
    BriefInfoSerializer, DetailInfoSerializer, ChangeSerializer, DiagnosisSerializer, DetailDiagnosisSerializer, \
    ChangeDiagnosisSerializer, DetailMessage, DetailConversion
from .models import Account, DiagnosticRecords, Context, Conversion
from django.db.models import Q
from CleverDoctor.utils import My_page
from Hospital.models import Department
import datetime
import pytz

utc = pytz.UTC


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
        if user.role == 'g':
            return Response({"code": STATUS_CODE['fail'], "msg": "游客无法使用该功能！"})
        try:
            message = AccountCertifiedSerializer(instance=user, data=request.data)
            message.update(instance=user, validated_data=request.data)
            if request.FILES.get("avatar"):
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
        role = request.query_params.get("role", "")
        role = 'd' if not role else role
        doctors = Account.objects.filter(Q(role=role) & Q(is_active=1))
        page_list = page.paginate_queryset(doctors, request, view=self)
        if role == 'p' and request.user.role != 'a':
            return Response({'code': STATUS_CODE['fail'], 'msg': "你不是管理员，不能直接访问患者！"})
        return Response(
            {'code': STATUS_CODE['success'], "total_page": page.count_pages, "num_data": len(doctors),
             'info': [DetailInfoSerializer(doctor, context={"request": request}, many=False).data for doctor in
                      page_list if
                      doctor.is_active],
             })


class EditDoctor(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            doctor_id = request.query_params.get("id")
            doctor = Account.objects.get(id=doctor_id)
            message = AccountCertifiedSerializer(instance=doctor, data=request.data)
            message.update(instance=doctor, validated_data=request.data)
            if request.FILES.get("avatar"):
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
        if user.role == 'g':
            return Response({"code": STATUS_CODE['fail'], "msg": "游客无法使用该功能！"})
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
        if user.role == 'g':
            return Response({"code": STATUS_CODE['fail'], "msg": "游客无法使用该功能！"})
        page = My_page()
        if user.role == 'd':
            diagnosis = user.doc_diag.all()
        else:
            diagnosis = user.pat_diag.all()
        page_list = page.paginate_queryset(diagnosis, request, view=self)
        return Response(
            {"code": STATUS_CODE["success"], "personal_msg": BriefInfoSerializer(user).data,
             "total_page": page.count_pages, "num_data": len(diagnosis),
             "diag_msg": [DetailDiagnosisSerializer(diag, context={"request": request}, many=False).data for diag in
                          page_list], })


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


class ChangeDiagnose(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        diag_id = request.query_params.get("diag_id")
        diag = DiagnosticRecords.objects.get(id=diag_id)
        if user.role != "d" or user != diag.attending_doctor:
            return Response({"code": STATUS_CODE['fail'], "msg": "你无权限更改该就诊记录！"})
        message = ChangeDiagnosisSerializer(diag)
        message.update(diag, request.data)
        return Response(
            {"code": STATUS_CODE['success'], "msg": "更改成功！", "info": DetailDiagnosisSerializer(diag).data})


class GuestLogin(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = (AllowAny,)

    def get(self, request):
        real_name = str(len(Account.objects.all())) + "@YouKe.com"
        validated_data = {"real_name": real_name, "password": "afsdhkfajhsdgjk", "username": real_name}
        vd = {"email": real_name, "password": "afsdhkfajhsdgjk"}
        guest = Account.objects.create_user(**validated_data)  # **解包 将字典解包为key value的关键字参数
        guest.role = 'g'
        guest.save()
        login = AccountLoginSerializer(data=vd)
        if login.is_valid():
            try:
                user = Account.objects.get(username=login.validated_data["username"])
                if check_password(login.validated_data["password"], user.password):
                    auth.login(request, user)
                    try:
                        token = Token.objects.get(user=user).key
                    except:
                        token = Token.objects.create(user=user).key
                    return Response(
                        {'code': STATUS_CODE["success"], "msg": "您现在为游客模式，解锁更多功能请登录", "token": token,
                         "info": BriefInfoSerializer(user).data})
                else:
                    return Response({"code": STATUS_CODE["fail"], "msg": "账号或密码错误！"})
            except:
                return Response({"code": STATUS_CODE["fail"], "msg": "账号或密码错误！"})
        return Response({"code": STATUS_CODE["fail"], "msg": "邮箱格式错误！"})


class SendMessage(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        conv_uuid = request.query_params.get("conv_uuid", '')
        content = request.data["content"]
        try:
            conv = Conversion.objects.get(uuid=conv_uuid)
        except:
            conv = Conversion.objects.create(patient=request.user, doctor_id=1)
        context = Context.objects.create(content=content, speaker=request.user, conversion=conv)
        return Response(
            {"code": STATUS_CODE['success'], "msg": "发送成功！", "detail": DetailMessage(context).data})


class GetAllConversation(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # return Response({"code": STATUS_CODE["success"],
        #                  "conv": {str(conv.uuid): DetailConversion(conv).data for conv in Conversion.objects.all()}})
        return Response({"code": STATUS_CODE["success"],
                         "conv": [{"uuid": conv.uuid, "conv": DetailConversion(conv).data} for conv in
                                  Conversion.objects.all()]})


class FindPatConv(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        page = My_page()
        for cov in Conversion.objects.all():
            if cov.close == 0 and datetime.datetime.now().__ge__(
                    (cov.create_time + datetime.timedelta(minutes=5)).replace(tzinfo=None)):
                cov.delete()
        my_conv = [conv for conv in Conversion.objects.all().order_by('-id') if conv.close == 0 and conv.doctor == user]
        page_list = page.paginate_queryset(my_conv, request, view=self)
        return Response({"code": STATUS_CODE["success"], "total_page": page.count_pages, "num_data": len(my_conv),
                         "conv": [{"uuid": conv.uuid,"create_time": conv.create_time, "patient": DetailInfoSerializer(conv.patient).data,
                                   "conv": DetailConversion(conv).data} for conv in
                                  page_list]})


