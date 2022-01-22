from graphqlclient import GraphQLClient
import ast, json
import requests


def process():

    with open('file.txt','r') as h:
        fulfilmentList = list(set(ast.literal_eval(h.read())))

    for ids in fulfilmentList:

        graphqlUrl = 'https://bridge.sandbox.api.fluentretail.com/graphql'
        query = "query{"
        query += "fulfilmentById(id: "+str(ids)+ "){ id items{ edges{ node{ ref id filledQuantity requestedQuantity rejectedQuantity }}} }"
        query += "}"

        client = GraphQLClient(graphqlUrl)
        client.inject_token("bearer 8edb88fd-400a-4b6d-945d-7afc99f52fda")
        response = client.execute(query)
        response = json.loads(response)


    ReassignURL = 'https://bridge.sandbox.api.fluentretail.com/api/v4.1/event/sync'

    #code to update the rejected quantities
        for edge in response['data']['fulfilmentById']['items']['edges']:
            if (edge['node']['requestedQuantity'] != edge['node']['rejectedQuantity']) and edge['node']['filledQuantity'] == 0:

                updateQuery = "mutation{"
                updateQuery += "updateFulfilment(input: {id: \""+str(ids)+ "\",items:{id:\""+str(edge['node']['id'])+"\",rejectedQuantity:"+str(edge['node']['requestedQuantity'])+"} }){ id items{ edges{ node{filledQuantity requestedQuantity rejectedQuantity }}} }"
                updateQuery += "}"
                #print(updateQuery)
                client = GraphQLClient(graphqlUrl)
                client.inject_token("bearer 8edb88fd-400a-4b6d-945d-7afc99f52fda")
                updateResponse = client.execute(updateQuery)
                updateResponse = json.loads(updateResponse)
            else:
                print(response)


            #code for Reassign SKU
            body = {
            "retailerId": "4",
            "entityId": str(ids),
            "name": "REASSIGN_SKU_TO_REJECT_LOCATION",
            "entityType": "FULFILMENT",
            "entityStatus": response['data']['fulfilmentById']['status'],       #is it correct
            "attributes": {
                "skuReference": edge['node']['ref'],                            #is it correct
                "reassignQuantity": edge['node']['requestedQuantity'],
                "locationReference": "REJECTLOC"
                }
            }


            x = requests.post(ReassignURL,
                                data = json.dumps(body),
                                headers = {"Authorization": "Bearer e5b7e8a1-30bd-421d-bc11-d9bcebd10f4f","Content-type":"application/json"})


            if 'COMPLETE' not in str(response.text):
            print(response.status_code)
            print(fulfilmentId)
            print(response.text)

process()
