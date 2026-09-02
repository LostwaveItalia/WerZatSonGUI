[Setup]
; Basic Installer Configuration
AppName=WerZatSonGUI
AppVersion=1.3.0
AppPublisher=LostwaveItalia
AppPublisherURL=https://github.com/LostwaveItalia/WerZatSonGUI-dev
AppSupportURL=https://github.com/LostwaveItalia/WerZatSonGUI-dev/issues
AppUpdatesURL=https://github.com/LostwaveItalia/WerZatSonGUI-dev/releases
VersionInfoVersion=1.3.0.0
VersionInfoCompany=WerZatSonGUI
VersionInfoDescription=WerZatSonGUI Installer
VersionInfoCopyright=WerZatSonGUI
DefaultDirName={sd}\WerZatSonGUI
DefaultGroupName=WerZatSonGUI
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
OutputDir=output
OutputBaseFilename=WerZatSonGUI_Installer
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableWelcomePage=no
SetupIconFile=assets\logo.ico
WizardSmallImageFile=assets\logo.png

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "italian"; MessagesFile: "Languages\Italian.isl"

[CustomMessages]
english.DesktopIconDesc=Create a desktop shortcut
italian.DesktopIconDesc=Crea un collegamento sul desktop
english.AdditionalShortcuts=Additional shortcuts:
italian.AdditionalShortcuts=Collegamenti aggiuntivi:
english.InstallingDepsStatus=Installing dependencies (Node.js, Python, FFmpeg, Rust, C++ Tools)... you may be asked to confirm a couple of installs
italian.InstallingDepsStatus=Installazione delle dipendenze (Node.js, Python, FFmpeg, Rust, strumenti per C++)... potrebbe venirti chiesto di confermare un paio di installazioni
english.LaunchAppDesc=Launch Application Now
italian.LaunchAppDesc=Avvia l'applicazione ora

[Files]
; Helper files for installing dependencies
Source: "setup_deps.ps1"; DestDir: "{app}"; Flags: ignoreversion
Source: "get_pip.py"; DestDir: "{app}"; Flags: ignoreversion

; IMPORTANT: Place your actual files in the same directory as this .iss script
Source: "WerZatSonGUI.pyw"; DestDir: "{app}"; Flags: ignoreversion
Source: "requirements.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "config.json"; DestDir: "{app}"; Flags: ignoreversion
Source: "package.json"; DestDir: "{app}"; Flags: ignoreversion
; Add any additional files/folders your program needs below:
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "input"; DestDir: "{app}\input"; Flags: ignoreversion recursesubdirs createallsubdirs

[Tasks]
Name: "desktopicon"; Description: "{cm:DesktopIconDesc}"; GroupDescription: "{cm:AdditionalShortcuts}"

[Icons]
Name: "{group}\WerZatSonGUI"; Filename: "{app}\WerZatSonGUI.pyw"; WorkingDir: "{app}"; IconFilename: "{app}\assets\logo.ico"
Name: "{group}\Uninstall WerZatSonGUI"; Filename: "{uninstallexe}"
Name: "{autodesktop}\WerZatSonGUI"; Filename: "{app}\WerZatSonGUI.pyw"; WorkingDir: "{app}"; IconFilename: "{app}\assets\logo.ico"; Tasks: desktopicon

[Run]
; 1. Execute the dependency setup script (passing the installer's own active language
; through, so setup_deps.ps1's console output matches it too)
Filename: "powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -File ""{app}\setup_deps.ps1"" -AppDir ""{app}"" -Language ""{language}"""; StatusMsg: "{cm:InstallingDepsStatus}"; Flags: waituntilterminated

; 2. Clean up ALL installer helper files so no trace is left behind
Filename: "cmd.exe"; Parameters: "/c del /f /q ""{app}\setup_deps.ps1"" ""{app}\get_pip.py"""; Flags: runhidden
Filename: "cmd.exe"; Parameters: "/c rmdir /s /q ""{app}\output"" ""{app}\input"""; Flags: runhidden

; 3. Launch Application on Finish
Filename: "powershell.exe"; Parameters: "-NoProfile -ExecutionPolicy Bypass -Command ""$env:Path = [System.Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [System.Environment]::GetEnvironmentVariable('Path', 'User'); Start-Process pythonw -ArgumentList '{app}\WerZatSonGUI.pyw'"""; Description: "{cm:LaunchAppDesc}"; Flags: postinstall nowait runhidden

[UninstallDelete]
; This tells the uninstaller to completely wipe the installation folder and any 
; generated files (like node_modules or cache) when the user uninstalls your app.
Type: filesandordirs; Name: "{app}"

[Code]
// If Setup itself ran in Italian, also switch the freshly-installed config.json's
// default language to Italiano, so WerZatSonGUI opens in the same language you just
// installed in instead of always landing on English first.
procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigPath: string;
  ConfigContentAnsi: AnsiString;
  ConfigContentStr: string;
begin
  if (CurStep = ssPostInstall) and (ActiveLanguage = 'italian') then
  begin
    ConfigPath := ExpandConstant('{app}\config.json');
    
    // 1. Load the file into an AnsiString
    if LoadStringFromFile(ConfigPath, ConfigContentAnsi) then
    begin
      // 2. Convert to standard string for manipulation
      ConfigContentStr := string(ConfigContentAnsi);
      
      // 3. Perform the string replacement on the standard string
      StringChangeEx(ConfigContentStr, '"language": "English"', '"language": "Italiano"', False);
      
      // 4. Convert back to AnsiString for saving
      ConfigContentAnsi := AnsiString(ConfigContentStr);
      
      // 5. Save the updated file
      SaveStringToFile(ConfigPath, ConfigContentAnsi, False);
    end;
  end;
end;