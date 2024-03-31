#-------------------------------------------------------------------------------
# Name:        Dump passw from 25AA160A SPI EEPROM (METRAN-150)
#              with the Buspirate using SPI bitbanging mode
#
# Author:      Alexey K
# Created:     29.03.2024
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

spi = None

use_file_log = True
file_log = 'dump_psw.log'

def read_eep(address, rx_bytes):
    data = bytes()
    spi.cs = True
    spi.transfer([EEP_READ, address[0], address[1]])
    for i in range(rx_bytes) :
        data += spi.transfer([0xFF])
    spi.cs = False
    return data

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

# dump program
sys.stdout.flush()
add_log_file(file_log,'Connect BusPirate...')
spi = SPI(portname='COM4', speed=115200, timeout=0.1, connect=True)
add_log_file(file_log,'Entering SPI mode...')
spi.enter()
add_log_file(file_log,'Configuring SPI...')
spi.pins = spi.PIN_POWER | spi.PIN_CS
spi.speed = '125kHz'
spi.config = spi.CFG_PUSH_PULL | spi.CFG_CLK_EDGE
add_log_file(file_log,'Reading EEPROM...')
eep_addr = [0x00, 0x4a]
rxdata = read_eep(eep_addr, 4)
str_hex = ''
str_int =''
for b in rxdata:
    str_int = str_int + str(int(b))
    str_hex = str_hex + str(hex(b)) + ' '

add_log_file(file_log,'------------------------------------')
add_log_file(file_log,'Value from EEPROM (hex): ' + str_hex)
add_log_file(file_log,'Value from EEPROM (int): ' + str_int)
add_log_file(file_log,'------------------------------------')
add_log_file(file_log,'Disconnect BusPirate...')
spi.disconnect()


