# myapp/urls.py
from django.urls import path
from .views import  get_chart_data, save_chart_to_dashboard,get_saved_charts,upload_pdf,get_saved_files,signup
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('chart-data/', get_chart_data, name='chart-data'),
    path('save-chart-to-dashboard/', save_chart_to_dashboard, name='save_chart_to_dashboard'),
    path('get-charts/', get_saved_charts, name='get_charts'),
    path('upload/', upload_pdf, name='upload_pdf'),
    path('get-files/',get_saved_files,name='get_files'),
    path('token/', csrf_exempt(TokenObtainPairView.as_view()), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', signup, name='signup'),
]
