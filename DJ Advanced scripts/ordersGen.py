import json, csv, requests, time
from graphqlclient import GraphQLClient
from http.client import IncompleteRead
from datetime import datetime, timedelta
# email imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from os.path import basename


page_query = '''
query($after: String,$first: Int, $count: Int, $from: DateTime, $to: DateTime){
orders(createdOn:{from:$from,to:$to},after: $after,first: $first){
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
oauth_url = 'https://palacio.api.fluentretail.com:443/oauth/token?username=elpalaciodehierro_admin&password=GT8Y4Q&client_id=PALACIO&client_secret=44f824ad-eb5d-4936-af10-86ebbcf5be61&grant_type=password&scope=api'

entity = "orders"

cols=['Order Id','Order Ref','Order createdOn','Item Ref','Fulfilment Id','Fulfilment Status','Pending Qty']

fields_order=['id','ref','createdOn']


graphql_url = 'https://PALACIO.api.fluentretail.com/graphql'

def get_page_of_data(after,first,count):
    client = GraphQLClient(graphql_url)
    token = get_token()
    
    client.inject_token(token)
    fromTime = (datetime.utcnow() - timedelta(hours=29)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    toTime = (datetime.utcnow() - timedelta(hours=5)).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    res = client.execute(page_query,{'after': after, 'first': first, 'count':count, 'from':'2020-08-26T02:58:13.845853Z', 'to':'2020-09-15T02:58:13.845853Z'})
    data = json.loads(res)['data']
    
    return data


def get_token():
    auth_token_response = requests.post(oauth_url)    
    if auth_token_response.status_code != 200:
        print("Couldn't get auth token {}".format(auth_token_response.status_code))
    access_token = 'bearer ' + auth_token_response.json()['access_token']
    #print("Access token: {}".format(access_token))
    return access_token

def get_all_data(all_labels=[], cursor=None, first=500, count=20, retries_left=5):
    global data
    '''
    try:
        data = get_page_of_data(cursor, first, count)
    except:
        print("error occurred for cursor: {} retrying with retries left:{}".format(cursor, retries_left))
        if retries_left > 0:
            retries_left -=1
            get_all_data(all_labels, cursor, retries_left)
        else:
            print('retries exhausted')
            return all_labels'''
    data = get_page_of_data(cursor, first, count)
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
    emailableReport = 'orders_'+datetime.utcnow().strftime("%Y%m%d%H%M%S")+'.csv'
    file = csv.writer(open(emailableReport, "wt"), delimiter=',')
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
                            if z['node']['ref']==items_concat_ref[t] and (y['node']['status']=="RMA Reintegro de Inventario" or y['node']['status']=="RMA Reverso de Pago Aplicado" or y['node']['status']=="CECOM RMA Cerrado" or y['node']['status']=="SGE RMA Autorizado" or y['node']['status']=="SGE Reintegro de Inventario" or y['node']['status']=="Cancelado por Validacion" or y['node']['status']=="Saldo Liberado"):
                                ano=z['node']['requestedQuantity']
                                #diff=diff+z['node']['requestedQuantity']-z['node']['rejectedQuantity']
                                items_concat_quantity[t]=items_concat_quantity[t]-ano
                                 
                            elif z['node']['ref']==items_concat_ref[t]:
                                diff=diff+z['node']['requestedQuantity']-z['node']['rejectedQuantity']
                                
                                
                pend_quant.append(items_concat_quantity[t]-diff)
           
                diff=0
            
            for x in range(0,len(items_concat_ref)):
                if pend_quant[x]!=0:
                    item_pend.append([items_concat_ref[x],pend_quant[x]])
            row.append(item_pend)    
                
               
        for n in pend_quant:
            if n>0 and len(var1['node']['fulfilments']['edges'])>0 :
                flag=1
        if flag==1:
            file.writerow(row)
    return emailableReport

'''
def send_email(report):
    mail_content = "Hi,   PFA daily orders report \n\n note: this is auto-generated email, do not reply. \n\n  Regards\n   Dhananjay"
    
    sender_address = "secommerce@ph.com.mx"
    #sender_pass = "Myarsenal@1"
    
    receiver_address = ['dhananjay.pandey@bridgesgi.com']

    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = ", ".join(receiver_address)
    message['Subject'] = 'Fulfilment failure report'

    message.attach(MIMEText(mail_content))
    #f = "/opt/monarch/yc_report_gen/reports/nwms_20200414154726714147.html"

    for files in report:
        with open(files, "rb") as handle:
            part = MIMEApplication(handle.read(), Name=basename(files))
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(files)
        message.attach(part)

    session = smtplib.SMTP("outlook.office365.com", 587)
    session.starttls()
    session.login(sender_address, '')
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')'''


start = time.time()

result = get_all_data()
report = write_to_csv(result)
#send_email([report])

print("Time taken: " + str((time.time()-start)/60) + " minutes")

