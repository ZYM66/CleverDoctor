# Create your views here.
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from CleverDoctor.Authentication import CsrfExemptSessionAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated


class room(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, TokenAuthentication)
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # room_name = request.query_params.get("room_name")
        return Response({"msg": "成功加入聊天室"})
