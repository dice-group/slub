from slub import Slub
from fox import Fox
from controller import SlubController
import logging as log
import os
import shutil
from multiprocessing import Pool
from functools import partial


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
    log.info("Loaded {} identifiers".format(len(identifiers)))
    return identifiers


def foxf(identifier, folder, slubcrtl):
    slubcrtl.readRecordSendFox(folder, identifier)


def main():
    log.basicConfig(
        filename='log.log',
        level=log.DEBUG,
        format='%(asctime)s %(levelname)-2s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    processes = 5

    log.info("Main started...")

    # init controller and model
    slubcrtl = SlubController(Slub(), Fox())

    # record identifiers
    identifiers = getIdentifiers(slubcrtl)

    # store for each identifier the text data
    folder = "records"
    slubcrtl.storeRecords(folder, identifiers)

    # removes empty folders
    # for identifier in identifiers:
    #    identifierDir = folder+"/"+identifier
    #    if os.path.isdir(identifierDir) and not os.listdir(identifierDir):
    #        shutil.rmtree(identifierDir)

    # send text data to fox and store turtle files
    with Pool(processes) as pool:
        pool.map(partial(foxf, folder=folder, slubcrtl=slubcrtl), identifiers)

    # for identifier in identifiers:
    #    slubcrtl.readRecordSendFox(folder, identifier)

    # skip = len(identifiers)
    # for identifier in identifiers[skip:len(identifiers)]:
    #     identifierDir = folder+"/"+identifier
    #     if os.path.isdir(identifierDir):
    #         # print("delet identifierDir" +identifierDir)
    #         shutil.rmtree(identifierDir)

    log.info("Main finsihed.")


if __name__ == '__main__':
    main()
