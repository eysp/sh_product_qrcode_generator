# -*- coding: utf-8 -*-
import logging

import psycopg2

from odoo import api, fields, models, tools, _

_logger = logging.getLogger(__name__)


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.model
    def _process_order(self, order, draft, existing_order):
        order = order['data']
        pos_session = self.env['pos.session'].browse(order['pos_session_id'])
        if pos_session.state == 'closing_control' or pos_session.state == 'closed':
            order['pos_session_id'] = self._get_valid_session(order).id

        if not existing_order:
            pos_order = self.create(self._order_fields(order))
        else:
            pos_order = existing_order
            pos_order.lines.unlink()
            order['user_id'] = pos_order.user_id.id
            pos_order.write(self._order_fields(order))

        self._process_payment_lines(order, pos_order, pos_session, draft)

        if not draft:
            try:
                pos_order.action_pos_order_paid()
            except psycopg2.DatabaseError:
                raise
            except Exception as e:
                _logger.error('Could not fully process the POS Order: %s', tools.ustr(e))

        unpaid_invoice = False
        for line in pos_order.payment_ids:
            # if line.payment_method_id.name == 'Unpaid invoice':
            if line.payment_method_id.unpaid_invoice:
                unpaid_invoice = True

        if (pos_order.to_invoice or unpaid_invoice) and pos_order.state == 'paid':
            pos_order.action_pos_order_invoice()
        return pos_order.id
