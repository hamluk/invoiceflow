import logging
from invoiceflow.models.invoice import Invoice
from invoiceflow.models.erp_detail import ERPDetails, ERPMatchStatus

logger = logging.getLogger(__name__)

OPEN_PURCHASE_ORDERS = [
    {
        "po_id": "PO-AT-453118",
        "supplier_uid": "ATU61234567",
        "mandant_id": "M-AT-03",
        "amount_gross": 419.20,
        "approver": "joe@kunde-ag.at"
    },
    {
        "po_id": "PO-AT-453201",
        "supplier_uid": "ATU76543210",
        "mandant_id": "M-AT-01",
        "amount_gross": 4116.00,
        "approver": "alice@kunde-ag.at"
    }
]


def _match_by_po_number(invoice: Invoice) -> dict | None:
    for po in OPEN_PURCHASE_ORDERS:
        if po["po_id"] == invoice.po_number:
            logger.info(f"PO match found via PO number: {po['po_id']}")
            return po
    return None


def _match_by_fallback(invoice: Invoice) -> dict | None:
    for po in OPEN_PURCHASE_ORDERS:
        uid_match = po["supplier_uid"] == invoice.supplier_uid
        mandant_match = po["mandant_id"] == invoice.recipient_mandant_id

        if uid_match and mandant_match:
            logger.info(f"PO match found via uuid and mandant: {po['po_id']}")
            return po

    return None


def _match_invoice_with_erp(invoice: Invoice) -> ERPDetails:
    erp_details = ERPDetails()

    po = None
    if invoice.po_number:
        po = _match_by_po_number(invoice)

    if po is None:
        po = _match_by_fallback(invoice)

    if po is None:
        logger.warning(f"No ERP match found for invoice: {invoice.invoice_number}")

        erp_details.status = ERPMatchStatus.NO_MATCH
        erp_details.errors.append(
            "No matching purchase order found in ERP — manual review required."
        )
        return erp_details

    erp_details.status = ERPMatchStatus.MATCH
    erp_details.po_id = po["po_id"]
    erp_details.approver = po["approver"]

    return erp_details


def erp_match(invoice: Invoice) -> ERPDetails:
    return _match_invoice_with_erp(invoice=invoice)