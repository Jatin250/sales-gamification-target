from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = "sale.order"

    commission_earned = fields.Monetary(
        string="Estimated Commission (2%)",
        compute="_compute_commission",
        currency_field="currency_id",
    )

    user_target_progress = fields.Float(
        related="user_id.target_progress", string="User Target Progress", readonly=True
    )

    # --> NEW FIELD ADDED <--
    user_target_type = fields.Selection(
        related="user_id.target_type", string="Target Type", readonly=True
    )

    @api.depends("amount_total", "state")
    def _compute_commission(self):
        for order in self:
            if order.state in ["sale", "done"]:
                order.commission_earned = order.amount_total * 0.02
            else:
                order.commission_earned = 0.0
