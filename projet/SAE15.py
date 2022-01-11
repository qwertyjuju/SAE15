# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 09:22:55 2022

@author: Julien
"""
import os
import re

HEADER_CONTENT = ["time", "IP emetor", "IP receptor", "TCP flag", "seq", "ack", "window size", "length"]
CONTENT_CONTENT = ["hexa", "number"]
PROTOCOLS = ["IP"]


def read_file(path):
    """
    Lecture d'un fichier.

    :param path: le chemin du fichier
    :return: liste des lignes du fichier
    """

    try:
        with open(path, encoding="utf8") as f:
            return f.read().splitlines()
    except:
        print("Le fichier n'existe pas %s", os.path.abspath(path))
        return None
    
    
def parse_header():
    pass

def is_time(part):
    """
    
    """
    if part.count(":")==2 and part.count(".")==1:
        for subpart in re.split(": |.") :
            try:
                int(subpart)
            except ValueError:
                return 0
        return 1
    else:
        return 0
    
def is_protocol(part):
    if part in PROTOCOLS:
        return 1

def is_comparator(part):
    if part == ">":
        return 1
    
def interpret_part(part):
    if is_time(part):
        return "time"
    if is_comparator(part):
        return "comparator"
    if part.count("x") and part[:1] == "0x":
        return "hexa"
    
    
    
def interpret_line(line):
    linetype = None
    linesplit = line.split(" ")
    result = None
    for part in linesplit:
        if interpret_part(part) in HEADER_CONTENT:
            linetype = "header"
        result = [None]*8
        for i in linesplit[1]:
            result[0]=linesplit[0]
            try :
                index = linesplit.index(">")
            except ValueError:
                pass
            else:
                result[1]= linesplit[index-1]
                result[2]= linesplit[index+1]
            
    if interpret_part(linesplit[0]) == "hexa":
        linetype = "content"
    return linetype, result
        
def main(filename):
    file = read_file(filename)
    for line in file:
        line_type, result = interpret_line(line)
        if line_type == "header":
            print(result)
            
"""
header content:[time, IP emetor, IP receptor, TCP flag, seq, ack, window size, length]
IP_frame_content: content
"""        
        
main("fichier_a_traiter.txt")
        
