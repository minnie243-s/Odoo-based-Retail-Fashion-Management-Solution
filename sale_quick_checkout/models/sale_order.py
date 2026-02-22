from odoo import _, models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):
        """Check tồn kho trước khi confirm.

        - Check mọi dòng hàng hóa (Goods/Consumable), bỏ qua Service.
        - Nếu qty <= 0 hoặc > tồn kho → chặn, báo lỗi tiếng Việt.
        """
        for order in self:
            for line in order.order_line:
                product = line.product_id
                if not product:
                    continue

                ptype = getattr(product, "detailed_type", product.type)
                # Chỉ bỏ qua dịch vụ, còn lại (product/consu) đều phải check tồn
                if ptype == "service":
                    continue

                # Tính lại tồn tại thời điểm confirm
                line._compute_available_qty()

                if line.product_uom_qty <= 0:
                    raise UserError(
                        _(
                            "Dòng sản phẩm '%s' có số lượng phải lớn hơn 0.\n"
                            "Vui lòng điều chỉnh trước khi xác nhận đơn."
                        )
                        % (product.display_name,)
                    )

                if line.product_uom_qty > line.available_qty:
                    raise UserError(
                        _(
                            "Không đủ tồn kho cho sản phẩm '%(name)s'.\n"
                            "Còn %(available).2f trong kho, bạn đang đặt %(ordered).2f.\n"
                            "Vui lòng giảm số lượng hoặc nhập thêm hàng vào kho."
                        )
                        % {
                            "name": product.display_name,
                            "available": line.available_qty,
                            "ordered": line.product_uom_qty,
                        }
                    )

        return super().action_confirm()