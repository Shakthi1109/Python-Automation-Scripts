from graphqlclient import GraphQLClient
import ast, json
import requests

def process():

    URL = 'https://palacio.api.fluentretail.com/api/v4.1/event/sync'

    with open('input.txt','r') as h:
        fulfilmentList = list(ast.literal_eval(h.read()))

    for ids in fulfilmentList:
        print(ids)

        body = {
                "accountId": "PALACIO",
                "retailerId":"2",
                "entityId":str(ids),
                "name":"Palacio_HD_Reassign_Fulfilment_Logic",
                "entityType":"ORDER"
                }


        response = requests.post(URL,
                            data = json.dumps(body),
                            headers = {"Authorization": "Bearer dcd51dea-0735-47a3-b89b-aaac1a182489","Content-type":"application/json"})


        if 'COMPLETE' not in str(response.text):
            print(response.status_code)
            print(ids)
            print(response.text)

process()
