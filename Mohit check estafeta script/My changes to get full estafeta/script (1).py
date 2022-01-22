import csv, time, datetime, ast, json
from graphqlclient import GraphQLClient

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("bearer 72b013b8-b48a-4bff-b12d-8bc814e2332a")



def process():
    with open('input.txt','r') as h:
        fulfilmentList = list(set(ast.literal_eval(h.read())))

    f = open('output2.csv','a')
    f.write('fulfilment Id, ESTAFETA_TRACKING_NUMBER\n')
    for ffId in fulfilmentList:
        query = "query{"
        query += "fulfilmentById(id:\"" +str(ffId)+ "\"){id status articles{edges{node{consignmentArticles{edges{node{consignment{consignmentReference}}}}}}}}"
        query += "}"
        response = client.execute(query)
        response = json.loads(response)

        f.write(str(ffId)+','+'\'')
        for attribute in response['data']['fulfilmentById']['articles']['edges'][0]['node']['consignmentArticles']['edges'][0]['node']['consignment']['consignmentReference']:
            # if attribute['consignment'][consignmentReference] is not NULL:
            f.write(str(attribute))
            #f.write(str(ffId)+','+str(attribute['consignmentReference'])+'\n')
        f.write('\n')
    f.close()


start = time.time()

process()

print("Time taken: " + str((time.time()-start)/60) + " minutes")
