from django.db import models


# Create your models here.
# class Hospital(models.Model):
#     address = models.CharField(verbose_name="医院地址", max_length=150)
#     name = models.CharField(verbose_name="医院名称", max_length=36, null=True, blank=True)
#     telephone = models.CharField(verbose_name="联系电话", max_length=11, null=True, blank=True, unique=True)
#     # deparement = models.ManyToManyField(verbose_name="开设的科室", to="Department")


class Department(models.Model):
    name = models.CharField(verbose_name="科室", max_length=200)

    class Meta:
        verbose_name = "科室"
