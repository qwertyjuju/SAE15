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
    
    
def parse_line(line):
    linesplit = line.split(" ")
    for part in linesplit:
        
    
def main(filename):
    file = read_file(filename)
    for line in file:
        parse_line(line)
        
