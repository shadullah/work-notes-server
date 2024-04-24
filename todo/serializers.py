from rest_framework import serializers
from .models import Todo, PriorityChoices
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')

class PriorityChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriorityChoices
        fields = '__all__'

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ['id', 'user', 'title', 'description', 'completed', 'date', 'priority']
        depth=1
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] =UserSerializer(instance.user).data 
        return data
    
    def validate(self, obj):
        obj['user']=self.context['request'].user
        return obj


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(required = True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']
    
    def save(self):
        username = self.validated_data['username']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password2 = self.validated_data['confirm_password']
        
        if password != password2:
            raise serializers.ValidationError({'error' : "Password Doesn't Mactched"})
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error' : "Email Already exists"})
        account = User(username = username, email=email, first_name = first_name, last_name = last_name)
        print(account)
        account.set_password(password)
        account.is_active = False
        account.save()
        return account
    
class UserLoginSerializers(serializers.Serializer):
    username= serializers.CharField(required=True)
    password= serializers.CharField(required=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_superuser']