
import sys
from datetime import datetime, timedelta
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.core.exceptions import ClientAuthenticationError


def runcommand_vdi():
    az_client_id = os.getenv("AZURE_CLIENT_ID")
    az_client_secret = os.getenv("AZURE_CLIENT_SECRET")
    az_tenant_id = os.getenv("AZURE_TENANT_ID")
    subscription_id = os.getenv("SUBSCRIPTION_ID")

    try:
        credential = ClientSecretCredential(
            client_id=az_client_id,
            client_secret=az_client_secret,
            tenant_id=az_tenant_id
        )

        resource_group_name = 'name of the resource group containing the VM to execute the run_command'
        machine_name_to_run = 'win2019-datacenter'

        run_command_parameters = {
            'command_id': 'RunPowerShellScript',
            'script': [
                '(query session | Select-String active).Matches.Count'
            ]
        }

        compute_client = ComputeManagementClient(credential, subscription_id)
        poller = compute_client.virtual_machines.begin_run_command(
            resource_group_name=resource_group_name,
            vm_name=machine_name_to_run,
            parameters=run_command_parameters
        )

        result = poller.result()  # Blocking till executed
        print(result.value[0].message)  # stdout/stderr

    except ClientAuthenticationError as ex:
        print("Failed to authenticate:", ex.message)


def main():
    runcommand_vdi()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception as e:
        print(f'(Exception) Func:[{__name__.__name__}] '
              f'Line:[{sys.exc_info()[-1].tb_lineno}] [{type(e).__name__}] {e}')


"""
requirements.txt

azure-identity
azure-mgmt-compute
"""


"""
Run Command examples

(1) Load files and run
with open('check_session.ps1', 'r') as f:
    script = f.read()
run_command_parameters = {
    'command_id': 'RunPowerShellScript',
    'script': [
        script
    ]
}

(2) Execute a specific script inside the VM.
run_command_parameters = {
    'command_id': 'RunPowerShellScript',
    'script': [
        'c:\mgmt\check_sessions.ps1'
    ]
}
"""
