# EEPROM METRAN-150

You can use an SPI programmer to read the memory. I used [BusPirate](http://dangerousprototypes.com/docs/Bus_Pirate). 
The connection of the programmer is described in the figures below. 
To connect to the CS pin, you will need to solder to the chip pin.
I wrote utilities to take a full memory dump and to read just the password using BusPirate.

The password is stored in memory at the following addresses:

  - 0x4A: 1-first digit
  - 0x4B: 2nd digit
  - 0x4C: 3rd digit
  - 0x4D: 4th digit

## Script Usage
  - **dump_psw.py** is used to read user password from EEPROM.
  - **dump_all_eeprom.py** is used to dump everything from the EEPROM chip into a single binary file.
  - **bindiff.py** is used to compare binary files and display differences.

## Wiring Diagram

## Microchip 25AA160A

<img src="images/25AA160A_characteristics.png" width="300" >
Figure - 1 - Microchip 25AA160A  characteristics

<img src="images/25AA160A_pin_diagr.png" width="300" >
Figure - 2 - Microchip 25AA160A Pinout
&nbsp;

<img src="images/25AA160A_pin_function.png" width="300" >
Figure - 3 -Microchip 25AA160A pin function
&nbsp;

<img src="images/25AA160A_instr_set.png" width="300" >
Figure - 4 - Microchip 25AA160A instructions
&nbsp;

<img src="images/25AA160A_read_seq.png" width="300" >
Figure - 5 - Microchip 25AA160A read operation
&nbsp;

<img src="images/metran150_SPI_1.png" width="300" >
Figure - 6 - Connecting the programmer to the sensor connector
&nbsp;

<img src="images/metran150_SPI_2.png" width="300" >
Figure - 7 - Connecting the programmer to chip to the CS pin
&nbsp;

<img src="images/metran150_buspirate_mcu.png" width="300" >
Figure - 8 - Connecting BusPirate sensor connector
&nbsp;

<img src="images/metran150_buspirate_CS.png" width="300" >
Figure - 9 - Connecting BusPirate CS pin
&nbsp;


