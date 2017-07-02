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
from datetime import date,datetime, timedelta

class report_account_common(report_sxw.rml_parse, common_report_header):
    _name= 'report.account.common'
    def __init__(self, cr, uid, name, context=None):
        super(report_account_common, self).__init__(cr, uid, name, context=context)
        self.localcontext.update( {

            'get_lines': self.get_lines,
            'get_lines_bilan_passif': self.get_lines_bilan_passif,
            'get_lines_immobilisation': self.get_lines_immobilisation,
            'get_lines_child': self.get_lines_child,
            #'get_account_by_class': self.get_account_by_class,
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
        fisc_start = self.pool.get('account.fiscalyear').browse(self.cr, self.uid, data['form']['fiscalyear_id'],context=data['form']['used_context']).date_start
        date_start=datetime.strptime(fisc_start,"%Y-%m-%d")
        d = date_start - timedelta(days=1)
        
        domain = [('date_stop', '=', d)]
        prev_fisc=self.pool.get('account.fiscalyear').search(self.cr, self.uid, domain, limit=1)

        data['form']['used_context'].update({'fiscalyear_id':prev_fisc})
        fisc_stop = self.pool.get('account.fiscalyear').browse(self.cr, self.uid,prev_fisc,context=data['form']['used_context']).date_stop
        
        print('***************************',data['form']['used_context'].get('fiscalyear_id'))
        ids1=account_obj.search(self.cr, self.uid, [('name', '=', "COMPTES D'ACTIF IMMOBILISE")], context=data['form']['used_context'])
        ids2=account_obj.search(self.cr, self.uid, [('name', '=', "COMPTES D'ACTIF CIRCULANT (HORS TRESORERIE)")], context=data['form']['used_context'])
        ids3=account_obj.search(self.cr, self.uid, [('name', '=', "COMPTES DE TRESORERIE")], context=data['form']['used_context'])

        ids4=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids1)], context=data['form']['used_context'])

        ids5=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids2)], context=data['form']['used_context'])

        ids6=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids3)], context=data['form']['used_context'])

        ids_amm=account_obj.search(self.cr, self.uid, [('name', '=', "AMORTISSEMENTS DES IMMOBILISATIONS")], context=data['form']['used_context'])
        ids_amm1=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids_amm)], context=data['form']['used_context'])
        ids_provis1=account_obj.search(self.cr, self.uid, [('name', '=', "PROVISIONS POUR DEPRECIATION DES IMMOBILISATIONS")], context=data['form']['used_context'])
        ids_prov1=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids_provis1)], context=data['form']['used_context'])
        ids_provis2=account_obj.search(self.cr, self.uid, [('name', '=', "PROVISIONS POUR DEPRECIATION DES COMPTES DE L'ACTIF CIRCULANT")], context=data['form']['used_context'])
        ids_prov2=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids_provis2)], context=data['form']['used_context'])
        print("*****identifiant*******************",account_obj.browse(self.cr, self.uid, ids_amm1[0]).balance)
        vals = {
                     'amm_nv': account_obj.browse(self.cr, self.uid, ids_amm1[0]).balance,
                     'amm_imm_incorp': account_obj.browse(self.cr, self.uid,ids_amm1[1]).balance,
                     'amm_imm_corp': account_obj.browse(self.cr, self.uid, ids_amm1[2]).balance,
                            }
        lines.append(vals)

        vals = {
                     'prov_imm_incorp': account_obj.browse(self.cr, self.uid,ids_prov1[0]).balance,
                     'prov_imm_corp': account_obj.browse(self.cr, self.uid, ids_prov1[1]).balance,
                     'prov_imm_finan1': account_obj.browse(self.cr, self.uid, ids_prov1[2]).balance,
                     'prov_imm_finan2': account_obj.browse(self.cr, self.uid, ids_prov1[3]).balance,
                            }
        lines.append(vals)

        vals = {
                     'prov_stock': account_obj.browse(self.cr, self.uid,ids_prov2[0]).balance,
                     'prov_creance_ac': account_obj.browse(self.cr, self.uid, ids_prov2[1]).balance,
                     'prov_tvp': account_obj.browse(self.cr, self.uid, ids_prov2[2]).balance,
                            }
        lines.append(vals)

        for cls in account_obj.browse(self.cr, self.uid, ids4):
            
            vals = {
                    'name': cls.name,
                    'balance': cls.balance,
                        }
            
            lines.append(vals)

        for cls in account_obj.browse(self.cr, self.uid, ids5):
            vals = {
                'name': cls.name,
                'balance': cls.balance,
                
                        }
            lines.append(vals)

        for cls in account_obj.browse(self.cr, self.uid, ids6):
            vals = {
                'name': cls.name,
                'balance': cls.balance,
                
                        }

            lines.append(vals)

        return lines
    

    def get_lines_bilan_passif(self, data):
        lines = []
        account_obj = self.pool.get('account.account')
        fisc_start = self.pool.get('account.fiscalyear').browse(self.cr, self.uid, data['form']['fiscalyear_id'],context=data['form']['used_context']).date_start
        date_start=datetime.strptime(fisc_start,"%Y-%m-%d")
        d = date_start - timedelta(days=1)
        domain = [('date_stop', '=', d)]
        prev_fisc=self.pool.get('account.fiscalyear').search(self.cr, self.uid, domain, limit=1)

        data['form']['used_context'].update({'fiscalyear_id':prev_fisc})
        fisc_stop = self.pool.get('account.fiscalyear').browse(self.cr, self.uid,prev_fisc,context=data['form']['used_context']).date_stop
    
        ids1=account_obj.search(self.cr, self.uid, [('name', '=', "COMPTES DE FINANCEMENT PERMANENT")], context=data['form']['used_context'])
        ids2=account_obj.search(self.cr, self.uid, [('name', '=', "COMPTES DU PASSIF CIRCULANT (HORS TRESORERIE)")], context=data['form']['used_context'])
        ids3=account_obj.search(self.cr, self.uid, [('name', '=', "TRESORERIE - PASSIF")], context=data['form']['used_context'])

        ids4=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids1)], context=data['form']['used_context'])

        ids5=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids2)], context=data['form']['used_context'])

        ids6=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids3)], context=data['form']['used_context'])

        for cls in account_obj.browse(self.cr, self.uid, ids4):
            
            vals = {
                    'name': cls.name,
                    'balance': cls.balance,
                        }
            
            lines.append(vals)

        for cls in account_obj.browse(self.cr, self.uid, ids5):
            vals = {
                'name': cls.name,
                'balance': cls.balance,
                
                        }
            lines.append(vals)

        for cls in account_obj.browse(self.cr, self.uid, ids6):
            vals = {
                'name': cls.name,
                'balance': cls.balance,
                
                        }

            lines.append(vals)

        return lines

    def get_lines_immobilisation(self, data):
        lines = []
        
        vals = {'name': "IMMOBILISATIONS EN NON-VALEURS",} 
        lines.append(vals)
        vals = {'name': "IMMOBILISATIONS INCORPORELLES",}  
        lines.append(vals)
        vals = {'name': "IMMOBILISATIONS CORPORELLES",}  
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
                

