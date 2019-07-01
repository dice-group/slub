import logging as log
from ioutils import IOUtils
import os
import json


class SlubController(object):
    ioutils = IOUtils()
    fox = None
    slub = None
    identifiersFile = "identifiers.txt"

    def __init__(self, slub=slub, fox=fox):
        self.slub = slub
        self.fox = fox

    def storeRecord(self, folder, identifier):
        """
        Stores for each given identifier the text data in the xml file
        """
        identifierDir = folder+"/"+identifier
        if not os.path.isdir(identifierDir):
            os.mkdir(identifierDir)

        log.info("Stores record for identifier:{}".format(identifier))

        record = self.slub.requestToGetRecord(identifier)
        if record is None:
            log.error("identifier:{} not found".format(identifier))
            return

        xmlFiles = self.slub.parseFulltextFileNames(record)

        for xmlFile in xmlFiles:
            file = xmlFile[xmlFile.rfind("/"):len(xmlFile)]
            fileTxt = identifierDir+file+".txt"
            fileXml = identifierDir+file

            if os. path. isfile(fileTxt):
                continue

            xmlContent = self.slub.requestXML(xmlFile)
            if xmlContent is None:
                log.error("xmlContent:{} not found".format(xmlFile))
                continue

            content = self.slub.parseAppyFineReaderAnnotations(xmlContent)
            self.ioutils.writeFile(fileTxt, str(content), "w")
            self.ioutils.writeFile(fileXml, str(xmlContent), "w")

    def storeRecords(self, folder, identifiers):
        """
        Stores for each given identifier the text data in the xml file
        """
        for identifier in identifiers:
            self.storeRecord(folder, identifier)

    def readRecordSendFox(self, folder, identifier):
        """
        Reads all files for a specific identifier in the given folder
        and sends the files content to fox.
        The Fox response is stored in turtle.

        :param folder: folder with subfolders of the identifiers
        :type a: string
        :param identifier: identifier which is the folder name
        :type a: string
        """
        # find all files in identifier folder
        files = []
        for (dirpath, dirnames, filenames) in os.walk(folder+"/"+identifier):
            files.extend(filenames)
            break

        files = [fi for fi in files if not fi.endswith(".ttl")]

        if len(files) == 0:
            return None

        for file in files:
            textFile = folder+"/"+identifier+"/"+file
            if os.path.exists(textFile+".ttl"):
                continue

            log.info("read and send Fox: {}".format(textFile))

            content = self.ioutils.readFile(textFile, "r")
            if content is not None:
                res = self.fox.requestFox(content)
                if res is not None:
                    self.ioutils.writeFile(textFile+".ttl", res, "w")

    def loadIdentifiers(self):
        """
        Gets all identifiers from file

        :return: list with strings of the identifiers
        :rtype: list or None
        """
        log.info("Gets all identifiers from a file")
        identifiers = self.ioutils.readFile(self.identifiersFile, "r")
        return json.loads(identifiers)

    def storeIdentifiers(self):
        """
        Gets all identifiers and store it in a file
        """
        log.info("Gets all identifiers and store it in a file")
        resumptiontoken = None

        identifiers = []
        cursor = -1
        completelistsize = 0
        while cursor < completelistsize:
            tree = self.slub.requestTolistRecords(resumptiontoken)
            if tree is None:
                log.error("tree not found")
            else:
                resumptiontoken = self.slub.parseResumptiontoken(tree)
                log.info('resumptiontoken:{}'.format(resumptiontoken))

                cursor = int(self.slub.cursor(tree))
                completelistsize = int(self.slub.completelistsize(tree))
                log.info('cursor:{}, completelistsize:{}'.format(
                    cursor, completelistsize)
                )
                identifiers.extend(self.slub.parseIds(tree))
        # while done
        self.ioutils.writeFile(
            self.identifiersFile, json.dumps(identifiers), "w"
        )
