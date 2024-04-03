#-------------------------------------------------------------------------------
# Name:        SET/CLEAR passw and protect from 25AA160A SPI EEPROM (METRAN-150)
#              with the Buspirate using SPI bitbanging mode
#
# Author:      Alexey K
# Created:     03.04.2024
#-------------------------------------------------------------------------------
import datetime
import os
import sys
import time
from pyBusPirateLite.SPI import *

# EEPROM INSTRUCTION SET
EEP_READ = 0x03
EEP_WRITE = 0x02
EEP_WREN = 0x06
EEP_WRDI = 0x04
EEP_RDSR = 0x05
EEP_WRSR = 0x01

# ADDR PASSWORD IN EEPROM (4 byte)
# 0x4A - 1 digit
# 0x4B - 2 digit
# 0x4C - 3 digit
# 0x4D - 4 digit
# Byte protect
# 0x4E - 0x01 not protect, 0x00 protect
# CRC PASSWORD AND BYTE PROTECT
# 0x4F

# ADDR SERIAL NUMBER
#0x32 0x33 0x34

#Password (1234) SET protect
#0x01 0x02 0x03 0x04 0x00 0xDC
#Password (1234) CLEAR protect
#0x01 0x02 0x03 0x04 0x01 0x82
#  |    |    |    |    |    |
# D1   D2   D3   D4  PRT  CRC

# Save EEPROM password (1234) and clear protect
CLEAR_PROTECT = True

set_protect_pass = b'\x01\x02\x03\x04\x00\xDC'
clr_protect_pass = b'\x01\x02\x03\x04\x01\x82'

spi = None

use_file_log = True
file_log = 'clr_set_psw.log'

def read_eep(address, rx_bytes):
    data = bytes()
    spi.cs = True
    spi.transfer([EEP_READ, address[0], address[1]] )
    for i in range(rx_bytes) :
        data += spi.transfer([0xFF])
    spi.cs = False
    return data

def set_wren():
    spi.cs = True
    spi.transfer([EEP_WREN])
    spi.transfer([0xFF])
    spi.cs = False

def set_wrsr():
    spi.cs = True
    spi.transfer([EEP_WRSR, 0x02])
    spi.transfer([0xFF])
    spi.cs = False

def read_rdsr():
    spi.cs = True
    spi.transfer([EEP_RDSR])
    rx_data = spi.transfer([0xFF])
    spi.cs = False
    return rx_data

def write_eep(address, tx_bytes):
    spi.cs = True
    rx_data = spi.transfer([EEP_WRITE, address[0], address[1]])
    for i in range(0,len(tx_bytes)):
        spi.transfer([tx_bytes[i]])
    spi.cs = False
    return rx_data

def add_log_file(fname, msg, end_l = '\n'):
    if use_file_log :
        if os.path.exists(fname):
            log_f = open(fname, 'a')
        else:
            log_f = open(fname, 'w' )
        try:
            curr_time = datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S.%f') + ':'
            log_f.writelines(str(curr_time)+': '+msg + end_l)
            print(msg)
        finally:
            log_f.close()
    else:
        print(msg)

# Dump and write program
sys.stdout.flush()
add_log_file(file_log,'Connect BusPirate...')
spi = SPI(portname='COM4', speed=115200, timeout=0.1, connect=True)
add_log_file(file_log,'Entering SPI mode...')
spi.enter()
add_log_file(file_log,'Configuring SPI...')
spi.pins = spi.PIN_POWER | spi.PIN_CS
spi.speed = '30kHz'
spi.config = spi.CFG_PUSH_PULL | spi.CFG_CLK_EDGE
add_log_file(file_log,'Reading EEPROM...')

#Read passw
eep_psw_addr = [0x00, 0x4A]
rx_psw_data = read_eep(eep_psw_addr, 4)
str_psw_hex = ''
str_psw_int = ''
for b in rx_psw_data:
    str_psw_int = str_psw_int + str(int(b))
    str_psw_hex = str_psw_hex + str(hex(b)) + ' '

#Read serial number
eep_sn_addr = [0x00, 0x32]
rx_sn_data = read_eep(eep_sn_addr, 3)
str_sn_hex = ''
str_sn_int = str(int.from_bytes(rx_sn_data, 'big'))
for b in rx_sn_data:
    str_sn_hex = str_sn_hex + str(hex(b)) + ' '

add_log_file(file_log,'------------------------------------')
add_log_file(file_log,'Device: ')
add_log_file(file_log,'  Serial number value from EEPROM (hex): ' + str_sn_hex)
add_log_file(file_log,'  Serial number value from EEPROM (int): ' + str_sn_int)
add_log_file(file_log,'  Password value from EEPROM (hex): ' + str_psw_hex)
add_log_file(file_log,'  Password value from EEPROM (int): ' + str_psw_int)
add_log_file(file_log,' Write data in EEPROM: ')

#Write passw and protect
set_wren()
set_wrsr()
read_rdsr()
eep_psw_adr = [0x00, 0x4A]

if CLEAR_PROTECT:
    eep_tx_bytes = clr_protect_pass
    add_log_file(file_log,' Save new password and CLEAR protect: ')
else:
    eep_tx_bytes = set_protect_pass
    add_log_file(file_log,' Save new password and SET protect: ')

write_eep(eep_psw_adr, eep_tx_bytes)
#Read writing passw
eep_psw_addr = [0x00, 0x4A]
rx_psw_data = read_eep(eep_psw_addr, 4)
str_psw_hex = ''
str_psw_int = ''
for b in rx_psw_data:
    str_psw_int = str_psw_int + str(int(b))
    str_psw_hex = str_psw_hex + str(hex(b)) + ' '

add_log_file(file_log,'  Password value from EEPROM (hex): ' + str_psw_hex)
add_log_file(file_log,'  Password value from EEPROM (int): ' + str_psw_int)
add_log_file(file_log,'------------------------------------')
add_log_file(file_log,'Disconnect BusPirate...')
spi.disconnect()


