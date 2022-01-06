# -*- coding: utf-8 -*-
"""
Created on Fri Dec 17 02:01:02 2021

@author: Julien
"""

import os
import datetime

def contains_digit(string):
    """
    fonction verifiant la présence d'un nombre dans un string
    
    :param string: chaine de caractères
    """
    for character in string:
        if character.isdigit():
            return 1

def parse_line(line):
    """
    découpe une ligne d'un fichier ics pour avoir 2 parties: attribut et valeur
    Si la ligne n'est pas découpable en 2 parties, la fonction retourne None
    
    :param line: ligne du fichier ics
    :return: attribut et valeur ou rien
    """
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
    time_str= ':'.join([time[:2],time[2:4]])
    date = datetime.datetime(year=int(date[:4]), month=int(date[4:6]), day=int(date[6:8]), hour=int(time[:2]), minute=int(time[2:4])) #year, month, day, hour, minutes
    return date, date_str, time_str

def parse_desc(value):
    """
    """
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
    
    
def event_csv(tab):
    """
    création d'une liste, a partir d'un tableau de lignes ics, comportant dans l'ordre:
    uid; date; heure; duree; modalite; intitule; salle1|salle2|...; prof1|prof2|...;
    groupe1|groupe2|...
    
    :param tab: liste des lignes pour 1 evenement ics
    :return: liste des informations de l'evenement ics
    """
    csv_list = [None]*9
    end_date = None
    start_date = None
    for line in tab:
        attribute, value = parse_line(line)
        if attribute is not None:
            if attribute == 'UID': #recuperation UID
                csv_list[0]=value
            if attribute == 'DTSTART': #récuperation date début
                start_date, date_str, time_str = parse_time(value)
                csv_list[1]=date_str
                csv_list[2]=time_str
            if attribute == 'DTEND': #récuperation date de fin
                end_date, date_str, time_str = parse_time(value)
            if attribute == 'DESCRIPTION': #récuperation description
                groups, professors, mod = parse_desc(value)
                csv_list[8]=groups
                csv_list[7]=professors
                csv_list[4]=mod
            if attribute == 'SUMMARY': #récuperation résumé
                csv_list[5]=value
            if attribute == 'LOCATION': #récupération localisation
                csv_list[6]=value
    if end_date and start_date:
        csv_list[3]=str(end_date-start_date)[:-3]
    for i,data in enumerate(csv_list):
        if data is None or data =="":
            csv_list[i]= "vide"
    return csv_list

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
    
def write_file(csv_tab, out_file):
    if os.path.exists(out_file):
        with open(out_file, "w") as f:
            for line in csv_tab:
                f.write(line+"\n")
    else:
        with open(out_file, "x") as f:
            for line in csv_tab:
                f.write(line+"\n")
 
def main(file, out_file):
    """
    découpe d'un calendrier au format ics pour création d'un fichier
    csv.
    """
    filelines = read_file(file)
    csv_tab =[]
    for i, line in enumerate(filelines):
        attribute, value = parse_line(line)
        if attribute=="BEGIN" and value=="VEVENT":
            debut=i+1
            fin =debut
            while True: #
                fin+=1
                attribute, value = parse_line(filelines[fin])
                if attribute =="END" and value=="VEVENT":
                    break
            print(filelines[debut:fin])
            csv_list = event_csv(filelines[debut:fin])
            csv_line = ' ; '.join(csv_list)
            csv_tab.append(csv_line)
        i+=1
    write_file(csv_tab, out_file)
            
main("ADE_RT1_Septembre2021_Decembre2021.ics","ADE_RT1_Septembre2021_Decembre2021.csv")