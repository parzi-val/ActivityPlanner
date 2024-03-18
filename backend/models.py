from django.db import models
import google.generativeai as genai
import google.ai.generativelanguage as glm

import csv,json
import os
import textwrap
from dotenv import load_dotenv
load_dotenv()
gApi = os.environ.get('gApi')

genai.configure(api_key=gApi)


params = glm.Schema(
    type = glm.Type.OBJECT,
    properties = {
        'duration': glm.Schema(type=glm.Type.INTEGER),
        'budget': glm.Schema(type=glm.Type.INTEGER)
    }
)


findparams = glm.FunctionDeclaration(
    name = "findparams",
    description=textwrap.dedent("""\
        Find the parameters (budget and duration in hours (convert to hours from days if required)) from the given string
        """),
    parameters = glm.Schema(
        type = glm.Type.OBJECT,
            properties = {
                "params" : params
        }
    )
)

class ActivityRecommendation(genai.GenerativeModel):
    def __init__(self):
        super().__init__('gemini-1.0-pro',tools=[findparams])

    def breakdown(self,request):

        prompt= f"""Find the parameters from the given string : {request}"""
    
        response = self.generate_content(prompt)
        fc = response.candidates[0].content.parts[0].function_call
        res = type(fc).to_dict(fc)
        
        return res