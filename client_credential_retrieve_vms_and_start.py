import sys
from datetime import datetime, timedelta
from azure.identity import ClientSecretCredential
from azure.core.exceptions import ClientAuthenticationError
from azure.mgmt.compute import ComputeManagementClient


def start_vdi():
    AZURE_CLIENT_ID = '~~~~~'
    AZURE_CLIENT_SECRET = '~~~~'
    AZURE_TENANT_ID = '~~~~'
    SUBSCRIPTION_ID = '~~~~~'

    credential = ClientSecretCredential(
        client_id=AZURE_CLIENT_ID,
        client_secret=AZURE_CLIENT_SECRET,
        tenant_id=AZURE_TENANT_ID
    )

    try:
        token = credential.get_token('https://management.azure.com/.default')
        # print(token)

        resource_group_name = 'resourece-group-name-to_start_vms'
        compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)

        # vm_list = compute_client.virtual_machines.list_all()
        vms = compute_client.virtual_machines.list(resource_group_name)

        content_result = ''
        contents = ''
        n = 0

        for vm in vms:
            n += 1
            vm_status = compute_client.virtual_machines.instance_view(resource_group_name, vm.name).statuses
            power_state = next((s for s in vm_status if s.code.startswith('PowerState/')), None)

            if power_state and 'running' in power_state.code:
                contents = f' ⦿ Already running VM: {vm.name} in {vm.location}\n'
            elif power_state and ('deallocated' in power_state.code or 'stopped' in power_state.code):
                compute_client.virtual_machines.begin_start(resource_group_name, vm.name)
                contents = f' ✓ Successfully started VM: {vm.name} in {vm.location}\n'
            content_result += contents 
        
    except ClientAuthenticationError as ex:
        print("Failed to authenticate:", ex.message)


    if content_result:
        current_utc_datetime = datetime.utcnow()
        current_kst_datetime = current_utc_datetime + timedelta(hours=9)
        current_datetime = current_kst_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
        content_bottom = f'>> Total VMs started: {n}\n>> Completion time: {current_datetime}'
        content_result = f'{content_result}\n{content_bottom}'
    return content_result


def main():
    start_result = start_vdi()
    print(start_result)


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
