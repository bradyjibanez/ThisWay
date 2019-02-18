import os, json, sys, django
#from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from google.oauth2 import service_account
from google-cloud import vision
from google-cloud.vision import types
from google.protobuf.json_format import MessageToDict

#settings.configure(DEBUG=True) SAYS SETTINGS ALREADY CONFIGURED

sys.path.append("/CloudAssignment2/thisWay")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thisWay.settings")
#django.setup() FOR TRUELY STANDALONE SCRIPTS. IMPORTED BY MODELS, SO NO?

#from thisWay.models import Landmark

def getLandmark(imageURL):
    # Read env data for google api credentials
    credentials_raw = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    
    # Generate credentials
    #with open(credentials_raw, 'r') as cred:
    #    creds = json.load(cred)
    #service_account_info NOT NEEDED?
    service_account_info = json.loads(credentials_raw)
    credentials = service_account.Credentials.from_service_account_info(service_account_info)

    # Define a client, in this case Google's text to speech
    client = vision.ImageAnnotatorClient(credentials=credentials)
    image = vision.types.Image()
    image.source.image_uri = str(imageURL)
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
            location.append(lat)

    count = 0
    for words in splitted:
        count += 1
        if words == "'longitude':" or words == "{'longitude':":
            lon = splitted[count][:-4]
            location.append(lon)
           
    landMarkDetected = ' '.join(location)

    if landMarkDetected == None:
        Nothing = "Nothing"      
        return nothing
    else:
        return landMarkDetected

#LM = getLandmark("https://upload.wikimedia.org/wikipedia/commons/thumb/8/85/Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg/240px-Tour_Eiffel_Wikimedia_Commons_%28cropped%29.jpg")
#print(LM)