class report_financial_marocain(osv.AbstractModel):
    _name = 'report.account_tax_return.report_financial_marocain'
    _inherit = 'report.abstract_report'
    _template = 'account_tax_return.report_financial_marocain'
    _wrapped_report_class = report_account_common

class report_bilan_passif(osv.AbstractModel):
    _name = 'report.account_tax_return.report_bilan_passif'
    _inherit = 'report.abstract_report'
    _template = 'account_tax_return.report_bilan_passif'
    _wrapped_report_class = report_account_common

class report_passage_result(osv.AbstractModel):
    _name = 'report.account_tax_return.report_passage_result'
    _inherit = 'report.abstract_report'
    _template = 'account_tax_return.report_passage_result'
    _wrapped_report_class = report_account_common

class report_immobilisation(osv.AbstractModel):
    _name = 'report.account_tax_return.report_immobilisation'
    _inherit = 'report.abstract_report'
    _template = 'account_tax_return.report_immobilisation'
    _wrapped_report_class = report_account_common

class report_ammortissement(osv.AbstractModel):
    _name = 'report.account_tax_return.report_ammortissement'
    _inherit = 'report.abstract_report'
    _template = 'account_tax_return.report_ammortissement'
    _wrapped_report_class = report_account_common

class report_pmv_immobilisation(osv.AbstractModel):
    _name = 'report.account_tax_return.report_pmv_immobilisation'
    _inherit = 'report.abstract_report'
    _template = 'account_tax_return.report_pmv_immobilisation'
    _wrapped_report_class = report_account_common

class report_surete(osv.AbstractModel):
    _name = 'report.account_tax_return.report_surete'
    _inherit = 'report.abstract_report'
    _template = 'account_tax_return.report_surete'
    _wrapped_report_class = report_account_common

class report_tva(osv.AbstractModel):
    _name = 'report.account_tax_return.report_tva'
    _inherit = 'report.abstract_report'
    _template = 'account_tax_return.report_tva'
    _wrapped_report_class = report_account_common

class report_repartition_capital(osv.AbstractModel):
    _name = 'report.account_tax_return.report_repartition_capital'
    _inherit = 'report.abstract_report'
    _template = 'account_tax_return.report_repartition_capital'
    _wrapped_report_class = report_account_common

class report_credit_bail(osv.AbstractModel):
    _name = 'report.account_tax_return.report_credit_bail'
    _inherit = 'report.abstract_report'
    _template = 'account_tax_return.report_credit_bail'
    _wrapped_report_class = report_account_common
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
