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
    if part.count(":")==2 and part.count(".")==1:
        for subpart in re.split(r'\W+',part) :
            try:
                int(subpart)
            except ValueError:
                return 0
            else:
                pass
        return 1
    else:
        return 0
    
def is_protocol(part):
    if part in PROTOCOLS:
        return 1

def is_comparator(part):
    if part == ">":
        return 1
    
def is_hexa(part):
    if part.count("x") and part[:1] == "0x":
        return 1
    
def is_flag(part):
    if part.lower()=="flags":
        return 1

def interpret_part(part):
    if is_time(part):
        return "time"
    if is_comparator(part):
        return "comparator"
    if is_flag(part):
        return "flags"
    if is_hexa(part):
        return "hexa"
    
def create_header(line):
    linesplit = line.split(" ")
    attributes=[]
    values[]
    for partindex,part in enumerate(linesplit):
        part_type = interpret_part(part)
        if part_type=="time":
            result[0]=part
        if part_type=="comparator":
            result[1]= linesplit[partindex-1]
            result[2]= linesplit[partindex+1]
        if part_type =="flags":
            result[3]= linesplit[partindex+1]
    
def interpret_line(line, nbtest=2):
    linetype = None
    linesplit = line.split(" ")
    header_count=0
    content_count=0
    for testnb in range(nbtest):
        part_type = interpret_part(linesplit[testnb])
        if part_type in HEADER_CONTENT:
            header_count+=1
        if part_type in CONTENT_CONTENT:
            content_count+=1
    if header_count> content_count:
        linetype = "header"
    if content_count> header_count:
            linetype = "content"
    return linetype
        
def main(filename):
    file = read_file(filename)
    for line in file:
        line_type = interpret_line(line)
        if line_type == "header":
            create_header(line)
            
"""
header content:[time, IP emetor, IP receptor, TCP flag, seq, ack, window size, length]
IP_frame_content: content
"""        
        
main("fichier_a_traiter.txt")
        
