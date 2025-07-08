from src.core.use_cases.vm_commands.InstallCommand import InstallCommand, InstallCommandDTO
from src.infrastructure.containers.Repos import Repos


class BaseCommands:
    def __init__(self,
                 install_command: InstallCommand,
    ):
        self.install_command=install_command

    def install(self, args):
        print("Installing...")

        install_use_case_dto = InstallCommandDTO(
            skip_download=args.skip_download,
            no_verify=args.no_verify,
        )

        self.install_command.execute(install_use_case_dto)

        # install_use_case = InstallCommand(self.repos.storage_repository(), self.repos.virtual_machines_repository())
        # install_use_case.execute(InstallCommandDTO(
        #     skip_download=args.skip_download,
        #     no_verify=args.no_verify,
        # ))

    def startup(self, args):
        # print(f"Configuration path: {self.config_path}")
        print("Starting up...")

    def shutdown(self, args):
        # print(f"Configuration path: {self.config_path}")
        print("Shutting down...")
