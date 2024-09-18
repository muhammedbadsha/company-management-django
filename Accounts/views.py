from django.shortcuts import render
from django.http import HttpResponse
# import files in restframework 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
# import from my apps
from .permission import IsHRManager,IsManager
from .models import MyUser
from companys.models import Company
from departments.models import Department
from .serializers import UserSerializer,LoginSerializer

#inbuild imports
import uuid
# Create your views here.
def index(request):
  
   return HttpResponse("<h2>welcome</h2>")


class UserRegistrationsView(APIView):
    permission_classes = [IsHRManager | IsManager]
    def get(self, request): 
        # Fetch all users
        users = MyUser.objects.all()
        
        serializer = UserSerializer(users, many=True)  
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        
        company_sample_id = request.data['companys']
        company_sample = Company.objects.get(id=company_sample_id)  
        user_id = company_sample.company_name.upper().replace(" ","")[:4:]
        user_id += uuid.uuid4().hex[:12:].upper()
        data=request.data
        data["user_id"] = user_id
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserDetailView(APIView):
    def get(self, request, pk=None):
        try:
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

            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        except MyUser.DoesNotExist:
            return Response({"error": "User does not exist"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": "An error occurred"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def patch(self, request):
        data = request.data
        pass

class UserLoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data['user']
            
            # Create JWT token
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_id': user.user_id,
                'company': user.companys.company_name
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


def email_send(request, user_id):

    pass