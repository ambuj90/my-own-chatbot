from django.contrib import admin
from django.urls import path, include
from chatbot.views import run_migrations

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chatbot.urls')),
    path('migrate/', run_migrations),  # ✅ Add this line
]
