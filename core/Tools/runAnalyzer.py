import os

retval = os.getcwd()
os.chdir(retval + "\\TestOutput\\Profiling\\")


def marshalFile(fileName, filePath):
    os.chdir(filePath)
    timeDict = {}
    with open(fileName) as f:
        lines = f.readlines()
        for line in lines:
            if len(line) < 6 or "ncalls" in line:
                continue
            else:
                l = line.split(",")
                timeDict[l[5]] = l[1]

    print(timeDict)


marshalFile("__init__.prof", "qwak/")
