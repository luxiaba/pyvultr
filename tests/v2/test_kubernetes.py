import uuid
from typing import List

from pyvultr.base_api import SupportHttpMethod
from pyvultr.utils import get_only_value
from pyvultr.v2 import ClusterItem, ClusterNodePool, ClusterNodePoolFull, ClusterResource
from tests.base import BaseTest


class TestKubernetes(BaseTest):
    def test_list(self):
        """Test list."""
        with self._get("response/kubernetes_clusters") as mock:
            _excepted_result = mock.python_body["vke_clusters"][0]
            excepted_result = ClusterItem.from_dict(_excepted_result)

            _real_result = self.api_v2.kubernetes.list(capacity=1)
            real_result: ClusterItem = _real_result.first()

            self.assertEqual(mock.url, "https://api.vultr.com/v2/kubernetes/clusters")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create(self):
        """Test create cluster."""
        with self._post("response/kubernetes_cluster", expected_returned=ClusterItem, status_code=201) as mock:
            excepted_result = mock.python_body

            region = "ams"
            version = "test_version"
            label = "test_label"
            real_result: ClusterItem = self.api_v2.kubernetes.create(region=region, version=version, label=label)

            self.assertEqual(mock.url, "https://api.vultr.com/v2/kubernetes/clusters")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["region"], region)
            self.assertEqual(mock.req_json["version"], version)
            self.assertEqual(mock.req_json["label"], label)
            self.assertEqual(mock.status_code, 201)
            self.assertEqual(real_result, excepted_result)

    def test_get(self):
        """Test get kubernetes cluster."""
        with self._get("response/kubernetes_cluster", expected_returned=ClusterItem) as mock:
            excepted_result = mock.python_body

            vke_id = str(uuid.uuid4())
            real_result: ClusterItem = self.api_v2.kubernetes.get(vke_id=vke_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/kubernetes/clusters/{vke_id}")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_update(self):
        """Test update kubernetes cluster."""
        with self._put(status_code=204) as mock:
            vke_id = str(uuid.uuid4())
            label = "test_label"
            real_result = self.api_v2.kubernetes.update(vke_id=vke_id, label=label)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/kubernetes/clusters/{vke_id}")
            self.assertEqual(mock.method, SupportHttpMethod.PUT.value)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_delete(self):
        """Test delete kubernetes cluster."""
        with self._delete(status_code=204) as mock:
            vke_id = str(uuid.uuid4())
            real_result = self.api_v2.kubernetes.delete(vke_id=vke_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/kubernetes/clusters/{vke_id}")
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_delete_with_resources(self):
        """Test delete kubernetes cluster with all resources."""
        with self._delete(status_code=204) as mock:
            vke_id = str(uuid.uuid4())
            real_result = self.api_v2.kubernetes.delete_with_resources(vke_id=vke_id)

            _url = f"https://api.vultr.com/v2/kubernetes/clusters/{vke_id}/delete-with-linked-resources"
            self.assertEqual(mock.url, _url)
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_get_resource(self):
        """Test get resource."""
        with self._get("response/kubernetes_cluster_resource", expected_returned=ClusterResource) as mock:
            excepted_result = mock.python_body

            vke_id = str(uuid.uuid4())
            real_result: ClusterResource = self.api_v2.kubernetes.get_resource(vke_id=vke_id)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/kubernetes/clusters/{vke_id}/resources")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_list_node_pools(self):
        """Test list node pools."""
        with self._get("response/kubernetes_cluster_node_pools") as mock:
            _excepted_result = mock.python_body["node_pools"][0]
            excepted_result = ClusterNodePoolFull.from_dict(_excepted_result)

            vke_id = str(uuid.uuid4())
            _real_result = self.api_v2.kubernetes.list_node_pools(vke_id=vke_id)
            real_result: ClusterNodePoolFull = _real_result.first()

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/kubernetes/clusters/{vke_id}/node-pools")
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_create_node_pool(self):
        """Test create node pool.."""
        with self._post(
            "response/kubernetes_cluster_node_pool", expected_returned=ClusterNodePoolFull, status_code=201
        ) as mock:
            excepted_result = mock.python_body

            vke_id = str(uuid.uuid4())
            pool = ClusterNodePool(
                node_quantity=3,
                label="test_label",
                plan="test_plan",
                tag="test_tag",
            )
            real_result: ClusterNodePoolFull = self.api_v2.kubernetes.create_node_pool(vke_id, node_pool=pool)

            self.assertEqual(mock.url, f"https://api.vultr.com/v2/kubernetes/clusters/{vke_id}/node-pools")
            self.assertEqual(mock.method, SupportHttpMethod.POST.value)
            self.assertEqual(mock.req_json["node_quantity"], pool.node_quantity)
            self.assertEqual(mock.req_json["plan"], pool.plan)
            self.assertEqual(mock.req_json["label"], pool.label)
            self.assertEqual(mock.status_code, 201)
            self.assertEqual(real_result, excepted_result)

    def test_get_node_pool(self):
        """Test get node pool."""
        with self._get("response/kubernetes_cluster_node_pool", expected_returned=ClusterNodePoolFull) as mock:
            excepted_result = mock.python_body

            vke_id = str(uuid.uuid4())
            node_pool_id = str(uuid.uuid4())
            real_result: ClusterNodePoolFull = self.api_v2.kubernetes.get_node_pool(vke_id, node_pool_id)

            _url = f"https://api.vultr.com/v2/kubernetes/clusters/{vke_id}/node-pools/{node_pool_id}"
            self.assertEqual(mock.url, _url)
            self.assertEqual(mock.method, SupportHttpMethod.GET.value)
            self.assertEqual(real_result, excepted_result)

    def test_update_node_pool(self):
        """Test update node pool.."""
        with self._patch(
            "response/kubernetes_cluster_node_pool", expected_returned=ClusterNodePoolFull, status_code=202
        ) as mock:
            excepted_result = mock.python_body

            vke_id = str(uuid.uuid4())
            node_pool_id = str(uuid.uuid4())
            node_quantity = 3
            real_result: ClusterNodePoolFull = self.api_v2.kubernetes.update_node_pool(
                vke_id=vke_id,
                node_pool_id=node_pool_id,
                node_quantity=node_quantity,
            )

            _url = f"https://api.vultr.com/v2/kubernetes/clusters/{vke_id}/node-pools/{node_pool_id}"
            self.assertEqual(mock.url, _url)
            self.assertEqual(mock.method, SupportHttpMethod.PATCH.value)
            self.assertEqual(mock.req_json["node_quantity"], node_quantity)
            self.assertEqual(mock.status_code, 202)
            self.assertEqual(real_result, excepted_result)

    def test_delete_node_pool(self):
        """Test delete_node_pool."""
        with self._delete(status_code=204) as mock:
            vke_id = str(uuid.uuid4())
            node_pool_id = str(uuid.uuid4())
            real_result = self.api_v2.kubernetes.delete_node_pool(vke_id, node_pool_id)

            _url = f"https://api.vultr.com/v2/kubernetes/clusters/{vke_id}/node-pools/{node_pool_id}"
            self.assertEqual(mock.url, _url)
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_delete_node_pool_instance(self):
        """Test delete node pool instance."""
        with self._delete(status_code=204) as mock:
            vke_id = str(uuid.uuid4())
            node_pool_id = str(uuid.uuid4())
            node_id = str(uuid.uuid4())
            real_result = self.api_v2.kubernetes.delete_node_pool_instance(vke_id, node_pool_id, node_id)

            _url = f"https://api.vultr.com/v2/kubernetes/clusters/{vke_id}/node-pools/{node_pool_id}/nodes/{node_id}"
            self.assertEqual(mock.url, _url)
            self.assertEqual(mock.method, SupportHttpMethod.DELETE.value)
            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_recycle_node_pool_instance(self):
        """Test recycle_node_pool_instance."""
        with self._post(status_code=204) as mock:
            vke_id = str(uuid.uuid4())
            node_pool_id = str(uuid.uuid4())
            node_id = str(uuid.uuid4())
            real_result = self.api_v2.kubernetes.recycle_node_pool_instance(vke_id, node_pool_id, node_id)

            self.assertEqual(mock.status_code, 204)
            self.assertIsNone(real_result)

    def test_get_config(self):
        """Test get cluster config."""
        with self._get("response/kubernetes_cluster_config") as m:
            vke_id = str(uuid.uuid4())
            real_result: str = self.api_v2.kubernetes.get_config(vke_id=vke_id)

            self.assertEqual(real_result, get_only_value(m.body))

    def test_get_versions(self):
        """Test get versions."""
        real_result: List[str] = self.api_v2.kubernetes.get_versions()

        self.assertIn("v1.21.7+1", real_result)
        self.assertNotIn("test_version", real_result)
