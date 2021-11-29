from dataclasses import asdict, dataclass
from functools import partial
from typing import List, Optional
from urllib.parse import urljoin

import dacite

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value
from pyvultr.v2.base import BaseVultrV2


@dataclass
class ClusterNodePool(BaseDataclass):
    node_quantity: int
    label: str
    plan: str
    tag: str = None


@dataclass
class ClusterResourceItem(BaseDataclass):
    id: str
    label: str
    date_created: str
    status: str


@dataclass
class ClusterResource(BaseDataclass):
    block_storage: List[ClusterResourceItem]
    load_balancer: List[ClusterResourceItem]


@dataclass
class ClusterNode(BaseDataclass):
    id: str
    label: str
    date_created: str


@dataclass
class ClusterNodePoolFull(BaseDataclass):
    id: str
    date_created: str
    date_updated: str
    label: str
    tag: str
    plan: str
    status: str
    node_quantity: int
    nodes: List[ClusterNode]


@dataclass
class ClusterItem(BaseDataclass):
    id: str
    label: str
    date_created: str
    cluster_subnet: str
    service_subnet: str
    ip: str
    endpoint: str
    version: str
    region: str
    status: str
    node_pools: List[ClusterNodePoolFull]


class Kubernetes(BaseVultrV2):
    """Vultr Kubernetes API.

    Vultr Kubernetes Engine is a managed Kubernetes offering.

    Attributes:
        api_key: Vultr API key, we get it from env variable `VULTR_API_TOKEN` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "kubernetes")

    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[ClusterItem]:
        """List all Kubernetes clusters currently deployed.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: the capacity of the VultrPagination[ClusterItem],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[ClusterItem]: a paginated list of `ClusterItem`.
        """
        fetcher = partial(self._get, endpoint="/clusters")
        return VultrPagination[ClusterItem](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=ClusterItem,
            capacity=capacity,
        )

    def create(self, region: str, version: str, label: str = None, pools: List[ClusterNodePool] = None) -> ClusterItem:
        """Create Kubernetes Cluster.

        Args:
            region: Region you want to deploy VKE in. EWR or LAX.
            version: Version of Kubernetes you want to deploy.
            label: The label for your Kubernetes cluster.
            pools: List[ClusterNodePool]

        Returns:
            ClusterItem: A `ClusterItem` object.
        """
        _json = {
            "region": region,
            "version": version,
            "label": label,
            "node_pools": pools and [asdict(i) for i in pools],
        }
        resp = self._post("/clusters", json=_json)
        return dacite.from_dict(data_class=ClusterItem, data=get_only_value(resp))

    def get(self, vke_id: str) -> ClusterItem:
        """Get Kubernetes Cluster.

        Args:
            vke_id: The Cluster ID.

        Returns:
            ClusterItem: A `ClusterItem` object.
        """
        resp = self._get(f"/clusters/{vke_id}")
        return dacite.from_dict(data_class=ClusterItem, data=get_only_value(resp))

    def update(self, vke_id: str, label: str):
        """Update Kubernetes Cluster.

        Args:
            vke_id: The Cluster ID.
            label: Label for the Kubernetes cluster

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "label": label,
        }
        return self._put(f"/clusters/{vke_id}", json=_json)

    def delete(self, vke_id: str):
        """Delete Kubernetes Cluster.

        Args:
            vke_id: The Cluster ID.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/clusters/{vke_id}")

    def delete_with_resources(self, vke_id: str):
        """Delete Kubernetes Cluster and all related resources.

        Args:
            vke_id: The Cluster ID.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/clusters/{vke_id}/delete-with-linked-resources")

    def get_resource(self, vke_id: str) -> ClusterResource:
        """Get the block storage volumes and load balancers deployed by the specified Kubernetes cluster.

        Args:
            vke_id: The Cluster ID.

        Returns:
            ClusterResource: A `ClusterResource` object.
        """
        resp = self._get(f"/clusters/{vke_id}/resources")
        return dacite.from_dict(data_class=ClusterResource, data=get_only_value(resp))

    def list_node_pools(
        self,
        vke_id: str,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[ClusterNodePoolFull]:
        """List all available NodePools on a Kubernetes Cluster.

        Args:
            vke_id: The Cluster ID.
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: the capacity of the VultrPagination[ClusterNodePoolFull],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[ClusterNodePoolFull]: a paginated list of `ClusterItem`.
        """
        fetcher = partial(self._get, endpoint=f"/clusters/{vke_id}/node-pools")
        return VultrPagination[ClusterNodePoolFull](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=ClusterNodePoolFull,
            capacity=capacity,
        )

    def create_node_pool(self, vke_id: str, node_pool: ClusterNodePool) -> ClusterNodePoolFull:
        """Create NodePool for a Existing Kubernetes Cluster.

        Args:
            vke_id: The Cluster ID.
            node_pool: A `ClusterNodePool` object.

        Returns:
            ClusterNodePoolFull: A `ClusterNodePoolFull` object.
        """
        resp = self._post(f"/clusters/{vke_id}/node-pools", json=asdict(node_pool))
        return dacite.from_dict(data_class=ClusterNodePoolFull, data=get_only_value(resp))

    def get_node_pool(self, vke_id: str, node_pool_id: str) -> ClusterNodePoolFull:
        """Get NodePool from a Kubernetes Cluster.

        Args:
            vke_id: The Cluster ID.
            node_pool_id: The NodePool ID.

        Returns:
            ClusterNodePoolFull: A `ClusterNodePoolFull` object.
        """
        resp = self._get(f"/clusters/{vke_id}/node-pools/{node_pool_id}")
        return dacite.from_dict(data_class=ClusterNodePoolFull, data=get_only_value(resp))

    def update_node_pool(
        self,
        vke_id: str,
        node_pool_id: str,
        node_quantity: int = None,
        tag: str = None,
    ) -> ClusterNodePoolFull:
        """Update a NodePool on a Kubernetes Cluster.

        Args:
            vke_id: The Cluster ID.
            node_pool_id: The NodePool ID.
            node_quantity: Number of instances in the NodePool. Minimum of 1 is required, but at least 3 is recommended.
            tag: Tag for your node pool.

        Returns:
            ClusterNodePoolFull: A `ClusterNodePoolFull` object.
        """
        _json = {
            "node_quantity": node_quantity,
            "tag": tag,
        }
        resp = self._patch(f"/clusters/{vke_id}/node-pools/{node_pool_id}", json=_json)
        return dacite.from_dict(data_class=ClusterNodePoolFull, data=get_only_value(resp))

    def delete_node_pool(self, vke_id: str, node_pool_id: str):
        """Delete a NodePool from a Kubernetes Cluster.

        Args:
            vke_id: The Cluster ID.
            node_pool_id: The NodePool ID.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/clusters/{vke_id}/node-pools/{node_pool_id}")

    def delete_node_pool_instance(self, vke_id: str, node_pool_id: str, node_id: str):
        """Delete a single NodePool instance from a given NodePool.

        Args:
            vke_id: The Cluster ID.
            node_pool_id: The NodePool ID.
            node_id: The Instance ID.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/clusters/{vke_id}/node-pools/{node_pool_id}/nodes/{node_id}")

    def recycle_node_pool_instance(self, vke_id: str, node_pool_id: str, node_id: str):
        """Recycle a specific NodePool Instance.

        Args:
            vke_id: The cluster id
            node_pool_id: The NodePool ID.
            node_id: Node ID

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._post(f"/clusters/{vke_id}/node-pools/{node_pool_id}/nodes/{node_id}/recycle")

    def get_config(self, vke_id: str) -> str:
        """Get Kubernetes Cluster KubeConfig.

        Args:
            vke_id: The cluster id.

        Returns:
            str: Base64 encoded KubeConfig.
        """
        resp = self._get(f"/clusters/{vke_id}/config")
        return get_only_value(resp)

    def get_versions(self) -> List[str]:
        """Get a list of supported Kubernetes versions.

        Returns:
            List[str]: A list str of supported Kubernetes versions.
        """
        resp = self._get("/versions")
        return get_only_value(resp)
