# -*- coding: utf-8 -*-
"""
Sample test template.
At minimum, test: normal path + batch path + permission path.
"""

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase


class TestSampleModel(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.SampleModel = cls.env["module.sample"]
        cls.record = cls.SampleModel.create({
            "name": "Test Record",
        })

    def test_confirm_from_draft(self):
        """Normal path: draft → confirmed"""
        self.assertEqual(self.record.state, "draft")
        self.record.action_confirm()
        self.assertEqual(self.record.state, "confirmed")

    def test_confirm_batch(self):
        """Batch path: confirm multiple records at once"""
        records = self.SampleModel.create([
            {"name": "Batch 1"},
            {"name": "Batch 2"},
            {"name": "Batch 3"},
        ])
        records.action_confirm()
        for rec in records:
            self.assertEqual(rec.state, "confirmed")

    def test_confirm_non_draft_raises(self):
        """Error path: cannot confirm non-draft record"""
        self.record.action_confirm()  # → confirmed
        with self.assertRaises(UserError):
            self.record.action_confirm()  # → should fail

    # TODO: Add permission test with a non-admin user
    # TODO: Add multi-company test if applicable
