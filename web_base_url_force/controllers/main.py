# coding: utf-8
# Copyright (C) 2019 - Today: GRAP (http://www.grap.coop)
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import openerp
import openerp.http as http
from openerp.http import request


class Home(openerp.addons.web.controllers.main.Home):

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        request.registry['ir.config_parameter'].web_base_url_force(
            request.cr,
            openerp.SUPERUSER_ID,
            request.context)
        return super(Home, self).web_client(s_action=s_action, **kw)

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        request.registry['ir.config_parameter'].web_base_url_force(
            request.cr,
            openerp.SUPERUSER_ID,
            request.context)
        return super(Home, self).web_login(redirect=redirect, **kw)
