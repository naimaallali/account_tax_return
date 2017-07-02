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

from openerp.osv import fields, osv
#from openerp import models, fields, api
from openerp.report import report_sxw
#from account_balance import account_balance

class account_test(osv.osv_memory):

    #_inherits = {
	#'account.balance': 'account_balance',
        #'account.balance.report': 'account_balance_report',
		#}
    

    #_inherit = 'account.balance.report'
    #_inherit = 'account.balance'
    #_inherit = 'report.account.account.balance'
    _name = 'account.test'
    _description = 'Moroccan Trial Balance Report'
    _columns = {
    'accounts':fields.many2one('account.account', ondelete='cascade'),
    #'anouveau_debit':fields.float('A nouveau debit',required=False),
    #'anouveau_credit':fields.float('A nouveau credit',required=False),
    #'sum_debit':fields.float('debit',required=False),
    #'sum_credit':fields.float('credit',required=False),
		}

    def get_account(self, cr, uid, ids,context=None):
	for j in self.pool.get('account.account').browse(cr,uid,ids,context):
	  res['name']= j['name']
        return res

    
