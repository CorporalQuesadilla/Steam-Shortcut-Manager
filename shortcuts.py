#-------------------------------------------------------------------------------
# Name:        Steam Shortcut Manager
# Purpose:     Command line tool to add non-Steam application shortcuts.
#              Intended to be used in conjunction with a tool that automates the adding of shortcuts.
#              In addition to adding the shortcut, the steam://rungameid/### is returned.
#              Close Steam before running!
#
#              Currently hardcoded to Windows Steam installations in C:\Program Files (x86)\Steam\
#              I'll probably change this at some point, but for now it should take only a second to put in your path to Steam.
#              Otherwise, this should be cross-platform with Linux/Mac.
#
#              I might make a GUI, or support removing shortcuts at some point. For now, it just adds shortcuts.
#
#              Oh, and you NEED to have an existing shortcuts.vdf - basically, add at least one non-steam shortcut via the GUI.
#              This is an incredibly simple fix for me to implement, I'm just lazy.
#
#              For more information, I'll probably document the file format itself somewhere on a github wiki page sometime.
#              https://github.com/CorporalQuesadilla/Steam-Shortcut-Manager/wiki
#
# Usage:       Run from commandline. Needs the following arguments in this order:
#              Argument                 Explanation
#              --------                 -----------
#              UserID                   Your personal ID - steamID3 [U:1:THIS_PART_HERE_COPY_ME] from https://steamidfinder.com/
#                                           This is for the local path to your shortcuts.vdf file we're modifying,
#                                           located in \Path\To\Steam\userdata\USERIDHERE\config\shortcuts.vdf
#              Name of program          Whatever you want to call it. In double quotes if it has spaces or other funky characters
#              Path to program or URL   In double quotes if the path has spaces or other funky characters
#              Path to start program    Basically the folder it's in (use double quotes)
#              Path to icon             Optional place to source the icon. In double quotes. BTW, I'm not sure where the Grid/BigPicture image comes from
#              Shortcut path            No idea what this is. Just do "" (literally 'the empty string' - two double quotes in a row)
#              Launch options           Probably needs double quotes if you got any spaces or other funky characters in there
#              Hidden?                  Put a 1 here to make it only visible under "Hidden", anything else won't hide it. You need something though. 0 is fine.
#              Allow Desktop Config?    Use controller's Desktop Configurations in this game. Put a 1 to enable it, anything else to disable. You need something though. 0 is fine.
#              Allow Steam Overlay?     Put a 1 to enable it, anything else to disable. You need something though. 0 is fine.
#              In VR library?           For the 'VR Library' Category. Put a 1 to enable it, anything else to disable. You need something though. 0 is fine.
#              Last Play Time           Date last played. No idea how this works yet. For now, put 0 and I'll take care of it (mark it as "Never Played")
#              Categories               Any categories you want it to appear in. If you use spaces in a category name, put it in double quotes
#
#              Example:
#              shortcuts.py UserID WoohooMyProgramWorks C:\d.exe C:\ "C:\Program Files (x86)\Steam\bin\steamservice.exe" "" WHATUPLAUNCH 0 1 1 1 0 tag1 tag2
#
# Author:      Corporal Quesadilla
#
# Created:     2018.07.15
# Copyright:   (c) Corporal Quesadilla 2018
# Licence:     Everything in this file is under GPL v3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
#              with the exception of the getURL() function, which is under MIT license and adapted from Scott Rice's ICE application
#              https://github.com/scottrice/Ice/blob/7130b54c8d2fa7d0e2c0994ca1f2aa3fb2a27ba9/ice/steam_grid.py
#
#              Since I have adapted these few lines of code, I must include the following (between the sets of three asterisks)
#              ***
#              Copyright (c) 2012-2013, 2013 Scott Rice
#              All rights reserved.
#
#              Permission is hereby granted, free of charge, to any person obtaining a copy
#              of this software and associated documentation files (the "Software"), to
#              deal in the Software without restriction, including without limitation the
#              rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#              sell copies of the Software, and to permit persons to whom the Software is
#              furnished to do so, subject to the following conditions:
#
#              The above copyright notice and this permission notice shall be included in
#              all copies or substantial portions of the Software.
#
#              THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#              IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#              FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#              AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#              LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#              FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
#              IN THE SOFTWARE.
#              ***
#-------------------------------------------------------------------------------
import sys
import crc_algorithms

