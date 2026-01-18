from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

def get_tokens(user,request):
    refresh = RefreshToken.for_user(user)
    refresh['ip'] = request.META.get('REMOTE_ADDR')
    return {'refresh': str(refresh),'access': str(refresh.access_token)}

class RegisterView(APIView):
    def post(self,request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=201)
        return Response(serializer.errors,status=400)

class LoginView(APIView):
    def post(self,request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            tokens = get_tokens(user,request)
            return Response(tokens)
        return Response(serializer.errors,status=400)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        try:
            token = request.data["refresh"]
            RefreshToken(token).blacklist()
            return Response(status=205)
        except:
            return Response(status=400)

class SearchUsers(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        q = request.GET.get('q','')
        users = User.objects.filter(
            Q(username__icontains=q) |
            Q(email__icontains=q) |
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q)
        )
        data = [{'email':u.email,'username':u.username,'first_name':u.first_name,'last_name':u.last_name} for u in users]
        return Response(data)