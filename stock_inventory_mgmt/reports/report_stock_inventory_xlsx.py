from odoo import _, models

from odoo.addons.report_xlsx_helper.report.report_xlsx_format import (
    FORMATS,
    XLS_HEADERS,
)


class StockInventoryXlsx(models.AbstractModel):
    _name = "report.stock_inventory_mgmt.report_stock_inventory_xlsx"
    _inherit = "report.report_xlsx.abstract"
    _description = "Stock Inventory Report in XLSX"

    def _define_custom_formats(self, workbook, inventories):
        currency = inventories[0].currency_id
        s_before = currency.symbol if currency.position == "before" else ""
        s_after = " %s" % currency.symbol if currency.position == "after" else ""
        currency_format = (
            f"{f'{s_before}'}#,##0.{'0' * currency.decimal_places}{f'{s_after}'}"
        )
        FORMATS["format_currency_right"] = workbook.add_format(
            {"align": "right", "num_format": currency_format}
        )

    def generate_xlsx_report(self, workbook, data, inventories):
        self._define_formats(workbook)
        self._define_custom_formats(workbook, inventories)
        ws_params = self._get_ws_params(workbook, data, inventories.mapped("line_ids"))[
            0
        ]

        for inventory in inventories:
            ws_name = inventory.name
            ws_name = self._check_ws_name(ws_name)
            ws = workbook.add_worksheet(ws_name)
            generate_ws_method = getattr(self, ws_params["generate_ws_method"])
            generate_ws_method(workbook, ws, ws_params, data, inventory.line_ids)

    def _get_ws_params(self, wb, data, line_ids):
        columns_spec = self._get_columns_spec(line_ids)

        line_ids_template = {}
        for spec in columns_spec:
            line_ids_template[spec["name"]] = {
                "header": {
                    "value": spec["header_name"],
                },
                "data": {
                    "value": spec["data"],
                    "format": spec.get("format", False),
                },
                "width": spec["width"],
            }

        return [
            {
                "generate_ws_method": "_purchase_inventory_report",
                "wanted_list": [x["name"] for x in columns_spec],
                "col_specs": line_ids_template,
            }
        ]

    def _purchase_inventory_report(
        self, workbook, ws, ws_params, data, inventory_lines
    ):
        ws.set_portrait()
        ws.fit_to_pages(1, 0)
        ws.set_header(XLS_HEADERS["xls_headers"]["standard"])
        ws.set_footer(XLS_HEADERS["xls_footers"]["standard"])

        self._set_column_width(ws, ws_params)

        row_pos = 0
        row_pos = self._write_line(
            ws,
            row_pos,
            ws_params,
            col_specs_section="header",
            default_format=FORMATS["format_theader_yellow_left"],
        )
        ws.freeze_panes(row_pos, 0)

        for inventory_line in inventory_lines:
            row_pos = self._write_line(
                ws,
                row_pos,
                ws_params,
                col_specs_section="data",
                render_space={"inventory_line": inventory_line},
                default_format=FORMATS["format_tcell_right"],
            )

    def _get_columns_spec(self, inventory_lines):
        res = [
            {
                "name": "product_name",
                "header_name": _("Product"),
                "data": self._render("inventory_line.product_id.name"),
                "format": FORMATS["format_tcell_left"],
                "width": 50,
            },
            {
                "name": "category_name",
                "header_name": _("Category"),
                "data": self._render(
                    "inventory_line.product_category_id.complete_name"
                ),
                "format": FORMATS["format_tcell_left"],
                "width": 35,
            },
            {
                "name": "product_qty",
                "header_name": _("Quantity"),
                "data": self._render("inventory_line.product_qty"),
                "width": 10,
            },
            {
                "name": "uom_name",
                "header_name": _("UoM"),
                "data": self._render("inventory_line.product_uom_id.name"),
                "width": 10,
            },
            {
                "name": "price_unit",
                "header_name": _("Price Unit"),
                "data": self._render("inventory_line.price_unit"),
                "format": FORMATS["format_currency_right"],
                "width": 10,
            },
            {
                "name": "valuation",
                "header_name": _("Valuation"),
                "data": self._render("inventory_line.valuation"),
                "format": FORMATS["format_currency_right"],
                "width": 15,
            },
        ]

        return res
