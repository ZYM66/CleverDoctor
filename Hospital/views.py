from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from CleverDoctor.Authentication import CsrfExemptSessionAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from CleverDoctor.settings import STATUS_CODE
from CleverDoctor.utils import My_page
from .models import Department
from .serializers import IntroDepartmentSerializers, AllDepartmentSerializers


class AddDepartment(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAdminUser]

    def post(self, request):
        name = request.data["name"]
        try:
            Department.objects.get(name=name)
            return Response({"code": STATUS_CODE["fail"], "msg": "创建失败，该科室已存在！",
                             "info": {"name": name, "id": Department.objects.get(name=name).id}})
        except:
            Department.objects.create(name=name)
            return Response({"code": STATUS_CODE["success"], "msg": "创建成功！",
                             "info": {"name": name, "id": Department.objects.get(name=name).id}})


class DeleteDepartment(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAdminUser]

    def delete(self, request):
        department_id = request.query_params.get("id")
        Department.objects.get(id=department_id).delete()
        return Response({"code": STATUS_CODE["success"], "msg": "删除成功"})


class BriefDepartment(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        page = My_page()
        departments = Department.objects.all()
        page_list = page.paginate_queryset(departments, request, view=self)
        return Response(
            {'code': STATUS_CODE['success'],
             'total_page': page.count_pages,
             'num_data': len(departments),
             'msg': [AllDepartmentSerializers(department, context={"request": request}, many=False).data for
                     department in page_list]})


# class BriefDepartment(APIView):
#     authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         return Response(
#             {'code': STATUS_CODE['success'],
#              'msg': [AllDepartmentSerializers(department).data for department in Department.objects.all()]})


class ReadDepartment(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        department_id = request.query_params.get('department_id')
        print(department_id)
        return Response(
            {'code': STATUS_CODE['success'],
             'msg': IntroDepartmentSerializers(Department.objects.get(id=department_id)).data})
