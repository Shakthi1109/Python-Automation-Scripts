from graphqlclient import GraphQLClient
import ast, json

def updateRejectQty():

    with open('input.txt','r') as h:
        fulfilmentList = list(ast.literal_eval(h.read()))

    # graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
    graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
    client = GraphQLClient(graphqlUrl)
    client.inject_token("Bearer 479b3a26-527d-451d-a0db-08339e8a3895")

    for ids in fulfilmentList:
        print(ids)
        #query = "query{  fulfilmentById(id:\""+str(ids)+"\"){    id    status  }}"
        query = "query{"
        query += "fulfilmentById(id: "+str(ids)+ "){ id items{ edges{ node{ ref id filledQuantity requestedQuantity rejectedQuantity }}} }"
        query += "}"

        response = client.execute(query)
        response = json.loads(response)

        for edge in response['data']['fulfilmentById']['items']['edges']:
            if (edge['node']['requestedQuantity'] != edge['node']['rejectedQuantity']):
                #and edge['node']['filledQuantity'] == 0

                updateQuery = "mutation{"
                updateQuery += "updateFulfilment(input: {id: \""+str(ids)+ "\",items:{id:\""+str(edge['node']['id'])+"\",rejectedQuantity:"+str(edge['node']['requestedQuantity'])+",filledQuantity:"+"0"+"} }){ id items{ edges{ node{filledQuantity requestedQuantity rejectedQuantity }}} }"
                updateQuery += "}"

                #print(updateQuery)
                updateResponse = client.execute(updateQuery)
                updateResponse = json.loads(updateResponse)

            else:
                print(updateResponse)


updateRejectQty()
