# Copyright (c) 2023, ss and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry




def stock_entry_update(qty_to_update, bottle_type, unit, stock_entry_type, brand,system_warehouse):
    if len(unit) != 0:
        item_brand = f"{brand}-{bottle_type}{unit}"
    else:
        item_brand = f"{brand}-{bottle_type}"
    if stock_entry_type == "Material Issue":
        warehouse = "s_warehouse"
    else:
        warehouse = "t_warehouse"
    new_stock_entry = frappe.new_doc(
        "Stock Entry")
    new_stock_entry.stock_entry_type = stock_entry_type
    new_stock_entry.append("items", {
        "item_code": item_brand,
        warehouse: system_warehouse,
        "qty": qty_to_update,
        "allow_zero_valuation_rate": 1
    })
    new_stock_entry.insert()
    new_stock_entry.submit()


class Orders(Document):
    def on_submit(self):
        if self.status == "Done": #This  is to check whether the user has selected done status.  
            for item in self.items:
                if item.order_status:
                    item_code = item.items
                    brand = frappe.get_value(
                                    "Item", item_code, "brand")
                    item_packs_ml = item.item_packs_ml  #(30 ml,60ml,90ml) 
                    default_warehouse = frappe.db.get_value('Item Default',{'parent': item_code},'default_warehouse')
                    # frappe.throw(f"{item_bottle_ml}")
                    # # (item quantity is no. of pegs)
                    bottle_name = (frappe.get_doc("Item",f"{brand}-Bottles"))  #(bottle size)
                    item_bottle_ml = bottle_name.bar_bottle_size   #(bottle size)
                    
                    # variable to compare full bottle order
                    full_bottle_order=item_code == f"{brand}-full Bottle"
                    if full_bottle_order:
                        total_order_qty = item_bottle_ml * item_packs_ml
                    else:
                        total_order_qty = item.quantity * item_packs_ml
                    
                    new_loose_bottle_quantity = 0
                    count = 0
                    initial_loose_bottle_stock = 0

                #   item_packs_ml = frappe.get_value("Bin", {"item_code": f"{brand} - {item_packs_ml} ml", "warehouse": warehouse})
                    loose_bottle_stock = frappe.get_value(

                        "Bin", {"item_code": f"{brand}-Loose Bottle", "warehouse": default_warehouse}, "actual_qty")
                    # frappe.throw(f'{loose_bottle_stock}')

                    if loose_bottle_stock:
                        new_loose_bottle_quantity = loose_bottle_stock
                        initial_loose_bottle_stock = loose_bottle_stock
                        # frappe.throw(f'{new_loose_bottle_quantity}')
                    while new_loose_bottle_quantity < total_order_qty:
                        if not loose_bottle_stock:
                            # frappe.throw(f'{loose_bottle_stock}')
                            new_loose_bottle_quantity += item_bottle_ml
                            loose_bottle_stock = item_bottle_ml
                            count += 1
                        else:
                            new_loose_bottle_quantity += item_bottle_ml
                            count +=1
                    if count > 0:
                        bottle_stock = frappe.get_value(
                            "Bin", {"item_code": f"{brand}-Bottles", "warehouse": default_warehouse}, "actual_qty")
                        if bottle_stock >= count:
                            # deduct stock entry from  bottles stock
                                stock_entry_update(
                                    count, "Bottles", "", "Material Issue", brand,default_warehouse)
                                # stock entry for new loose bottle stock
                                stock_entry_update(
                                    new_loose_bottle_quantity - initial_loose_bottle_stock, "Loose Bottle", "", "Material Receipt", brand,default_warehouse)
                                frappe.msgprint(
                                    f"A new stock entry has been created for {item_code} in {default_warehouse} with quantity {new_loose_bottle_quantity}.")
                                # deduct stock entry from loose bottle stock
                                stock_entry_update(
                                    (total_order_qty), "Loose Bottle", "", "Material Issue", brand,default_warehouse)
                                if full_bottle_order:
                                    stock_entry_update(total_order_qty,"full Bottle","","Material Receipt",brand,default_warehouse)
                                else:
                                    # stock entry for no of pegs ordered  # stock entry for ml packs
                                    stock_entry_update(
                                        item.quantity, item_packs_ml, "ml", "Material Receipt", brand,default_warehouse)
                        else:
                            frappe.throw("Not enough stock")

                    else:
                        # deduct stock entry from loose bottle stock
                        stock_entry_update(
                            total_order_qty, "Loose Bottle", "", "Material Issue", brand,default_warehouse)
                        
                        if full_bottle_order:
                                    stock_entry_update(total_order_qty,"full Bottle","","Material Receipt",brand,default_warehouse)
                                    stock_entry_update(total_order_qty,"full Bottle","","Material Issue",brand,default_warehouse)
                        else:
                            # stock entry for no of pegs ordered  # stock entry for ml packs
                            stock_entry_update(
                                item.quantity, item_packs_ml, "ml", "Material Receipt", brand,default_warehouse)
                            stock_entry_update(
                                item.quantity, item_packs_ml, "ml", "Material Issue", brand,default_warehouse)
        else:
            frappe.throw("Status must be 'Done' to submit")      


# new_stock_entry = frappe.new_doc(
                    #     "Stock Entry")
                    # new_stock_entry.stock_entry_type = "Material Receipt"
                    # new_stock_entry.append("items", {
                    #     "item_code": f"{brand} - Loose Bottle",
                    #     "t_warehouse": "Stores - HC",
                    #     "qty": new_loose_bottle_quantity,
                    #     "allow_zero_valuation_rate": 1
                    # })
                    # new_stock_entry.insert()
                    # new_stock_entry.submit()


# new_stock_entry = frappe.new_doc("Stock Entry")
#                 new_stock_entry.stock_entry_type = "Material Issue"
#                 new_stock_entry.append("items", {
#                     "item_code": f"{brand} - Bottles",
#                     "s_warehouse": "Stores - HC",
#                     'qty': count,
#                     "allow_zero_valuation_rate": 1
#                 })
#                 new_stock_entry.insert()
#                 new_stock_entry.submit()
#                 count = 0


# bin_record = frappe.get_doc(
                    #        "Bin", {"item_code": f"{brand} - Loose Bottle", "warehouse": warehouse})

                    # bin_record.actual_qty = new_loose_bottle_quantity
                    # bin_record.save()
