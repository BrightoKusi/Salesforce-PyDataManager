from simple_salesforce import Salesforce, SalesforceLogin
import pandas as pd

import configparser
config = configparser.ConfigParser()
config.read('.env')

['SfLoginInfo']
username = config['SfLoginInfo']['username']
password = config['SfLoginInfo']['password']
security_token = config['SfLoginInfo']['security_token']
domain = 'login'

#Establish the salesforce connection string
session_id, instance = SalesforceLogin(username = username, password=password, security_token=security_token, domain= domain)

#create a Salesforce instance
sf = Salesforce(instance= instance, session_id= session_id)
print(sf)

#Sample Query 1
values = ['Energy', 'Banking', 'Apparel', 'Technology']
querySOQL = """SELECT Id, Name, Type, Industry FROM Account WHERE 
                Industry IN ('{0}')""".format("','".join(values))

accounts_record = sf.query(querySOQL)
response = accounts_record.get('records')

data = []
for record in response:
    data.append({
        'Id': record['Id'],
        'Name': record['Name'],
        'Type': record['Type'],
        'Industry': record['Industry']
    })

# Create DataFrame
df = pd.DataFrame(data)
print(df)

# Convert DataFrame to CSV
df.to_csv('accounts records.csv', index=False)




