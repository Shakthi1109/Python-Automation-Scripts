import json, csv, requests, time
from graphqlclient import GraphQLClient
from http.client import IncompleteRead
from datetime import datetime, timedelta

page_query = '''
query($after: String){
  orders(type:"CC", after: $after){
    pageInfo{
      hasNextPage
    }
    edges{
      cursor
      node{
        id
        ref
        status
        fulfilments(first:100){
          edges{
            node{
              id
              status
              toAddress{
                ref
              }
              articles(status:"Reintegrado a Stock", first:100){
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
f = open('FRS-109641_Art_Reintegradoa_Stock_test.csv','a')
f.write('Cursor, order Id, order Ref, order Status, fulfilment Id, fulfilment Status, to Address Ref, article Id, article Status'+'\n')

def get_page_of_data(after):
    client = GraphQLClient(graphql_url)
    #token = get_token()
    client.inject_token('bearer 18c221a6-3501-40e1-ab96-23ea96342ae7')
    res = client.execute(page_query, {​'after':after}​)
    #print(res)
    data = json.loads(res)['data']
    return data

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
