import json, ast, requests

def run(fulfilmentIds):
    print(fulfilmentIds)
    for fulfilmentId in list(set(fulfilmentIds)):
        url = 'https://palacio.api.fluentretail.com/api/v4.1/event/sync'

        body={
        "accountId": "PALACIO",
        "retailerId": "2",
        "entityId": str(fulfilmentId),
        "name": "DLX_CANCELLATION_WAREHOUSE_RECEIVED",
        "entityType": "FULFILMENT"
        }

        response = requests.post(url,
                    data = json.dumps(body),
                    headers = {"Authorization": "Bearer e5b7e8a1-30bd-421d-bc11-d9bcebd10f4f","Content-type":"application/json"})

        #print(response.status_code)
        if 'COMPLETE' not in str(response.text):
            print(response.status_code)
            print(fulfilmentId)
            print(response.text)


run([000,000,000])
