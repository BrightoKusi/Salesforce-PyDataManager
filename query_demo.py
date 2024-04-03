from simple_salesforce import Salesforce, SalesforceLogin
import pandas as pd
import configparser

def establish_salesforce_connection():
    config = configparser.ConfigParser()
    config.read('.env')
    
    username = config['SfLoginInfo']['username']
    password = config['SfLoginInfo']['password']
    security_token = config['SfLoginInfo']['security_token']
    domain = 'login'
    
    session_id, instance = SalesforceLogin(username=username, password=password, security_token=security_token, domain=domain)
    sf = Salesforce(instance=instance, session_id=session_id)
    
    return sf

def query_accounts(sf_instance):
    values = ['Energy', 'Banking', 'Apparel', 'Technology']
    querySOQL = """SELECT Id, Name, Type, Industry FROM Account WHERE 
                    Industry IN ('{0}')""".format("','".join(values))
    accounts_record = sf_instance.query(querySOQL)
    response = accounts_record.get('records')
    
    data = []
    for record in response:
        data.append({
            'Id': record['Id'],
            'Name': record['Name'],
            'Type': record['Type'],
            'Industry': record['Industry']
        })
    
    df = pd.DataFrame(data)
    return df

def export_to_csv(df, filename):
    df.to_csv(filename, index=False)

if __name__ == '__main__':
    sf_instance = establish_salesforce_connection()
    print(sf_instance)
    
    accounts_df = query_accounts(sf_instance)
    print(accounts_df)
    
    export_to_csv(accounts_df, 'accounts_records.csv')
