from src.bootstrap import get
from src.bootstrap.binder import bind

from src.core.interfaces.gateways import IVMsGateway, IVmsNetworkGateway, IVmsBootGateway
from src.core.interfaces.services import IFileSystemService, IParallelTaskService
from src.core.interfaces.services.vms import (IImportVMService,
                                              IInstallVMService,
                                              IVmNetworkService,
                                              IVmBootService)

from src.infrastructure.services import FileSystemServiceImpl, ParallelTaskServiceImpl
from src.infrastructure.services.vms import (ImportVMServiceImpl,
                                             InstallVMServiceImpl,
                                             VmNetworkServiceImpl,
                                             VmBootServiceImpl)


@bind
def make_file_system_service() -> IFileSystemService:
    return FileSystemServiceImpl()

@bind
def make_parallel_task_service() -> IParallelTaskService:
    return ParallelTaskServiceImpl()

@bind
def make_vm_networks_service() -> IVmNetworkService:
    vms_network_gateway = get(IVmsNetworkGateway)()

    return VmNetworkServiceImpl(vms_network_gateway)

@bind
def make_vm_boot_service() -> IVmBootService:
    vms_boot_gateway = get(IVmsBootGateway)()

    return VmBootServiceImpl(vms_boot_gateway)

@bind
def make_import_vm_service() -> IImportVMService:
    file_system_service = get(IFileSystemService)()
    parallel_task_service = get(IParallelTaskService)()
    vms_gateway = get(IVMsGateway)()

    return ImportVMServiceImpl(file_system_service, parallel_task_service, vms_gateway)

@bind
def make_install_vm_service() -> IInstallVMService:
    file_system_service = get(IFileSystemService)()

    return InstallVMServiceImpl(file_system_service)