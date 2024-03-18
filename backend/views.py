from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ActivityRecommendation
from .logger import FileLogger
from .parser import TravelPlanner
import json

logger = FileLogger("backend.log")
llmModel = ActivityRecommendation()

class LLM(APIView):
    def post(self, request, format=None):
        data = request.data
        logger.log(data)
        tokens = llmModel.breakdown(data.get("text"))["args"]["params"]
        model = TravelPlanner(tokens["duration"], tokens["budget"])
        path, total_duration, total_cost, total_distance = model.plan_travel_path(duration_tolerance=2, cost_tolerance=20)
        processed_data = [i[0] for i in path]
        res_data = {"activities": processed_data}
        return Response(json.dumps(res_data), status=status.HTTP_200_OK)
