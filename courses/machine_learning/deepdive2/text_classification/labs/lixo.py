import re
from datetime import datetime

dateformat="%H:%M:%S.%f"

class InformationLog:
    def __init__(self,datetimeorig:str,pod:str,msg:str) -> None:
        self.date_log:datetime=datetime.strptime(datetimeorig,dateformat)
        self.pod:str=pod
        self.origmsg=msg
        
    def __str__(self) -> str:
        return f"{self.date_log.strftime(dateformat)} {self.pod} {self.origmsg}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
class SearchingFolder(InformationLog):
    folder:str
    milleseconds:int    
    
    def __str__(self) -> str:
        return f"{super().__str__()} {self.folder} {self.milleseconds}"
    
    
class RootEmpty(SearchingFolder):
    pass


file = open("/mnt/huge/backup/remotelogfolde Manhã.log")

def choiceType(il:InformationLog):
    msg = il.origmsg
    m=re.findall("Root empty[ ]*([\w_\-\d]{8})>>(\d{13})",msg)
    if(m):
        m=m[0]
        il:RootEmpty=il
        il.folder=m[0]
        il.milleseconds=m[1]
        return il
    m=re.findall("Searching in Folder[ ]*([\w_\-\d]{8})>>(\d{13})",msg)
    if(m):
        m=m[0]
        il:SearchingFolder=il
        il.folder=m[0]
        il.milleseconds=m[1]
        return il

with file as f:
    for line in f.readlines():
        m=re.findall("([\d]{2}:[\d]{2}:[\d]{2}\.\d{3}) \[Get_File_four-folder-\w{10}-(\w{5})[^\]]+\][^-]+-\W+(.+)",line)
        if(m):
            m=m[0]
            il=InformationLog(m[0],m[1],m[2])
            il=choiceType(il)
            if(il):
                print(type(il),il)