def findLastEntryNumberAndPosition(pathToShortcutsVDF):
    foundChars = 1
    target = '\x00\x01appname'
    lookingfor = 'target'
    lastEntryNumber = ''

    # TODO: Change path. Get that instead of ID from argument?
    #f = open('C:\\Program Files (x86)\\Steam\\userdata\\' + str(pathToShortcutsVDF) + '\\config\\shortcuts.vdf', 'r')
    f = open(str(pathToShortcutsVDF), 'r')
    fileContents = f.read()

    for i in range(len(fileContents)):
        #print i
        #print repr(fileContents[-i])
        if lookingfor == 'target':
            if (fileContents[-i]) == target[-foundChars]:
                #print repr(target[-foundChars]) + " found"
                foundChars = foundChars + 1
                if foundChars > len(target):
                    lookingfor = 'number'
            else:
                foundChars = 1
                # make sure current character didn't 'restart' the pattern
                # yeah I know copy-paste code sucks
                if (fileContents[-i]) == target[-foundChars]:
                    #print repr(target[-foundChars]) + " found"
                    foundChars = foundChars + 1
                    if foundChars > len(target):
                        lookingfor = 'number'
        else:
            if (fileContents[-i]).isdigit():
                #print repr(fileContents[-i]) + " found"
                lastEntryNumber = str((fileContents[-i])) + str(lastEntryNumber)
                lastEntryPosition = len(fileContents) - i
            else:
                break
    #print repr(fileContents[lastEntryPosition+266]) + "hey"
    f.close()
    return (lastEntryNumber, lastEntryPosition)

def addEntry(pathToShortcutsVDF, inputTuple):
    #f = open('C:\\Program Files (x86)\\Steam\\userdata\\' + str(pathToShortcutsVDF) + '\\config\\shortcuts.vdf', 'r+')
    f = open(str(pathToShortcutsVDF), 'r+')
    #f.close()
    fileContents = f.read()
    f.seek(len(fileContents) - 2)
    endFileContents = f.read()
    f.seek(len(fileContents) - 2)
    f.write(createEntry(inputTuple) + endFileContents)
    #f.truncate()
    f.close()

def createEntry(inputTuple):
    '''
    # Variables
    Title = 'Paint (testing)'
    Type = 'exe'
    quotedPath = "\"C:\\c.exe\""
    quotedStartDir = "\"C:\\\""
    entryID = str(int(lastEntryInfo[0])+1)

    # Delimiter Structures
    delim_header = '\x00'
    delim_appname = '\x00\x01appname\x00'
    delim_type = '\x00\x01'
    delim_path = '\x00'
    delim_startdir = '\x00\x01StartDir\x00'

    newEntry = delim_header + entryID + delim_appname + str(Title) + delim_type + str(Type) + delim_path + str(quotedPath) + delim_startdir + str(quotedStartDir) + '\x00\x01icon\x00' + '\x00\x01ShortcutPath\x00\x00\x01LaunchOptions\x00\x00\x02IsHidden\x00\x00\x00\x00\x00\x02AllowDesktopConfig\x00\x01\x00\x00\x00\x02AllowOverlay\x00\x01\x00\x00\x00\x02OpenVR\x00\x00\x00\x00\x00\x02LastPlayTime\x00\x00\x00\x00\x00\x00tags\x00\x08\x08'
    '''

    var_entryID         = inputTuple[0]
    var_appName         = inputTuple[1]
    var_unquotedPath    = inputTuple[2]
    var_startDir        = inputTuple[3]
    var_iconPath        = inputTuple[4]
    var_shortcutPath    = inputTuple[5]
    var_launchOptions   = inputTuple[6]
    var_isHidden        = inputTuple[7]
    var_allowDeskConf   = inputTuple[8]
    var_allowOverlay    = inputTuple[9]
    var_openVR          = inputTuple[10]
    var_lastPlayTime    = inputTuple[11]
    var_tags            = inputTuple[12]


    # There are several parts to an entry, all on one line.
    # The data type refers to the input - \x01 indicates String, \x02 indicates boolean, \x00 indicates list
    # Strings must be encapsulated in quotes (aside from launch options)
    # Bools treat '\x01' as True and '\x00' as False
    # Lists are as follows: '\x01' + index + '\x00' + tagContents + '\x00'
    # I have no idea about Date. Not sure why LastPlayTime is marked as a bool.
    #   4 characters, usually ending in '[' (maybe?). All 4 being '\x00' is fine too (default?).


    # Key                # Data Type  # Internal Name       # Delimiter     # Input             # Delimiter
    full_entryID        =                                      '\x00'  +  var_entryID        +  '\x00'
    full_appName        =  '\x01'  +  'appname'             +  '\x00'  +  var_appName        +  '\x00'
    full_quotedPath     =  '\x01'  +  'exe'                 +  '\x00'  +  var_unquotedPath   +  '\x00'
    full_startDir       =  '\x01'  +  'StartDir'            +  '\x00'  +  var_startDir       +  '\x00'
    full_iconPath       =  '\x01'  +  'icon'                +  '\x00'  +  var_iconPath       +  '\x00'
    full_shortcutPath   =  '\x01'  +  'ShortcutPath'        +  '\x00'  +  var_shortcutPath   +  '\x00'
    full_launchOptions  =  '\x01'  +  'LaunchOptions'       +  '\x00'  +  var_launchOptions  +  '\x00'
    full_isHidden       =  '\x02'  +  'IsHidden'            +  '\x00'  +  var_isHidden       +  '\x00\x00\x00'
    full_allowDeskConf  =  '\x02'  +  'AllowDesktopConfig'  +  '\x00'  +  var_allowDeskConf  +  '\x00\x00\x00'
    full_allowOverlay   =  '\x02'  +  'AllowOverlay'        +  '\x00'  +  var_allowOverlay   +  '\x00\x00\x00'
    full_openVR         =  '\x02'  +  'OpenVR'              +  '\x00'  +  var_openVR         +  '\x00\x00\x00'
    full_lastPlayTime   =  '\x02'  +  'LastPlayTime'        +  '\x00'  +  var_lastPlayTime
    full_tags           =  '\x00'  +  'tags'                +  '\x00'  +  var_tags           +  '\x08\x08'

    newEntry = full_entryID + full_appName + full_quotedPath + full_startDir + full_iconPath + full_shortcutPath + full_launchOptions + full_isHidden + full_allowDeskConf + full_allowOverlay + full_openVR + full_tags
    return newEntry
    pass

