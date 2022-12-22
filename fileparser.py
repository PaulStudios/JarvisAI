import json
import jsonpath_rw_ext




def fileparser(name1):
    with open('dates.json') as json_file:
        data = json.load(json_file)
        result = jsonpath_rw_ext.parse("$..holidays[?(@.name==name1)].date.iso").find(data)
        return result[0].value
        

def getdate(name):
    with open('dates.json') as json_file:
        data = json.load(json_file)
        maindata = data["response"]["holidays"]
        li = [item.get('name') for item in maindata]
        lu = li.index(name)
        la = data["response"]["holidays"][lu]["date"]["iso"]
        return la




