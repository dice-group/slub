import logging as log
import pickle
import os


class SlubController(object):

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
            self.writeFile(fileTxt, str(content), "w")
            self.writeFile(fileXml, str(xmlContent), "w")

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

            content = self.readFile(textFile, "r")
            if content is not None:
                res = self.fox.requestFox(content)
                if res is not None:
                    self.writeFile(textFile+".ttl", res, "w")

    def loadIdentifiers(self):
        """
        Gets all identifiers from file

        :return: list with strings of the identifiers
        :rtype: list or None
        """
        log.info("Gets all identifiers from a file")
        identifiers = self.readSerialize(self.identifiersFile)
        return identifiers

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

        self.writeSerialize(self.identifiersFile, identifiers)

    def writeFile(self, filename, content, mode="wb"):
        f = open(filename, mode)
        f.write(content)
        f.close()

    def readFile(self, filename, mode="rb"):
        try:
            f = open(filename, mode)
            content = f.read()
            f.close()
            return content
        except FileNotFoundError:
            log.error("FileNotFoundError:{}".format(filename))
            return None

    def writeSerialize(self, filename, content):
        serial = pickle.dumps(content)
        self.writeFile(filename, serial)

    def readSerialize(self, filename):
        content = self.readFile(filename)
        if content:
            content = pickle.loads(content)
        return content
