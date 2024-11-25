from rest_framework import serializers
from user.models import Market_User,CustomUser
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

User = get_user_model()


from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password



class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    mobile_number = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    # password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("id",'username', 'password', 'email', 'first_name', 'last_name', 'mobile_number', 'address', 'user_type')

    # def validate(self, attrs):
    #     if attrs['password'] != attrs['password2']:
    #         raise serializers.ValidationError({"password": "Password fields didn't match."})
    #     return attrs

    def create(self, validated_data):
        user_type = validated_data.pop('user_type', 'user')
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            mobile_number=validated_data['mobile_number'],
            address=validated_data['address'],
            user_type=user_type,
            is_staff=user_type in ['superuser', 'admin'],
            is_superuser=user_type == 'superuser',
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Must include "username" and "password"')

        data['user'] = user
        return data

from django.core.validators import validate_email
import re
class Market_UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market_User
        fields = '__all__'
        read_only_fields = ['price']

    def validate_mobile_number(self, value):
       
        if not re.match(r'^\d{10,15}$', value):
            raise serializers.ValidationError("Mobile number must contain only digits and be 10 to 15 digits long.")
        return value
    
    def validate_email(self, value):
        
        try:
            validate_email(value)
        except serializers.ValidationError:
            raise serializers.ValidationError("Enter a valid email address.")
        return value