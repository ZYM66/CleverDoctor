# Generated by Django 4.1 on 2023-04-28 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Hospital", "0001_initial"),
        ("Account", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="relate_department",
            field=models.ManyToManyField(
                blank=True, to="Hospital.department", verbose_name="所属科室"
            ),
        ),
        migrations.AddField(
            model_name="account",
            name="relate_hospital",
            field=models.ManyToManyField(
                blank=True, to="Hospital.hospital", verbose_name="所属医院"
            ),
        ),
        migrations.AlterField(
            model_name="account",
            name="role",
            field=models.CharField(
                choices=[("p", "patience"), ("d", "Doctor")],
                default="p",
                max_length=1,
                verbose_name="角色",
            ),
        ),
    ]