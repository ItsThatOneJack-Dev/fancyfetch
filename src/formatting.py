import re as re
from rich.console import Console as RichConsole
from typing import Dict, Optional

def RemoveDirectives(Text: str):
    return re.sub(r"<:.*?:>", "", Text)

def EnsureResetEnding(Line):
    if not Line.endswith("<:reset:>"):
        return Line + "<:reset:>"
    return Line

class FancyfetchColourFormatter:
    def __init__(self, CustomColours: Optional[Dict[str, str]] = None):
        self.Console = RichConsole(highlight=False)
       
        self.ColourMap = {
            "red": "#FF0000",
            "green": "#00FF00", 
            "blue": "#0000FF",
            "yellow": "#FFFF00",
            "cyan": "#00FFFF",
            "magenta": "#FF00FF",
            "white": "#FFFFFF",
            "black": "#000000",
            "orange": "#FFA500",
            "purple": "#800080",
            "pink": "#FFC0CB",
            "gray": "#808080",
            "grey": "#808080",
            "lime": "#32CD32",
            "navy": "#000080",
            "maroon": "#800000",
            "olive": "#808000",
            "teal": "#008080",
            "silver": "#C0C0C0",
            "gold": "#FFD700",
        }
       
        self.StyleMap = {
            "bold": "bold",
            "faint": "dim",
            "italic": "italic",
            "underline": "underline",
            "normal": "",  # Will be handled specially
        }
       
        if CustomColours:
            self.ColourMap.update(CustomColours)
       
        self.TagPattern = re.compile(r"<:([^:]+):>")
   
    def AddColour(self, Name: str, HexCode: str):
        self.ColourMap[Name.lower()] = HexCode
   
    def AddStyle(self, Name: str, RichStyle: str):
        self.StyleMap[Name.lower()] = RichStyle
   
    def ParseColour(self, ColourStr: str) -> Optional[str]:
        ColourStr = ColourStr.strip().lower()
        
        # Check for hex codes with # prefix
        if ColourStr.startswith("#") and len(ColourStr) in [4, 7]:
            if re.match(r"^#[0-9a-f]{3}$", ColourStr):  # Added $ anchor
                return f"#{ColourStr[1]*2}{ColourStr[2]*2}{ColourStr[3]*2}"
            elif re.match(r"^#[0-9a-f]{6}$", ColourStr):  # Added $ anchor
                return ColourStr
    
        # Check for hex codes without # prefix
        elif re.match(r"^[0-9a-f]{6}$", ColourStr):  # Added $ anchor
            return f"#{ColourStr}"
        elif re.match(r"^[0-9a-f]{3}$", ColourStr):  # Added $ anchor
            return f"#{ColourStr[0]*2}{ColourStr[1]*2}{ColourStr[2]*2}"
        
        # Check named colors
        elif ColourStr in self.ColourMap:
            return self.ColourMap[ColourStr]
        
        return None
    
    def ParseTag(self, TagStr: str) -> Optional[str]:
        TagStr = TagStr.strip().lower()
        
        if TagStr in self.StyleMap:
            return self.StyleMap[TagStr]
        
        HexColour = self.ParseColour(TagStr)
        if HexColour:
            return HexColour
        
        return None
    
    def FormatString(self, Text: str) -> str:
        # Track active tags to handle reset properly
        ActiveTags = []
        Result = []
        
        def ProcessMatch(Match):
            nonlocal ActiveTags, Result
            TagSpec = Match.group(1).strip().lower()
            
            if TagSpec == "reset" or TagSpec == "normal":
                # Close all active tags in reverse order, one by one
                while ActiveTags:
                    Result.append(f"[/{ActiveTags.pop()}]")
                return ""
            else:
                # Handle regular tags (colors and styles)
                RichTag = self.ParseTag(TagSpec)
                if RichTag:
                    ActiveTags.append(RichTag)
                    return f"[{RichTag}]"
                else:
                    return Match.group(0)  # Return original if not recognized
        
        # Split text by tags and process each part
        LastEnd = 0
        for Match in self.TagPattern.finditer(Text):
            # Add text before the tag
            Result.append(Text[LastEnd:Match.start()])
            # Process the tag
            ProcessedTag = ProcessMatch(Match)
            if ProcessedTag:
                Result.append(ProcessedTag)
            LastEnd = Match.end()
        
        # Add remaining text
        Result.append(Text[LastEnd:])
        
        # Join all parts
        FormattedText = "".join(Result)
        
        # Auto-close any remaining tags at the end, in reverse order
        while ActiveTags:
            FormattedText += f"[/{ActiveTags.pop()}]"
        
        return FormattedText
    
    def Print(self, Text: str):
        Formatted = self.FormatString(Text)
        self.Console.print(Formatted)
    
    def GetAvailableColours(self) -> Dict[str, str]:
        return self.ColourMap.copy()
     
    def GetAvailableStyles(self) -> Dict[str, str]:
        return self.StyleMap.copy()

