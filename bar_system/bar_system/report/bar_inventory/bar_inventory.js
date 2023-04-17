// Copyright (c) 2023, ss and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Bar Inventory"] = {
	"filters": [
		{
		"fieldname":"item_code",
		"label": __("Item name"),
		"fieldtype": "Link",
		"options":"Item",
		// "width": 100,
		// "reqd": 0,
		},
		{
		"fieldname":"brand",
		"label":__("Brand"),
		"fieldtype":"Link",
		"options":"Brand",
		},
		{
			"fieldname":"from_date",
			"label":__("From Date"),
			"fieldtype":"Date",
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname":"end_date",
			"label":__("To Date"),
			"fieldtype":"Date",
			"default":frappe.datetime.get_today(),
		}
	]
};
