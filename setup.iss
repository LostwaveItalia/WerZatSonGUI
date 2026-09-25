[Setup]
; Basic Installer Configuration
AppName=WerZatSonGUI
AppVersion=2.1.3
AppPublisher=LostwaveItalia
AppPublisherURL=https://github.com/LostwaveItalia/WerZatSonGUI
AppSupportURL=https://github.com/LostwaveItalia/WerZatSonGUI/issues
AppUpdatesURL=https://github.com/LostwaveItalia/WerZatSonGUI/releases
VersionInfoVersion=2.1.3.0
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

// ============================================================
//  Uninstaller: closes WerZatSonGUI (and its child tree) first
// ============================================================

// Reads {app}\config.json (which WerZatSonGUI itself wrote, and which still
// exists at this point: [UninstallDelete] only runs after this function
// returns True) and returns a short language code.
//
// Compared against the ASCII prefix of each language name rather than the
// full "Português"/"Français" literals, because those names contain
// non-ASCII characters and the config.json file on disk is UTF-8 without a
// BOM (Python's json.dump with encoding="utf-8"), which LoadStringFromFile
// may or may not decode correctly depending on the host's active code page.
// The ASCII prefixes ("Italiano", "Portugu", "Fran") are unique across the
// four languages the GUI supports, so they are enough to disambiguate and
// are immune to code-page issues.
function GetConfiguredLanguage(): string;
var
  ConfigPath: string;
  Content: AnsiString;
begin
  Result := 'en'; // default to English if anything goes wrong

  ConfigPath := ExpandConstant('{app}\config.json');
  if not FileExists(ConfigPath) then
    Exit;
  if not LoadStringFromFile(ConfigPath, Content) then
    Exit;

  if Pos('"language": "Italiano"', Content) > 0 then
    Result := 'it'
  else if Pos('"language": "Portugu', Content) > 0 then
    Result := 'pt'
  else if Pos('"language": "Fran', Content) > 0 then
    Result := 'fr';
end;

function GetUninstallPrompt(Count: Integer): string;
var
  Lang: string;
  NL: String;
begin
  Lang := GetConfiguredLanguage();
  NL := Chr(13) + Chr(10);   // CRLF

  if Lang = 'it' then
    Result := Format(
      'WerZatSonGUI è ancora in esecuzione (%d processi correlati rilevati, ' +
      'inclusi eventuali processi figli Node/FFmpeg di una scansione in corso).' +
      NL + NL +
      'Chiuderli e continuare la disinstallazione?' + NL +
      'Eventuali scansioni in corso verranno interrotte.', [Count])

  else if Lang = 'pt' then
    Result := Format(
      'WerZatSonGUI ainda está em execução (%d processo(s) relacionado(s) ' +
      'encontrado(s), incluindo quaisquer processos filhos Node/FFmpeg de ' +
      'uma verificação em andamento).' + NL + NL +
      'Fechá-los e continuar a desinstalação?' + NL +
      'Qualquer verificação em andamento será abortada.', [Count])

  else if Lang = 'fr' then
    Result := Format(
      'WerZatSonGUI est toujours en cours d''exécution (%d processus associé(s) ' +
      'détecté(s), y compris les processus enfants Node/FFmpeg d''une analyse ' +
      'en cours).' + NL + NL +
      'Les fermer et poursuivre la désinstallation ?' + NL +
      'Toute analyse en cours sera interrompue.', [Count])

  else
    Result := Format(
      'WerZatSonGUI is still running (%d related process(es) found, including ' +
      'any in-progress scan''s Node/FFmpeg children).' + NL + NL +
      'Close them and continue uninstalling?' + NL +
      'Any pending scan in progress will be aborted.', [Count]);
end;

function GetWerZatSonRootPIDs(): TArrayOfString;
var
  ResultCode: Integer;
  TmpFile: string;
  Lines: TArrayOfString;
  I: Integer;
  PIDs: TArrayOfString;
begin
  SetArrayLength(PIDs, 0);
  TmpFile := ExpandConstant('{tmp}\wzs_pids.txt');
  DeleteFile(TmpFile);

  Exec('powershell.exe',
    '-NoProfile -ExecutionPolicy Bypass -Command ' +
    '"Get-CimInstance Win32_Process | ' +
    ' Where-Object { $_.CommandLine -and (' +
    '   $_.CommandLine -like ''*WerZatSonGUI*'' -or ' +
    '   $_.CommandLine -like ''*werzatsong.js*'' ' +
    ' ) } | ' +
    ' Where-Object { $_.Name -in @(''pythonw.exe'',''python.exe'',''python3.exe'',''py.exe'',''cmd.exe'',''node.exe'',''ffmpeg.exe'',''ffprobe.exe'') } | ' +
    ' ForEach-Object { $_.ProcessId } | ' +
    ' Out-File -Encoding ASCII ''' + TmpFile + '''"',
    '', SW_HIDE, ewWaitUntilTerminated, ResultCode);

  if LoadStringsFromFile(TmpFile, Lines) then
  begin
    for I := 0 to GetArrayLength(Lines) - 1 do
    begin
      if Trim(Lines[I]) <> '' then
      begin
        SetArrayLength(PIDs, GetArrayLength(PIDs) + 1);
        PIDs[GetArrayLength(PIDs) - 1] := Trim(Lines[I]);
      end;
    end;
  end;
  DeleteFile(TmpFile);
  Result := PIDs;
end;

// Called automatically by Inno Setup before the uninstall process starts.
// Returning False aborts the uninstall.
function InitializeUninstall(): Boolean;
var
  PIDs: TArrayOfString;
  I: Integer;
  ResultCode: Integer;
  Params: string;
begin
  Result := True;
  PIDs := GetWerZatSonRootPIDs();
  if GetArrayLength(PIDs) = 0 then
    Exit;

  if MsgBox(GetUninstallPrompt(GetArrayLength(PIDs)),
            mbConfirmation, MB_YESNO) <> IDYES then
  begin
    Result := False;
    Exit;
  end;

  // /T on each PID kills the whole tree (cmd.exe -> node -> ffmpeg grandchildren),
  // matching exactly what WerZatSonGUI itself does in _kill_pid_tree().
  for I := 0 to GetArrayLength(PIDs) - 1 do
  begin
    Params := '/c taskkill /F /T /PID ' + PIDs[I];
    Exec('cmd.exe', Params, '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  end;

  // Give Windows a moment to release handles on assets\, console_logs\, etc.
  Sleep(2000);
end;