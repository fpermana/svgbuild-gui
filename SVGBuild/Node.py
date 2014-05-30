
from PyQt4 import QtCore

class Node(QtCore.QObject):
    command = ""
    attrib = []
    showCommand = False
    
    def __init__(self):
        super(Node, self).__init__()
        
    def getValue(self):
        value = ""
        if self.showCommand:
            value = '%s %s' % (self.command,  ' '.join(self.attrib))
        else:
            value = ' '.join(self.attrib)
            
        return value
        
    def getTarget(self):
        if Node.getCharacterCount(self.command) > 1:
            return self.attrib[-2:]
        return []
    
#    def getCharacterCount(self):
#        return getCharacterCount(command)
        
    @staticmethod
    def getCharacterCount(command):
        '''http://www.w3.org/TR/SVG11/paths.html'''
        characterCount = 0
        if command == "m" or command == "M":
            characterCount = 2
        elif command == "z" or command == "Z":
            characterCount = 0
        elif command == "l" or command == "L":
            characterCount = 2
        elif command == "h" or command == "H":
            characterCount = 1
        elif command == "v" or command == "V":
            characterCount = 1
        elif command == "c" or command == "C":
            characterCount = 6
        elif command == "s" or command == "S":
            characterCount = 4
        elif command == "q" or command == "Q":
            characterCount = 4
        elif command == "t" or command == "T":
            characterCount = 2
        elif command == "a" or command == "A":
            characterCount = 7
        else:
            characterCount = 1
            
        return characterCount
