# Copyright (c) 2023, ss and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from erpnext.stock.doctype.stock_entry.stock_entry import StockEntry


import frappe
from frappe.model.document import Document


class Orders(Document):
	def on_submit(self):
                available_stock = 0
                for item in self.items:
                                        if item.order_status == 'True' or self.status == "Done":
                                                item_code = item.items
                                                order_quantity = int(item.quantity)
                                                item_doc = frappe.get_doc("Item",item_code)
                                                brand = item_doc.brand
                                                main_bottle_itemcode = frappe.db.get_value(
                                                        "Item",
                                                        filters={
                                                                "brand": brand,
                                                                "inventory_item":1
                                                        },
                                                        fieldname="item_code"
                                                )
                                                item_main = frappe.get_doc("Item", main_bottle_itemcode)
                                                item_bottle_ml = item_main.bar_bottle_size
                                                item_packs_ml = int(item_doc.bar_bottle_size)
                                               
                                                total_order_qty = item_packs_ml * order_quantity
                                                # frappe.throw(f'{total_order_qty}')
                                                count = 0
                                                new_loose_bottle_quantity = 0
                                                initial_loose_bottle_stock = 0
                                                default_warehouse = frappe.db.get_value('Item Default', {'parent': item_code}, 'default_warehouse')
                                                bottle_stock = frappe.get_value("Bin", {"item_code": main_bottle_itemcode, "warehouse": default_warehouse}, "actual_qty")
                                                loose_bottle_item = frappe.get_value("Item", {"item_code": f"{brand}- Loose Bottle"})

                                                if not loose_bottle_item:
                                                        # create loose bottle item
                                                        new_item = frappe.new_doc('Item')
                                                        new_item.item_code = f"{brand}- Loose Bottle"
                                                        new_item.item_name = f"{brand}- Loose Bottle"
                                                        new_item.item_group = 'consumable'
                                                        new_item.stock_uom = 'Millilitre'
                                                        new_item.is_stock_item = 1
                                                        new_item.has_variants = 0
                                                        new_item.description = 'This is a loose bottle item'
                                                        new_item.append('item_defaults', {'default_warehouse': default_warehouse})
                                                        new_item.insert()

                                                #checks stock of loose item bottle
                                                loose_bottle_stock = frappe.get_value("Bin", {"item_code": f"{brand}- Loose Bottle", "warehouse": default_warehouse}, "actual_qty")
                                                
                                                if loose_bottle_stock:
                                                        new_loose_bottle_quantity = loose_bottle_stock
                                                        initial_loose_bottle_stock = loose_bottle_stock

                                                while new_loose_bottle_quantity < total_order_qty:
                                                        if not loose_bottle_stock:
                                                                new_loose_bottle_quantity = item_bottle_ml
                                                                loose_bottle_stock = item_bottle_ml
                                                                count += 1
                                                        else:
                                                                new_loose_bottle_quantity += item_bottle_ml
                                                                count += 1
                                                # frappe.throw(f'{new_loose_bottle_quantity}')
                                                if available_stock == 0:
                                                        available_stock = f"{int(bottle_stock)} bottle and {initial_loose_bottle_stock} ml."                                                
                                                if count > 0:        
                                                        if bottle_stock >= count:
                                                                #reduce stock from Main Bottel
                                                                stock_entry_update(count, main_bottle_itemcode,"Material Issue",default_warehouse)

                                                                #update stock of Losse bootel
                                                                stock_entry_update(new_loose_bottle_quantity - initial_loose_bottle_stock,f"{brand}- Loose Bottle","Material Receipt",default_warehouse)

                                                                # reduce stock of Loose bottel
                                                                stock_entry_update(total_order_qty,f"{brand}- Loose Bottle","Material Issue",default_warehouse)

                                                                #stock entry for item packs
                                                                stock_entry_update(order_quantity,item_code,"Material Receipt",default_warehouse)

                                                                #stock issue for item packs
                                                                stock_entry_update(order_quantity, item_code,"Material Issue",default_warehouse)
                                                        else:
                                                                frappe.throw(f"Not enough stock for {brand} - Bottle.Available stock is {available_stock}")
                                                else:
                                                        #reduce the stock frome loosebottel 
                                                        stock_entry_update(total_order_qty,f"{brand}- Loose Bottle","Material Issue",default_warehouse)

                                                        #stock entry for item packs
                                                        stock_entry_update(order_quantity, item_code,"Material Receipt",default_warehouse)

                                                        #stock issue for item packs
                                                        stock_entry_update(order_quantity, item_code,"Material Issue",default_warehouse)
                                        else:
                                                frappe.throw("please confirm your order.")                                        
                                        

                                
