// Copyright (c) 2016, igrekus and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["DC Product Filter Status"] = {
	"filters": [
	],
	formatter: frappe.dc_plc.utils.status_link_formatter,
};
