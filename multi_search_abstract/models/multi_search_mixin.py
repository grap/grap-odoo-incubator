# Copyright (C) 2013 - Today: GRAP (http://www.grap.coop)
# @author: Julien WESTE
# @author: Sylvain LE GAL (https://twitter.com/legalsylvain)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import string

from odoo import api, models


class MultiSearchMixin(models.AbstractModel):
    _name = "multi.search.mixin"
    _description = "Multi Search Mixin"

    _MULTI_SEARCH_OPERATORS = ["ilike", "not ilike"]

    # To Overwrite Section
    @api.model
    def _multi_search_search_fields(self):
        """Overwrite in inherited model to define field on which the search
        will be processed"""
        pass

    @api.model
    def _multi_search_write_fields(self):
        """Overwrite in inherited model to define fields that will not
        contain the special char"""
        pass

    @api.model
    def _multi_search_separator(self):
        """Overwrite in inherited model to define witch char will be used to
        split the search words"""
        return False

    # Overload Section
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        copy_args = list(args)
        if self._multi_search_separator():
            for arg in copy_args:
                if isinstance(arg, (tuple, list)) and len(arg) == 3:
                    name, operator, value = arg
                    if (
                        name in self._multi_search_search_fields()
                        and operator in self._MULTI_SEARCH_OPERATORS
                        and self._multi_search_separator() in value
                    ):
                        criterias = value.split(self._multi_search_separator())
                        new_arg_lst = [
                            (name, operator, x) for x in criterias if x != ""
                        ]
                        args = (
                            args[: args.index(arg)]
                            + ["&"] * (len(new_arg_lst) - 1)
                            + new_arg_lst
                            + args[args.index(arg) + 1 :]
                        )
        return super(MultiSearchMixin, self).search(
            args, offset=offset, limit=limit, order=order, count=count
        )

    @api.model
    def create(self, vals):
        if self._multi_search_separator():
            vals = self._multi_search_replace_dict(vals, True)
        return super(MultiSearchMixin, self).create(vals)

    # Custom Section
    @api.model
    def _multi_search_replace_all(self):
        """Replace the separator by the replacement char in all fields defined
        in _multi_search_write_fields() for the current model"""
        domain = []
        for field in self._multi_search_write_fields():
            domain.append(
                (field, "like", "%" + self._multi_search_separator() + "%")
            )
        domain = ["|" for x in range(len(domain) - 1)] + domain
        items = super(MultiSearchMixin, self).search(domain)
        for item in items:
            vals = {}
            for field in self._multi_search_write_fields():
                vals[field] = getattr(item, field)
            vals = self._multi_search_replace_dict(vals, False)
            if vals:
                item.write(vals)

    @api.model
    def _multi_search_replace_dict(self, vals, return_all):
        res = {}
        for field, value in vals.iteritems():
            if field in self._multi_search_write_fields() and value:
                new_value = string.replace(
                    value, self._multi_search_separator(), ""
                )
                if new_value != value or return_all:
                    res[field] = new_value
            elif return_all:
                res[field] = vals[field]
        return res
