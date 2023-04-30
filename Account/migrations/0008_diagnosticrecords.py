# Generated by Django 4.1 on 2023-04-30 00:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Hospital", "0002_delete_hospital"),
        ("Account", "0007_alter_account_department"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiagnosticRecords",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "diagnostic_time",
                    models.TimeField(auto_now_add=True, verbose_name="就诊时间"),
                ),
                ("symptom", models.TextField(default="", verbose_name="患者症状")),
                (
                    "therapeutic_method",
                    models.TextField(default="", verbose_name="处理方法"),
                ),
                (
                    "attending_doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doc_diag",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="主治医生",
                    ),
                ),
                (
                    "diagnostic_department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Hospital.department",
                        verbose_name="所挂科室",
                    ),
                ),
                (
                    "patience",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pat_diag",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="患者",
                    ),
                ),
            ],
        ),
    ]