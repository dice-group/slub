from slub import Slub
from fox import Fox
from controller import SlubController
import logging as log
import os
import shutil

def getIdentifiers(slubcrtl):
    """
    Gets identifiers from file or creates the identifiers file.
    """
    # get identifiers from file
    identifiers = slubcrtl.loadIdentifiers()

    # if no file create identifiers file
    if identifiers is None:
        # get all identifiers and store it
        slubcrtl.storeIdentifiers()
        identifiers = slubcrtl.loadIdentifiers()
    return identifiers


def main():
    log.basicConfig(filename='slub.log', level=log.DEBUG)

    log.info("Main started...")

    # init controller and model
    slubcrtl = SlubController(Slub(), Fox())

    # record identifiers
    identifiers = getIdentifiers(slubcrtl)

    # store for each identifier the text data
    folder = "records"
    slubcrtl.storeRecords(folder, identifiers)

		# removes empty folders
    for identifier in identifiers:
        identifierDir = folder+"/"+identifier
        if os.path.isdir(identifierDir) and not os.listdir(identifierDir):
            shutil.rmtree(identifierDir)

    # send text data to fox and store turtle files
    for identifier in identifiers:
        slubcrtl.readRecordSendFox(folder, identifier)

		# skip = len(identifiers)
    # for identifier in identifiers[skip:len(identifiers)]:
    #     identifierDir = folder+"/"+identifier
    #     if os.path.isdir(identifierDir):
    #         # print("delet identifierDir" +identifierDir)
    #         shutil.rmtree(identifierDir)
		
    log.info("Main finsihed.")


if __name__ == '__main__':
    main()
