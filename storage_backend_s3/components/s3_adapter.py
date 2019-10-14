# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo.addons.component.core import Component

logger = logging.getLogger(__name__)

try:
    import boto3
except ImportError as err:  # pragma: no cover
    logger.debug(err)


class S3StorageBackend(Component):
    _name = "s3.adapter"
    _inherit = "base.storage.adapter"
    _usage = "amazon_s3"

    def _get_aws_session_params(self):
        params = {
            'aws_access_key_id': self.collection.aws_access_key_id,
            'aws_secret_access_key': self.collection.aws_secret_access_key,
            'region_name': self.collection.aws_region,
        }
        if self.collection.aws_host:
            params['endpoint_url'] = self.collection.aws_host
        return params

    def _get_resource(self):
        return boto3.Session(**self._get_aws_session_params()).resource("s3")

    def _get_object(self, relative_path):
        s3 = self._get_resource()
        path = self._fullpath(relative_path)
        return s3.Object(self.collection.aws_bucket, path)

    def add(self, relative_path, data, mimetype=None, **kwargs):
        s3object = self._get_object(relative_path)
        s3object.put(
            Body=data,
            ContentType=mimetype,
            CacheControl=self.collection.aws_cache_control or "",
        )

    def get(self, relative_path):
        s3object = self._get_object(relative_path)
        return s3object.get()["Body"].read()

    def list(self, relative_path):
        resource = self._get_resource()
        bucket = resource.Bucket(self.collection.aws_bucket)
        dir_path = self.collection.directory_path or ""
        return [
            o.key.replace(dir_path, "").lstrip("/")
            for o in bucket.objects.filter(Prefix=dir_path)
        ]

    def delete(self, relative_path):
        s3object = self._get_object(relative_path)
        s3object.delete()
