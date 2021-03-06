# Copyright (c) 2013, igrekus and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe

from frappe import _

from dc_plc.custom.utils import add_translation, add_completeness, add_query_relevance, add_newline
from dc_plc.controllers.stats_query import get_dept_head_stats, get_developers_for_product, get_consultants_for_product


def execute(filters=None):
	if not filters:
		filters = dict()
	return get_columns(), get_data(filters)


def get_columns():
	return [
		"ID:Link/DC_PLC_Product_Summary",
		_("Relevance"),
		_("Progress"),
		_("Lifecycle step"),
		_("RnD Title"),
		_("Consultants"),
		_("Developers"),
		_("Function"),
		_("Description") + ":Data:300",
		_("External number"),
		_("Internal number")
	]


def get_data(filters):
	def add_devs_and_cons(row):
		row[3] = cons.get(row[0], '').replace(',', '<br>')
		row[4] = devs.get(row[0], '').replace(',', '<br>')
		return row

	devs = get_developers_for_product()
	cons = get_consultants_for_product()

	# TODO use frappe API to determine perms
	has_perms = 'DC_PLC_MMIC_Dept_Head' in frappe.get_roles(frappe.session.user)

	res = get_dept_head_stats(filters)
	res = [add_devs_and_cons(row) for row in res]
	res = [add_completeness(row, [1, 2, 4, 5]) for row in res]
	res = [add_query_relevance(row, has_perms) for row in res]
	res = [add_newline(row) for row in res]

	# TODO calc stats by appointed fields
	return res
