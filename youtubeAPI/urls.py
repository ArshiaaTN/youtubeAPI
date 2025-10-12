from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/videos/', include('videos.urls')),
    path('api/subscriptions/', include('subscriptions.urls')),
    path('api/history/', include('history.urls')),
]
