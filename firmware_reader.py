#!/usr/bin/python3
# -*- coding: utf-8 -*-  
import getopt
import os
import re
import serial
import sys


def write_bin_from_file():
    try:
        with open(output_file, 'ab+') as fo:
            with open(input_file, 'r') as fi:
                for line in fi:
                    hex_string = line[10:59].replace(' ', '')
                    fo.write(bytes.fromhex(hex_string))
    except Exception as e:
        print(e)


def write_bin_from_tty():
    try:
        with open(output_file, 'ab+') as fo:
            ser.write(command)

            uboot_shortcut = input('u-boot shortcut:').encode("utf-8") + b'\x0d'
            while(1):
                line = ser.readline()
                if line == b'\rAutobooting in 1 seconds\n':
                    ser.write(uboot_shortcut)
                elif line == b'\rrlxboot# ':
                    print(line.decode("utf-8")[:-1], command.decode("utf-8"))
                    ser.write(command)
                    print(ser.readline().decode("utf-8")[:-1])
                    break
                else:
                    print(line.decode("utf-8")[:-1])
            i = 0
            while(i < line_number):
                i += 1
                hex_string = ser.readline().decode("utf-8")[11:59].replace(' ', '')
                sys.stdout.write('{0}  Current/Total  {1}/{2}\r'.format(hex_string, i, line_number))
                sys.stdout.flush()
                fo.write(bytes.fromhex(hex_string))
            ser.close()
    except Exception as e:
        print(e)


def usage():
    print(
        "Usage: \npython {0} -i ./hex.txt -o ./firmware.bin".format(sys.argv[0]));
    print(
        "python {0} -s 82000000 -l 1000000 -b 57600 -d /dev/ttyUSB0 -o ./firmware.bin".format(sys.argv[0]))


if __name__ == '__main__':
    print('+' + '-' * 60 + '+')
    print('\t  Firmware Reader')
    print('\t  @Author: Gorgias\thttps://gorgias.me')
    print('+' + '-' * 60 + '+')
    if len(sys.argv) == 5:
        try:
            options, args = getopt.getopt(sys.argv[1:], "i:o:")
            for opt, arg in options:
                if opt == '-i':
                    input_file = arg
            for opt, arg in options:
                if opt == '-o':
                    output_file = arg
            write_bin_from_file()
        except Exception as e:
            print(e)
            usage()
    elif len(sys.argv) == 11:
        try:
            options, args = getopt.getopt(sys.argv[1:], "s:l:b:d:o:")
            for opt, arg in options:
                if opt == '-s':
                    start_addr = arg
            for opt, arg in options:
                if opt == '-l':
                    firmware_size = arg
                    line_number = int(int(arg, 16) / 16)
            for opt, arg in options:
                if opt == '-b':
                    baud_rate = int(arg)
            for opt, arg in options:
                if opt == '-d':
                    device = arg
            for opt, arg in options:
                if opt == '-o':
                    output_file = arg
            ser = serial.Serial(device, baud_rate, timeout=1)
            if ser.isOpen():
                print("connent success!")
                print('baud_rate:', baud_rate)
                print('device:', device)
                print('total size', int(firmware_size, 16))
            if os.path.exists(output_file):
                print("output file exist in the path!")
                exit()
            command = 'md.b {0} {1}'.format(start_addr, firmware_size).encode("utf-8") + b'\x0d'
            write_bin_from_tty()
        except Exception as e:
            print(e)
            usage()
    else:
        usage()
