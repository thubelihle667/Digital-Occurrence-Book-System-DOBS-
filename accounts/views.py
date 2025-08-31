from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserRegistrationSerializer, CustomTokenObtainPairSerialzer
from .mixins import RoleRequiredMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.http import HttpResponse
from django.core.management import call_command
from django.views.decorators.csrf import csrf_exempt


class UserRegistrationView(APIView):
    permission_classes = [AllowAny] #IsAuthenticated, RoleRequiredMixin]
    RoleRequiredMixin.allowed_roles = ['Administrator']

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerialzer

class OccurrenceCreateView(APIView):
    permission_classes = [IsAuthenticated, RoleRequiredMixin]
    RoleRequiredMixin.allowed_roles = ['Operator']

class ReportsView(APIView):
    permission_classes = [IsAuthenticated, RoleRequiredMixin]
    RoleRequiredMixin.allowed_roles = ['Supervisor', 'Administrator']

@csrf_exempt
def run_migrations(request):
    if request.method == "POST":
        call_command("migrate", interactive=False)
        return HttpResponse("Migrations applied successfully!")
    return HttpResponse("Send a POST request to run migrations.")
