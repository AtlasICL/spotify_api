from dotenv import load_dotenv
import requests as rq
import os
import base64
import json

load_dotenv()
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")


def get_token() -> any:
    auth_string = CLIENT_ID+':'+CLIENT_SECRET
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'

    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": 'client_credentials'}

    result = rq.post(url, headers=headers, data=data)
    
    if result.status_code == 200:
        json_result = json.loads(result.content)
        token = json_result["access_token"]

        return token
    else: 
        raise rq.ConnectionError('Could not get Token: Status Code {result.status_code}')


def fetchArtistID(token, artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_header(token)
    query = f'q={artist_name}&type=artist&limit=1'

    query_url = url + query
    result = rq.get(query_url, headers=headers)
    
    if result.status_code == 200: 
        return json.loads(result.content)
    else: 
        raise rq.ConnectionError('Could not Fetch Artist ID: Status Code {result.status_code}')

def get_profile(token):
    ...
    

def get_auth_header(token):
    return {"Authorization": "Bearer "+token}

#--------------------------------------------------#
def main() -> None:
    token = get_token()

    print(fetchArtistID(artist_name='ACDC', token=token))


#--------------------------------------------------#
if __name__ == '__main__':
    main()

