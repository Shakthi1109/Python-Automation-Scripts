import csv, time, datetime, ast, json
from graphqlclient import GraphQLClient

graphqlUrl = 'https://PALACIO.api.fluentretail.com/graphql'
client = GraphQLClient(graphqlUrl)
client.inject_token("Bearer e5b7e8a1-30bd-421d-bc11-d9bcebd10f4f")

def process(ffList):
    ffListUnique = list(set(ffList))
    print(len(ffListUnique))
    multiSku = []
    singleSku = []
    for ffId in ffListUnique:
        query = "query{"
        query += "fulfilmentById(id:\"" +str(ffId)+ "\"){id status items{edges{node{ref}}}}"
        query += "}"
        response = client.execute(query)
        response = json.loads(response)
        if len(response['data']['fulfilmentById']['items']['edges']) == ffList.count(ffId):
            singleSku.append(ffId)
        else:
            multiSku.append(ffId)

    with open('singleSku','w') as f:
        f.write(str(singleSku))
        print(len(singleSku))
    with open('multiSku','w') as f:
        f.write(str(multiSku))
        print(len(multiSku))

ffList=[895562,896273,896273,896612,896828,896928,899042,899271,900007,903401,905272,876777,862416,862543,862749,862749,862811,862976,862923,862981,863163,863366,863236,863379,863408,863410,863582,863662,863662,863607,863754,864034,864388,864448,864537,866006,866232,902529,866312,866607,866705,867318,867409,867741,867749,867779,867807,867905,867982,868376,868717,868816,868944,869404,869476,869659,869748,870011,870234,870379,870411,870592,870948,870797,870802,870808,870986,871803,872286,872441,872898,873072,873288,873424,873456,873652,874000,874650,874651,874675,875041,875529,875578,875607,876930,877578,877604,878382,878487,879050,879062,879115,879277,879631,880093,880944,880909,880933,880987,880938,881023,881057,881168,881288,881765,881831,882086,882295,882523,883061,883271,884304,885018,885018,885018,885220,885799,885946,886604,886481,886945,887315,887198,887198,887198,887561,887614,887614,887974,888399,888474,889045,889792,889819,890023,890034,890351,890768,891768,891712,892579,892689,892786,893231,893361,917184,893335,894949,895432,897356,898443,898527,929717,899728,899800,901432,902361,902563,902763,903625,904532,904815]
start = time.time()

process(ffList)

print("Time taken: " + str((time.time()-start)/60) + " minutes")
