from graphqlclient import GraphQLClient
import ast, json
import requests

def process(fulfilmentList):
    URL = 'https://palacio.api.fluentretail.com/api/v4.1/event/sync'

    i=0
    for ids in fulfilmentList:
        print(i, end=" ")
        print(ids)
        i=i+1

        body = {
    "accountId": "PALACIO",
    "retailerId": "2",
    "entityId": str(ids),
    "name": "Fraud_Review_Already_Passed",
    "entityType": "FULFILMENT"
}


        response = requests.post(URL,
                            data = json.dumps(body),
                            headers = {"Authorization": "Bearer afa1bf55-7219-40eb-8454-b13ce00b1600","Content-type":"application/json"})


        if 'COMPLETE' not in str(response.text):
            print(response.status_code)
            print(ids)
            print(response.text)

process([2873764,2873710,2873709,2873675,2873384,2873349,2873318,2873264,2872802,2872801,2872745,2872735,2872374,2872271,2872139,2872100,2872001,2871828,2871805,2871651,2871620,2871120])
