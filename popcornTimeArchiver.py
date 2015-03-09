import re
import os
import logging
import shutil
from pprint import pformat
tvSeriesPattern = r".*\.S{1}[0-9]+E{1}[0-9]+\..*"
xpat = r"\.S{1}[0-9]+E{1}[0-9]+\..*"
epicex = r"S{1}[0-9]+E{1}[0-9]+"
seasonex = r"[0-9]+"


def prepareLogger(logFile):
    logging.basicConfig(filename=logFile,
                        level=logging.DEBUG,
                        format='%(asctime)4s%(message)4s\n')


def getSerialTupple(name):
    serialName = re.compile(xpat).split(name)
    season = "season " + re.findall(seasonex, re.findall(epicex, name)[0])[0]
    return serialName[0].replace(".", " "), season


def getFullPath(name):
    serialName, season = getSerialTupple(name)
    return serialName + "/" + season + "/" + name


def getExpectedDirectory(name):
    serialName, season = getSerialTupple(name)
    return serialName + "/" + season + "/"


def createDirectory(name):
    try:
        os.makedirs(name)
        logging.debug("creating directory" + str(name))
    except OSError:
        if not os.path.isdir(name):
            logging.debug("directory already exists")


def getListOfEpisodes(directory):
    listOfEpisodes = []
    pathMap = {}
    for (dir, _, files) in os.walk(directory):
        for eachFile in files:
            if re.match(tvSeriesPattern, eachFile):
                listOfEpisodes.append(eachFile)
                pathMap[eachFile] = os.path.join(dir, eachFile)
    return listOfEpisodes, pathMap

SourceDirectory = "/data/media/PopCornTime/Popcorn-Time/"
destinationDir = "/data/media/archived/Tv/"
logFile = "/home/appster/logs/PopCornTimeArhiver.log"
prepareLogger(logFile)
sourceEpisodes, sourceFileMap = getListOfEpisodes(SourceDirectory)
logging.debug("Processing files " + pformat(sourceEpisodes))
listOfExpectedPaths = [getFullPath(eachEpisode) for eachEpisode in
                       sourceEpisodes]
logging.info("Going to create following files " + pformat(listOfExpectedPaths))
createDirectory(destinationDir)
for eachFile in sourceEpisodes:
    logging.debug("Processing File " + pformat(eachFile))
    targetFilePath = destinationDir + getFullPath(eachFile)
    if not os.path.exists(targetFilePath):
        createDirectory(destinationDir +
                        getExpectedDirectory(eachFile))
        logging.debug("copying a file")
        shutil.copy(sourceFileMap[eachFile], targetFilePath)
        logging.debug("Done copying file")
    else:
        logging.info("File already present. Skipping  this one")
logging.debug("Done Processing everything. Rest for a while. take a break.")
