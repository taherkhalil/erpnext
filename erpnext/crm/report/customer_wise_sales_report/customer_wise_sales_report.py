# Copyright (c) 2013, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from operator import itemgetter

def execute(filters=None):
	columns, data = [], []

	columns = get_columns()
	data = get_customer_details(filters)
	data.sort(key=itemgetter(1), reverse=True)
	return columns, data


def get_columns():
	return [
		"Customer:Link/Customer:100",
		"Total Paid:Float:100",
		"Total Unpaid:Float:100"
	]

def get_customer_details(filters):
	result = []
	data = []
	from_date = filters.get("from_date")
	to_date = filters.get("to_date")
	for customer in frappe.db.get_all("Customer", as_list=True):
		billing = frappe.db.sql("""
			select sum(grand_total)
			from `tabSales Invoice`
			where customer='{0}' and docstatus=1 and posting_date between '{1}' and '{2}'
		""".format(customer[0], from_date, to_date), debug=1)[0][0] or 0.0
		print(billing)
		
		total_unpaid = frappe.db.sql("""
			select sum(debit_in_account_currency) - sum(credit_in_account_currency)
			from `tabGL Entry`
			where party_type = 'Customer' and party='{0}'""".format(customer[0]), debug=1)[0][0] or 0.0
		print(total_unpaid)

		result.append([customer[0], billing, total_unpaid])

	return result			

