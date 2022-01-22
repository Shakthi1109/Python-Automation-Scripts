import json, csv, requests, time
from graphqlclient import GraphQLClient
from http.client import IncompleteRead
from datetime import datetime, timedelta


accountId = 'PALACIO'
oauth_url = 'https://palacio.api.fluentretail.com:443/oauth/token?username=elpalaciodehierro_admin&password=GT8Y4Q&client_id=PALACIO&client_secret=44f824ad-eb5d-4936-af10-86ebbcf5be61&grant_type=password&scope=api'

graphql_url = 'https://PALACIO.api.fluentretail.com/graphql'


def get_token():
    auth_token_response = requests.post(oauth_url)
    if auth_token_response.status_code != 200:
        print("Couldn't get auth token {}".format(auth_token_response.status_code))
    access_token = 'bearer ' + auth_token_response.json()['access_token']
    #print("Access token: {}".format(access_token))
    return access_token



with open('testing.csv','a') as f, open('output.csv','a') as output:

    f.write('S.No, Order Id, SKU Refs, Fulfilment ID, ff Status, SKU REFS, Result\n')
    output.write('Order Id, Status, CreatedOn, SKU Refs, Required Quantity, Price\n')

    def get_all_data():

        inputIdList=set([1203267,1201521,1203209,1203209,1203126,1203120,1203115,1203107,1203107,1203106,1203100,1203094,1203091,1203089,1203028,1202988,1202988,1202988,1202979,1202967,1202927,1202918,1202910,1202907,1202873,1202871,1202855,1202742,1202721,1202721,1202721,1202720,1202703,1202688,1202684,1202684,1202671,1202655,1202640,1202579,1202491,1202485,1202467,1202452,1202440,1202440,1202436,1202397,1202362,1202348,1202291,1066243,1202246,1202216,1202215,1202214,1202212,1202200,1202185,1202061,1202061,1202030,1202029,1202013,1201974,1201939,1201866,1201827,1201825,1201743,1201719,1201704,1201622,1201619,1201611,1201600,1201600,1201586,1201575,1201558,1201556,1201555,1201539,1201521,1201488,1201364,1201365,1201363,1201363,1201363,1201358,1201340,1201336,1201312,1201314,1201281,1201281,1201281,1201281,1201238,1201183,1201183,1201180,1201180,1201178,1201178,1201177,1201145,1201145,1201133,1201124,1201101,1201095,1201062,1201069,1201045,1201035,1201035,1201030,1201003,1200982,1200979,1200959,1200949,1200917,1200905,1200859,1200819,1200808,1200803,1200801,1200781,1200773,1200752,1200740,1200735,1200721,1200720,1200704,1200704,1200675,1200674,1200665,1200665,1200665,1200624,1200602,1200593,1200514,1200509,1200488,1200485,1200477,1200423,1200409,1200354,1200350,1200348,1200342,1200341,1200337,1200321,1200317,1200272,1200242,1200209,1200199,1200196,1200190,1200169,1200147,1200136,1200126,1200122,1200096,1200093,1200042,1200010,1200004,1199994,1199994,1199994,1199976,1199970,1199962,1199962,1199962,1199947,1199947,1199947,1199947,1199915,1199905,1199831,1199829,1199829,1199815,1199779,1199746,1199700,1199668,1199662,1199546,1199545,1199497,1199460,1199458,1199451,1199451,1199420,1199403,1199369,1199367,1199350,1199257,1199237,1199228,1199224,1199216,1199166,1199152,1199146,1199104,1199104,1199104,1199084,1199045,1199043,1199025,1199004,1198991,1198984,1198972,1198917,1198916,1198916,1198883,1198877,1198868,1198864,1198835,1198835,1198827,1198784,1198781,1198729,1198644,1198624,1198616,1198606,1198583,1198567,1198546,1198530,1198530,1198530,1198520,1198508,1198468,1198424,1198420,1198420,1198403,1198389,1198378,1198345,1198339,1198334,1198322,1198296,1198242,1198218,1198203,1198194,1198194,1198195,1198166,1198165,1198162,1198136,1198114,1198107,1198077,1198074,1198036,1198030,1197990,1197970,1197964,1197948,1197942,1197869,1197862,1197844,1197840,1196314,1197799,1197727,1197720,1197710,1197697,1197673,1197641,1197622,1197603,1197163,1197569,1197567,1197557,1197500,1197500,1197500,1197482,1197473,1197473,1197473,1197471,1197437,1197423,1197415,1197338,1197253,1197240,1197210,1197210,1197135,1197104,1197087,1197066,1197059,1197056,1197056,1197058,1197049,1197047,1196997,1196994,1196968,1196960,1196920,1196853,1196834,1196828,1196806,1196797,1196789,1196789,1196786,1196781,1196775,1196752,1196656,1196647,1196645,1196627,1196621,1196619,1196603,1196601,1196599,1196596,1196567,1196565,1196541,1196528,1196475,1196460,1196460,1196460,1196460,1196458,1196404,1196380,1196378,1196376,1196340,1196340,1196340,1196340,1196343,1196308,1196300,1196244,1196238,1196152,1196088,1196085,1196050,1196033,1195993,1195974,1195970,1195960,1195959,1195957,1195952,1195948,1195948,1195948,1195946,1195943,1195916,1195852,1195845,1195833,1195831,1195809,1195809,1195809,1195794,1195786,1195723,1195704,1195695,1195695,1195679,1195658,1195640,1195576,1195530,1195527,1193875,1195497,1195475,1194511,1195431])
        global response
        sno=0

        for ids in inputIdList:

            page_query = "query{"
            page_query += "orderById(id: "+str(ids)+ "){id createdOn status items(first:100){edges{node{ref quantity price}}}fulfilments(first:100){edges{node{id status items(first:100){edges{node{ref}}}}}}}}"

            client = GraphQLClient(graphql_url)
            token = get_token()
            client.inject_token(token)
            response = client.execute(page_query)
            response = json.loads(response)
            #print(response)

            if response is not None:
                sno=sno+1
                print(sno)
                with open('testing.csv','a') as f, open('output.csv','a') as output:


                    orderSKU=[]
                    FulfilmentSKU=[]
                    quantity=[]
                    price=[]

                    f.write(str(sno)+','+response['data']['orderById']['id']+'\n')

                    n=len(response['data']['orderById']['items']['edges'])
                    for k in range(0,n):
                        f.write(','+','+response['data']['orderById']['items']['edges'][k]['node']['ref']+'\n')
                        orderSKU.append(response['data']['orderById']['items']['edges'][k]['node']['ref'])
                        quantity.append(response['data']['orderById']['items']['edges'][k]['node']['quantity'])
                        price.append(response['data']['orderById']['items']['edges'][k]['node']['price'])

                    o=len(response['data']['orderById']['fulfilments']['edges'])

                    for l in range(0,o):
                        f.write(','+','+','+response['data']['orderById']['fulfilments']['edges'][l]['node']['id'])
                        f.write(','+response['data']['orderById']['fulfilments']['edges'][l]['node']['status']+'\n')


                        p=len(response['data']['orderById']['fulfilments']['edges'][l]['node']['items']['edges'])

                        for mm in range(0,p):
                            f.write(','+','+','+','+','+response['data']['orderById']['fulfilments']['edges'][l]['node']['items']['edges'][mm]['node']['ref']+'\n')
                            FulfilmentSKU.append(response['data']['orderById']['fulfilments']['edges'][l]['node']['items']['edges'][mm]['node']['ref'])

                        # if(len(set(orderSKU).symmetric_difference(set(FulfilmentSKU)))==0):
                        #     f.write(','+','+','+','+','+'All SKUs present'+'\n')
                        # else:
                        #     f.write(','+','+','+','+','+str(set(orderSKU).symmetric_difference(set(FulfilmentSKU)))+'\n')

                    if(len(orderSKU)>len(FulfilmentSKU)):
                        f.write(','+','+','+','+','+','+'Unassigned Items'+','+str(set(orderSKU).symmetric_difference(set(FulfilmentSKU)))+'\n')
                    elif(len(orderSKU)<len(FulfilmentSKU)):
                        f.write(','+','+','+','+','+','+'Alert check'+','+str(set(FulfilmentSKU).symmetric_difference(set(orderSKU)))+'\n')
                    else:
                        f.write(','+','+','+','+','+','+'All SKU assigned'+','+str(set(FulfilmentSKU).symmetric_difference(set(orderSKU)))+'\n')




f.close()
output.close()

start = time.time()

get_all_data()

print("Time taken: " + str((time.time()-start)/60) + " minutes")
