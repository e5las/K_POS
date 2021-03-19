# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError, ValidationError

class ResPartner(models.Model):
    _inherit='res.partner'
    card_id=fields.Char("CARD ID")

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    
    lst_price_usd=fields.Float(string="Price/USD",default=1.0)
    date = fields.Datetime("Date",default=fields.Datetime.now())
    type=fields.Selection(default='product')
    company_new_id = fields.Many2one("res.company","Company",default=lambda self: self.env.company)
    available_in_pos = fields.Boolean(string='Available in POS', default=True)

    # @api.onchange('type')
    # def scrap_exipry_product(self):
    #     los_obj=self.env['stock.production.lot'].search([('removal_date','=',self.date)])
    #     print("################",los_obj)



class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    product_remove_alert = fields.Boolean(compute='_compute_product_remove_alert')
    product_remove_reminded = fields.Boolean(string="Expiry Remove has been reminded")
    d=fields.Boolean("D")
    user_id = fields.Many2one('res.users', string='USER', default=lambda self: self.env.uid)
    

    # @api.onchange('d')
    # def notificate_exipry_cron(self):        
    #     los_obj=self.search([('d','=',True)])
    #     model_obj=self.env['ir.model'].search([('model','=','stock.production.lot')])
    #     print("3333333333333333333333333333",model_obj)
    #     for rec in los_obj:
    #         pop_obj=self.env['mail.activity'].create({
    #         'activity_type_id':8,
    #         'res_model_id':model_obj.id,
    #         'res_name':model_obj.name,
    #         'res_id':rec.id,
    #         'user_id':rec.user_id.id

    #         })
            # message = self.env['calendar.event'].create({
            #     'name': str(x.name),
            #     # 'partner_ids': [(4, x.id)],
            #     'alarm_ids': [(4, 5), (4, 3), (4, 2)],
            #     'start': rec.alert_date,
            #     'stop': rec.removal_date,
            #     'allday': True,
            # }).id

        ##############create draft scrap
        # for rec in los_obj:
        #     scrap_obj=self.env['stock.scrap'].create({
        #     'product_id':rec.product_id.id,
        #     'lot_id':rec.id,
        #     'scrap_qty':rec.product_qty,
        #     'product_uom_id':rec.product_uom_id.id
        #     })
        # return message



     


    @api.depends('removal_date')
    def _compute_product_remove_alert(self):
        current_date = fields.Datetime.now()
        lots = self.filtered(lambda l: l.removal_date)
        for lot in lots:
            lot.product_remove_alert = lot.removal_date <= current_date
        (self - lots).product_remove_alert = False


    @api.depends('alert_date')
    def _compute_product_expiry_alert(self):
        current_date = fields.Datetime.now()
        lots = self.filtered(lambda l: l.alert_date)
        for lot in lots:
            lot.product_expiry_alert = lot.alert_date <= current_date
        (self - lots).product_expiry_alert = False
        self.d=self.product_remove_alert


        # los_obj=self.search([('d','=',True)])
        # model_obj=self.env['ir.model'].search([('model','=','stock.production.lot')])
        # print("3333333333333333333333333333",model_obj)
        # for rec in los_obj:
        #     activity=self.env['mail.activity'].search([('res_id','=',rec.id)])
        #     print("############3",activity)
        #     if not activity:
        #         # raise ValidationError(_("  is already opened for this point of sale."))
        #         pop_obj=self.env['mail.activity'].create({
        #         'activity_type_id':8,
        #         'res_model_id':model_obj.id,
        #         'res_name':model_obj.name,
        #         'res_id':rec.id,
        #         'user_id':rec.user_id.id

        #         })




    @api.model
    def _remove_date_exceeded(self):
        """Log an activity on internally stored lots whose alert_date has been reached.

        No further activity will be generated on lots whose alert_date
        has already been reached (even if the alert_date is changed).
        """
        alert_lots = self.env['stock.production.lot'].search([
            ('removal_date', '<=', fields.Date.today()),
            ('product_remove_reminded', '=', False)])

        lot_stock_quants = self.env['stock.quant'].search([
            ('lot_id', 'in', alert_lots.ids),
            ('quantity', '>', 0),
            ('location_id.usage', '=', 'internal')])
        alert_lots = lot_stock_quants.mapped('lot_id')

        for lot in alert_lots:
            lot.activity_schedule(
                'product_expiry.mail_activity_type_alert_date_reached',
                user_id=lot.product_id.responsible_id.id or SUPERUSER_ID,
                note=_("The alert date has been reached for this lot/serial number")
            )
        alert_lots.write({
            'product_remove_reminded': True
        })






class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'

    @api.model
    def _run_scheduler_tasks(self, use_new_cursor=False, company_id=False):
        super(ProcurementGroup, self)._run_scheduler_tasks(use_new_cursor=use_new_cursor, company_id=company_id)
        self.env['stock.production.lot']._remove_date_exceeded()
        if use_new_cursor:
            self.env.cr.commit()

class product_price(models.TransientModel):

    _name="update.product.price"

    currency_id=fields.Many2one("res.currency","Currency")
    date = fields.Date("Date",default=fields.Date.today())
    company_id = fields.Many2one("res.company","Company",default=lambda self: self.env.company)
    # cur_rate=fields.Float(string="Currency")
    
    # @api.onchange('currency_id')
    # def get_rate(self):
    #     currency_rate=self.env['res.currency.rate'].search([('currency_id','=',self.currency_id.id)])
    #     currency_rate_id = currency_rate and max(currency_rate)
    #     print ("@@@@@@@@@@@@@@@",currency_rate_id)
    #     self.cur_rate=currency_rate_id.rate
    #     print ("@@@@@@@@@@@@@@@22",self.cur_rate)


    def done(self):
        if self.currency_id:
            product_obj=self.env['product.template'].search([])

            total=0.0
            total=self.currency_id.rate
            print ("$$$$$$$$$$$$$$$",total)

            for rec in product_obj:
            	if rec.lst_price_usd>1:
            		rec.lst_price=rec.lst_price_usd*total


            # for rec in product_obj:
            #     total=self.currency_id.rate
            #     # total += self.currency_id._convert(rec.lst_price,self.currency_id,self.company_id,self.date)
            #     print ("$$$$$$$$$$$$$$$",total)
            #     if total!= 0.0:
            #     # rec.lst_price=total
            #    		rec.lst_price+=rec.lst_price/total

class PosOrder(models.Model):
    _inherit='pos.order'

    amount_total_new = fields.Float(string='Total per discount', digits=0, readonly=True, required=True,compute='_amount_all_new')

    @api.depends('lines.price_subtotal_incl')
    def _amount_all_new(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed  = 0.0
            for line in order.lines:
                if line.product_id.type=='product':
                    amount_untaxed += line.price_subtotal_incl
                    # amount_tax += line.price_tax
            order.update({
                # 'amount_untaxed_new': amount_untaxed,
                'amount_total_new': amount_untaxed ,
            })