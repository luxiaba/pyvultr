from dataclasses import asdict, dataclass
from functools import partial
from typing import List, Optional
from urllib.parse import urljoin

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value

from .base import BaseVultrV2, command


@dataclass
class ReqClusterNodePool(BaseDataclass):
    # Number of instances to deploy in this node-pool.
    # Minimum of 1 node required, but at least 3 is recommended.
    node_quantity: int
    # Label for this node-pool. You cannot change the label after a node-pool is created.
    # You cannot have duplicate node pool labels in the same cluster.
    label: str
    plan: str  # Plan you want this node-pool to use. Note: minimum plan must be $10.
    tag: str = None  # Tag for node pool


@dataclass
class ClusterNode(BaseDataclass):
    id: str  # ID of the node-pool instance.
    label: str  # Label of the node-pool instance.
    date_created: str  # Date of creation.
    status: str  # Node status.


@dataclass
class ClusterNodePoolFull(BaseDataclass):
    id: str  # The NodePool ID, check `ClusterNodePool` for details.
    date_created: str  # Date of creation.
    date_updated: str  # Date of last update.
    label: str  # Label for node pool.
    tag: str  # Tag for node pool
    plan: str  # Plan used for node-pool.
    status: str  # Status for node-pool. enums?
    node_quantity: int  # Number of nodes in node-pool.
    nodes: List[ClusterNode]  # List of nodes in node-pool.


@dataclass
class Cluster(BaseDataclass):
    id: str  # ID for the VKE cluster.
    label: str  # Label for your cluster.
    date_created: str  # Date of creation.
    cluster_subnet: str  # IP range that your pods will run on in this cluster.
    service_subnet: str  # IP range that services will run on this cluster.
    ip: str  # IP for your Kubernetes Clusters Control Plane.
    endpoint: str  # Domain for your Kubernetes Clusters Control Plane.
    version: str  # Version of Kubernetes this cluster is running on.
    region: str  # Region this Kubernetes Cluster is running in.
    status: str  # Status for VKE cluster.
    node_pools: List[ClusterNodePoolFull]  # List of node pools in this cluster.


@dataclass
class ClusterResourceItem(BaseDataclass):
    id: str  # Unique identifier for the block storage volume.
    label: str  # Label given to the block storage volume.
    date_created: str  # Date the block storage volume was created.
    status: str  # Status of the block storage volume.


@dataclass
class ClusterResource(BaseDataclass):
    block_storage: List[ClusterResourceItem]
    load_balancer: List[ClusterResourceItem]


class KubernetesAPI(BaseVultrV2):
    """Vultr Kubernetes API.

    Reference: https://www.vultr.com/api/#tag/kubernetes

    Vultr Kubernetes Engine is a managed Kubernetes offering.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "kubernetes")

    @command
    def list(self, per_page: int = None, cursor: str = None, capacity: int = None) -> VultrPagination[Cluster]:
        """List all Kubernetes clusters currently deployed.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[ClusterItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[Cluster]: A list-like object of `ClusterItem` object.
        """
        fetcher = partial(self._get, endpoint="/clusters")
        return VultrPagination[Cluster](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=Cluster,
            capacity=capacity,
        )

    @command
    def create(self, region: str, version: str, label: str = None, pools: List[ReqClusterNodePool] = None) -> Cluster:
        """Create Kubernetes Cluster.

        Args:
            region: Region you want to deploy VKE in. EWR or LAX.
            version: Version of Kubernetes you want to deploy.
            label: The label for your Kubernetes cluster.
            pools: List[ClusterNodePool]

        Returns:
            Cluster: A `ClusterItem` object.
        """
        _json = {
            "region": region,
            "version": version,
            "label": label,
            "node_pools": pools and [asdict(i) for i in pools],
        }
        resp = self._post("/clusters", json=_json)
        return Cluster.from_dict(get_only_value(resp))

    @command
    def get(self, vke_id: str) -> Cluster:
        """Get Kubernetes Cluster.

        Args:
            vke_id: The Cluster ID.

        Returns:
            Cluster: A `ClusterItem` object.
        """
        resp = self._get(f"/clusters/{vke_id}")
        return Cluster.from_dict(get_only_value(resp))

    @command
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

    @command
    def delete(self, vke_id: str):
        """Delete Kubernetes Cluster.

        Args:
            vke_id: The Cluster ID.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/clusters/{vke_id}")

    @command
    def delete_with_resources(self, vke_id: str):
        """Delete Kubernetes Cluster and all related resources.

        Args:
            vke_id: The Cluster ID.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/clusters/{vke_id}/delete-with-linked-resources")

    @command
    def get_resource(self, vke_id: str) -> ClusterResource:
        """Get the block storage volumes and load balancers deployed by the specified Kubernetes cluster.

        Args:
            vke_id: The Cluster ID.

        Returns:
            ClusterResource: A `ClusterResource` object.
        """
        resp = self._get(f"/clusters/{vke_id}/resources")
        return ClusterResource.from_dict(get_only_value(resp))

    @command
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
            capacity: The capacity of the VultrPagination[ClusterNodePoolFull], see `VultrPagination` for details.

        Returns:
            VultrPagination[ClusterNodePoolFull]: A list-like object of `ClusterItem` object.
        """
        fetcher = partial(self._get, endpoint=f"/clusters/{vke_id}/node-pools")
        return VultrPagination[ClusterNodePoolFull](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=ClusterNodePoolFull,
            capacity=capacity,
        )

    @command
    def create_node_pool(self, vke_id: str, node_pool: ReqClusterNodePool) -> ClusterNodePoolFull:
        """Create NodePool for a Existing Kubernetes Cluster.

        Args:
            vke_id: The Cluster ID.
            node_pool: A `ClusterNodePool` object.

        Returns:
            ClusterNodePoolFull: A `ClusterNodePoolFull` object.
        """
        resp = self._post(f"/clusters/{vke_id}/node-pools", json=asdict(node_pool))
        return ClusterNodePoolFull.from_dict(get_only_value(resp))

    @command
    def get_node_pool(self, vke_id: str, node_pool_id: str) -> ClusterNodePoolFull:
        """Get NodePool from a Kubernetes Cluster.

        Args:
            vke_id: The Cluster ID.
            node_pool_id: The NodePool ID.

        Returns:
            ClusterNodePoolFull: A `ClusterNodePoolFull` object.
        """
        resp = self._get(f"/clusters/{vke_id}/node-pools/{node_pool_id}")
        return ClusterNodePoolFull.from_dict(get_only_value(resp))

    @command
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
        return ClusterNodePoolFull.from_dict(get_only_value(resp))

    @command
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

    @command
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

    @command
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

    @command
    def get_config(self, vke_id: str) -> str:
        """Get Kubernetes Cluster KubeConfig.

        Args:
            vke_id: The cluster id.

        Returns:
            str: Base64 encoded KubeConfig.
        """
        resp = self._get(f"/clusters/{vke_id}/config")
        return get_only_value(resp)

    @command
    def get_versions(self) -> List[str]:
        """Get a list of supported Kubernetes versions.

        Returns:
            List[str]: A list str of supported Kubernetes versions.
        """
        resp = self._get("/versions")
        return get_only_value(resp)
