from .models import ActivityRecommendation
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
model = ActivityRecommendation()




class LLM(APIView):
    def post(self,request,format = None):


        data = request.data
        print(data.get("text"))
        # pre = model.breakdown(data.get("text"))["args"]["params"]
        # processed_data = model.gensets(pre["budget"],pre["duration"])
        # res_data = {"activities":processed_data}
        # print(json.dumps(processed_data))
        res_data = {"activities": [{"title": "Place 39", "categoryName": "Swimming Pool", "address": "X5F6+Q88, VIT University, Vellore, Tamil Nadu 632014", "phone":9048131066, "url": "https://maps.app.goo.gl/8oQwfYJusgm9mhhQ8", "price": 300, "time": 2}]
}
        return Response(json.dumps(res_data), status=status.HTTP_200_OK)

