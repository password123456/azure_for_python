
import sys
from azure.identity import ClientSecretCredential
from azure.core.exceptions import ClientAuthenticationError


def main():
    AZURE_CLIENT_ID = '~~~~~'
    AZURE_CLIENT_SECRET = '~~~~'
    AZURE_TENANT_ID = '~~~~'

    credential = ClientSecretCredential(
        client_id=AZURE_CLIENT_ID,
        client_secret=AZURE_CLIENT_SECRET,
        tenant_id=AZURE_TENANT_ID
    )

    try:
        token = credential.get_token('https://management.azure.com/.default')
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

Access Token: eyJ0eXAiOiJKV1QiLCJhb....
"""
