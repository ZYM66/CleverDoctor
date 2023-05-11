# Generated by Django 4.1 on 2023-05-09 12:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("Account", "0016_alter_account_role"),
    ]

    operations = [
        migrations.CreateModel(
            name="Conversion",
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
                    "conv_name",
                    models.CharField(
                        blank=True, max_length=20, null=True, verbose_name="聊天室名字"
                    ),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4)),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doc_conv",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="医生",
                    ),
                ),
                (
                    "patient",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="pat_conv",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="病人",
                    ),
                ),
            ],
            options={"verbose_name": "聊天室",},
        ),
        migrations.CreateModel(
            name="Context",
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
                ("content", models.TextField(default="", verbose_name="聊天内容")),
                (
                    "send_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="发送时间"),
                ),
                (
                    "conversion",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="context",
                        to="Account.conversion",
                        verbose_name="聊天室",
                    ),
                ),
                (
                    "speaker",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="text",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="说话人",
                    ),
                ),
            ],
            options={"verbose_name": "对话",},
        ),
    ]