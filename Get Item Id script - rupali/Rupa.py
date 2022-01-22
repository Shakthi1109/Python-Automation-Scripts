import csv, time, datetime, ast, json
from graphqlclient import GraphQLClient

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("bearer c4ca253a-0cb3-49e8-8c69-81f611c81e8d")

def process():
    with open('output.csv','w') as f:

        fulfilmentList = [31511,32085,33869,35222,36191,37656,46842,51383,58187,59084,60285,66043,67292,74518,78962,79622,93709,94897,253536,253536,101233,103770,103816,103816,2373604,106164,106775,113850,114690,115827,116733,116736]
        SKURefList = [40422566,39961562,40422566,37967153,40422566,40381886,39419923,39419987,38638087,38269944,40050089,39657044,40038348,39242151,38269944,40195301,39009927,38144897,39159133,39159136,37967155,36617321,40283497,37509191,38638087,39419923,36894143,40926247,39200301,39503718,38123920,38123919]

        f.write('fulfilment Id, SKURef, Item Id, Filled Qty \n')

        for i in range(0,len(fulfilmentList)):

            query = "query{"
            query += "fulfilmentById(id:\"" +str(fulfilmentList[i])+ "\"){"
            query += "items(ref:\"" +str(SKURefList[i])+ "\"){ edges { node { id ref filledQuantity } } } }"
            query += "}"
            response = client.execute(query)
            response = json.loads(response)

            n=len(response['data']['fulfilmentById']['items']['edges'])
            for j in range(0,n):
                print(i, end=' ')
                print(response['data']['fulfilmentById'])
                f.write(str(fulfilmentList[i])+',')
                f.write(response['data']['fulfilmentById']['items']['edges'][j]['node']['ref']+',')
                f.write(response['data']['fulfilmentById']['items']['edges'][j]['node']['id']+',')
                f.write(str(response['data']['fulfilmentById']['items']['edges'][j]['node']['filledQuantity'])+',')
                f.write('\n')
                #responseList.append(response['data']['fulfilmentById'])
                # responseList.append(response['data']['fulfilmentById']['items']['edges']['node']['requestedQuantity'])
                # responseList.append(response['data']['fulfilmentById']['items']['edges']['node']['filledQuantity'])
                # responseList.append(response['data']['fulfilmentById']['items']['edges']['node']['rejectedQuantity'])
                i=i+1



start = time.time()

process()

print("Time taken: " + str((time.time()-start)/60) + " minutes")
