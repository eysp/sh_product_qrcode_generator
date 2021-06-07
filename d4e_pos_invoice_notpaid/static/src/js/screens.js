odoo.define('d4e_pos_invoice_notpaid.screens', function (require) {
"use strict";

const core = require('web.core');
const PaymentScreen = require('point_of_sale.PaymentScreen');
const Registries = require('point_of_sale.Registries');
const models = require('point_of_sale.models');
const QWeb = core.qweb;
const _t = core._t;

models.load_fields('pos.payment.method', 'unpaid_invoice');

const includePaymentScreen = PaymentScreen => class extends PaymentScreen {
    constructor() {
        super(...arguments);
    }
    async validateOrder(isForceValidate) {
        var self = this;
        var order = self.currentOrder;
        if (await self._isOrderValid(isForceValidate)) {
            var unpaid_invoice = false;
            for (let line of self.paymentLines) {
                if (line.payment_method && line.payment_method.unpaid_invoice === true) {
                    unpaid_invoice = true;
                    break;
                }
            }
            if (unpaid_invoice && !order.get_client()) {
                return self.showPopup('ErrorPopup', {
                    title: _t('Error'),
                    body: _t('Missing customer!'),
                });
            } else {
                return await super.validateOrder(isForceValidate);
            }
        }
    }
}

Registries.Component.extend(PaymentScreen, includePaymentScreen);

return PaymentScreen;
});
