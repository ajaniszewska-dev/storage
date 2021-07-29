# Copyright 2017 Akretion (http://www.akretion.com).
# @author Sébastien BEAU <sebastien.beau@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Storage Image",
    "summary": "Store image and resized image in a storage backend",
    "version": "14.0.1.0.1",
    "category": "Storage",
    "website": "https://github.com/OCA/storage",
    "author": " Akretion, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "development_status": "Production/Stable",
    "depends": ["storage_thumbnail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/assets.xml",
        "views/storage_image.xml",
        "views/storage_image_relation_abstract.xml",
        "data/ir_config_parameter.xml",
    ],
    "qweb": ["static/src/xml/custom_xml.xml"],
}
