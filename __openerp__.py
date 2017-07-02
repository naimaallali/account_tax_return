#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

{
    'name': 'tax return',
    'version': '1.0',
    'category': 'Accounting & Finance',
    'description': """
Morrocan Tax Return Management.
====================================

Tax Return module that covers:
--------------------------------------------
    * General Accounting
    * Morrocan Balance
    * Morrocan Balance Sheet
    * Morrocan state synthesis
    * Tax Return management
    * Customer and Supplier Invoices
    * Bank statements
    * Reconciliation process by partner

Creates a dashboard for accountants that includes:
--------------------------------------------------
    * List of Customer Invoices to Approve
    * Company Analysis
    * Graph of Treasury

Processes like maintaining general ledgers are done through the defined Financial Journals (entry move line or grouping is maintained through a journal) 
for a particular financial year and for preparation of vouchers there is a module named account_voucher.
    """,
    'author': 'OpenERP SA',
    'website': 'https://www.odoo.com/page/billing',
    'depends': [
        'base_setup',
        'account',
        'account_accountant',
        'account_payment',
        'account_bank_statement_extensions',
        'account_budget',
        'report',
        'board', 
        'edi',
        
    ],
    'data': [
        'account_menuitem_ma.xml',
        'wizard/account_report_account_balance_ma_view.xml',
        'wizard/account_financial_view.xml',
        'views/report_trialbalance_ma.xml',
        'views/report_financial_ma.xml',
        'views/report_financial_marocain.xml',
        'views/report_bilan_passif.xml',
        'views/report_passage_result.xml',
        'views/report_immobilisation.xml',
        'views/report_ammortissement.xml',
        'views/report_pmv_immobilisation.xml',
        'views/report_surete.xml',
        'views/report_tva.xml',
        'views/report_repartition_capital.xml',
        'views/report_credit_bail.xml',
        'views/report_cpc_ma.xml',
    ],
    'test': [
        '',
    ],
    'demo': ['account_demo.xml'],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
