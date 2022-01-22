import json, csv, requests, time
from graphqlclient import GraphQLClient
from http.client import IncompleteRead
from datetime import datetime, timedelta


page_query = '''
query($after: String, $from: DateTime, $to: DateTime){
  fulfilments(createdOn: {from: $from, to: $to}, status: "Enviado al Cliente", after: $after) {
    pageInfo{
      hasNextPage
    }
    edges {
      cursor
      node {
        id
        fromLocation {
          ref
        }
        order {
          ref
          id
          status
        }
        articles(first:100) {
          edges {
            node {
              id
              status
              consignmentArticles {
                edges {
                  node {
                    consignment {
                      consignmentReference
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
}
'''
accountId = 'PALACIO'
oauth_url = 'https://palacio.api.fluentretail.com:443/oauth/token?username=elpalaciodehierro_admin&password=GT8Y4Q&client_id=PALACIO&client_secret=44f824ad-eb5d-4936-af10-86ebbcf5be61&grant_type=password&scope=api'

graphql_url = 'https://PALACIO.api.fluentretail.com/graphql'
entity = 'fulfilments'
f = open('july.csv','a')
'''f.write('cursor,fulfilment id,fulfilment status,fromLocation ref,order ref,order id,order status,\
        article id,article status,consignmentReference(estafeta)'+'\n')'''

def get_page_of_data(after):
    client = GraphQLClient(graphql_url)
    #token = get_token()

    client.inject_token('bearer 321007bd-ec91-429d-ac82-3d89e8dd7c08')

    res = client.execute(page_query,{'after': after, 'from':'2020-07-01', 'to':'2020-07-31'})
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
    data = get_page_of_data(cursor)
    if data is not None:
        new_labels = data[entity]['edges']
        for edge in new_labels:
            if len(edge['node']['articles']['edges']) != 0:
                for article in edge['node']['articles']['edges']:
                    if len(article['node']['consignmentArticles']['edges']) == 0:
                        f.write(edge['cursor'] + ',' +\
                                edge['node']['id'] + ',' +\
                                'Enviado al Cliente' + ',' +\
                                edge['node']['fromLocation']['ref'] + ',' +\
                                edge['node']['order']['ref'] + ',' +\
                                edge['node']['order']['id'] + ',' +\
                                edge['node']['order']['status'] + ',' +\
                                article['node']['id'] + ',' +\
                                article['node']['status'] + ',' +\
                                "'"'\n')
                    else:
                        for consignment in article['node']['consignmentArticles']['edges']:
                            f.write(edge['cursor'] + ',' +\
                                    edge['node']['id'] + ',' +\
                                    'Enviado al Cliente' + ',' +\
                                    edge['node']['fromLocation']['ref'] + ',' +\
                                    edge['node']['order']['ref'] + ',' +\
                                    edge['node']['order']['id'] + ',' +\
                                    edge['node']['order']['status'] + ',' +\
                                    article['node']['id'] + ',' +\
                                    article['node']['status'] + ',' +\
                                    "'"+consignment['node']['consignment']['consignmentReference']+ '\n')

        has_next_page = data[entity]['pageInfo']['hasNextPage']
        if has_next_page:
            if len(new_labels) > 0:
                cursor = new_labels[-1]['cursor']
            get_all_data(cursor)



start = time.time()

get_all_data()
f.close()
print("Time taken: " + str((time.time()-start)/60) + " minutes")
