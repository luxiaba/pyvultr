from typing import List

from pyvultr.v2 import RegionItem
from pyvultr.v2.enum import RegionType
from tests.v2 import BaseTestV2


class TestRegion(BaseTestV2):
    def test_list(self):
        """Test list plan."""
        real_result = self.api_v2.region.list(capacity=1)
        region: RegionItem = real_result.first()

        self.assertEqual(region.id, "ams")
        self.assertEqual(region.country, "NL")
        self.assertEqual(region.options, ["ddos_protection"])
        self.assertEqual(region.continent, "Europe")
        self.assertEqual(region.city, "Amsterdam")

    def test_list_in_region(self):
        """Test list bare metal plan."""
        real_result: List[str] = self.api_v2.region.list_in_region("ams", region_type=RegionType.VC2)

        self.assertIn("vc2-4c-8gb", real_result)
        self.assertNotIn(None, real_result)
