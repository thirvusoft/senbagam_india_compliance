import base64
from datetime import datetime
from io import BytesIO

import pyqrcode
from barcode import Code128
from barcode.writer import ImageWriter

import frappe

from india_compliance.gst_india.constants import STATE_NUMBERS
from india_compliance.gst_india.constants.e_waybill import (
    SUB_SUPPLY_TYPES,
    TRANSPORT_MODES,
    TRANSPORT_TYPES,
)
from india_compliance.gst_india.utils import as_ist


def add_spacing(string, interval):
    """
    Add spaces to string at specified intervals
    (https://stackoverflow.com/a/65979478/4767738)
    """

    string = str(string)
    return " ".join(string[i : i + interval] for i in range(0, len(string), interval))


def get_state(state_number):
    """Get state from State Number"""

    state_number = str(state_number)

    for state, code in STATE_NUMBERS.items():
        if code == state_number:
            return state


def get_sub_supply_type(code):
    return SUB_SUPPLY_TYPES[int(code)]


def get_transport_type(code):
    return TRANSPORT_TYPES[int(code)]


def get_transport_mode(code):
    for transport_mode, _code in TRANSPORT_MODES.items():
        if int(_code) == code:
            return transport_mode


def get_e_waybill_qr_code(e_waybill, gstin, ewaybill_date):
    e_waybill_date = as_ist(ewaybill_date)
    qr_text = "/".join(
        (
            e_waybill,
            gstin,
            datetime.strftime(e_waybill_date, "%d-%m-%Y %H:%M:%S"),
        )
    )
    return get_qr_code(qr_text)


def get_qr_code(qr_text, scale=5):
    return pyqrcode.create(qr_text).png_as_base64_str(scale=scale, quiet_zone=1)


def get_ewaybill_barcode(ewaybill):
    barcode_fp = BytesIO()
    # options = {"font_size": 10}
    Code128(ewaybill, writer=ImageWriter()).write(barcode_fp)
    barcode_base64 = base64.b64encode(barcode_fp.getbuffer()).decode()

    return barcode_base64
