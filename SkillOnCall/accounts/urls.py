from django.urls import path
from .views import signup_view, sign_in, sign_out

urlpatterns = [
    path('signup/', signup_view, name='signup_view'),
    path('login/', sign_in, name='sign_in'),
    path('logout/', sign_out, name='sign_out'),
]
