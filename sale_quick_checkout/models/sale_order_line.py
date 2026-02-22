from odoo import api, fields, models, _


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # available_qty: tồn kho thực tế tại kho bán (warehouse stock location)
    available_qty = fields.Float(
        string="Available Qty",
        compute="_compute_available_qty",
        store=False,
    )

    def _compute_available_qty(self):
        """Compute on-hand quantity in the warehouse stock location.

        - Nếu sản phẩm là service: luôn 0, không check.
        - Các loại khác (product, consu) đều tính tồn.
        """
        Quant = self.env["stock.quant"]
        for line in self:
            available = 0.0
            product = line.product_id
            if not product:
                line.available_qty = 0.0
                continue

            # Odoo 18: detailed_type = 'product' / 'consu' / 'service' / 'combo'
            ptype = getattr(product, "detailed_type", product.type)
            if ptype == "service":
                line.available_qty = 0.0
                continue

            location = line._sqc_get_stock_location()
            if location:
                data = Quant.read_group(
                    domain=[
                        ("product_id", "=", product.id),
                        ("location_id", "child_of", location.id),
                    ],
                    fields=["quantity:sum"],
                    groupby=[],
                )
                if data:
                    qty_key = next(k for k in data[0].keys() if k.startswith("quantity"))
                    available = data[0][qty_key] or 0.0

            line.available_qty = available

    # ---------------------------------------------------------------------
    # Helper: xác định location để check tồn
    # ---------------------------------------------------------------------

    def _sqc_get_stock_location(self):
        """Return the main stock.location for this line's warehouse."""
        self.ensure_one()
        order = self.order_id
        company = order.company_id or self.env.company

        warehouse = order.warehouse_id
        if not warehouse:
            warehouse = (
                self.env["stock.warehouse"]
                .search([("company_id", "=", company.id)], limit=1)
            )

        if warehouse and warehouse.lot_stock_id:
            return warehouse.lot_stock_id

        # Fallback: location internal đầu tiên của company
        location = (
            self.env["stock.location"]
            .search([("usage", "=", "internal"), ("company_id", "=", company.id)], limit=1)
        )
        return location

    # ------------------------------------------------------------------
    # Onchanges: UX hạn chế bán vượt tồn ngay trên dòng SO
    # ------------------------------------------------------------------

    @api.onchange("product_id", "product_template_id")
    def _onchange_product_id_available_qty(self):
        """Khi chọn sản phẩm, chỉ cập nhật tồn và reset qty, KHÔNG popup.

        Cảnh báo (popup) sẽ chỉ xảy ra khi user nhập số lượng > tồn
        hoặc khi Confirm đơn (để tránh làm phiền khi mới chọn sản phẩm).
        """
        for line in self:
            product = line.product_id
            # Nếu chưa có variant, lấy variant mặc định từ template
            if not product and line.product_template_id:
                product = line.product_template_id.product_variant_id

            if not product:
                line.available_qty = 0.0
                continue

            ptype = getattr(product, "detailed_type", product.type)
            if ptype == "service":
                line.available_qty = 0.0
                continue

            line._compute_available_qty()

            # Nếu hết hàng: chỉ đặt qty = 0, không hiện popup ngay.
            # User sẽ được cảnh báo nếu cố nhập qty > 0 ở onchange qty
            # hoặc khi Confirm SO (action_confirm).
            if line.available_qty <= 0:
                line.product_uom_qty = 0.0

    @api.onchange("product_uom_qty", "product_id", "product_template_id")
    def _onchange_product_uom_qty_available(self):
        """Khi đổi số lượng, tự giới hạn theo available_qty + cảnh báo."""
        for line in self:
            product = line.product_id
            if not product and line.product_template_id:
                product = line.product_template_id.product_variant_id

            if not product:
                continue

            ptype = getattr(product, "detailed_type", product.type)
            if ptype == "service":
                continue

            line._compute_available_qty()

            if line.product_uom_qty and line.product_uom_qty > line.available_qty:
                if line.available_qty > 0:
                    msg = _(
                        "Chỉ còn %(available).2f sản phẩm '%(name)s' trong kho. "
                        "Số lượng đặt sẽ được giảm từ %(ordered).2f xuống %(available).2f."
                    ) % {
                        "available": line.available_qty,
                        "name": product.display_name,
                        "ordered": line.product_uom_qty,
                    }
                    line.product_uom_qty = line.available_qty
                else:
                    msg = _(
                        "Biến thể '%s' hiện đang hết hàng trong kho. "
                        "Số lượng đặt sẽ được đặt về 0."
                    ) % (product.display_name,)
                    line.product_uom_qty = 0.0

                return {
                    "warning": {
                        "title": _("Không đủ tồn kho"),
                        "message": msg,
                    }
                }