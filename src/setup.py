import constants as MeowfetchConstants

# Functions
def EnsureConfigurationDirectory():
    MeowfetchConstants.ConfigurationDirectory.mkdir(exist_ok=True, parents=True)

def EnsureConfigurationFile():
    EnsureConfigurationDirectory()

