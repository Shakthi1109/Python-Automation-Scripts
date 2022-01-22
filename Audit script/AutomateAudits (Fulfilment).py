import json, requests, csv, time, datetime, ast
from graphqlclient import GraphQLClient
from datetime import datetime

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("Bearer 9de06491-c95b-4ed6-a581-5520fd4819d4")

def process(fulfilmentIds):

    f = open('Date.csv','a')
    f.write('fulfilment Id, fulldate, currentDate, previousDate, nextDate\n')
    i=0

    AuditURL = 'http://palacio.api.fluentretail.com/api/v4.1/event'


    for fulfilmentId in list(fulfilmentIds):

        query = "query{"
        query += "fulfilmentById(id:\"" +str(fulfilmentId)+ "\"){createdOn}"
        query += "}"

        response = client.execute(query)
        response = json.loads(response)

        i=i+1
        print(fulfilmentId)

        f.write(str(fulfilmentId)+',')

        currentDate=str(response['data']['fulfilmentById']['createdOn'])
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
        fromDate=year+'-'+previousMonth+'-'+previousDate+"T11:00:00.000Z"
        toDate=year+'-'+nextMonth+'-'+nextDate+"T12:00:00.000Z"
        # print("fromDate:{}".format(fromDate))
        # print(type(fromDate))
        f.write('\n')


        audit = requests.get(AuditURL,
                    headers = {"Authorization": "Bearer 9de06491-c95b-4ed6-a581-5520fd4819d4","fluent.account":"PALACIO"},
                    params = {"context.entityType":"FULFILMENT","count":"1000","fluent.account":"PALACIO","context.entityId":str(fulfilmentId),"from":fromDate,"to":toDate}
                    )

        a = open(str(fulfilmentId)+".json",'a')
        print(audit.url)
        a.write(audit.text)

    a.close()
    f.close()

start = time.time()

process([2178576,2170638])

print("Time taken: " + str((time.time()-start)/60) + " minutes")
