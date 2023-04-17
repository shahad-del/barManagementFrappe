# Copyright (c) 2023, ss and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = [], []
	return columns, data

# def execute(filters=None):
#     return get_columns(),get_data(filters)
# def get_data(filters):
#     print(f"\n\n\n{filters}\n\n\n")
#     data = frappe.db.sql("""Select item_code,actual_qty,incoming_rate,posting_date from `tabStock Ledger Entry`;""")
#     return data
	
main_bottle_name = frappe.db.get_all("Item", 
filters={
        "disabled": 0,
        # "item_name": ["like", "loose"],
        "inventory_item":1,
    },                          
fields=["name","brand"])
frappe.msgprint(f'{main_bottle_name}')
# loose_bottle_name =frappe.db.sql("""SELECT item_code from `tabItem` where item_code  LIKE '%loose%' """);
# # frappe.msgprint(f'{loose_bottle_name}')
# k = [item[0] for item in loose_bottle_name]
# frappe.msgprint(f'{k}')
for item in main_bottle_name:
   
    # brand = frappe.db.get_value("Item",item.name,"item_code")
    
    brand_name = item.brand
    main_and_loose_bottle = frappe.db.sql("""select item_code,actual_qty  FROM `tabBin` where item_code like %(brand_name)s and actual_qty > 0""",{'brand_name': f'{brand_name}%'});

    frappe.msgprint(f'{main_and_loose_bottle}')  
def get_columns():
    return[
		"Brand:Data:200",
		"Main bottle Qty:Data:200",
		"Loose bottle Qty:Data: 200",
  		"Total Qty:200"
	]