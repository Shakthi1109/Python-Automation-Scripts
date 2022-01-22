import csv, time, datetime, ast, json
from graphqlclient import GraphQLClient

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("bearer 4dbb2747-40b3-4c2a-b01b-5cfd4fad8470")

def process():

    query1 = '''
query{
  fulfilmentById(id:"67680"){
    order{
      id
      createdOn
      fulfilments{
        edges{
          node{
            items{
              edges{
                node{
                  ref
                  requestedQuantity
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

    query2 = '''
query{
  fulfilmentOptions(createdOn:{
    from:"2020-11-09T19:48:14.433Z" to:"2020-11-09T19:53:14.433Z"
  }){
    edges{
      node{
        plans{
          edges{
            node{

              fulfilments{
                locationRef
                items{
                  productRef
                  availableQuantity
                  requestedQuantity

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
        for ffId in fulfilmentList:
            response1 = client.execute(query1)
            response1 = json.loads(response1)
            # print(response)
            m=len(response['data']['orders']['edges'])
            print(m)
            for j in range (0,m):
                print(j)
                print(response['data']['orders']['edges'][j]['node']['id'])

                n=len(response['data']['orders']['edges'][j]['node']['items']['edges'])
                for k in range(0,n):
                    print(response['data']['orders']['edges'][j]['node']['items']['edges'][k]['node']['ref'])

                o=len(response['data']['orders']['edges'][j]['node']['fulfilments']['edges'])
                for l in range(0,o):
                    print(response['data']['orders']['edges'][j]['node']['fulfilments']['edges'][l]['node']['id'])

                    p=len(response['data']['orders']['edges'][j]['node']['fulfilments']['edges'][l]['node']['items']['edges'])
                    for mm in range(0,p):
                        print(response['data']['orders']['edges'][j]['node']['fulfilments']['edges'][l]['node']['items']['edges'][mm]['node']['ref'])
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
