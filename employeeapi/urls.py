from django.urls import path
from employeeapi import views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register("vehicle",views.VehicleView,basename="vehicles")
router.register("equipment",views.EquipmentView,basename="equipment")
router.register("training",views.TrainingViewSet,basename="training")

urlpatterns = [
    path("register/",views.EmployeeCreateView.as_view(),name="signup"),
    path("token/",ObtainAuthToken.as_view(),name="token"),
    # path("logout/",views.sign_out,name="logout"),

] +router.urls
