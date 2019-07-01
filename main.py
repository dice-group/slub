from slub import Slub
from fox import Fox
from controller import SlubController
import logging as log
# import os
# import shutil
from multiprocessing import Pool
from functools import partial

"""
 Change in case you need to.
"""
DEBUG = 0


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


def readRecordSendFox(identifier, folder, slubcrtl):
    slubcrtl.readRecordSendFox(folder, identifier)


def storeRecord(identifier, folder, slubcrtl):
    slubcrtl.storeRecord(folder, identifier)


def main():

    log.basicConfig(
        filename='log.log',
        level=log.DEBUG if DEBUG else log.INFO,
        # format='%(asctime)s %(levelname)-2s %(message)s',
        format="[%(filename)s:%(lineno)s-%(funcName)20s() ] %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    if DEBUG:
        log.info("Application started in DEBUG mode.")

    processes = 1 if DEBUG else 20

    log.info("Main started...")

    # init controller and model
    slubcrtl = SlubController(Slub(), Fox())

    # record identifiers
    identifiers = getIdentifiers(slubcrtl)

    if DEBUG:
        identifiers = identifiers[0:1]

    # store for each identifier the text data
    folder = "records"

    # slubcrtl.storeRecords(folder, identifiers)
    with Pool(processes) as pool:
        pool.map(
            partial(storeRecord, folder=folder, slubcrtl=slubcrtl),
            identifiers)

    # send text data to fox and store turtle files
    # for identifier in identifiers:
    #    slubcrtl.readRecordSendFox(folder, identifier)
    with Pool(processes) as pool:
        pool.map(
            partial(readRecordSendFox, folder=folder, slubcrtl=slubcrtl),
            identifiers)

    log.info("Main finsihed.")


if __name__ == '__main__':
    main()
