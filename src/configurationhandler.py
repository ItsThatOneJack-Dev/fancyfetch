import constants as FancyfetchConstants
import json5 as JSONFiveLibrary

def FetchConfiguration():
    with open(FancyfetchConstants.ConfigurationFile, 'r', encoding='UTF-8') as FilePointer:
        try:
            return JSONFiveLibrary.load(FilePointer) # Return the configuration, parsed into a Python dictionary.
        except Exception as e:
            raise ValueError(str(e))