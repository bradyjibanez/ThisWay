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
    #service_account_info = {
    #    "type": "service_account",
    #    "project_id": "landmarkdetection",
    #    "private_key_id": "de83cbe7b4dfdc5ed44da73c61d93ecefdee9459",
    #    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDYBVD/PM3MNBA1\nCXreJEY3r1qiMcpe4NT4+twHjEmWAeCAQmv5SW8f10XB0SnTvZ5UCAnr8ZgUYR1u\nv5a7ieM5jzpvMcbI5bdR+MjAJ08uxx8Le4Djvzg30KpG/eDFwrr7n7xSxbBY9zq4\nUxydIPrmKnSxvytQPC0FnvRkw4QHbxYMvmMT390hVcCi7IlyBwPBmKFD03R+Efq2\nL1j1ou1dRUOw6FLwnXdfY2t/iYxi8nVw7hO3h7RY8EUQuUNTYkOPCoV4WFot0NK6\nGSMkz82ETToGwwqeHBuCgEABGfdRaQlbENxT/KvdsCWxckbdS0uiFLo2XFzRQGLp\nQV2aspldAgMBAAECggEAMlR4xOMAiueFcCn7hca7Um2JZxlFLnphPHpMKfkKSwg4\na4GuQPhWSvufzdLDFUmMWkU+NIoHNhZTYnKCdsLfXVGM2ovlJfj5j4Bwm259MSel\nCMqXYtiySzTTe3Nau5DNemNC4CEdn3jIpln85HIi6t3w7tncyFag4bqhc9mmyQkv\n2Sah+cxUBm6ChCfGf7kXPaxscMbLh8yC4Sjl2Mcq0U6ZB44K0xBPapGIxLYSf/yZ\nhxxM8ST+lvyFOpMIZ97iXi/64cOwskVdRr6tGa78XHi/GJBZhcj1sRYDWUMxodLW\nJbSOBEnee1OT8/jGcfD06e1u86T1/Ny2NJjRSgOIyQKBgQDz8CPXOsjpoQ2RcJ14\ndw4gZf/4zgDP8mRVDrQntHdcT5Vqd1Nzo7TG+lE67BBeqWlZefjVxAo8h9QpOUZZ\nPasg+nknhE8raBKM+d7Mj8UHL4Ob3KibMFUd0+GDAHa3uSTzKilqe0N+louQtzx7\n2198rNLwZu8PEXqPiiqkjoo+yQKBgQDis8n2OTX4gWisSosCc/CJAuLZQObtpqZD\nUxg9sivA7ayXILENo5xRPA8JTWy1sq0+SfnwkM/0pXZsDjwg5/pR2I0be0EgWsS/\nV6tURmr0aZm0Vx7BU72NXzj5w+YiAdcaAju5+a/JqCpF/kSOfgBuxVWw9k/1EMtA\nn9EPGbLr9QKBgQDvis1nOU66PXD5dUDtXtv8bK1kQccCbOChtgKrSsg7Wds75VmJ\noSSQkJbb6ZxZmLrfJqt4Hz5+GlP490lhsPEvPUdjysWDtnsg/O4Qqs2sNLhkgdcA\nLgInfD1jSz1JRQJH1ws8iTbKRENhJM68QbwOzheGA06V2XAlLGSbm22eIQKBgHmB\nj3/PDiRRh/7APV1lMsjcqSV0adF6fqabBOUcd+MCAH1H4l3DEWdg31ZHDzsbt0sp\nbzMHCs6/WId14bhpXXs8q/TMzQ1AWS+NF6El1PGHIADOqQdJkNES9oC4BMK5Zcbk\n54o4T4WwAmhdbfVJh4XXcqRUgGqDQ80xW2XSill5AoGBAMdtiwAvhJVMC4eE+g4h\n0GLvqoY9/IoJsB6hy31buN+eL4O6IzePXUIxvwSwOS00ZFBxNOm6luM1DsSSu2WR\nhbXbBQQpZZIvFC/RcmHpjDWL4Q6loXhKcJdHf+waHR/J++Ks4vKVGbQ4z8x3FB4/\nCcxhYgaaJsXfRrKTWl0mDTC9\n-----END PRIVATE KEY-----\n",
    #    "client_email": "my-vision-sa@landmarkdetection.iam.gserviceaccount.com",
    #    "client_id": "108885269155100628107",
    #    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    #    "token_uri": "https://oauth2.googleapis.com/token",
    #    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    #    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/my-vision-sa%40landmarkdetection.iam.gserviceaccount.com"
    #}
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