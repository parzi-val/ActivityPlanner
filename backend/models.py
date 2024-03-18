from django.db import models
import google.generativeai as genai
import google.ai.generativelanguage as glm
import csv,json
import textwrap
from .places import places
gApi = "AIzaSyB-Uf2DfhX7w5d13ViQ5Cxj3nUFkSU5z2s"

genai.configure(api_key=gApi)



# activities = glm.Schema(
#     type = glm.Type.ARRAY,
#     items = glm.Schema(
#     type = glm.Type.OBJECT,
#     properties = {
#         'name' : glm.Schema(type=glm.Type.STRING),
#         'duration': glm.Schema(type=glm.Type.INTEGER),
#         'budget':glm.Schema(type=glm.Type.INTEGER)
#         },
#     required = ['name','duration','budget']
#     ) 
# )

params = glm.Schema(
    type = glm.Type.OBJECT,
    properties = {
        'duration': glm.Schema(type=glm.Type.INTEGER),
        'budget': glm.Schema(type=glm.Type.INTEGER)
    }
)       

row = glm.Schema(
    type = glm.Type.OBJECT,
    properties = {
        'activity' : glm.Schema(type = glm.Type.STRING),
        'timeframe' : glm.Schema(type=glm.Type.STRING),
    }
)

itinerary = glm.Schema(
    type = glm.Type.ARRAY,
    items = row
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

# add_to_db = glm.FunctionDeclaration(
#     name = "add_to_db",
#     description=textwrap.dedent("""\
#         Adds entities to the database.
#         """),
#     parameters = glm.Schema(
#         type = glm.Type.OBJECT,
#         properties = {
#             'places' : activities
#         }
#     )
# )




class ActivityRecommendation(genai.GenerativeModel):
    def __init__(self):
        super().__init__('gemini-1.0-pro',tools=[findparams])

    def breakdown(self,request):

        prompt= f"""Find the parameters from the given string: {request}"""
    
        response = self.generate_content(prompt)
        fc = response.candidates[0].content.parts[0].function_call
        res = type(fc).to_dict(fc)
        
        return res
    
    
    def gensets(self,budget,duration):


#         prompt = '''
# Given a list of places with their durations and costs, find the best combination of places to visit within a total duration of X hours and a total budget of Y dollars. Maximize the number of places visited while staying within the constraints.\n''' + places + f'''
# Total Duration: 10 hours
# Total Budget: 200 dollars


# Please add the places to the databases.
# '''

#         response = self.generate_content(prompt)
#         print(response)
#         fc = response.candidates[0].content.parts[0].function_call
#         parsed = type(fc).to_dict(fc)
#         return parsed

    # Sort places by cost in ascending order
            sorted_places = sorted(places, key=lambda x: x['Cost'])

            max_places = []
            total_duration = 0
            total_cost = 0

            # Iterate over sorted places
            for place in sorted_places:
                if total_duration + place['Duration'] <= duration and total_cost + place['Cost'] <= budget:
                    # Add the place if constraints are met
                    max_places.append(place)
                    total_duration += place['Duration']
                    total_cost += place['Cost']

            return max_places




    def plan(self,places):
        prompt = """
        Given a list of places along with their duration and costs and the total duration and cose. 
        Chart out an itinerary for visiting these places by giving time frames for each place."""+places+"""

        Example:
        Input:

        [
            {
                "Name": "Place 39",
                "Duration": 3,
                "Cost": 11
            },
            {
                "Name": "Place 57",
                "Duration": 3,
                "Cost": 12
            },
            {
                "Name": "Place 47",
                "Duration": 1,
                "Cost": 13
            },
            {
                "Name": "Place 76",
                "Duration": 1,
                "Cost": 33
            }
        ]

        Output:

        Alright, here's a possible plan to hit all these places with some meal breaks factored in. 
        We can start our day bright and early at 9:00 AM, spending three hours exploring Place 39. 
        By noon, our minds will be buzzing and our stomachs rumbling, so let's take a well-deserved lunch break at 1:00 PM.
        Feeling recharged, we can head to Place 57 for another exploration adventure from 1:00 PM to 4:00 PM. 
        Another meal break at 5:00 PM will keep our energy levels high!  
        The afternoon lets us tackle shorter visits. 
        Let's spend an hour at Place 47 from 5:00 PM to 6:00 PM, followed by another refuel session at 7:00 PM.
        To wrap up the day, we can visit Place 76 for an hour, from 7:00 PM to 8:00 PM.
        """


        response = self.generate_content(prompt)
        print(response)

        return response