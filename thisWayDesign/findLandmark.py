from django.core.serializers.json import DjangoJSONEncoder
from google.oauth2 import service_account
from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToDict
import os
import json


def getLandmark(self, imageURL):
    # Read env data
    credentials_raw = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

    # Generate credentials
    service_account_info = json.loads(credentials_raw)
    credentials = service_account.Credentials.from_service_account_info(
        service_account_info)

    # Define a client, in this case Google's text to speech
    client = vision.ImageAnnotatorClient(credentials=credentials)
    image = vision.types.Image()
    image.source.image_uri = imageURL
    resp = client.landmark_detection(image=image)

    response = str(MessageToDict(resp))
    splitted = response.split()

    count = 0
    location = []
    lat = "null"
    lon = "null"

    #print(splitted)

    for words in splitted:
        count += 1
        if words == "'description':" or words == "[{'description':":
            while True:
                #Necessary for everything else
                if "'," in splitted[count]:
                    splitted[count] = splitted[count][:-1]
                    location.append(splitted[count])
                    break
                #Necessary for end of Google JSON
                if "}]}" in splitted[count]:
                    splitted[count] = splitted[count][:-3]
                    location.append(splitted[count]) 
                    break
                else:
                    location.append(splitted[count])
                count += 1

    count = 0
    for words in splitted:
        count += 1
        if words == "'latitude':" or words == "{'latitude':":
            lat = splitted[count][:-4]

    count = 0
    for words in splitted:
        count += 1
        if words == "'longitude':" or words == "{'longitude':":
            lon = splitted[count][:-4]
           
    place = ' '.join(location)       

    return place
