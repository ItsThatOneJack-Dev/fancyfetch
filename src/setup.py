import shutil
import os

import shared as FancyfetchShared

# Functions
def EnsureConfigurationDirectory():
    FancyfetchShared.ConfigurationDirectory.mkdir(exist_ok=True, parents=True)

def CopyDirectoryContents(SourceDirectory, DestinationDirectory):
    for Item in os.listdir(SourceDirectory):
        SourceItem = os.path.join(SourceDirectory, Item)
        DestinationItem = os.path.join(DestinationDirectory, Item)
        
        if os.path.isdir(SourceItem):
            shutil.copytree(SourceItem, DestinationItem, dirs_exist_ok=True)
        else:
            os.makedirs(DestinationDirectory, exist_ok=True)
            shutil.copy(SourceItem, DestinationItem)

def EnsureConfiguration():
    if not FancyfetchShared.ConfigurationFile.exists():
        EnsureConfigurationDirectory()
        CopyDirectoryContents(FancyfetchShared.DefaultConfiguationDirectory, FancyfetchShared.ConfigurationDirectory)

