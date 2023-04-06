# Copyright (c) 2023, ss and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.model.document import Document
from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry

class TestOrders(FrappeTestCase):
	def validate(self):
                for item in self.items:
                       if item.order_status:
                              item_code = item.items
                              frappe.msgprint(item_code)
                              brand = frappe.get_value(
                                  "Item", item_code, "brand")
                              item_packs_ml = item.item_packs_ml  #(30 ml,60ml,90ml)
                              item_bottle_ml = item.item_bottle_ml  #(bottle size)
                            #   total_order_qty = item.quantity * item_packs_ml     #(item quantity is no. of pegs)
                              warehouse = "Stores - HC"
                              loose_bottle_stock = frappe.get_value(
                           "Bin", {"item_code": f"{brand} - Loose Bottle", "warehouse": warehouse})
                              item_packs_ml = frappe.get_value("Bin", {"item_code": f"{brand} - {item_packs_ml} ml", "warehouse": warehouse})
                              if not item_packs_ml:
                                       new_stock_entry = frappe.new_doc(
                                           "Stock Entry")
                                       new_stock_entry.stock_entry_type = "Material Receipt"
                                       new_stock_entry.append("Items",{
                                           "item_code" : item_code,
                                           "t_warehouse": "Stores - HC",
                                           "qty" : item.quantity
                                       })
                                       new_stock_entry.insert()
                                       frappe.msgprint(f"A new stock entry has been created for {item_code} in {warehouse} with quantity 1.")
                                       if not loose_bottle_stock:
                                           
                                       

