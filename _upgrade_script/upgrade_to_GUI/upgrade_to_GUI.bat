@echo off
setlocal EnableDelayedExpansion
set "SCRIPT_DIR=%~dp0"

:: NOTE: deliberately no "chcp" call here. This file is saved using the
:: Windows 850 codepage (the standard Western-European OEM codepage, which
:: also correctly renders plain ASCII English) so eventual accented Italian text
:: SHOULD display correctly on the vast majority of real systems without any
:: runtime codepage switch (I still didn't want to risk it though lol).
:: Do NOT add "chcp 65001" (breaks "set /p" when stdin is redirected/piped)
:: and do NOT add "chcp 850" (corrupts cmd's parsing of the rest
:: of this same script. cmd appears to partially cache/tokenize ahead
:: using the codepage active when it started reading the file). both were
:: tried and both broke the script. If you need to edit this file's Italian
:: strings, save it back with the 850 codepage (not UTF-8/ANSI) to keep them
:: intact.

:: =======================
:: 0. Language selection
:: =======================
echo.
echo Select your language:
echo   [1] English
echo   [2] Italian
echo   [3] French
echo   [4] Portuguese
:: /c specifies the allowed keys (1, 2, 3, 4)
:: /m specifies the prompt message
choice /c 1234 /m "Choice: "

:: The choice command sets an "errorlevel" based on the order of the keys.
:: IMPORTANT: You must always check errorlevels in descending order (highest to lowest)!
if errorlevel 4 goto set_strings_portuguese
if errorlevel 3 goto set_strings_french
if errorlevel 2 goto set_strings_italian
if errorlevel 1 goto set_strings_english

:set_strings_english
set "LANG=english"
set "YES_KEY=Y"
set "MSG_TITLE_BANNER=WerZatSonGUI Migration / Update Tool"
set "MSG_FOLDER_PROMPT=Enter the full path to your WerZatSong or WerZatSonGUI folder"
set "MSG_FOLDER_NOT_FOUND=That folder doesn't exist. Please try again."
set "MSG_NEITHER_DETECTED=This doesn't look like a WerZatSong or WerZatSonGUI folder (no WerZatSonGUI.pyw or werzatsong.js found directly inside it). Please try again."
set "MSG_DETECTED_UPDATE=Detected an existing WerZatSonGUI installation. This will refresh it in place:"
set "MSG_DETECTED_MIGRATE=Detected a legacy (non-GUI) WerZatSong installation. This will migrate it to WerZatSonGUI:"
set "MSG_ASSETS_ALREADY_EXISTS=Warning: an assets folder already exists here. It will be merged into, which may not be a clean migration if this is left over from a previous attempt."
set "MSG_UPDATE_SUMMARY_LINE1= - Replace assets contents (werzatsong.js, utils, scripts, libs, resources, images, localizations, etc.)"
set "MSG_UPDATE_SUMMARY_LINE2= - Replace WerZatSonGUI.pyw, requirements.txt, package.json"
set "MSG_UPDATE_SUMMARY_LINE3= - config.json is NOT touched (your existing settings are kept)"
set "MSG_UPDATE_SUMMARY_LINE4= - assets\database and assets\.env are NOT touched"
set "MSG_MIGRATE_SUMMARY_LINE1= - Move everything currently in the folder into a new assets subfolder"
set "MSG_MIGRATE_SUMMARY_LINE2= - Move assets\logs back out to logs (if present)"
set "MSG_MIGRATE_SUMMARY_LINE3= - Move the contents of assets\input to db_inputs\legacy_werzatsong_input (if present)"
set "MSG_MIGRATE_SUMMARY_LINE4= - Replace assets contents, then copy in WerZatSonGUI.pyw, config.json, requirements.txt, package.json"
set "MSG_CONFIRM_PROMPT=Continue? (Y/N): "
set "MSG_ABORTED=Aborted. Nothing was changed."
set "MSG_STEP_RESTRUCTURE=Restructuring folder into assets..."
set "MSG_STEP_LOGS_BACK=Moving logs back out of assets..."
set "MSG_STEP_INPUT_MOVE=Moving legacy input files to db_inputs\legacy_werzatsong_input..."
set "MSG_STEP_STALE_CLEANUP=Removing outdated advanced-setting-explanations file(s)..."
set "MSG_STEP_ASSETS_COPY=Updating assets contents..."
set "MSG_STEP_CORE_FILES_COPY=Copying WerZatSonGUI.pyw, requirements.txt, package.json..."
set "MSG_STEP_CONFIG_COPY=Copying default config.json..."
set "MSG_STEP_PIP_INSTALL=Installing Python dependencies (pip install -r requirements.txt)..."
set "MSG_STEP_SHORTCUT=Creating desktop shortcut..."
set "MSG_DONE_UPDATE=Update complete^!"
set "MSG_DONE_MIGRATE=Migration complete^!"
set "MSG_LAUNCH_NOTE=Double-click the WerZatSonGUI desktop shortcut (or WerZatSonGUI.pyw directly inside the folder) to launch it."
set "MSG_NPM_FALLBACK_NOTE=Note: if you see a missing Node module error the first time you run a scan, open a terminal in that folder and run npm install once."
set "MSG_PRESS_KEY_EXIT=Press any key to exit..."
goto strings_done

:set_strings_italian
set "LANG=italian"
set "YES_KEY=S"
set "MSG_TITLE_BANNER=Strumento di Migrazione/Aggiornamento di WerZatSonGUI"
set "MSG_FOLDER_PROMPT=Inserisci il percorso completo della tua cartella con WerZatSong o WerZatSonGUI"
set "MSG_FOLDER_NOT_FOUND=Quella cartella non esiste. Riprova."
set "MSG_NEITHER_DETECTED=Questa non sembra una cartella con WerZatSong o WerZatSonGUI (non e' stato trovato ne' WerZatSonGUI.pyw ne' werzatsong.js direttamente al suo interno). Riprova."
set "MSG_DETECTED_UPDATE=Rilevata un'installazione esistente di WerZatSonGUI. Verra' aggiornata sul posto:"
set "MSG_DETECTED_MIGRATE=Rilevata un'installazione legacy (senza GUI) di WerZatSong. Verra' migrata a WerZatSonGUI:"
set "MSG_ASSETS_ALREADY_EXISTS=Attenzione: una cartella assets si trova gia' qui. Si mettera' insieme a quella nuova, il che potrebbe non risultare in una migrazione pulita se e' rimasta da un tentativo precedente."
set "MSG_UPDATE_SUMMARY_LINE1= - Sostituzione del contenuto di assets (werzatsong.js, utils, scripts, libs, resources, images, localizations, ecc.)"
set "MSG_UPDATE_SUMMARY_LINE2= - Sostituzione di WerZatSonGUI.pyw, requirements.txt, package.json"
set "MSG_UPDATE_SUMMARY_LINE3= - config.json NON viene toccato (le tue impostazioni attuali vengono mantenute)"
set "MSG_UPDATE_SUMMARY_LINE4= - assets\database e assets\.env NON vengono toccati"
set "MSG_MIGRATE_SUMMARY_LINE1= - Spostamento di tutto il contenuto attuale della cartella in una nuova sottocartella assets"
set "MSG_MIGRATE_SUMMARY_LINE2= - Spostamento di assets\logs di nuovo in logs (se presente)"
set "MSG_MIGRATE_SUMMARY_LINE3= - Spostamento del contenuto di assets\input in db_inputs\legacy_werzatsong_input (se presente)"
set "MSG_MIGRATE_SUMMARY_LINE4= - Sostituzione del contenuto di assets, poi copia di WerZatSonGUI.pyw, config.json, requirements.txt, package.json"
set "MSG_CONFIRM_PROMPT=Continuare? (S/N): "
set "MSG_ABORTED=Operazione annullata. Nessuna modifica effettuata."
set "MSG_STEP_RESTRUCTURE=Ristrutturazione della cartella in assets in corso..."
set "MSG_STEP_LOGS_BACK=Spostamento dei log fuori da assets in corso..."
set "MSG_STEP_INPUT_MOVE=Spostamento dei vecchi file di input in db_inputs\legacy_werzatsong_input in corso..."
set "MSG_STEP_STALE_CLEANUP=Rimozione dei file obsoleti delle spiegazioni delle impostazioni avanzate in corso..."
set "MSG_STEP_ASSETS_COPY=Aggiornamento del contenuto di assets in corso..."
set "MSG_STEP_CORE_FILES_COPY=Copia di WerZatSonGUI.pyw, requirements.txt, package.json in corso..."
set "MSG_STEP_CONFIG_COPY=Copia del config.json predefinito in corso..."
set "MSG_STEP_PIP_INSTALL=Installazione delle dipendenze Python (pip install -r requirements.txt) in corso..."
set "MSG_STEP_SHORTCUT=Creazione del collegamento sul desktop in corso..."
set "MSG_DONE_UPDATE=Aggiornamento completato^!"
set "MSG_DONE_MIGRATE=Migrazione completata^!"
set "MSG_LAUNCH_NOTE=Fai doppio clic sul collegamento WerZatSonGUI sul desktop (o su WerZatSonGUI.pyw direttamente nella cartella) per avviarlo."
set "MSG_NPM_FALLBACK_NOTE=Nota: se al primo avvio di una scansione vedi un errore relativo a un modulo Node mancante, apri un terminale in quella cartella ed esegui una volta npm install."
set "MSG_PRESS_KEY_EXIT=Premi un tasto qualsiasi per uscire..."
goto strings_done

:set_strings_french
set "LANG=french"
set "YES_KEY=O"
set "MSG_TITLE_BANNER=Outil de Migration / Mise a jour de WerZatSonGUI"
set "MSG_FOLDER_PROMPT=Entrez le chemin complet vers votre dossier WerZatSong ou WerZatSonGUI"
set "MSG_FOLDER_NOT_FOUND=Ce dossier n'existe pas. Veuillez reessayer."
set "MSG_NEITHER_DETECTED=Cela ne ressemble pas a un dossier WerZatSong ou WerZatSonGUI (aucun WerZatSonGUI.pyw ou werzatsong.js trouve directement a l'interieur). Veuillez reessayer."
set "MSG_DETECTED_UPDATE=Installation existante de WerZatSonGUI detectee. Cela va la rafraichir sur place:"
set "MSG_DETECTED_MIGRATE=Installation classique (sans GUI) de WerZatSong detectee. Cela va la migrer vers WerZatSonGUI:"
set "MSG_ASSETS_ALREADY_EXISTS=Attention: un dossier assets existe deja ici. Il sera fusionne avec le nouveau, ce qui pourrait ne pas donner une migration propre s'il s'agit d'un reste d'une tentative precedente."
set "MSG_UPDATE_SUMMARY_LINE1= - Remplacer le contenu de assets (werzatsong.js, utils, scripts, libs, resources, images, localizations, etc.)"
set "MSG_UPDATE_SUMMARY_LINE2= - Remplacer WerZatSonGUI.pyw, requirements.txt, package.json"
set "MSG_UPDATE_SUMMARY_LINE3= - config.json n'est PAS modifie (vos parametres actuels sont conserves)"
set "MSG_UPDATE_SUMMARY_LINE4= - assets\database et assets\.env ne sont PAS modifies"
set "MSG_MIGRATE_SUMMARY_LINE1= - Deplacer tout ce qui se trouve actuellement dans le dossier vers un nouveau sous-dossier assets"
set "MSG_MIGRATE_SUMMARY_LINE2= - Ramener assets\logs vers logs (si present)"
set "MSG_MIGRATE_SUMMARY_LINE3= - Deplacer le contenu de assets\input vers db_inputs\legacy_werzatsong_input (si present)"
set "MSG_MIGRATE_SUMMARY_LINE4= - Remplacer le contenu de assets, puis copier WerZatSonGUI.pyw, config.json, requirements.txt, package.json"
set "MSG_CONFIRM_PROMPT=Continuer ? (O/N): "
set "MSG_ABORTED=Annule. Aucune modification n'a ete apportee."
set "MSG_STEP_RESTRUCTURE=Restructuration du dossier vers assets en cours..."
set "MSG_STEP_LOGS_BACK=Deplacement des logs hors de assets en cours..."
set "MSG_STEP_INPUT_MOVE=Deplacement des anciens fichiers d'entree vers db_inputs\legacy_werzatsong_input en cours..."
set "MSG_STEP_STALE_CLEANUP=Suppression du ou des fichiers obsoletes d'explications des parametres avances..."
set "MSG_STEP_ASSETS_COPY=Mise a jour du contenu de assets en cours..."
set "MSG_STEP_CORE_FILES_COPY=Copie de WerZatSonGUI.pyw, requirements.txt, package.json en cours..."
set "MSG_STEP_CONFIG_COPY=Copie du config.json par defaut en cours..."
set "MSG_STEP_PIP_INSTALL=Installation des dependances Python (pip install -r requirements.txt) en cours..."
set "MSG_STEP_SHORTCUT=Creation du raccourci sur le bureau en cours..."
set "MSG_DONE_UPDATE=Mise a jour terminee^!"
set "MSG_DONE_MIGRATE=Migration terminee^!"
set "MSG_LAUNCH_NOTE=Double-cliquez sur le raccourci bureau WerZatSonGUI (ou WerZatSonGUI.pyw directement dans le dossier) pour le lancer."
set "MSG_NPM_FALLBACK_NOTE=Note: si vous voyez une erreur de module Node manquant lors du premier scan, ouvrez un terminal dans ce dossier et lancez npm install une fois."
set "MSG_PRESS_KEY_EXIT=Appuyez sur une touche pour quitter..."
goto strings_done

:set_strings_portuguese
set "LANG=portuguese"
set "YES_KEY=S"
set "MSG_TITLE_BANNER=Ferramenta de Migracao / Atualizacao do WerZatSonGUI"
set "MSG_FOLDER_PROMPT=Insira o caminho completo da sua pasta do WerZatSong ou WerZatSonGUI"
set "MSG_FOLDER_NOT_FOUND=Essa pasta nao existe. Por favor, tente novamente."
set "MSG_NEITHER_DETECTED=Esta nao parece ser uma pasta do WerZatSong ou WerZatSonGUI (nenhum WerZatSonGUI.pyw ou werzatsong.js foi encontrado diretamente dentro dela). Por favor, tente novamente."
set "MSG_DETECTED_UPDATE=Instalacao existente do WerZatSonGUI detectada. Isso ira atualiza-la no local:"
set "MSG_DETECTED_MIGRATE=Instalacao legada (sem GUI) do WerZatSong detectada. Isso ira migra-la para o WerZatSonGUI:"
set "MSG_ASSETS_ALREADY_EXISTS=Aviso: uma pasta assets ja existe aqui. Ela sera mesclada, o que pode nao resultar em uma migracao limpa se for o resto de uma tentativa anterior."
set "MSG_UPDATE_SUMMARY_LINE1= - Substituir o conteudo de assets (werzatsong.js, utils, scripts, libs, resources, images, localizations, etc.)"
set "MSG_UPDATE_SUMMARY_LINE2= - Substituir WerZatSonGUI.pyw, requirements.txt, package.json"
set "MSG_UPDATE_SUMMARY_LINE3= - config.json NAO sera modificado (suas configuracoes atuais serao mantidas)"
set "MSG_UPDATE_SUMMARY_LINE4= - assets\database e assets\.env NAO serao modificados"
set "MSG_MIGRATE_SUMMARY_LINE1= - Mover tudo que esta atualmente na pasta para uma nova subpasta assets"
set "MSG_MIGRATE_SUMMARY_LINE2= - Mover assets\logs de volta para logs (se presente)"
set "MSG_MIGRATE_SUMMARY_LINE3= - Mover o conteudo de assets\input para db_inputs\legacy_werzatsong_input (se presente)"
set "MSG_MIGRATE_SUMMARY_LINE4= - Substituir o conteudo de assets, depois copiar WerZatSonGUI.pyw, config.json, requirements.txt, package.json"
set "MSG_CONFIRM_PROMPT=Continuar? (S/N): "
set "MSG_ABORTED=Cancelado. Nenhuma alteracao foi feita."
set "MSG_STEP_RESTRUCTURE=Reestruturando a pasta para assets..."
set "MSG_STEP_LOGS_BACK=Movendo os logs para fora de assets..."
set "MSG_STEP_INPUT_MOVE=Movendo arquivos de entrada legados para db_inputs\legacy_werzatsong_input..."
set "MSG_STEP_STALE_CLEANUP=Removendo arquivo(s) desatualizado(s) de explicacoes de configuracoes avancadas..."
set "MSG_STEP_ASSETS_COPY=Atualizando o conteudo de assets..."
set "MSG_STEP_CORE_FILES_COPY=Copiando WerZatSonGUI.pyw, requirements.txt, package.json..."
set "MSG_STEP_CONFIG_COPY=Copiando config.json padrao..."
set "MSG_STEP_PIP_INSTALL=Instalando dependencias do Python (pip install -r requirements.txt)..."
set "MSG_STEP_SHORTCUT=Criando atalho na area de trabalho..."
set "MSG_DONE_UPDATE=Atualizacao concluida^!"
set "MSG_DONE_MIGRATE=Migracao concluida^!"
set "MSG_LAUNCH_NOTE=Clique duas vezes no atalho da area de trabalho do WerZatSonGUI (ou no WerZatSonGUI.pyw diretamente dentro da pasta) para inicia-lo."
set "MSG_NPM_FALLBACK_NOTE=Nota: se voce ver um erro de modulo Node ausente na primeira vez que executar um scan, abra um terminal nessa pasta e execute npm install uma vez."
set "MSG_PRESS_KEY_EXIT=Pressione qualquer tecla para sair..."
goto strings_done

:strings_done
echo.
echo ===============================================================
echo  !MSG_TITLE_BANNER!
echo ===============================================================

:: ================================================================
:: 1. Ask for the target folder (strip quotes/trailing backslash so
:: Explorer's "Copy as path" pastes in cleanly)
:: ================================================================
:ask_folder
echo.
set /p "FOLDER_I=!MSG_FOLDER_PROMPT!: "
set FOLDER_I=%FOLDER_I:"=%
rem The "X" sentinel avoids a classic batch parsing gotcha: a literal backslash
rem immediately followed by a closing quote (as in a bare "\") can confuse cmd's
rem parser, so both sides get a harmless trailing character before comparing.
if "%FOLDER_I:~-1%X"=="\X" set "FOLDER_I=%FOLDER_I:~0,-1%"

if not exist "%FOLDER_I%\" (
    echo !MSG_FOLDER_NOT_FOUND!
    goto ask_folder
)

:: ======================================================================
:: 2. Detect mode: update (existing GUI install) vs migrate (legacy,
:: non-GUI install) vs neither (re-prompt)
::
:: Note: every echo of a MSG_* variable below uses delayed expansion
:: (!VAR! instead of %VAR%) rather than as a style choice: several of
:: these messages contain literal parentheses (e.g. "(if present)"), and
:: a folder path passed in by the user could too (e.g. "Program Files
:: (x86)"), which breaks cmd's block parsing if expanded with %VAR% from
:: inside an if/for (...) block. See the docs for more on this batch
:: quirk. !VAR! sidesteps it since it expands after the block is parsed.
:: ======================================================================
set "MODE="
if exist "%FOLDER_I%\WerZatSonGUI.pyw" set "MODE=update"
if not defined MODE if exist "%FOLDER_I%\werzatsong.js" set "MODE=migrate"
if not defined MODE (
    echo !MSG_NEITHER_DETECTED!
    goto ask_folder
)

set "ASSETS_EXISTS_WARNING="
if "%MODE%"=="migrate" if exist "%FOLDER_I%\assets\" set "ASSETS_EXISTS_WARNING=1"

:: ======================================
:: 3. Mode-specific confirmation summary
:: ======================================
echo.
if "%MODE%"=="update" (
    echo !MSG_DETECTED_UPDATE!
    echo !MSG_UPDATE_SUMMARY_LINE1!
    echo !MSG_UPDATE_SUMMARY_LINE2!
    echo !MSG_UPDATE_SUMMARY_LINE3!
    echo !MSG_UPDATE_SUMMARY_LINE4!
) else (
    echo !MSG_DETECTED_MIGRATE!
    echo !MSG_MIGRATE_SUMMARY_LINE1!
    echo !MSG_MIGRATE_SUMMARY_LINE2!
    echo !MSG_MIGRATE_SUMMARY_LINE3!
    echo !MSG_MIGRATE_SUMMARY_LINE4!
    if defined ASSETS_EXISTS_WARNING (
        echo.
        echo !MSG_ASSETS_ALREADY_EXISTS!
    )
)
echo.

:: Clears the variable first, just in case
set "CONFIRM="
set /p "CONFIRM=!MSG_CONFIRM_PROMPT!"

:: Compares the input against the YES_KEY for the selected language
if /i not "!CONFIRM!"=="!YES_KEY!" (
    echo !MSG_ABORTED!
    goto end
)

:: ================================================================
:: 4. Migrate-mode-only: restructure the legacy folder into assets\
:: ================================================================
if "%MODE%"=="migrate" (
    echo.
    echo !MSG_STEP_RESTRUCTURE!
    if not exist "%FOLDER_I%\assets\" mkdir "%FOLDER_I%\assets"

    for %%F in ("%FOLDER_I%\*") do (
        if /i not "%%~nxF"=="assets" move "%%F" "%FOLDER_I%\assets\" >nul
    )
    for /d %%F in ("%FOLDER_I%\*") do (
        if /i not "%%~nxF"=="assets" move "%%F" "%FOLDER_I%\assets\" >nul
    )

    if exist "%FOLDER_I%\assets\logs\" (
        echo !MSG_STEP_LOGS_BACK!
        move "%FOLDER_I%\assets\logs" "%FOLDER_I%\logs" >nul
    )

    if exist "%FOLDER_I%\assets\input\" (
        echo !MSG_STEP_INPUT_MOVE!
        if not exist "%FOLDER_I%\db_inputs\legacy_werzatsong_input\" mkdir "%FOLDER_I%\db_inputs\legacy_werzatsong_input"
        for %%F in ("%FOLDER_I%\assets\input\*") do move "%%F" "%FOLDER_I%\db_inputs\legacy_werzatsong_input\" >nul 2>nul
        for /d %%F in ("%FOLDER_I%\assets\input\*") do move "%%F" "%FOLDER_I%\db_inputs\legacy_werzatsong_input\" >nul 2>nul
    )
)

:: ==================================================================
:: 5. Update-mode-only: clear out any pre-localization leftover from
:: older WerZatSonGUI versions (superseded by assets\localizations\)
:: ==================================================================
if "%MODE%"=="update" (
    echo.
    echo !MSG_STEP_STALE_CLEANUP!
    if exist "%FOLDER_I%\assets\advanced_setting*explain*.json" (
        for %%F in ("%FOLDER_I%\assets\advanced_setting*explain*.json") do (
            if /i not "%%~nxF"=="advanced_setting_explanations_English.json" ^
            if /i not "%%~nxF"=="advanced_setting_explanations_Italiano.json" ^
            if /i not "%%~nxF"=="advanced_setting_explanations_Français.json" ^
            if /i not "%%~nxF"=="advanced_setting_explanations_Português.json" ^
            del /f /q "%%F" >nul 2>nul
        )
    )
)

:: ==============================
:: 6. Shared install/update step
:: ==============================
echo.
echo !MSG_STEP_ASSETS_COPY!
rem Merge-copy only: never deletes anything at the destination that isn't part of the
rem bundled assets\ tree, so assets\database, assets\.env and assets\node_modules all
rem survive untouched (none of them exist in the source to overwrite them with).
xcopy "%SCRIPT_DIR%assets" "%FOLDER_I%\assets\" /e /i /y /q >nul

echo !MSG_STEP_CORE_FILES_COPY!
copy /y "%SCRIPT_DIR%WerZatSonGUI.pyw" "%FOLDER_I%\WerZatSonGUI.pyw" >nul
copy /y "%SCRIPT_DIR%requirements.txt" "%FOLDER_I%\requirements.txt" >nul
copy /y "%SCRIPT_DIR%package.json" "%FOLDER_I%\package.json" >nul

if "%MODE%"=="migrate" (
    echo !MSG_STEP_CONFIG_COPY!
    copy /y "%SCRIPT_DIR%config.json" "%FOLDER_I%\config.json" >nul
)

echo !MSG_STEP_PIP_INSTALL!
pushd "%FOLDER_I%"
python -m pip install -r requirements.txt
popd

echo !MSG_STEP_SHORTCUT!
set "WZSGUI_TARGET_DIR=%FOLDER_I%"
powershell -NoProfile -Command "$desktop = [Environment]::GetFolderPath('Desktop'); $s = (New-Object -ComObject WScript.Shell).CreateShortcut((Join-Path $desktop 'WerZatSonGUI.lnk')); $s.TargetPath = Join-Path $env:WZSGUI_TARGET_DIR 'WerZatSonGUI.pyw'; $s.WorkingDirectory = $env:WZSGUI_TARGET_DIR; $s.IconLocation = (Join-Path $env:WZSGUI_TARGET_DIR 'assets\logo.ico') + ',0'; $s.Save()" 2>nul

:: ========
:: 7. Done
:: ========
echo.
if "%MODE%"=="update" (echo !MSG_DONE_UPDATE!) else (echo !MSG_DONE_MIGRATE!)
echo !MSG_LAUNCH_NOTE!
echo !MSG_NPM_FALLBACK_NOTE!

:end
echo.
echo !MSG_PRESS_KEY_EXIT!
pause >nul
endlocal
