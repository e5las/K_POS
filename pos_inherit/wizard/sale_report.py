from odoo import models, fields, api,_


class PosOrderWizard(models.TransientModel):
    _name = 'pos.order.report'

    date_start = fields.Date(string="Start Date", default=fields.Date.today)
    date_end = fields.Date(string="End Date",  default=fields.Date.today)

    def get_report(self):
        """Call when button 'Get Report' clicked.
        """

        data = {
            'ids': self.ids,
            'model': self._name,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
            },
        }

        return self.env.ref('pos_inherit.action_pos_order_list_report').report_action(self, data=data)

class ReportPOS_temp(models.AbstractModel):

    _name = 'report.pos_inherit.pos_order_list'

    @api.model
    def _get_report_values(self, docids, data=None):
        pos_obj = self.env['pos.order'].sudo()
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        res = pos_obj.search([
            ('date_order', '>=', date_start),
            ('date_order', '<=', date_end),

        ])
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end':date_end,
            'docs': res,
        }

