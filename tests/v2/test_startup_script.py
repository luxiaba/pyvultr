import uuid

from pyvultr.base_api import SupportHttpMethod
from pyvultr.v2 import StartupScriptItem
from pyvultr.v2.enum import StartupScriptType
from tests.v2 import BaseTestV2


class TestStartupScript(BaseTestV2):
    def test_list(self):
        """Test list scripts."""
        with self._get("response/startup_scripts") as mock:
            _excepted_result = mock.python_body["startup_scripts"][0]
            excepted_result = StartupScriptItem.from_dict(_excepted_result)

            _real_result = self.api_v2.startup_script.list(capacity=1)
            real_result: StartupScriptItem = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/startup-scripts")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create(self):
        """Test create script."""
        with self._post("response/startup_script", expected_returned=StartupScriptItem, status_code=201) as mock:
            excepted_result = mock.python_body

            name = "test_name_1"
            script = "test_script"
            script_type = StartupScriptType.PXE
            real_result: StartupScriptItem = self.api_v2.startup_script.create(
                name=name,
                script=script,
                script_type=script_type,
            )

            self.assertEqual(mock.url, "https://api.vultr.com/v2/startup-scripts")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["name"], name)
            self.assertEqual(mock.req_json["script"], script)
            self.assertEqual(mock.req_json["type"], script_type.value)
            self.assertEqual(mock.status_code, 201)
            self.assertEqual(real_result, excepted_result)

    def test_get(self):
        """Test get script."""
        with self._get("response/startup_script", expected_returned=StartupScriptItem) as mock:
            excepted_result = mock.python_body

            startup_script_id = str(uuid.uuid4())
            real_result: StartupScriptItem = self.api_v2.startup_script.get(startup_id=startup_script_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/startup-scripts/{startup_script_id}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_update(self):
        """Test update script."""
        with self._patch(status_code=204) as mock:
            startup_script_id = str(uuid.uuid4())
            name = "test_name_2"
            real_result: StartupScriptItem = self.api_v2.startup_script.update(startup_script_id, name=name)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/startup-scripts/{startup_script_id}")
            self.assertEqual(mock.method, SupportHttpMethod.PATCH.value)
            self.assertEqual(mock.req_json["name"], name)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_delete(self):
        """Test delete script."""
        with self._delete(status_code=204) as mock:
            startup_script_id = str(uuid.uuid4())
            self.api_v2.startup_script.delete(startup_id=startup_script_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/startup-scripts/{startup_script_id}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
