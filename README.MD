# Steam Shortcut Manager

This is a cross-platform command-line tool to add non-Steam application shortcuts. You pass a set of options about the program you want to add (name, path, categories, etc.) and in return it'll appear the next time you launch Steam - just as if you had added/configured it from the official Steam GUI. Additionally, it will generate the appid to launch the game through steam through the command line. (e.g. steam://rungameid/###)

This is intended to be used in conjunction with a tool that automates the adding of shortcuts. But you can totally use it on your own, too!

Personally, I plan to use it to launch all my games through Steam for controller support and a unified library. That includes GOG:// or similar links, so that even uninstalled games from 3rd party libraries will work!

Ideally, you could use another application (such as Playnite) to build up your GOG/Steam/Emulated/etc. libraries into one database, then write a basic script to pass all those into Steam using this application!

# Documentation

If you're just here because you're interested in how Steam shortcuts and steam:// links are stored/generated, look [here](https://github.com/CorporalQuesadilla/Steam-Shortcut-Manager/wiki/Steam-Shortcuts-Documentation) for documentation.

If you're here for documentation on how this program works, continue reading.

Please note that there are some differences in the arguments my program expects vs. how Steam actually stores shortcuts - the documentation below is simply for the "easy" input my program can be given in order to generate the funky input that Steam actually needs. This prevents the user from worrying about funky ASCII characters or quote encapsulation. It's much easier to type 0 than (insert series of invisible characters here).

# Getting Started

Make sure Steam is closed. Not sure if there's any harm keeping it open, but I do know Steam won't reflect changes made here until next time it's launched.

Run the program (shortcuts.py) from the command line. Be sure to download both .py files and keep them in the same directory, though.

# Example
```
python shortcuts.py "C:\Program Files (x86)\Steam\userdata\ID_HERE\config\shortcuts.vdf" "Super Video Game IV" "C:\SVG IV.exe" C:\ "C:\Path to\an\icon\someEXEorICO.exe" "" "-fullscreen heckno" 0 1 1 1 0 FPS Puzzle
```
will add a shortcut called "WoohooMyProgramWorks" to Steam. It launches "SVG IV.exe", which is located in C:\. It's custom icon is the one used for someEXEorICO.exe. The argument (launch option) "-fullscreen heckno" is passed to "SVG IV.exe" when launching the shortcut. It is not marked as Hidden. It uses any Steam Input-supported controller's Desktop Configuration (for launchers and stuff I think), allows the Steam Overlay, is in the VR Library, has never been played before, and is in the FPS and Puzzle categories.

You need to fill out every argument in the following order. If any argument has spaces or other funky characters (such as the title in my example, which has multiple) you'll need to encapsulate the entire argument with double quotes. To be safe, you probably should do this no matter what.

# Arguments
Argument | Explanation
-------- | -----------
Path to Shortcuts.vdf | Requires Your personal ID - steamID3 [U:1:THIS_PART_HERE_COPY_ME] from https://steamidfinder.com/ This is for the local path to your shortcuts.vdf file we're modifying, located in \Path\To\Steam\userdata\USERIDHERE\config\shortcuts.vdf.
Name of program | Whatever you want to call it. This is how it appears in Steam.
Path to program or URL | Direct path to executable file or URL. That means that steam:// or GOG:// links work.
Path to start program | Basically the path to the folder the game is in. Take the path above and cut the executable file out. If it's a URL, I think you can just leave this blank.
Path to icon | Optional place to source the icon. BTW, I'm not sure where the Grid/BigPicture image comes from.
Shortcut path | No idea what this is. Just do "" (literally 'the empty string' - two double quotes in a row)
Launch options | Anything to pass to the exe.
Hidden? | Put a 1 here to make it only visible under "Hidden", anything else won't hide it. You need something though. 0 is fine.
Allow Desktop Config? | Use controller's Desktop Configurations in this game. Put a 1 to enable it, anything else to disable. You need to put some argument here. 0 is fine.
Allow Steam Overlay? | Put a 1 to enable it, anything else to disable. You need something though. 0 is fine.
In VR library? | For the 'VR Library' Category. Put a 1 to enable it, anything else to disable. You need something though. 0 is fine.
Last Play Time | Date last played. No idea how this works yet. For now, put 0 and I'll take care of it (defaulting to "Never Played".) Steam will update this once you actually start playing. I don't know why you'd want to fake it with anything else anyways.
Categories | Any categories you want it to appear in. Categories are separated by spaces. If you want to use spaces in a category name, put it in double quotes. Everything from this point onward is a category, you can do as many as you like.

# Prerequisites

Just Python. I made this having 2.7 installed, but it's probably compatible with 3. I can port it if neccessary.

Oh, and make sure your Steam\userdata\ID_HERE\config\shortcuts.vdf exists. Maybe just manually add one shortcut first before using this tool.

If you don't know your ID, get it from here: steamID3 [U:1:THIS_PART_HERE_COPY_ME] from https://steamidfinder.com/

# How it works

I simply modify shortcuts.vdf based on what I've seen in other entries generated by Steam itself. You can read more here: https://github.com/CorporalQuesadilla/Steam-Shortcut-Manager/wiki/Steam-Shortcuts-Documentation

As for the steam:// ID generation, see the comment used in the excerpt of Scott Rice's code in shortcuts.py in the GetURL() function.

# Future Roadmap

In no particular order:
* Further document attributes I don't understand (time played, shortcut path) and what values are accepted/how they're interpreted.
* Support users who don't have an existing shortcuts.vdf (should be simple to create a new one)
* Test to make sure this works on Linux/Mac (or have other users confirm). I don't see why it wouldn't work, though.
* Detect broken files or other malformed data to prevent making issues worse. This also includes the ability to recognize any new attributes Steam may have added so that I don't break the entire file by creating entries with missing attributes.
* Further documentation on what acceptable values for attributes are. (i.e. can stuff be missing, etc.)
* Friendlier "experience" - stop asking for things everyone leaves blank by default, like last played date. Accept having no tags. Automatically determine "starting path" from path to executable.
* Ability to remove shortcuts (perhaps based on id or appname?)

# License

SEE LICENSE.MD

# Acknowledgments

* Scott Rice for ICE, or rather his work finding how steam:// IDs are generated.
* PsychoTheHedgehog for also documenting how shortcuts.vdf is laid out. Unfortunately, their work was trashed some time ago and the Google cached version dissappeared sometime in July 2018. It turns out they had discovered essentially the same things I had, but at least it's reassuring to find someone else had documented almost the exact the same things. Their documentation was fairly old (missing some variables added in recent years) and I wasn't a fan of how it was explained anyways, but hey, credit to them for independently finding the same things first. Hopefully my documentation here will remain updated and accessible, as it seems to be the only documentation publicly available now.
