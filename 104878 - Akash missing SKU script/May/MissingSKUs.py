import json, csv, requests, time
from graphqlclient import GraphQLClient
from http.client import IncompleteRead
from datetime import datetime, timedelta


page_query = '''
query($after: String, $first: Int){
  orders(createdOn:{
    from:"2020-05-01T00:00:00.192Z" to:"2020-05-31T23:59:59.192Z"
  },after:$after, first:$first){
    pageInfo{
      hasNextPage
    }
    edges{
      cursor
      node{
        id
        createdOn
        status
        items(first:100){
          edges{
            node{
              ref
              quantity
              price
            }
          }
        }
        fulfilments(first:100){
          edges{
            node{
              id
              items(first:100){
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
accountId = 'PALACIO'
oauth_url = 'https://palacio.api.fluentretail.com:443/oauth/token?username=elpalaciodehierro_admin&password=GT8Y4Q&client_id=PALACIO&client_secret=44f824ad-eb5d-4936-af10-86ebbcf5be61&grant_type=password&scope=api'
# entity = "waves"
graphql_url = 'https://PALACIO.api.fluentretail.com/graphql'


def get_page_of_data(after,first):
    client = GraphQLClient(graphql_url)
    token = get_token()
    client.inject_token(token)

    response = client.execute(page_query,{'after': after,'first': first})

    response = json.loads(response)
    #print(response)

    return response


def get_token():
    auth_token_response = requests.post(oauth_url)
    if auth_token_response.status_code != 200:
        print("Couldn't get auth token {}".format(auth_token_response.status_code))
    access_token = 'bearer ' + auth_token_response.json()['access_token']
    #print("Access token: {}".format(access_token))
    return access_token



with open('testing.csv','a') as f, open('cursor.csv','a') as c, open('output.csv','a') as output:
    c.write('S.No, Order Id, cursor\n')
    f.write('S.No, Order Id, SKU Refs, Fulfilment ID, SKU REFS, Result\n')
    output.write('Order Id, Status, CreatedOn, SKU Refs, Required Quantity, Price\n')

    def get_all_data(cursor="Y3Vyc29yOi0tLTU0MThfXzE1ODk2ODkwOTgzNDU=", first=100):
        global response
        response = get_page_of_data(cursor, first)
        if response is not None:
            with open('testing.csv','a') as f, open('cursor.csv','a') as c, open('output.csv','a') as output:
                m=len(response['data']['orders']['edges'])
                print(m)
                for j in range (0,m):
                    orderSKU=[]
                    FulfilmentSKU=[]
                    quantity=[]
                    price=[]
                    f.write(str(j+1))
                    print(j+1)
                    c.write(str(j+1)+','+response['data']['orders']['edges'][j]['node']['id']+','+response['data']['orders']['edges'][j]['cursor']+'\n')
                    f.write(','+response['data']['orders']['edges'][j]['node']['id']+'\n')

                    n=len(response['data']['orders']['edges'][j]['node']['items']['edges'])
                    for k in range(0,n):
                        f.write(','+','+response['data']['orders']['edges'][j]['node']['items']['edges'][k]['node']['ref']+'\n')
                        orderSKU.append(response['data']['orders']['edges'][j]['node']['items']['edges'][k]['node']['ref'])
                        quantity.append(response['data']['orders']['edges'][j]['node']['items']['edges'][k]['node']['quantity'])
                        price.append(response['data']['orders']['edges'][j]['node']['items']['edges'][k]['node']['price'])

                    o=len(response['data']['orders']['edges'][j]['node']['fulfilments']['edges'])

                    for l in range(0,o):
                        f.write(','+','+','+response['data']['orders']['edges'][j]['node']['fulfilments']['edges'][l]['node']['id']+'\n')


                        p=len(response['data']['orders']['edges'][j]['node']['fulfilments']['edges'][l]['node']['items']['edges'])

                        for mm in range(0,p):
                            f.write(','+','+','+','+response['data']['orders']['edges'][j]['node']['fulfilments']['edges'][l]['node']['items']['edges'][mm]['node']['ref']+'\n')
                            FulfilmentSKU.append(response['data']['orders']['edges'][j]['node']['fulfilments']['edges'][l]['node']['items']['edges'][mm]['node']['ref'])
                    if(len(set(orderSKU).symmetric_difference(set(FulfilmentSKU)))==0):
                        f.write(','+','+','+','+','+'All SKUs present'+'\n')
                    else:
                        f.write(','+','+','+','+','+str(set(orderSKU).symmetric_difference(set(FulfilmentSKU)))+'\n')

                        #print(','+str(set(orderSKU).symmetric_difference(set(FulfilmentSKU)))+'\n')
                        temp=list(set(orderSKU).symmetric_difference(set(FulfilmentSKU)))
                        ListLen=len(temp)
                        for iterator1 in range(0,ListLen):
                            output.write(response['data']['orders']['edges'][j]['node']['id'])
                            output.write(','+response['data']['orders']['edges'][j]['node']['status'])
                            output.write(','+response['data']['orders']['edges'][j]['node']['createdOn'])
                            output.write(','+str(temp[iterator1]))
                            index=orderSKU.index(temp[iterator1])
                            output.write(','+str(quantity[index]))
                            output.write(','+str(price[index])+'\n')



            has_next_page = response['data']['orders']['pageInfo']['hasNextPage']
            print(has_next_page)
            if has_next_page:
                if len(response['data']['orders']['edges']) > 0:
                    cursor = response['data']['orders']['edges'][-1]['cursor']
                get_all_data(cursor)
f.close()
c.close()
output.close()

start = time.time()

get_all_data()

print("Time taken: " + str((time.time()-start)/60) + " minutes")
