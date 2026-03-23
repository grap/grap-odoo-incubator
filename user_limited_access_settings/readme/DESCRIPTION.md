This module adds a new basic Administration group named, "Limited
Settings".

Members of this group can only create :

- Users (`res.users`)
- Companies (`res.company`)
- Sequences (`ir.sequence` and `ir.sequence.date.range`)
- Banks (`res.bank`)

And see :

- User Roles (`res.users.role`)
- `ir.module.category`
- `ir.rule`
- `ir.model.fields`
- `ir.model.access`

**Note:**

We prevent right escalation, by preventing user to give access to groups
if he is not member of the group himself.
