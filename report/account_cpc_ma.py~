##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
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

import time

from openerp.report import report_sxw
from common_report_header import common_report_header
from openerp.tools.translate import _
from openerp.osv import osv


class report_account_common(report_sxw.rml_parse, common_report_header):
    _name= 'report.account.common'
    def __init__(self, cr, uid, name, context=None):
        super(report_account_common, self).__init__(cr, uid, name, context=context)
        self.localcontext.update( {

            'get_lines': self.get_lines,
            'get_lines_child': self.get_lines_child,
            'time': time,
            'get_fiscalyear': self._get_fiscalyear,
            'get_account': self._get_account,
            'get_start_period': self.get_start_period,
            'get_end_period': self.get_end_period,
            'get_filter': self._get_filter,
            'get_start_date':self._get_start_date,
            'get_end_date':self._get_end_date,
            'get_target_move': self._get_target_move,
        })
        self.context = context

    def set_context(self, objects, data, ids, report_type=None):
        new_ids = ids
        if (data['model'] == 'ir.ui.menu'):
            new_ids = 'chart_account_id' in data['form'] and [data['form']['chart_account_id']] or []
            objects = self.pool.get('account.account').browse(self.cr, self.uid, new_ids)
        return super(report_account_common, self).set_context(objects, data, new_ids, report_type=report_type)

    

    def get_lines(self, data):
        lines = []
        account_obj = self.pool.get('account.account')
        ids1=account_obj.search(self.cr, self.uid, [('name', '=', "PRODUITS D'EXPLOITATION")], context=data['form']['used_context'])
        ids2=account_obj.search(self.cr, self.uid, [('name', '=', "CHARGES D'EXPLOITATION")], context=data['form']['used_context'])
        ids3=account_obj.search(self.cr, self.uid, [('name', '=', "RESULTAT D'EXPLOITATION")], context=data['form']['used_context'])
        ids4=account_obj.search(self.cr, self.uid, [('name', '=', "PRODUITS FINANCIERS")], context=data['form']['used_context'])
        ids5=account_obj.search(self.cr, self.uid, [('name', '=', "CHARGES FINANCIERES")], context=data['form']['used_context'])
        ids6=account_obj.search(self.cr, self.uid, [('name', '=', "RESULTAT FINANCIER")], context=data['form']['used_context'])
        ids7=account_obj.search(self.cr, self.uid, [('name', '=', "RESULTAT COURANT")], context=data['form']['used_context'])
        ids8=account_obj.search(self.cr, self.uid, [('name', '=', "PRODUITS NON COURANTS")], context=data['form']['used_context'])
        ids9=account_obj.search(self.cr, self.uid, [('name', '=', "CHARGES NON COURANTES")], context=data['form']['used_context'])
        ids10=account_obj.search(self.cr, self.uid, [('name', '=', "RESULTAT NON COURANT")], context=data['form']['used_context'])
        ids11=account_obj.search(self.cr, self.uid, [('name', '=', "RESULTAT AVANT IMPOTS")], context=data['form']['used_context'])
        ids12=account_obj.search(self.cr, self.uid, [('name', '=', "IMPOTS SUR LES RESULTATS")], context=data['form']['used_context'])
      

        ids14=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids1)], context=data['form']['used_context'])
        ids15=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids2)], context=data['form']['used_context'])
        ids16=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids3)], context=data['form']['used_context'])
        ids17=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids4)], context=data['form']['used_context'])
        ids18=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids5)], context=data['form']['used_context'])
        ids19=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids6)], context=data['form']['used_context'])
        ids20=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids7)], context=data['form']['used_context'])
        ids21=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids8)], context=data['form']['used_context'])
        ids22=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids9)], context=data['form']['used_context'])
        ids23=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids10)], context=data['form']['used_context'])
        ids24=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids11)], context=data['form']['used_context'])
        ids25=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids12)], context=data['form']['used_context'])
       
        

        vals = {
                'name_parent': account_obj.browse(self.cr, self.uid, ids1).name,
                        }           
        lines.append(vals)
        for cls in account_obj.browse(self.cr, self.uid, ids14):
            vals = {
                'name': cls.name,
                'balance': cls.balance,
               
                        }           
            lines.append(vals)
        vals = {
                'name_parent': account_obj.browse(self.cr, self.uid, ids2).name,
                        }           
        lines.append(vals)

        for cls in account_obj.browse(self.cr, self.uid, ids15):
            vals = {
                'name': cls.name,
                'balance': cls.balance,
                
                        }
            lines.append(vals)
        vals = {
                'name_parent': account_obj.browse(self.cr, self.uid, ids3).name,
                        }           
        lines.append(vals)

        
        vals = {
                'name_parent': account_obj.browse(self.cr, self.uid, ids4).name,
                        }           
        lines.append(vals)
        for cls in account_obj.browse(self.cr, self.uid, ids14):
            vals = {
                'name': cls.name,
                'balance': cls.balance,
               
                        }           
            lines.append(vals)
        vals = {
                'name_parent': account_obj.browse(self.cr, self.uid, ids5).name,
                        }           
        lines.append(vals)

        for cls in account_obj.browse(self.cr, self.uid, ids15):
            vals = {
                'name': cls.name,
                'balance': cls.balance,
                
                        }
            lines.append(vals)
        vals = {
                'name_parent': account_obj.browse(self.cr, self.uid, ids6).name,
                        }           
        lines.append(vals)

        
        vals = {
                'name_parent': account_obj.browse(self.cr, self.uid, ids7).name,
                        }           
        lines.append(vals)
        
        vals = {
                'name_parent': account_obj.browse(self.cr, self.uid, ids8).name,
                        }           
        lines.append(vals)

        for cls in account_obj.browse(self.cr, self.uid, ids18):
            vals = {
                'name': cls.name,
                'balance': cls.balance,
                
                        }
            lines.append(vals)
        vals = {
                'name_parent': account_obj.browse(self.cr, self.uid, ids9).name,
                        }           
        lines.append(vals)

        for cls in account_obj.browse(self.cr, self.uid, ids19):
            vals = {
                'name': cls.name,
                'balance': cls.balance,
                
                        }
            lines.append(vals)
        vals = {
                'name_parent': account_obj.browse(self.cr, self.uid, ids10).name,
                        }           
        lines.append(vals)
        
        vals = {
                'name_parent': account_obj.browse(self.cr, self.uid, ids11).name,
                        }           
        lines.append(vals)

        
        vals = {
                'name_parent': account_obj.browse(self.cr, self.uid, ids12).name,
                        }           
        lines.append(vals)
        vals = {
                'name_parent': 'RESULTAT NET',
                        }           
        lines.append(vals)
        vals = {
                'name_parent': 'TOTAL DES PRODUITS',
                        }           
        lines.append(vals)
        vals = {
                'name_parent': 'TOTAL DES CHARGES',
                        }           
        lines.append(vals)
        vals = {
                'name_parent': 'RESULTAT NET (Total des produits - Total des charges)',
                        }           
        lines.append(vals)



        return lines


    def get_lines_child(self, data,cl):
        lines = []
        account_obj = self.pool.get('account.account')
        ids1=account_obj.search(self.cr, self.uid, [('name', '=', cl)], context=data['form']['used_context'])
        ids_child=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids1)], context=data['form']['used_context'])

        for child in account_obj.browse(self.cr, self.uid, ids_child):
            vals = {
                 'name_child': child.name,
                 'balance_child': child.balance,
               
                        }
            lines.append(vals)
        return lines
                



class report_cpc_ma(osv.AbstractModel):
    _name = 'report.account_tax_return.report_cpc_ma'
    _inherit = 'report.abstract_report'
    _template = 'account_tax_return.report_cpc_ma'
    _wrapped_report_class = report_account_common

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
