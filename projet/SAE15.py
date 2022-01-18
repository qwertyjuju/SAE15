# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 09:22:55 2022

@author: Julien
"""
import os, sys, csv, copy, json
import interpreters
#import openpyxl as xl


TESTING =1

class HeaderDict:
    def __init__(self):
        self.index=0
        self.data={}
        self.ipcount_list={
            'sd':{},
            's':{},
            'd':{},
        }
        
    def add_header(self,header):
        self.index+=1
        self.data[self.index]=header
        return self.index
    
    def get_csv_list(self):
        csv_list=[]
        for header in self.data.values():
            csv_list.append(header.get_csv_format())
        return csv_list
    
    def create_ip_count(self, iptype="sd",sort=False):
        if iptype not in ["sd","s","d"]:
            return None
        if iptype=="sd":
            for header in self.data.values():
                for ip in header.get_ips():
                    try:
                        self.ipcount_list['sd'][ip]
                    except KeyError:
                        self.ipcount_list['sd'][ip]=1
                    else:
                        self.ipcount_list['sd'][ip]+=1
        if iptype=="s":
            for header in self.data.values():
                try:
                    ip=self.ipcount_list['s'][header.get_srcip()]
                except KeyError:
                    self.ipcount_list['s'][header.get_srcip()]=1
                else:
                    self.ipcount_list['s'][header.get_srcip()]+=1
        if iptype=="d":
            for header in self.data.values():
                try:
                    ip=self.ipcount_list['d'][header.get_dstip()]
                except KeyError:
                    self.ipcount_list['d'][header.get_dstip()]=1
                else:
                    self.ipcount_list['d'][header.get_dstip()]+=1
        if sort=="r":
            self.ipcount_list = sorted(self.ipcount_list[iptype].items(), key=lambda x: x[1], reverse=True)
        if sort=="n":
            self.ipcount_list = sorted(self.ipcount_list[iptype].items(), key=lambda x: x[1], reverse=True)
        return self.ipcount_list[iptype]
    
    def get_port_count(self):
        port_list={}
        for header in self.data.values():
            for port in header.get_ports():
                try:
                    port_list[port]
                except KeyError:
                    port_list[port]=1
                else:
                    port_list[port]+=1
                    
    def get_nb_headers(self):
        return len(self.data)
        

class Header:
    header_content = {
        "time":"",
        "protocol":"",
        "ip src":"",
        "src port":"",
        "ip dst":"",
        "dst port":"",
        "flags":"",
        "seq":"",
        "ack":"",
        "options":"",
        "length":"",
    }
    headers=[]

    def __init__(self, headerdict, line=None):
        self.data=copy.deepcopy(Header.header_content)
        if line:
            self.init(line)
        self.index=headerdict.add_header(self)

    def init(self, line):
        linesplit = line.split(" ")
        for partindex,part in enumerate(linesplit):
            lowerpart = part.lower()
            part_type= interpreters.interpret_part(lowerpart)
            if part_type == "attr":
                if lowerpart == "options":
                    options=[]
                    for i in range(partindex, len(linesplit)):
                        if linesplit[i].find("[") != -1:
                            options.append(linesplit[i][1:])
                        elif linesplit[i].find("]") != -1:
                            options.append(linesplit[i][:-2])
                            break
                        else:
                            options.append(linesplit[i])
                    optionsstr = "|".join(options)
                    self["options"] = optionsstr
                else:
                    if linesplit[partindex+1][-1] in [",",":"]:
                        value = linesplit[partindex+1][:-1]
                    else:
                        value = linesplit[partindex+1]
                    if lowerpart in self.data.keys():
                        self[lowerpart]=value
            else:
                if part_type == "time":
                    self[part_type] = part
                if part_type == "protocol":
                    self[part_type] = part
                if part_type == "comparator":
                    self["ip src"], self["src port"] = create_ip(linesplit[partindex-1])
                    self["ip dst"], self["src dst"] = create_ip(linesplit[partindex+1][:-1])
                    
    def get_ips(self):
        return self["ip src"], self["ip dst"]
    
    def get_srcip(self):
        return self["ip src"]
    
    def get_dstip(self):
        return self["ip dst"]
    
    def get_ports(self):
        return self["src port"], self["dst port"]
    
    def get_values(self):
        return self.data.values()
    
    def get_csv_format(self):
        return ';'.join(self.data.values())
    
    def __getitem__(self, key):
        if key not in self.data.keys():
            return None
        else:
            return self.data[key]

    def __setitem__(self, key, value):
        if key not in self.data.keys():
            pass
        else:
            self.data[key]=value
            
    def __str__(self):
        return '{}'.format(self.data)


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
            
def write_json(obj, file):
    with open(file, "w") as f:
        json.dump(obj,f)

            
def create_ip(part):
    splitpart= part.split(".")
    ip = ".".join(splitpart[:-1])
    port= splitpart[-1]
    return ip, port


def interpret_line(line, nbtest=2):
    linetype = None
    linesplit = line.split(" ")
    header_count = 0
    content_count = 0
    for testnb in range(nbtest):
        part_type = interpreters.interpret_part(linesplit[testnb].lower())
        if part_type in ["time", "ip emetor", "ip receptor", "attr"]:
            header_count += 1
        if part_type in ["hexa", "number"]:
            content_count += 1
    if header_count> content_count:
        linetype = "header"
    if content_count> header_count:
        linetype = "content"
    return linetype

def user_input():
    filename=None
    out_repo= None
    while not filename:
        filename=str(input("Please enter wich file you want to parse:"))
        if not os.path.exists(filename):
            filename=None
    while not out_repo:
        out_repo=str(input("Please enter a new repository name for results:"))
        if os.path.exists(out_repo):
            out_repo=None
    return filename, out_repo


def main():
    if TESTING:
        filename="fichier_a_traiter.txt"
    else:
        filename, out_repo= user_input()
    file = read_file(filename)
    headers=HeaderDict()
    for line in file:
        line_type = interpret_line(line)
        if line_type == "header":
            header = Header(headers,line)
    #os.makedirs(out_repo)
    ipcount= headers.create_ip_count("sd")
    write_json(ipcount, "result.json")
    print(ipcount)




"""
header content:[time, protocol, IP emetor, IP receptor, TCP flag, seq, ack, window size, length]
IP_frame_content: content
"""        
        
main()
        
