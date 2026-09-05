
# WerZatSonGUI
![Platform: Windows x64](https://img.shields.io/badge/Platform-Windows%20x64-blue)
![Version: 1.3.1](https://img.shields.io/badge/Version-1.3.1-orange)

**WerZatSonGUI** is a Windows x64 desktop app that puts a full graphical interface on top of [**WerZatSong**](https://github.com/Nel80s/WerZatSong), the original command line song finder tool. If you've used WerZatSong before, this app functions in essentially the same way, you just don't need to manually open a terminal and type commands to use it anymore. Check [*Features of the GUI*](#features-of-the-gui) for more info.

This document explains how to install WerZatSonGUI, set it up for the first time, and use every part of its interface.
> **Per chi parla italiano**: una traduzione completa di questo documento è disponibile in [**README_ITA.md**](README_ITA.md).

![WerZatSonGUI running a scan in dark mode](assets/images/gui_screenshot_1.png)
![WerZatSonGUI running a scan in light mode](assets/images/gui_screenshot_2.png)

## Table of Contents

- [Quick Start](#quick-start)
- [Features of the GUI](#features-of-the-gui)
- [Requirements](#requirements)
- [Installation](#installation)
- [First-Time Setup](#first-time-setup)
- [Using WerZatSonGUI](#using-werzatsongui)
- [Search Modes Explained](#search-modes-explained)
- [Running a Scan: Quick vs. Long Mode](#running-a-scan-quick-vs-long-mode)
- [Processed Files & PROCESSED.txt](#processed-files--processedtxt)
- [Where to Find Results](#where-to-find-results)
- [Log Format](#log-format)
- [Adding a Language / Translations](#adding-a-language--translations)
- [SmartScreen / Antivirus Warnings](#smartscreen--antivirus-warnings)
- [Credits](#credits)

## Quick Start Guide

### If you already have WerZatSong or an older WerZatSonGUI build:

1. **Download** and **extract in an empty folder** `upgrade_to_GUI.zip`.
2. **Run** `upgrade_to_GUI.bat` and follow the instructions.
3. **Launch** the app.
> If you cannot double click on it directly, open the `WerZatSonGUI.pyw` file with `Python`, `pythonw.exe` or `pyw.exe`-

4. **Add** your songs via the **Add Audio Files...** button.
5. **Add** your pklz files via the **Add PKLZ Files...** button.
6. **Select** your preferred search modes.
7. Click on **Start WerZatSong**.

### Otherwise, if you are a new user:
1. **Download** and run `WerZatSonGUI_Installer.exe`.

2. **Launch** the installer and follow the instructions; the wizard will make you install **Visual Studio Build Tools** and **Rust,** and take care of other dependencies automatically.
> Make sure to select the **"Desktop development with C++ workload** when installing the Visual Studio Build Tools. If you already have Visual Studio, **edit** your "Visual Studio Build Tools 2026" installation to add that option.


3. (If your PC restarts) **Re-launch** the installer to finish installing dependencies.

4. **Double click** the shortcut created on the desktop, or **run** `WerZatSonGUI.pyw` in the installation folder.

> If you cannot double click on it directly, open the `WerZatSonGUI.pyw` file with `Python`, `pythonw.exe` or `pyw.exe`-

> Read [*"Troubleshooting: How to Fix the "missing dependencies" / "Crash prevented!" Startup Error"*](#troubleshooting-how-to-fix-the-missing-dependencies--crash-prevented-startup-error) if you are having trouble starting the program.


5. **Enter** your Discord Webhook and API keys (AcoustID, AudioTag) when prompted.

> See [*"How to Get a Discord Webhook URL"*](#how-to-get-a-discord-webhook-url) below.

> See [*"How to Get an AudioTag API Key"*](#how-to-get-an-audiotag-api-key) below.

> See [*"How to Get an AcoustID (MusicBrainz) API Key"*](#how-to-get-an-acoustid-musicbrainz-api-key) below.


6. **Add** your songs via the **Add Audio Files...** button.
7. **Add** your pklz files via the **Add PKLZ Files...** button.
8. **Select** your preferred search modes.
9. Click on **Start WerZatSong**.

## Features of the GUI
- Every [**WerZatSong**](https://github.com/Nel80s/WerZatSong) command is supported: all 4 search modes (**MusicBrainz (AcoustID), AudioTag, Shazam** and **Audfprint**) are here, and any number of them can be combined in a single scan.
- Support for entire **Song Databases** thanks to a **batch-scanning engine,** which lets you add as many audio files as you want to the program: it will automatically scan at most 20-30 at a time, as efficiently as possible (see [*Running a Scan: Quick vs. Long Mode*](#running-a-scan-quick-vs-long-mode) below). Links to the community-ran [Lostwave Italia](https://drive.google.com/drive/folders/1S0Tj-PrdKzUc1jZ4c2feUGcyBABLdaEy) and [French Lostwaves](https://drive.google.com/drive/folders/1NLVjBYXNdWy_kxp21Npds6T3F6QpA520) Song Databases are included in the program under the **Add Audio Files...** section.
- A built-in script by **Mystic65**, which can automatically generate and search dozens of **tempo/pitch-shifted variations** of each file, to help catch songs that were sped up, slowed down, or pitched differently (see [*Running a Scan: Quick vs. Long Mode*](#running-a-scan-quick-vs-long-mode) below).
- A **base WerZatSong rework** and a **logs rework** (see [*Log Format*](#log-format) below) by **EierkuchenHD.**
- A new **Processed files...** section. If you have a significant amount of songs in your input folder, you can now easily decide which ones you want to run with WerZatSonGUI, **without** having to move anything out of that folder (see [*Processed Files & PROCESSED.txt*](#processed-files--processedtxt) below).
- Support for **multiple languages** and **translations.** Currently, the supported languages are English and Italian (see [*Adding a Language / Translations*](#adding-a-language--translations) below).
- Support for **light** and **dark** modes.

## Requirements

WerZatSonGUI is currently **only supported on Windows x64** (it relies on Windows-specific features such as opening folders in File Explorer and spawning native console windows).

> **Note:** You do **not** need to install any of these yourself! The installer described below takes care of Node.js, Python and FFmpeg fully automatically using **WinGet** (correctly checking both that they're installed *and* that they meet the minimum version above, upgrading them if an older copy is found), and walks you through installing Rust and the C++ Build Tools yourself (see below for why).
The requirements are only listed here so the user knows what's happening during installation, and in the exceptional case of installation failing for one of them (see *"If the Installer Doesn't Work"* below).

The requirements are the same ones the original WerZatSong needs to run:

- [**Node.js**](https://nodejs.org) (v20.0 or higher)
- [**Python**](https://www.python.org/downloads) (v3.13 or higher)
- [**FFmpeg**](https://www.gyan.dev/ffmpeg/builds)
- **Rust** and the **C++ Build Tools** (only needed to fix a few errors when compiling a couple of the Python dependencies). Any Visual Studio release from **2017 onwards** works, as long as its **"Desktop development with C++"** workload (the actual C++ Build Tools) is installed; a full Visual Studio *IDE* install isn't required at all, and isn't detected as a substitute if the C++ workload itself is missing

Before your first scan, you'll also want:

- A **Discord Webhook URL**, to receive match notifications (see *"How to Get a Discord Webhook URL"* below)
- An **AudioTag API key**, required for AudioTag search mode (see *"How to Get an AudioTag API Key"* below)
- An **AcoustID API key**, required for MusicBrainz search mode (see *"How to Get an AcoustID (MusicBrainz) API Key"* below)
- A **database of Audfprint fingerprints** (`.pklz` files), required for Audfprint search mode. You can download most of the community-made pklz database files from [**here.**](https://wzs.cosine.club)
  - **Note**: These databases can take up a lot of disk space (even hundreds of gigabytes); an SSD is recommended for good performance, if you are looking to download all the available database files. Thankfully, though, for some searches only using a handful of pklz files covering the correct sources (same genre, same years, etc.) can be just as effective, so it is recommended to look up the pklz filenames and figure out which ones can be useful for your searches.

## Installation

### Recommended (if you've never had WerZatSong before): Use the Installer

1. Download `WerZatSonGUI_Installer.exe` and run it
2. If your Windows install is set to a language other than English or one of the other supported languages, the installer will ask you to pick one of them for the wizard itself; the app's own interface language is then automatically set to match afterwards (you can always change it later in **Advanced Settings**, see [*General tab*](#general-tab) below)
3. On the next page, you can choose whether to create a **desktop shortcut** (checked by default) alongside the usual Start Menu entry
4. The installer will automatically:
   - Install Node.js, Python 3.13 and FFmpeg if they're not already on your system, or upgrade them if an existing copy is below the required minimum version (via WinGet)
   - Detect an existing Visual Studio C++ Build Tools install (2017 or newer) and Rust install, and skip them if already present
   - If either is missing, open the correct official download page for your version of Windows and pause, asking you to finish that install yourself before continuing (see *"Why some installs aren't fully automatic"* below) **Once either of the two installations has finished, you will have to go to the PowerShell screen opened for the installation and press ENTER manually to continue.**
   - Run `npm install`
   - Run `pip install -r requirements.txt`
   - Install pip and all the required Python packages
   - Launch WerZatSonGUI once everything is ready

Once installation finishes, WerZatSonGUI opens and walks you through [**First-Time Setup**](#first-time-setup) below.
You may be asked to restart your computer instead (this can happen after installing the C++ Build Tools or Rust): if that happens, it's completely safe to just run `WerZatSonGUI_Installer.exe` again once you're back: anything already installed will be detected and skipped automatically.
When your computer restarts and installation has finished, you can use the desktop/Start Menu shortcut created above, or go to the folder where you chose to install the program and double click the file `WerZatSonGUI.pyw`, to initiate the First-Time Setup directly. If you cannot double click on it directly, open the `WerZatSonGUI.pyw` file with `pythonw.exe` or `pyw.exe`.

#### Why some installs aren't fully automatic, but guided

Visual Studio Build Tools and Rust are both intentionally **not** installed silently in the background. Visual Studio Build Tools in particular is a large, slow install, and previous versions of this installer couldn't reliably detect an existing install, so it ended up reinstalling (and re-downloading hundreds of components) on every single run even when it was already present. Installing it (and Rust) now opens the correct official installer for your version of Windows in your browser and simply waits for you to confirm once you're done, which is slower to click through but far more predictable and far less likely to silently fail or balloon in size.

#### Troubleshooting: How to Fix the "missing dependencies" / "Crash prevented!" Startup Error

!["missing dependencies" / "Crash prevented!" Startup Error](assets/images/missing-dependencies-error.png)

If you used the WerZatSonGUI installer and are getting a crash error when trying to start the program (like the one shown above) it usually means the Visual Studio Build Tools weren't installed correctly.
This is a known issue and a very easy fix!

##### Step 1: Save Your Error Message

Keep the error window open, or open your `crash_logs.txt` file. Make sure you have everything the error window said written down somewhere. You will need to look at a specific command from this error message in *Step 5.*

##### Step 2: Install Visual Studio Build Tools

> **Important Note:** If your computer is set to a language other than English, the buttons and options in this installer will be in your local language! Just look for the options that *translate* to the English terms below.

1. Download the official installer here: [Visual Studio Build Tools](https://aka.ms/vs/stable/vs_BuildTools.exe)
2. Open the installer. If you see a list of different programs, scroll until you find **Visual Studio Build Tools 2026** (or whatever the latest version is).
3. Click the **Modify** (or **Edit**) button next to it.
4. A window with several options will pop up. Look in the top left corner and check the box that says **Desktop development with C++** or something like that. *(Note: You do not need to check any other options).*
5. Click **"Install"** in the bottom right corner and wait for it to finish.

##### Step 3: Restart Your Computer
Once the installation is completely finished, restart your PC to make sure the changes are applied.

##### Step 4: Open Command Prompt as Administrator
1. Click on your Windows search bar at the bottom of your screen and type `cmd`.
2. Right-click on **Command Prompt** and select **Run as administrator**.

##### Step 5: Run the Fix Command
Now, look back at the error message from Step 1. You will see a line of text that looks something like this: 
`"C:\Program Files\Python313\python.exe" -m pip install -r C:\WerZatSonGUI\requirements.txt`

Just copy and paste that line, `"C:\Program Files\Python313\python.exe" -m pip install -r C:\WerZatSonGUI\requirements.txt`, into your cmd window, then press **Enter**.

After this, let it load and finish doing its thing.
Once it's done, you can close the window, and run WerZatSonGUI: it will now work.

### Recommended (if you already have WerZatSong or an older WerZatSonGUI installed): upgrade_to_GUI.zip

If you'd rather not run the installer at all (for example, to avoid the SmartScreen warning described in [*SmartScreen / Antivirus Warnings*](#smartscreen--antivirus-warnings) below), and you already have either the original command-line **WerZatSong** or an older copy of **WerZatSonGUI** installed and working, you don't need to reinstall everything from scratch. In the releases, you will find `upgrade_to_GUI.zip`. Extract that archive in an empty folder and run `upgrade_to_GUI.bat`: it will handle both cases automatically since almost everything it needs (Node.js, Python, Rust, the C++ Build Tools, FFmpeg) is already on your system.

Double-click it and it will:

1. Ask you to choose English (or another supported language) for its own messages
2. Ask for the full path to your existing WerZatSong/WerZatSonGUI folder (Explorer's "Copy address as text" works fine here, quotes and a trailing backslash are handled automatically)
3. Detect which situation applies, show you exactly what it's about to do, and ask for confirmation before touching anything:
   - **A legacy, non-GUI WerZatSong install** (a `werzatsong.js` directly inside the folder, no `WerZatSonGUI.pyw`): it restructures the folder for you, moving everything that's currently there into a new `assets` subfolder, moving `assets\logs` back out to `logs`, and moving the contents of `assets\input` into `db_inputs\legacy_werzatsong_input` (so anything you'd previously queued up isn't lost, just relocated to where WerZatSonGUI expects manually-added input files to live)
   - **An existing WerZatSonGUI install** (a `WerZatSonGUI.pyw` already inside the folder): it refreshes it in place instead, without restructuring anything
4. Either way, it then replaces the entire `assets` folder's contents (`werzatsong.js` and everything under `utils`, `scripts`, `libs`, `resources`, `images`, `localizations`, etc.) with the current version's, and copies in the latest `WerZatSonGUI.pyw`, `requirements.txt` and `package.json`. **Your `assets\database` (pklz fingerprints) and `assets\.env` (API keys/webhook) are never touched or deleted**, since neither is part of the bundle being copied in
   - When migrating a legacy install, `config.json` is also copied in for the first time (there's no existing GUI configuration yet to preserve)
   - When updating an existing WerZatSonGUI install, **`config.json` is deliberately left alone**, so your directories, theme, and language stay exactly as you left them; the script also clears out any leftover `advanced_settings_explainations.json`-style file from `assets`, an older, pre-localization settings-explanation file that's fully superseded by the `assets\localizations` folder (see [*Adding a Language / Translations*](#adding-a-language--translations) below) and would otherwise linger around unused
5. Runs `pip install -r requirements.txt` for you
6. Creates (or refreshes) a **WerZatSonGUI** desktop shortcut pointing at the folder, exactly like the installer's own shortcut

Once it's done, use that shortcut (or double-click `WerZatSonGUI.pyw` directly inside the folder) to launch the app. If you cannot double click on the file or use the shortcut directly, open the `WerZatSonGUI.pyw` file with `pythonw.exe` or `pyw.exe`. If a scan ever complains about a missing Node module afterwards, open a terminal in that folder and run `npm install` once.

### If the Installer Doesn't Work

If a step of the automatic installer fails, you can install everything by hand instead:

1. **Install Node.js, Python and FFmpeg** manually from the links in [Requirements](#requirements), making sure each one is added to your system's `PATH`. Verify they installed correctly (and meet the minimum versions above) by opening a terminal in the WerZatSonGUI folder and running:

    ```bash
    node -v
    npm -v
    python --version
    pip --version
    ffmpeg -version
    ```

    You should see version numbers for each, similar to this:

    ![Programs](assets/images/programs.png)

2. **Install the Node.js dependencies**:

    ```bash
    npm install
    ```

3. **Install the Python dependencies**, one command at a time:

    ```bash
    pip install -r requirements.txt
    pip install audioop-lts
    pip install shazamio
    ```

    - **Note**: If you encounter an error during the installation of these dependencies, it may be due to missing dependencies. Here are two common issues and their solutions:
        - **Rust Error** (see screenshot below):
            - Install Rust from [the official website](https://www.rust-lang.org/tools/install) (or directly via the [rustup-init.exe download](https://static.rust-lang.org/rustup/dist/x86_64-pc-windows-msvc/rustup-init.exe))
            - After installation, verify it works by running `rustc --version` in your terminal
            - Once Rust is installed, retry the `pip install` commands above
            ![Rust Error](assets/images/rust-error.png)
        - **C++ Build Tools Error** (see screenshot below):
            - Install the Visual Studio C++ Build Tools: on **Windows 11**, use the [current release](https://aka.ms/vs/stable/vs_BuildTools.exe); on **Windows 10**, use [Visual Studio 2022 Build Tools](https://aka.ms/vs/17/release/vs_buildtools.exe) instead (the newest version still supported there). Any release from 2017 onwards works the same way, this is just the current download link
            - During installation, select the *"Desktop development with C++"* workload. The rest of Visual Studio itself isn't needed
            - After installation, restart your machine
            - Retry the `pip install` commands above
            ![Shazam Error](assets/images/shazam-error.png)

4. **Download the source code** by clicking on `<> Code` -> `Download ZIP`, then extracting the ZIP file with the source code wherever you prefer. The following files/folders can then be deleted, as they are only used by the installer:
	```
	get_pip.py
	setup.iss
	setup_deps.ps1
	Languages folder
	output folder
	```

5. **Launch WerZatSonGUI** by double-clicking `WerZatSonGUI.pyw` (or running `pythonw WerZatSonGUI.pyw` from a terminal in that folder)

## First-Time Setup

The very first time you launch WerZatSonGUI, it notices that no `.env` file exists yet in its `assets` folder and switches into a small setup window instead of showing the full interface:

1. It first checks that the `db_inputs` and `assets\input` folders are both empty. If either one already contains files, you'll get an error message asking you to clear them out and relaunch: this is a safety check to make sure nothing gets accidentally processed before setup finishes.
2. It runs `npm install` in its own terminal window, closing it automatically once that's done.
3. It runs `pip install -r requirements.txt` in its own terminal window, closing it automatically once that's done.
4. It then opens a second terminal window that asks you, one at a time, for your **Discord Webhook URL**, your **AudioTag API key** and your **AcoustID API key**:

    ![Setup](assets/images/setup.png)

    Paste each value when prompted and press Enter. If something you enter is rejected (an invalid key or webhook), WerZatSonGUI will reopen this terminal automatically so you can try again: you don't need to restart the whole app.
5. Once all three are accepted, they're saved to `assets\.env` and WerZatSonGUI relaunches itself automatically into the full interface.

### How to Get a Discord Webhook URL

Your Discord webhook is where WerZatSonGUI sends you a notification (with details, and for some search modes a results file) every time a scan turns up a likely match.

1. Open Discord and create your own server, if you don't already have one to use for this
2. In any text channel (e.g. **#general**), click the gear icon next to it to open **Edit Channel**
3. Go to **Integrations → Webhooks**
4. Click **Create Webhook**, then open it and select **Copy Webhook URL**
5. Paste this URL when WerZatSonGUI asks for it during setup (or afterwards, in the **API Keys & Webhook (.env)** section of the main interface)

You can optionally give this webhook a custom display name and avatar image directly from the **Discord tab** of WerZatSonGUI's **Advanced Settings** (see [*Using WerZatSonGUI*](#using-werzatsongui) below).

### How to Get an AudioTag API Key

This key is required if you want to use the **AudioTag** search mode.

1. Go to the [AudioTag](https://audiotag.info) website and create a new account (or log in, if you already have one)
2. Go to your [**User Section**](https://user.audiotag.info) and open the **API keys** tab
3. Click **Create new API key**, then copy it
4. Paste this key when WerZatSonGUI asks for it during setup (or afterwards, in the **API Keys & Webhook (.env)** section of the main interface)

### How to Get an AcoustID (MusicBrainz) API Key

This is the key that powers WerZatSonGUI's **MusicBrainz (AcoustID)** search mode: in the interface it's simply labeled **"AcoustID API Key"**.

1. Go to the [AcoustID](https://acoustid.org) website and create a new account (or log in, if you already have one)
2. Go to [**My Applications**](https://acoustid.org/my-applications) and click **Register a new application**
3. Fill in the fields with basic info (it can be random) and click **Register**
4. Copy the application's **API key** that appears
5. Paste this key when WerZatSonGUI asks for it during setup (or afterwards, in the **API Keys & Webhook (.env)** section of the main interface)

### Setting Up the Audfprint Database

If you plan to use the **Audfprint** search mode, you can download the community-made database folders (containing `.pklz` fingerprint files) from [**here**](https://wzs.cosine.club), then place them inside your **Audfprint Database Directory**: either drop them in via the **Open...** button next to it in the **Directories** section, or use the **Add PKLZ Files...** button at the bottom of the window (which also has a **Public PKLZ Database...** link that takes you straight to the same site). Each top-level folder acts as its own independent collection of fingerprints (for example, split by genre or source):

![Database](assets/images/database.png)

You can later restrict a scan to just one of these subfolders using **"Use only fingerprints from this subdirectory"** in **Advanced Settings**.

## Using WerZatSonGUI

Once setup is complete, WerZatSonGUI opens its full interface every time you launch it. In both windowed and maximized/fullscreen mode, the top action bar (**Add PKLZ Files...**, **Add Audio Files...**, **Processed Files...**, **Force Stop**, **Start WerZatSong**) always stays visible and reachable. If the rest of the interface doesn't fit in the available space (for example with both **API Keys & Webhook** and **Directories** expanded on a smaller screen), the section above the action bar scrolls instead of pushing it off-screen.

### Header

The logo and title in the top-left, and a **Credits** button that opens a small popup crediting everyone who worked on WerZatSonGUI, the batch scanning script, and the original WerZatSong project.

### Console

A live terminal view. Whenever WerZatSonGUI runs a command in the background (during setup, or while a scan is running) its output appears here in real time. You can zoom its text in and out at any time with **Ctrl + Scroll Wheel**, **Ctrl + Plus/Minus**, or reset it back to the default size with **Ctrl + 0**, handy for reading a small screen or a stream of dense log lines. This never interferes with the console's normal scrolling or any other keyboard shortcut.

### API Keys & Webhook (.env)

Shows your **AcoustID API Key**, **AudioTag API Key** and **Discord Webhook**, each hidden behind a **Show...** button so they aren't visible on screen by default. Click **Show...** to reveal and edit a value, or **Hide...** to conceal it again. Any change made here is saved to `assets\.env` immediately, unless a scan is currently running, in which case it's applied automatically the moment that scan finishes.

### Default Directories

- **Input Directory:** where you place all the audio files you want WerZatSonGUI to scan (defaults to a `db_inputs` folder next to the app). This is **separate** from WerZatSong's own internal `assets\input` folder, which WerZatSonGUI manages automatically behind the scenes during a scan.
- **Audfprint Database Directory:** where your `.pklz` fingerprint database folders live (see [*Setting Up the Audfprint Database*](#setting-up-the-audfprint-database)).
- **Log Directory:** where result logs are saved after each scan (see [*Where to Find Results*](#where-to-find-results) and [*Log Format*](#log-format) below).

Each row has an **Open...** button (opens that folder in File Explorer, creating it first if it doesn't exist) and a **Browse...** button (lets you pick a different folder to use instead). This whole section is greyed out while a scan is running.

### Search Modes

Four checkboxes to enable or disable **MusicBrainz (AcoustID)**, **AudioTag**, **Shazam** and **Audfprint** (see [*Search Modes Explained*](#search-modes-explained) below for what each one does). You can enable any combination; when more than one is checked, they always run in this fixed order:

1. **MusicBrainz** (AcoustID)
2. **AudioTag**
3. **Shazam**
4. **Audfprint**

### Advanced Settings

Split into five tabs so related settings are grouped together. Each individual setting has a small **[?]** button to its left with a short explanation, and this section also summarizes what each one does. This whole panel is greyed out while a scan is running.

#### General tab

- **Mark all audio files as processed in:** Useful if you have a lot of files in your input folder, and you want to run only a few specific ones. Marks all audio files in your input folder as **processed** in either **Quick** mode (no additional tempo generation), **Long** mode (original files and additional tempos) or **both** modes, so you can manually delete the lines of the songs you do not want to run by editing **PROCESSED.txt.** Pressing any of the 3 buttons **overwrites** your current PROCESSED.txt file (see [*Processed Files & PROCESSED.txt*](#processed-files--processedtxt) below).
- **Theme:** Changes the visual appearance of the application. Set to **Light,** **Dark,** or **System Default** to automatically match your OS settings.
- **Language:** Switches the interface between **English** and **Italiano**. Takes effect immediately, no restart required (see [*Adding a Language / Translations*](#adding-a-language--translations) below if you'd like to help add more).

#### Long Mode tab

- **Enable Long Mode (generate different speeds/tempos for each audio file):** switches scans between **Quick** and **Long** mode. See [*Running a Scan: Quick vs. Long Mode*](#running-a-scan-quick-vs-long-mode) below.
- **Negative tempo multipliers** / **Positive tempo multipliers:** the tempo ratios used to generate variations in Long mode (negative = slowed down/pitched down, below `1.0`; positive = sped up/pitched up, above `1.0`). Edit these as a comma-separated list in brackets, e.g. `[0.9, 0.95, 1.05, 1.1]`. Leaving **one** field empty (or `[]`) makes WerZatSonGUI generate variations from only the other array; leaving **both** empty restores the full default set of 40 variations (20 negative + 20 positive).

#### Audfprint tab

- **Use only fingerprints from this subdirectory:** restricts Audfprint mode to a single subfolder of your Audfprint Database Directory instead of searching all of them. Use **Browse...** to pick one, or type its name directly (it must already exist inside the Audfprint Database Directory).
- **Set the number of CPU threads to use:** sets how many CPU threads Audfprint mode uses. WerZatSong itself caps this at **16** regardless of what you enter, to help avoid running out of memory; leaving this unchecked lets it use all available threads on your machine automatically.
- **Set search depth to:** controls how aggressively Audfprint searches for a match, from `1` to `8`. Higher values perform a more thorough "deep search" for low-quality clips, but may significantly increase processing time. Defaults to `4`.

#### MusicBrainz tab

- **Set duration range (in seconds) to:** restricts MusicBrainz matches to songs whose duration falls between the two values you enter. Each value must be between `30` and `600`; anything outside that range is reset back to the defaults (`30`/`600`).
- **Set initial extension (in seconds) to:** helps MusicBrainz find a match when the beginning of your audio file is cut off or delayed, by extending the analyzed window by this many seconds. Must be between `1` and `25`; anything outside that range is reset back to the default (`25`).

#### Discord tab

- **Use a custom Webhook name:** overrides the display name your Discord webhook uses when posting, instead of the default "WerZatSong".
- **Use a custom Webhook image:** overrides the avatar image your Discord webhook uses when posting. The link must start with either `https://cdn.discordapp.com/icons/` or `https://cdn.discordapp.com/avatars/`, or Discord won't recognize it. You can get a correctly formatted link by setting the image as a Discord bot's profile picture and copying the link from there.

### Adding Files to Scan

Use **Add Audio Files...** at the bottom of the window to add the songs you want to search for, either by picking individual files or an entire folder. WerZatSonGUI accepts `.mp3`, `.wav`, `.flac` and `.m4a` files. Anything that isn't already an `.mp3` is **automatically converted** to the highest-quality VBR mp3 FFmpeg can produce the moment a scan starts.

> **WARNING: This conversion REPLACES the original file.** 
> Once a `.wav`/`.flac`/`.m4a` is converted, only the resulting `.mp3` remains in your input folder. Keep a copy elsewhere first if you want to hold on to the original losslessly-encoded (or differently-encoded) file. The conversion is crash-safe (an interrupted run never leaves you with a half-converted or missing file, it just retries cleanly next time), but it is one-way.

## Search Modes Explained

- **MusicBrainz (AcoustID):** computes an acoustic fingerprint of the file (via `fpcalc`) and looks it up against the [AcoustID](https://acoustid.org)/MusicBrainz database, keeping only results above a minimum confidence score. Needs an **AcoustID API key**.
- **AudioTag:** sends the file to the [AudioTag.info](https://audiotag.info) API and reports back whatever match it finds. Needs an **AudioTag API key**.
- **Shazam:** identifies the file the same way the Shazam app does, using the `shazamio` Python library. Needs no key, but is deliberately rate-limited (a short pause between files) to avoid tripping Shazam's own abuse detection.
- **Audfprint:** matches the file against your own local `.pklz` fingerprint database(s) instead of an online service (see [*Setting Up the Audfprint Database*](#setting-up-the-audfprint-database)). The only mode that works entirely offline once your databases are downloaded, and the main one that benefits from **Long Mode**'s tempo/pitch variations, since it's sensitive enough to those.

## Running a Scan: Quick vs. Long Mode

- **Quick Mode** (the default) searches every pending file exactly as-is, no variations generated.
- **Long Mode** additionally generates tempo/pitch-shifted variations of each file first (see the **Long Mode tab** above), then searches every variation too. Much more thorough, but much slower, since it's effectively scanning dozens of extra files per song.

Either way, WerZatSonGUI never hands the whole file list to the underlying engine at once: WerZatSong itself has a **hard limit of 30 files per search**, so everything is split into batches beforehand. Batches normally target **20 files** (or, in Long Mode, 20 variations) at a time, since that comfortably leaves room to grow if a batch needs to absorb a few extra files/variations without ever approaching the hard 30-file limit.

In Quick Mode this is straightforward: 45 pending files becomes a 20/20/5 split. In Long Mode it's a little smarter, because the *number of variations per file* isn't fixed and rarely divides evenly by 20: rather than dispatching a batch of 20 followed by a tiny batch of, say, 3 leftover variations, WerZatSonGUI keeps a running pool of not-yet-searched variations across files and only finalizes a batch's size once it knows how much is actually left to search. Concretely: if file A produces 23 variations, the first 20 are dispatched as soon as they're ready, and the remaining 3 are held and combined with the first 17 variations generated for file B into a second, full batch of 20. And so on for as many files as needed, rather than ever sending out a wasteful near-empty batch. The 30-file hard limit is still always respected; a batch only ever grows past 20 when doing so avoids a small trailing batch and still fits under 30.

## Processed Files & PROCESSED.txt

Every file WerZatSonGUI finishes searching (in Quick Mode, Long Mode, or both, depending on which mode(s) it ran under) is recorded as a line in `PROCESSED.txt`, at the root of the WerZatSonGUI folder, so re-running a scan later never searches the same file twice in the same mode. Each line is the file's relative path inside your Input Directory, optionally suffixed with `|quick` or `|long` if it's only been processed in one specific mode rather than both.

You can freely hand-edit this file: delete a line (or a whole file) to make WerZatSonGUI search it again next time, or use **Mark all audio files as processed in** (see the **General tab** above) to bulk-mark everything so you can then delete just the handful of lines for files you actually want to (re-)search. Much faster than deleting hundreds of individual lines the other way around.

## Where to Find Results

Whenever a scan finds a likely match, two things happen:

1. A notification (and, for most modes, a small results `.txt` file with the raw match data) is posted to your **Discord Webhook**.
2. At the end of processing each batch/file, WerZatSonGUI copies every results file generated during it into a new, timestamped subfolder of your **Log Directory** (see [*Default Directories*](#default-directories) above and [*Log Format*](#log-format) below), and prints exactly where in the console (`[SUCCESS]: Logs for '...' saved in '...'`) so you never have to go hunting for it manually.

If a batch/file produces no matches at all in any enabled mode, no log subfolder is created for it. Only genuine matches ever show up under your Log Directory.

## Log Format

The exact format depends on the search mode:

- **MusicBrainz, Audiotag and Shazam** logs are simple: one result per line (MusicBrainz), or the raw match data as-is (Audiotag/Shazam). Nothing fancier is needed since each of these modes returns at most a small number of already-scored candidates.
- **Audfprint** logs are richer, since a single search can return many candidates that need to be judged against each other. Each one starts with a short **LEGEND** block explaining the format, followed by every candidate match, listed from most to least likely, formatted as two lines each:
	```
    [LABEL] <aligned> aligned / <raw> raw (<cons>%) | x<hits> | #<rank> | <source pklz> | offset <t>s
    <matched file name> (<matched file path>)
    ```
    - **aligned:** the number of time-consistent matching hashes between your file and the candidate. This is the main piece of evidence you should take into account: Audfprint's own documentation notes that more than 5-6 aligned hashes usually means a genuine match.
    - **raw:** all hashes the two files have in common, before filtering for ones that line up in time.
    - **cons% (consistency):** `aligned / raw` as a percentage. Random, unrelated files stay under roughly 1%, so even a modest percentage here is meaningful.
    - **hits:** how many separate alignment hits were found for this candidate.
    - **rank:** the candidate's position in Audfprint's own internal pre-ranking (useful context, not a confidence measure by itself).
    - **offset:** where your file's audio lines up against the candidate, in seconds (negative means your file appears to start earlier).
    - **LABEL:** a plain-language summary of how confident the match is: **VERY STRONG**, **STRONG** and **PROBABLE** are strong enough that a Discord webhook message is also sent for them; **BORDERLINE** means it's below that bar but still worth a manual look; **NO MATCH** means it didn't clear any threshold.

The same legend and formatting is used both in the `.txt` log file and in the results file attached to the Discord webhook post, so they always match.

## Adding a Language / Translations

WerZatSonGUI currently ships with **English** and **Italian**, simply because those are the languages that can currently be written and double-checked properly, not a hard limit on what it'll ever support. If you'd like to translate it into another language, see [**TRANSLATION_GUIDE.md**](TRANSLATION_GUIDE.md) for a full walkthrough of every file involved, then get in touch so your translation can be added to the repo officially and everyone can use it.

## SmartScreen / Antivirus Warnings

Because `WerZatSonGUI_Installer.exe`, `setup_deps.ps1` and `WerZatSonGUI.pyw` aren't signed with a paid code-signing certificate (which would cost me an amount I'm not able to afford), Windows SmartScreen and some antivirus engines may flag them as coming from an "Unknown publisher" or even quarantine them outright. This is a trust/reputation heuristic based on how new and how widely-distributed a file is, **not** a sign that anything is actually malicious. It's a well-known side effect of independently-distributed Windows software in general, and code-signing certificates aren't something a free/open-source hobby project can typically obtain, so this warning is expected to keep appearing regardless of any change made to the scripts themselves.

If you see a **"Windows protected your PC"** dialog after downloading `WerZatSonGUI_Installer.exe`:

1. Click **More info**
2. Click the **Run anyway** button that appears

If your antivirus quarantines or deletes `setup.iss`, `setup_deps.ps1`, `upgrade_to_GUI.bat` or `WerZatSonGUI.pyw` instead of just warning about them, restore the file from quarantine (or re-download/re-extract it) and add an exclusion for the WerZatSonGUI folder if your antivirus lets you.

If you'd rather sidestep the flagged installer entirely, and you already have a working WerZatSong or WerZatSonGUI install, see [*Recommended (if you already have WerZatSong or an older WerZatSonGUI installed): upgrade_to_GUI.zip*](#recommended-(if-you-already-have-WerZatSong-or-an-older-WerZatSonGUI-installed):-upgrade_to_GUI.zip) above. `upgrade_to_GUI.bat` reuses your existing Node.js/Python/Rust/C++ Build Tools/FFmpeg install and never needs to touch WinGet or the guided Visual Studio/Rust installers at all.

## Credits

- **WerZatSonGUI v1.3.1** by some random account, with contributions from EierkuchenHD. Testers: EierkuchenHD, Shardanik, VoidGod.
- **WerZatSong batch script** by some random account, with speed/tempo-based file generation logic by Mystic65.
- **WerZatSong** by Nel, with contributions from Numerophobe, AzureBlast, and Mystic65.
