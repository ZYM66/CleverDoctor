from django.db import models
from django.contrib.auth.models import AbstractUser
from Hospital.models import Department


def pic_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/<id>/<filename>
    return f"user_{instance.id}/{filename}"


# Create your models here.
class Account(AbstractUser):
    """用户"""
    ROLES = (('p', "patient"),
             ('d', "Doctor"),
             ('a', "administrator"))
    GENDER = (('f', 'female'),
              ('m', 'male'),
              ('s', 'secret'))
    age = models.IntegerField(verbose_name="年龄", default=0)
    gender = models.CharField(verbose_name="性别", max_length=1, choices=GENDER, default='s')
    avatar = models.ImageField(verbose_name="用户头像", upload_to=pic_path)
    nick_name = models.CharField(verbose_name="用户昵称", max_length=36, null=True)
    real_name = models.CharField(verbose_name="真实姓名", max_length=150, null=True, blank=True,
                                 help_text="后期用于实名")
    telephone = models.CharField(max_length=11, null=True, blank=True, unique=True, help_text="后期用于实名")
    role = models.CharField(verbose_name="角色", max_length=1, choices=ROLES, default='p')
    introduction = models.TextField(verbose_name="个人简介", default="还没有个人简介!")
    major = models.TextField(verbose_name="专业擅长", default="")
    positions = models.CharField(verbose_name="职位", max_length=100, blank=True)
    department = models.ManyToManyField(verbose_name="所属科室", to=Department, blank=True, related_name="doctor")

    def __str__(self):
        return self.username


class DiagnosticRecords(models.Model):
    diagnostic_time = models.DateTimeField(verbose_name="就诊时间", auto_now_add=True)
    attending_doctor = models.ForeignKey(verbose_name="主治医生", to="Account", related_name="doc_diag",
                                         on_delete=models.CASCADE)
    diagnostic_department = models.ForeignKey(verbose_name="所挂科室", to=Department, on_delete=models.CASCADE)
    patient = models.ForeignKey(verbose_name="患者", to="Account", related_name="pat_diag", on_delete=models.CASCADE)
    symptom = models.TextField(verbose_name="患者症状", default="")
    therapeutic_method = models.TextField(verbose_name="处理方法", default="")

    class Meta:
        verbose_name = "诊断信息"
