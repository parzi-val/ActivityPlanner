from .serializers import OrderEnlistingSerializer
from .models import OrderEnlisting
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class LLM(APIView):
    def post(self,request,format = None):
        data = request.data
        origin = request.headers.get('Origin')
        processed_data = {
            "result" : data.get("param1","")+data.get("param2",""),"origin" : origin
        }
        return Response(processed_data, status=status.HTTP_200_OK)


class OrderEnlistingList(generics.ListAPIView):
    queryset = OrderEnlisting.objects.all()
    serializer_class = OrderEnlistingSerializer

class OrderEnlistingDetail(generics.RetrieveAPIView):
    queryset = OrderEnlisting.objects.all()
    serializer_class = OrderEnlistingSerializer