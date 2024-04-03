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

def read_lead_object(sf):
    soql_query = """
        SELECT Id, Name, Email
        FROM LEAD
        LIMIT 10
    """
    soql_result = sf.query_all(soql_query)
    df = pd.DataFrame(soql_result.get('records'))
    return df

def insert_records_into_lead_object(sf):
    list_of_records = [
        {'FirstName': 'Bob', 'LastName': 'Test', 'Company': 'Bobs Company'},
        {'FirstName': 'Jamine', 'LastName': 'Mensah', 'Company': 'Jamines Company'}
    ]
    sf.bulk.Lead.insert(list_of_records)

def update_email_column(sf):
    soql_query = """
        SELECT Id, FirstName, LastName, Email
        FROM LEAD
        WHERE Company IN ('Bobs Company', 'Jamines Company')
    """
    soql_result = sf.query_all(soql_query)
    df = pd.DataFrame(soql_result.get('records'))

    df.drop(columns=['attributes'], inplace=True)

    record_ids_and_emails = [('00QWU000003Zahg2AC', 'bob@test.com'),
                             ('00QWU000003Zahh2AC', 'jamine@mensah.com')]
    for record_id, email in record_ids_and_emails:
        df.loc[df['Id'] == record_id, 'Email'] = email

    df.drop(columns=['FirstName', 'LastName'], inplace=True)

    list_of_records = df.to_dict('records')
    sf.bulk.Lead.update(list_of_records)

def delete_records_from_lead_object(sf):
    soql_query = """
        SELECT Id
        FROM LEAD
        WHERE LastName = 'Test'
    """
    soql_result = sf.query_all(soql_query)
    df = pd.DataFrame(soql_result.get('records'))
    df.drop(columns=['attributes'], inplace=True)

    list_of_records = df.to_dict('records')
    sf.bulk.Lead.delete(list_of_records)

if __name__ == '__main__':
    sf_instance = establish_salesforce_connection()
    print(sf_instance)

    lead_df = read_lead_object(sf_instance)
    print(lead_df)

    insert_records_into_lead_object(sf_instance)
    update_email_column(sf_instance)
    delete_records_from_lead_object(sf_instance)
