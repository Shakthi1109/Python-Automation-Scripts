import json, csv, requests, time
from graphqlclient import GraphQLClient

query_gql = '''
query($ref:String){
  order(ref:$ref){
    id
    status
    createdOn
    fulfilments(first:1000){
      edges{
        node{
          createdOn
          id
          status
          items{
            edges{
              node{
                ref
                id
                requestedQuantity
                filledQuantity
                rejectedQuantity
              }
            }
          }
        }
      }
    }
  }
}
'''

graphql_url = 'https://PALACIO.api.fluentretail.com/graphql'



orderRefs = [3001210054]



def get_page_of_data():
    f1 = open('lessThan10.csv', 'a', newline='')
    w1 = csv.writer(f1)
    w1.writerow([
        'Order Ref',
        'Order Id',
        'Order Status',
        'Order createdOn',
        'Fulfilment Id',
        'Fulfilment Status',
        'Fulfilment createdOn',
        'SKU ref',
        'Item Id',
        'requestedQuantity',
        'filledQuantity',
        'rejectedQuantity'
        ])

    f2 = open('moreThan10.csv', 'a', newline='')
    w2 = csv.writer(f2)
    w2.writerow([
        'Order Ref',
        'Order Id',
        'Order Status',
        'Order createdOn',
        'Fulfilment Id',
        'Fulfilment Status',
        'Fulfilment createdOn',
        'SKU ref',
        'Item Id',
        'requestedQuantity',
        'filledQuantity',
        'rejectedQuantity'
        ])

    client = GraphQLClient(graphql_url)
    #token = get_token()
    client.inject_token('bearer e9fc9390-d157-4e85-b58e-81cb9400ffd3')
    fulfilments = []
    for refs in orderRefs:
        res = client.execute(query_gql,{'ref': refs})
        data = json.loads(res)['data']
        #print(data)
        #print(len(data['order']['fulfilments']['edges']))

        # segregating on the basis of fulfilment count
        if len(data['order']['fulfilments']['edges']) < 10:
            for edge in data['order']['fulfilments']['edges']:
                #print(edge)
                for item in edge['node']['items']['edges']:
                    w1.writerow([
                        str(refs),
                        data['order']['id'],
                        data['order']['status'],
                        data['order']['createdOn'],
                        edge['node']['id'],
                        edge['node']['status'],
                        edge['node']['createdOn'],
                        item['node']['ref'],
                        item['node']['id'],
                        item['node']['requestedQuantity'],
                        item['node']['filledQuantity'],
                        item['node']['rejectedQuantity']
                      ])
        else:
            for edge in data['order']['fulfilments']['edges']:
                for item in edge['node']['items']['edges']:
                    w2.writerow([
                        str(refs),
                        data['order']['id'],
                        data['order']['status'],
                        data['order']['createdOn'],
                        edge['node']['id'],
                        edge['node']['status'],
                        edge['node']['createdOn'],
                        item['node']['ref'],
                        item['node']['id'],
                        item['node']['requestedQuantity'],
                        item['node']['filledQuantity'],
                        item['node']['rejectedQuantity']
                      ])
    f1.close()
    f2.close()





start = time.time()

get_page_of_data()

print('processed {} orders ids, time taken: {} minutes'.format(str(len(orderRefs)),str((time.time()-start)/60)))
