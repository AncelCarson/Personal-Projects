Set WshShell = CreateObject("WScript.Shell")
cmds=WshShell.RUN("""C:\Users\Ancel Carson\Documents\Coding\Python\Anti Yodol Box\nircmd\nircmd.exe"" setdefaultsounddevice ""Speakers""", 0, True)
cmds=WshShell.RUN("""C:\Users\Ancel Carson\Documents\Coding\Python\Anti Yodol Box\nircmd\nircmd.exe"" mutesysvolume ""0""", 0, True)
cmds=WshShell.RUN("""C:\Users\Ancel Carson\Documents\Coding\Python\Anti Yodol Box\nircmd\nircmd.exe"" setsysvolume ""49151""", 0, True)
Set WshShell = Nothing