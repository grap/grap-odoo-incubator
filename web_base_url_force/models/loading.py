# coding: utf-8
# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import logging

from openerp.tools import config as odoo_config
from openerp.modules import loading

_logger = logging.getLogger(__name__)


original_load_module_graph = loading.load_module_graph


def overload_load_module_graph(
        cr, graph, status=None, perform_checks=True, skip_modules=None,
        report=None):
    res = original_load_module_graph(
        cr, graph, status=status, perform_checks=perform_checks,
        skip_modules=skip_modules, report=report)

    if not odoo_config.get('web_base_url_force', False):
        return res

    new_setting = odoo_config.get('web_base_url_force', False)

    cr.execute("""
        SELECT value
        FROM ir_config_parameter
        WHERE key = 'web.base.url';""")
    result = cr.fetchone()
    if result:
        current_setting = result[0]
        if current_setting != new_setting:
            _logger.info("key 'web.base.url' %s replaced by %s" % (
                current_setting, new_setting))
            cr.execute("""
                UPDATE ir_config_parameter
                SET value = %s
                WHERE KEY = 'web.base.url';""", (new_setting, ))
    return res


loading.load_module_graph = overload_load_module_graph
