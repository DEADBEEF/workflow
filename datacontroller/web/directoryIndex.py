import sys
import os

class Directory:
    def __init__(self, directory,parent=None):
        self.name = os.path.abspath(directory)
        self.parent = parent
        self.dirs = []
        self.pyFiles = []
        for child in os.listdir(self.name):
            path = os.path.join(self.name,child)
            if os.path.isdir(path) and child[0] != ".":
                self.dirs.append(Directory(path,self))
            elif child[0] != ".":
                self.pyFiles.append(PyFile(path,self))

    def getListInterface(self):
        result = "<ul>\n"
        for direc in self.dirs:
            result += "<li>%s\n%s</li>\n" % (direc, direc.getListInterface()) 
        for fi in self.pyFiles:
            result += "<li>%s</li>" % (fi.name)
        
        result += "</ul>\n"
        return result
    def hasDirs(self):
        return len(self.dirs) != 0

    def __str__(self):
        children = [ "\n".join(["->" + i for i in  str(x).split("\n")])  for x in self.dirs]
        header = self.name
        for pyfile in self.pyFiles:
            header += "\n" + str(pyfile)
        if self.hasDirs():
            return header + "\n" + "\n".join(children)
        else:
            return header

    def getSearchable(self):
        index = {}
        for name, pyFile in self.getFileList():
            index[name] = pyFile
        return index


    def getFileList(self):
        fileList = [ (x.filename, x) for x in self.pyFiles]
        for direc in self.dirs:
            fileList.extend(direc.getFileList())
        return fileList

    def __repr__(self):
        return self.name.split("/")[-1]



class PyFile:
    def __init__(self, filename, parent):
        self.filename = filename
        self.parent = parent
    def __str__(self):
        return self.filename







if __name__ == "__main__":
    print str(Directory(sys.argv[1]))

