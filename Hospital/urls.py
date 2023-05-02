from django.urls import path
from .views import AddDepartment, DeleteDepartment, BriefDepartment, ReadDepartment

urlpatterns = [
    # path("createhospital/", CreateHospital.as_view())
    path("add_department/", AddDepartment.as_view()),
    path("delete_department/", DeleteDepartment.as_view()),
    # path("department_index/", DepartmentIndex.as_view()),
    path("brief_department/", BriefDepartment.as_view()),
    path("doctor_department/", ReadDepartment.as_view())
]