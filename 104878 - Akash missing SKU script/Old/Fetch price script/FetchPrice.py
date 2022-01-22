import csv, time, datetime, ast, json
from graphqlclient import GraphQLClient

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("bearer 455e2505-dd7e-4433-a09b-77ff7bbc4e4f")

def process():

    orderList=[577226,574968,574959,574958,574954,574950,574947,574946,574926,574926,574924,574923,574922,574920,574919,574915,574912,574912,574912,574912,574912,574911,574911,574907,574906,574903,574903,574903,574163,573983,557423,552971,545570,540234,526009,516448]

    SKUList=[39054452,39873392,40747110,40831579,41148920,40831409,41143406,40749448,41204245,40430343,39364908,41022642,40675814,38745602,40878458,40144025,39414310,18289417,36777296,11167815,39544704,41204245,40381886,41181798,40831579,10860035,12174165,12709435,39013339,40205502,39693678,16854925,40033572,40445652,40643574,'TestProduct1']

    with open('output.csv','a') as f:
        f.write('Order ID, SKU Ref, Required Quantity, Price'+'\n')

        for i in range(len(orderList)):
            query = "query{"
            query += "orderById(id:\""+str(orderList[i])+"\"){items(ref:\""+str(SKUList[i])+"\"){edges{node{id quantity price }}}}"
            query += "}"

            response = client.execute(query)
            response = json.loads(response)
            print(i)
            # f.write(str(response['data']['orderById']['items']['edges']['node']['quantity'])+',')
            # f.write(str(response['data']['orderById']['items']['edges']['node']['price'])+'\n')
            f.write(str(orderList[i])+','+str(SKUList[i])+',')
            f.write(str(response['data']['orderById']['items']['edges'][0]['node']['quantity'])+',')

            f.write(str(response['data']['orderById']['items']['edges'][0]['node']['price'])+'\n')





start = time.time()

process()

print("Time taken: " + str((time.time()-start)/60) + " minutes")
