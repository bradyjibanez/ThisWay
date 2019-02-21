import os, json, sys, django
from django.conf import settings
from google.oauth2 import service_account
from google.cloud import vision
from google.cloud.vision import types
from google.protobuf.json_format import MessageToDict

sys.path.append("/CloudAssignment2/thisWay")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "thisWay.settings")

#Method for finding landmark in user provided image from Google Cloud Vision
def getLandmark(imageURL):
    # Read env data for google api credentials
    #CHANGE THIS ALL BACK TO ENVIRON VAR FOR CREDS IF POSSIBLE IN HEROKU STILL
    #DO THE SAME FOR STORAGE
    credentials_raw = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    service_account_info = json.loads(credentials_raw)
    credentials = service_account.Credentials.from_service_account_info(service_account_info)

    # Define a client, in this case Google's vision Image Annotator
    try:
        client = vision.ImageAnnotatorClient(credentials=credentials)
        image = vision.types.Image()
        image.source.image_uri = str(imageURL)
        resp = client.landmark_detection(image=image)

        #Used for return text diagnostic (Google uses a custom JSON format that can't be easily parsed/interpreted)
        response = str(MessageToDict(resp))
        splitted = response.split()

        #Variables for interpreting and populating results
        count = 0
        location = []
        lat = "null"
        lon = "null"

        #Arduous digging through a JSON format that shouldn't exist (I guess Google wanted to be security innovative?)
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

        #Add the latitude from that JSON-ish provision for playing with route definition
        count = 0
        for words in splitted:
            count += 1
            if words == "'latitude':" or words == "{'latitude':":
                lat = splitted[count][:-4]
                location.append(lat)

        #Same thing for longitude
        count = 0
        for words in splitted:
            count += 1
            if words == "'longitude':" or words == "{'longitude':":
                lon = splitted[count][:-4]
                location.append(lon)
               
        #Add it all together for sending to the user/playing with later in route dev
        landMarkDetected = ' '.join(location)

        count = 0
        LANDMARK = []
        while count < len(landMarkDetected):
            if landMarkDetected[count] == "'":
                pass
                if landMarkDetected[count+1] == " ":
                    break
            else:
                LANDMARK.append(landMarkDetected[count])
            count += 1

        LANDMARK = ''.join(LANDMARK)

        #If the JSON garbage didn't have anything, it'll generate a list less than 2, say so such that we can ignore the result
        if len(landMarkDetected) < 2:
            Nothing = "Nothing"      
            return Nothing
        #If longer than 2, it's good. Maybe. More conditions in the View playing with the results that guarantee no mess up. 
        else:
            return LANDMARK
    except IndexError:
        error = "We are unable to navigate to that landmark because we can't identify from that URL."
        return error