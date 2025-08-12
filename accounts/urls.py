from django.urls import path
from .views import UserSignInView, UserSignUpView, UserLogoutView, UsersGridView, UserRegistrationChartView, MetricsView, UserUpdateView, UserDeleteView
app_name = 'accounts'

urlpatterns = [
    path('signin/', UserSignInView.as_view(), name='signin'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('edit_user/<int:pk>/', UserUpdateView.as_view(), name='edit_user'),
    path('delete_user/<int:pk>/', UserDeleteView.as_view(), name='delete_user'),
    path('ag_grid/', UsersGridView.as_view(), name='agGrid'),
    # path('metrics/user_register/', UserRegistrationChartView.as_view(), name='users_register'),
    path('metrics/', MetricsView.as_view(), name='metrics'),
]