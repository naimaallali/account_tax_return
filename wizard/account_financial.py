# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
from openerp.osv import fields, osv
from openerp.tools.translate import _
#from openerp import models, fields, api
from openerp.report import report_sxw
#from report_account_common import report_account_common

class account_financial(osv.osv_memory):

    #_inherits = {
	#'report.account.common': 'report_account',
        #'accounting.report': 'accounting_report',
		#}
    

    _inherit = 'accounting.report'
    _name = 'accounting.report.ma'
    _description = 'Moroccan Trial Balance Report'

    #_columns= {}
	
    
    def get_data(self,data):
       return self.get_lines(self, data)

    def _print_report(self, cr, uid, ids, data, context=None):
        data['form'].update(self.read(cr, uid, ids, ['date_from_cmp',  'debit_credit', 'date_to_cmp',  'fiscalyear_id_cmp', 'period_from_cmp', 'period_to_cmp',  'filter_cmp', 'account_report_id', 'enable_filter', 'label_filter','target_move'], context=context)[0])

	if data['form']['account_report_id'][1] == "BILAN ACTIF":
        	return self.pool['report'].get_action(cr, uid, [], 'account_tax_return.report_financial_marocain', data=data, context=context)

	if data['form']['account_report_id'][1] == "BILAN PASSIF":
        	return self.pool['report'].get_action(cr, uid, [], 'account_tax_return.report_bilan_passif', data=data, context=context)

	if data['form']['account_report_id'][1] == "PASSAGE DU RESULTAT NET COMPTABLE AU RESULTAT NET FISCAL":
        	return self.pool['report'].get_action(cr, uid, [], 'account_tax_return.report_passage_result', data=data, context=context)

	if data['form']['account_report_id'][1] == "TABLEAU DES IMMOBILISATIONS AUTRES QUE FINANCIERES":
        	return self.pool['report'].get_action(cr, uid, [], 'account_tax_return.report_immobilisation', data=data, context=context)

	if data['form']['account_report_id'][1] == "TABLEAU DES AMMORTISSEMENTS":
        	return self.pool['report'].get_action(cr, uid, [], 'account_tax_return.report_ammortissement', data=data, context=context)

	if data['form']['account_report_id'][1] == "TABLEAU DES + OU - VALUES SUR CESSIONS OU RETRAITS D'IMMOBILISATIONS":
        	return self.pool['report'].get_action(cr, uid, [], 'account_tax_return.report_pmv_immobilisation', data=data, context=context)

	if data['form']['account_report_id'][1] == "TABLEAU DES SURETES REELLES DONNEES OU RECUES":
        	return self.pool['report'].get_action(cr, uid, [], 'account_tax_return.report_surete', data=data, context=context)

	if data['form']['account_report_id'][1] == "DETAIL DE LA TAXE SUR VALEUR AJOUTEE":
        	return self.pool['report'].get_action(cr, uid, [], 'account_tax_return.report_tva', data=data, context=context)

	if data['form']['account_report_id'][1] == "ETAT DE REPARTITION DU CAPITAL":
        	return self.pool['report'].get_action(cr, uid, [], 'account_tax_return.report_repartition_capital', data=data, context=context)

	if data['form']['account_report_id'][1] == "TABLEAU DES BIENS EN CREDIT-BAIL":
        	return self.pool['report'].get_action(cr, uid, [], 'account_tax_return.report_credit_bail', data=data, context=context)

	if data['form']['account_report_id'][1] == "COMPTES DE PRODUITS ET CHARGES":

		return self.pool['report'].get_action(cr, uid, [], 'account_tax_return.report_cpc_ma', data=data, context=context)
    
	
    def print_report1(self, cr, uid, ids, data, context=None):
		if context is None:
		    context = {}
		data = self.read(cr, uid, ids)[0]
		#data=self.pool.get('account.test').read(cr,uid,ids)[0]
		datas = {

		         'form': data
		        }

		return { 'type': 'ir.actions.report.xml', 'report_name': 'bilan_maroc', 'datas': datas}
