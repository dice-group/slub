
import requests
from bs4 import BeautifulSoup
import logging as log


class Slub(object):

    # api endpoint
    endpoint = "https://digital.slub-dresden.de/oai/"

    # data to be send for ListRecords
    listRecordsParameter = {
        "verb": "ListRecords",
        "metadataPrefix": "epicur",
        "set": "ldp-boersenblatt"
    }

    # data to be send for ListRecords
    listRecordsParameterResumption = {
        "verb": "ListRecords"
    }

    # data to be send for GetRecord
    getRecordParameter = {
        "verb": "GetRecord",
        "metadataPrefix": "mets"
    }

    def __init__(self, endpoint=endpoint):
        self.endpoint = endpoint

    def requestTolistRecords(self, resumptiontoken=None):
        """
        Requests to list records.

        :param resumptiontoken: token
        :type a: int
        :return: xml tree or None
        :rtype: BeautifulSoup
        """
        if resumptiontoken is None:
            data = self.listRecordsParameter
        else:
            data = self.listRecordsParameterResumption
            data["resumptionToken"] = resumptiontoken

        return self._send(data)

    def requestToGetRecord(self, identifier):
        """
        Requests a record by the given record identifier.

        :return: xml tree or None
        :rtype: BeautifulSoup
        """
        data = self.getRecordParameter
        data["identifier"] = identifier
        return self._send(data)

    def parseIds(self, tree):
        """
        Pareses the identifiers from the given tree.

        :return: identifiers
        :rtype: list
        """
        identifiers = []
        for recordHeader in tree.findAll("header"):
            identifiers.append(recordHeader.find("identifier").getText())
        return identifiers

    def parseResumptiontoken(self, tree):
        """
        Gets the resumptiontoken value.
        """
        resumptiontokenTag = tree.find("resumptiontoken")
        resumptiontoken = resumptiontokenTag.getText()
        return resumptiontoken

    def _send(self, data):
        """
        Sends POST request and returns a BeautifulSoup xml tree.

        :param data: body data to send
        :type a: json
        :return: xml tree or None in case of not http code 200
        :rtype: BeautifulSoup
        """
        resp = requests.post(self.endpoint, data=data)

        if resp.status_code != 200:
            # raise Exception
            log.error('status: {} message: {}'.format(
                resp.status_code, resp.text
                ))
            return None
        else:
            respXML = resp.text
            tree = BeautifulSoup(respXML, "lxml")# .prettify()
            return tree

    def requestXML(self, url):
        """
        Sends GET request and returns a BeautifulSoup xml tree.

        :param url: url
        :type a: stirng
        :return: xml tree or None in case of not http code 200
        :rtype: BeautifulSoup
        """
        resp = requests.get(url=url)
        if resp.status_code != 200:
            log.error('status: {} message: {} file:{}'.format(
                resp.status_code, resp.text, url
                ))
            return None
        else:
            respXML = resp.text
            tree = BeautifulSoup(respXML, "lxml")# .prettify()
            return tree

    def parseAppyFineReaderAnnotations(self, tree):
        """
        Parses the xml with annotations to text.

        :param xmlFile: body of the xml file
        :type a: string
        :return: content
        :rtype: string
        """

        textblocks = tree.findAll("textblock")
        content = ""
        # for each block
        for textblock in textblocks:
            # for each line
            for line in textblock.findAll("textline"):
                # find each word
                for contentString in line.findAll("string"):
                    word = str(contentString.get("content").strip())
                    content = content + word + " "
                # after each line we start a new line
                content = content + "\r\n"
            # after each block we add a line break
            content = content + "\r\n\n"
        return content

    def parseAppyFineReaderAnnotations_OLD(self, tree):
        """
        Parses the xml with annotations to text.

        :param xmlFile: body of the xml file
        :type a: string
        :return: content
        :rtype: string
        """

        contentStrings = tree.findAll("string")
        content = ""
        for contentString in contentStrings:
            # word = str(contentString.get("content").encode('utf-8').strip())
            word = str(contentString.get("content").strip())
            content = content + " " + word
        return content

    def cursor(self, tree):
        resumptiontokenTag = tree.find("resumptiontoken")
        cursor = resumptiontokenTag.get('cursor')
        return cursor

    def completelistsize(self, tree):
        resumptiontokenTag = tree.find("resumptiontoken")
        completelistsize = resumptiontokenTag.get('completelistsize')
        return completelistsize

    def parseFulltextFileNames(self, tree):
        """
        Returns the XML file names parsed from the given record tree

        :return: xml files
        :rtype: list
        """
        xmlFiles = []
        metsflocat = tree.findAll(mimetype="text/xml")
        for a in metsflocat:
            a = a.find(loctype="URL")
            if len(str(a)) > 0 and str(a) != "None":
                a = "https" + str(a).split("https")[1].split("xml")[0] + "xml"
                xmlFiles.append(a)
        return xmlFiles
