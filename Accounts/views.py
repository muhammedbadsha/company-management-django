from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes,smart_str
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponsePermanentRedirect
# import files in restframework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken

# import from my apps
from .permission import IsHRManager, IsManager
from .models import MyUser
from companys.models import Company
from departments.models import Department
from .serializers import (
    UserSerializer,
    LoginSerializer,
    PasswordResetSendLinkSerializer,
    PasswordResetSerializer,
    
)

# inbuild imports
import uuid
from decouple import config

# Create your views here.
def index(request):

    # subject = 'email sending test'
    # body = f'{subject} this is working properly'
    # from_email = settings.EMAIL_HOST_USER
    # to_email = 'nasertk20@gmail.com'
    # send_email = EmailMessage(subject, body, from_email, [to_email])
    # send_email.send()
    return Response({"status": "welcome"})


class UserRegistrationsView(APIView):
    permission_classes = [IsHRManager | IsManager]

    def get(self, request):
        # Fetch all users
        users = MyUser.objects.all()

        serializer = UserSerializer(users, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        company_sample_id = request.data["companys"]
        company_sample = Company.objects.get(id=company_sample_id)
        user_id = company_sample.company_name.upper().replace(" ", "")[:4:]
        user_id += uuid.uuid4().hex[:12:].upper()
        data = request.data
        data["user_id"] = user_id
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [config('APP_SCHEME'), 'http', 'https']
class UserDetailView(APIView):
    def get(self, request, pk=None):
        try:
            redirect_url = request.data.get("redirect_url", "")    
            users = MyUser.objects.get(pk=pk)
            serializers = UserSerializer(users)
            return Response(serializers.data)
        except Exception as e:
            return Response({"error": "User couldn't found"})

    def put(self, request, pk=None):
        try:
            # Fetch user information from the database
            user = MyUser.objects.get(pk=pk)

            if user:
                # Pass the existing user instance and request data to the serializer
                serializer = UserSerializer(instance=user, data=request.data)

                if serializer.is_valid():
                    # Save and update the instance using serializer
                    serializer.save()  # This calls the serializer's update method
                    return Response(serializer.data, status=status.HTTP_200_OK)

                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        except MyUser.DoesNotExist:
            return Response(
                {"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"error": "An error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]    
            # Create JWT token
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                    "user_id": user.user_id,
                    "company": user.companys.company_name,
                },
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class passwordResetSendRequestView(APIView):
    def post(self, request):

        serializer = PasswordResetSendLinkSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
    

            user = MyUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse(
                "password-reset", kwargs={"uidb64": uidb64, "token": token}
            )
            # redirect_url = request.data.get('redirect_url','')
            absurl = 'http://'+current_site+relativeLink
    
            subject = "Password Reset request"
            # from_email = user.companys.email
            from_email = settings.EMAIL_HOST_USER            
            token = RefreshToken.for_user(user).access_token    
            link = "127.0.0.1:8000/api/user"
            reset_url = f"{link}/password_reset?token={str(token)}"
            email_body = f"Hi click this link below to reset your password \n"+ absurl

            send_mail = EmailMessage(subject, email_body, from_email, [email])
            send_mail.send()

            # return Response({"error": "email has error"})
            return Response(
                {"message": "password reset like sent to your email"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    def get(self, request, uidb64, token):
        try:
            id  = smart_str(urlsafe_base64_decode(uidb64))    
            user = MyUser.objects.get(id = id)    
            check = PasswordResetTokenGenerator().check_token(user,token)
            if check is True:
                return Response({"success": True}, status=status.HTTP_200_OK)    
            
            return Response({'error is ': False},status=status.HTTP_200_OK)
        except:
            return Response({'error':"check not good"},status=status.HTTP_400_BAD_REQUEST)
        

    def patch(self, request,uidb64,token):
        password = request.data.get('password')
        serializer = PasswordResetSerializer(data={'password':password})
        try:
            id = smart_bytes(urlsafe_base64_decode(uidb64))
            user = MyUser.objects.get(id = id)
            if user:
                check_password_time_out = PasswordResetTokenGenerator().check_token(user, token)
                if check_password_time_out:            
                    if serializer.is_valid():                
                        serializer.save(user=user)
                
                        return Response({"success":"password changed successfully!!!!"},status=status.HTTP_200_OK)
                    return Response(serializer.errors,status=status.HTTP_201_CREATED)

                else:
                    return Response({"error":"your token is timeout please try again"},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":"user not found please try another email address"},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e :    
            return Response({"error":e})
            # if not token:
            #     return Response(
            #         {"error": "Token Not Provided"}, status=status.HTTP_400_BAD_REQUEST
            #     )
            # try:
            #     access_token = AccessToken(token)
            #     user = MyUser.objects.get(id=access_token["user_id"])
            #     # Update the password
            #     serializer = PasswordResetSerializer(data=request.data)
            #     if serializer.is_valid():
            #         user.password = serializer.validated_data["password"]
            #         user.save()
            #         return Response(
            #             {"message": "Password has been reset successfully"},
            #             status=status.HTTP_200_OK,
            #         )

            #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # except Exception as e:
            #     return Response(
            #         {"error": "Invalid token or user"}, status=status.HTTP_400_BAD_REQUEST
            #     )
