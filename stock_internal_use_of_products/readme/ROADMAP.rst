If the user use a product without an expense account, it can confirm the
internal use, and so, generate stock move, but the generation of the
accounting move will be blocked.

We could imagine to introduce a field account_id, with a on_change, as
any accounting object. (invoice, move, etc.)
