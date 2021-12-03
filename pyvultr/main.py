#! /usr/bin/env python

import logging

from pyvultr.v2 import (
    DNSAPI,
    ISOAPI,
    AccountAPI,
    ApplicationAPI,
    BackupAPI,
    BareMetalAPI,
    BillingAPI,
    BlockStorageAPI,
    FirewallAPI,
    InstanceAPI,
    KubernetesAPI,
    LoadBalanceAPI,
    ObjectStorageAPI,
    OperatingSystemAPI,
    PlanAPI,
    PrivateNetworkAPI,
    RegionAPI,
    ReservedIPAPI,
    SnapshotAPI,
    SSHKeyAPI,
    StartupScriptAPI,
    UserAPI,
)

__author__ = "fishermanadg"
__copyright__ = "Copyright 2021, The pyvultr Project"
__license__ = "License: MIT"
__version__ = "0.1.4"
__email__ = "fishermanadg@gmail.com"


log = logging.getLogger(__name__)


class VultrV2:
    """Python Library for Vultr API(V2).

    Reference: https://www.vultr.com/api/

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: str = None):
        self.account = AccountAPI(api_key)
        self.application = ApplicationAPI(api_key)
        self.backup = BackupAPI(api_key)
        self.bare_metal = BareMetalAPI(api_key)
        self.billing = BillingAPI(api_key)
        self.block_storage = BlockStorageAPI(api_key)
        self.dns = DNSAPI(api_key)
        self.firewall = FirewallAPI(api_key)
        self.instance = InstanceAPI(api_key)
        self.iso = ISOAPI(api_key)
        self.kubernetes = KubernetesAPI(api_key)
        self.load_balance = LoadBalanceAPI(api_key)
        self.object_storage = ObjectStorageAPI(api_key)
        self.operating_system = OperatingSystemAPI(api_key)
        self.plan = PlanAPI(api_key)
        self.private_network = PrivateNetworkAPI(api_key)
        self.region = RegionAPI(api_key)
        self.reserved_ip = ReservedIPAPI(api_key)
        self.snapshot = SnapshotAPI(api_key)
        self.ssh_key = SSHKeyAPI(api_key)
        self.startup_script = StartupScriptAPI(api_key)
        self.user = UserAPI(api_key)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    v2 = VultrV2()
    ...
