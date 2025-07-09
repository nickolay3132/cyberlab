from src.core.use_cases.vm_commands.InstallCommand import InstallCommand, InstallCommandDTO
from src.infrastructure.containers.Repos import Repos


class BaseCommands:
    def __init__(self,
                 install_command: InstallCommand,
    ):
        self.install_command=install_command

    def install(self, args):
        install_use_case_dto = InstallCommandDTO(
            skip_download=args.skip_download,
            no_verify=args.no_verify,
        )

        self.install_command.execute(install_use_case_dto)

    def startup(self, args):
        # print(f"Configuration path: {self.config_path}")
        print("Starting up...")

    def shutdown(self, args):
        # print(f"Configuration path: {self.config_path}")
        print("Shutting down...")
