// Copyright (c) 2023, ss and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Product', {
// 	// refresh: function(frm) {

// 	// }
// });

frappe.ui.form.on('Product', {
    brand: function(frm){
		frm.set_query('items', function(){
			console.log('Product',frm.doc)
			return {
				filters : [
					['brand', '=', frm.doc.brand]
				]
			}
		});
	}
});