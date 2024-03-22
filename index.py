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


#Explore the attributes of the sf instance
for element in dir(sf):
    if not element.startswith('_'):
        if isinstance(getattr(sf, element), str):
            print('Property Name: {0}; Value: {1}'.format(element, getattr(sf,element)))


#Get the properties of SF metadata
metadata_org = sf.describe()
print(type(metadata_org))
print(metadata_org.keys())
print(metadata_org['encoding'])
print(metadata_org['maxBatchSize'])
print(metadata_org['sobjects'])

#  write properties of sf metadata to csv
df_sobjects = pd.DataFrame(metadata_org['sobjects'])
df_sobjects.to_csv('org metadata info.csv', index = False)

# write properties of sf account info to csv
account = sf.account
account_metadata = account.describe()
print(type(account_metadata))
df_account_metadata = pd.DataFrame(account_metadata.get('fields'))
df_account_metadata.to_csv('account object metadata')