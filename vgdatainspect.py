# VGDataInspect
# Written by Divingkatae on 12/16/2020-12/20/2020

import os
import sys
import json

def check_wad(file_input):
    if ((file_input[0:8] == "49574144") or (file_input[0:8] == "50574144")):
        return "Doom WAD file suspected"
    else:
        return "Unknown WAD file"
        
def check_xld(file_input):
    if (file_input[0:10] == "584C443049"):
        return "Albion XLD file suspected" 
    else:
        return "Unknown XLD file"
        
def check_pak(file_input):
    if (file_input[0:8] == "5041434B"):
        return "Quake PAK file suspected" 
    else:
        return "Unknown PAK file"

def check_cod_ff(file_input):
    grab_sig = file_input[0:16]

    codsig = {
        "4957666675313030" : "Unsigned Infinity Ward FF file",
        "4957666630313030" : "Signed Infinity Ward FF file",
        "5441666630313030" : "Signed Treyarch FF file (Black Ops II)",
        "5331666630313030" : "Signed Sledgehammer Games FF file",
        "5441666630303030" : "Signed Treyarch FF file (Black Ops III)",
    }

    return codsig.get(grab_sig, "Unrecognized Fastfile") 
    
def check_magic_number(file_input):
    if (file_input[0:8] == "504B0304"):
        return "ZIP file suspected" 
    elif (file_input[0:12] == "526172211A07"):
        return "RAR file suspected" 
    elif (file_input[0:12] == "377ABCAF271C"):
        return "7zip file suspected"
    elif (file_input[0:6] == "524E53"):
        return "RNC-compressed file suspected"
    else:
        return "Magic number not known"
    
def grab_extension_match(argument): 
    with open('rcogfileexts.json', 'r') as json_file:
        switcher = json.load(json_file)
  
    return switcher.get(argument.lower(), "Unrecognized File Extension") 

if __name__ == "__main__":
    txt = input("Enter the file you would like to inspect: ")
    argument=os.path.splitext(txt)
    print (argument[1])
    print (grab_extension_match(argument[1]))

    if os.path.exists(txt):
        grabfile = open(txt, 'rb')
        filesize = os.stat(txt).st_size
        print("File Size (in bytes):", filesize)
        if (filesize >= 256):
            print("First 256 bytes:")
            step1 = grabfile.read()[0:256].hex()

            for sub_offset in range(0, 512, 32):
                print(step1[sub_offset:(sub_offset +32)].upper())
        else:
            print("Entire File Contents:")
            step1 = grabfile.read().hex()
                
            print(step1.upper())
       
        # Kludge - Signature check
            
        if (argument[1] == ".wad"):
            print(check_wad(step1))
        elif (argument[1] == ".xld"):
            print(check_xld(step1))
        elif (argument[1] == ".pak"):
            print(check_pak(step1))
        elif (argument[1] == ".ff"):
            print(check_cod_ff(step1))
        else:
            print("Checking for a magic number...")
            print(check_magic_number(step1))

    else:
        print("It seems the file does not exist. Make sure it is in the proper file path specified.")
    
