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

        inputIdList = [1299482,1298245,1298210,1298137,1298121,1297738,1297622,1297449,1297374,1297291,1297155,1297149,1296987,1296878,1296878,1296878,1296836,1296785,1296717,1296647,1296647,1296641,1296513,1296411,1296132,1296000,1295980,1295812,1295570,1295553,1295516,1295374,1295374,1295346,1295340,1295273,1295261,1295193,1295099,1295099,1295093,1295057,1295020,1294992,1294990,1294979,1294943,1294930,1294887,1294828,1294752,1294718,1294655,1294585,1294442,1294436,1294430,1294427,1294419,1294393,1294333,1294316,1294291,1294267,1294266,1294249,1294238,1294199,1294191,1294170,1294137,1294103,1294101,1294100,1294099,1293914,1293901,1293837,1293804,1293688,1293682,1293623,1293593,1293569,1293567,1293536,1293536,1293533,1293518,1293482,1293456,1293399,1293293,1293248,1293227,1293224,1293165,1293122,1293119,1293104,1293081,1293025,1292952,1292938,1292879,1292748,1292729,1292728,1292714,1292676,1292648,1292621,1292612,1292612,1292573,1292558,1292551,1292542,1292520,1292511,1292480,1292478,1292478,1292478,1292474,1292467,1292450,1292434,1292425,1292412,1292399,1292362,1292343,1292318,1292306,1292283,1292245,1292240,1292204,1292197,1292190,1292177,1292147,1292125,1292058,1292047,1292045,1292026,1292025,1292015,1292004,1291994,1291988,1291982,1291974,1291974,1291974,1291974,1291917,1291879,1291875,1291869,1291833,1291815,1291807,1291806,1291797,1291791,1291775,1291775,1291771,1291760,1291733,1291678,1291658,1291653,1291626,1291625,1291614,1291578,1291570,1291514,1291503,1291490,1291432,1291399,1291383,1291365,1291323,1291272,1291267,1291215,1291199,1291189,1291168,1291158,1291139,1291115,1291105,1291097,1291085,1290872,1290848,1290839,1290809,1290724,1290722,1290716,1290673,1290667,1290621,1290590,1290589,1290561,1290561,1290527,1290521,1290520,1290513,1290457,1290403,1290399,1290383,1290363,1290347,1290338,1290320,1290304,1290280,1290246,1290233,1290223,1290201,1290189,1290176,1290173,1290169,1290169,1290167,1290121,1290119,1290066,1289940,1289934,1289931,1289911,1289911,1289881,1289881,1289816,1289811,1289774,1289731,1289724,1289661,1289615,1289612,1289608,1289600,1289599,1289596,1289596,1289591,1289578,1289576,1289558,1289542,1289540,1289539,1289521,1289484,1289396,1289341,1289307,1289286,1289280,1289268,1289208,1289127,1289125,1289110,1289095,1289091,1289049,1289026,1289007,1288958,1288930,1288873,1288338,1288842,1288826,1288818,1288797,1288730,1288706,1288699,1288674,1288673,1288656,1288644,1288625,1288596,1288595,1288587,1288525,1288525,1288520,1288490,1288469,1288468,1288433,1288416,1288407,1288405,1288305,1288286,1288232,1288216,1288210,1288195,1288184,1288184,1288182,1288168,1288161,1288142,1288106,1288055,1287886,1287872,1287842,1287811,1287779,1287760,1287741,1287665,1287594,1287590,1287553,1287546,1287524,1287488,1287444,1287425,1287363,1287362,1287356,1287125,1287080,1287061,1287035,1287017,1287011,1287011,1287005,1286985,1286985,1286985,1286985,1286977,1286910,1286863,1286845,1286843,1286801,1286708,1286694,1286550,1286657,1286654,1286626,1286614,1286604,1286581,1286550,1286519,1286498,1286486,1286474,1286428,1286407,1286394,1286380,1286356,1286313,1286295,1286262,1286262,1286248,1286223,1286208,1286174,1286104,1286090,1286060,1286034,1286001,1285987,1285965,1285960,1285955,1285937,1285935,1285920,1285920,1285907,1285907,1285899,1285899,1285874,1285873,1285841,1285840,1285836,1285785,1285784,1285779,1285767,1285763,1285763,1285763,1285735,1285701,1285688,1285595,1285546,1285531,1285519,1285472,1285443,1285421,1285398,1285383,1285372,1285358,1285345,1285344,1285340,1285302,1285283,1285279,1285270,1285231,1285202,1285200,1283031,1285183,1285174,1285168,1285141,1285141,1285138,1285128,1285123,1285120,1285117,1285061,1284982,1284979,1284974,1284969,1284929,1284906,1284896,1284839,1284835,1284783,1284778,1284702,1284695,1284625,1284619,1284605,1284580,1284580,1284566,1284553,1284530,1284522,1284509,1284497,1284473,1284441,1284435,1284424,1284422,1284411,1284364,1284362,1284330,1284324,1284283,1284265,1284264,1284255,1284248,1284245,1284245,1284241,1284226,1284226,1284214,1284205,1284185,1284163,1284146,1284146,1284125,1284111,1284108,1284101,1284085,1284085,1284071,1284067,1284063,1284056,1284001,1283961,1283937,1283937,1283921,1283920,1283889,1283866,1283856,1283852,1283846,1283845,1283844,1283843,1282556,1283824,1283817,1283812,1283802,1283756,1283717,1283710,1283688,1283688,1283671,1283670,1283624,1283610,1283596,1283598,1283572,1283526,1283480,1283447,1283407,1283398,1283371,1283349,1283342,1283253,1283185,1283176,1283170,1283166,1283134,1283116,1283103,1283085,1283079,1283071,1283071,1283071,1283031,1283031,1283018,1282983,1282976,1282974,1282934,1282841,1282805,1282677,1282662,1282632,1282626,1282625,1282618,1282613,1282585,1282561,1282561,1282554,1282551,1282546,1282542,1282525,1282516,1282499,1282493,1282489,1282484,1282453,1282447,1282445,1282444,1282428,1282391,1282364,1282347,1282318,1282318,1282306,1282287,1282264,1282261,1282234,1282214,1282213,1282209,1282192,1282183,1282164,1282147,1282126,1282089,1282088,1282086,1282082,1282038,1282029,1282026,1281988,1281935,1281921,1281895,1281891,1281890,1281879,1281862,1281861,1281849,1281832,1281800,1281791,1281753,1281749,1281735,1281715,1281703,1281696,1281696,1281687,1281657,1281532,1281505,1281498,1281491,1281474,1281466,1281465,1281445,1281444,1281438,1281435,1281434,1281406,1281394,1281389,1281388,1281342,1281340,1281338,1281318,1281318,1281310,1281306,1281301,1281240,1281230,1281228,1281210,1281190,1281182,1281172,1281163,1281155,1281147,1281137,1281120,1281109,1281102,1281097,1281039,1281025,1280996,1280984,1280956,1280955,1280939,1280873,1280832,1280828,1280819,1280818,1280815,1280806,1278119,1280800,1280794,1280782,1280774,1280770,1280756,1280756,1280755,1280746,1280714,1280704,1280700,1280663,1280663,1280657,1280649,1280617,1280606,1280601,1280599,1280583,1280568,1280563,1280541,1280525,1280497,1280489,1280484,1280469,1280468,1280462,1280438,1280432,1280417,1280416,1280359,1280350,1280309,1280308,1280271,1280256,1280251,1280221,1280221,1280188,1280180,1280179,1280153,1280145,1280128,1280120,1280119,1280102,1280098,1280098,1280086,1280055,1280055,1280055,1280050,1279957,1279938,1279927,1279924,1279920,1279912,1279899,1279894,1279867,1279867,1279866,1279851,1279840,1279821,1279760,1279729,1279720,1279696,1279670,1279645,1279623,1279620,1279613,1279603,1279592,1279588,1279569,1279560,1279535,1279530,1279527,1279526,1279520,1279519,1279509,1279487,1279466,1279351,1279455,1279449,1279417,1279370,1279366,1279365,1279333,1279329,1279276,1279274,1279262,1279253,1279250,1279236,1279223,1279214,1279184,1279159,1279147,1279116,1279114,1279064,1279046,1279022,1279004,1279004,1278983,1278966,1278963,1278959,1278923,1278918,1278886,1278880,1278880,1278858,1278855,1278852,1278840,1278838,1278805,1278770,1278754,1278743,1278693,1278661,1278622,1278617,1278611,1278565,1278527,1278522,1278522,1278520,1278520,1278511,1278507,1278434,1278417,1278417,1278418,1278387,1278372,1278369,1278349,1278340,1278325,1278288,1278267,1278251,1278240,1278229,1278218,1278215,1278214,1278204,1278192,1278178,1278165,1278166,1278137,1278131,1278118,1278090,1278090,1278071,1278007,1277975,1277961,1277953,1277938,1277929,1277919,1277902,1277880,1277877,1277865,1277856,1277854,1277840,1277838,1277819,1277807,1277795,1277786,1277761,1277758,1277730,1277720,1277704,1277692,1277674,1277673,1277672,1277668,1277667,1277664,1277665,1277663,1277658,1277652,1277652,1277640,1277634,1277620,1277613,1277611,1277596,1277579,1277577,1277575,1277574,1277565,1277558,1277558,1277552,1277539,1277533,1277525,1277502,1277498,1277494,1277489,1277472,1277462,1277462,1277461,1277435,1277416,1277396,1277389,1277386,1277376,1277376,1277376,1277375,1277374,1277358,1277355,1277315,1277314,1277310,1277310,1277302,1277301,1277292,1277288,1277275,1277274,1277255,1277252,1277237,1277230,1277219,1277220,1277211,1277206,1277188,1277183,1277183,1277177,1277174,1277142,1277113,1277114,1277113,1277094,1277081,1277070,1277066,1277016,1277008,1277005,1276985,1276980,1276963,1276954,1276942,1276930,1276923,1276915,1276906,1276888,1275139,1276857,1276841,1276839,1276823,1276821,1276817,1276815,1276804,1276802,1276800,1276798,1276771,1276744,1276743,1276742,1276742,1276742,1276730,1276728,1276712,1276709,1276709,1276707,1276687,1276675,1276665,1276664,1276641,1276641,1276622,1276605,1276597,1276597,1276580,1276574,1276571,1276544,1276542,1276533,1276516,1276511,1276508,1276504,1276504,1276494,1276493,1276464,1276449,1276433,1276430,1276430,1276423,1276411,1276347,1276316,1276311,1276295,1276267,1276247,1276228,1276217,1276199,1276192,1276189,1276179,1276159,1275784,1276136,1276130,1276117,1276110,1276089,1276089,1276078,1276021,1276007,1275991,1275960,1275959,1275932,1275925,1275916,1275906,1275898,1275879,1275877,1275865,1275862,1275862,1275853,1275851,1275845,1275845,1275845,1275827,1275806,1275783,1275710,1275706,1275703,1275692,1275683,1275656,1275641,1275635,1275633,1275628,1275611,1275607,1275605,1275599,1275593,1275591,1275588,1275586,1272547,1275568,1275558,1275552,1273609,1275523,1275522,1275517,1275482,1275474,1275473,1275472,1275471,1275440,1275438,1275417,1275403,1275398,1275360,1275347,1275346,1275319,1275312,1275293,1275288,1275263,1275259,1275253,1275248,1275248,1275229,1275208,1275199,1275189,1275184,1275170,1275162,1275145,1275142,1275128,1275122,1275117,1275106,1275106,1275106,1275105,1275099,1275091,1275080,1275060,1275037,1275026,1275025,1275017,1275008,1274990,1274930,1274914,1274888,1274877,1274877,1274860,1274846,1274838,1274829,1274810,1274803,1274795,1274769,1274764,1274744,1274705,1274693,1274677,1274670,1274656,1274645,1274635,1274630,1274628,1274605,1274588,1274580,1274567,1274561,1274558,1274558,1274516,1274512,1274491,1274480,1274472,1274457,1274445,1274443,1274408,1274390,1274376,1274336,1274331,1274318,1274314,1274306,1274301,1274281,1274280,1274278,1274273,1274270,1274267,1274217,1274208,1274202,1274200,1274192,1274115,1274114,1274112,1274108,1274106,1274105,1274099,1274082,1274078,1274050,1274016,1274003,1273998,1273990,1273980,1273980,1273980,1273978,1273932,1273925,1273919,1273914,1273907,1273867,1273848,1273840,1273839,1273837,1273838,1273836,1273835,1273834,1273833,1273832,1273831,1273830,1273829,1273828,1273827,1273826,1273825,1273824,1271202,1273821,1273819,1273818,1273817,1273814,1273813,1273812,1273811,1273810,1273809,1273808,1273807,1273806,1273805,1273804,1273803,1273802,1273801,1273800,1273799,1273799,1273798,1273797,1273796,1273795,1273794,1273793,1273792,1273791,1273790,1273789,1273788,1273787,1273786,1273785,1273784,1273783,1273782,1273781,1273780,1273779,1273778,1273777,1273776,1273775,1273774,1273771,1273770,1273769,1273768,1273765,1273764,1273762,1273758,1273757,1273756,1273754,1273753,1273752,1273752,1273752,1273751,1273750,1273749,1273748,1273746,1273746,1273747,1273745,1273745,1273743,1273742,1273741,1273740,1273739,1273738,1273736,1273735,1273735,1273735,1273735,1273734,1273733,1273732,1273731,1273730,1273729,1273727,1273726,1273725,1273725,1273724,1273723,1273721,1273720,1273719,1273718,1273717,1273716,1273715,1273714,1273713,1273712,1273711,1273710,1273709,1273708,1273707,1273706,1273705,1273704,1273703,1273702,1273701,1273700,1273699,1273698,1273694,1273692,1273690,1273689,1273688,1273686,1273686,1273687,1273684,1273683,1273682,1273680,1273678,1273677,1273675,1273674,1273673,1273672,1273671,1273670,1273669,1273668,1273667,1273666,1273664,1273662,1273663,1273661,1273660,1273659,1273658,1273657,1273656,1273655,1273654,1273653,1273652,1273651,1273650,1273649,1273648,1273645,1273641,1273640,1273639,1273639,1273638,1273637,1273636,1273635,1273634,1273633,1273632,1273632,1273632,1273631,1273630,1273629,1273627,1273626,1273625,1273624,1273623,1273622,1273621,1273620,1273618,1273617,1273616,1273615,1273614,1273613,1273612,1273611,1273609,1273608,1273607,1273605,1273602,1273601,1273600,1273599,1273598,1273597,1273595,1273593,1273592,1273588,1273587,1273586,1273585,1273584,1273583,1273582,1273581,1273580,1273579,1273578,1273577,1273576,1273575,1273573,1273572,1273571,1273570,1273569,1273568,1273567,1273566,1273565,1273564,1273563,1273562,1273561,1273560,1273559,1273558,1273556,1273557,1273555,1273554,1273552,1273551,1273550,1273550,1273549,1273547,1273546,1273545,1273544,1273543,1273542,1273541,1273537,1273536,1273535,1273534,1273533,1273532,1273530,1273529,1273528,1273525,1273525,1273524,1273524,1273524,1273524,1273524,1273524,1273523,1273523,1273522,1273521,1273520,1273520,1273518,1273517,1273516,1273515,1273514,1273513,1273513,1273510,1273509,1273507,1273506,1273504,1273503,1273502,1273500,1273499,1273498,1273497,1273496,1273495,1273494,1273493,1273493,1273493,1273492,1273491,1273490,1273489,1273488,1273487,1273479,1273459,1273450,1273437,1273388,1273386,1273372,1273368,1273357,1273349,1273332,1273290,1273278,1273231,1273229,1273228,1273214,1273209,1273171,1273127,1273121,1273111,1273097,1273090,1273079,1273067,1273045,1273041,1273028,1273027,1273001,1273001,1272994,1272968,1272958,1272954,1272927,1272925,1272923,1272917,1269292,1272881,1272874,1272842,1272789,1272785,1272785,1272743,1272737,1272690,1272670,1272657,1272655,1272616,1272611,1272593,1272583,1272583,1272570,1272569,1272547,1272485,1272484,1272463,1272434,1272422,1272413,1272407,1272398,1272396,1272391,1272382,1272381,1272344,1272337,1272326,1272312,1272304,1272284,1272281,1272277,1272274,1272260,1272248,1272240,1272238,1272236,1272203,1272180,1272179,1272154,1272147,1272145,1272121,1272098,1272073,1272072,1272063,1272063,1272063,1272063,1272063,1272061,1272060,1272058,1272051,1272028,1272004,1271995,1271988,1271959,1271959,1271962,1271952,1271949,1271948,1271926,1271904,1271893,1271865,1271860,1271859,1271818,1271795,1271781,1271780,1271779,1271710,1271709,1271690,1271688,1271674,1271653,1271648,1271641,1271632,1271628,1271615,1271611,1271596,1271582,1271575,1271573,1271570,1271555,1271548,1271520,1271486,1271473,1271473,1271433,1271409,1271384,1271343,1271333,1271314,1271306,1271297,1271279,1271249,1271224,1271224,1271219,1271208,1271206,1271200,1271188,1271188,1271161,1271150,1271143,1271139,1271137,1271101,1271099,1271025,1271001,1270988,1270973,1270964,1270955,1270950,1270947,1270910,1270904,1270895,1270890,1270890,1270881,1270861,1270844,1270811,1270808,1270782,1270770,1270765,1270763,1270761,1270743,1270740,1270740,1270740,1270732,1270702,1270684,1270668,1270658,1270647,1270645,1270642,1270635,1270623,1270623,1270619,1270604,1270594,1270588,1270588,1270582,1270576,1270553,1270540,1270534,1270512,1270488,1270482,1270476,1270475,1270472,1270472,1270471,1270471,1270471,1270470,1270461,1270457,1270457,1270456,1269928,1270437,1270411,1270410,1270402,1270389,1270385,1270355,1270347,1270343,1270261,1270255,1270251,1270250,1270245,1270232,1270230,1270221,1270212,1270185,1270165,1270160,1270107,1270094,1270089,1270074,1270067,1270061,1270060,1270050,1270046,1270046,1270046,1270027,1270026,1269997,1269991,1269990,1269963,1269958,1269936,1269928,1269926,1269886,1269881,1269864,1269863,1269849,1269782,1269763,1269754,1269735,1269713,1269712,1269712,1269708,1269679,1269654,1269648,1269645,1269630,1269620,1269615,1269614,1269588,1269585,1269581,1269579,1269572,1269562,1269540,1269537,1269527,1269525,1269524,1269499,1269472,1269468,1269455,1269453,1269425,1269423,1269419,1269408,1269402,1269371,1269365,1269356,1269343,1269330,1269315,1269313,1269299,1269294,1269291,1269259,1269256,1269235,1269235,1269221,1269210,1269210,1269210,1269206,1269197,1269175,1269174,1269144,1269138,1269137,1269100,1269087,1269083,1269062,1269061,1269050,1269047,1269038,1269038,1269031,1269029,1269029,1269017,1269017,1269012,1269007,1269000,1268995,1268973,1268963,1268962,1268961,1268959,1268952,1268931,1268919,1268911,1268885,1268868,1268864,1268863,1268824,1268815,1268809,1268804,1268791,1268789,1268786,1268785,1268774,1268763,1268762,1268746,1268744,1268739,1268713,1268710,1268705,1268704,1268699,1268697,1268655,1268649,1268638,1268604,1268560,1268553,1268546,1268538,1268535,1268535,1268535,1268534,1268534,1268524,1268501,1268483,1268471,1268463,1268458,1268456,1268449,1268449,1268449,1268442,1268428,1268412,1268395,1268382,1268367,1268361,1268346,1268341,1268336,1268319,1268309,1268280,1268262,1268260,1268255,1268254,1268237,1268232,1268228,1268226,1268202,1268181,1268162]
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
