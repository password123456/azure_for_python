
import sys
from azure.identity import DefaultAzureCredential
from azure.core.exceptions import ClientAuthenticationError


# you have to defind environment-variables
# https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python#environment-variables
# --> AZURE_CLIENT_ID	ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET
#
# To execute the code in Azure's Automation service, only the subscription ID is required. (No Need AZURE_CLIENT_ID	ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET)

def main():
    credentials = DefaultAzureCredential()

    try:
        token = credentials.get_token('https://management.azure.com/.default')
        print("Access Token:", token.token)
    except ClientAuthenticationError as ex:
        print("Failed to authenticate:", ex.message)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f'(Exception) Func:[{__name__.__name__}] '
              f'Line:[{sys.exc_info()[-1].tb_lineno}] [{type(e).__name__}] {e}')


"""
RESULT

Access Token: eyJ0eXAiOiJKV1QiLCJhbG....
"""
