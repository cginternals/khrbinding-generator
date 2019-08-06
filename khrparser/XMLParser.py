
import xml.etree.ElementTree
import os.path
import datetime

from khrapi.API import API

class XMLParser:

    @classmethod
    def parse(cls, profile):
        xmlFile = profile.inputfile
        apiRequire = profile.apiRequire

        revision_date = datetime.datetime.fromtimestamp(os.path.getmtime(xmlFile))
        revision_string = revision_date.isoformat(timespec='seconds')
        
        api = API(profile.api, revision_string)
        
        tree = xml.etree.ElementTree.parse(xmlFile)

        cls.parseXML(api, tree.getroot())

        return api
