# Generated by Django 4.1 on 2023-04-30 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Account", "0013_alter_diagnosticrecords_diagnostic_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="diagnosticrecords",
            name="diagnostic_time",
            field=models.DateTimeField(auto_now_add=True, verbose_name="就诊时间"),
        ),
    ]
