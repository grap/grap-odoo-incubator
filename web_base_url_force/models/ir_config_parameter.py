# coding: utf-8
# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openerp import api, models
from openerp.tools import config as odoo_config

_logger = logging.getLogger(__name__)


class IrconfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    @api.model
    def set_param(self, key, value, groups=[]):
        force_url = odoo_config.get('web_base_url_force', False)
        if key == 'web.base.url' and force_url:
            _logger.info(
                "key 'web.base.url' : skipping regular update.")
            return True
        else:
            return super(IrconfigParameter, self).set_param(
                key, value, groups=groups)