def FormatASCII(Lines, TargetLength:int|None=None):
    def ExtractVisibleText(Line):
        VisibleChars = []
        I = 0
        
        while I < len(Line):
            # Check for start of directive <:
            if I + 1 < len(Line) and Line[I:I+2] == "<:":
                # Find the end of directive :>
                EndPos = Line.find(":>", I + 2)
                if EndPos != -1:
                    # Skip the entire directive including :>
                    I = EndPos + 2
                else:
                    # Malformed directive, treat as visible character
                    VisibleChars.append((Line[I], I))
                    I += 1
            else:
                # Regular visible character
                VisibleChars.append((Line[I], I))
                I += 1
        
        return VisibleChars
    
    def GetVisibleLength(Line):
        return len(ExtractVisibleText(Line))
    
    def TruncateToTarget(Line, TargetLen):
        if TargetLen is None:
            return Line
        
        Line = EnsureResetEnding(Line)
        VisibleChars = ExtractVisibleText(Line)
        
        if len(VisibleChars) <= TargetLen:
            return Line
        
        if TargetLen == 0:
            CutoffPos = 0
        else:
            CutoffPos = VisibleChars[TargetLen - 1][1] + 1
        
        Result = []
        I = 0
        
        while I < len(Line):
            if I >= CutoffPos:
                # Check if we're in the middle of a directive
                if I + 1 < len(Line) and Line[I:I+2] == "<:":
                    # Find the end of this directive and include it
                    EndPos = Line.find(":>", I + 2)
                    if EndPos != -1:
                        # Include the complete directive
                        Result.extend(Line[I:EndPos+2])
                        I = EndPos + 2
                    else:
                        break
                else:
                    break
            else:
                Result.append(Line[I])
                I += 1
        
        ResultStr = "".join(Result)
        
        if not ResultStr.endswith("<:reset:>"):
            ResultStr += "<:reset:>"
        
        return ResultStr
    
    ProcessedLines = []
    for Line in Lines:
        ProcessedLine = EnsureResetEnding(Line)
        if TargetLength is not None:
            ProcessedLine = TruncateToTarget(ProcessedLine, TargetLength)
        ProcessedLines.append(ProcessedLine)
    
    if TargetLength is None:
        MaxVisibleLength = max(GetVisibleLength(Line) for Line in ProcessedLines)
    else:
        MaxVisibleLength = TargetLength
    
    AlignedLines = []
    for Line in ProcessedLines:
        VisibleLength = GetVisibleLength(Line)
        if VisibleLength < MaxVisibleLength:
            if Line.endswith("<:reset:>"):
                SpacesNeeded = MaxVisibleLength - VisibleLength
                AlignedLine = Line[:-10] + " " * SpacesNeeded + "<:reset:>"
            else:
                SpacesNeeded = MaxVisibleLength - VisibleLength
                AlignedLine = Line + " " * SpacesNeeded
        else:
            AlignedLine = Line
        
        AlignedLines.append(AlignedLine)
    
    return AlignedLines

def FormatInfoLines(InfoLines, TargetLength:int|None=None):
    if TargetLength==None:return InfoLines

    ResetLines = []
    for Line in InfoLines:
        ResetLines.append(EnsureResetEnding(Line))
    
    AlignedLines = []
    for Line in ResetLines:
        if len(RemoveDirectives(Line)) < TargetLength:
            AlignedLines.append(Line + " " * (TargetLength - len(RemoveDirectives(Line))))
        elif len(RemoveDirectives(Line)) > TargetLength:
            AlignedLines.append(EnsureResetEnding(RemoveDirectives(Line)[:TargetLength]))
        else:
            AlignedLines.append(Line)
    return AlignedLines

