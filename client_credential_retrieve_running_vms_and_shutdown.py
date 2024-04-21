import sys
from datetime import datetime, timedelta
from azure.identity import ClientSecretCredential
from azure.mgmt.compute import ComputeManagementClient


def shutdown_vdi():
    AZURE_CLIENT_ID = '~~~~~'
    AZURE_CLIENT_SECRET = '~~~~'
    AZURE_TENANT_ID = '~~~~'
    SUBSCRIPTION_ID = '~~~~~'

    credential = ClientSecretCredential(
        client_id=AZURE_CLIENT_ID,
        client_secret=AZURE_CLIENT_SECRET,
        tenant_id=AZURE_TENANT_ID
    )

    compute_client = ComputeManagementClient(credential, SUBSCRIPTION_ID)

    content_result = ''
    contents = ''
    n = 0
  
    resource_group_name = 'resourece-group-name-to_start_vms'
    running_vms = 0

    vms = compute_client.virtual_machines.list(resource_group_name)
    for vm in vms:
        vm_instance_view = compute_client.virtual_machines.instance_view(resource_group_name, vm.name)
        for status in vm_instance_view.statuses:
            if status.code.startswith('PowerState/running'):
                running_vms += 1

    # if running_vms exists
    if int(running_vms) >= 1:
        vms = compute_client.virtual_machines.list(resource_group_name)
        for vm in vms:
            n += 1
            vm_instance_view = compute_client.virtual_machines.instance_view(resource_group_name, vm.name)
            for status in vm_instance_view.statuses:
                if status.code.startswith('PowerState/running'):
                    async_vm_stop = compute_client.virtual_machines.begin_deallocate(resource_group_name, vm.name)
                    result_status = async_vm_stop.wait()
                    if result_status is None:
                        contents = f' ✓ Successfully stopped VM: {vm.name} in {resource_group_name}\n'
                    else:
                        contents = (f' ✗ Failed to stop VM: {vm.name} in {resource_group_name}\n'
                                    f'  -> Shut it down manually.')
                else:
                    contents = f' ⦿ Already stopped VM: {vm.name} in {resource_group_name}\n'
            content_result += contents
    else:
        content_result = f' ✓ No VMs to shut down in "{resource_group_name}"\n'
    

    if content_result:
        current_utc_datetime = datetime.utcnow()
        current_kst_datetime = current_utc_datetime + timedelta(hours=9)
        current_datetime = current_kst_datetime.strftime('%Y-%m-%d %H:%M:%S.%f')
        content_bottom = f'>> Total VMs started: {n}\n>> Completion time: {current_datetime}'
        content_result = f'{content_result}\n{content_bottom}'
    return content_result


def main():
    shutdown_result = shutdown_vdi()
    print(shutdown_result)


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
