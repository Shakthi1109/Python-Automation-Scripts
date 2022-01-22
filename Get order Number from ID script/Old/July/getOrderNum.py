import csv, time, datetime, ast, json
from graphqlclient import GraphQLClient

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("bearer 9fbdc821-b278-4fd1-997c-4d7d1d96df06")



def process(fulfilmentList):

    f = open('out.csv','a')
    f.write('Order ID, Order Ref\n')
    i=0
    for ffId in list(fulfilmentList):
        i=i+1
        print(i)
        query = "query{"
        query += "order(id:\""+str(ffId)+"\"){ref}"
        query += "}"
        response = client.execute(query)
        response = json.loads(response)

        f.write(str(ffId)+',')
        for attribute in response['data']['order']['ref']:
            f.write(str(attribute))

        f.write('\n')
    f.close()

    # with open('output.txt','w') as f:
    #     #f.write("id \t status \t ref \t requestedQuantity \t filledQuantity \t rejectedQuantity")
    #     f.write(str(responseList))


start = time.time()

process([258370,257490,257361,257361,257361,256956,256956,256324,256143,256143,256143,256143,256143,255796,255796,255764,255290,253537,252633,252633,252577,252432,252432,252267,252267,252264,252136,252014,251841,251841,251841,251841,251761,251761,251761,251761,251761,251761,251761,251761,251539,251539,251539])

print("Time taken: " + str((time.time()-start)/60) + " minutes")
