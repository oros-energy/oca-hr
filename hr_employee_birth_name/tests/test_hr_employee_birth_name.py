# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import AccessError
from odoo.tests import new_test_user
from odoo.tests.common import TransactionCase


class TestHrEmployeeBirthName(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.employee = cls.env["hr.employee"].create(
            {"name": "Jane Doe", "birth_name": "Jane Smith"}
        )

    def test_create_and_read(self):
        self.employee.invalidate_recordset(["birth_name"])
        self.assertEqual(self.employee.birth_name, "Jane Smith")
        self.assertEqual(
            self.employee.read(["birth_name"])[0]["birth_name"], "Jane Smith"
        )

    def test_write_and_search(self):
        self.employee.write({"birth_name": "Jane Miller"})
        self.employee.invalidate_recordset(["birth_name"])
        self.assertEqual(self.employee.birth_name, "Jane Miller")
        self.assertEqual(
            self.env["hr.employee"].search([("birth_name", "=", "Jane Miller")]),
            self.employee,
        )

    def test_hr_officer_can_write_and_read(self):
        officer = new_test_user(
            self.env, login="birth_name_officer", groups="hr.group_hr_user"
        )
        employee = self.employee.with_user(officer)
        employee.write({"birth_name": "Jane Brown"})
        employee.invalidate_recordset(["birth_name"])
        self.assertEqual(employee.birth_name, "Jane Brown")

    def test_internal_user_cannot_read(self):
        user = new_test_user(
            self.env, login="birth_name_internal", groups="base.group_user"
        )
        with self.assertRaises(AccessError):
            self.employee.with_user(user).read(["birth_name"])