def inputPreperation(args, lastEntryInfo):
    var_entryID = str(int(lastEntryInfo[0])+1)

    # Strings
    var_appName         =       args[2]
    var_unquotedPath    = '"' + args[3] + '"'
    var_startDir        = '"' + args[4] + '"'
    var_iconPath        = '"' + args[5] + '"'
    var_shortcutPath    = '"' + args[6] + '"' # quoted? what is this?
    var_launchOptions   =       args[7]

    # Boolean checks
    if args[8] == '1':
        var_isHidden = '\x01'
    else:
        var_isHidden = '\x00'
    if args[9] == '1':
        var_allowDeskConf = '\x01'
    else:
        var_allowDeskConf = '\x00'
    if args[10] == '1':
        var_allowOverlay = '\x01'
    else:
        var_allowOverlay = '\x00'
    if args[11] == '1':
        var_openVR = '\x01'
    else:
        var_openVR = '\x00'

    # Date
    # Since the format hasn't been cracked yet, I'll populate with default
    #   values if you just keep it as '0'
    var_tags= ''
    if args[12] == '0':
        var_lastPlayTime = '\x00\x00\x00\x00'
    else:
        var_lastPlayTime = args[12]

    for tag in range(13,len(args)-1):
        var_tags = var_tags + '\x01' + str(tag-13) + '\x00' + args[tag] + '\x00'

    return (var_entryID, var_appName, var_unquotedPath, var_startDir, var_iconPath, var_shortcutPath, var_launchOptions, var_isHidden, var_allowDeskConf, var_allowOverlay, var_openVR, var_lastPlayTime, var_tags)

def getURL(inputTuple):
    # Comments by Scott Rice:
    """
    Calculates the filename for a given shortcut. This filename is a 64bit
    integer, where the first 32bits are a CRC32 based off of the name and
    target (with the added condition that the first bit is always high), and
    the last 32bits are 0x02000000.
    """
    # This will seem really strange (where I got all of these values), but I
    # got the xor_in and xor_out from disassembling the steamui library for
    # OSX. The reflect_in, reflect_out, and poly I figured out via trial and
    # error.
    algorithm = crc_algorithms.Crc(width = 32, poly = 0x04C11DB7, reflect_in = True, xor_in = 0xffffffff, reflect_out = True, xor_out = 0xffffffff)
    input_string = ''.join([inputTuple[2],inputTuple[1]])
    top_32 = algorithm.bit_by_bit(input_string) | 0x80000000
    full_64 = (top_32 << 32) | 0x02000000
    return str(full_64)

def main():
    pathToShortcutsVDF = sys.argv[1]
    print pathToShortcutsVDF
    # fileExistenceCheck()
    lastEntryInfo = findLastEntryNumberAndPosition(pathToShortcutsVDF)
    inputTuple = inputPreperation(sys.argv, lastEntryInfo)

    #print lastEntryInfo[0] + 'pp'
    addEntry(pathToShortcutsVDF, inputTuple)

    print getURL(inputTuple)
main()