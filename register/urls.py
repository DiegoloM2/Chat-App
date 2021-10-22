from django.urls import path

from .views import registerView

urlpatterns = [
    path('', registerView, name = 'register')
]