import csv, time, datetime, ast, json
from graphqlclient import GraphQLClient

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("bearer fb19c536-7eac-4a19-9ffc-07b17caaefec")

def process():
    # with open('input.txt','r') as h:
    #     fulfilmentList = list(ast.literal_eval(h.read()))

    responseList = []
    z = 1
    with open('output.csv','w') as f:
        f.write('Fulfilment ID, Fulfilment Status, CreatedOn,SKU ref, requestedQuantity, filledQuantity, rejectedQuantity\n')
        for ffId in range(-1,-100,-1):
            query = "query{"
            query += "fulfilmentItems(requestedQuantity: "+str(ffId)+",first: 5000){edges{node{fulfilment{id status createdOn items{edges{node{ref requestedQuantity filledQuantity rejectedQuantity}}}}}}}"
            query += "}"
            response = client.execute(query)
            response = json.loads(response)

            # print(response['data']['fulfilmentById']['id'], end=' ')
            # print(response['data']['fulfilmentById']['status'])
            #responseList.append(response['data']['fulfilmentItems']['edges'][0]['node']['fulfilment']['id'])
            # responseList.append(response['data']['fulfilmentById']['status'])
            edge1=len(response['data']['fulfilmentItems']['edges'])


            #f.write(str(response))
            for i in range(0,edge1):
                edge2=len(response['data']['fulfilmentItems']['edges'][i]['node']['fulfilment']['items']['edges'])
                for j in range(0,edge2):

                    f.write(response['data']['fulfilmentItems']['edges'][i]['node']['fulfilment']['id'])
                    f.write(',')
                    f.write(response['data']['fulfilmentItems']['edges'][i]['node']['fulfilment']['status'])
                    f.write(',')
                    f.write(response['data']['fulfilmentItems']['edges'][i]['node']['fulfilment']['createdOn'])
                    f.write(',')
                    f.write(response['data']['fulfilmentItems']['edges'][i]['node']['fulfilment']['items']['edges'][j]['node']['ref'])
                    f.write(',')
                    f.write(str(response['data']['fulfilmentItems']['edges'][i]['node']['fulfilment']['items']['edges'][j]['node']['requestedQuantity']))
                    f.write(',')
                    f.write(str(response['data']['fulfilmentItems']['edges'][i]['node']['fulfilment']['items']['edges'][j]['node']['filledQuantity']))
                    f.write(',')
                    f.write(str(response['data']['fulfilmentItems']['edges'][i]['node']['fulfilment']['items']['edges'][j]['node']['rejectedQuantity']))

                    # f.write(response['data']['fulfilmentById']['status'])
                    f.write('\n')
                    #responseList.append(response['data']['fulfilmentById'])
                    # responseList.append(response['data']['fulfilmentById']['items']['edges'][0]['node']['requestedQuantity'])
                    # responseList.append(response['data']['fulfilmentById']['items']['edges'][0]['node']['filledQuantity'])
                    # responseList.append(response['data']['fulfilmentById']['items']['edges'][0]['node']['rejectedQuantity'])
                    responseList.append('\n')
                print(z)
                z=z+1


        #print(len(responseList))



start = time.time()

process()

print("Time taken: " + str((time.time()-start)/60) + " minutes")
