import csv, time, datetime, ast, json
from graphqlclient import GraphQLClient

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("bearer dcd51dea-0735-47a3-b89b-aaac1a182489")

def process(fulfilmentList):
    i = 1
    with open('output.csv','w') as f:

        for ffId in fulfilmentList:
            query = "query{"
            query += "orderById(id:\"" +str(ffId)+ "\"){id status}"
            query += "}"
            response = client.execute(query)
            response = json.loads(response)
            print(response)
            print(i, end=' ')
            f.write(response['data']['orderById']['id'])
            f.write(',')
            f.write(response['data']['orderById']['status'])
            f.write('\n')
            #responseList.append(response['data']['fulfilmentById'])
            # responseList.append(response['data']['fulfilmentById']['items']['edges']['node']['requestedQuantity'])
            # responseList.append(response['data']['fulfilmentById']['items']['edges']['node']['filledQuantity'])
            # responseList.append(response['data']['fulfilmentById']['items']['e[dges']['node']['rejectedQuantity'])
            i=i+1



start =time.time()

process([1306862,1259453,1257918,1257898,1252759,1220114,1220101,1220091,1220046,1220027,1191683,1191512,1106178,1084064,1084045,1074327,1060802,976867])

print("Time taken: " + str((time.time()-start)/60) + " minutes")
