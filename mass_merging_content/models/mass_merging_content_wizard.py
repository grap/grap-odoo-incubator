# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import api, models


class MassMergingContentWizard(models.TransientModel):
    _name = 'mass.merging.content.wizard'
    _inherit = 'mass.operation.wizard.mixin'

    @api.multi
    def _apply_operation(self, items):
        print ">>>>>>>>>>>>>>>> BIM"
        pass
