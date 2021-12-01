import uuid
from typing import Dict, List

from pyvultr.base_api import SupportHttpMethod
from pyvultr.utils import get_only_value
from pyvultr.v2 import (
    AvailableUpgrade,
    BackupSchedule,
    BandwidthItem,
    InstanceItem,
    InstancePrivateNetworkItem,
    IPv4Item,
    IPv6Item,
    IPv6ReverseItem,
    ISOStatus,
    RestoreStatus,
    UserData,
)
from pyvultr.v2.enum import BackupScheduleType
from tests.base import BaseTest


class TestInstance(BaseTest):
    def test_list(self):
        """Test list instance."""
        with self._get("response/instances") as mock:
            _excepted_result = mock.python_body["instances"][0]
            excepted_result = InstanceItem.from_dict(_excepted_result)

            _real_result = self.api_v2.instance.list(capacity=1)
            real_result: InstanceItem = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/instances")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create(self):
        """Test create."""
        with self._post("response/instance", expected_returned=InstanceItem) as mock:
            excepted_result = mock.python_body

            region = "ams"
            plan = "test_plan"
            real_result: InstanceItem = self.api_v2.instance.create(region=region, plan=plan)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/instances")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(real_result, excepted_result)

    def test_get(self):
        """Test get instance."""
        with self._get("response/instance", expected_returned=InstanceItem) as mock:
            excepted_result = mock.python_body

            instance_id = str(uuid.uuid4())
            real_result: InstanceItem = self.api_v2.instance.get(instance_id=instance_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_update(self):
        """Test update."""
        with self._patch("response/instance", expected_returned=InstanceItem) as mock:
            excepted_result = mock.python_body

            instance_id = str(uuid.uuid4())
            plan = "test_plan"
            real_result: InstanceItem = self.api_v2.instance.update(instance_id=instance_id, plan=plan)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}")
            self.assertEqual(mock.method, SupportHttpMethod.PATCH.value)
            self.assertEqual(mock.req_json["plan"], plan)
            self.assertEqual(real_result, excepted_result)

    def test_delete(self):
        """Test delete."""
        with self._delete(status_code=204) as mock:
            instance_id = str(uuid.uuid4())
            real_result = self.api_v2.instance.delete(instance_id=instance_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_batch_halt(self):
        """Test batch halt instances."""
        with self._post(status_code=204) as mock:

            instance_ids = [str(uuid.uuid4()) for _ in range(10)]
            resp = self.api_v2.instance.batch_halt(instance_ids)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/instances/halt")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json, {"instance_ids": instance_ids})
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(resp)

    def test_batch_reboot(self):
        """Test batch reboot instances."""
        with self._post(status_code=204) as mock:

            instance_ids = [str(uuid.uuid4()) for _ in range(10)]
            resp = self.api_v2.instance.batch_reboot(instance_ids)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/instances/reboot")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json, {"instance_ids": instance_ids})
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(resp)

    def test_batch_start(self):
        """Test batch start instances."""
        with self._post(status_code=204) as mock:

            instance_ids = [str(uuid.uuid4()) for _ in range(10)]
            resp = self.api_v2.instance.batch_start(instance_ids)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/instances/start")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json, {"instance_ids": instance_ids})
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(resp)

    def test_start(self):
        """Test start."""
        with self._post(status_code=204) as mock:

            instance_ids = [str(uuid.uuid4()) for _ in range(10)]
            resp = self.api_v2.instance.batch_start(instance_ids)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/instances/start")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json, {"instance_ids": instance_ids})
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(resp)

    def test_reboot(self):
        """Test reboot."""
        with self._post(status_code=204) as mock:

            instance_id = str(uuid.uuid4())
            resp = self.api_v2.instance.reboot(instance_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/reboot")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(resp)

    def test_reinstall(self):
        """Test reinstall."""
        with self._post("response/instance", expected_returned=InstanceItem, status_code=202) as mock:
            excepted_result: InstanceItem = mock.python_body

            instance_id = str(uuid.uuid4())
            real_result: InstanceItem = self.api_v2.instance.reinstall(instance_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/reinstall")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.status_code, 202)
            self.assertEqual(real_result, excepted_result)

    def test_get_bandwidth(self):
        """Test get bandwidth."""
        with self._get("response/instance_bandwidth") as mock:
            _excepted_result = mock.python_body["bandwidth"]
            excepted_result = {_date: BandwidthItem.from_dict(item) for _date, item in _excepted_result.items()}

            instance_id = str(uuid.uuid4())
            real_result: Dict[str, BandwidthItem] = self.api_v2.instance.get_bandwidth(instance_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/bandwidth")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_list_neighbors(self):
        """Test list neighbors."""
        with self._get("response/instance_neighbors") as mock:
            excepted_result: List[str] = get_only_value(mock.python_body)

            instance_id = str(uuid.uuid4())
            real_result: Dict[str, BandwidthItem] = self.api_v2.instance.list_neighbors(instance_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/neighbors")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_list_private_networks(self):
        """Test list_private_networks."""
        with self._get("response/instances_private_networks") as mock:
            _excepted_result = mock.python_body["private_networks"][0]
            excepted_result = InstancePrivateNetworkItem.from_dict(_excepted_result)

            instance_id = str(uuid.uuid4())
            _real_result = self.api_v2.instance.list_private_networks(instance_id=instance_id, capacity=1)
            real_result: InstancePrivateNetworkItem = _real_result.first()

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/private-networks")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_get_iso_status(self):
        """Test get iso status."""
        with self._get("response/instances_iso_status") as mock:
            excepted_result: ISOStatus = ISOStatus.from_dict(get_only_value(mock.python_body))

            instance_id = str(uuid.uuid4())
            real_result: ISOStatus = self.api_v2.instance.get_iso_status(instance_id=instance_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/iso")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_attach_iso(self):
        """Test attach iso."""
        with self._post(status_code=202) as mock:
            instance_id = str(uuid.uuid4())
            real_result = self.api_v2.instance.attach_iso(instance_id=instance_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/iso/attach")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.status_code, 202)
            self.assertIsNone(real_result)

    def test_detach_iso(self):
        """Test detach_iso."""
        with self._post(status_code=202) as mock:
            instance_id = str(uuid.uuid4())
            real_result = self.api_v2.instance.detach_iso(instance_id=instance_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/iso/detach")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.status_code, 202)
            self.assertIsNone(real_result)

    def test_attach_private_network(self):
        """Test attach private network."""
        with self._post(status_code=202) as mock:
            instance_id = str(uuid.uuid4())
            network_id = str(uuid.uuid4())
            real_result = self.api_v2.instance.attach_private_network(instance_id, network_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/private-networks/attach")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.status_code, 202)
            self.assertIsNone(real_result)

    def test_detach_private_network(self):
        """Test detach private network."""
        with self._post(status_code=202) as mock:
            instance_id = str(uuid.uuid4())
            real_result = self.api_v2.instance.detach_private_network(instance_id=instance_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/private-networks/detach")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.status_code, 202)
            self.assertIsNone(real_result)

    def test_set_backup_schedule(self):
        """Test set backup schedule."""
        with self._post("response/instances_backup_schedule") as mock:
            excepted_result: BackupSchedule = BackupSchedule.from_dict(get_only_value(mock.python_body))

            instance_id = str(uuid.uuid4())
            backup_type = BackupScheduleType.WEEKLY
            real_result: BackupSchedule = self.api_v2.instance.set_backup_schedule(instance_id, backup_type)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/backup-schedule")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(real_result, excepted_result)

    def test_get_backup_schedule(self):
        """Test get backup schedule."""
        with self._get("response/instances_backup_schedule") as mock:
            excepted_result: BackupSchedule = BackupSchedule.from_dict(get_only_value(mock.python_body))

            instance_id = str(uuid.uuid4())
            real_result: BackupSchedule = self.api_v2.instance.get_backup_schedule(instance_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/backup-schedule")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_restore(self):
        """Test restore."""
        with self._post("response/instances_restore", status_code=202) as mock:
            excepted_result = RestoreStatus.from_dict(get_only_value(mock.python_body))

            instance_id = str(uuid.uuid4())
            backup_id = str(uuid.uuid4())
            real_result = self.api_v2.instance.restore(instance_id=instance_id, backup_id=backup_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/restore")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.status_code, 202)
            self.assertEqual(real_result, excepted_result)

    def test_list_ipv4s(self):
        """Test list_ipv4s."""
        with self._get("response/instance_ipv4s") as mock:
            _excepted_result = mock.python_body["ipv4s"][0]
            excepted_result = IPv4Item.from_dict(_excepted_result)

            instance_id = str(uuid.uuid4())
            _real_result = self.api_v2.instance.list_ipv4s(instance_id, capacity=1)
            real_result: IPv4Item = _real_result.first()

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/ipv4")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create_ipv4(self):
        """Test create ipv4."""
        with self._post("response/instance_ipv4", expected_returned=IPv4Item) as mock:
            excepted_result: IPv4Item = mock.python_body

            instance_id = str(uuid.uuid4())
            reboot = False
            real_result: IPv4Item = self.api_v2.instance.create_ipv4(instance_id=instance_id, reboot=reboot)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/ipv4")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["reboot"], reboot)
            self.assertEqual(real_result, excepted_result)

    def test_list_ipv6s(self):
        """Test list_ipv6s."""
        with self._get("response/instance_ipv6s") as mock:
            _excepted_result = mock.python_body["ipv6s"][0]
            excepted_result = IPv6Item.from_dict(_excepted_result)

            instance_id = str(uuid.uuid4())
            _real_result = self.api_v2.instance.list_ipv6s(instance_id, capacity=1)
            real_result: IPv6Item = _real_result.first()

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/ipv6")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create_ipv6_reverse(self):
        """Test create_ipv6_reverse."""
        with self._post(status_code=204) as mock:
            instance_id = str(uuid.uuid4())
            ip = "test_ip"
            reverse = "test_reverse"
            real_result = self.api_v2.instance.create_ipv6_reverse(instance_id=instance_id, ip=ip, reverse=reverse)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/ipv6/reverse")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["ip"], ip)
            self.assertEqual(mock.req_json["reverse"], reverse)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_list_ipv6_reverses(self):
        """Test list_ipv6_reverses."""
        with self._get("response/instance_reverse_ipv6s") as mock:
            _excepted_result = get_only_value(mock.python_body)
            excepted_result: List[IPv6ReverseItem] = [IPv6ReverseItem.from_dict(i) for i in _excepted_result]

            instance_id = str(uuid.uuid4())
            real_result: List[IPv6ReverseItem] = self.api_v2.instance.list_ipv6_reverses(instance_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/ipv6/reverse")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create_ipv4_reverse(self):
        """Test create_ipv4_reverse."""
        with self._post(status_code=204) as mock:
            instance_id = str(uuid.uuid4())
            ip = "test_ip_2"
            reverse = "test_reverse_2"
            real_result = self.api_v2.instance.create_ipv4_reverse(instance_id=instance_id, ip=ip, reverse=reverse)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/ipv4/reverse")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["ip"], ip)
            self.assertEqual(mock.req_json["reverse"], reverse)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_get_user_date(self):
        """Test get_user_date."""
        with self._get("response/instance_user_data", expected_returned=UserData) as mock:
            excepted_result: UserData = mock.python_body

            instance_id = str(uuid.uuid4())
            real_result: UserData = self.api_v2.instance.get_user_date(instance_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/user-data")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_halt(self):
        """Test halt."""
        with self._post(status_code=204) as mock:

            instance_id = str(uuid.uuid4())
            resp = self.api_v2.instance.halt(instance_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/halt")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(resp)

    def test_set_default_reverse_dns_entry(self):
        """Test set_default_reverse_dns_entry."""
        with self._delete(status_code=204) as mock:
            instance_id = str(uuid.uuid4())
            ip = "127.0.0.1"
            real_result = self.api_v2.instance.set_default_reverse_dns_entry(instance_id=instance_id, ip=ip)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/reverse/default")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.req_json["ip"], ip)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_delete_ipv4(self):
        """Test delete_ipv4."""
        with self._delete(status_code=204) as mock:

            instance_id = str(uuid.uuid4())
            ipv4 = "127.0.0.1"
            resp = self.api_v2.instance.delete_ipv4(instance_id=instance_id, ipv4=ipv4)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/ipv4/{ipv4}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(resp)

    def test_delete_reverse_ipv6(self):
        """Test delete_reverse_ipv6."""
        with self._delete(status_code=204) as mock:
            instance_id = str(uuid.uuid4())
            ipv6 = "ipv6"
            real_result = self.api_v2.instance.delete_reverse_ipv6(instance_id=instance_id, ipv6=ipv6)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/ipv6/reverse/{ipv6}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_list_upgrades(self):
        """Test list upgrades."""
        with self._get("response/instance_upgrades", expected_returned=AvailableUpgrade) as mock:
            excepted_result: AvailableUpgrade = mock.python_body

            instance_id = str(uuid.uuid4())
            real_result: AvailableUpgrade = self.api_v2.instance.list_upgrades(instance_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/instances/{instance_id}/upgrades")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)
