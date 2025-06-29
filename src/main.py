import setup as MeowfetchSetup
import constants as MeowfetchConstants
import configurationhandler as MeowfetchConfigurationHandler
import formatting as MeowfetchFormatting
import widgets as MeowfetchWidgets

import shutil as ShellUtilityLibrary
import os as OperatingSystemLibrary
import argparse as ArgumentParserLibrary

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
    if (not MeowfetchConstants.WidgetsDirectory.exists()) or (not MeowfetchConstants.ConfigurationFile.exists()):
        MeowfetchSetup.EnsureConfiguration()
        print("Your configuration has been regenerated!")
        exit(0)
    if len(CompareChildren(MeowfetchConstants.WidgetsDirectory, MeowfetchConstants.DefaultWidgetsDirectory)) > 0:
        return True
    if open(MeowfetchConstants.ConfigurationFile, "r").read() != open(MeowfetchConstants.DefaultConfigurationFile, "r").read():
        return True

def OPTION_RegenerateConfiguration():
    if not HasConfigurationBeenChanged():
        print("Your configuration has not been changed, no need to regenerate it!")
        exit(0)
    else:
        print("Are you sure you want to regenerate your configuration? This will reset everything to default!")
        print("Type 'yes' to confirm, or anything else to cancel.")
        Confirmation = input().strip().lower()
        if Confirmation.lower().strip() in "yes":
            ShellUtilityLibrary.rmtree(MeowfetchConstants.ConfigurationDirectory, ignore_errors=True)
            MeowfetchSetup.EnsureConfiguration()
            print("Your configuration has been regenerated!")
            exit(0)
        else:
            print("Configuration regeneration cancelled!")
            exit(0)

def OPTION_Configuration():
    MeowfetchSetup.EnsureConfiguration()
    print("Configuration files are accessible at '~/.config/fancyfetch/'!")
    exit(0)

def SetupArgumentParser():
    Parser = ArgumentParserLibrary.ArgumentParser(
        description="Your custom help message goes here. Describe what your program does.",
        epilog="Additional help text can go here at the bottom.",
        formatter_class=ArgumentParserLibrary.RawDescriptionHelpFormatter
    )
    
    Parser.add_argument(
        '--config', '-c',
        action='store_true',
        help='Get the location of the fancyfetch configuration files!'
    )
    
    Parser.add_argument(
        '--regen', '-r', 
        action='store_true',
        help='Regenerate the fancyfetch configuration files, resetting them to default values!'
    )
    
    return Parser

def Main():
    Parser = SetupArgumentParser()
    Args,UnknownArgs = Parser.parse_known_args()
    if Args.config:
        OPTION_Configuration()
    elif Args.regen:
        OPTION_RegenerateConfiguration()

    MeowfetchSetup.EnsureConfiguration()
    Configuration = MeowfetchConfigurationHandler.FetchConfiguration()

    CONFIG_DisplayASCII = Configuration.get("display_ascii", True) # Default to True if not set.
    CONFIG_ASCIILocation = Configuration.get("ascii_location", "left") # Default to "left" if not set.
    CONFIG_Spacing = Configuration.get("spacing", 5) # Default to 5 if not set.
    CONFIG_ASCII = Configuration.get("ascii", ["You have no ASCII defined!","Set the 'ascii' key in your config!","Or run fancyfetch with the '--regen'/'-r' flag!"]) # Default to a warning if not set.

    CONFIG_Layout = Configuration.get("layout", ["hello","datetime","credits"]) # Default to ["hello", "datetime"] if not set.

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
    exit(0)

if __name__ == "__main__":
    try:
        Main()
    except KeyboardInterrupt:
        print("\nExiting Meowfetch...")
        exit(0)