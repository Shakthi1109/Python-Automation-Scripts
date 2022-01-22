import csv, time, datetime, ast, json
from graphqlclient import GraphQLClient

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("bearer afa1bf55-7219-40eb-8454-b13ce00b1600")

def process(fulfilmentList):
    i = 1
    with open('output.csv','w') as f:

        for ffId in fulfilmentList:
            query = "query{"
            query += "fulfilmentById(id:\"" +str(ffId)+ "\"){id status}"
            query += "}"
            response = client.execute(query)
            response = json.loads(response)
            print(response)
            print(i, end=' ')
            f.write(response['data']['fulfilmentById']['id'])
            f.write(',')
            f.write(response['data']['fulfilmentById']['status'])
            f.write('\n')
            #responseList.append(response['data']['fulfilmentById'])
            # responseList.append(response['data']['fulfilmentById']['items']['edges']['node']['requestedQuantity'])
            # responseList.append(response['data']['fulfilmentById']['items']['edges']['node']['filledQuantity'])
            # responseList.append(response['data']['fulfilmentById']['items']['e[dges']['node']['rejectedQuantity'])
            i=i+1



start =time.time()

process([])

print("Time taken: " + str((time.time()-start)/60) + " minutes")
