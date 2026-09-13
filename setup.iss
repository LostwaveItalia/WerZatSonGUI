[Setup]
; Basic Installer Configuration
AppName=WerZatSonGUI
AppVersion=2.0.0
AppPublisher=LostwaveItalia
AppPublisherURL=https://github.com/LostwaveItalia/WerZatSonGUI
AppSupportURL=https://github.com/LostwaveItalia/WerZatSonGUI/issues
AppUpdatesURL=https://github.com/LostwaveItalia/WerZatSonGUI/releases
VersionInfoVersion=2.0.0.0
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
WizardStyle=modern dynamic
UsePreviousAppDir=no
UsePreviousGroup=no
DisableWelcomePage=no
SetupIconFile=assets\logo.ico
WizardSmallImageFile=assets\logo.png

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "italian"; MessagesFile: "Languages\Italian.isl"
Name: "french"; MessagesFile: "Languages\French.isl"
Name: "portuguese"; MessagesFile: "Languages\BrazilianPortuguese.isl"

[CustomMessages]
english.DesktopIconDesc=Create a desktop shortcut
english.AdditionalShortcuts=Additional shortcuts:
english.InstallingDepsStatus=Installing dependencies (Node.js, Python, FFmpeg, Rust, C++ Tools)... you may be asked to confirm a couple of installs
english.LaunchAppDesc=Launch Application Now
english.InstallModeTitle=Installation Mode
english.InstallModeDesc=Please choose how you want to install WerZatSonGUI.
english.InstallModeAll=Install for all users
english.InstallModeUser=Install just for me

italian.DesktopIconDesc=Crea un collegamento sul desktop
italian.AdditionalShortcuts=Collegamenti aggiuntivi:
italian.InstallingDepsStatus=Installazione delle dipendenze (Node.js, Python, FFmpeg, Rust, strumenti per C++)... potrebbe venirti chiesto di confermare un paio di installazioni
italian.LaunchAppDesc=Avvia l'applicazione ora
italian.InstallModeTitle=Modalità di installazione
italian.InstallModeDesc=Scegli per chi desideri installare WerZatSonGUI.
italian.InstallModeAll=Installa per tutti gli utenti
italian.InstallModeUser=Installa solo per me

french.DesktopIconDesc=Créer un raccourci sur le bureau
french.AdditionalShortcuts=Raccourcis supplémentaires:
french.InstallingDepsStatus=Installation des dépendances (Node.js, Python, FFmpeg, Rust, outils C++)... il se peut qu'on vous demande de confirmer certaines installations
french.LaunchAppDesc=Lancer l'application maintenant
french.InstallModeTitle=Mode d'installation
french.InstallModeDesc=Veuillez choisir pour qui vous souhaitez installer WerZatSonGUI.
french.InstallModeAll=Installer pour tous les utilisateurs
french.InstallModeUser=Installer uniquement pour moi

portuguese.DesktopIconDesc=Criar um atalho na área de trabalho
portuguese.AdditionalShortcuts=Atalhos adicionais:
portuguese.InstallingDepsStatus=Instalando dependências (Node.js, Python, FFmpeg, Rust, ferramentas C++)... pode ser necessário confirmar algumas instalações
portuguese.LaunchAppDesc=Iniciar o aplicativo agora
portuguese.InstallModeTitle=Modo de instalação
portuguese.InstallModeDesc=Escolha para quem deseja instalar o WerZatSonGUI.
portuguese.InstallModeAll=Instalar para todos os usuários
portuguese.InstallModeUser=Instalar apenas para mim

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
var
  InstallModePage: TInputOptionWizardPage;
  LastSelectedMode: Integer; 

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
  if (CurStep = ssPostInstall) and (ActiveLanguage = 'french') then
  begin
    ConfigPath := ExpandConstant('{app}\config.json');
    
    
    if LoadStringFromFile(ConfigPath, ConfigContentAnsi) then
    begin
    
      ConfigContentStr := string(ConfigContentAnsi);
      
      
      StringChangeEx(ConfigContentStr, '"language": "English"', '"language": "Français"', False);
      
      
      ConfigContentAnsi := AnsiString(ConfigContentStr);
      
      
      SaveStringToFile(ConfigPath, ConfigContentAnsi, False);
    end;
  end;
  if (CurStep = ssPostInstall) and (ActiveLanguage = 'portuguese') then
  begin
    ConfigPath := ExpandConstant('{app}\config.json');
    
    
    if LoadStringFromFile(ConfigPath, ConfigContentAnsi) then
    begin
    
      ConfigContentStr := string(ConfigContentAnsi);
      
      
      StringChangeEx(ConfigContentStr, '"language": "English"', '"language": "Português"', False);
      
      
      ConfigContentAnsi := AnsiString(ConfigContentStr);
      
      
      SaveStringToFile(ConfigPath, ConfigContentAnsi, False);
    end;
  end;
end;

// Install logic
procedure InitializeWizard;
begin
  // Create a custom page right after the Welcome page
  InstallModePage := CreateInputOptionPage(wpWelcome,
    CustomMessage('InstallModeTitle'), CustomMessage('InstallModeDesc'),
    '', True, False);
  InstallModePage.Add(CustomMessage('InstallModeAll'));
  InstallModePage.Add(CustomMessage('InstallModeUser'));
  
  // Default to the first option (All users)
  InstallModePage.SelectedValueIndex := 0;
  LastSelectedMode := -1; // Force an update the first time the page loads
end;

procedure CurPageChanged(CurPageID: Integer);
begin
  // Updates the path when arriving at the Directory page
  // Only if the mode was changed (or it's the first time)
  // This should ensure user-typed paths aren't wiped if they click Back and Next
  if CurPageID = wpSelectDir then
  begin
    if InstallModePage.SelectedValueIndex <> LastSelectedMode then
    begin
      if InstallModePage.SelectedValueIndex = 0 then
        WizardForm.DirEdit.Text := ExpandConstant('{sd}\WerZatSonGUI')
      else
        WizardForm.DirEdit.Text := GetEnv('USERPROFILE') + '\WerZatSonGUI';
        
      LastSelectedMode := InstallModePage.SelectedValueIndex;
    end;
  end;
end;