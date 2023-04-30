from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import Department


#
# class InitHospitalSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = Hospital
#         fields = ["name", "address", "telephone"]

class AllDepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ["id", "name"]


class IntroDepartmentSerializers(serializers.ModelSerializer):
    doctor = serializers.SerializerMethodField()

    class Meta:
        model = Department
        fields = ["id", "name", "doctor"]

    def get_doctor(self, obj):
        doctors = obj.doctor.all()
        return [doctor.real_name for doctor in doctors]

