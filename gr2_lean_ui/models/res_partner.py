from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    # NOTE: Uncomment this after upgrading module to create the database column
    # birthdate = fields.Date(
    #     string="Ngày sinh",
    #     help="Ngày tháng năm sinh của khách hàng",
    # )

