[Setup]
AppName=Snakes Prototype
AppVerName=Snakes Prototype pre-alpha 0.0.1
DefaultDirName={pf}\Snakes Prototype
DefaultGroupName=Snakes Prototype
UninstallDisplayIcon={app}\main.exe
Compression=lzma2
SolidCompression=yes
OutputDir=setup_dist

[Dirs]
Name: "{app}\data"

[Files]
;Source: "dist/main.exe"; DestDir: "{app}"

Source: "dist/*"; DestDir: "{app}"
Source: "dist/data/*"; DestDir: "{app}/data"
Source: "dist/data/maps/*"; DestDir: "{app}/data/maps"
Source: "dist/data/fonts/*"; DestDir: "{app}/data/fonts"
Source: "dist/data/graphs/*"; DestDir: "{app}/data/graphs"

;Source: "Readme.txt"; DestDir: "{app}"; Flags: isreadme

[Icons]
Name: "{group}\Snakes Prototype"; Filename: "{app}\main.exe"
