
import xml.etree.ElementTree
import os.path
import datetime
import re

from khrapi.API import API

class XMLParser:

    @classmethod
    def parse(cls, profile):
        xmlFile = profile.inputfilepath
        apiRequire = profile.apiRequire

        revision_date = datetime.datetime.fromtimestamp(os.path.getmtime(xmlFile))
        revision_string = revision_date.strftime('%Y%m%d')
        
        api = API(profile.api, revision_string)
        
        tree = xml.etree.ElementTree.parse(xmlFile)

        cls.parseXML(api, profile, tree.getroot())

        return api
