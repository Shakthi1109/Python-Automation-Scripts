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

        inputIdList=set([1213255,1213252,1213211,1213191,1213167,1213163,1213105,1213105,1213064,1212987,1212986,1212961,1212940,1212927,1212905,1212864,1212793,1212783,1212778,1212761,1212755,1212718,1212699,1212691,1206630,1212678,1212664,1212626,1212568,1212545,1212528,1212509,1212499,1212498,1212467,1212467,1212467,1212440,1212440,1212444,1212421,1212379,1212340,1212248,1212220,1212114,1212085,1212081,1212064,1212040,1212019,1212011,1211989,1211989,1211989,1211978,1211973,1211960,1211960,1211959,1211923,1211920,1211902,1211902,1211902,1211865,1211845,1211831,1211823,1211808,1211764,1211764,1211764,1211764,1211728,1211663,1211648,1211629,1211601,1211575,1211525,1211525,1211473,1211465,1211440,1211427,1211384,1211378,1211370,1211310,1211249,1211239,1211203,1211203,1211197,1211164,1211136,1211128,1211097,1211093,1211091,1211025,1211022,1211022,1211022,1211022,1211022,1210965,1210961,1210956,1210855,1210846,1210840,1210831,1210819,1210812,1210791,1210773,1210743,1210736,1205407,1210723,1210703,1210687,1210663,1210621,1210618,1210609,1210588,1210558,1210539,1210539,1210476,1210465,1210460,1210445,1210418,1210416,1210406,1210252,1210241,1210233,1210217,1210216,1210123,1210119,1210115,1210098,1210072,1210072,1210072,1210068,1210068,1210068,1210068,1210005,1210003,1210003,1210003,1209997,1209996,1209990,1209990,1209990,1209990,1209993,1209946,1209946,1209946,1209946,1209822,1209781,1209777,1209726,1209725,1209700,1209645,1209588,1209566,1209565,1209477,1209460,1209447,1209411,1209386,1209375,1209355,1209297,1209235,1209228,1209212,1209210,1209208,1209208,1209179,1209179,1209161,1209156,1209111,1209076,1209036,1209025,1208978,1208860,1208805,1208796,1208699,1208636,1208630,1208552,1208451,1208451,1208372,1208278,1208278,1208259,1208238,1208204,1208192,1208182,1208180,1208166,1208126,1208113,1208105,1208105,1208077,1208053,1208020,1174766,1207942,1200107,1207931,1207922,1207919,1207912,1207888,1207888,1207851,1207827,1207827,1207818,1207812,1207795,1207782,1207742,1207676,1207672,1207608,1207594,1207556,1207532,1207525,1207499,1207457,1207448,1207446,1207432,1207432,1207432,1207429,1207429,1207429,1207411,1207355,1207355,1207355,1207355,1207284,1207277,1207267,1207246,1207242,1207240,1207202,1207156,1207155,1207112,1207099,1207078,1207070,1207006,1206989,1206989,1206989,1206989,1206990,1206986,1206956,1206888,1206888,1206886,1206879,1206867,1206865,1206857,1206856,1206850,1206826,1206653,1206652,1206525,1206525,1206525,1206511,1206511,1206500,1206500,1206500,1206480,1206456,1206422,1206393,1206369,1206367,1206327,1206324,1206250,1206250,1206224,1206219,1206190,1206171,1206167,1206128,1206092,1206063,1206047,1206048,1206046,1206012,1206012,1206012,1206005,1205970,1205910,1205876,1205860,1205830,1205828,1205797,1205795,1205773,1205734,1205725,1205694,1205694,1205694,1205694,1205653,1205627,1205615,1205605,1205605,1205586,1205552,1205483,1205477,1205407,1205387,1205344,1205334,1205334,1205282,1205278,1205251,1205243,1205215,1205215,1205204,1188759,1205181,1205167,1205166,1205134,1205129,1205119,1205113,1205108,1205100,1205051,1205039,1205031,1205031,1205009,1205004,1205004,1205004,1205003,1204977,1204969,1204960,1204959,1204921,1204899,1204899,1204826,1204747,1204747,1204741,1204709,1204699,1204693,1204663,1204626,1204598,1204597,1204587,1204584,1204491,1204491,1204488,1204416,1204410,1204352,1204197,1204177,1204130,1204130,1204118,1204093,1204093,1204087,1204085,1204047,1204047,1204040,1204037,1204037,1204037,1204007,1204004,1203973,1203972,1203921,1203914,1203880,1203804,1203804,1203799,1203764,1203751,1203739,1203728,1203706,1203703,1203648,1203629,1203620,1203591,1203573,1203538,1203524,1203507,1203494,1203490,1203445,1203416,1203410,1203388,1203374,1203355,1196460,1203314,1203314,1203309])
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
