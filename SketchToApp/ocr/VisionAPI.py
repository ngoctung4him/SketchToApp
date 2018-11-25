import base64
#from googleapiclient import discovery
#from googleapiclient import errors
import cv2
import os

#from oauth2client.client import GoogleCredentials

DISCOVERY_URL = 'https://{api}.googleapis.com/$discovery/rest?version={apiVersion}'  # noqa
BATCH_SIZE = 10

class VisionApi:
    """Construct and use the Google Vision API service."""

    def __init__(self, api_discovery_file='vision_api.json'):
        self.credentials = GoogleCredentials.get_application_default()
        self.service = discovery.build(
            'vision', 'v1', credentials=self.credentials,
            discoveryServiceUrl=DISCOVERY_URL)

    def detect_text(self, input_filename, num_retries=3, max_results=6):
        """Uses the Vision API to detect text in the given file.
        """
        image = []
        with open(input_filename, 'rb') as image_file:
            image = image_file.read()
        batch_request = []
        batch_request.append({
                'image': {
                    'content': base64.b64encode(
                            image).decode('UTF-8')
                },
                'features': [{
                    'type': 'TEXT_DETECTION',
                    'maxResults': max_results,
                }]
            })
        request = self.service.images().annotate(
            body={'requests': batch_request})

        try:
            responses = request.execute(num_retries=num_retries)
            if 'responses' not in responses:
                return 
            response = responses[ 'responses']
            singleResponse = response[0]
            if 'error' in singleResponse:
                print("API Error for %s: %s" % (
                            input_filename,
                            singleResponse[0]['error']['message']
                            if 'message' in responses['error']
                            else ''))
                return 
            if 'textAnnotations' in singleResponse:
                return singleResponse['textAnnotations']
            else:
                return

        except errors.HttpError as e:
            print("Http Error for %s: %s" % ("not working", e))
        except KeyError as e2:
            print("Key error: %s" % e2)


    def getTextfromNA(self, mImage):
        cv2.imwrite("vision_temp.jpg",mImage)
        textOut = self.detect_text("vision_temp.jpg")
        os.remove("vision_temp.jpg")
        return textOut
