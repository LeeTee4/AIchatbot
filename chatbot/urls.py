from django.urls import path
from .views import ChatbotView, TestView

urlpatterns = [
    path('api/chat/', ChatbotView.as_view(), name='chatbot'),
    path('api/test/', TestView.as_view(), name='test'),
]
