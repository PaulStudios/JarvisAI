# importing the requests library
import requests

# api-endpoint
URL = "http://api.brainshop.ai/get"

# location given here
brain = "156099"
apikey = "4TG9iu82pFOu9XjD"
uiid = "5"
message = "lol"

# defining a params dict for the parameters to be sent to the API
PARAMS = {
    'bid' : brain,
    'key' : apikey,
    'uid' : uiid,
    'msg' : message
}

# sending get request and saving the response as response object
r = requests.get(url=URL, params=PARAMS)

# extracting data in json format
data = r.json()
print(data)

# extracting latitude, longitude and formatted address
# of the first matching location
