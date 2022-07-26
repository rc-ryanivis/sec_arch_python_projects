import boto3
import os
import sys
from libs import sigsci_redcanary

def main():
    #CONFIGURATION SECTION
    regions_to_list= ('us-east-1','us-east-2','us-west-1','eu-west-1')

    #USER NOTIFICATION SECTION
    print("You need!!!  to import AWS Credentials into your env vars for boto3 to pick them up. AWS SSO temp credentials can be used.")
    print("You need!!!  to have your sigsci env vars configured for this script to work. Env Vars should look like the following.")
    print("-------- export SIGSCI_EMAIL=name@redcanary.com --------")
    print("-------- export SIGSCI_API_TOKEN=<TOKEN VALUE> --------")
    print("-------- export SIGSCI_CORP=redcanary --------")

    #LOAD IN SIGSCI API Requirements
    sig_sci_api_key=os.environ['SIGSCI_API_TOKEN']
    sig_sci_corp=os.environ['SIGSCI_CORP']
    sig_sci_email=os.environ['SIGSCI_EMAIL']
    sig_sci_site_name="cb_servers"

    sig_sci_list_identifier="site.redcanary-aws-public-ips"

    ################################################################
    ################ PROCESSING SECTION ############################
    list_of_public_ips = []

    ###ENSURES YOUR SIGSCI COMPONENTS ARE SET; IF THEY ARE NOT EXIT
    try:
        sigsciRC = sigsci_redcanary.SigSciApiRedCanary(email=sig_sci_email, api_token=sig_sci_api_key)
        sigsciRC.corp = sig_sci_corp
    except:
        print("No User / API Key was found / or no corp was found.... Exit.")
        sys.exit(1)

    ###USE BOTO3 TO EXTRACT THE PUBLIC IPs
    for region in regions_to_list:
        client = boto3.client(    
            'ec2', 
            region )

        addresses_dict = client.describe_addresses()
        for eip_dict in addresses_dict['Addresses']:
            list_of_public_ips.append(eip_dict['PublicIp'])

    ###BUILD DATA OBJECT TO PUSH TO SIGSCI API TO UPDATE THE DYNAMIC LIST
    data_obj = {
        "description": "List of all public IP addresses inside of the Primary Red Canary AWS Account All Regions.",
        "entries": list_of_public_ips
    }

    #INTERACT WITH THE SIGSCI API TO UPDATE THE LIST
    sigsciRC.update_site_rule_lists(site_name=sig_sci_site_name,data=data_obj,identifier=sig_sci_list_identifier)

    print(str(data_obj) + "  <-- Pushed to SigSci.")

    ############## END PROCESSING SECTION ##########################
    ################################################################


if __name__ == "__main__":
    main()