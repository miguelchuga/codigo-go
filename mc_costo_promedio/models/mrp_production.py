# -*- coding: utf-8 -*-
# © 2015 Oihane Crucelaegui - AvanzOSC
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

#from openerp import fields, models
from openerp import models,fields,api,exceptions
from datetime import timedelta,date



class MrpProduction(models.Model):
    _inherit = 'mrp.production'


    @api.multi
    def calcular_costo_unitario(self):
        if self.costo_calculado:
            return
     
#        self.costo_materia_prima =  0
        if self.state == 'confirmed' or self.state == 'ready' or self.state == 'in_production':
            self.costo_unitario_produccion = 0
            self.costo_materia_prima = 0
            for m in self.move_lines:
                stock = self.env['stock.move'].browse(m.id)
                self.costo_materia_prima = self.costo_materia_prima + (stock.price_unit * stock.product_qty)
            self.costo_unitario_produccion = (self.costo_materia_prima / self.product_qty)
            self.costo_unitario_actual = self.product_id.standard_price
            self.costo_stock_actual = self.product_id.qty_available
            self.costo_unitario_final = ((self.product_id.standard_price*self.product_id.qty_available) +  self.costo_materia_prima) / ( self.product_qty + self.product_id.qty_available )
            self.env['stock.move'].browse(self.move_created_ids.id).write({'price_unit':self.costo_unitario_final})                
            self.env['product.product'].browse(self.product_id.id).write({'standard_price':self.costo_unitario_final})                
            self.costo_calculado = True

        return 

    notes = fields.Html()
    costo_materia_prima = fields.Float('Costo materia prima')##,compute=_calcular_costo, store=True)
    costo_unitario_produccion  = fields.Float('Costo unitario produccion')
    costo_unitario_actual  = fields.Float('Costo unitario actual ')
    costo_stock_actual  = fields.Float('Stock actual')
    costo_unitario_final  = fields.Float('Costo unitario final', default=False)

    costo_calculado = fields.Boolean('Calcula materia prima')

