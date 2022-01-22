import json, requests, csv, time, datetime, ast
from graphqlclient import GraphQLClient
from datetime import datetime

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("Bearer f3211ff6-2cbe-4587-bdc2-14c4e4baa487")

def process(fulfilmentIds):

    with open('Date.csv','w') as f:
        f.write('fulfilment Id, fulldate, currentDate, previousDate, nextDate\n')
        i=0

        AuditURL = 'http://palacio.api.fluentretail.com/api/v4.1/event'


        for fulfilmentId in list(fulfilmentIds):

            query = "query{"
            query += "orderById(id:\"" +str(fulfilmentId)+ "\"){createdOn}"
            query += "}"

            response = client.execute(query)
            response = json.loads(response)

            i=i+1
            print(fulfilmentId)

            f.write(str(fulfilmentId)+',')

            currentDate=str(response['data']['orderById']['createdOn'])
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

            f.write(fulldate+','+currentDate+'-'+month+'-'+year+','+previousDate+'-'+previousMonth+'-'+year+','+nextDate+'-'+nextMonth+'-'+year)
            fromDate=year+'-'+previousMonth+'-'+previousDate+"T00:00:00.192Z"
            toDate=year+'-'+nextMonth+'-'+nextDate+"T23:59:59.192Z"
            # print("fromDate:{}".format(fromDate))
            # print(type(fromDate))
            f.write('\n')


            audit = requests.get(AuditURL,
                        headers = {"Authorization": "Bearer f3211ff6-2cbe-4587-bdc2-14c4e4baa487","Content-Type":"application/json"},
                        params = {"context.rootEntityType":"ORDER","count":"2000","context.rootEntityId":str(fulfilmentId),"from":fromDate}
                        )

            with open(str(fulfilmentId)+".json","w",encoding="utf-8") as a:
                print(audit.url.encode("utf-8"))
                a.write(audit.text)


start = time.time()

process([577226,574968,574959,574958,574954,574950,574947,574946,574926,574924,574923,574922,574920,574919,574915,574912,574911,574907,574906,574903,574163,573983,557423,552971,545570,540234,526009,516448])

print("Time taken: " + str((time.time()-start)/60) + " minutes")
