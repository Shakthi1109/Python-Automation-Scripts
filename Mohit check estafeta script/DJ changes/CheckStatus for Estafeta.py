import csv, time, datetime, ast, json
from graphqlclient import GraphQLClient

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("bearer 10ee1245-ae88-4176-99da-d3baedaef1de")

def process():
    with open('input.txt','r') as h:
        fulfilmentList = list(set(ast.literal_eval(h.read())))

    responseList = []
    i = 1
    for ffId in fulfilmentList:
        query = "query{"
        query += "fulfilmentById(id:\"" +str(ffId)+ "\"){id status attributes{name type value}}"
        query += "}"
        response = client.execute(query)
        response = json.loads(response)
        print(i, end=' ')
        print(response['data']['fulfilmentById']['id'], end=' ')
        print(response['data']['fulfilmentById']['status'])
        responseList.append(response['data']['fulfilmentById']['id'])
        responseList.append(response['data']['fulfilmentById']['attributes']['name'])
        #responseList.append(response['data']['fulfilmentById'])
        # responseList.append(response['data']['fulfilmentById']['items']['edges']['node']['requestedQuantity'])
        # responseList.append(response['data']['fulfilmentById']['items']['edges']['node']['filledQuantity'])
        # responseList.append(response['data']['fulfilmentById']['items']['edges']['node']['rejectedQuantity'])
        responseList.append(";;;;;")
        i=i+1

    print(len(responseList))
    with open('output.txt','w') as f:
        #f.write("id \t status \t ref \t requestedQuantity \t filledQuantity \t rejectedQuantity")
        f.write(str(responseList))


start = time.time()

process()

print("Time taken: " + str((time.time()-start)/60) + " minutes")
