import copy

class Sipp_Element:
    def __init__(self,elmt_str):
        self.elmt_str=copy.deepcopy(str(elmt_str))
    
    def __str__(self):
        return (self.elmt_str)
