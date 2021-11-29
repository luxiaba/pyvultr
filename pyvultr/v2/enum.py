from enum import unique

from pyvultr.utils import Enums


@unique
class ApplicationType(Enums):
    ALL = "all"
    MARKETPLACE = "marketplace"
    ONE_CLICK = "one-click"


@unique
class RegionType(Enums):
    ALL = "all"  # All available types
    VC2 = "vc2"  # Cloud Compute
    VDC = "vdc"  # Dedicated Cloud
    VHF = "vhf"  # High Frequency Compute
    VBM = "vbm"  # Bare Metal


@unique
class ACL(Enums):
    ABUSE = "abuse"
    ALERTS = "alerts"
    BILLING = "billing"
    DNS = "dns"
    FIREWALL = "firewall"
    LOAD_BALANCER = "loadbalancer"
    MANAGE_USERS = "manage_users"
    OBJ_STORE = "objstore"
    PROVISIONING = "provisioning"
    SUBSCRIPTIONS = "subscriptions"
    SUBSCRIPTIONS_VIEW = "subscriptions_view"
    SUPPORT = "support"
    UPGRADE = "upgrade"


@unique
class StartupScriptType(Enums):
    BOOT = "boot"
    PXE = "pxe"


@unique
class IPType(Enums):
    V4 = "v4"
    V6 = "v6"


@unique
class Protocol(Enums):
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    TCP = "TCP"


@unique
class FirewallProtocol(Enums):
    ICMP = "ICMP"
    TCP = "TCP"
    UDP = "UDP"
    GRE = "GRE"
    ESP = "ESP"
    AH = "AH"


@unique
class BareMetalUpgradeType(Enums):
    ALL = "all"
    APPLICATIONS = "applications"
    OS = "os"


@unique
class InstanceUpgradeType(Enums):
    ALL = "all"
    APPLICATIONS = "applications"
    OS = "os"
    PLANS = "plans"


@unique
class DNSRecordType(Enums):
    A = "A"
    AAAA = "AAAA"
    CNAME = "CNAME"
    NS = "NS"
    MX = "MX"
    SRV = "SRV"
    TXT = "TXT"
    CAA = "CAA"
    SSHFP = "SSHFP"


@unique
class BackupScheduleType(Enums):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    DAILY_ALT_EVEN = "daily_alt_even"
    DAILY_ALT_ODD = "daily_alt_odd"
