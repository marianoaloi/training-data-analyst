import re
from datetime import datetime
from typing import List

dateformat="%H:%M:%S.%f"

class InformationLog:
    ignore:bool=False
    def __init__(self,datetimeorig:str,pod:str,msg:str) -> None:
        self.date_log:datetime=datetimeorig if isinstance(datetimeorig,datetime) else datetime.strptime(datetimeorig,dateformat)
        self.pod:str=pod
        self.origmsg=msg
        
    def __str__(self) -> str:
        return f"{self.date_log.strftime(dateformat)} {self.pod} {self.origmsg[:100]}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
class OwnerSaved(InformationLog):
    owner:str
    def __init__(self, ilorig:InformationLog) -> None:
        super().__init__(ilorig.date_log,        ilorig.pod,        ilorig.origmsg)
class WithFolder(InformationLog):
    folder:str
    def __init__(self, ilorig:InformationLog) -> None:
        super().__init__(ilorig.date_log,        ilorig.pod,        ilorig.origmsg)
class CleanTopic(WithFolder):
    def __init__(self, ilorig:InformationLog) -> None:
        super().__init__(ilorig)
    
class SearchingFolder(WithFolder):
    def __init__(self, ilorig:InformationLog) -> None:
        super().__init__(ilorig)
    milleseconds:int    
    
    def __str__(self) -> str:
        return f"{super().__str__()} {self.folder} {self.milleseconds}"
        
    
class RootEmpty(SearchingFolder):
    pass


class SearchedFolder(WithFolder):
    def __init__(self, ilorig:InformationLog) -> None:
        super().__init__(ilorig)
    subfolders:List[str]
class FolderRootAlread(WithFolder):
    def __init__(self, ilorig:InformationLog) -> None:
        super().__init__(ilorig)
    def __str__(self) -> str:
        return f"{super().__str__()} {self.folder} <<"
    

class SubFolder:
    
    def __init__(self,folder:str,quantityClean:int,quantityTotal:int) -> None:        
        self.folder:str = folder
        self.quantityClean:int = quantityClean
        self.quantityTotal:int = quantityTotal
    def __repr__(self) -> str:
        return f"{self.folder} {self.quantityClean}/{self.quantityTotal}"
class SearchedFiles(WithFolder):
    def __init__(self, ilorig:InformationLog) -> None:
        super().__init__(ilorig)
    subfolders:List[SubFolder]
    
class BeginPreview(WithFolder):
    def __init__(self, ilorig:InformationLog) -> None:
        super().__init__(ilorig)
    quantity:int
class EndPreview(WithFolder):
    def __init__(self, ilorig:InformationLog) -> None:
        super().__init__(ilorig)
    quantity:int
class ErrorFind(WithFolder):
    def __init__(self, ilorig:InformationLog) -> None:
        super().__init__(ilorig)
    error:str
class SavedFolder(WithFolder):
    def __init__(self, ilorig:InformationLog) -> None:
        super().__init__(ilorig)
    collection:str
    
    matcoll   :int=0
    delcoll   :int=0
    inscoll   :int=0
    updcoll   :int=0
class SavingFolder(WithFolder):
    def __init__(self, ilorig:InformationLog) -> None:
        super().__init__(ilorig)
    collection:str

file = open("/mnt/huge/backup/remotelogfolde Manhã.log")

