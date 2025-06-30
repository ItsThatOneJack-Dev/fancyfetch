import shutil as ShellUtilityLibrary
import os as OperatingSystemLibrary

import shared as FancyfetchShared

# Functions
def EnsureConfigurationDirectory():
    FancyfetchShared.ConfigurationDirectory.mkdir(exist_ok=True, parents=True)

def CopyDirectoryContents(SourceDirectory, DestinationDirectory):
    for Item in OperatingSystemLibrary.listdir(SourceDirectory):
        SourceItem = OperatingSystemLibrary.path.join(SourceDirectory, Item)
        DestinationItem = OperatingSystemLibrary.path.join(DestinationDirectory, Item)
        
        if OperatingSystemLibrary.path.isdir(SourceItem):
            ShellUtilityLibrary.copytree(SourceItem, DestinationItem, dirs_exist_ok=True)
        else:
            OperatingSystemLibrary.makedirs(DestinationDirectory, exist_ok=True)
            ShellUtilityLibrary.copy(SourceItem, DestinationItem)

def EnsureConfiguration():
    if not FancyfetchShared.ConfigurationFile.exists():
        EnsureConfigurationDirectory()
        CopyDirectoryContents(FancyfetchShared.DefaultConfiguationDirectory, FancyfetchShared.ConfigurationDirectory)

