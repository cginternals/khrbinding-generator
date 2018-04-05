#!/usr/bin/python

import os, sys, getopt, json

from khrparser.ParserDetector import ParserDetector
from khrparser.Profile import Profile

from khrparser.gl.GLParser import GLParser
from khrparser.egl.EGLParser import EGLParser
from khrparser.vk.VKParser import VKParser

from khrapi.API import API

from khrgenerator.cpp.CPPGenerator import CPPGenerator


def main(argv):
    try:
        opts, args = getopt.getopt(argv[1:], "p:d:", ["profile=", "directory=" ])
    except getopt.GetoptError:
        print("usage: %s -p <profile JSON> [-d <output directory>]" % argv[0])
        sys.exit(1)

    profileFile = None
    targetDir = "."

    for opt, arg in opts:
        if opt in ("-p", "--profile"):
            profileFile = arg
        
        if opt in ("-d", "--directory"):
            targetDir = arg

    if profileFile == None or not os.path.isfile(profileFile):
        print("no profile given or not readable")
        sys.exit(1)

    profile = Profile(json.load(open(profileFile)), targetDir)
    
    parsers = {
      "gl": GLParser,
      "egl": EGLParser,
      "vk": VKParser,
      # "idl": IDLParser
      # "auto": ParserDetector
    }
    
    generators = {
      "cpp": CPPGenerator
    }
    
    if profile.parserIdentifier in parsers:
        khrParser = parsers[profile.parserIdentifier]
    else:
        print("Parser " + profile.parserIdentifier + " not registered")
        sys.exit(1)
    
    if profile.generatorIdentifier in generators:
        khrGenerator = generators[profile.generatorIdentifier]
    else:
        print("Generator " + profile.generatorIdentifier + " not registered")
        sys.exit(1)

    api = khrParser.parse(profile)
    # khrGenerator.generate(profile, api)
    
    # print(api.identifier)

if __name__ == "__main__":
    main(sys.argv)
