from graphqlclient import GraphQLClient
import ast, json

def updateStatus():

    with open('input.txt','r') as h:
        fulfilmentList = list(ast.literal_eval(h.read()))

    graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
    client = GraphQLClient(graphqlUrl)
    client.inject_token("Bearer 479b3a26-527d-451d-a0db-08339e8a3895")

    for ids in fulfilmentList:
        print(ids)
        #query = "query{  fulfilmentById(id:\""+str(ids)+"\"){    id    status  }}"

        updateQuery = "mutation{"
        updateQuery += "updateFulfilment(input: {id: \""+str(ids)+ "\", status: \"Asignado\" }){ id status }"
        updateQuery += "}"
        #print(updateQuery)
        updateResponse = client.execute(updateQuery)
        #updateResponse = json.loads(updateResponse)
        print(updateResponse)


updateStatus()
