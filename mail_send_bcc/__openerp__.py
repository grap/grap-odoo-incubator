# -*- encoding: utf-8 -*-
##############################################################################
#
#    Mail - Send BCC for Odoo
#    Copyright (C) 2014 GRAP (http://www.grap.coop)
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

{
    'name': 'Mail - Send Email Bcc',
    'version': '1.0',
    'category': 'Social Network',
    'description': """
Give the possibility to users to receive each mail sent by OpenERP
==================================================================

Functionnality:
---------------
    * Add an extra field 'email_send_bcc' in res.users;
    * If Checked, for each mail the user send, the user will receive the copy
    in BCC mode;

Use Case:
---------
This feature can be usefull for users:
    * to be sure the mail was sent because OpenERP send mail depending of
    some partner parameters;
    * to have the whole conversation if the partner writes an answer and if
    mailbox manages thread by object;
    * to be sure smtp server works;

Copyright, Author and Licence:
------------------------------
    * Copyright: 2014, Groupement Régional Alimentaire de Proximité
    * Author: Sylvain LE GAL (https://twitter.com/legalsylvain)
    * Licence: AGPL-3 (http://www.gnu.org/licenses/)
    """,
    'author': 'GRAP',
    'website': 'http://www.grap.coop',
    'license': 'AGPL-3',
    'depends': [
        'mail',
    ],
    'data': [
        'view/res_users_view.xml',
    ],
    'installable': True,
}
