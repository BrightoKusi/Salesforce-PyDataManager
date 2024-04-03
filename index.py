import os
import pandas as pd
from simple_salesforce import Salesforce, SalesforceLogin
import configparser

def establish_salesforce_connection():
    """
    Establishes connection to Salesforce using credentials from .env file.
    Returns Salesforce instance.
    """
    config = configparser.ConfigParser()
    config.read('.env')

    username = config['SfLoginInfo']['username']
    password = config['SfLoginInfo']['password']
    security_token = config['SfLoginInfo']['security_token']
    domain = 'login'

    session_id, instance = SalesforceLogin(username=username, password=password, security_token=security_token, domain=domain)
    sf_instance = Salesforce(instance=instance, session_id=session_id)

    return sf_instance

def explore_salesforce_attributes(sf_instance):
    """
    Prints out non-private attributes of the Salesforce instance.
    """
    print("Exploring Salesforce instance attributes:")
    for element in dir(sf_instance):
        if not element.startswith('_'):
            if isinstance(getattr(sf_instance, element), str):
                print('Property Name: {0}; Value: {1}'.format(element, getattr(sf_instance, element)))

def get_salesforce_metadata(sf_instance):
    """
    Retrieves and returns metadata information from Salesforce.
    """
    print("Retrieving Salesforce metadata information...")
    return sf_instance.describe()

def write_to_csv(dataframe, filename):
    """
    Writes DataFrame to a CSV file.
    """
    dataframe.to_csv(filename, index=False)
    print("Data written to", filename)

if __name__ == '__main__':
    # Establish Salesforce connection
    try:
        sf_instance = establish_salesforce_connection()
        print("Salesforce connection established successfully.")
    except Exception as e:
        print("Failed to establish Salesforce connection:", str(e))
        exit()

    # Explore Salesforce instance attributes
    explore_salesforce_attributes(sf_instance)

    # Get Salesforce metadata
    try:
        metadata_org = get_salesforce_metadata(sf_instance)
        print("Metadata retrieved successfully.")
    except Exception as e:
        print("Failed to retrieve Salesforce metadata:", str(e))
        exit()

    # Write Salesforce metadata to CSV
    try:
        df_sobjects = pd.DataFrame(metadata_org['sobjects'])
        write_to_csv(df_sobjects, 'org_metadata_info.csv')
    except Exception as e:
        print("Failed to write metadata to CSV:", str(e))
        exit()

    # Write Salesforce account metadata to CSV
    try:
        account = sf_instance.account
        account_metadata = account.describe()
        df_account_metadata = pd.DataFrame(account_metadata.get('fields'))
        write_to_csv(df_account_metadata, 'account_object_metadata.csv')
    except Exception as e:
        print("Failed to write account metadata to CSV:", str(e))
        exit()
