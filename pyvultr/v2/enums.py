from enum import unique

from pyvultr.utils import Enums


@unique
class ApplicationType(Enums):
    MARKETPLACE = "marketplace"
    ONE_CLICK = "one-click"
    ALL = "all"  # just for search.


@unique
class BackupStatus(Enums):
    COMPLETE = "complete"
    PENDING = "pending"


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
class IPType(Enums):
    V4 = "v4"
    V6 = "v6"


@unique
class LoadBalanceProtocol(Enums):
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    TCP = "TCP"


@unique
class BareMetalStatus(Enums):
    ACTIVE = "active"
    REBOOTING = "rebooting"
    HALTED = "halted"


@unique
class IPV4Type(Enums):
    MAIN_IP = "main_ip"


@unique
class IPV6Type(Enums):
    MAIN_IP = "main_ip"


@unique
class BareMetalUpgradeType(Enums):
    ALL = "all"
    APPLICATIONS = "applications"
    OS = "os"


@unique
class InvoiceUnitType(Enums):
    HOURS = "hours"
    OVERAGE = "overage"
    DISCOUNT = "discount"


@unique
class BlockStorageStatus(Enums):
    ACTIVE = "active"


@unique
class DomainDNSSECStatus(Enums):
    ENABLED = "enabled"
    DISABLED = "disabled"


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
class FirewallRuleAction(Enums):
    ACCEPT = "accept"


@unique
class FirewallProtocol(Enums):
    ICMP = "ICMP"
    TCP = "TCP"
    UDP = "UDP"
    GRE = "GRE"
    ESP = "ESP"
    AH = "AH"


@unique
class FirewallRuleSource(Enums):
    SUBNET = ""
    CLOUDFLARE = "cloudflare"


@unique
class InstanceStatus(Enums):
    ACTIVE = "active"
    HALTED = "halted"
    REBOOTING = "rebooting"
    resizing = "resizing"


@unique
class InstancePowerStatus(Enums):
    RUNNING = "running"


@unique
class InstanceServerStatus(Enums):
    OK = "ok"


@unique
class InstanceFeatures(Enums):
    AUTO_BACKUPS = "auto_backups"
    IPV6 = "ipv6"
    DDOS_PROTECTION = "ddos_protection"


@unique
class ISOStatusState(Enums):
    READY = "ready"
    ATTACHED = "attached"


@unique
class InstanceUpgradeType(Enums):
    ALL = "all"
    APPLICATIONS = "applications"
    OS = "os"
    PLANS = "plans"


@unique
class ISOStatus(Enums):
    COMPLETE = "complete"
    PENDING = "pending"


@unique
class LoadBalanceStatus(Enums):
    active = "active"


@unique
class LoadBalanceAlgorithm(Enums):
    ROUND_ROBIN = "roundrobin"
    LEAST_CONN = "leastconn"


@unique
class BackupScheduleType(Enums):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    DAILY_ALT_EVEN = "daily_alt_even"
    DAILY_ALT_ODD = "daily_alt_odd"


@unique
class ObjectStorageStatus(Enums):
    ACTIVE = "active"
    PENDING = "pending"


@unique
class ObjectStorageClusterDeployStatus(Enums):
    YES = "yes"
    NO = "no"


@unique
class PlayType(Enums):
    vc2 = "vc2"  # Cloud Compute
    vhf = "vhf"  # High Frequency Compute
    vdc = "vdc"  # Dedicated Cloud


@unique
class BareMetalPlayType(Enums):
    SSD = "SSD"


@unique
class SnapshotStatus(Enums):
    PENDING = "pending"
    COMPLETE = "complete"
    DELETED = "deleted"


@unique
class StartupScriptType(Enums):
    BOOT = "boot"
    PXE = "pxe"
