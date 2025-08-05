from dataclasses import dataclass


@dataclass
class Storage:
    repository: str
    ova_store_to: str
    vms_store_to: str
    import_log_store_to: str