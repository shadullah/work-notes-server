from django.shortcuts import render,redirect
from rest_framework import viewsets
from .serializers import TodoSerializer
from .models import Todo, PriorityChoices
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login,logout
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


# Create your views here.
class TodoView(viewsets.ModelViewSet):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all().order_by("-id")

class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            print(user)
            token = default_token_generator.make_token(user)
            print(token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print(uid)
            confirm_link = f"http://127.0.0.1:8000/todo/active/{uid}/{token}"
            email_subject="Confirm your Email"
            email_body= render_to_string('confirm_email.html', {'confirm_link': confirm_link})
            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check Your email for confirmation")
        return Response(serializer.errors)
    
def activate(req, uid64, token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user=None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True
        user.save()
        return redirect('login')
    else:
        return redirect('register')
    
class UserLoginApiView(APIView):
    def post(self,request):
        serializer = serializers.UserLoginSerializers(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user=authenticate(username=username, password=password)
            login(request, user)

            if user:
                token, _=Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({"error": "invalid Credential"})
        return Response(serializer.errors)
    
class UserLogoutView(APIView):
    authentication_classes = [BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, req):
        print(req.user)
        req.user.auth_token.delete()
        logout(req)
        return Response({"message": "logout Successfull"})
        # return redirect('login')
    
class ProfileInfo(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class= serializers.UserSerializer

class PriorityChoiceViewset(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = PriorityChoices.objects.all()
    serializer_class = serializers.PriorityChoiceSerializer