def stock_entry_update(qty_to_update,bottle_type,stock_entry_type,default_warehouse):
                    if stock_entry_type == "Material Issue":
                        warehouse = "s_warehouse"
                    else:
                        warehouse = "t_warehouse"
                    new_stock_entry = frappe.new_doc(
                                "Stock Entry")
                    new_stock_entry.stock_entry_type =  stock_entry_type
                    new_stock_entry.append("items", {
                        "item_code": bottle_type,
                        warehouse: default_warehouse ,
                        "qty": qty_to_update,
                        "allow_zero_valuation_rate": 1
                    })
                    new_stock_entry.insert()
                    new_stock_entry.submit()

















































# def stock_entry_update(qty_to_update, main_bottle_itemcode, stock_entry_type, brand,system_warehouse):
#     if stock_entry_type == "Material Issue":
#         warehouse = "s_warehouse"
#     else:
#         warehouse = "t_warehouse"
#     new_stock_entry = frappe.new_doc(
#         "Stock Entry")
#     new_stock_entry.stock_entry_type = stock_entry_type
#     new_stock_entry.append("items", {
#         "item_code": main_bottle_itemcode,
#         warehouse: system_warehouse,
#         "qty": qty_to_update,
#         "allow_zero_valuation_rate": 1
#     })
#     new_stock_entry.insert()
#     new_stock_entry.submit()


# class Orders(Document):
#     def on_submit(self):
#         if self.status == "Done": #This  is to check whether the user has selected done status.  
#             for item in self.items:
#                 if item.order_status:
#                     item_code = item.items
#                     item_doc = frappe.get_doc("Item",item_code)
#                     brand = item_doc.brand
#                     default_warehouse = frappe.db.get_value('Item Default',{'parent': item_code},'default_warehouse')
                    
                    
#                     main_bottle_itemcode = frappe.db.get_value("Item",filters={'brand':brand,
#                                                                             'opening_stock':(">",0)},fieldname ="item_code")
#                     # frappe.throw(f'{main_bottle_itemcode}')
                    
#                     bottle_name = (frappe.get_doc('Item',item_code, main_bottle_itemcode))
#                     # frappe.throw(f'{bottle_name}')
                    
#                     bottle_name_size_ml = bottle_name.bar_bottle_size #bottle size
#                     # frappe.throw(f'{bottle_name_size_ml}')
                    
#                     item_packs_ml = item_doc.pack_size #pack size 30, 60 80
#                     # frappe.throw(f'{item_packs_ml}')
#                      # (item quantity is no. of pegs)
                     
                    
#                     total_order_qty = item.quantity * item_packs_ml
#                     new_loose_bottle_quantity = 0
#                     count = 0
#                     initial_loose_bottle_stock = 0
#                     loose_bottle_stock = frappe.get_value(
#                         "Bin", {"item_code": f"{brand}-Loose Bottle", "warehouse": default_warehouse}, "actual_qty")
                    
#                     loose_bottle_item = frappe.get_value("Item", {"item_code": f"{brand}-Loose Bottle"})
#                     # frappe.throw(f'{loose_bottle_item}')
#                     if not loose_bottle_item:
#                         # create loose bottle item
#                         new_item = frappe.new_doc('Item')
#                         new_item.item_code = f"{brand}-Loose Bottle"
#                         new_item.item_name = f"{brand}-Loose Bottle"
#                         new_item.item_group = 'Consumable'
#                         new_item.stock_uom = 'Millilitre'
#                         new_item.is_stock_item = 1
#                         new_item.has_variants = 0
#                         new_item.description = 'This is a loose bottle item'
#                         new_item.append('item_defaults', {'default_warehouse': default_warehouse})
#                         new_item.insert()
                    
