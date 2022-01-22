import csv, time, datetime, ast, json
from graphqlclient import GraphQLClient

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("bearer 567263ad-d75c-4cfb-9037-112742033216")



def process(fulfilmentList):

    f = open('OrderIDoutput.csv','a')
    f.write('Order Ref, Order ID\n')
    i=0
    for ffId in list(fulfilmentList):
        i=i+1
        print(i)
        query = "query{"
        query += "order(ref:\""+str(ffId)+"\"){id}"
        query += "}"
        response = client.execute(query)
        response = json.loads(response)

        f.write(str(ffId)+',')
        for attribute in response['data']['order']['id']:
            f.write(str(attribute))

        f.write('\n')
    f.close()

    # with open('output.txt','w') as f:
    #     #f.write("id \t status \t ref \t requestedQuantity \t filledQuantity \t rejectedQuantity")
    #     f.write(str(responseList))


start = time.time()

process([1001752078,1001788000,1001788498,1001788630,1001788745,1001789304,1001789304,1001789366,1001790460,1001790645,1001791045,1001791904,1001792399,1001792430,1001793343,1001794537,1001794561,2001789100,3001769989,3001769989,3001769989,3001787232,3001788241,3001790834,3001790845,3001795063])

print("Time taken: " + str((time.time()-start)/60) + " minutes")
