MinecraftDeathLogger
====================

Works for Minecraft 1.8.X, should be working for every version from 1.0.0 up, but they have not been tested.

This is a python script, which checks the logs of a minecraft server for any death message. By default it only checks new deathmessages, which were added to the file after the script has been started. A function 'actionOnDeath' is defined at the top and can be modified to execute own scripts and actions when someone died.

Options to set at the top are the location of the log file, the location of an up-to-date Minecraft language file (to specify which death messages exist), and the interval how often the log should be checked.

lang.txt - The MC language file. Always extract it yourself to have an up-to-date version.