#                     if loose_bottle_stock:
#                         new_loose_bottle_quantity = loose_bottle_stock
#                         initial_loose_bottle_stock = loose_bottle_stock
#                         # frappe.throw(f'{new_loose_bottle_quantity}')
                        
#                     while new_loose_bottle_quantity < total_order_qty:
#                         if not loose_bottle_stock:
#                             # frappe.throw(f'{loose_bottle_stock}')
#                             new_loose_bottle_quantity = bottle_name_size_ml
#                             loose_bottle_stock = bottle_name_size_ml
#                             count += 1
#                         else:
#                             new_loose_bottle_quantity += item_packs_ml
#                             count +=1
#                     # frappe.throw(f'{loose_bottle_stock}')       
#                     if count > 0:
#                         bottle_stock = frappe.get_value(
#                             "Bin", {"item_code": main_bottle_itemcode, "warehouse": default_warehouse}, "actual_qty")
#                         # frappe.throw(f'{bottle_stock}')
#                         if bottle_stock >= count:
#                             # deduct stock entry from  bottles stock
#                                 stock_entry_update(
#                                     count, main_bottle_itemcode, "Material Issue", brand,default_warehouse)
#                                 # stock entry for new loose bottle stock
#                                 stock_entry_update(
#                                     new_loose_bottle_quantity - initial_loose_bottle_stock, f"{brand}-Loose Bottle","Material Receipt", brand,default_warehouse)
#                                 frappe.msgprint(
#                                     f"A new stock entry has been created for {item_code} in {default_warehouse} with quantity {new_loose_bottle_quantity}.")
#                                 # deduct stock entry from loose bottle stock
#                                 stock_entry_update(
#                                     (total_order_qty), f"{brand}-Loose Bottle","Material Issue", brand,default_warehouse)
#                                 # stcok entry for item packs
#                                 stock_entry_update(
#                                         item.quantity, item_code, "Material Receipt", brand,default_warehouse)
#                                 #deduct  item packs
#                                 stock_entry_update(item.quantity, item_code, "Material Issue", brand,default_warehouse)
#                         else:
#                             frappe.throw("Not enough stock")

#                     else:
#                         # stock entry for new loose bottle stock
#                         stock_entry_update(
#                             new_loose_bottle_quantity - initial_loose_bottle_stock, f"{brand}-Loose Bottle","Material Receipt", brand,default_warehouse)
#                         # deduct stock entry from loose bottle stock
#                         stock_entry_update(
#                             total_order_qty, f"{brand}-Loose Bottle","Material Issue", brand,default_warehouse)
#                         #stock demand from  bottle stock
#                         stock_entry_update(total_order_qty,main_bottle_itemcode,"Material Receipt",brand,default_warehouse)
#                          # deduct stock entry from  bottles stock  
#                         stock_entry_update(total_order_qty,main_bottle_itemcode,"Material Issue",brand,default_warehouse)
#                         # stock entry for no of pegs ordered  # stock entry for ml packs
                    
#                         stock_entry_update(
#                             item.quantity, item_code,"Material Receipt", brand,default_warehouse)
#                         stock_entry_update(
#                             item.quantity, item_code,"Material Issue", brand,default_warehouse)
#         else:
#             frappe.throw("Status must be 'Done' to submit")      


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
# bottle_itemcode = frappe.db.sql_list(    #to know whether the item is stock item or not
                    #     """
                    #     SELECT item_code 
                    #     FROM `tabItem`
                    #     WHERE brand = %s AND opening_stock > 0
                    #     """,
                    #     (brand)
                    # )
                    
# brand = frappe.get_value(
                    #                 "Item", item_code, "brand")
                    # frappe.throw(f'{brand}')