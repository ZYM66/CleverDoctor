# Generated by Django 4.1 on 2023-04-29 01:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Account", "0004_account_res_hospital"),
    ]

    operations = [
        migrations.RenameField(
            model_name="account", old_name="relate_department", new_name="department",
        ),
        migrations.RenameField(
            model_name="account", old_name="relate_hospital", new_name="hospital",
        ),
    ]