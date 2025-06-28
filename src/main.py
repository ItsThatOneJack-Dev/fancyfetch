import setup as MeowfetchSetup
import constants as MeowfetchConstants
import configurationhandler as MeowfetchConfigurationHandler
import formatting as MeowfetchFormatting
import widgets as MeowfetchWidgets

import shutil as ShellUtilityLibrary
import os as OperatingSystemLibrary

def GetChildren(Directory):
    try:
        return OperatingSystemLibrary.listdir(Directory)
    except (OSError, FileNotFoundError):
        return []
def CompareChildren(OriginalDirectory, Directory):
    OriginalFiles = set(GetChildren(OriginalDirectory))
    Files = set(GetChildren(Directory))
    return OriginalFiles - Files

def HasConfigurationBeenChanged():
    if len(CompareChildren(MeowfetchConstants.WidgetsDirectory, MeowfetchConstants.DefaultWidgetsDirectory)) > 0:
        return True
    if open(MeowfetchConstants.ConfigurationFile, "r").read() != open(MeowfetchConstants.DefaultConfigurationFile, "r").read():
        return True

def OPTION_RegenerateConfiguration():
    if not HasConfigurationBeenChanged:
        print("Configuration has not been changed, no need to regenerate your configuration!")
        exit(0)
    else:
        print("Are you sure you want to regenerate your configuration? This will reset everything to default!")
        print("Type 'yes' to confirm, or anything else to cancel.")
        Confirmation = input().strip().lower()
        if Confirmation.lower().strip() in "yes":
            ShellUtilityLibrary.rmtree(MeowfetchConstants.ConfigurationDirectory, ignore_errors=True)
        else:
            print("Configuration regeneration cancelled!")
            exit(0)

MeowfetchSetup.EnsureConfiguration()
Configuration = MeowfetchConfigurationHandler.FetchConfiguration()

CONFIG_DisplayASCII = Configuration.get("display_ascii", True) # Default to True if not set.
CONFIG_ASCIILocation = Configuration.get("ascii_location", "left") # Default to "left" if not set.
CONFIG_Spacing = Configuration.get("spacing", 5) # Default to 5 if not set.
CONFIG_ASCII = Configuration.get("ascii", None) # Default to None if not set.

CONFIG_Layout = Configuration.get("layout", ["hello","datetime"]) # Default to ["hello", "datetime"] if not set.

ASCII = CONFIG_ASCII if CONFIG_DisplayASCII else []
try:
    Layout = [MeowfetchWidgets.LoadWidget(str(MeowfetchConstants.WidgetsDirectory), X) for X in CONFIG_Layout]
except ValueError as e:
    print(e.args[0])
    exit(1)

MeowfetchFormatting.MeowfetchColourFormatter(None).Print(
    MeowfetchFormatting.Formatter(
        ASCII,
        Layout,
        ShellUtilityLibrary.get_terminal_size().columns,
        CONFIG_ASCIILocation,
        CONFIG_Spacing
    )
)