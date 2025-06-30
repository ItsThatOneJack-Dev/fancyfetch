import pathlib as PathLibrary

ConfigurationDirectory = PathLibrary.Path("~/.config/fancyfetch").expanduser()
ConfigurationFile = ConfigurationDirectory / "configuration.json5"
ConstantsDirectory = ConfigurationDirectory / "constants"

DefaultConfiguationDirectory = PathLibrary.Path(__file__).parent / "defaults"
DefaultConfigurationFile = DefaultConfiguationDirectory / "configuration.json5"
DefaultConstantsDirectory = DefaultConfiguationDirectory / "constants"