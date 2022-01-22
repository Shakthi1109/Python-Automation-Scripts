from graphqlclient import GraphQLClient
import ast, json

def process():
    with open('info.json', 'r') as h:
        content = h.read()
    content = ast.literal_eval(content)
    forCancelation = content['Asignado']   #Ask whether all "py code"? with assignado status is put in forCancelation as list?

    print(forCancelation['singleSkusCount']) #is forCancelation a list?
    print(forCancelation['zeroSkuCount'])
    print(forCancelation['multiSkusCount'])

    if forCancelation['multiSkusCount'] != 0:
        ctr = 0
        for ids in forCancelation['multiSkus']:
            graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
            query = "query{"
            query += "fulfilmentById(id: "+str(ids['id'])+ "){ id items{ edges{ node{ ref id filledQuantity requestedQuantity rejectedQuantity }}} }"
            query += "}"
            client = GraphQLClient(graphqlUrl)
            client.inject_token("Bearer e2fbf158-1139-479c-a9bd-8ab5cf8d2e7a")
            response = client.execute(query)
            response = json.loads(response)
            #print(response['data']['fulfilmentById']['id'])
            for edge in response['data']['fulfilmentById']['items']['edges']:
                if edge['node']['requestedQuantity'] != edge['node']['rejectedQuantity']:
                    if edge['node']['filledQuantity'] == 0:
                        updateQuery = "mutation{"
                        updateQuery += "updateFulfilment(input: {id: \""+str(ids['id'])+ "\",items:{id:\""+str(edge['node']['id'])+"\",rejectedQuantity:"+str(edge['node']['requestedQuantity'])+"} }){ id items{ edges{ node{filledQuantity requestedQuantity rejectedQuantity }}} }"
                        updateQuery += "}"
                        #print(updateQuery)
                        client = GraphQLClient(graphqlUrl)
                        client.inject_token("Bearer e2fbf158-1139-479c-a9bd-8ab5cf8d2e7a")
                        updateResponse = client.execute(updateQuery)
                        updateResponse = json.loads(updateResponse)
                    else:
                        print(response)
                else:
                    print(response)
        print(ctr)
process()
