# Adding a new language to WerZatSonGUI

WerZatSonGUI currently ships with English and Italian simply because those are the languages that I (some random account) speak and can thus write and double-check properly, not because two is some kind of limit. If you can help translate it into another language, this guide walks you through exactly what's involved, and any translation you send in can be added to the repo officially so everyone gets to use it, not just kept as your own personal copy. DM me on Discord (.somerandomaccount) if you'd like to help with this.

WerZatSonGUI's text lives in five separate places: the main app, the console output, the installer, a small migration script, and the README. They don't share one translation system (the app mixes Python, Node.js, Inno Setup, and plain batch scripting), but all five work the same simple way: a text file full of `{placeholder}` slots that get filled in when the app runs, and if a translation is ever missing, it just quietly falls back to English instead of crashing.

This guide uses **Esperanto** as the example language everywhere below. Adding your own language works exactly the same way: just swap every `Esperanto` for your language's name written the same way, every `ESPERANTO` for your language's name in ALL CAPS, every `ESP` for your language's 3 letter code, and every `esperanto` for your language's name in lowercase, and you'll know exactly what to type. For example, adding Portuguese would mean using `Portuguese`, `PORTUGUESE`, `POR`, and `portuguese` in the exact same spots shown below.

## 1. The main app (`WerZatSonGUI.pyw`)

All of the app's text (buttons, labels, and the little **[?]** help popups in Advanced Settings) lives in pairs of JSON files inside `assets/localizations/`. Taking into account English and Italian, they are: `gui_strings_English.json`, `gui_strings_Italiano.json`, `advanced_setting_explanations_English.json`, and `advanced_setting_explanations_Italiano.json`. Each one is just a simple list of `"key": "some text"` pairs. Some of that text contains a `{placeholder}` like `{count}`, which gets swapped for a real number or word while the app is running, so leave those exactly as they are, brackets and spelling included, or that piece of text won't get filled in.

**To add Esperanto:**

1. Copy `gui_strings_English.json`, rename the copy to `gui_strings_Esperanto.json`, and translate every value inside (leave every `{placeholder}` untouched).
2. Do the same with `advanced_setting_explanations_English.json`, saving it as `advanced_setting_explanations_Esperanto.json`.
3. To open `WerZatSonGUI.pyw` and tell it Esperanto exists now, there are a few small spots to touch: add `GUI_STRINGS_FILE_ESPERANTO` and `SETTING_EXPLANATIONS_FILE_ESPERANTO` next to the existing English/Italian/other language file paths, add an `"Esperanto"` case wherever those files get loaded, add `"Esperanto"` to the list of accepted languages, and add a third language button next to the English/Italiano/other ones (there are two places with this button: the first-time setup screen, and the General tab of Advanced Settings).

That's it, Esperanto now shows up as a language option, and switching to it takes effect immediately, no restart needed. One small heads-up: `_change_language()` happens to be written twice in the file with identical content, only the second copy actually matters, so make your edit there (touching the first one too doesn't hurt, it just won't do anything).

## 2. What the console prints (`assets/werzatsong.js`, `assets/scripts/audfprint.js` and `assets/utils/validators.js`)

Taking English and Italian into account, everything the underlying engine prints while it's running (progress messages, warnings, the API key/webhook setup prompts) comes from `console_strings_English.json` and `console_strings_Italiano.json`, also inside `assets/localizations/`. A small helper file, `assets/utils/i18n.js`, checks `config.json` to see which language you picked in the app and loads the matching translations, falling back to English if that file is missing or unreadable, so the console still works fine even if you run it outside the GUI.

Every console line also starts with a small tag, `[INFO]` / `[SUCCESS]` / `[WARNING]` / `[ERROR]` / `[EMPTY]`, and these get translated too, using the same `tag_info` / `tag_success` / `tag_warning` / `tag_error` / `tag_empty` keys inside these same files. English keeps them as INFO/SUCCESS/WARNING/ERROR/EMPTY, and Italian uses INFO/SUCCESSO/ATTENZIONE/ERRORE/VUOTO, matching what the app's own log lines already do elsewhere. The one thing that's never translated is the actual match-report files saved to disk, since those are meant to look the same no matter what language you're using.

**To add Esperanto:**

1. Copy `console_strings_English.json` to `console_strings_Esperanto.json` and translate it (again, leave `{placeholder}` bits as-is).
2. Open `assets/utils/i18n.js` and make it so that `"Esperanto"` in `config.json` loads `console_strings_Esperanto.json`.
3. Make sure step 1 of the previous section is done too, since that's what lets `config.json` actually contain `"Esperanto"` in the first place.

## 3. The installer (`setup.iss`)

The installer's text comes from two places. The built-in wizard pages (Welcome, Next, Back, Install, and so on) come from a `.isl` translation file registered under `[Languages]`, English uses the one that ships with Inno Setup itself, and Italian uses the bundled `Languages\Italian.isl` so the build doesn't rely on anything extra being installed on the machine that compiles it. The handful of custom lines this installer adds on top (the desktop shortcut option, the dependency-install message, and similar) live under `[CustomMessages]` instead, as simple `language.KeyName=Some text` lines.

**To add Esperanto:**

1. Grab an Esperanto `.isl` file from <https://jrsoftware.org/files/istrans/> and save it as `Languages\Esperanto.isl`.
2. Add a line under `[Languages]`: `Name: "esperanto"; MessagesFile: "Languages\Esperanto.isl"`.
3. Add an `esperanto.KeyName=...` line under `[CustomMessages]` for every key that already exists there for English and Italian.
4. To make a fresh install let you choose to set the app itself to Esperanto by default, open the `[Code]` section near the bottom of `setup.iss` and add Esperanto next to the existing Italian check. Use lowercase `"esperanto"` there, since that has to match the internal `Name:` from step 2, not the language's display name.

## 4. The migration/update script (`upgrade_to_GUI.bat`)

Batch files can't really do proper translation lookups, so this script just asks which language you want right at the start, then fills in a batch of `MSG_...` variables once (one whole block per language) and uses those variables for everything from then on.

Two easy mistakes to avoid if you ever edit this script: always read a variable as `!MSG_SOMETHING!`, never `%MSG_SOMETHING%`, because if a translated message contains parentheses (easy to do in normal writing) the `%...%` form can break the script once it's inside an `if` block. And if a message needs to end with a literal `!`, write it as `^!` (for example `Fatto^!`), otherwise it silently disappears when the variable gets read later.

**To add Esperanto:**

1. Add a new option to the language menu at the top of the script, e.g. `[3] Esperanto`, and a matching line that sets `LANG=esperanto` when someone picks it.
2. Copy the whole `:set_strings_english` block, rename the copy to `:set_strings_esperanto`, translate every message inside it (remembering the `^!` rule above for any message ending in `!`), and add a `goto set_strings_esperanto` line next to the existing English/Italian ones near the top.

## 5. The README (`README.md`)

Lastly, the README is the general guide users first see when going to the project's GitHub repo.

**To add Esperanto:**

1. Copy the file called `README.md`, translate it, and rename it `README_ESP.md`
2. Add a reference to Esperanto in the other existing README files (e.g. `README.md`, `README_ITA.md`...)

## A few things that apply to all five

Keep every `{placeholder}` spelled exactly like the English original, it's a plain text swap rather than smart matching, so a typo just means that piece of text silently never gets filled in. If you're not sure how formal or casual to sound, just try to make the text as widely and easily understandable as possible.