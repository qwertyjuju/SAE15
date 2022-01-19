# -*- coding: utf-8 -*-
"""
Created on Thu Jan  6 09:22:55 2022

@author: Julien
"""

import os, copy, json, shutil
import interpreters
try:
    import openpyxl as xl
except ModuleNotFoundError:
    XL=0
    print("openpyxl module not found can't create excel")
else:
    XL=1

class HeaderDict:
    def __init__(self):
        self.index=0
        self.data={}
        self.ipcount_list={
            'sd':{},
            's':{},
            'd':{},
        }
        self.port_list={}
        self.ipinfo={}
        
    def add_header(self,header):
        self.index+=1
        self.data[self.index]=header
        return self.index
    
    def create_csv_list(self):
        csv_list=[]
        csv_list.append(";".join(Header.header_content.keys()))
        for header in self.data.values():
            csv_list.append(header.get_csv_format())
        return csv_list
    
    def create_json(self):
        data={}
        self.create_ip_count("sd")
        self.create_ip_count("s")
        self.create_ip_count("d")
        self.create_ip_info()
        data['ip_count']= self.ipcount_list
        data['ip_info']= self.ipinfo
        return data
    
    def create_ip_count(self, iptype="sd"):
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
        total=0
        for nb in self.ipcount_list[iptype].values():
            total+=nb
        self.ipcount_list[iptype]['_total']=total
        return self.ipcount_list[iptype]
    
    def create_port_count(self):
        for header in self.data.values():
            for port in header.get_ports():
                try:
                    self.port_list[port]
                except KeyError:
                    self.port_list[port]=1
                else:
                    self.port_list[port]+=1
                    
    def create_ip_info(self):
        for header in self.data.values():
            srcip=header.get_srcip()
            dstip=header.get_dstip()
            try:
                self.ipinfo[srcip]
            except KeyError:
                self.ipinfo[srcip] = {}
            try:
                self.ipinfo[srcip][dstip]
            except KeyError:
                self.ipinfo[srcip][dstip] = 1
            else:
                self.ipinfo[srcip][dstip] += 1
        for srcip, ipinfo in self.ipinfo.items():
            total=0
            for nb in ipinfo.values():
                total += nb
            ipinfo['_total'] = total

    def get_nb_headers(self):
        return len(self.data)
    
    def get_ipcount(self):
        return self.ipcount_list
    
    def get_ipinfo(self):
        return self.ipinfo
    
    def get_headers(self):
        return self.data.values()
        

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
    
    def get_values(self):
        return self.data.values()
    
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
            
def write_json(obj, path):
    """
    write json file
    """
    with open(path, "w") as f:
        json.dump(obj,f,indent=4)
        
def write_csv(content, path):
    with open(path, 'w') as f:
        for line in content:
            f.write(line+'\n')

def write_xl(headers, path):
    """
    creates excel file
    """
    wb = xl.Workbook()
    ws1 = wb.active
    ws1.title="headers"
    for row, header in enumerate(headers.get_headers(), start=1):
        for col,value in enumerate(header.get_values(), start=1):
            ws1.cell(row,col).value=value
    wb.save(path)
            
            
def create_ip(part):
    """
    returns ip adress and port from string
    """
    splitpart= part.split(".")
    if len(splitpart)>1:
        ip = ".".join(splitpart[:-1])
        port= splitpart[-1]
    else:
        ip=part
        port=""
    return ip, port


def interpret_line(line, nbtest=2):
    """
    interprets line, returns if line is header or content
    """
    linetype = None
    linesplit = line.split(" ")
    if len(linesplit)>1:
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
    """
    gets input from user. returns filename to parse, and repertory 
    for saving results
    """
    filename = None
    out_rep = None
    while not filename:
        filename=str(input("Please enter wich file you want to parse (default: fichier_a_traiter.txt):")or "fichier_a_traiter.txt")
        if not os.path.exists(filename):
            filename=None
    while not out_rep:
        out_rep=str(input("Please enter a new repository name for results (default: results):") or"results" )
        if any(i in out_rep for i in ["/","."]):
            out_rep=None
    return filename, out_rep

def main():
    filename, out_rep= user_input()
    htmldir=out_rep+"/html"
    jsondir=htmldir+"/result.json"
    csvdir=out_rep+"/result.csv"
    xldir=out_rep+"/result.xlsx"
    print("creating directories...")
    if os.path.exists(out_rep):
        shutil.rmtree(out_rep)
        os.mkdir(out_rep)
    else:
        os.mkdir(out_rep)
    shutil.copytree("html skeleton", htmldir)
    print("reading file...")
    file = read_file(filename)
    print("creating header dict...")
    headers=HeaderDict()
    print("creating headers...")
    for line in file:
        line_type = interpret_line(line)
        if line_type == "header":
            Header(headers,line)
    print("creating json data...")
    json_data= headers.create_json()
    print("writing json data...")
    write_json(json_data, jsondir)
    print("creating csv data...")
    csv_data = headers.create_csv_list()
    print("writing csv data...")
    write_csv(csv_data,csvdir)
    if XL:
        print("writing excel...")
        write_xl(headers, xldir)
    print("End, result files put in repertory:", out_rep)

"""
header content:[time, protocol, IP emetor, IP receptor, TCP flag, seq, ack, window size, length]
IP_frame_content: content
"""        
        
main()
        
