# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase, at_install, post_install
from odoo.tools.safe_eval import safe_eval


@at_install(False)
@post_install(True)
class TestModule(TransactionCase):
    def setUp(self):
        super().setUp()
        self.ResGroups = self.env["res.groups"]
        self.ResCompany = self.env["res.company"]
        self.IrModelData = self.env["ir.model.data"]
        self.synchronization_group = self.env.ref(
            "database_synchronization.synchronisation_res_groups"
        )
        self.synchronization_company = self.env.ref(
            "database_synchronization.synchronisation_res_company"
        )

    def _prepare_synchronization_data(self, synchronization_data):
        # We emulate a request on Master instance
        external_datas = (
            self.env[synchronization_data.model]
            .with_context(
                active_test=(synchronization_data.synchronization_type == "active")
            )
            .search_read(safe_eval(synchronization_data.domain))
        )

        external_xml_id_datas = self.IrModelData.search_read(
            [("model", "=", synchronization_data.model_id.model)],
            ["complete_name", "res_id"],
            order="complete_name",
        )

        return (external_xml_id_datas, external_datas)

    # Test Section
    def test_fields_view_get(self):
        arch_form_view = self.ResGroups.fields_view_get(view_type="form")["arch"]
        self.assertIn("Readonly Table", arch_form_view)

        arch_tree_view = self.ResGroups.fields_view_get(view_type="tree")["arch"]
        self.assertNotIn("Readonly Table", arch_tree_view)

    def test_synchronize_id(self):
        (external_xml_id_datas, external_datas) = self._prepare_synchronization_data(
            self.synchronization_group
        )

        # Make a correct synchronization (id only)
        self.synchronization_group._synchronize_execute(
            external_xml_id_datas,
            external_datas,
        )

        # check if mapping has been created
        groups_qty = len(self.ResGroups.search([]))
        self.assertEqual(groups_qty, self.synchronization_group.mapping_qty)

        # simulate that external datas are incorrect
        incorrect_external_datas = external_datas.copy()
        incorrect_external_datas.append({"id": -1, "name": "Unexisting Group locally"})

        with self.assertRaises(UserError):
            self.synchronization_group._synchronize_execute(
                external_xml_id_datas,
                incorrect_external_datas,
            )

    def test_synchronize_data(self):
        (external_xml_id_datas, external_datas) = self._prepare_synchronization_data(
            self.synchronization_company
        )

        # Make a correct synchronization (data)
        self.synchronization_company._synchronize_execute(
            external_xml_id_datas,
            external_datas,
        )

        company_qty = len(self.ResCompany.search([]))
        self.assertEqual(company_qty, self.synchronization_company.mapping_qty)

        # Simulate the creation of another company in distant
        company_value = "My New Company on Distant Server"
        street_value = "FIELD NOT SYNCHRONIZED"
        external_datas_with_new_company = external_datas.copy()
        external_datas_with_new_company.append(
            {
                "id": 999,
                "name": company_value,
                "street": street_value,
            }
        )

        # Make a new synchronization
        self.synchronization_company._synchronize_execute(
            external_xml_id_datas,
            external_datas_with_new_company,
        )

        # Check if the company has been created
        new_companies = self.ResCompany.search([("name", "=", company_value)])
        self.assertEqual(len(new_companies), 1)

        # Check that non synchronized fields has not been integrated
        # in the local database
        new_company = new_companies[0]
        self.assertNotEqual(new_company.street, street_value)

        # Synchronize with more recent data
        new_company_value = "New Company Name"
        external_datas_with_new_company = external_datas.copy()
        external_datas_with_new_company.append(
            {
                "id": 999,
                "name": new_company_value,
                "write_date": "2100-01-01 00:00:00",
            }
        )
        self.synchronization_company._synchronize_execute(
            external_xml_id_datas,
            external_datas_with_new_company,
        )

        new_company = self.ResCompany.browse(new_company.id)

        self.assertEqual(new_company.name, new_company_value)

        # Synchronize with obsolete data
        obsolete_company_value = "Obsolete Company Name"
        external_datas_with_new_company = external_datas.copy()
        external_datas_with_new_company.append(
            {
                "id": 999,
                "name": obsolete_company_value,
                "write_date": "1990-01-01 00:00:00",
            }
        )
        self.synchronization_company._synchronize_execute(
            external_xml_id_datas,
            external_datas_with_new_company,
        )

        new_company = self.ResCompany.browse(new_company.id)

        self.assertNotEqual(new_company.name, obsolete_company_value)
