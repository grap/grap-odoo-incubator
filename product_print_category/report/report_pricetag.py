from odoo import api, models


class ReportPricetag(models.AbstractModel):
    _name = "report.product_print_category.report_pricetag"
    _description = "Pricetag report"

    @api.model
    def _get_report_values(self, docids, data=None):

        docargs = {
            "categories_data": self._prepare_categories_data(data),
        }
        # mark the selected products as Up To Date if print succeed
        line_obj = self.env["product.print.wizard.line"]
        lines = line_obj.browse([int(x) for x in data["line_data"]])
        lines.mapped("product_id").write({"to_print": False})
        return docargs

    @api.model
    def _prepare_categories_data(self, data):
        category_obj = self.env["product.print.category"]
        line_obj = self.env["product.print.wizard.line"]

        # ordering data to print
        lines_dict = {}
        for line_id in data["line_data"]:
            line = line_obj.browse(int(line_id))
            category = line.product_id.print_category_id
            if category.id not in lines_dict:
                lines_dict[category.id] = [line.id]
            else:
                lines_dict[category.id].append(line.id)

        # Computing data to transfer
        categories_data = []
        for category_id, line_ids in lines_dict.items():
            category = category_obj.browse(category_id)
            categories_data.append(
                {
                    "print_category": category,
                    "report_model": "report_pricetag_custom",
                    "lines": line_obj.browse(line_ids),
                }
            )
        return categories_data
