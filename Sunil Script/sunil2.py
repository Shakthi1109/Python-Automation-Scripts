import json, csv, requests, time
from graphqlclient import GraphQLClient
from http.client import IncompleteRead
from datetime import datetime, timedelta


page_query = '''
query($after: String, $from: DateTime, $to: DateTime){
  orders(createdOn: {from: $from, to: $to}, type:"CC", after: $after) {
    pageInfo{
     hasNextPage
    }
    edges{
      cursor
      node{
        id
        ref
        status
        fulfilments(first:30){
          edges{
            node{
              id
              status
              toAddress{
                ref
              }
              articles(first:30){
                edges{
                  node{
                    id
                    status
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

graphql_url = 'https://PALACIO.api.fluentretail.com/graphql'
entity = 'orders'
f = open('output.csv','a')
f.write('Cursor, order Id, order Ref, order Status, fulfilment Id, fulfilment Status, to Address Ref, article Id, article Status'+'\n')

def get_page_of_data(after):
    client = GraphQLClient(graphql_url)
    #token = get_token()

    client.inject_token('bearer 27573629-0de8-4c43-b60e-a54fcd07186a')

    res = client.execute(page_query,{'after': after, 'from':'2021-02-04T00:00:00.000Z', 'to':'2021-02-04T23:59:59.999Z'})
    #print(res)
    data = json.loads(res)['data']

    return data


def get_token():
    auth_token_response = requests.post(oauth_url)
    if auth_token_response.status_code != 200:
        print("Couldn't get auth token {}".format(auth_token_response.status_code))
    access_token = 'bearer ' + auth_token_response.json()['access_token']
    #print("Access token: {}".format(access_token))
    return access_token

def get_all_data(cursor=None):
    global data
    i=0
    data = get_page_of_data(cursor)
    if data is not None:
        new_labels = data[entity]['edges']
        for edge in new_labels:
            print(i)
            i=i+1
            for fulfilmentEdge in edge['node']['fulfilments']['edges']:
                if len(fulfilmentEdge['node']['articles']['edges']) != 0:
                    for articleEdge in fulfilmentEdge['node']['articles']['edges']:
                        f.write(edge['cursor'] + ',' +\
                                edge['node']['id'] + ',' +\
                                edge['node']['ref'] + ',' +\
                                edge['node']['status'] + ',' +\
                                fulfilmentEdge['node']['id'] + ',' +\
                                fulfilmentEdge['node']['status'] + ',' +\
                                fulfilmentEdge['node']['toAddress']['ref'] + ',' +\
                                articleEdge['node']['id'] + ',' + \
                                articleEdge['node']['status'] + '\n')
        has_next_page = data[entity]['pageInfo']['hasNextPage']
        if has_next_page:
            if len(new_labels) > 0:
                cursor = new_labels[-1]['cursor']
            get_all_data(cursor)


start = time.time()

get_all_data()
f.close()
print("Time taken: " + str((time.time()-start)/60) + " minutes")
