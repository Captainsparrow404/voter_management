from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'passes'

router = DefaultRouter()
router.register(r'passes', views.PassViewSet, basename='pass')

urlpatterns = [
    path('passes/', views.pass_request_view, name='pass_request'),
    path('api/', include(router.urls)),
    path('api/passes/pending/', views.PassViewSet.as_view({'get': 'pending'})),
    path('api/passes/approved/', views.PassViewSet.as_view({'get': 'approved'})),
    path('api/passes/rejected/', views.PassViewSet.as_view({'get': 'rejected'})),
    path('api/passes/<int:pk>/approve/', views.PassViewSet.as_view({'post': 'approve'})),
    path('api/passes/<int:pk>/reject/', views.PassViewSet.as_view({'post': 'reject'})),

]