from odoo import models, fields, api
from datetime import date
from dateutil.relativedelta import relativedelta


class ResUsers(models.Model):
    _inherit = "res.users"

    # New Dynamic Fields
    target_amount = fields.Monetary(
        string="Target Amount", currency_field="company_id_currency"
    )
    target_type = fields.Selection(
        [("monthly", "Monthly"), ("yearly", "Yearly"), ("custom", "Custom")],
        string="Target Type",
        default="monthly",
    )

    target_start_date = fields.Date(string="Start Date")
    target_end_date = fields.Date(string="End Date")

    current_sales = fields.Monetary(
        compute="_compute_target_progress",
        string="Sales Achieved",
        currency_field="company_id_currency",
    )
    target_progress = fields.Float(
        compute="_compute_target_progress", string="Target Progress (%)"
    )

    company_id_currency = fields.Many2one(
        "res.currency", related="company_id.currency_id", readonly=True
    )

    # Automatically set dates when Admin selects Monthly or Yearly
    @api.onchange("target_type")
    def _onchange_target_type(self):
        today = date.today()
        if self.target_type == "monthly":
            self.target_start_date = today.replace(day=1)
            # Last day of current month
            self.target_end_date = (
                today + relativedelta(months=1, day=1)
            ) - relativedelta(days=1)
        elif self.target_type == "yearly":
            self.target_start_date = today.replace(month=1, day=1)
            self.target_end_date = today.replace(month=12, day=31)

    @api.depends("target_amount", "target_start_date", "target_end_date")
    def _compute_target_progress(self):
        for user in self:
            # If dates aren't set, default to 0
            if not user.target_start_date or not user.target_end_date:
                user.current_sales = 0.0
                user.target_progress = 0.0
                continue

            # Search based on the custom dates!
            sales = self.env["sale.order"].search(
                [
                    ("user_id", "=", user.id),
                    ("state", "in", ["sale", "done"]),
                    ("date_order", ">=", user.target_start_date),
                    ("date_order", "<=", user.target_end_date),
                ]
            )

            total = sum(sales.mapped("amount_total"))
            user.current_sales = total

            if user.target_amount and user.target_amount > 0:
                user.target_progress = (total / user.target_amount) * 100
            else:
                user.target_progress = 0.0
