# Generated by Django 4.1 on 2023-05-01 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Account", "0014_alter_diagnosticrecords_diagnostic_time"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="diagnosticrecords", options={"verbose_name": "诊断信息"},
        ),
        migrations.AlterField(
            model_name="account",
            name="role",
            field=models.CharField(
                choices=[("p", "patient"), ("d", "Doctor"), ("a", "administrator")],
                default="p",
                max_length=1,
                verbose_name="角色",
            ),
        ),
    ]
