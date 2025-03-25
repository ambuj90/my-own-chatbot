from django.urls import path
from .views import home, chatbot_response, signup_view, login_view, logout_view
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('chat/', chatbot_response, name='chatbot_response'),
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path("migrate/", views.run_migrations, name="run_migrations"),
]
