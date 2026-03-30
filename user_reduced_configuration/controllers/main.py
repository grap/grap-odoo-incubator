from odoo import _, http
from odoo.exceptions import AccessError
from odoo.http import request

from odoo.addons.base_setup.controllers.main import BaseSetup


class UserReducedConfigurationSetup(BaseSetup):
    @http.route("/base_setup/data", type="json", auth="user")
    def base_setup_data(self, **kw):
        """Copy of the original base_setup_data() present in
        'base_setup' and 'auth_signup' module.
        Only the first line (check of group) is modified
        because it is not possible to sudo a Controllers
        # The rest is a copy of the base_setup code merged
        with the result of the auth_signup module.
        """
        # <Begin of the change>
        if not request.env.user.has_group(
            "base.group_erp_manager"
        ) and not request.env.user.has_group(
            "user_reduced_configuration.group_reduced_configuration"
        ):
            raise AccessError(_("Access Denied"))
        # </End of the change>

        cr = request.cr
        cr.execute(
            """
            SELECT count(*)
              FROM res_users
             WHERE active=true AND
                   share=false
        """
        )
        active_count = cr.dictfetchall()[0].get("count")

        cr.execute(
            """
            SELECT count(u.*)
            FROM res_users u
            WHERE active=true AND
                  share=false AND
                  NOT exists(SELECT 1 FROM res_users_log WHERE create_uid=u.id)
        """
        )
        pending_count = cr.dictfetchall()[0].get("count")

        cr.execute(
            """
           SELECT id, login
             FROM res_users u
            WHERE active=true AND
                  share=false AND
                  NOT exists(SELECT 1 FROM res_users_log WHERE create_uid=u.id)
         ORDER BY id desc
            LIMIT 10
        """
        )
        pending_users = cr.fetchall()
        action_pending_users = (
            request.env["res.users"]
            .browse([uid for (uid, login) in pending_users])
            ._action_show()
        )

        return {
            "active_users": active_count,
            "pending_count": pending_count,
            "pending_users": pending_users,
            "action_pending_users": action_pending_users,
            "resend_invitation": True,
        }
