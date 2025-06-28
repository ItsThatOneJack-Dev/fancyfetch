import constants as MeowfetchConstants
import json5 as JSONFiveLibrary

def FetchConfiguration():
    with open(MeowfetchConstants.ConfigurationFile, 'r', encoding='UTF-8') as FilePointer:
        try:
            return JSONFiveLibrary.load(FilePointer) # Return the configuration, parsed into a Python dictionary.
        except Exception as e:
            raise ValueError(str(e))