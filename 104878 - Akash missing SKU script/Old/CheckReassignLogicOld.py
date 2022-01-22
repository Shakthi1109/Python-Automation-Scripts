import json, csv, requests, time, ast
from graphqlclient import GraphQLClient
from http.client import IncompleteRead
from datetime import datetime, timedelta

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("bearer 4dbb2747-40b3-4c2a-b01b-5cfd4fad8470")

def process():



    query = '''
query($after: String){
  orders(createdOn:{
    from:"2020-11-09T00:00:00.192Z" to:"2020-11-09T23:59:59.192Z"
  }, first:500,after:$after){

    edges{
      cursor
      node{

        id
        items{
          edges{
            node{
              ref
            }
          }
        }
        fulfilments{
          edges{
            node{
              id
              items{
                edges{
                  node{
                    ref

                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
'''

    with open('output.csv','w') as f:

        response = client.execute(query)
        response = json.loads(response)
        # print(response)
        f.write('S.No, Order Id, SKU Refs, Fulfilment ID, SKU REFS, Result\n')
        m=len(response['data']['orders']['edges'])
        print(m)
        for j in range (0,m):
            orderSKU=[]
            FulfilmentSKU=[]
            f.write(str(j+1))
            print(j+1)
            f.write(',')
            f.write(response['data']['orders']['edges'][j]['node']['id'])
            f.write('\n')


            n=len(response['data']['orders']['edges'][j]['node']['items']['edges'])
            for k in range(0,n):
                f.write(',')
                f.write(',')
                f.write(response['data']['orders']['edges'][j]['node']['items']['edges'][k]['node']['ref'])
                orderSKU.append(response['data']['orders']['edges'][j]['node']['items']['edges'][k]['node']['ref'])

                f.write('\n')


            o=len(response['data']['orders']['edges'][-1][j]['node']['fulfilments']['edges'])

            for l in range(0,o):
                f.write(',')
                f.write(',')
                f.write(',')
                f.write(response['data']['orders']['edges'][j]['node']['fulfilments']['edges'][l]['node']['id'])
                f.write('\n')

                p=len(response['data']['orders']['edges'][j]['node']['fulfilments']['edges'][l]['node']['items']['edges'])

                for mm in range(0,p):
                    f.write(',')
                    f.write(',')
                    f.write(',')
                    f.write(',')
                    f.write(response['data']['orders']['edges'][j]['node']['fulfilments']['edges'][l]['node']['items']['edges'][mm]['node']['ref'])
                    FulfilmentSKU.append(response['data']['orders']['edges'][j]['node']['fulfilments']['edges'][l]['node']['items']['edges'][mm]['node']['ref'])
                    f.write('\n')
            if(len(set(orderSKU).symmetric_difference(set(FulfilmentSKU)))==0):
                f.write(',')
                f.write(',')
                f.write(',')
                f.write(',')
                f.write(',')
                f.write('All SKUs present')
                f.write('\n')
            else:
                f.write(',')
                f.write(',')
                f.write(',')
                f.write(',')
                f.write(',')
                f.write(str(set(orderSKU).symmetric_difference(set(FulfilmentSKU))))
                f.write('\n')
            # print(orderSKU)
            # print(set(FulfilmentSKU))


        # responseList.append(response['data']['fulfilmentById']['id'])
        # responseList.append(response['data']['fulfilmentById']['status'])
        # f.write(response['data']['fulfilmentById']['id'])
        # f.write(',')
        # f.write(response['data']['fulfilmentById']['status'])
        # f.write('\n')
        #responseList.append(response['data']['fulfilmentById'])
        # responseList.append(response['data']['fulfilmentById']['items']['edges']['node']['requestedQuantity'])
        # responseList.append(response['data']['fulfilmentById']['items']['edges']['node']['filledQuantity'])
        # responseList.append(response['data']['fulfilmentById']['items']['edges']['node']['rejectedQuantity'])
        #responseList.append('\n')
        #i=i+1

        #print(len(responseList))



start = time.time()

process()

print("Time taken: " + str((time.time()-start)/60) + " minutes")
