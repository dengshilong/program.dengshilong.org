import os,sys

def getTitle(firstLine):
    strs = ':'.join(firstLine.split(':')[1:])
    strs = strs.replace("'", '')
    strs = strs.strip()
    title = '-'.join(strs.split(' '))
    return title
if __name__ == "__main__":
    dirName = sys.argv[1]
    for root,dirs,fileNames in os.walk(dirName):
        for fileName in fileNames:
            print fileName 
            print root
            fileName = os.path.join(root, fileName)
            f = open(fileName)
            firstLine = f.readline()
            title = getTitle(firstLine)
            print title
            content = firstLine + f.read()
            f.close()
            newname = title + '.md'
            print newname
            os.rename(fileName, os.path.join(root,newname))
