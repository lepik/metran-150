#
# author: Adel Daouzli
#
# Adapted for Python3 by Mario Orlandi (2021)
#
# Modified Alexey K (29.03.2024)

import os
import sys
import time

class CompareFiles():
    '''Comparing two binary files'''

    def __init__(self, file1, file2):
        '''Get the files to compare and initialise message, offset and diff list.
        :param file1: a file
        :type file1: string
        :param file2: an other file to compare
        :type file2: string
        '''
        self._buffer_size = 512

        self.message = None
        '''message of diff result: "not found", "size", "content", "identical"'''
        self.offset = None
        '''offset where files start to differ'''
        self.diff_list = []
        '''list of diffs made of tuples: (offset, hex(byte1), hex(byte2))'''

        self.file1 = file1
        self.file2 = file2

    def compare(self):
        '''Compare the two files

        :returns: Comparison result: True if similar, False if different.
        Set vars offset and message if there's a difference.

        '''
        self.message = None
        self.offset_differs = None
        offset = 0
        offset_diff = 0
        first = False
        if not os.path.isfile(self.file1)or not os.path.isfile(self.file2):
            self.message = "not found"
            return False
        if os.path.getsize(self.file1) != os.path.getsize(self.file2):
            self.message = "size"
            return False
        result = True
        f1 = open(self.file1,'rb')
        f2 = open(self.file2,'rb')

        loop = True
        while loop:
            buffer1 = f1.read(self._buffer_size)
            buffer2 = f2.read(self._buffer_size)
            if len(buffer1) == 0 or len(buffer2) == 0:
                loop = False
            for byte1, byte2 in zip(buffer1, buffer2):
                if byte1 != byte2:
                    if first == False:
                        first = True
                    result = False
                    self.diff_list.append((offset, byte1, byte2))

                offset += 1
                if first == False:
                    offset_diff += 1
        f1.close()
        f2.close()

        if result == False:
            self.message = 'content'
            self.offset = hex(offset_diff)
        else:
            self.message = 'identical'

        return result

def ascii_display(e):
    if e < 32:
        text = "%3d" % e
    else:
        text = "'%s'" % chr(e)
    return text

def compare_files(f1, f2, ls):
    c = CompareFiles(f1, f2)
    result = c.compare()
    print("Result of comparison: " + c.message)
    print("File 1 name: ", f1)
    print("File 1 length: ", os.stat(f1).st_size)
    print("File 2 name: ", f2)
    print("File 2 length: ", os.stat(f2).st_size)
    print("Num. differences: ", len(c.diff_list))
    if not result and c.message == 'content':
        print("offset differs: " + c.offset)
        if ls:
            print ("List of differences:")
            for o, e1, e2 in c.diff_list:
                print ("offset 0x%08x: 0x%02x != 0x%02x (%s != %s)" % (
                    o, e1, e2, ascii_display(e1), ascii_display(e2),
                ))


if __name__ == '__main__':
    ls = True
    t0 = time.time()
    # set files compare
    f1 = 'dump_raw_eeprom_1.bin'
    f2 = 'dump_raw_eeprom_2.bin'
    compare_files(f1, f2, ls)
    t1 = time.time()
    print('Elapsed time: ', time.strftime("%H:%M:%S", time.gmtime(t1 - t0)))

