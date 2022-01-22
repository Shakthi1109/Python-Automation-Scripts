import json
import csv
import requests
from graphqlclient import GraphQLClient
from http.client import IncompleteRead
from datetime import datetime

page_query = '''
query($after: String,$first: Int, $count: Int){
orders(createdOn:{from:"2020-07-10T00:00:00.993Z",to:"2020-07-10T01:00:00.993Z"},after: $after,first: $first){
    pageInfo{
      hasNextPage
    }
  edges{
    cursor
    node{
      id
      ref
      createdOn
      items(first:$count){
        edges{
          node{
            ref
            quantity
            id
          }
        }
      }
      fulfilments(first:$count){
        edges{
          node{
            id
            status
            items(first:$count){
              edges{
                node{
                  ref
                  rejectedQuantity
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
}
'''
accountId = 'PALACIO'
oauth_url = ''

entity = "orders"

cols=['Order Id','Order Ref','Order createdOn','Item Ref','Fulfilment Id','Fulfilment Status','Pending Qty']

fields_order=['id','ref','createdOn']


graphql_url = 'https://PALACIO.api.fluentretail.com/graphql'
filename ='test_data4.csv'

def get_page_of_data(after,first,count):
    client = GraphQLClient(graphql_url)
    client.inject_token("bearer 00e4276f-46e7-4b8b-be0d-233fd85711bc")
    res = client.execute(page_query,{'after': after, 'first': first, 'count':count})
    data = json.loads(res)['data']
    return data


def get_token():
    auth_token_response = requests.post(oauth_url)
    if auth_token_response.status_code == 200:
        print(auth_token_response.json())
    else:
        print("Couldn't get auth token {}".format(auth_token_response.status_code))
    access_token = 'bearer ' + auth_token_response.json()['access_token']
    print("Access token: {}".format(access_token))
    return access_token

def get_all_data(all_labels=[], cursor=None, first=500, count=20, retries_left=5):
    global data
    try:
        data = get_page_of_data(cursor, first, count)
    except IncompleteRead:
        print('reconnect and keep tracking')
        if retries_left > 0:
            retries_left = retries_left - 1
           
            get_all_data(all_labels, cursor, retries_left)
        else:
            print('retries exhausted')
            return all_labels
    except:
        print("error occurred for cursor: {} retrying with retries left:{}".format(cursor, retries_left))
        if retries_left > 0:
            retries_left -=1
            get_all_data(all_labels, cursor, retries_left)
        else:
            print('retries exhausted')
            return all_labels
    if data is not None:
        new_labels = data[entity]['edges']
        has_next_page = data[entity]['pageInfo']['hasNextPage']
        all_labels = all_labels+new_labels
        if has_next_page:
            if len(new_labels) > 0:
                cursor = get_cursor(new_labels)
            all_labels = get_all_data(all_labels, cursor)
    return all_labels


def get_cursor(new_labels):
    if len(new_labels) > 0:
        last = len(new_labels) - 1
        while True:
            if 'cursor' in new_labels[last]:
                return new_labels[last]['cursor']
            else:
                last -= 1
                if 'cursor' in new_labels[last]:
                    return new_labels[last]['cursor']
    else:
        pass


def write_to_csv(all_labels):
    file = csv.writer(open(filename, "wt"), delimiter=',')
    file.writerow(cols)
    for var1 in all_labels:
        if len(var1.keys()) > 0:
            flag=0
            row = []
            items_concat_ref= []
            items_concat_quantity= []
            fulfilment_concat_ref=[]
            fulfilment_concat_status=[]
            pend_quant=[]
            item_pend=[]
            diff=0
            for field in fields_order:
                if len(var1)>0:
                    row.append(var1['node'][field])
                else:
                    row.append('')
            for x in var1['node']['items']['edges']:
                if(len(x)>0):
                    items_concat_ref.append(x['node']['ref'])
                    items_concat_quantity.append(x['node']['quantity'])
            row.append(items_concat_ref)
            
            for m in var1['node']['fulfilments']['edges']:
                if(len(m)>0):
                    fulfilment_concat_ref.append(m['node']['id'])
                    fulfilment_concat_status.append(m['node']['status'])
            row.append(fulfilment_concat_ref)
            row.append(fulfilment_concat_status)
            
            for t in range(0,len(items_concat_ref)): 
                for y in var1['node']['fulfilments']['edges']:
                    if(len(y)>0):
                        for z in y['node']['items']['edges']:
                            if z['node']['ref']==items_concat_ref[t] and (y['node']['status']=="RMA Reintegro de Inventario" or y['node']['status']=="RMA Reverso de Pago Aplicado"):
                                diff=diff+z['node']['requestedQuantity']-z['node']['rejectedQuantity']
                                items_concat_quantity[t]=items_concat_quantity[t]-diff
                            
                            elif z['node']['ref']==items_concat_ref[t]:
                                diff=diff+z['node']['requestedQuantity']-z['node']['rejectedQuantity']
                                
                                
                pend_quant.append(items_concat_quantity[t]-diff)
           
                diff=0
            
            for x in range(0,len(items_concat_ref)):
                if pend_quant[x]!=0:
                    item_pend.append([items_concat_ref[x],pend_quant[x]])
            row.append(item_pend)    
                
               
        for n in pend_quant:
            if n!=0 and len(var1['node']['fulfilments']['edges'])>0 :
                flag=1
        if flag==1:
            file.writerow(row)


result = get_all_data()
write_to_csv(result)

