from dataclasses import dataclass
from functools import partial
from typing import Optional
from urllib.parse import urljoin

import dacite

from pyvultr.utils import BaseDataclass, VultrPagination, get_only_value
from pyvultr.v2.base import BaseVultrV2


@dataclass
class ObjectStorageItem(BaseDataclass):
    id: str
    date_created: str
    cluster_id: int
    region: str
    label: str
    status: str
    s3_hostname: str
    s3_access_key: str
    s3_secret_key: str


@dataclass
class ObjectStorageS3Credential(BaseDataclass):
    s3_hostname: str
    s3_access_key: str
    s3_secret_key: str


@dataclass
class ObjectStorageClusterItem(BaseDataclass):
    id: str
    region: str
    hostname: str
    deploy: str


class ObjectStorage(BaseVultrV2):
    """Vultr ObjectStorage API.

    Object Storage is S3 API compatible. Objects uploaded to object storage can be accessed privately or
    publicly on the web. Object storage supports a virtually unlimited number of objects.
    Control your Object Storage via the API or browse in the Customer Portal.

    Attributes:
        api_key: Vultr API key, we get it from env variable `VULTR_API_TOKEN` if not provided.
    """

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(api_key)

    @property
    def base_url(self):
        """Get base url for all API in this section."""
        return urljoin(super().base_url, "object-storage")

    def list(
        self,
        per_page: int = None,
        cursor: str = None,
        capacity: int = None,
    ) -> VultrPagination[ObjectStorageItem]:
        """Get a list of all Object Storage in your account.

        Args:
            per_page: Number of items requested per page. Default is 100 and Max is 500.
            cursor: Cursor for paging.
            capacity: the capacity of the VultrPagination[ObjectStorageItem],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[ObjectStorageItem]: a paginated list of `ObjectStorageItem`.
        """
        return VultrPagination[ObjectStorageItem](
            fetcher=self._get,
            cursor=cursor,
            page_size=per_page,
            return_type=ObjectStorageItem,
            capacity=capacity,
        )

    def create(self, cluster_id: str, label: str = None) -> ObjectStorageItem:
        """Create new Object Storage. The `cluster_id` attribute is required.

        Args:
            cluster_id: The Cluster id where the Object Storage will be created.
            label: The user-supplied label for this Object Storage.

        Returns:
            ObjectStorageItem: A `ObjectStorageItem` object.
        """
        _json = {
            "cluster_id": cluster_id,
            "label": label,
        }
        resp = self._post(json=_json)
        return dacite.from_dict(data_class=ObjectStorageItem, data=get_only_value(resp))

    def get(self, object_storage_id: str) -> ObjectStorageItem:
        """Get information about an Object Storage.

        Args:
            object_storage_id: A Object Storage id.

        Returns:
            ObjectStorageItem: A `ObjectStorageItem` object.
        """
        resp = self._get(f"/{object_storage_id}")
        return dacite.from_dict(data_class=ObjectStorageItem, data=get_only_value(resp))

    def delete(self, object_storage_id: str):
        """Delete an Object Storage.

        Args:
            object_storage_id: The Object Storage id.

        Returns:
            STATUS CODE: 204
            /NO CONTENT/
        """
        return self._delete(f"/{object_storage_id}")

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

    def regenerate_keys(self, object_storage_id: str) -> ObjectStorageS3Credential:
        """Regenerate the keys for an Object Storage.

        Args:
            object_storage_id: The Object Storage id.

        Returns:
            ObjectStorageS3Credential: A `ObjectStorageS3Credential` object.
        """
        resp = self._post(f"/{object_storage_id}/regenerate-keys")
        return dacite.from_dict(data_class=ObjectStorageS3Credential, data=get_only_value(resp))

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
            capacity: the capacity of the VultrPagination[ObjectStorageClusterItem],
            see `pyvultr.utils.VultrPagination` for detail.

        Returns:
            VultrPagination[ObjectStorageClusterItem]: a paginated list of `ObjectStorageClusterItem`.
        """
        fetcher = partial(self._get, endpoint="/clusters")
        return VultrPagination[ObjectStorageClusterItem](
            fetcher=fetcher,
            cursor=cursor,
            page_size=per_page,
            return_type=ObjectStorageClusterItem,
            capacity=capacity,
        )
