# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 08:23:09 2021

@author: Julien
"""
import os
import datetime

def contains_digit(string):
    for character in string:
        if character.isdigit():
            return 1

def parse_line(line):
    line_content = line.split(":")
    try:
        attribute = line_content[0]
        value = line_content[1]
        return attribute, value
    except:
        return None, None
    
def parse_time(value):
    date, time = value.split("T")
    date_str = '-'.join([date[:4],date[4:6],date[6:8]])
    time_str= '-'.join([time[:2],time[2:4]])
    date = datetime.datetime(year=int(date[:4]), month=int(date[4:6]), day=int(date[6:8]), hour=int(time[:2]), minute=int(time[2:4])) #year, month, day, hour, minutes
    return date, date_str, time_str

def parse_desc(value):
    professors = None
    groups = None
    mod = None
    for value in value.split(","):
        if contains_digit(value):
            subvalue = value.split(" ")
            if len(subvalue)>1:
                if groups is None:
                    groups = subvalue[1]
                else:
                    groups += " | "+subvalue[1]
                for info in subvalue[0].split("-"):
                    if info.lower() in ["tp","td"]:
                        mod=info
        else:
            if professors is None:
                professors= value
            else:
                professors+= " | " + value
    return groups, professors, mod
    
    
def read_file(path):
    """
    Lecture d'un fichier.

    :param chemin: le chemin du fichier
    :return: la chaine de caractère contenant tout le fichier ou None si le fichier n'a pu être lu
    """

    try:
        with open(path, encoding="utf8") as f:
            return f.read().splitlines()
    except:
        print("Le fichier n'existe pas %s", os.path.abspath(path))
        return None
    
def event_csv(tab):
    csv_tab = [None]*9
    end_date = None
    start_date = None
    for line in tab:
        attribute, value = parse_line(line)
        if attribute is not None:
            if attribute == 'UID':
                csv_tab[0]=value
            if attribute == 'DTSTART':
                start_date, date_str, time_str = parse_time(value)
                csv_tab[1]=date_str
                csv_tab[2]=time_str
            if attribute == 'DTEND':
                end_date, date_str, time_str = parse_time(value)
            if attribute == 'DESCRIPTION':
                groups, professors, mod = parse_desc(value)
                csv_tab[8]=groups
                csv_tab[7]=professors
                csv_tab[4]=mod
            if attribute == 'SUMMARY':
                csv_tab[5]=value
            if attribute == 'LOCATION':
                csv_tab[6]=value
    if end_date and start_date:
        csv_tab[3]=str(end_date-start_date)[:-3]
    return csv_tab

def main(file):
    filelines = read_file(file)
    i=0
    while i<len(filelines):
        attribute, value = parse_line(filelines[i])
        if attribute=="BEGIN":
            debut=i+1
            fin =i
            while True:
                fin+=1
                attribute, value = parse_line(filelines[fin])
                if attribute =="END":
                    break
            csv_tab = event_csv(filelines[debut:fin])
            csv_line = ";".join(csv_tab)
            print(csv_line)
        i+=1
            
main("evenementSAE_15.ics")