#!/usr/bin/env python

__author__ = "NeverLost"
__version__ = "1.0.1"

import argparse, glob, struct

# TODO: HANDLE ALL FORMATS

MAGICNUMBER = 542327876
CHOICES_FORMATS = ["DXT1", "DXT2", "DXT3", "DXT4", "DXT5", "BC7", "OTHER"]
STRING_FORMAT = "ASCII"
OFFSET_FORMAT = 84
OFFSET_FORMAT_EXTENDED = 128

def get_format_ext(fHandle):
    fHandle.seek(OFFSET_FORMAT_EXTENDED)
    format_ext = struct.unpack('i', fHandle.read(4))[0]

    if format_ext >= 98 and format_ext <= 100:
        return "BC7"
    else:
        return "OTHER"
    
def get_format(fHandle):
    fHandle.seek(OFFSET_FORMAT)
    format = fHandle.read(4).decode(STRING_FORMAT)
    
    if format == "DX10":
        return get_format_ext(fHandle)
    else:
        return format

def extension_dds(string):
    if not string.lower().endswith(".dds"):
        raise argparse.ArgumentTypeError("Provided argument does not have the .dds extension.")
    else:
        return string

def main():
    parser = argparse.ArgumentParser(prog = "DDS Format Genie")
    parser.add_argument("-r", dest = "rec", help = "enables the ** pattern for file paths.", action='store_true')
    parser.add_argument("-fo", dest = "format", help = "specifies the dds format", choices = CHOICES_FORMATS)
    parser.add_argument("path", help = "specifies the file path", type= extension_dds)

    args = parser.parse_args()
    files = glob.iglob(args.path, recursive=args.rec)
    readFiles = 0

    print(parser.prog+":")
    print("     TRYING TO READ FILES:")
    print()
    for file in files:
        fHandle = open(file, 'rb')
        magicno = fHandle.read(4)
        
        if len(magicno) == 4 and struct.unpack('i', magicno)[0] == MAGICNUMBER:
            format = get_format(fHandle)
            
            if args.format == None or args.format == format:
                readFiles += 1
                print("     {}: \"{}\" uses the \"{}\" format".format(readFiles, file, format))
            
        fHandle.close()
       
    print()
    if readFiles == 0:
        print("     DONE. Could not find any files matching the provided path and arguments")
        exit(2)
    else:
        print("     DONE. A total of {} files matched the path and arguments.".format(readFiles))
        exit(1)

main()