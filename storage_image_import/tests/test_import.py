# Copyright 2020 Akretion (https://www.akretion.com).
# Copyright 2021 Camptocamp (http://www.camptocamp.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# @author Iván Todorovich <ivan.todorovich@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import os
import urllib
from contextlib import contextmanager
from unittest.mock import patch

from odoo.addons.storage_image.tests.common import StorageImageCommonCase

from .models.fake_image_relation import FakeImageRelation


class ImportImageCase(StorageImageCommonCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Load fake image relation model
        cls.env["base"].flush()  # flush to recompute everything before
        FakeImageRelation._build_model(cls.env.registry, cls.env.cr)
        cls.env.registry.setup_models(cls.env.cr)
        cls.env.registry.init_models(
            cls.env.cr,
            [FakeImageRelation._name],
            dict(cls.env.context, update_custom_fields=True),
        )
        # Create some permissions for our fake model
        model = cls.env["ir.model"].search([("model", "=", "fake.image.relation")])
        cls.env["ir.model.access"].sudo().create(
            {
                "name": "access.tester",
                "model_id": model.id,
                "perm_read": 1,
                "perm_write": 1,
                "perm_create": 1,
                "perm_unlink": 1,
            }
        )
        # Load test image
        cls.base_path = os.path.dirname(os.path.abspath(__file__))
        cls.oca_image = cls._create_storage_image_from_file("static/oca-logo.png")
        cls.logo_image = cls._create_storage_image_from_file("static/akretion-logo.png")
        # Some other data
        cls.product_tmpl = cls.env.ref("product.product_product_4_product_template")

    @classmethod
    def tearDownClass(cls):
        # tear down fake image relation model
        del cls.env.registry.models[FakeImageRelation._name]
        cls.env.registry.setup_models(cls.env.cr)
        return super().tearDownClass()

    @contextmanager
    def _patched_request(self, filename, base_path=None):
        path = base_path or self.base_path
        with open(os.path.join(path, filename), "rb") as file:
            with patch.object(urllib.request, "urlopen", return_value=file):
                yield

    def test_import_from_url(self):
        # Case 1: Create image from url
        vals = {"import_from_url": "https://www.example.com/oca-logo.png"}
        with self._patched_request("static/oca-logo.png"):
            relation = self.env["fake.image.relation"].create(vals)
        self.assertEqual(relation.image_id.name, self.oca_image.name)
        self.assertEqual(relation.image_id.data, self.oca_image.data)
        # Case 2: Write image from url
        vals = {"import_from_url": "https://www.example.com/akretion-logo.png"}
        with self._patched_request("static/akretion-logo.png"):
            relation.write(vals)
        self.assertEqual(relation.image_id.name, self.logo_image.name)
        self.assertEqual(relation.image_id.data, self.logo_image.data)
