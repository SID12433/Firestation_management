from rest_framework import serializers
from stationapi.models import Employee,Vehicle,Equipment,Training

        
class EmployeeSerializer(serializers.ModelSerializer):
    id=serializers.CharField(read_only=True)
    password=serializers.CharField(write_only=True)

    class Meta:
        model=Employee
        fields=["id","username","name","phone","email_address","password"]

    def create(self, validated_data):
        return Employee.objects.create_user(**validated_data)
    
    
class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        fields="__all__"
        

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Equipment
        fields="__all__"
        

class TrainingSerializer(serializers.ModelSerializer):
    employee=serializers.CharField(read_only=True)
    class Meta:
        model = Training
        fields = "__all__"