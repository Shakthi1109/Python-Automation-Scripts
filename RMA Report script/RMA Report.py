import json, csv, requests, time
from graphqlclient import GraphQLClient
from http.client import IncompleteRead
from datetime import datetime, timedelta
import re


page_query = '''
query($after: String, $first: Int){
  fulfilments(createdOn:{
    from:"2020-12-23T23:25:37.040Z" to:"2020-12-23T23:25:42.040Z"
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
          }
        }
      }
      attributes{
        name
        value
      }
        order{
          id
          ref
          createdOn
          status
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
    # print(response)
    return response


def get_token():
    auth_token_response = requests.post(oauth_url)
    if auth_token_response.status_code != 200:
        print("Couldn't get auth token {}".format(auth_token_response.status_code))
    access_token = 'bearer ' + auth_token_response.json()['access_token']
    #print("Access token: {}".format(access_token))
    return access_token


def get_Audit(fulfilmentId,currentDate,fulfilDate):


    AuditURL = 'http://palacio.api.fluentretail.com/api/v4.1/event'

    fulldate=currentDate
    year=currentDate[0]+currentDate[1]+currentDate[2]+currentDate[3]
    month=currentDate[5]+currentDate[6]
    currentDate=currentDate[8]+currentDate[9]
    if(currentDate=='01'):
        previousDate='30'
        if (len(str(abs(int(month))))==1):
            previousMonth=str('0')+str(int(month)-1)
        elif(month=='10'):
            previousMonth='09'
        else:
            previousMonth=str(int(month)-1)

        if (len(str(abs(int(currentDate))))==1):
            nextDate=str('0')+str(int(currentDate)+1)
        elif(currentDate=='09'):
            nextDate='10'
        else:
            nextDate=str(int(currentDate)+1)
        nextMonth=month
    elif(currentDate=='31' or currentDate=='30'):
        nextDate='01'
        if(month=='09'):
            nextMonth='10'
        elif (len(str(abs(int(month))))==1):
            nextMonth=str('0')+str(int(month)+1)
        elif(month=='12'):
            nextMonth='01'
        else:
            nextMonth=str(int(month)+1)
        previousDate=str(int(currentDate)-1)
        previousMonth=month
    else:
        if(len(str(abs(int(currentDate))))==1):
            previousDate='0'+str(int(currentDate)-1)
        elif(currentDate=='10'):
            previousDate='09'
        else:
            previousDate=str(int(currentDate)-1)

        if(currentDate=='09'):
            nextDate='10'
        elif(len(str(abs(int(currentDate))))==1):
            nextDate='0'+str(int(currentDate)+1)
        else:
            nextDate=str(int(currentDate)+1)

        previousMonth=month
        nextMonth=month

    # f.write(fulldate+','+currentDate+'-'+month+'-'+year+','+previousDate+'-'+previousMonth+'-'+year+','+nextDate+'-'+nextMonth+'-'+year)
    fromDate=year+'-'+previousMonth+'-'+previousDate+"T00:00:00.192Z"
    toDate=year+'-'+nextMonth+'-'+nextDate+"T23:59:59.192Z"
    # print("fromDate:{}".format(fromDate))
    # print(type(fromDate))
    # f.write('\n')

    audit = requests.get(AuditURL,
                headers = {"Authorization": "Bearer e9852dc6-ec57-4b0c-ba3e-73187afe48ad","Content-Type":"application/json"},
                params = {"context.rootEntityType":"ORDER","count":"5000","context.rootEntityId":str(fulfilmentId),"from":fromDate}
                )

    # print("\"generatedOn\": "+"\""+fulfilDate[:10])
    # print(audit.text.rfind("\"generatedOn\": "+"\""+fulfilDate[:10]))
    whoRMA=audit.text.rfind("\"generatedOn\": \""+fulfilDate[:10])
    # print(whoRMA)
    whoRMA=audit.text[whoRMA-100:whoRMA]
    # print(whoRMA)
    WhoRMAFirst=whoRMA.find("\"generatedBy\"")
    WhoRMAEnd=whoRMA.find("\"generatedOn\"")
    whoRMA=whoRMA[WhoRMAFirst+17:WhoRMAEnd-7]
    # print(whoRMA)
    return str(whoRMA)



with open('cursor.csv','a') as c, open('output.csv','a') as output:
    c.write('S.No, Order Id, cursor\n')
    output.write('Order Id, Order Ref, Fulfilment Id, Fulfilment Status, SKU Refs, RMA Date, RMA Number, Who Created\n')

    def get_all_data(cursor=None, first=200):
        global response
        global RMANum, printRMA
        response = get_page_of_data(cursor, first)
        if response is not None:
            with open('cursor.csv','a') as c, open('output.csv','a') as output:
                # print(response)
                m=len(response['data']['fulfilments']['edges'])
                print(m)
                for j in range (0,m):
                    print(j)
                    c.write(str(j)+','+response['data']['fulfilments']['edges'][j]['node']['id']+','+response['data']['fulfilments']['edges'][j]['cursor']+'\n')
                    # output.write(response['data']['fulfilments']['edges'][j]['node']['order']['id']+','+response['data']['fulfilments']['edges'][j]['node']['order']['ref'])
                    # output.write(response['data']['fulfilments']['edges'][j]['node']['id']+','+response['data']['fulfilments']['edges'][j]['node']['status'])

                    o=len(response['data']['fulfilments']['edges'][j]['node']['items']['edges'])
                    if "RMA" in response['data']['fulfilments']['edges'][j]['node']['status']:
                        global RMANum, printRMA
                        RMANumberStr=str(response['data']['fulfilments']['edges'][j]['node']['attributes'])
                        RMANumberEnd=len(RMANumberStr)
                        RMANumberStart=RMANumberStr.find("CANCEL_STORE_FULFILMENT_RMA_Number",0,RMANumberEnd)
                        if((str(RMANumberStr.find("CANCEL_STORE_FULFILMENT_RMA_Number",0,RMANumberEnd))).isnumeric()):
                            RMANum=RMANumberStr[RMANumberStart:RMANumberStart+58]
                            valueStart=RMANum.find("'value':",0,len(RMANum))
                            RMANum=RMANum[valueStart+9:]
                            RMANum=RMANum[:-1]

                            # print(RMANum)
                        elif((str(RMANumberStr.find("CANCEL_CEDIS_FULFILMENT_RMA_Number",0,RMANumberEnd))).isnumeric()):
                            RMANumberStart=RMANumberStr.find("CANCEL_CEDIS_FULFILMENT_RMA_Number",0,RMANumberEnd)
                            RMANum=RMANumberStr[RMANumberStart:RMANumberStart+58]
                            valueStart=RMANum.find("'value':",0,len(RMANum))
                            RMANum=RMANum[valueStart+9:]
                            RMANum=RMANum[:-1]

                        elif((str(RMANumberStr.find("CANCEL_CECOM_FULFILMENT_RMA_Number",0,RMANumberEnd))).isnumeric()):
                            RMANumberStart=RMANumberStr.find("CANCEL_CECOM_FULFILMENT_RMA_Number",0,RMANumberEnd)
                            RMANum=RMANumberStr[RMANumberStart:RMANumberStart+58]
                            valueStart=RMANum.find("'value':",0,len(RMANum))
                            RMANum=RMANum[valueStart+9:]
                            RMANum=RMANum[:-1]

                        else:
                            RMANum = "Null"

                        printRMA=get_Audit(str(response['data']['fulfilments']['edges'][j]['node']['order']['id']),str(response['data']['fulfilments']['edges'][j]['node']['order']['createdOn']),str(response['data']['fulfilments']['edges'][j]['node']['createdOn']))
                        if(printRMA is None):
                            printRMA = "Null"
                        for l in range(0,o):
                            output.write(response['data']['fulfilments']['edges'][j]['node']['order']['id']+','+response['data']['fulfilments']['edges'][j]['node']['order']['ref']+',')
                            output.write(response['data']['fulfilments']['edges'][j]['node']['id']+','+response['data']['fulfilments']['edges'][j]['node']['status'])
                            output.write(','+response['data']['fulfilments']['edges'][j]['node']['items']['edges'][l]['node']['ref'])
                            output.write(','+response['data']['fulfilments']['edges'][j]['node']['createdOn'])
                            output.write(','+RMANum)
                            output.write(','+printRMA)
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
