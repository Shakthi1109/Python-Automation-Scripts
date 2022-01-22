import json, csv, requests, time
from graphqlclient import GraphQLClient
from http.client import IncompleteRead
from datetime import datetime, timedelta


page_query = '''
query($after: String,$first: Int, $status: [String], $locationId: String!){
  waves(first:$first,after:$after,processingLocation:{ref:$locationId}){
  pageInfo{
    hasNextPage
  }
edges{
  cursor
  node{
    id
    fulfilments(status:$status){
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
'''
accountId = 'PALACIO'
oauth_url = 'https://palacio.api.fluentretail.com:443/oauth/token?username=elpalaciodehierro_admin&password=GT8Y4Q&client_id=PALACIO&client_secret=44f824ad-eb5d-4936-af10-86ebbcf5be61&grant_type=password&scope=api'

entity = "waves"

graphql_url = 'https://PALACIO.api.fluentretail.com/graphql'

def get_page_of_data(after,first):
    client = GraphQLClient(graphql_url)
    token = get_token()

    client.inject_token(token)

    res = client.execute(page_query,{'after': after, 'first': first, 'status':'Asignado','locationId':'1009'})
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

def get_all_data(cursor=None, first=1000):
    global data
    data = get_page_of_data(cursor, first)
    if data is not None:
        new_labels = data[entity]['edges']
        for edge in new_labels:
            if len(edge['node']['fulfilments']['edges']) != 0:
                for fulfilmentEdge in edge['node']['fulfilments']['edges']:
                    print(fulfilmentEdge['node']['id'])
        has_next_page = data[entity]['pageInfo']['hasNextPage']
        if has_next_page:
            if len(new_labels) > 0:
                cursor = new_labels[-1]['cursor']
            get_all_data(cursor)



start = time.time()

get_all_data()

print("Time taken: " + str((time.time()-start)/60) + " minutes")
