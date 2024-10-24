
import xml.etree.ElementTree
import os.path
import datetime
import re

from khrapi.API import API
from khrbinding.Binding import Binding

class XMLParser:

    @classmethod
    def parse(cls, profile):
        xmlFile = profile.inputfilepath

        revision_date = datetime.datetime.fromtimestamp(os.path.getmtime(xmlFile))
        revision_string = revision_date.strftime('%Y%m%d')

        api = API(profile.baseNamespace, revision_string)
        
        tree = xml.etree.ElementTree.parse(xmlFile)

        cls.parseXML(api, profile, tree.getroot())
        return api

    @classmethod
    def parseXML(cls, api, profile, registry):
        pass
    
    @classmethod
    def filterAPI(cls, api, profile):
        pass

    @classmethod
    def patch(cls, api, profile):
        pass
    
    @classmethod
    def deriveBinding(cls, api, profile):
        return Binding(api)
