import importlib.util as ImportLibraryUtilities
import pathlib as PathLibrary

def LoadWidget(Directory, Filename):
    if not Filename.endswith('.py'):
        Filename += '.py'
   
    FilePath = PathLibrary.Path(Directory) / Filename
    
    if not FilePath.exists():
        print(f"File {Filename} not found in {Directory}")
        raise ValueError(f"You attempted to use the constant {Filename.rstrip('.py')}, but a constant definition for it could not be found, it must be a direct child of {Directory}!")
    
    Spec = ImportLibraryUtilities.spec_from_file_location("temp_module", FilePath)
    if Spec is None:
        raise ValueError(f"An error occured while processing the definition for the constant {Filename.rstrip('.py')}. A spec for the file could not be generated.")
    
    Module = ImportLibraryUtilities.module_from_spec(Spec)
    Spec.loader.exec_module(Module) # type: ignore
    
    if not hasattr(Module, 'Widget'):
        raise ValueError(f"An error occured while processing the definition for the constant {Filename.rstrip('.py')}. Widget definitions must define the class `Widget`.")
    
    WidgetClass = getattr(Module, 'Widget')
    WidgetInstance = WidgetClass()
    
    if not hasattr(WidgetInstance, 'Get'):
        raise ValueError(f"An error occured while processing the definition for the constant {Filename.rstrip('.py')}. Widget classes must define the method `Get`.")
    
    return WidgetInstance.Get()