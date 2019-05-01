import requests
import json
import logging as log


class Fox(object):
    """
    fox = Fox()
    res = fox.sendFox("Leipzig ist eine Stadt in Deutschland.")
    print(res)
    """

    # api endpoint
    endpointExtraction = "http://fox.cs.uni-paderborn.de:4444/fox"
    endpointConfig = "http://fox.cs.uni-paderborn.de:4444/config"

    # data to be send to fox
    requestData = {
        "type": "text",
        "task": "re",
        "output": "Turtle",
        "lang": "de"
    }

    requestHeaders = {
        "charset": "utf-8",
        "Content-Type": "application/json"
    }

    def __init__(self, extraction=endpointExtraction, cfg=endpointConfig):
        self.endpointExtraction = extraction
        self.endpointConfig = cfg

    def requestFox(self, text, cfg=requestData):
        """
        Appends text as value to the input parameter and sends request to fox

        :param text: text to send
        :type a: String
        :param cfg: request config
        :type a: json
        :return: trutle
        :rtype: xml/rdf
        """
        data = cfg
        data["input"] = text
        return self._send(json.dumps(data))

    def _send(self, data):
        """
        Sends request and returns the body

        :param data: body data to send
        :type a: json
        :return: trutle
        :rtype: xml/rdf
        """
        resp = requests.post(
            self.endpointExtraction,
            data=data,
            headers=self.requestHeaders
        )

        if resp.status_code != 200:
            log.error('status: {} message: {}'.format(
                resp.status_code, resp.text
                ))
            return None
        else:
            return resp.text
