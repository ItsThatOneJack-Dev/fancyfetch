import shared as FancyfetchShared
import json5 as JSONFiveLibrary # type: ignore # This line commonly errors stating that json5 cannot be found, oddly only when working with Nuitka, to my experience.
# Though json5 is perfectly available to the code, Nuitka finds and includes it, so I have no clue what is happening here.

def FetchConfiguration():
    with open(FancyfetchShared.ConfigurationFile, 'r', encoding='UTF-8') as FilePointer:
        try:
            return JSONFiveLibrary.load(FilePointer) # Return the configuration, parsed into a Python dictionary.
        except Exception as e:
            raise ValueError(str(e))