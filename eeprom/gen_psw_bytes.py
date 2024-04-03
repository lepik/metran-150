#-------------------------------------------------------------------------------
# Name:        Generate passw and protect from 25AA160A SPI EEPROM (METRAN-150)
#              with the Buspirate using SPI bitbanging mode
#
# Author:      Alexey K
# Created:     03.04.2024
#-------------------------------------------------------------------------------
import datetime
import os
import sys
import time
from fastcrc import crc8

#Password (1234) SET protect
#0x01 0x02 0x03 0x04 0x00 0xDC
#Password (1234) CLEAR protect
#0x01 0x02 0x03 0x04 0x01 0x82
#  |    |    |    |    |    |
# D1   D2   D3   D4  PRT  CRC

#CRC8 init value
crc_init = 0x2F

def set_passw_protect(passw):
    """ Create setting password protection
        Parameters
        ----------
        passw: Bytes password (4 bytes)

        Returns
        -------
            Bytes containing generate data
    """
    if len(passw) != 4:
        raise ValueError("The password must contain 4 bytes")
    for b in passw:
        if int(b) > 9:
            raise ValueError("The value is not in the range 0-9")
    prot_for_crc = b'\x01'
    prot_end = b'\x00'
    psw_byte = bytes(passw)
    psw_byte_calc = psw_byte + prot_for_crc
    crc = crc8.maxim_dow(psw_byte_calc,crc_init)
    ret = psw_byte + prot_end + crc.to_bytes(1,'big')
    return ret

def clr_passw_protect(passw):
    """ Clear setting password protection
        Parameters
        ----------
        passw: Bytes password (4 bytes)

        Returns
        -------
            Bytes containing generate data
    """
    if len(passw) != 4:
        raise ValueError("The password must contain 4 bytes")
    for b in passw:
        if int(b) > 9:
            raise ValueError("The value is not in the range 0-9")
    prot_for_crc = b'\x00'
    prot_end = b'\x01'
    psw_byte = bytes(passw)
    psw_byte_calc = psw_byte + prot_for_crc
    crc = crc8.maxim_dow(psw_byte_calc,crc_init)
    ret = psw_byte + prot_end + crc.to_bytes(1,'big')
    return ret


####################################################################
# These utilities can be used for the password string in the module clr_set_psw.py
#
#
# Example usage

#Prepare bytes password
bytes_passwd = b'\x01\x02\x03\x04'

# Result include password, protect byte, CRC
protect_psw = set_passw_protect(bytes_passwd)
clear_psw = clr_passw_protect(bytes_passwd)

print('Bytes for set protect password: ' + str(protect_psw))
print('Bytes for clear protect password: ' + str(clear_psw))


