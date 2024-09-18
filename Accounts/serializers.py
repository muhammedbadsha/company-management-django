from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import MyUser
from companys.models import Company
import uuid


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = MyUser
        fields = ['user_id','first_name','last_name','companys','department','email','role','salary',"password"]
    

    def create(self, validated_data):
       
        user = MyUser(
            user_id = validated_data['user_id'],
            first_name=validated_data['first_name'],
            last_name = validated_data['last_name'],
            companys = validated_data['companys'],
            department = validated_data['department'],
            email = validated_data['email'],
            role = validated_data['role'],
            salary = validated_data['salary'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
    # def update(self, instance, validated_data):
    def update(self, instance, validated_data):
        # Update the instance with validated data
        print('Updating user instance...')
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.companys = validated_data.get('companys', instance.companys)
        instance.department = validated_data.get('department', instance.department)
        instance.email = validated_data.get('email', instance.email)
        instance.role = validated_data.get('role', instance.role)
        instance.salary = validated_data.get('salary', instance.salary)
        if 'passsword' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()

        return instance
    def patch(self, instace):
        pass
    

class LoginSerializer(serializers.Serializer):
    companys = serializers.CharField(write_only=True)
    user_id = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, data):
        companys = data.get('companys')
        user_id = data.get('user_id')
        password = data.get('password')

        # Get the user associated with this company and user_id
        try:
            user = MyUser.objects.get(companys=companys, user_id=user_id)
        except MyUser.DoesNotExist:
            raise AuthenticationFailed('User not found')

        # Authenticate using the password
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect password')

        # Return user if validation passed
        data['user'] = user
        return data