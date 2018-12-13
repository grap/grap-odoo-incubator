# coding: utf-8
# Copyright (C) 2018 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from openerp import models


class MassMergingContent(models.Model):
    _name = 'mass.merging.content'
    _inherit = 'mass.operation.mixin'

    _action_pattern_name = "Merge Content"

    _wizard_model_name = 'mass.merging.context.wizard'
