# -*- encoding: utf-8 -*-
##############################################################################
#
#    Point Of Sale - Street Market module for Odoo
#    Copyright (C) 2013-Today GRAP (http://www.grap.coop)
#    @author Sylvain LE GAL (https://twitter.com/legalsylvain)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields


class MarketPlace(models.Model):
    _name = 'market.place'

    # Default section
    def _default_company_id(self):
        return self.env.user.company_id.id

    # Columns section
    code = fields.Char(required=True, size=6)

    name = fields.Char(required=True)

    active = fields.Boolean(default=True)

    company_id = fields.Many2one(
        string='Company', comodel_name='res.company', required=True,
        readonly=True, default=_default_company_id)
