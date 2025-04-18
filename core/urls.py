from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('voters/', include('voters.urls')),
    path('', include('voters.urls')),
    path('notifications/', include('notifications.urls')),
    path('', include('passes.urls')),

]

# Customize admin site
admin.site.site_header = 'Voter Management System'
admin.site.site_title = 'Voter Management'
admin.site.index_title = 'Welcome to Voter Management System'