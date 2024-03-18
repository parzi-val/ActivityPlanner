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
        pre = model.breakdown(data.get("text"))["args"]["params"]
        processed_data = model.gensets(pre["budget"],pre["duration"])
        res_data = {"activities":processed_data}
        print(json.dumps(processed_data))
        return Response(json.dumps(res_data), status=status.HTTP_200_OK)

