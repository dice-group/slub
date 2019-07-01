import logging as log


class IOUtils(object):

    def __init__(self):
        pass

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
