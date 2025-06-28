import pathlib as PathLibrary

ConfigurationDirectory = PathLibrary.Path("~/.config/meowfetch").expanduser()

ConfigurationFile = ConfigurationDirectory / "configuration.json5"
