from .views import CreateUser, Login, Logout, CertifiedDoctor, DetailPerson, AllDoctor, EditDoctor, DeleteDoctor, \
    ChangeInformation, Diagnose, AllMyDiagnose, UploadPicture, ChangeDiagnose
from django.urls import path

urlpatterns = [
    path("register/", CreateUser.as_view()),
    path("login/", Login.as_view()),
    path("logout/", Logout.as_view()),
    path("certify/", CertifiedDoctor.as_view()),
    path("info/", DetailPerson.as_view()),
    path("doctor_index/", AllDoctor.as_view()),
    path("edit_doctor/", EditDoctor.as_view()),
    path("delete_doctor/", DeleteDoctor.as_view()),
    path("change_info/", ChangeInformation.as_view()),
    path("diagnose/", Diagnose.as_view()),
    path("my_diagnose/", AllMyDiagnose.as_view()),
    path("upload_pic/", UploadPicture.as_view()),
    path("change_diag/", ChangeDiagnose.as_view())
]
