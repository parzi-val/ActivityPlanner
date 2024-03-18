from django.urls import path
from .views import LLM

urlpatterns = [

    path('recommend/', LLM.as_view(), name='process_data'),
]

