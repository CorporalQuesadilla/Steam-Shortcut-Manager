# Steam Shortcut Manager

This is a command-line tool to add non-Steam application shortcuts. You pass a set of options about the program you want to add (name, path, categories, etc.) and in return it'll appear the next time you launch Steam - just as if you had added/configured it from the official Steam GUI. Additionally, it will generate the appid to launch the game through steam through the command line. (e.g. steam://rungameid/###)

This is intended to be used in conjunction with a tool that automates the adding of shortcuts. But you can totally use it on your own, too!

## Getting Started

Make sure Steam is closed. Not sure if there's any harm keeping it open, but I do know Steam won't reflect changes made here until next time it's launched.

Run the program from the command line. Be sure to download both .py files.

## Example
```
python shortcuts.py "C:\Program Files (x86)\Steam\userdata\ID_HERE\config\shortcuts.vdf" WoohooMyProgramWorks C:\d.exe C:\ "C:\Program Files (x86)\Steam\bin\steamservice.exe" "" WHATUPLAUNCH 0 1 1 1 0 FPS Puzzle
```
will add a shortcut called "WoohooMyProgramWorks" to Steam. It launches d.exe, which is located in C:\. It's custom icon is the one used for steamservice.exe. The argument (launch option) "WHATUPLAUNCH" is passed to d.exe when launching the shortcut. It is not marked as Hidden. It uses any Steam Input-supported controller's Desktop Configuration (for launchers and stuff), allows the Steam Overlay, is in the VR Library, has never been played before, and is in the FPS and Puzzle categories.

You need to fill out every argument in this order:

              Argument                 Explanation
              --------                 -----------
              Path to Shortcuts.vdf    Requires Your personal ID - steamID3 [U:1:THIS_PART_HERE_COPY_ME] from https://steamidfinder.com/
                                           This is for the local path to your shortcuts.vdf file we're modifying,
                                           located in \Path\To\Steam\userdata\USERIDHERE\config\shortcuts.vdf. Use double quotes.
              Name of program          Whatever you want to call it. In double quotes if it has spaces or other funky characters
              Path to program or URL   In double quotes if the path has spaces or other funky characters
              Path to start program    Basically the folder it's in (use double quotes)
              Path to icon             Optional place to source the icon. In double quotes. BTW, I'm not sure where the Grid/BigPicture image comes from
              Shortcut path            No idea what this is. Just do "" (literally 'the empty string' - two double quotes in a row)
              Launch options           Probably needs double quotes if you got any spaces or other funky characters in there
              Hidden?                  Put a 1 here to make it only visible under "Hidden", anything else won't hide it. You need something though. 0 is fine.
              Allow Desktop Config?    Use controller's Desktop Configurations in this game. Put a 1 to enable it, anything else to disable. You need something though. 0 is fine.
              Allow Steam Overlay?     Put a 1 to enable it, anything else to disable. You need something though. 0 is fine.
              In VR library?           For the 'VR Library' Category. Put a 1 to enable it, anything else to disable. You need something though. 0 is fine.
              Last Play Time           Date last played. No idea how this works yet. For now, put 0 and I'll take care of it (mark it as "Never Played")
              Categories               Any categories you want it to appear in. If you use spaces in a category name, put it in double quotes

### Prerequisites

Just Python. I made this having 2.7 installed, but it's probably compatible with 3. I can port it if neccessary.

Oh, and make sure your Steam\userdata\ID_HERE\config\shortcuts.vdf exists. Maybe just manually add one shortcut first before using this tool.

If you don't know your ID, get it from here: steamID3 [U:1:THIS_PART_HERE_COPY_ME] from https://steamidfinder.com/

### How it works

See here: https://github.com/CorporalQuesadilla/Steam-Shortcut-Manager/wiki/Steam-Shortcuts-Documentation

## License

This project is licensed under SEE LICENSE.MD

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
