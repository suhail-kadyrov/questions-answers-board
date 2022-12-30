from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Q&A Board API",
      default_version='v1',
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('authentication.urls')),
    path('api/v1/profile/', include('profiles.urls')),
    
    path('api/v1/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-swagger-ui'),
]
