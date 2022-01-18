import re
ATTR=["flags","seq","ack","win","options","length"]

PROTOCOLS = ["ip"]

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
    if part.count("x")==1 and part[:1] == "0x":
        return 1
    
def is_attr(part):
    if part in ATTR:
        return 1

def interpret_part(part):
    if is_time(part):
        return "time"
    if is_protocol(part):
        return "protocol"
    if is_comparator(part):
        return "comparator"
    if is_attr(part):
        return "attr"
    if is_hexa(part):
        return "hexa"