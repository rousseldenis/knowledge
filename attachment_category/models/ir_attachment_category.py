# Copyright 2019 Denis Roussel
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _


class IrAttachmentCategory(models.Model):

    _name = 'ir.attachment.category'
    _description = 'Attachment Category'
    _parent_store = True

    name = fields.Char()
    display_name = fields.Char(
        compute="_compute_complete_name",
        store=True,
    )
    parent_id = fields.Many2one(
        "ir.attachment.category",
    )
    parent_path = fields.Char(index=True)
    attachment_ids = fields.Many2many(
        compute="_compute_attachment_ids",
    )
    attachment_count = fields.Integer(
        compute="_compute_attachment_count",
    )

    @api.depends('name', 'parent_id.complete_name')
    def _compute_display_name(self):
        """

        :return:
        """
        for category in self:
            if category.parent_id.complete_name:
                category.display_name = '%s/%s' % (
                category.parent_id.complete_name, category.name)
            else:
                category.display_name = category.name

    @api.depends()
    def _compute_attachment_count(self):
        self.env.cr.execute("SELECT attachment_id")
        for category in self:

            self.env.cr.execute(
                """
                
WITH RECURSIVE attachments AS (
   SELECT
      id,
      category_id,
   FROM
      ir_attachment
   UNION
      SELECT
         ir.id,
         ir.category_id
      FROM
         ir_attachment ir
      INNER JOIN subordinates s ON s.employee_id = e.manager_id
) SELECT
   *
FROM
   subordinates;
                """
            )