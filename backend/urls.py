from django.urls import path
from .views import OrderEnlistingList,OrderEnlistingDetail,LLM

urlpatterns = [
    path('order-enlistings/', OrderEnlistingList.as_view(), name='order-enlisting-list'),
    path('order-enlistings/<str:pk>/', OrderEnlistingDetail.as_view(), name='order-enlisting-detail'),
    path('process/', LLM.as_view(), name='process_data'),
]

