import csv, time, datetime, ast, json
from graphqlclient import GraphQLClient

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("Bearer dcd51dea-0735-47a3-b89b-aaac1a182489")

def updateStatus(fulfilmentList):
    i = 1
    for ids in fulfilmentList:
        #query = "query{  fulfilmentById(id:\""+str(ids)+"\"){    id    status  }}"

        updateQuery = "mutation{"
        updateQuery += "updateOrder(input: {id: \""+str(ids)+ "\", status: \"CREATED\" }){ id status }"
        updateQuery += "}"
        #print(updateQuery)
        updateResponse = client.execute(updateQuery)
        #updateResponse = json.loads(updateResponse)
        print(i, end=' ')
        print(updateResponse)
        i=i+1

start = time.time()

updateStatus([1306862,1259453,1257918,1257898,1252759,1220114,1220101,1220091,1220046,1220027,1191683,1191512,1106178,1084064,1084045,1074327,1060802,976867])

print("Time taken: " + str((time.time()-start)/60) + " minutes")
