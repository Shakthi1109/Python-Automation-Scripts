import csv, time, datetime, ast, json
from graphqlclient import GraphQLClient

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("bearer b0f8ae87-a2d9-4034-ae31-92b2bc059d64")

def process(fulfilmentList):
    i = 1
    with open('output.csv','w') as f:

        for ffId in fulfilmentList:
            query = "query{"
            query += "orderById(id:\"" +str(ffId)+ "\"){ref createdOn}"
            query += "}"
            response = client.execute(query)
            response = json.loads(response)
            print(i, end=' ')
            print(response['data']['orderById']['ref'])
            f.write(str(ffId))
            f.write(',')
            f.write(response['data']['orderById']['ref'])
            f.write(',')
            f.write(response['data']['orderById']['createdOn'])
            f.write('\n')
            #responseList.append(response['data']['fulfilmentById'])
            # responseList.append(response['data']['fulfilmentById']['items']['edges']['node']['requestedQuantity'])
            # responseList.append(response['data']['fulfilmentById']['items']['edges']['node']['filledQuantity'])
            # responseList.append(response['data']['fulfilmentById']['items']['edges']['node']['rejectedQuantity'])
            i=i+1



start = time.time()

process([228857,225682,209151,207029,204553,204376,202920,147545,138694,107496,392880,384959,384959,384526,384526,384526,384526,384526,384526,384090,384090,384090,384090,384090,384090,384090,384090,384090,383201,383201,382818,382818,382818,380989,380989,380989,380989,377397,375066,375066,375066,375066,375066,375066,364007,364007,364007,363359,363359,361875,355409,355409,355409,353571,353571,353571,353186,353186,353186,352722,351530,349587,349587,349401,345490,344885,344885,344885,344885,343744,343474,341641,341619,341619,341619,341619,341619,339791,339791,339791,339741,339026,338613,305249,288430,259821,393631,393652,393698,393698,393698,395372,400690,406957,413946,413946,413946,413946,413946,413946,413946,413946,413946,413946,413946,502433,502433,502433,497735,496943,496943,496943,496901,496901,496643,474742,474742,474742,474228,474228,473836,473196,473162,473124,473090,472850,472695,472621,472417,472082,472082,472000,465618,416929,415393,415393,415358,415358,415358,415358,415358,415358,415358,414644,557423,573983,574926,574947,640113,640113,640113,642382,644668,779279,379132,379132,252136,496374])

print("Time taken: " + str((time.time()-start)/60) + " minutes")