def Formatter(ASCIILines, InfoLines, TerminalWidth: int, ASCIIPosition="top", Spacing: int = 0) -> str:
    if ASCIIPosition not in ["top", "bottom", "left", "right"]:
        raise ValueError("ASCIIPosition must be 'top', 'bottom', 'right', or 'left'.")
    
    if ASCIIPosition == "top":
        return "\n".join(ASCIILines) + ("\n" * (Spacing or 0)) + "\n".join(InfoLines)
    elif ASCIIPosition == "bottom":
        return "\n".join(InfoLines) + ("\n" * (Spacing or 0)) + "\n".join(ASCIILines)
    elif ASCIIPosition == "left":
        ExtraLinesNeeded = len(InfoLines) - len(ASCIILines) if len(InfoLines) > len(ASCIILines) else 0
        for i in range(ExtraLinesNeeded):
            ASCIILines.append("")
        Output = ""

        MaxmimumASCIILength = max(len(RemoveDirectives(Line)) for Line in ASCIILines)
        MaximumInfoLength = max(len(RemoveDirectives(Line)) for Line in InfoLines)

        AllowedASCIIWidth = 0
        AllowedInfoWidth = 0

        if MaxmimumASCIILength + Spacing + MaximumInfoLength > TerminalWidth:
            AllowedASCIIWidth = TerminalWidth - (Spacing + MaximumInfoLength)
            AllowedInfoWidth = TerminalWidth - (Spacing + AllowedASCIIWidth)
        else:
            AllowedASCIIWidth = MaxmimumASCIILength
            AllowedInfoWidth = MaximumInfoLength

        FormattedInfoLines = FormatInfoLines(InfoLines, TargetLength=AllowedInfoWidth)
        FormattedASCIILines = FormatASCII(ASCIILines, TargetLength=AllowedASCIIWidth)

        if FormattedInfoLines is None or FormattedASCIILines is None:
            raise ValueError("Formatting functions returned None")

        for Index, Line in enumerate(FormattedASCIILines):
            if Index < len(FormattedInfoLines):
                Output += Line + (" " * Spacing if Spacing > 0 else "") + FormattedInfoLines[Index] + "\n"
            else:
                Output += Line + (" " * Spacing if Spacing > 0 else "") + "\n"
        
        return Output.rstrip("\n")
    
    elif ASCIIPosition == "right":
        ExtraLinesNeeded = len(InfoLines) - len(ASCIILines) if len(InfoLines) > len(ASCIILines) else 0
        for i in range(ExtraLinesNeeded):
            ASCIILines.append("")
        Output = ""

        MaximumASCIILength = max(len(RemoveDirectives(Line)) for Line in ASCIILines)
        MaximumInfoLength = max(len(RemoveDirectives(Line)) for Line in InfoLines)

        AllowedASCIIWidth = 0
        AllowedInfoWidth = 0

        if MaximumInfoLength + Spacing + MaximumASCIILength > TerminalWidth:
            AllowedASCIIWidth = TerminalWidth - (Spacing + MaximumInfoLength)
            AllowedInfoWidth = TerminalWidth - (Spacing + AllowedASCIIWidth)
        else:
            AllowedASCIIWidth = MaximumASCIILength
            AllowedInfoWidth = MaximumInfoLength

        FormattedInfoLines = FormatInfoLines(InfoLines, TargetLength=AllowedInfoWidth)
        FormattedASCIILines = FormatASCII(ASCIILines, TargetLength=AllowedASCIIWidth)

        if FormattedInfoLines is None or FormattedASCIILines is None:
            raise ValueError("Formatting functions returned None")

        for Index, Line in enumerate(FormattedInfoLines):
            if Index < len(FormattedASCIILines):
                Output += Line + (" " * Spacing if Spacing > 0 else "") + FormattedASCIILines[Index] + "\n"
            else:
                Output += Line + (" " * Spacing if Spacing > 0 else "") + "\n"
        
        return Output.rstrip("\n")
    
    raise ValueError(f"Unexpected ASCIIPosition value: \"{ASCIIPosition}\" valid values are 'top', 'bottom', 'left' and 'right'!") # For type safety, should never be reached.