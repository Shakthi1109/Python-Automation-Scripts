import csv, time, datetime, ast, json
from graphqlclient import GraphQLClient

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("bearer 7c7c39d0-e00c-4f5b-950d-2eb35ffac9ba")



def process(fulfilmentList):

    f = open('OrderIDoutput.csv','a')
    f.write('fulfilment Id, Order ID\n')
    i=0
    for ffId in list(fulfilmentList):
        i=i+1
        print(i)
        query = "query{"
        query += "fulfilmentById(id:\"" +str(ffId)+ "\"){order {id}}"
        query += "}"
        response = client.execute(query)
        response = json.loads(response)

        f.write(str(ffId)+',')
        for attribute in response['data']['fulfilmentById']['order']['id']:
            f.write(str(attribute))

        f.write('\n')
    f.close()

    # with open('output.txt','w') as f:
    #     #f.write("id \t status \t ref \t requestedQuantity \t filledQuantity \t rejectedQuantity")
    #     f.write(str(responseList))


start = time.time()

process([229336,300271,423760,15803,96622,95324,93862,93659,59546,59009,58629,108826,104303,103793,102475,72615,74175,100380,105889,113944])

print("Time taken: " + str((time.time()-start)/60) + " minutes")
