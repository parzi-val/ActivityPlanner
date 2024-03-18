from django.db import models
import google.generativeai as genai
import google.ai.generativelanguage as glm
import csv,json
import textwrap


gApi = "AIzaSyB-Uf2DfhX7w5d13ViQ5Cxj3nUFkSU5z2s"



genai.configure(api_key=gApi)
places = ""

with open('./backend/places.csv', mode="r") as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for idx, row in enumerate(reader, start=1):
        place_name = row[0]
        duration = row[1]
        cost = row[2]
        places += f"{idx}. {place_name} - Duration: {duration} hours, Cost: ${cost}\n"


activities = glm.Schema(
    type = glm.Type.ARRAY,
    items = glm.Schema(
    type = glm.Type.OBJECT,
    properties = {
        'name' : glm.Schema(type=glm.Type.STRING),
        'duration': glm.Schema(type=glm.Type.INTEGER),
        'budget':glm.Schema(type=glm.Type.INTEGER)
        },
    required = ['name','duration','budget']
    ) 
)

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
        Find the parameters (budget and duration) from the given string
        """),
    parameters = glm.Schema(
        type = glm.Type.OBJECT,
            properties = {
                "params" : params
        }
    )
)

add_to_db = glm.FunctionDeclaration(
    name = "add_to_db",
    description=textwrap.dedent("""\
        Adds entities to the database.
        """),
    parameters = glm.Schema(
        type = glm.Type.OBJECT,
        properties = {
            'places' : activities
        }
    )
)




class ActivityRecommendation(genai.GenerativeModel):
    def __init__(self):
        super().__init__('gemini-1.0-pro',tools=[add_to_db,findparams])

    def breakdown(self,request):

        prompt= f"""Find the parameters from the given string: {request}"""
    
        response = self.generate_content(prompt)
        fc = response.candidates[0].content.parts[0].function_call
        res = type(fc).to_dict(fc)
        
        return res
    
    
    def gensets(self,budget,duration,placesCount=5):


        prompt = '''
Given a list of places with their durations and costs, find the best combination of places to visit within a total duration of X hours and a total budget of Y dollars. Maximize the number of places visited while staying within the constraints.\n''' + places + f'''
Total Duration: 10 hours
Total Budget: 200 dollars


Please add the places to the databases.
'''

        response = self.generate_content(prompt)
        print(response)
        fc = response.candidates[0].content.parts[0].function_call
        parsed = type(fc).to_dict(fc)
        return parsed