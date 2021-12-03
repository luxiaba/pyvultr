from dataclasses import dataclass
from functools import partial
from typing import Optional
from urllib.parse import urljoin

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value

from .base import BaseVultrV2, command


@dataclass
class ObjectStorage(BaseDataclass):
    id: str  # A unique ID for the Object Storage.
    date_created: str  # Date the Object Store was created.
    cluster_id: int  # The Cluster id.
    # The Region id where the instance is located, check `RegionAPI.list` and `RegionItem.id` for available regions.
    region: str
    label: str  # The user-supplied label for this Object Storage.
    status: str  # The status of this Object Storage, see `enums.ObjectStorageStatus` for possible values.
    s3_hostname: str  # The Cluster hostname for this Object Storage.
    s3_access_key: str  # The Object Storage access key.
    s3_secret_key: str  # The Object Storage secret key.


@dataclass
class ObjectStorageS3Credential(BaseDataclass):
    s3_hostname: str  # The Cluster hostname for this Object Storage.
    s3_access_key: str  # The new Object Storage access key.
    s3_secret_key: str  # The new Object Storage secret key.


@dataclass
class ObjectStorageClusterItem(BaseDataclass):
    id: str  # A unique ID for the Object Storage cluster.
    # The Region id where the instance is located, check `RegionAPI.list` and `RegionItem.id` for available regions.
    region: str
    hostname: str  # The cluster host name.
    deploy: str  # The Cluster is eligible for Object Storage deployment, see `enums.ObjectStorageClusterDeployStatus`.


class ObjectStorageAPI(BaseVultrV2):
    """Vultr ObjectStorage API.

    Reference: https://www.vultr.com/api/#tag/s3

    Object Storage is S3 API compatible. Objects uploaded to object storage can be accessed privately or
    publicly on the web. Object storage supports a virtually unlimited number of objects.
    Control your Object Storage via the API or browse in the Customer Portal.

    Attributes:
        api_key: Vultr API key, we get it from env variable `$VULTR_API_KEY` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "object-storage")

    @command
    def list(
        self,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[ObjectStorage]:
        """Get a list of all Object Storage in your account.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[ObjectStorageItem], see `VultrPagination` for details.

        Returns:
            VultrPagination[ObjectStorage]: A list-like object of `ObjectStorageItem` object.
        """
        return VultrPagination[ObjectStorage](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=ObjectStorage,
            capacity=capacity,
        )

    @command
    def create(self, cluster_id: str, label: str = None) -> ObjectStorage:
        """Create new Object Storage. The `cluster_id` attribute is required.

        Args:
            cluster_id: The Cluster id where the Object Storage will be created.
            label: The user-supplied label for this Object Storage.

        Returns:
            ObjectStorage: A `ObjectStorageItem` object.
        """
        _json = {
            "cluster_id": cluster_id,
            "label": label,
        }
        resp = self._post(json=_json)
        return ObjectStorage.from_dict(get_only_value(resp))

    @command
    def get(self, object_storage_id: str) -> ObjectStorage:
        """Get information about an Object Storage.

        Args:
            object_storage_id: A Object Storage id.

        Returns:
            ObjectStorage: A `ObjectStorageItem` object.
        """
        resp = self._get(f"/{object_storage_id}")
        return ObjectStorage.from_dict(get_only_value(resp))

    @command
    def delete(self, object_storage_id: str):
        """Delete an Object Storage.

        Args:
            object_storage_id: The Object Storage id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{object_storage_id}")

    @command
    def update(self, object_storage_id: str, label: str):
        """Update the label for an Object Storage.

        Args:
            object_storage_id: The Object Storage id.
            label: The user-supplied label for the Object Storage.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        _json = {
            "label": label,
        }
        return self._patch(f"/{object_storage_id}", json=_json)

    @command
    def regenerate_keys(self, object_storage_id: str) -> ObjectStorageS3Credential:
        """Regenerate the keys for an Object Storage.

        Args:
            object_storage_id: The Object Storage id.

        Returns:
            ObjectStorageS3Credential: A `ObjectStorageS3Credential` object.
        """
        resp = self._post(f"/{object_storage_id}/regenerate-keys")
        return ObjectStorageS3Credential.from_dict(get_only_value(resp))

    @command
    def list_clusters(
        self,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[ObjectStorageClusterItem]:
        """Get a list of all Object Storage Clusters.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: The capacity of the VultrPagination[ObjectStorageClusterItem],
            see `VultrPagination` for details.

        Returns:
            VultrPagination[ObjectStorageClusterItem]: A list-like object of `ObjectStorageClusterItem` object.
        """
        fetcher = partial(self._get, endpoint="/clusters")
        return VultrPagination[ObjectStorageClusterItem](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=ObjectStorageClusterItem,
            capacity=capacity,
        )
