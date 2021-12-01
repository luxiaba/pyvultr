from pyvultr.v2 import ApplicationItem
from pyvultr.v2.enum import ApplicationType
from tests.v2 import BaseTestV2


class TestApplication(BaseTestV2):
    def test_list(self):
        """Test get application."""
        real_result = self.api_v2.application.list(capacity=1, app_type=ApplicationType.MARKETPLACE)
        application: ApplicationItem = real_result.first()

        self.assertEqual(application.deploy_name, "CloudPanel 1 on Debian 10.11")
        self.assertEqual(application.id, 1003)
        self.assertEqual(application.image_id, "cloudpanel-1")
        self.assertEqual(application.name, "CloudPanel 1")
        self.assertEqual(application.short_name, "cloudpanel1")
        self.assertEqual(application.type, "marketplace")
        self.assertEqual(application.vendor, "cloudpanel")
