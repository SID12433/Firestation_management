from django.shortcuts import render
from stationapi.models import Station,Employee,Equipment,Incident,Team,User,Vehicle,Feedback,Certification,TrainingList,Training,IncidentStatus
from stationapi.serializer import StationSerializer,EmployeeSerializer,UserSerializer,EquipmentSerializer,IncidentSerializer,TeamSerializer,AssignteamSerializer,VehicleSerializer,FeedbackSerializer,CertificationSerializer,TrainingListSerializer,IncidentStatusSerializer
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet,ViewSet
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework import permissions
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta





# Create your views here.

class StationCreateView(APIView):
    def post(self,request,*args,**kwargs):
        serializer=StationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_type="Station",is_superuser=True)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class EmployeeView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=Employee.objects.all()
        serializer=EmployeeSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Employee.objects.get(id=id)
        serializer=EmployeeSerializer(qs)
        return Response(data=serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance = Employee.objects.get(id=id)
            instance.delete()
            return Response({"msg": "Employee removed"})
        except Employee.DoesNotExist:
            return Response({"msg": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        

class UserView(ViewSet):        
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        one_hour_ago = timezone.now() - timedelta(hours=1)
        qs=User.objects.filter(last_logged__gte=one_hour_ago)
        # qs=User.objects.all()
        serializer=UserSerializer(qs,many=True)
        return Response(data=serializer.data)
        
       
class EquipmentView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=Equipment.objects.all()
        serializer=EquipmentSerializer(qs,many=True)
        return Response(data=serializer.data)
    
class TeamCreateView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def create(self,request,*args,**kwargs):
        serializer=TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
    
    def list(self,request,*args,**kwargs):
        qs=Team.objects.all()
        serializer=TeamSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    def retrieve(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Team.objects.get(id=id)
        serializer=TeamSerializer(qs)
        return Response(data=serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        try:
            instance = Team.objects.get(id=id)
            instance.delete()
            return Response({"msg": "Team removed"})
        except Employee.DoesNotExist:
            return Response({"msg": "Team not found"}, status=status.HTTP_404_NOT_FOUND)
        
        

class IncidentView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=Incident.objects.all()
        serializer=IncidentSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    @action(methods=["post"],detail=True)
    def assign_team(self,request,*args,**kwargs):
        serializer=AssignteamSerializer(data=request.data)
        incident_id=kwargs.get("pk")
        incident_obj=Incident.objects.get(id=incident_id)
        if serializer.is_valid():
            serializer.save(incident=incident_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    @action(methods=["post"],detail=True)
    def incident_status(self,request,*args,**kwargs):
        serializer=IncidentStatusSerializer(data=request.data)
        incident_id=kwargs.get("pk")
        incident_obj=Incident.objects.get(id=incident_id)
        if serializer.is_valid():
            serializer.save(Incident=incident_obj)
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)
        
    @action(methods=["get"],detail=True)   
    def review_list(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        incident_obj=Incident.objects.get(id=id)
        qs=Feedback.objects.filter(incident=incident_obj)
        serializer=FeedbackSerializer(qs,many=True)
        return Response(data=serializer.data)
    
class IncidentStatusView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=IncidentStatus.objects.all()
        serializer=IncidentStatusSerializer(qs,many=True)
        return Response(data=serializer.data)
        
class VehicleView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=Vehicle.objects.all()
        serializer=VehicleSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    
class EquipmentView(ViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    
    def list(self,request,*args,**kwargs):
        qs=Equipment.objects.all()
        serializer=EquipmentSerializer(qs,many=True)
        return Response(data=serializer.data)
    
    
class CertificationViewSet(ModelViewSet):
    authentication_classes=[authentication.TokenAuthentication]
    permission_classes=[permissions.IsAuthenticated]
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer
    

class TrainingListViewSet(ModelViewSet):
    queryset = TrainingList.objects.all()
    serializer_class = TrainingListSerializer
    
    
class StationCompletedStatusView(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        employee_data = []
        for employee in employees:
            completed_trainings = Training.objects.filter(employee=employee, status='Completed').count()
            # total_trainings = Training.objects.filter(employee=employee).count()
            total_trainings = TrainingList.objects.all().count()

            completion_percentage = (completed_trainings / total_trainings) * 100 if total_trainings > 0 else 0
            employee_data.append({
                'employee_id': employee.id,
                'employee_name': employee.name,
                'completion_percentage': completion_percentage,
                'completed_trainings': completed_trainings,
                'total_trainings': total_trainings
            })

        return Response(employee_data)
    
        
      

# def sign_out(request):
#     logout(request)
#     return render("signin")
