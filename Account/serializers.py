from rest_framework import serializers
from rest_framework.authtoken.models import Token

from Account.models import Account, DiagnosticRecords, Context, Conversion
from Hospital.models import Department


class AccountRegisterSerializer(serializers.ModelSerializer):
    # 注册反序列化器
    email = serializers.EmailField(source="username")

    class Meta:
        model = Account
        fields = ["email", "password", "real_name"]

    def create(self, validated_data):  # validated_data已经验证过的数据  字典类型
        if Account.objects.filter(username=validated_data["username"]):
            return "fail"
        user = Account.objects.create_user(**validated_data)  # **解包 将字典解包为key value的关键字参数
        token_key = Token.objects.create(user=user).key
        return token_key


class AccountLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="username")

    class Meta:
        model = Account
        fields = ["email", "password"]


class AccountInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "telephone", "role"]


class AccountCertifiedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["real_name", "department", "introduction", "major", "telephone"]

    def update(self, instance, validated_data):
        if instance.telephone != validated_data.get('telephone', instance.telephone) and validated_data["telephone"]:
            instance.telephone = validated_data.get('telephone', instance.telephone)
        if validated_data.get("real_name", ''):
            instance.real_name = validated_data['real_name']
        if validated_data.get('introduction', ''):
            instance.introduction = validated_data.get('introduction', instance.introduction)
        if validated_data.get('major', ''):
            instance.major = validated_data.get('major', instance.major)
        if validated_data.get('department', ''):
            temp_department = validated_data.get("department", instance.department).split(',')
            instance.department.clear()
            instance.department.add(*temp_department)
        instance.role = 'd'
        instance.save()
        return instance


class BriefInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["real_name", "role", "id", "telephone", "age", "gender"]


class DetailInfoSerializer(BriefInfoSerializer):
    department = serializers.SerializerMethodField()

    class Meta:
        model = Account
        fields = ["id", "role", "real_name", "department", "telephone", "avatar",
                  "introduction", "major", "age", "gender"]

    def get_department(self, obj):
        try:
            return [department.name for department in obj.department.all()]
        except:
            return ""


class ChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["real_name", "telephone", "age", "gender"]

    def update(self, instance, validated_data):
        if instance.telephone != validated_data.get('telephone', instance.telephone) and validated_data["telephone"]:
            instance.telephone = validated_data.get('telephone', instance.telephone)
        if validated_data.get('real_name', ""):
            instance.real_name = validated_data.get('real_name', instance.real_name)
        if validated_data.get('age', ''):
            instance.age = validated_data.get('age', instance.age)
        if validated_data.get('gender', ""):
            instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance


class DiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticRecords
        fields = ["symptom", "therapeutic_method"]


class DetailDiagnosisSerializer(serializers.ModelSerializer):
    attending_doctor = serializers.SerializerMethodField()
    diagnostic_department = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()

    class Meta:
        model = DiagnosticRecords
        fields = "__all__"

    def get_attending_doctor(self, obj):
        return obj.attending_doctor.real_name

    def get_diagnostic_department(self, obj):
        return obj.diagnostic_department.name

    def get_patient(self, obj):
        return obj.patient.real_name


class ChangeDiagnosisSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiagnosticRecords
        fields = ["symptom", "therapeutic_method"]

    def update(self, instance, validated_data):
        if validated_data.get('symptom', ""):
            instance.symptom = validated_data['symptom']
        if validated_data.get("therapeutic_method", ""):
            instance.therapeutic_method = validated_data['therapeutic_method']
        instance.save()
        return instance


class DetailMessage(serializers.ModelSerializer):
    conversion = serializers.SerializerMethodField()

    class Meta:
        model = Context
        fields = ["speaker", "send_time", "content", "conversion"]

    def get_conversion(self, obj):
        return DetailConversion(obj.conversion).data


class DetailConversion(serializers.ModelSerializer):
    context = serializers.SerializerMethodField()

    class Meta:
        model = Conversion
        fields = ["context"]

    def get_context(self, obj):
        # ret = {obj.patient.id:[], obj.doctor.id:[]}
        # for cont in obj.context.all():
        #     ret[cont.speaker.id].append(cont.content)
        return [{"content": cont.content, "speaker": cont.speaker.real_name, "role": cont.speaker.role} for cont in
                obj.context.all()]
