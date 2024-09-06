/* global html2canvas */

/*
Copyright (C) 2024-Today GRAP (http://www.grap.coop)
@author: Sylvain LE GAL (https://twitter.com/legalsylvain)
License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
*/


odoo.define('pos_odoo_pos_driver.devices', function (require) {
    "use strict";

    var devices = require('point_of_sale.devices');

    var ProxyDeviceSuper = devices.ProxyDevice;

    devices.ProxyDevice = devices.ProxyDevice.extend({

        print_receipt: function(receipt){
            console.log("OVERLOADED");
            var self = this;

            console.log(self);
            if (!self.pos.config.use_odoo_pos_driver) {
                return ProxyDeviceSuper.prototype.print_receipt.call(this, receipt);
            }

            if(receipt){
                this.receipt_queue.push(receipt);
            }

            function send_printing_job(){
                if (self.receipt_queue.length > 0){
                    var r = self.receipt_queue.shift();
                    var image = self.htmlToImg(receipt);
                    self.message(
                        'default_printer_action',
                        {
                            data: {
                                action: 'print_receipt',
                                receipt: image,
                            }
                        },
                        { timeout: 5000 }
                    ).then(function(){
                            send_printing_job();
                        },function(error){
                            if (error) {
                                self.pos.gui.show_popup('error-traceback',{
                                    'title': _t('Odoo-Pos-Driver: Printing Error: ') + error.data.message,
                                    'body':  error.data.debug,
                                });
                                return;
                            }
                            self.receipt_queue.unshift(r);
                        });
                }
            }
            send_printing_job();
        },


        /**
         * COPY and ADAPTATION of
         * odoo/16.0/addons/point_of_sale/static/src/js/printers.js
         *
         * Renders the html as an image to print it
         * @param {String} receipt: The receipt to be printed, in HTML
         */
        htmlToImg: function (receipt) {
            console.log("htmlToImg");
/*            $('.pos-receipt-print').html(receipt);
            this.receipt = $('.pos-receipt-print>.pos-receipt');
            // Odoo RTL support automatically flip left into right but html2canvas
            // won't work as expected if the receipt is aligned to the right of the
            // screen so we need to flip it back.
            this.receipt.parent().css({ left: 0, right: 'auto' });
            return html2canvas(this.receipt[0], {
                height: Math.ceil(this.receipt.outerHeight() + this.receipt.offset().top),
                width: Math.ceil(this.receipt.outerWidth() + 2 * this.receipt.offset().left),
                scale: 1,
            }).then(canvas => {
                $('.pos-receipt-print').empty();
                return this.process_canvas(canvas);
            });*/
        },
    })
})
