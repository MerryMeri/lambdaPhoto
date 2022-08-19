import json
import boto3
import requests

def lambda_handler(event, context):
    client = boto3.client('lex-runtime')
    input = event['queryStringParameters']['q']
    response = client.post_text(botName="SearchBot", botAlias="lexConnectOne", userId="903647304818", inputText=input)
    print(response)
    if 'slots' in response:
        url = "https://search-photos-z5ptjwic2ktfmrk6vmd3lpz52y.us-east-1.es.amazonaws.com/photos/_search?q="
        tag = response['slots']['tagOne'].capitalize()
        url = url + tag
        if (tag[-1] == "s"):
            url += " OR " + tag[:-1]
        print(tag)
        if (response['slots']['tagTwo'] != None and response['slots']['tagTwo'] != ""): 
            tag2 = response['slots']['tagTwo'].capitalize()
            url = url + " OR " + tag2
            if (tag2[-1] == "s"):
                url += " OR " + tag2[:-1]
            print(tag2)
        if (response['slots']['tagThree'] != None and response['slots']['tagThree'] != ""):
            tag3 = response['slots']['tagThree'].capitalize()
            url = url + " OR " + tag3
            if (tag3[-1] == "s"):
                url += " OR " + tag3[:-1]
            print(tag3)
        
        photos = []
        print(url)
        responseES = requests.get(url, auth=("Meri", "Gjs920568#"))
        print(responseES.content)
        r = responseES.json()
        if 'hits' in r:
            for val in r['hits']['hits']:
                key = val['_source']['objectKey']
                tags = val['_source']['labels']
                photoName = "https://picturesbucketfp.s3.amazonaws.com/" + key
                photo = [photoName, tags]
                photos.append(photo)
        print(photos)
        response = {"statusCode": 200, "headers": {}, "body": json.dumps({"photos": photos})}
        return response
    else:
        return {"statusCode": 200, "headers": {}, "body": json.dumps({"photos": photos})}