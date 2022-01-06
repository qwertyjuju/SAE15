# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 09:22:55 2022

@author: Julien
"""
import os

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
    
def interpret_part(part):
    part_type = None
    if part.count(":")==3 and part.count(".")==1:
        part_type == "time"
    if part.count("x") and part[:1] == "0x":
        part_type == "hexa"
    return part_type
    
    
def interpret_line(line):
    linetype = None
    linesplit = line.split(" ")
    result = [None]
    if interpret_part(linesplit[0]) == "time":
        linetype = "header"
        try :
            index = linesplit.index(">")
        except ValueError:
            pass
        else:
            result
    if interpret_part(linesplit[0]) == "hexa":
        linetype = "content"
    return linetype
        
def main(filename):
    file = read_file(filename)
    for line in file:
        line_type = interpret_line(line)
        if line_type == "header":
            
    #for line in file:
    #   parse_line(line)
        
        
main("fichier_a_traiter.txt")
        
