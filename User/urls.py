from django.urls import path
from User.views import *

urlpatterns = [
    path('login/', LogView.as_view(), name="Login"),
    path('logout/', logout_view, name="Logout"),
    path('registration/', registration_view, name="Registration"),
    path('profile/', see_profile, name='Profile'),
]
