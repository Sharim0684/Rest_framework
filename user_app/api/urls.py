from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from user_app.api.views import logout_view, registratioin_view
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

urlpatterns = [
    path('login/', obtain_auth_token, name='login'),
    path('register/', registratioin_view, name='register'),
    path('logout/', logout_view, name='logout'),  # Use the same view for logout

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
