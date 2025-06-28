import pathlib as PathLibrary

ConfigurationDirectory = PathLibrary.Path("~/.config/meowfetch").expanduser()
ConfigurationFile = ConfigurationDirectory / "configuration.json5"
WidgetsDirectory = ConfigurationDirectory / "widgets"

DefaultConfiguationDirectory = PathLibrary.Path(__file__).parent / "defaults"
DefaultConfigurationFile = DefaultConfiguationDirectory / "configuration.json5"
DefaultWidgetsDirectory = DefaultConfiguationDirectory / "widgets"