def choiceType(ilorig:InformationLog):
    msg = ilorig.origmsg
    
    
    m=re.findall("\[--\]",msg)
    if(m):
        ilorig.ignore=True
        return ilorig
    
    m=re.findall("Folder root[ ]*\[([\w_\-\d]{8})",msg)
    if(m):
        m=m[0]
        il:FolderRootAlread=FolderRootAlread(ilorig)
        il.folder=m
        return il
    m=re.findall("Root empty[ ]*([\w_\-\d]{8})>>(\d{13})",msg)
    if(m):
        m=m[0]
        il:RootEmpty=RootEmpty(ilorig)
        il.folder=m[0]
        il.milleseconds=m[1]
        return il
    m=re.findall("Searching in Folder[ ]*([\w_\-\d]{8})>>(\d{13})",msg)
    if(m):
        m=m[0]
        il:SearchingFolder=SearchingFolder(ilorig)
        il.folder=m[0]
        il.milleseconds=m[1]
        return il
    m=re.findall("Searched[ ]+\[([\w_\-\d]{8})\][ ]+Folders[ ]+\[([^\]]+)\]",msg)
    if(m):
        m=m[0]
        il:SearchedFolder=SearchedFolder(ilorig)
        il.folder=m[0]
        il.subfolders=m[1].split(",")
        return il
    m=re.findall("Search \[([^\]]{8})\] files from \[(.*)",msg)
    if(m):
        m=m[0]
        il:SearchedFiles=SearchedFiles(ilorig)
        il.folder=m[0]
        il.subfolders=[SubFolder(x[0],x[1],x[2]) for x in re.findall("([^\]]{8})\[(\d+)/(\d+)\]",m[1])]
        return il
    
    
    m=re.findall("Begin preview \[([\w_\-\d]{8})\] files[ ]*(\d+)",msg)
    if(m):
        m=m[0]
        il:BeginPreview=BeginPreview(ilorig)
        il.folder=m[0]
        il.quantity=m[1]
        return il
    m=re.findall("End preview \[([\w_\-\d]{8})\] files finished (\d+)",msg)
    if(m):
        m=m[0]
        il:EndPreview=EndPreview(ilorig)
        il.folder=m[0]
        il.quantity=m[1]
        return il
    m=re.findall("Error find files into folder\[([\w_\-\d]{8})\] error ==>[ ]*(.+)",msg)
    if(m):
        m=m[0]
        il:ErrorFind=ErrorFind(ilorig)
        il.folder=m[0]
        il.error=m[1]
        return il
    m=re.findall("^Error try get the folders at folders ([\w_\-\d]{8})[ ]*(.+)",msg)
    if(m):
        m=m[0]
        il:ErrorFind=ErrorFind(ilorig)
        il.folder=m[0]
        il.error=m[1]
        return il
    
    
    m=re.findall("^Saving \[([\w_\-\d]{8})\].*([^ ]+)$",msg)
    if(m):
        m=m[0]
        il:SavingFolder=SavingFolder(ilorig)
        il.folder=m[0]
        il.collection=m[1]
        return il
    m=re.findall("^Saved \[([\w_\-\d]{8})\].*([^ ]+)$",msg)
    if(m):
        m=m[0]
        il:SavedFolder=SavedFolder(ilorig)
        il.folder=m[0]
        il.collection=m[1]
        return il
    m=re.findall("^Clean Permanentely the topic \[folderConsume/([^ ]+)\]$",msg)
    if(m):
        m=m[0]
        il:CleanTopic=CleanTopic(ilorig)
        il.folder=m
        return il
    
    m=re.findall("^Owner unSaved.*([^ ]+)$",msg)
    if(m):
        m=m[0]
        il:OwnerSaved=OwnerSaved(ilorig)
        il.owner=m[0]
        return il

rootTree={"lixo":[],"ignored":[],"data":{}}
with file as f:
    for line in f.readlines():
        m=re.findall("([\d]{2}:[\d]{2}:[\d]{2}\.\d{3}) \[Get_File_four-folder-\w{10}-(\w{5})[^\]]+\][^-]+-\W+(.+)",line)
        if(m):
            m=m[0]
            il=InformationLog(m[0],m[1],m[2])
            il=choiceType(il)
            if(il):
                il.origmsg=None
                if(not il.ignore):
                    className=re.findall("__main__.([^']+)",str(type(il)))[0]
                    if isinstance(il,WithFolder) :
                        il:WithFolder=il
                        folderCollection:dict  = rootTree["data"].get(il.folder)
                        if(not folderCollection):
                            folderCollection=rootTree["data"][il.folder]={}
                        classCollection:List[InformationLog] = folderCollection.get(className)
                        if(not classCollection):
                            classCollection=folderCollection[className]=[]
                        classCollection.append(il)
                        # print(type(il),il)
                    else :
                        rootTree["lixo"].append(il)
                        
                else:                    
                    rootTree["ignored"].append(il)
            else:
                rootTree["lixo"].append(il)
                # print("FFFFFF",m[2][:100])
                pass
            
import json

with open("temp.json","w")    as fJson:
    json.dump(rootTree,fJson)