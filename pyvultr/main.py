import logging

from pyvultr.v2 import (
    DNS,
    ISO,
    Account,
    Application,
    Backup,
    BareMetal,
    Billing,
    BlockStorage,
    Firewall,
    Instance,
    Kubernetes,
    LoadBalance,
    ObjectStorage,
    OperatingSystem,
    Plan,
    PrivateNetwork,
    Region,
    ReservedIP,
    Snapshot,
    SSHKey,
    StartupScript,
    User,
)

log = logging.getLogger(__name__)


class VultrV2:
    def __init__(self, api_key: str = None):
        self.account = Account(api_key)
        self.application = Application(api_key)
        self.backup = Backup(api_key)
        self.bare_metal = BareMetal(api_key)
        self.billing = Billing(api_key)
        self.block_storage = BlockStorage(api_key)
        self.dns = DNS(api_key)
        self.firewall = Firewall(api_key)
        self.instance = Instance(api_key)
        self.iso = ISO(api_key)
        self.kubernetes = Kubernetes(api_key)
        self.load_balance = LoadBalance(api_key)
        self.object_storage = ObjectStorage(api_key)
        self.operating_system = OperatingSystem(api_key)
        self.plan = Plan(api_key)
        self.private_network = PrivateNetwork(api_key)
        self.region = Region(api_key)
        self.reserved_ip = ReservedIP(api_key)
        self.snapshot = Snapshot(api_key)
        self.ssh_key = SSHKey(api_key)
        self.startup_script = StartupScript(api_key)
        self.user = User(api_key)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    v2 = VultrV2()
    log.warning(v2.account.get())
