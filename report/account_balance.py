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

from openerp.osv import osv
from openerp.report import report_sxw
from common_report_header import common_report_header
from datetime import date
from datetime import date,datetime, timedelta

class account_balance(report_sxw.rml_parse, common_report_header):


    def __init__(self, cr, uid,name, context=None):
        super(account_balance, self).__init__(cr, uid, name, context=context)
        self.sum_debit = 0.00
        self.sum_credit = 0.00
        self.date_lst = []
        self.date_lst_string = ''
        self.result_acc = []
        self.result_acc1 = []
        self.result = []
        self.localcontext.update({
            'time': time,
            'grp_lines': self.grp_lines,
            'lines': self.lines,
            'get_lines': self.get_lines,
            'get_lines_child': self.get_lines_child,
            'anv_lines': self.anv_lines,
            'sum_debit': self._sum_debit,
            'sum_credit': self._sum_credit,
            'get_fiscalyear':self._get_fiscalyear,
            'get_filter': self._get_filter,
            'get_start_period': self.get_start_period,
            'get_end_period': self.get_end_period ,
            'get_account': self._get_account,
            'get_journal': self._get_journal,
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
        return super(account_balance, self).set_context(objects, data, new_ids, report_type=report_type)

    def lines(self, form, ids=None, done=None):
        def _process_child(accounts, disp_acc, parent):
                account_rec = [acct for acct in accounts if acct['id']==parent][0]
                currency_obj = self.pool.get('res.currency')
                acc_id = self.pool.get('account.account').browse(self.cr, self.uid, account_rec['id'])
                currency = acc_id.currency_id and acc_id.currency_id or acc_id.company_id.currency_id
                res = {
                    'id': account_rec['id'],
                    'type': account_rec['type'],
                    'code': account_rec['code'],
                    'name': account_rec['name'],
                    'level': account_rec['level'],
                    'debit': account_rec['debit'],
                    'credit': account_rec['credit'],
                    'balance': account_rec['balance'],
                    'parent_id': account_rec['parent_id'],
                    'bal_type': '',
                }
                self.sum_debit += account_rec['debit']
                self.sum_credit += account_rec['credit']
                if disp_acc == 'movement':
                    if not currency_obj.is_zero(self.cr, self.uid, currency, res['credit']) or not currency_obj.is_zero(self.cr, self.uid, currency, res['debit']) or not currency_obj.is_zero(self.cr, self.uid, currency, res['balance']):
                        self.result_acc.append(res)
                elif disp_acc == 'not_zero':
                    if not currency_obj.is_zero(self.cr, self.uid, currency, res['balance']):
                        self.result_acc.append(res)
                else:
                    self.result_acc.append(res)
                if account_rec['child_id']:
                    for child in account_rec['child_id']:
                        _process_child(accounts,disp_acc,child)


        def _process_child1(accounts, disp_acc, parent):
                account_rec = [acct for acct in accounts if acct['id']==parent][0]
                currency_obj = self.pool.get('res.currency')
                acc_id = self.pool.get('account.account').browse(self.cr, self.uid, account_rec['id'])
                currency = acc_id.currency_id and acc_id.currency_id or acc_id.company_id.currency_id
                res = {
                    'id': account_rec['id'],
                    'type': account_rec['type'],
                    'code': account_rec['code'],
                    'name': account_rec['name'],
                    'level': account_rec['level'],
                    'debit': account_rec['debit'],
                    'credit': account_rec['credit'],
                    'balance': account_rec['balance'],
                    'parent_id': account_rec['parent_id'],
                    'bal_type': '',
                }
                self.sum_debit += account_rec['debit']
                self.sum_credit += account_rec['credit']
                if disp_acc == 'movement':
                    if not currency_obj.is_zero(self.cr, self.uid, currency, res['credit']) or not currency_obj.is_zero(self.cr, self.uid, currency, res['debit']) or not currency_obj.is_zero(self.cr, self.uid, currency, res['balance']):
                        self.result_acc1.append(res)
                elif disp_acc == 'not_zero':
                    if not currency_obj.is_zero(self.cr, self.uid, currency, res['balance']):
                        self.result_acc1.append(res)
                else:
                    self.result_acc1.append(res)
                if account_rec['child_id']:
                    for child in account_rec['child_id']:
                        _process_child(accounts,disp_acc,child)

        obj_account = self.pool.get('account.account')
        if not ids:
            ids = self.ids
        if not ids:
            return []
        if not done:
            done={}

        ctx = self.context.copy()
        ctx1 = self.context.copy()
        ctx['fiscalyear'] = form['fiscalyear_id']
        ctx1['fiscalyear'] = form['fiscalyear_id']+1
        if form['filter'] == 'filter_period':
            ctx['period_from'] = form['period_from']
            ctx['period_to'] = form['period_to']
            ctx1['period_from'] = form['period_from']
            ctx1['period_to'] = form['period_to']
        elif form['filter'] == 'filter_date':
            ctx['date_from'] = form['date_from']
            ctx['date_to'] =  form['date_to']
            ctx1['date_from'] = form['date_from']
            ctx1['date_to'] =  form['date_to']
        ctx['state'] = form['target_move']
        ctx1['state'] = form['target_move']
        parents = ids
        child_ids = obj_account._get_children_and_consol(self.cr, self.uid, ids, ctx)
        if child_ids:
            ids = child_ids
        accounts = obj_account.read(self.cr, self.uid, ids, ['type','code','name','debit','credit','balance','parent_id','level','child_id'], ctx)
        accounts1 = obj_account.read(self.cr, self.uid, ids, ['type','code','name','debit','credit','balance','parent_id','level','child_id'], ctx1)

        for parent in parents:
                if parent in done:
                    continue
                done[parent] = 1
                _process_child(accounts,form['display_account'],parent)
                _process_child1(accounts1,form['display_account'],parent)
        self.result.append(self.result_acc)
        self.result.append(self.result_acc1)
        return self.result

    def get_lines(self, data):
        lines = []
        account_obj = self.pool.get('account.account')
        fisc_start = self.pool.get('account.fiscalyear').browse(self.cr, self.uid, data['form']['fiscalyear_id'],context=data['form']['used_context']).date_start
        date_start=datetime.strptime(fisc_start,"%Y-%m-%d")
        d = date_start - timedelta(days=1)
        
        domain = [('date_stop', '=', d)]
        prev_fisc=self.pool.get('account.fiscalyear').search(self.cr, self.uid, domain, limit=1)

        fisc_stop = self.pool.get('account.fiscalyear').browse(self.cr, self.uid,prev_fisc,context=data['form']['used_context']).date_stop
        
        print('***************************',data['form']['used_context'].get('fiscalyear_id'))
        ids1=account_obj.search(self.cr, self.uid, [('name', '=', "COMPTES DE FINANCEMENT PERMANENT")], context=data['form']['used_context'])
        ids2=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids1)], context=data['form']['used_context'])

        data['form']['used_context'].update({'fiscalyear_id':prev_fisc})
        ids3=account_obj.search(self.cr, self.uid, [('name', '=', "COMPTES DE FINANCEMENT PERMANENT")], context=data['form']['used_context'])
        ids4=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids3)], context=data['form']['used_context'])
        

        for cls in account_obj.browse(self.cr, self.uid, ids2):
            
            vals = {
                    'code': cls.code,
                    'name': cls.name,
                    'debit': cls.debit,
                    'credit': cls.credit,
                    'balance': cls.balance,
                        }
            
            lines.append(vals)
        
       
        return lines

    def get_lines_child(self, data,cl):
        lines = []
        account_obj = self.pool.get('account.account')
        ids1=account_obj.search(self.cr, self.uid, [('name', '=', cl)], context=data['form']['used_context'])
        ids_child=account_obj.search(self.cr, self.uid, [('parent_id', '=', ids1)], context=data['form']['used_context'])


        for cls in account_obj.browse(self.cr, self.uid, ids_child):
                vals = {
                    'code': cls.code,
                    'name': cls.name,
                    'debit': cls.debit,
                    'credit': cls.credit,
                    'balance': cls.balance,
                   
                            }
                lines.append(vals)
   
        
        return lines




    def anv_lines(self, form, ids=None, done=None):
        def _process_child(accounts, disp_acc, parent):
                account_rec = [acct for acct in accounts if acct['id']==parent][0]
                currency_obj = self.pool.get('res.currency')
                acc_id = self.pool.get('account.account').browse(self.cr, self.uid, account_rec['id'])
                currency = acc_id.currency_id and acc_id.currency_id or acc_id.company_id.currency_id
                res1 = {
                    'id': account_rec['id'],
                    'type': account_rec['type'],
                    'code': account_rec['code'],
                    'name': account_rec['name'],
                    'level': account_rec['level'],
                    'debit': account_rec['debit'],
                    'credit': account_rec['credit'],
                    'balance': account_rec['balance'],
                    'parent_id': account_rec['parent_id'],
                    'bal_type': '',
                }
                self.sum_debit += account_rec['debit']
                self.sum_credit += account_rec['credit']
                if disp_acc == 'movement':
                    if not currency_obj.is_zero(self.cr, self.uid, currency, res1['credit']) or not currency_obj.is_zero(self.cr, self.uid, currency, res1['debit']) or not currency_obj.is_zero(self.cr, self.uid, currency, res1['balance']):
                        self.result_acc1.append(res1)
                elif disp_acc == 'not_zero':
                    if not currency_obj.is_zero(self.cr, self.uid, currency, res1['balance']):
                        self.result_acc1.append(res1)
                else:
                    self.result_acc1.append(res1)
                if account_rec['child_id']:
                    for child in account_rec['child_id']:
                        _process_child(accounts,disp_acc,child)

        obj_account = self.pool.get('account.account')
        if not ids:
            ids = self.ids
        if not ids:
            return []
        if not done:
            done={}

        ctx = self.context.copy()
        fiscalyear_obj=self.pool.get('account.fiscalyear')
        #debut=form['fiscalyear_id'].date_start
        #prev_year=debut.year-1
        #db=time.strptime(debut,"%d/%m/%y")
        
        #now=time.strftime("%d/%m/%y",time.localtime())
        #prev_fiscalyear = fiscalyear_obj.search(self.cr, self.uid, [('date_start','=',date(debut.year + 1, debut.month, debut.day))])
        ctx['fiscalyear'] = form['fiscalyear_id']
        if form['filter'] == 'filter_period':
            ctx['period_from'] = form['period_from']
            ctx['period_to'] = form['period_to']
        elif form['filter'] == 'filter_date':
            ctx['date_from'] = form['date_from']
            ctx['date_to'] =  form['date_to']
        ctx['state'] = form['target_move']
        parents = ids
        child_ids = obj_account._get_children_and_consol(self.cr, self.uid, ids, ctx)
        if child_ids:
            ids = child_ids
        accounts = obj_account.read(self.cr, self.uid, ids, ['type','code','name','debit','credit','balance','parent_id','level','child_id'], ctx)

        for parent in parents:
                if parent in done:
                    continue
                done[parent] = 1
                _process_child(accounts,form['display_account'],parent)
        return self.result_acc1

    def grp_lines(self, form, ids=None, done=None):
        l1=self.lines(form, ids, done)
        l2=self.anv_lines(form, ids, done)
        result.append(l1)
        result.append(l2)
        print('***************debit************',result[0]['debit'])
        #print('***************debit2************',l2[0]['anv_debit'])
        return result



class report_trialbalance_ma(osv.AbstractModel):
    _name = 'report.account_tax_return.report_trialbalance_ma'
    _inherit = 'report.abstract_report'
    _template = 'account_tax_return.report_trialbalance_ma'
    _wrapped_report_class = account_balance

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
