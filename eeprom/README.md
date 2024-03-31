# EEPROM METRAN-150

You can use an SPI programmer to read the memory. I used BusPirate. 
The connection of the programmer is described in the figures below. 
To connect to the CS pin, you will need to solder to the chip pin.
I wrote utilities to take a full memory dump and to read just the password using BusPirate.

The password is stored in memory at the following addresses:
0x4A: 1-first digit
0x4B: 2nd digit
0x4C: 3rd digit
0x4D: 4th digit

# Wiring Diagram

## Microchip 25AA160A

<img src="metran-150/images/25AA160A_characteristics.png" width="300" >
Figure - 1 - Microchip 25AA160A  characteristics
&nbsp;

<img src="metran-150/images/25AA160A_pin_diagr.png" width="300" >
Figure - 2 - Microchip 25AA160A Pinout
&nbsp;

<img src="metran-150/images/25AA160A_pin_function.png" width="300" >
Figure - 3 -Microchip 25AA160A pin function
&nbsp;

<img src="metran-150/images/25AA160A_instr_set.png" width="300" >
Figure - 4 - Microchip 25AA160A instructions
&nbsp;

<img src="metran-150/images/25AA160A_read_seq.png" width="300" >
Figure - 5 - Microchip 25AA160A read operation
&nbsp;

<img src="metran-150/images/metran150_SPI_1.png" width="300" >
Figure - 6 - Connecting the programmer to the sensor connector
&nbsp;

<img src="metran-150/images/metran150_SPI_2.png" width="300" >
Figure - 7 - Connecting the programmer to chip to the CS pin
&nbsp;



