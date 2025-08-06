import subprocess

from src.core.interfaces.gateways import IVmsBootGateway


class VmsBootGatewayImpl(IVmsBootGateway):
    def startup(self, vm_name: str, startup_type: str) -> bool:
        cmd = [
            "VBoxManage", "startvm", vm_name, "--type", startup_type
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()

        return process.returncode == 0

    def shutdown(self, vm_name: str, shutdown_type: str) -> bool:
        cmd = [
            "VBoxManage", "controlvm", vm_name, shutdown_type
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        process.wait()

        return process.returncode == 0