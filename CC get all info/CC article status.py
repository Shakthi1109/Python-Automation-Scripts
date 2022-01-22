import json, csv, requests, time
from graphqlclient import GraphQLClient
from http.client import IncompleteRead
from datetime import datetime, timedelta

page_query = '''
query($after: String, $first: Int){
  fulfilments(status:"Vencido", after:$after, first:$first){
    pageInfo{
      hasNextPage
    }
    edges{
    cursor
      node{
        id
        status
        attributes{
          name
          value
          type
        }
        articles(first:100){
          pageInfo{
            hasNextPage
          }
          edges{
            node{
              id
              status
            }
          }
        }
        order{
          id
          ref
        }
      }
    }
  }
}
'''
accountId = 'PALACIO'
oauth_url = 'https://palacio.api.fluentretail.com:443/oauth/token?username=elpalaciodehierro_admin&password=GT8Y4Q&client_id=PALACIO&client_secret=44f824ad-eb5d-4936-af10-86ebbcf5be61&grant_type=password&scope=api'
graphql_url = 'https://PALACIO.api.fluentretail.com/graphql'


def get_page_of_data(after,first):
    client = GraphQLClient(graphql_url)
    token = get_token()
    client.inject_token(token)
    response = client.execute(page_query,{'after': after,'first': first})
    response = json.loads(response)
    # print(response)
    return response


def get_token():
    auth_token_response = requests.post(oauth_url)
    if auth_token_response.status_code != 200:
        print("Couldn't get auth token {}".format(auth_token_response.status_code))
    access_token = 'bearer ' + auth_token_response.json()['access_token']
    #print("Access token: {}".format(access_token))
    return access_token


with open('cursor.csv','a') as c, open('output.csv','a') as output:
    c.write('S.No, Fulfilment Id, Cursor\n')
    output.write('Order Id, Order Ref, Fulfilment Id, Fulfilment Status, Article ID, Article Status\n')

    def get_all_data(cursor=None, first=500):
        global response
        response = get_page_of_data(cursor, first)
        if response is not None:
            with open('cursor.csv','a') as c, open('output.csv','a') as output:
                # print(response)
                m=len(response['data']['fulfilments']['edges'])
                print(m)
                for j in range (0,m):
                    # print(j)
                    c.write(str(j)+','+response['data']['fulfilments']['edges'][j]['node']['id']+','+response['data']['fulfilments']['edges'][j]['cursor']+'\n')
                    # output.write(response['data']['fulfilments']['edges'][j]['node']['order']['id']+','+response['data']['fulfilments']['edges'][j]['node']['order']['ref'])
                    # output.write(response['data']['fulfilments']['edges'][j]['node']['id']+','+response['data']['fulfilments']['edges'][j]['node']['status'])
                    attributes=str(response['data']['fulfilments']['edges'][j]['node']['attributes'])
                    if(attributes.find("storeSAPSalesOrderWebhook")>0):
                        o=len(response['data']['fulfilments']['edges'][j]['node']['articles']['edges'])
                        for l in range(0,o):
                            output.write(response['data']['fulfilments']['edges'][j]['node']['order']['id']+','+response['data']['fulfilments']['edges'][j]['node']['order']['ref']+',')
                            output.write(response['data']['fulfilments']['edges'][j]['node']['id']+','+response['data']['fulfilments']['edges'][j]['node']['status'])
                            output.write(','+response['data']['fulfilments']['edges'][j]['node']['articles']['edges'][l]['node']['id'])
                            output.write(','+response['data']['fulfilments']['edges'][j]['node']['articles']['edges'][l]['node']['status'])
                            output.write('\n')



            has_next_page = response['data']['fulfilments']['pageInfo']['hasNextPage']
            print(has_next_page)
            if has_next_page:
                if len(response['data']['fulfilments']['edges']) > 0:
                    cursor = response['data']['fulfilments']['edges'][-1]['cursor']
                get_all_data(cursor)

c.close()
output.close()

start = time.time()

get_all_data()

print("Time taken: " + str((time.time()-start)/60) + " minutes")
