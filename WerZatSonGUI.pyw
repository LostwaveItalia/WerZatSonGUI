import sys
import os
import traceback
from datetime import datetime

crash_log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "crash_logs.txt")
errlog_gui_file = open(crash_log_path, "a", buffering=1)

class Tee:
    def __init__(self, *files):
        self.files = files
    def write(self, obj):
        for f in self.files:
            if f:
                f.write(obj)
                f.flush()
    def flush(self):
        for f in self.files:
            if f:
                f.flush()

# This redirects streams immediately before importing pywinstyles, which can create a specific bug affecting .pyw files
sys.stdout = Tee(sys.stdout, errlog_gui_file)
sys.stderr = Tee(sys.stderr, errlog_gui_file)

try:
    import sv_ttk
    import darkdetect
    import pywinstyles

    import concurrent.futures
    import ctypes
    from ctypes import wintypes

    if os.name == "nt":
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
                "LostwaveItalia.WerZatSonGUI"
            )
        except Exception:
            pass
        
    import contextlib
    import io
    import importlib
    import json
    import math
    import queue
    import re
    import shutil
    import subprocess
    import tempfile
    import threading
    import time
    import webbrowser

    import tkinter as tk
    import tkinter.font as tkfont
    from tkinter import ttk, filedialog, messagebox, simpledialog
    from tkinter.scrolledtext import ScrolledText

except Exception as e:
    error_details = traceback.format_exc()

    python_dir = os.path.dirname(sys.executable)
    pyw_folder = os.path.dirname(os.path.abspath(__file__))
    req_file = os.path.join(pyw_folder, "requirements.txt")

    possible_exes = ["py.exe", "python.exe", "python3.exe"]
    python_executable = None
    for exe in possible_exes:
        exe_path = os.path.join(python_dir, exe)
        if os.path.exists(exe_path):
            python_executable = exe_path
            break

    error_msg = (
    f"Crash prevented!\n\n"
    f"Windows is running this file using:\n{sys.executable}\n"
    f"The installation listed above could have missing dependencies.\n"
    f"You may have multiple Python installations, or Visual Studio Build Tools could be missing.\n"
    f"Make sure to properly install the Visual Studio Build Tools with the \"Desktop Development with C++\" option checked, restart your PC, then install the remaining requirements, by running the following command in cmd or PowerShell (which you can copy from the crash_logs.txt file):\n\n"
    f"\"{python_executable}\" -m pip install -r {pyw_folder}\\requirements.txt\n\n"
    f"Guide on how to fix the error: https://github.com/LostwaveItalia/WerZatSonGUI/tree/main#troubleshooting-how-to-fix-the-missing-dependencies--crash-prevented-startup-error\n\n"
    f"Error details:\n{error_details}"
    )

    # Writes explicitly to the log file as a safety net
    try:
        with open(crash_log_path, "a", encoding="utf-8") as f:
            f.write(f"\n--- Crash Log [{datetime.now()}] ---\n")
            f.write(error_msg)
    except Exception:
        pass

    # Safely attempts to install missing dependencies
    import subprocess

    # Runs pip directly through the current Python executable, avoiding cmd.exe
    try:
        # In a standard console window showing the pip install progress
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", req_file],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
            check=True
        )
        
        # If it succeeds, politely asks the user to restart instead of forcing it
        success_msg = "Missing dependencies were just installed!\n\nPlease close this window and launch the application again."

        import tkinter as tk
        from tkinter import messagebox
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Missing Dependencies Installed", success_msg)
        root.destroy()
        sys.exit(0)

    except subprocess.CalledProcessError:

    # Shows an error box if automatic fix isn't possible
        try:
            # Try to use standard tkinter instead of raw Windows API calls
            import tkinter as tk
            from tkinter import messagebox
            
            # Creates a hidden main window so the user just gets the popup
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror("WerZatSonGUI Failed To Start", error_msg)
            root.destroy()
            
        except Exception:
            # If even tkinter fails, just write to the stderr log (which your Tee class catches)
            print(error_msg, file=sys.stderr)

        sys.exit(1)
# ============================================================================================
# Paths (all relative to the folder this script lives in)
# ============================================================================================

CUR_FOLDER = os.path.dirname(os.path.abspath(__file__))
ASSETS_FOLDER = os.path.join(CUR_FOLDER, "assets")
CONFIG_FILE = os.path.join(CUR_FOLDER, "config.json")
ENV_FILE = os.path.join(ASSETS_FOLDER, ".env")
ENV_EXAMPLE_FILE = os.path.join(ASSETS_FOLDER, ".env.example")
AUDIOTAG_KEYS_FILE = os.path.join(ASSETS_FOLDER, "audiotag_keys.json")
AUDIOTAG_KEYS_EXAMPLE_FILE = os.path.join(ASSETS_FOLDER, "audiotag_keys.example.json")
LOGO_FILE = os.path.join(ASSETS_FOLDER, "logo.png")
LOGO_ICO_FILE = os.path.join(ASSETS_FOLDER, "logo.ico")
WEBHOOK_JS_FILE = os.path.join(ASSETS_FOLDER, "utils", "webhook.js")

SETTING_EXPLANATIONS_FILE_ENGLISH = os.path.join(ASSETS_FOLDER, "localizations", "advanced_setting_explanations_English.json")
SETTING_EXPLANATIONS_FILE_ITALIANO = os.path.join(ASSETS_FOLDER, "localizations", "advanced_setting_explanations_Italiano.json")
SETTING_EXPLANATIONS_FILE_FRANÇAIS = os.path.join(ASSETS_FOLDER, "localizations", "advanced_setting_explanations_Français.json")
SETTING_EXPLANATIONS_FILE_PORTUGUÊS = os.path.join(ASSETS_FOLDER, "localizations", "advanced_setting_explanations_Português.json")

GUI_STRINGS_FILE_ENGLISH = os.path.join(ASSETS_FOLDER, "localizations", "gui_strings_English.json")
GUI_STRINGS_FILE_ITALIANO = os.path.join(ASSETS_FOLDER, "localizations", "gui_strings_Italiano.json")
GUI_STRINGS_FILE_FRANÇAIS = os.path.join(ASSETS_FOLDER, "localizations", "gui_strings_Français.json")
GUI_STRINGS_FILE_PORTUGUÊS = os.path.join(ASSETS_FOLDER, "localizations", "gui_strings_Português.json")

INTERNAL_INPUT_FOLDER = os.path.join(ASSETS_FOLDER, "input")
INTERNAL_TEMP_FOLDER = os.path.join(ASSETS_FOLDER, "temp")
# PROCESSED_DIR holds the two per-mode processed-songs JSON files (Quick and Long) plus the
# PKLZ folder selection JSON. These replace the old single PROCESSED.txt: a song is listed in
# a mode's JSON if it has already been scanned in that mode (or the user deliberately excluded
# it), and any song not listed there is pending for that mode. LEGACY_PROCESSED_FILE is the old
# file, kept on disk only for one-time migration (see migrate_legacy_processed_file()); once
# migrated it is renamed to LEGACY_PROCESSED_FILE + ".migrated.bak" so it stops being an
# ambiguous leftover sitting in the app folder.
PROCESSED_DIR = os.path.join(ASSETS_FOLDER, "listsProcessed")
PROCESSED_SONGS_QUICK_FILE = os.path.join(PROCESSED_DIR, "processed-songs-mode-quick.json")
PROCESSED_SONGS_LONG_FILE = os.path.join(PROCESSED_DIR, "processed-songs-mode-long.json")
PKLZ_FOLDERS_FILE = os.path.join(PROCESSED_DIR, "pklz-folders-to-process.json")
SELECTION_SUMMARY_FILE = os.path.join(PROCESSED_DIR, "selection-summary.json")
LEGACY_PROCESSED_FILE = os.path.join(CUR_FOLDER, "PROCESSED.txt")
TEMP_STAGING_DIRNAME = "___TEMP"

DEFAULT_INPUT_DIR = os.path.join(CUR_FOLDER, "db_inputs")
DEFAULT_DB_DIR = os.path.join(ASSETS_FOLDER, "database")
DEFAULT_LOG_DIR = os.path.join(CUR_FOLDER, "logs")
DEFAULT_HASH_TABLES_DIR = os.path.join(CUR_FOLDER, "hash_counts")
DEFAULT_CONSOLE_LOGS_DIR = os.path.join(CUR_FOLDER, "console_logs")
CRASH_LOG_FILE = os.path.join(CUR_FOLDER, "crash_logs.txt")
FORCE_STOP_LOG_MARKER_FILE = os.path.join(CUR_FOLDER, "force_stop_log_pending.json")
APP_VERSION = "2.1.1"

PUBLIC_PKLZ_DATABASE_URL = "https://wzs.cosine.club/"
PUBLIC_PKLZ_DATABASE_URL_ALT = "https://werzatdb.com/fingerprints"
FINGERPRINTING_GUI_URL = "https://github.com/EierkuchenHD/fingerprinter/releases"
LOSTWAVE_ITALIA_SONGS_URL = "https://drive.google.com/drive/folders/1S0Tj-PrdKzUc1jZ4c2feUGcyBABLdaEy"
FRENCH_LOSTWAVE_SONGS_URL = "https://drive.google.com/drive/folders/1NLVjBYXNdWy_kxp21Npds6T3F6QpA520"
USER_QLOSTWAVE_UPLOADS_URL = "https://drive.google.com/drive/folders/1dlU0MmdcwzYXB_LqYz9KZdokD7lO5ZMW"

SETUP_CMD = ["cmd.exe", "/c", "node", r"assets\werzatsong.js", "--audiotag", "--musicbrainz"]

# ============================================================================================
# .env handling
# ============================================================================================

REQUIRED_ENV_KEYS = ("WEBHOOK_URL", "AUDIOTAG_KEY", "ACOUSTID_KEY")
ENV_PLACEHOLDER_VALUES = {"", "<your_key>", "<your_webhook>"}
ENV_KEY_ORDER = ["ACOUSTID_KEY", "AUDIOTAG_KEY", "FFMPEG_COMMAND", "NODE_COMMAND", "PYTHON_COMMAND", "WEBHOOK_URL"]
ENV_DEFAULTS = {
    "ACOUSTID_KEY": "<your_key>",
    "AUDIOTAG_KEY": "<your_key>",
    "FFMPEG_COMMAND": "ffmpeg",
    "NODE_COMMAND": "node",
    "PYTHON_COMMAND": "python",
    "WEBHOOK_URL": "<your_webhook>",
}
# Now using translation keys
ENV_FIELD_ROWS = (
    ("ACOUSTID_KEY", "acoustid_key_label"),
    ("AUDIOTAG_KEY", "audiotag_key_label"),
    ("WEBHOOK_URL", "webhook_url_label"),
)

DIRECTORY_ROWS = (
    ("input_dir", "input_dir_label"),
    ("db_dir", "db_dir_label"),
    ("log_dir", "log_dir_label"),
)

# ============================================================================================
# Tempo arrays (negative = <1.0 slow-down/pitch-down group, positive = >1.0 speed-up/pitch-up group)
# ============================================================================================

NEGATIVE_TEMPO_DEFAULT = [0.9, 0.905, 0.91, 0.915, 0.92, 0.925, 0.93, 0.935, 0.94, 0.945,
                           0.95, 0.955, 0.96, 0.965, 0.97, 0.975, 0.98, 0.985, 0.99, 0.995]
POSITIVE_TEMPO_DEFAULT = [1.005, 1.01, 1.015, 1.02, 1.025, 1.03, 1.035, 1.04, 1.045, 1.05,
                          1.055, 1.06, 1.065, 1.07, 1.075, 1.08, 1.085, 1.09, 1.095, 1.1]

AUDIO_EXTENSIONS = {".mp3", ".wav", ".flac", ".m4a"}
# werzatsong.js itself still only recognizes .mp3 (see assets/werzatsong.js's loadSamples()):
# these get converted to .mp3 up front instead (see _convert_non_mp3_files_to_mp3), so the
# whole downstream pipeline only ever has to deal with one format.
NON_MP3_AUDIO_EXTENSIONS = AUDIO_EXTENSIONS - {".mp3"}
CONVERTING_TMP_SUFFIX = ".converting.tmp"
VARIATION_CHUNK_SIZE = 30
QUICK_BATCH_CHUNK_SIZE = 30
# werzatsong.js's own MAX_FILES_PER_SEARCH: a single search/scan must never exceed this,
# but batches should otherwise stick to VARIATION_CHUNK_SIZE/QUICK_BATCH_CHUNK_SIZE if different
# for whatever reason (see compute_batch_sizes below).
MAX_FILES_PER_BATCH_HARD_LIMIT = 30
OUTPUT_BITRATE = "192k"

CONSOLE_FONT_FAMILY = "Consolas"
CONSOLE_FONT_DEFAULT = 9
CONSOLE_FONT_MIN = 6
CONSOLE_FONT_MAX = 24

ANSI_ESCAPE_RE = re.compile(r"\x1b\[([0-9;]*)([A-Za-z])")
# Maps chalk's SGR foreground color codes (see assets/utils/messages.js's Message object:
# cyan/gray/greenBright/redBright/yellow) to the matching Tk console tag configured in
# _init_console. Any other SGR code (bold, other colors, etc.) or non-"m" escape sequence
# (cursor movement, erase line, etc. e.g. from npm/pip) is silently dropped without
# applying a tag, same as the old strip_ansi() behavior for anything not specifically
# recognized here.
CONSOLE_COLOR_TAGS = {
    "36": "console_info",
    "90": "console_empty",
    "92": "console_success",
    "91": "console_error",
    "33": "console_warning",
}
CONSOLE_RESET_CODES = {"", "0", "39"}
CONSOLE_TAG_TO_SGR = {tag: code for code, tag in CONSOLE_COLOR_TAGS.items()}
# Matches a message's own leading "[TAG]" (as already produced by _tr(...)), used by
# _console_severity_for_message to color the GUI's own log lines the same way.
LEADING_TAG_RE = re.compile(r"^\[([^\]]+)\]")
NAV_KEYSYMS = {
    "Left", "Right", "Up", "Down", "Home", "End", "Prior", "Next",
    "Shift_L", "Shift_R", "Control_L", "Control_R", "Alt_L", "Alt_R", "Tab", "Escape"
}

DEFAULT_WEBHOOK_USERNAME = "WerZatSonGUI"
DEFAULT_WEBHOOK_AVATAR = "https://cdn.discordapp.com/app-icons/1509584409748050011/5136222148bbb7541919a2e5c89924f1.webp"
WEBHOOK_USERNAME_RE = re.compile(r"const WEBHOOK_USERNAME = '.*?'")
WEBHOOK_AVATAR_RE = re.compile(r"const WEBHOOK_AVATAR = '.*?'")

# MusicBrainz --duration/--extension limits (mirrors assets/utils/validators.js exactly,
# including the extension floor of 1 that its own README text doesn't call out)
MUSICBRAINZ_DURATION_MIN = 30
MUSICBRAINZ_DURATION_MAX = 600
MUSICBRAINZ_DURATION_MIN_DEFAULT = 30
MUSICBRAINZ_DURATION_MAX_DEFAULT = 600
MUSICBRAINZ_EXTENSION_MIN = 1
MUSICBRAINZ_EXTENSION_MAX = 25
MUSICBRAINZ_EXTENSION_DEFAULT = 25

# Audfprint --shifts ("Search Depth") limits (mirrors assets/werzatsong.js's own 1-8 range
# and its default of 4)
SEARCH_DEPTH_MIN = 1
SEARCH_DEPTH_MAX = 8
SEARCH_DEPTH_DEFAULT = 4

# AudioTag safety-dial limits: cooldown/pause are plain seconds, rotate-after-tracks mirrors
# the Node side's AudiotagKeyManager checkpoint (assets/utils/audiotagKeys.js), and min
# duration's floor of 5 matches the AudioTag API's own documented minimum file duration.
AUDIOTAG_COOLDOWN_MIN = 10
AUDIOTAG_COOLDOWN_MAX = 300
AUDIOTAG_COOLDOWN_MIN_DEFAULT = 10
AUDIOTAG_COOLDOWN_MAX_DEFAULT = 30
AUDIOTAG_ROTATE_AFTER_MIN = 100
AUDIOTAG_ROTATE_AFTER_MAX = 1000
AUDIOTAG_ROTATE_AFTER_DEFAULT = 100
AUDIOTAG_PAUSE_SECONDS_MIN = 60
AUDIOTAG_PAUSE_SECONDS_MAX = 3600
AUDIOTAG_PAUSE_SECONDS_DEFAULT = 300
AUDIOTAG_MIN_DURATION_MIN = 5
AUDIOTAG_MIN_DURATION_MAX = 60
AUDIOTAG_MIN_DURATION_DEFAULT = 15

CREATIONFLAGS = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
# Used to launch the first-time setup command in its own real console window (rather than
# piping stdin/stdout through the custom Tk console), so interactive prompts behave exactly
# like they would if the user typed the command directly into a terminal themselves.
NEW_CONSOLE_FLAG = subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0


# ============================================================================================
# Config helpers
# ============================================================================================

def compute_werzatsong_cmd(config, pklz_folder_override=None):
    """Builds the argv list passed to werzatsong.js. pklz_folder_override lets the
    orchestrator force a specific PKLZ subfolder (or the full database) for a single pass
    without touching config.json:
        None  -> fall back to config's own only_use_fingerprint_subfolder / dirname
                 (unchanged pre-rework behavior, used outside of an active scan)
        ""    -> explicitly force a full-database search (no --folder flag at all)
        "<x>" -> force --folder "<x>"
    """
    cmd = ["cmd.exe", "/c", "node", r"assets\werzatsong.js"]
    if config.get("mode_musicbrainz"):
        cmd.append("--musicbrainz")
        if config.get("custom_musicbrainz_duration_range"):
            minvalue = config.get("custom_musicbrainz_duration_range_minvalue", MUSICBRAINZ_DURATION_MIN_DEFAULT)
            maxvalue = config.get("custom_musicbrainz_duration_range_maxvalue", MUSICBRAINZ_DURATION_MAX_DEFAULT)
            cmd.extend(["--duration", f"{minvalue}:{maxvalue}"])
        if config.get("custom_musicbrainz_extension"):
            extvalue = config.get("custom_musicbrainz_extension_value", MUSICBRAINZ_EXTENSION_DEFAULT)
            cmd.extend(["--extension", str(extvalue)])
    if config.get("mode_audiotag"):
        cmd.append("--audiotag")
    if config.get("mode_shazam"):
        cmd.append("--shazam")
    if config.get("mode_audfprint"):
        cmd.append("--audfprint")
        if pklz_folder_override is not None:
            if pklz_folder_override != "":
                # Two separate list elements, "--folder" and the plain folder name: subprocess
                # itself adds the surrounding quotes when it assembles the final command-line
                # string that Windows' CreateProcess sees. Writing quote characters so would make the
                # quotes part of the argument's VALUE instead of a string-assembly artifact,
                # and node's argv parser would then look up a folder whose name literally
                # starts with a stray '"' character and fail with a confusing "not found"
                # error that has nothing to do with the folder actually being missing.
                cmd.extend(["--folder", pklz_folder_override])
        elif config.get("only_use_fingerprint_subfolder"):
            cmd.extend(["--folder", config.get("fingerprint_subfolder_dirname") or "default_subdir"])
        if config.get("use_custom_thread_count"):
            cmd.extend(["--threads", str(config.get("custom_thread_count_value") or "4")])
        if config.get("use_custom_search_depth"):
            cmd.extend(["--shifts", str(config.get("custom_search_depth_value") or str(SEARCH_DEPTH_DEFAULT))])
    return cmd


def default_config():
    return {
        "envfile_dir": ENV_FILE,
        "envfile_example_dir": ENV_EXAMPLE_FILE,
        "input_dir": DEFAULT_INPUT_DIR,
        "db_dir": DEFAULT_DB_DIR,
        "log_dir": DEFAULT_LOG_DIR,
        "hash_tables_dir": DEFAULT_HASH_TABLES_DIR,
        "console_logs_dir": DEFAULT_CONSOLE_LOGS_DIR,
        "mode_musicbrainz": True,
        "mode_audiotag": True,
        "mode_shazam": True,
        "mode_audfprint": True,
        # scan_mode is the three-way top-level mode switch that replaced the old boolean
        # generate_different_tempos. It selects which search modes run in a given session:
        #   "quick" -> only the original audio files are scanned (fast; this is the default,
        #              matching the original generate_different_tempos=False)
        #   "long"  -> only tempo/pitch variations (plus the original, for songs that have not
        #              yet had a Quick pass) are scanned
        #   "both"  -> Quick runs to completion first, then Long
        "scan_mode": "quick",
        "negative_tempo_array": list(NEGATIVE_TEMPO_DEFAULT),
        "positive_tempo_array": list(POSITIVE_TEMPO_DEFAULT),
        "only_use_fingerprint_subfolder": False,
        "fingerprint_subfolder_dirname": "default_subdir",
        "use_custom_webhook_name": False,
        "custom_webhook_name_value": DEFAULT_WEBHOOK_USERNAME,
        "use_custom_webhook_image": False,
        "custom_webhook_image_link": DEFAULT_WEBHOOK_AVATAR,
        "use_custom_thread_count": False,
        "custom_thread_count_value": "4",
        "use_custom_search_depth": False,
        "custom_search_depth_value": str(SEARCH_DEPTH_DEFAULT),
        "custom_musicbrainz_duration_range": False,
        "custom_musicbrainz_duration_range_minvalue": MUSICBRAINZ_DURATION_MIN_DEFAULT,
        "custom_musicbrainz_duration_range_maxvalue": MUSICBRAINZ_DURATION_MAX_DEFAULT,
        "custom_musicbrainz_extension": False,
        "custom_musicbrainz_extension_value": MUSICBRAINZ_EXTENSION_DEFAULT,
        "audiotag_use_multiple_keys": False,
        "custom_audiotag_cooldown_min_value": AUDIOTAG_COOLDOWN_MIN_DEFAULT,
        "custom_audiotag_cooldown_max_value": AUDIOTAG_COOLDOWN_MAX_DEFAULT,
        "custom_audiotag_rotate_after_tracks_value": AUDIOTAG_ROTATE_AFTER_DEFAULT,
        "custom_audiotag_pause_seconds_value": AUDIOTAG_PAUSE_SECONDS_DEFAULT,
        "custom_audiotag_min_duration_value": AUDIOTAG_MIN_DURATION_DEFAULT,
        "theme_mode": "System",
        "language": "English",
        "create_pklz_hash_tables_on_load_val": False,
        # Copy/Move preference for the Add PKLZ Files.../Add Audio Files... dialogs. "move"
        # (the default) copies the source into the destination, then deletes the original
        # after a successful copy (see _is_safe_to_delete_source for the safety check that
        # guards this). "copy" leaves the originals where they are, matching the pre-rework
        # behavior. These two keys are independent and are written directly by each dialog's
        # own radio group, not through _sync_widgets_to_config (see _prompt_files_or_folder).
        "add_pklz_action": "move",
        "add_audio_action": "move",
        "WERZATSONG_CMD": [],
    }


def _is_number_list(value):
    # An empty list is deliberately allowed here: it lets negative_tempo_array/
    # positive_tempo_array be explicitly emptied (see parse_tempo_list) and have that
    # persist correctly across config.json reloads, instead of always reverting to the
    # non-empty default the moment the app restarts.
    return isinstance(value, list) and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in value)


def _valid_int_in_range(value, min_v, max_v):
    """Returns value as an int if it is an int (not bool) within [min_v, max_v], else None."""
    if isinstance(value, bool) or not isinstance(value, int):
        return None
    if value < min_v or value > max_v:
        return None
    return value


def validate_config(raw):
    """Merge whatever is on disk over the computed defaults, falling back to the default
    for any key that is missing or looks malformed."""
    result = default_config()
    if isinstance(raw, dict):
        bool_keys = ["mode_musicbrainz", "mode_audiotag", "mode_shazam", "mode_audfprint",
                     "only_use_fingerprint_subfolder",
                     "use_custom_webhook_name", "use_custom_webhook_image", "use_custom_thread_count",
                     "use_custom_search_depth", "custom_musicbrainz_duration_range", "custom_musicbrainz_extension",
                     "create_pklz_hash_tables_on_load_val", "audiotag_use_multiple_keys"]
        for key in bool_keys:
            if isinstance(raw.get(key), bool):
                result[key] = raw[key]

        # Migration from the old generate_different_tempos boolean happens before the ordinary
        # scan_mode validation below: a config.json written by the pre-rework app has
        # generate_different_tempos and no scan_mode, so this translates it once here, so
        # existing users do not silently lose their Long-mode preference on first launch of the
        # new version. A config that already has scan_mode (post-migration, or a fresh install)
        # falls through to the ordinary validation and is left as-is.
        if "scan_mode" not in raw and "generate_different_tempos" in raw:
            legacy_gt = raw.get("generate_different_tempos")
            if isinstance(legacy_gt, bool):
                result["scan_mode"] = "long" if legacy_gt else "quick"

        scan_val = raw.get("scan_mode")
        if isinstance(scan_val, str) and scan_val in ("quick", "long", "both"):
            result["scan_mode"] = scan_val

        # Copy/Move preference for the two Add-files dialogs. See default_config()'s comment
        # for the semantics. These are ordinary persistent keys; the only unusual thing about
        # them is that they are written directly by a modal dialog's own trace callback rather
        # than through _sync_widgets_to_config (see _prompt_files_or_folder).
        for key in ("add_pklz_action", "add_audio_action"):
            value = raw.get(key)
            if isinstance(value, str) and value in ("copy", "move"):
                result[key] = value

        str_keys = ["fingerprint_subfolder_dirname", "custom_webhook_name_value", "custom_webhook_image_link"]
        for key in str_keys:
            value = raw.get(key)
            if isinstance(value, str) and value.strip():
                result[key] = value

        theme_val = raw.get("theme_mode")
        if isinstance(theme_val, str) and theme_val in ["Light", "Dark", "System"]:
            result["theme_mode"] = theme_val

        lang_val = raw.get("language")
        if isinstance(lang_val, str) and lang_val in ["English", "Italiano", "Français", "Português"]:
            result["language"] = lang_val

        for key in ["input_dir", "db_dir", "log_dir", "hash_tables_dir", "console_logs_dir"]:
            value = raw.get(key)
            if isinstance(value, str) and value.strip():
                result[key] = value

        for key in ["negative_tempo_array", "positive_tempo_array"]:
            value = raw.get(key)
            if _is_number_list(value):
                result[key] = [float(v) for v in value]

        thread_value = raw.get("custom_thread_count_value")
        if isinstance(thread_value, str) and thread_value.strip().isdigit():
            result["custom_thread_count_value"] = thread_value.strip()
        elif isinstance(thread_value, int) and not isinstance(thread_value, bool):
            result["custom_thread_count_value"] = str(thread_value)

        search_depth_raw = raw.get("custom_search_depth_value")
        if isinstance(search_depth_raw, str) and search_depth_raw.strip().isdigit():
            search_depth_raw = int(search_depth_raw.strip())
        search_depth_value = _valid_int_in_range(search_depth_raw, SEARCH_DEPTH_MIN, SEARCH_DEPTH_MAX)
        result["custom_search_depth_value"] = (
            str(search_depth_value) if search_depth_value is not None else str(SEARCH_DEPTH_DEFAULT))

        duration_min = _valid_int_in_range(raw.get("custom_musicbrainz_duration_range_minvalue"),
                                            MUSICBRAINZ_DURATION_MIN, MUSICBRAINZ_DURATION_MAX)
        result["custom_musicbrainz_duration_range_minvalue"] = (
            duration_min if duration_min is not None else MUSICBRAINZ_DURATION_MIN_DEFAULT)

        duration_max = _valid_int_in_range(raw.get("custom_musicbrainz_duration_range_maxvalue"),
                                            MUSICBRAINZ_DURATION_MIN, MUSICBRAINZ_DURATION_MAX)
        result["custom_musicbrainz_duration_range_maxvalue"] = (
            duration_max if duration_max is not None else MUSICBRAINZ_DURATION_MAX_DEFAULT)

        extension_value = _valid_int_in_range(raw.get("custom_musicbrainz_extension_value"),
                                               MUSICBRAINZ_EXTENSION_MIN, MUSICBRAINZ_EXTENSION_MAX)
        result["custom_musicbrainz_extension_value"] = (
            extension_value if extension_value is not None else MUSICBRAINZ_EXTENSION_DEFAULT)

        cooldown_min = _valid_int_in_range(raw.get("custom_audiotag_cooldown_min_value"),
                                            AUDIOTAG_COOLDOWN_MIN, AUDIOTAG_COOLDOWN_MAX)
        result["custom_audiotag_cooldown_min_value"] = (
            cooldown_min if cooldown_min is not None else AUDIOTAG_COOLDOWN_MIN_DEFAULT)

        cooldown_max = _valid_int_in_range(raw.get("custom_audiotag_cooldown_max_value"),
                                            AUDIOTAG_COOLDOWN_MIN, AUDIOTAG_COOLDOWN_MAX)
        result["custom_audiotag_cooldown_max_value"] = (
            cooldown_max if cooldown_max is not None else AUDIOTAG_COOLDOWN_MAX_DEFAULT)

        rotate_after = _valid_int_in_range(raw.get("custom_audiotag_rotate_after_tracks_value"),
                                            AUDIOTAG_ROTATE_AFTER_MIN, AUDIOTAG_ROTATE_AFTER_MAX)
        result["custom_audiotag_rotate_after_tracks_value"] = (
            rotate_after if rotate_after is not None else AUDIOTAG_ROTATE_AFTER_DEFAULT)

        pause_seconds = _valid_int_in_range(raw.get("custom_audiotag_pause_seconds_value"),
                                             AUDIOTAG_PAUSE_SECONDS_MIN, AUDIOTAG_PAUSE_SECONDS_MAX)
        result["custom_audiotag_pause_seconds_value"] = (
            pause_seconds if pause_seconds is not None else AUDIOTAG_PAUSE_SECONDS_DEFAULT)

        min_duration = _valid_int_in_range(raw.get("custom_audiotag_min_duration_value"),
                                            AUDIOTAG_MIN_DURATION_MIN, AUDIOTAG_MIN_DURATION_MAX)
        result["custom_audiotag_min_duration_value"] = (
            min_duration if min_duration is not None else AUDIOTAG_MIN_DURATION_DEFAULT)

    # These two are purely derived/informational: never trust a stale value from disk
    result["envfile_dir"] = ENV_FILE
    result["envfile_example_dir"] = ENV_EXAMPLE_FILE
    result["WERZATSONG_CMD"] = compute_werzatsong_cmd(result)
    return result


def load_config():
    raw = {}
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except Exception:
            raw = {}
    return validate_config(raw)

def load_gui_strings(language="English"):
    """Loads the GUI translation dictionary from the appropriate JSON file."""
    if language == "Italiano":
        file_path = GUI_STRINGS_FILE_ITALIANO
    elif language == "Français":
        file_path = GUI_STRINGS_FILE_FRANÇAIS
    elif language == "Português":
        file_path = GUI_STRINGS_FILE_PORTUGUÊS
    else:
        file_path = GUI_STRINGS_FILE_ENGLISH
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def load_setting_explanations(language="English"):
    """Loads the short popup explanations shown behind each advanced setting's [?] button.
    The language parameter selects which JSON file to load. Missing/malformed file falls back
    to an empty dict, and the help popup will show a generic message."""
    if language == "Italiano":
        file_path = SETTING_EXPLANATIONS_FILE_ITALIANO
    elif language == "Français":
        file_path = SETTING_EXPLANATIONS_FILE_FRANÇAIS
    elif language == "Português":
        file_path = SETTING_EXPLANATIONS_FILE_PORTUGUÊS
    else:
        file_path = SETTING_EXPLANATIONS_FILE_ENGLISH
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def save_config(config):
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4)
        return True
    except Exception:
        return False


def format_tempo_list(values):
    return "[" + ", ".join(str(v) for v in values) + "]"


def parse_tempo_list(text, fallback):
    """Parses a tempo array text field. Explicitly empty input ("", "[]", or brackets
    containing only whitespace) returns a genuine empty list rather than the fallback -
    callers combine both tempo arrays and only fall back to the full default set when
    BOTH end up empty, so blanking a single field means "skip this half, use only the
    other one". Malformed/unparsable non-empty text (e.g. stray non-numeric tokens)
    still falls back to whatever was previously stored, same as before."""

    text = (text or "").strip()
    if text.startswith("[") and text.endswith("]"):
        text = text[1:-1]

    # Standardize commas inside numbers before splitting entries
    parts = [p.strip() for p in text.split(",") if p.strip()]
    if not parts:
        return []

    values = []
    try:
        for p in parts:
            # Replace European decimal commas with standard dots
            clean_num = p.replace(",", ".") if p.count(",") == 0 or "." in p else p
            values.append(float(clean_num))
    except ValueError:
        return list(fallback)
    return values


# ============================================================================================
# Processed-songs / PKLZ-selection JSON helpers (assets/listsProcessed/*.json)
# ============================================================================================
# These replace the old single PROCESSED.txt with three small JSON files: one processed-songs
# list per scan mode (Quick, Long), plus the PKLZ folder selection. All reads go through
# load_json_file (never raises), and all writes go through atomic_write_json (write to a .tmp
# file, then os.replace), so a crash or Force Stop mid-write can never leave a half-written,
# corrupt JSON file on disk. The higher-level helpers that need self._log/self._tr/
# self.config_data (load/save of the processed-songs sets, the PKLZ selection, and the legacy
# migration) live as methods on WerZatSongGUI itself, further down.

def load_json_file(path, default):
    """Reads and parses a JSON file, returning `default` on any error: missing file,
    unreadable file, or malformed JSON. Never raises."""
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def atomic_write_json(path, data):
    """Writes `data` as JSON to `path` atomically: writes to `path + ".tmp"` first, then
    os.replace()s it into place, so a reader never sees a half-written file and a crash mid-
    write leaves the original file (if any) untouched. Creates the parent directory first
    (idempotent, safe to call on every write) so the very first save on a fresh install does
    not fail just because assets/listsProcessed/ doesn't exist yet. Returns True/False."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp_path = path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        os.replace(tmp_path, path)
        return True
    except Exception:
        return False


def atomic_write_json_staged(path, data):
    """Same as atomic_write_json, but stops short of the os.replace(): only writes
    `path + ".tmp"` and leaves it on disk. Paired with atomic_replace_staged(path), this lets a
    caller stage several files first and only then commit all of them, so a multi-file
    operation (see WerZatSongGUI._migrate_legacy_processed_file) is atomic as a unit instead of
    as separate independent writes. Returns True/False."""
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp_path = path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception:
        return False


def atomic_replace_staged(path):
    """Commits a file previously staged by atomic_write_json_staged: os.replace()s
    `path + ".tmp"` into `path`. Returns True/False. On failure, removes the leftover .tmp file
    so it doesn't linger on disk and get mistaken for a fresh stage on a later run."""
    tmp_path = path + ".tmp"
    try:
        os.replace(tmp_path, path)
        return True
    except Exception:
        try:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
        except Exception:
            pass
        return False


# ============================================================================================
# .env helpers
# ============================================================================================

def parse_env_file(path):
    env = {}
    if not os.path.exists(path):
        return env
    try:
        # utf-8-sig transparently strips a leading BOM if present (e.g. files saved by
        # some text editors), while still reading plain UTF-8 files with no BOM correctly
        with open(path, "r", encoding="utf-8-sig") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = line.split("=", 1)
                env[key.strip()] = value.strip().strip('"').strip("'")
    except Exception:
        pass
    return env


def env_is_complete(env):
    for key in REQUIRED_ENV_KEYS:
        if (env.get(key) or "").strip() in ENV_PLACEHOLDER_VALUES:
            return False
    return True


def write_env_file(path, env):
    lines = []
    for key in ENV_KEY_ORDER:
        value = env.get(key)
        if value is None or value == "":
            value = ENV_DEFAULTS.get(key, "")
        lines.append(f"{key}={value}")
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(lines) + "\n")
        return True
    except Exception:
        return False


# ============================================================================================
# AudioTag multi-key rotation state (assets/audiotag_keys.json). Both this GUI and the Node
# side (assets/utils/audiotagKeys.js) read/write this same file, the same way both sides
# already touch .env: the GUI only ever edits the key list itself (add/remove), while usage
# counters and status are updated exclusively by the Node side while a scan runs.
# ============================================================================================

AUDIOTAG_KEY_STATUSES = ("ok", "exhausted", "invalid")


def load_audiotag_keys():
    if not os.path.exists(AUDIOTAG_KEYS_FILE):
        if os.path.exists(AUDIOTAG_KEYS_EXAMPLE_FILE):
            try:
                shutil.copyfile(AUDIOTAG_KEYS_EXAMPLE_FILE, AUDIOTAG_KEYS_FILE)
            except Exception:
                pass
        else:
            return {"activeIndex": 0, "keys": []}
    try:
        with open(AUDIOTAG_KEYS_FILE, "r", encoding="utf-8") as f:
            raw = json.load(f)
    except Exception:
        raw = {}
    keys = []
    for entry in (raw.get("keys", []) if isinstance(raw, dict) else []):
        if not isinstance(entry, dict):
            continue
        key = str(entry.get("key", "")).strip()
        if not key:
            continue
        status = entry.get("status")
        if status not in AUDIOTAG_KEY_STATUSES:
            status = "ok"
        tracks_used = entry.get("tracksUsed")
        if not isinstance(tracks_used, int) or isinstance(tracks_used, bool) or tracks_used < 0:
            tracks_used = 0
        keys.append({
            "key": key,
            "tracksUsed": tracks_used,
            "status": status,
            "lastError": entry.get("lastError") if isinstance(entry.get("lastError"), str) else None,
            "lastUsedAt": entry.get("lastUsedAt") if isinstance(entry.get("lastUsedAt"), str) else None,
        })
    active_index = raw.get("activeIndex") if isinstance(raw, dict) else 0
    if not isinstance(active_index, int) or isinstance(active_index, bool) or not (0 <= active_index < len(keys)):
        active_index = 0
    return {"activeIndex": active_index, "keys": keys}


def save_audiotag_keys(data):
    try:
        os.makedirs(os.path.dirname(AUDIOTAG_KEYS_FILE), exist_ok=True)
        with open(AUDIOTAG_KEYS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception:
        return False


# ============================================================================================
# webhook.js sync (config.json is always the source of truth for these two constants)
# ============================================================================================

def _js_escape_single_quotes(value):
    return (value or "").replace("\\", "\\\\").replace("'", "\\'")


def sync_webhook_js(config):
    if not os.path.exists(WEBHOOK_JS_FILE):
        return False
    try:
        with open(WEBHOOK_JS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return False

    username = config.get("custom_webhook_name_value") or DEFAULT_WEBHOOK_USERNAME
    if not config.get("use_custom_webhook_name"):
        username = DEFAULT_WEBHOOK_USERNAME
    avatar = config.get("custom_webhook_image_link") or DEFAULT_WEBHOOK_AVATAR
    if not config.get("use_custom_webhook_image"):
        avatar = DEFAULT_WEBHOOK_AVATAR

    new_content = WEBHOOK_USERNAME_RE.sub(
        f"const WEBHOOK_USERNAME = '{_js_escape_single_quotes(username)}'", content, count=1)
    new_content = WEBHOOK_AVATAR_RE.sub(
        f"const WEBHOOK_AVATAR = '{_js_escape_single_quotes(avatar)}'", new_content, count=1)

    if new_content != content:
        try:
            with open(WEBHOOK_JS_FILE, "w", encoding="utf-8", newline="\n") as f:
                f.write(new_content)
        except Exception:
            return False
    return True


# ============================================================================================
# Process tree tracking (used by Force Stop and by closing the window mid-run)
# ============================================================================================
# Every subprocess this app launches while a scan is running, the node werzatsong.js console
# command, plus every ffmpeg/ffprobe call used to generate tempo/pitch variations, registers
# its PID here for as long as it's "alive". Force Stop (and the "close while running" prompt)
# walks this set and kills each one's full process tree, since a plain .terminate() on just
# the top-level process can leave grandchildren running as orphans (audfprint forks several
# worker processes of its own, and werzatsong.js's node process itself is usually wrapped in
# a cmd.exe parent).
_tracked_pids_lock = threading.Lock()
_tracked_pids = set()


def _track_pid(pid):
    with _tracked_pids_lock:
        _tracked_pids.add(pid)


def _untrack_pid(pid):
    with _tracked_pids_lock:
        _tracked_pids.discard(pid)


def _kill_pid_tree(pid):
    try:
        subprocess.run(
            ["taskkill", "/F", "/T", "/PID", str(pid)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=CREATIONFLAGS
        )
    except Exception:
        pass


def _kill_all_tracked_processes():
    with _tracked_pids_lock:
        pids = list(_tracked_pids)
    for pid in pids:
        _kill_pid_tree(pid)


def run_tracked(cmd, capture_stdout=False):
    """Same contract as subprocess.run(cmd, check=True, ...), but registers the child's PID
    while it runs so Force Stop can kill it immediately instead of waiting for it to finish
    on its own. Always captures stderr (regardless of capture_stdout) so a failure's
    CalledProcessError carries the tool's actual error text instead of just an exit code -
    ffmpeg/ffprobe only ever write their real error details to stderr."""
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE if capture_stdout else subprocess.DEVNULL,
        stderr=subprocess.PIPE,
        creationflags=CREATIONFLAGS
    )
    _track_pid(process.pid)
    try:
        stdout, stderr = process.communicate()
    finally:
        _untrack_pid(process.pid)
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, cmd, output=stdout, stderr=stderr)
    return stdout


def format_subprocess_error(e, max_lines=4):
    """Returns a short, useful description of a failed subprocess call: the last few
    non-empty lines of stderr for a CalledProcessError that has one (where ffmpeg/ffprobe
    write their real error), or str(e) for anything else (e.g. a plain OSError)."""
    if isinstance(e, subprocess.CalledProcessError) and e.stderr:
        raw = e.stderr
        text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else str(raw)
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        if lines:
            return " | ".join(lines[-max_lines:])
    return str(e)


# ============================================================================================
# Work-area-aware window geometry (keeps windows from overlapping the taskbar)
# ============================================================================================

SPI_GETWORKAREA = 0x0030


def get_work_area():
    """Returns (left, top, right, bottom) of the primary monitor's work area (the visible
    screen area excluding the taskbar), or None if the Win32 call fails for any reason."""
    try:
        rect = wintypes.RECT()
        if ctypes.windll.user32.SystemParametersInfoW(SPI_GETWORKAREA, 0, ctypes.byref(rect), 0):
            return rect.left, rect.top, rect.right, rect.bottom
    except Exception:
        pass
    return None


def compute_clamped_geometry(root, width, height, min_width, min_height, margin=20):
    """Returns (geometry_string, (min_w, min_h)) sized/positioned to fit within the
    taskbar-aware work area instead of blindly using the requested size: a window taller
    than the visible work area (e.g. a smaller display, higher DPI scaling, or a taskbar
    docked somewhere non-default) would otherwise get pushed partly behind the taskbar."""
    work_area = get_work_area()
    if work_area:
        left, top, right, bottom = work_area
        avail_w = right - left
        avail_h = bottom - top
    else:
        left, top = 0, 0
        avail_w = root.winfo_screenwidth()
        # No work-area info available: fall back to the full screen height minus a
        # conservative taskbar allowance, rather than assuming the whole screen is usable.
        avail_h = max(root.winfo_screenheight() - 48, 480)

    final_w = min(width, max(avail_w - margin, 320))
    final_h = min(height, max(avail_h - margin, 480))
    final_min_w = min(min_width, final_w)
    final_min_h = min(min_height, final_h)

    x = left + max((avail_w - final_w) // 2, 0)
    y = top + max((avail_h - final_h) // 2, 0)

    return f"{final_w}x{final_h}+{x}+{y}", (final_min_w, final_min_h)


# ============================================================================================
# Theme / Filesystem / ffmpeg helpers (ported from temp/werzatsongrunner.py)
# ============================================================================================

def setup_theme_listener(root):
    """Starts a background thread to listen for OS-level theme changes."""
    def on_theme_change(theme_name):
        # Safely trigger your theme application function on the main Tkinter thread
        if getattr(root, "config_data", {}).get("theme_mode", "System") == "System":
            root.after(0, lambda: apply_theme_to_gui(root, "System"))

    # Run darkdetect's listener in a background daemon thread so it closes cleanly with the app
    listener_thread = threading.Thread(
        target=darkdetect.listener,
        args=(on_theme_change,),
        daemon=True
    )
    listener_thread.start()


def apply_titlebar_theme(window, theme_mode="System"):
    """Applies the native OS title-bar theme (dark/light) to any window (root or
    Toplevel). sv_ttk only styles the widget tree *inside* a window; the OS-drawn
    title bar needs this DWM/pywinstyles treatment separately, which is why every
    Toplevel must also call this."""
    if theme_mode == "Light":
        target_theme = "light"
    elif theme_mode == "Dark":
        target_theme = "dark"
    else:
        target_theme = darkdetect.theme() or "light"
    target_theme = target_theme.lower()
    is_dark = (target_theme == "dark")

    # Ensure the toplevel's HWND is actually realized before we poke DWM. Without
    # this, calling DwmSetWindowAttribute on a just-created Toplevel is a silent
    # no-op on Windows: the frame hasn't been created yet, so there's nothing for
    # the attribute to attach to. This is why after_idle alone was not enough.
    try:
        window.update_idletasks()
    except tk.TclError:
        return

    version = sys.getwindowsversion()
    is_server = getattr(version, 'product_type', 1) != 1

    try:
        if version.major == 10 and version.build >= 22000:
            try:
                pywinstyles.apply_style(window, "dark" if is_dark else "normal")
            except Exception:
                hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
                value = ctypes.c_int(1 if is_dark else 0)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, 20, ctypes.byref(value), ctypes.sizeof(value))
            try:
                pywinstyles.change_header_color(window, "#1c1c1c" if is_dark else "#fafafa")
            except Exception:
                pass

        elif version.major == 10:
            if is_server:
                hwnd = ctypes.windll.user32.GetParent(window.winfo_id())
                attribute = 20 if version.build >= 18985 else 19
                value = ctypes.c_int(1 if is_dark else 0)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd, attribute, ctypes.byref(value), ctypes.sizeof(value))
            else:
                pywinstyles.apply_style(window, "dark" if is_dark else "normal")

            window.wm_attributes("-alpha", 0.99)
            window.wm_attributes("-alpha", 1)

    except Exception as e:
        print(f"[WARNING]: Could not apply custom title bar styles: {e}")


def apply_theme_to_gui(root, theme_mode="System"):
    if theme_mode == "Light":
        target_theme = "light"
    elif theme_mode == "Dark":
        target_theme = "dark"
    else:
        target_theme = darkdetect.theme() or "light"
    target_theme = target_theme.lower()
    sv_ttk.set_theme(target_theme)

    apply_titlebar_theme(root, theme_mode)
    for child in root.winfo_children():
        if isinstance(child, tk.Toplevel):
            apply_titlebar_theme(child, theme_mode)

class ThemedToplevel(tk.Toplevel):
    """Toplevel that mirrors the main window's native title-bar theme.

    Plain tk.Toplevel gets sv_ttk-styled widget contents but keeps the OS-default
    (light) title bar, because sv_ttk cannot reach the DWM-drawn frame. This
    subclass applies the same title-bar treatment the root window gets in
    apply_theme_to_gui, and walks up the master chain so nested dialogs (e.g.
    the ones created inside _prompt_files_or_folder) find the root's config_data
    too.
    """
    def __init__(self, master=None, **kwargs):
        super().__init__(master=master, **kwargs)

        theme_mode = "System"
        widget = master
        while widget is not None:
            if hasattr(widget, "config_data"):
                theme_mode = widget.config_data.get("theme_mode", "System")
                break
            widget = getattr(widget, "master", None)

        self._titlebar_themed = False

        def _on_map(_event=None):
            # Fires the first time the window is actually shown. At that point the
            # OS-level frame exists, so DWM will accept the style change. Also
            # re-applies on subsequent maps (e.g. after minimize/restore) since
            # some Windows builds lose the attribute across those transitions.
            try:
                self.update_idletasks()
            except tk.TclError:
                return
            self._titlebar_themed = True
            apply_titlebar_theme(self, theme_mode)

        self.bind("<Map>", _on_map, add="+")

        # Safety net: if for any reason <Map> never fires (very old Tk, exotic WM),
        # also try once after a short delay. after_idle was too early; 60ms is
        # comfortably past the point where the frame exists on every Windows build
        # I've tested, and it's still imperceptible to a user opening a dialog.
        def _delayed_apply():
            if self._titlebar_themed:
                return
            try:
                if self.winfo_exists() and self.winfo_ismapped():
                    _on_map()
            except tk.TclError:
                pass
        self.after(60, _delayed_apply)


def format_size(num_bytes):
    """1234567 -> '1.2 MB'. Used for the PKLZ selection dialog's Size column and summary."""
    size = float(num_bytes or 0)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"

def compute_fully_checked_folders(all_files_set, checked_set):
    """Returns the top-most folder rel paths (relative to input_dir, os.sep-separated)
    whose every audio file (recursively) is in checked_set. Subfolders of an already-
    listed fully-checked folder are omitted, since they're implied by their parent."""
    from collections import defaultdict
    folder_total = defaultdict(int)
    folder_checked = defaultdict(int)
    for rel in all_files_set:
        parts = rel.split(os.sep)
        accum = ""
        for i in range(len(parts) - 1):
            accum = parts[i] if not accum else os.path.join(accum, parts[i])
            folder_total[accum] += 1
            if rel in checked_set:
                folder_checked[accum] += 1
    fully = {f for f, n in folder_total.items() if n == folder_checked[f]}
    top = []
    for f in sorted(fully):
        if any(f != anc and f.startswith(anc + os.sep) for anc in fully):
            continue
        top.append(f)
    return top


# ------------------------------------------------------------------
# PKLZ staging (database/___TEMP)
#
# Audfprint can only be pointed at a folder, so restricting a search to an arbitrary
# selection of .pklz files means physically gathering them in one place. The selected
# files are MOVED (never copied: databases run to hundreds of gigabytes) into a ___TEMP
# subfolder of the database that mirrors the database's own folder structure, and the
# scan is pointed at ___TEMP. "Use full database" moves everything back out again and
# the scan is pointed at the database root, so ___TEMP is empty whenever it is not the
# target. This is the same ___TEMP name the input folder already uses for staging songs.
#
# Every move is an os.replace() within one volume (___TEMP lives inside the database),
# so it is atomic per file and a crash mid-way can only ever leave a file in one of its
# two possible places, never lost or half-written. reconcile_pklz_staging() is
# idempotent and is re-run at the start of every scan, so an interrupted move is simply
# finished the next time round.
# ------------------------------------------------------------------

def pklz_staging_dir(db_dir):
    return os.path.join(db_dir, TEMP_STAGING_DIRNAME)


def scan_pklz_database(db_dir):
    """Every .pklz under db_dir, as {relative_path: size_bytes}, plus the set of relative
    paths currently sitting in ___TEMP rather than at their home location.

    Both locations are walked and merged by relative path, so a file the previous
    selection already staged still shows up under the folder it belongs to: the dialog
    and the reconcile both see one logical database regardless of where each file
    physically is right now. os.scandir is used rather than os.walk because DirEntry
    sizes come from the directory listing itself on Windows, which matters at 30,000
    files."""
    files = {}
    staged = set()

    def walk(base, is_staging):
        stack = [base]
        while stack:
            current = stack.pop()
            try:
                with os.scandir(current) as it:
                    for entry in it:
                        try:
                            if entry.is_dir(follow_symlinks=False):
                                # Only the top-level ___TEMP is the staging tree; a user
                                # folder that happens to share the name deeper down is data.
                                if not is_staging and current == base and entry.name == TEMP_STAGING_DIRNAME:
                                    continue
                                stack.append(entry.path)
                            elif entry.is_file(follow_symlinks=False) and entry.name.lower().endswith(".pklz"):
                                rel = os.path.relpath(entry.path, base)
                                try:
                                    size = entry.stat(follow_symlinks=False).st_size
                                except OSError:
                                    size = 0
                                files[rel] = size
                                if is_staging:
                                    staged.add(rel)
                        except OSError:
                            continue
            except OSError:
                continue

    walk(db_dir, False)
    staging = pklz_staging_dir(db_dir)
    if os.path.isdir(staging):
        walk(staging, True)
    return files, staged


def selected_pklz_set(files, folders_sel, files_sel):
    """Resolves a selection (folder relative paths + file relative paths) to the concrete
    set of .pklz relative paths it covers, against a scan_pklz_database() index. A folder
    covers every file beneath it, wherever that file physically is at the moment."""
    prefixes = [os.path.normcase(f.rstrip("\\/")) + os.sep for f in folders_sel if f]
    wanted_files = {os.path.normcase(f) for f in files_sel}
    wanted = set()
    for rel in files:
        norm = os.path.normcase(rel)
        if norm in wanted_files or any(norm.startswith(p) for p in prefixes):
            wanted.add(rel)
    return wanted


def prune_empty_dirs(root):
    """Removes empty directories under root, bottom-up, then root itself if it is empty.
    Never raises: a directory that will not go is left alone."""
    if not os.path.isdir(root):
        return
    for current, dirs, files in os.walk(root, topdown=False):
        if not dirs and not files or not os.listdir(current):
            try:
                os.rmdir(current)
            except OSError:
                pass


def reconcile_pklz_staging(db_dir, use_full, folders_sel, files_sel, on_plan=None, progress=None):
    """Makes database/___TEMP hold exactly the current selection and nothing else.

    Computes what should be staged from the selection, compares it with what is staged,
    and moves only the difference: files newly selected go in, files no longer selected
    come out. Nothing is ever overwritten; a file already present at its destination is
    reported and left where it is. With use_full every staged file goes home.

    on_plan(to_temp_count, to_db_count) is called once before any move, so a caller can
    announce what is about to happen. progress(done, total) is called after each move.

    Returns a dict: moved_in, moved_out, problems (list of (kind, rel, detail) with kind
    "conflict" or "error"), and staged_after (how many .pklz files ___TEMP holds now)."""
    files, staged = scan_pklz_database(db_dir)
    wanted = set() if use_full else selected_pklz_set(files, folders_sel, files_sel)
    staging = pklz_staging_dir(db_dir)
    to_temp = sorted(wanted - staged)
    to_db = sorted(staged - wanted)
    if on_plan:
        on_plan(len(to_temp), len(to_db))

    total = len(to_temp) + len(to_db)
    done = 0
    result = {"moved_in": 0, "moved_out": 0, "problems": [], "staged_after": 0}
    now_staged = set(staged)

    def move(src, dst, rel):
        if os.path.exists(dst):
            result["problems"].append(("conflict", rel, dst))
            return False
        try:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            os.replace(src, dst)
            return True
        except OSError as e:
            result["problems"].append(("error", rel, str(e)))
            return False

    for rel in to_temp:
        if move(os.path.join(db_dir, rel), os.path.join(staging, rel), rel):
            result["moved_in"] += 1
            now_staged.add(rel)
        done += 1
        if progress:
            progress(done, total)
    for rel in to_db:
        if move(os.path.join(staging, rel), os.path.join(db_dir, rel), rel):
            result["moved_out"] += 1
            now_staged.discard(rel)
        done += 1
        if progress:
            progress(done, total)

    # Folders emptied by moving files home are dead weight, and ___TEMP itself should not
    # exist at all when nothing is staged: a full-database scan walks the whole database
    # and an empty leftover tree is just noise in it.
    prune_empty_dirs(staging)
    result["staged_after"] = len(now_staged)
    return result


class _Tooltip:
    """Minimal hover tooltip: text_fn is called at show time so the text can be dynamic."""

    def __init__(self, widget, text_fn, delay_ms=450):
        self.widget = widget
        self.text_fn = text_fn
        self.delay_ms = delay_ms
        self._after_id = None
        self._tip = None
        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")

    def _schedule(self, _event=None):
        self._cancel()
        self._after_id = self.widget.after(self.delay_ms, self._show)

    def _cancel(self):
        if self._after_id is not None:
            try:
                self.widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _show(self):
        self._after_id = None
        text = self.text_fn() if callable(self.text_fn) else self.text_fn
        if not text or self._tip is not None:
            return
        x = self.widget.winfo_rootx() + 12
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        self._tip = tk.Toplevel(self.widget)
        self._tip.wm_overrideredirect(True)
        self._tip.wm_geometry(f"+{x}+{y}")
        frame = ttk.Frame(self._tip, padding=(8, 5), relief="solid", borderwidth=1)
        frame.pack()
        if isinstance(text, str):
            ttk.Label(frame, text=text, justify="left").pack(anchor="w")
        else:
            for item_text, is_bold in text:
                kwargs = {"text": item_text, "justify": "left"}
                if is_bold:
                    kwargs["font"] = ("Segoe UI", 9, "bold")
                ttk.Label(frame, **kwargs).pack(anchor="w")

    def _hide(self, _event=None):
        self._cancel()
        if self._tip is not None:
            try:
                self._tip.destroy()
            except Exception:
                pass
            self._tip = None


def force_clean_directory(dir_path, recreate=False):
    """Safely cleans a directory without throwing errors, and optionally recreates it."""
    for _ in range(15):
        try:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path, ignore_errors=True)
            if recreate:
                os.makedirs(dir_path, exist_ok=True)
            break
        except Exception:
            time.sleep(1)
    if recreate and not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


def apply_time_stretch(input_path, ratio, sys_temp_dir):
    if abs(ratio - 1.0) < 1e-6:
        return input_path
    steps = []
    r = ratio
    while r < 0.5 or r > 2.0:
        if r > 2.0:
            steps.append("atempo=2.0")
            r /= 2.0
        else:
            steps.append("atempo=0.5")
            r /= 0.5
    steps.append(f"atempo={r:.6f}")
    filter_str = ",".join(steps)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir=sys_temp_dir)
    temp_path = temp_file.name
    temp_file.close()

    cmd = ["ffmpeg", "-y", "-i", input_path, "-af", filter_str, temp_path]
    run_tracked(cmd)
    return temp_path


def apply_pitch_shift(input_path, semitones, sys_temp_dir):
    if abs(semitones) < 1e-6:
        return input_path

    probe_stdout = run_tracked(
        ["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=sample_rate",
         "-of", "default=noprint_wrappers=1:nokey=1", input_path],
        capture_stdout=True
    )
    sr = int(probe_stdout.decode().strip())

    ratio = 2 ** (semitones / 12)
    filters = [f"asetrate={int(sr * ratio)}", f"aresample={sr}"]
    inv = 1 / ratio

    if inv < 0.5 or inv > 2.0:
        parts = []
        r2 = inv
        while r2 < 0.5 or r2 > 2.0:
            if r2 > 2.0:
                parts.append("atempo=2.0")
                r2 /= 2.0
            else:
                parts.append("atempo=0.5")
                r2 /= 0.5
        parts.append(f"atempo={r2:.6f}")
        filters.extend(parts)
    else:
        filters.append(f"atempo={inv:.6f}")

    filter_str = ",".join(filters)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav", dir=sys_temp_dir)
    temp_path = temp_file.name
    temp_file.close()

    cmd = ["ffmpeg", "-y", "-i", input_path, "-af", filter_str, temp_path]
    run_tracked(cmd)
    return temp_path


def process_single_variation(task_data):
    input_file, tempo, target_folder, base_name, sys_temp_dir = task_data

    if tempo <= 0:
        return False, f"[WARN] Invalid tempo {tempo}"

    pitch = 12 * math.log2(tempo)
    tempo_str = f"{tempo:.4f}"
    pitch_str = f"{pitch:.4f}"
    out_file = os.path.join(target_folder, f"{base_name}_t{tempo_str}_p{pitch_str}.mp3")

    try:
        ts_path = apply_time_stretch(input_file, tempo, sys_temp_dir)
        ps_path = apply_pitch_shift(ts_path, pitch, sys_temp_dir)

        cmd = ["ffmpeg", "-y", "-i", ps_path, "-codec:a", "libmp3lame", "-b:a", OUTPUT_BITRATE, out_file]
        run_tracked(cmd)

        if ts_path != input_file and os.path.exists(ts_path):
            os.remove(ts_path)
        if ps_path not in (input_file, ts_path) and os.path.exists(ps_path):
            os.remove(ps_path)

        return True, out_file
    except Exception as e:
        return False, f"Error on {base_name} at t{tempo}: {format_subprocess_error(e)}"


def compute_batch_sizes(total, target=QUICK_BATCH_CHUNK_SIZE, hard_limit=MAX_FILES_PER_BATCH_HARD_LIMIT):
    """Splits `total` items into a list of batch sizes. Prefers batches of exactly `target`,
    but avoids ever dispatching a small leftover "tail" batch on its own: when `total` isn't
    a clean multiple of `target`, the final standard batch is merged with the remainder and
    re-split as evenly as possible (never exceeding `hard_limit` per batch) instead of being
    left as a separate, needlessly small run. For example: 21 -> [21] (not [20, 1]); 23 ->
    [23] (not [20, 3]); 41 -> [20, 21] (not [20, 20, 1])."""
    if total <= 0:
        return []

    full_batches, remainder = divmod(total, target)
    if remainder == 0:
        return [target] * full_batches

    if full_batches == 0:
        tail = total
        leading = []
    else:
        tail = target + remainder
        leading = [target] * (full_batches - 1)

    if tail <= hard_limit:
        return leading + [tail]

    tail_batches = math.ceil(tail / hard_limit)
    base, extra = divmod(tail, tail_batches)
    tail_sizes = [base + 1 if i < extra else base for i in range(tail_batches)]
    return leading + tail_sizes


class PipelineAbort(Exception):
    pass



# ============================================================================================
# Main application
# ============================================================================================

class WerZatSongGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self._should_exit = False
        self._suppress_trace = False
        self._flush_after_id = None

        self.console_queue = queue.Queue()
        self.active_process = None
        self.is_running = False
        self.pending_env = False
        self.show_state = {}
        self.dir_vars = {}
        self.env_vars = {}
        self.env_show_frames = {}
        self.env_show_buttons = {}
        self.env_hide_buttons = {}
        self._env_dirty_keys = set()
        self.env_data = {}
        self.audiotag_keys_data = load_audiotag_keys()
        self._sync_body_geometry = None

        # None = use whatever config_data says (i.e. pre-orchestration behavior). "" = force
        # a full-database search for this pass. "<x>" = force --folder "<x>" for this pass.
        # See compute_werzatsong_cmd's pklz_folder_override and _run_pipeline.
        self._runtime_pklz_folder = None
        # Set for the whole duration of an orchestrated run so _save_config_to_disk() becomes
        # a no-op: the temporary mode-toggle/folder-override state _run_pipeline flips into
        # config_data must never land in config.json. See _save_config_to_disk.
        self._suppress_config_saves = False
        # Session-level state for the input_dir-mismatch prompt (_on_start_clicked). Reset to
        # empty / all-writable at construction, not persisted across sessions: the prompt is
        # meant to fire at most once per launch, not once ever.
        self._mismatch_prompted = set()
        self._processed_json_writable = {"quick": True, "long": True}

        # Translation related
        self._text_widgets = []  # (widget, key, kwargs)
        self._notebook_tabs = []  # (notebook, tab_id, key)
        self._toggle_buttons = []  # (button, content_frame, default_expanded)
        self._env_toggle_buttons = []  # (button, key)

        self._icon_img = None
        ico_path = os.path.join(ASSETS_FOLDER, "logo.ico")
        if os.name == "nt" and os.path.exists(ico_path):
            try:
                self.iconbitmap(default=ico_path)
            except Exception:
                pass
        try:
            self._icon_img = tk.PhotoImage(file=LOGO_FILE)
            self.iconphoto(True, self._icon_img)
        except Exception:
            pass

        self.config_data = load_config()
        self.language = self.config_data.get("language", "English")
        self.setting_explanations = load_setting_explanations(self.language)
        self.gui_strings = load_gui_strings(self.language)
        self.var_language = tk.StringVar(value=self.language)
        self.var_language.trace_add("write", self._make_language_trace())
        self._audiotag_show_keys = tk.BooleanVar(value=False)

        # Runs before the UI is built (but after self.gui_strings exists, so any log line it
        # emits is localized). On a fresh install there is nothing to migrate (no legacy
        # PROCESSED.txt yet), so this is a no-op there, including on the first-time-setup path
        # where the console doesn't exist yet to display it.
        self._migrate_legacy_processed_file()

        self._boot()

        if not self._should_exit:
            self.deiconify()
            # geometry()/minsize() calls made while withdrawn can be overridden by Tk's own
            # natural-size reconciliation on first map, so re-assert them once visible.
            if getattr(self, "_target_geometry", None):
                self.geometry(self._target_geometry)
            if getattr(self, "_target_minsize", None):
                self.minsize(*self._target_minsize)

    # ------------------------------------------------------------------
    # Translation helper
    # ------------------------------------------------------------------

    def _tr(self, key, **kwargs):
        """Return the localized string for the given key, with optional formatting."""
        text = self.gui_strings.get(key, key)  # flat dict lookup, fallback to key itself
        if kwargs:
            return text.format(**kwargs)
        return text

    def _add_text_widget(self, widget, key, **kwargs):
        """Register a widget for text updates and set initial text. Returns the widget for chaining."""
        self._text_widgets.append((widget, key, kwargs))
        self._update_widget_text(widget, key, **kwargs)
        return widget

    def _update_widget_text(self, widget, key, **kwargs):
        text = self._tr(key, **kwargs)
        try:
            widget.config(text=text)
        except tk.TclError:
            pass  # Some widgets may not have a 'text' option

    def _set_all_texts(self):
        """Update all registered widgets' text based on current language."""
        for widget, key, kwargs in self._text_widgets:
            self._update_widget_text(widget, key, **kwargs)
        # Update notebook tab titles
        for notebook, frame, key in self._notebook_tabs:
            try:
                notebook.tab(frame, text=self._tr(key))
            except Exception:
                pass
        # Update toggle buttons (collapsible sections)
        for button, content_frame, _ in self._toggle_buttons:
            if content_frame.winfo_manager():
                text = self._tr("collapse_btn")
            else:
                text = self._tr("expand_btn")
            button.config(text=text)
        # Update env show/hide buttons: each button has a fixed label
        for key, show_btn in self.env_show_buttons.items():
            show_btn.config(text=self._tr("show_btn"))
            if key in self.env_hide_buttons:
                self.env_hide_buttons[key].config(text=self._tr("hide_btn"))
        # The selection summary is built from counts at display time rather than being a
        # fixed string, so it is not in _text_widgets and has to be re-rendered by hand.
        self._refresh_selection_summary_label()
        # Update window title
        if hasattr(self, '_is_first_time_setup') and self._is_first_time_setup:
            self.title(self._tr("first_time_setup_title"))
        else:
            self.title(self._tr("app_title"))

    def _set_env_command(self, env_key, value):
        """Updates a command entry in the .env file and the in-memory env_data."""
        self.env_data[env_key] = value
        # Immediately persists to disk (same as _write_env_now, but without clearing all dirty keys)
        try:
            write_env_file(ENV_FILE, self.env_data)
            self._env_dirty_keys.discard(env_key)   # remove from dirty set if present
        except Exception as e:
            messagebox.showerror(self._tr("error_title"), self._tr("env_write_error", error=e))

    def _sync_env_from_disk_force(self):
        """Reads the current .env file and force all in-memory data (and visible GUI fields)
        to match it, discarding any unsaved edits. What is written in the file takes priority."""
        disk_env = parse_env_file(ENV_FILE)
        if not disk_env:
            return  # File missing or unreadable. Nothing to do

        # Overrides self.env_data completely with the file's content
        self.env_data = disk_env
        self._env_dirty_keys.clear()

        # Updates the GUI fields for the API keys / webhook if they are currently shown
        for key in REQUIRED_ENV_KEYS:
            if key in self.env_vars:
                value = disk_env.get(key, "")
                if self.show_state.get(key):
                    self._set_var_silently(self.env_vars[key], value)
                # Even if not shown, keep the variable consistent so if the user later
                # clicks "Show" they'll see the current file value.
                else:
                    self._set_var_silently(self.env_vars[key], value)

    def _change_language(self, lang):
        if lang not in ("English", "Italiano", "Français", "Português"):
            return
        if lang == self.language:
            return
        self.language = lang
        self.config_data["language"] = lang
        self.setting_explanations = load_setting_explanations(lang)
        self.gui_strings = load_gui_strings(self.language)
        self._set_all_texts()
        self._save_config_to_disk()

    def _make_language_trace(self):
        def handler(*_args):
            if self._suppress_trace:
                return
            new_lang = self.var_language.get()
            self._change_language(new_lang)
            if getattr(self, "_is_first_time_setup", False):
                self._save_config_to_disk()
            else:
                self._schedule_flush()
        return handler

    # ------------------------------------------------------------------
    # Boot sequence
    # ------------------------------------------------------------------

    @staticmethod
    def _has_any_files(path):
        if not os.path.isdir(path):
            return False
        try:
            return len(os.listdir(path)) > 0
        except Exception:
            return False

    def _boot(self):
        env_exists = os.path.exists(ENV_FILE)
        env = parse_env_file(ENV_FILE) if env_exists else {}

        if env_is_complete(env):
            self._boot_case2(env)
            return

        if not env_exists:
            input_dir = self.config_data.get("input_dir", DEFAULT_INPUT_DIR)
            if self._has_any_files(input_dir) or self._has_any_files(INTERNAL_INPUT_FOLDER):
                messagebox.showerror(
                    self._tr("first_time_setup_title"),
                    self._tr("setup_folder_conflict", input_dir=input_dir, internal=INTERNAL_INPUT_FOLDER)
                )
                self._should_exit = True
                self.destroy()
                return

        self._boot_case1()

    def _boot_case1(self):
        self._is_first_time_setup = True
        self._target_geometry, self._target_minsize = compute_clamped_geometry(self, 520, 300, 460, 260)
        self.geometry(self._target_geometry)
        self.minsize(*self._target_minsize)
        self.title(self._tr("first_time_setup_title"))

        # Main container
        container = ttk.Frame(self, padding=20)
        container.pack(fill="both", expand=True)

        # ----- Language selection frame (shown initially) -----
        self.lang_frame = ttk.Frame(container)
        self.lang_frame.pack(fill="both", expand=True)

        self._add_text_widget(ttk.Label(self.lang_frame, font=("Segoe UI", 13, "bold")),
                              "first_time_setup_title").pack(anchor="w", pady=(0, 20))

        self._add_text_widget(ttk.Label(self.lang_frame, text=""), "language_label").pack(anchor="w", pady=(0, 5))

        lang_radio_frame = ttk.Frame(self.lang_frame)
        lang_radio_frame.pack(anchor="w", pady=(0, 20))

        self._add_text_widget(ttk.Radiobutton(lang_radio_frame, variable=self.var_language, value="English"),
                              "english_lang").pack(side="left", padx=(0, 10))
        self._add_text_widget(ttk.Radiobutton(lang_radio_frame, variable=self.var_language, value="Italiano"),
                              "italiano_lang").pack(side="left")
        self._add_text_widget(ttk.Radiobutton(lang_radio_frame, variable=self.var_language, value="Français"),
                              "français_lang").pack(side="left")
        self._add_text_widget(ttk.Radiobutton(lang_radio_frame, variable=self.var_language, value="Português"),
                              "português_lang").pack(side="left")

        self.btn_start_setup = self._add_text_widget(ttk.Button(self.lang_frame, command=self._start_setup_after_language), "start_setup_btn")
        self.btn_start_setup.pack(anchor="w", pady=(10, 0))

        # ----- Setup progress frame (hidden initially) -----
        self.setup_frame = ttk.Frame(container)
        # Not packed yet; will be shown after language selection

        self.setup_status_var = tk.StringVar(value=self._tr("setup_status_preparing"))
        self._add_text_widget(ttk.Label(self.setup_frame, textvariable=self.setup_status_var,
                                        wraplength=460, justify="left"),
                              "setup_status_preparing").pack(anchor="w", fill="x")

        self._add_text_widget(ttk.Label(self.setup_frame, wraplength=460, justify="left",
                                        foreground="#555555"),
                              "setup_instructions").pack(anchor="w", pady=(14, 0), fill="x")

        # Protocol and initial state
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _start_setup_after_language(self):
        """Hides language selection, shows setup progress, and kicks off the install chain."""
        # Disable the start button to prevent multiple clicks
        self.btn_start_setup.configure(state="disabled")
        # Hide language frame
        self.lang_frame.pack_forget()
        # Show setup frame
        self.setup_frame.pack(fill="both", expand=True)
        # Make sure all texts in setup_frame are up to date (they already are,
        # but this is safe if language changed)
        self._set_all_texts()
        # Start the installation process
        self._start_npm_install()

    def _boot_case2(self, env):
        self._is_first_time_setup = False
        for key, value in ENV_DEFAULTS.items():
            env.setdefault(key, value)
        self.env_data = env

        self._target_geometry, self._target_minsize = compute_clamped_geometry(self, 950, 960, 860, 880)
        self.geometry(self._target_geometry)
        self.minsize(*self._target_minsize)
        self.title(self._tr("app_title"))

        self._build_full_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._recompute_command()
        self._save_config_to_disk()
        self._sync_webhook_js()
        self._set_all_texts()
        self.after(300, self._check_pending_force_stop_log)

    # ------------------------------------------------------------------
    # First-time setup (CASE 1)
    # ------------------------------------------------------------------

    def _start_npm_install(self):
        # Always run npm install once, unconditionally, before the first-time setup.
        self.setup_status_var.set(self._tr("setup_installing_npm"))
        threading.Thread(target=self._npm_install_worker, daemon=True).start()

    def _npm_install_worker(self):
        self._run_in_new_terminal(["cmd.exe", "/c", "npm", "install"], cwd=CUR_FOLDER)
        self.after(0, self._start_pip_install)

    def _start_pip_install(self):
            # Always run pip install -r requirements.txt once, unconditionally, before the first-time setup.
            self.setup_status_var.set(self._tr("setup_installing_pip"))
            threading.Thread(target=self._pip_install_worker, daemon=True).start()

    def _pip_install_worker(self):
        self._run_in_new_terminal(["cmd.exe", "/c", "pip", "install", "-r", "requirements.txt"], cwd=CUR_FOLDER)
        self.after(0, self._start_first_time_setup)

    def _start_first_time_setup(self):
        os.makedirs(self.config_data.get("input_dir", DEFAULT_INPUT_DIR), exist_ok=True)
        os.makedirs(INTERNAL_INPUT_FOLDER, exist_ok=True)
        self.setup_status_var.set(self._tr("setup_opening_terminal"))
        threading.Thread(target=self._setup_worker, daemon=True).start()

    def _setup_worker(self):
        extra_env = self._directory_env_overrides()
        returncode, launch_error = self._run_in_new_terminal(SETUP_CMD, cwd=CUR_FOLDER, extra_env=extra_env)
        self.after(0, self._on_setup_process_exit, returncode, launch_error)

    def _run_in_new_terminal(self, cmd, cwd, extra_env=None):
        """Runs cmd in a brand-new, real console window instead of piping stdin/stdout
        through the custom Tk console, so interactive prompts (readline, paste, etc.)
        behave exactly like they would if the user typed the command themselves.
        Blocking, only ever call this from a background worker thread."""
        full_env = os.environ.copy()
        if extra_env:
            full_env.update({k: str(v) for k, v in extra_env.items()})
        try:
            process = subprocess.Popen(cmd, cwd=cwd, env=full_env, creationflags=NEW_CONSOLE_FLAG)
        except Exception as e:
            return None, str(e)
        process.wait()
        return process.returncode, None

    def _on_setup_process_exit(self, returncode, launch_error=None):
        if launch_error:
            messagebox.showerror(
                self._tr("setup_failed_title"),
                self._tr("setup_failed_msg", error=launch_error)
            )
            self._should_exit = True
            self.destroy()
            return

        env = parse_env_file(ENV_FILE)
        if env_is_complete(env):
            self.setup_status_var.set(self._tr("setup_complete"))
            self.after(800, self._relaunch_self)
        else:
            self.setup_status_var.set(self._tr("setup_incomplete"))
            self.after(1200, self._start_first_time_setup)

    def _relaunch_self(self):
        try:
            subprocess.Popen([sys.executable, os.path.abspath(__file__)], cwd=CUR_FOLDER, close_fds=True)
        except Exception as e:
            messagebox.showerror(
                self._tr("relaunch_failed_title"),
                self._tr("relaunch_failed_msg", error=e)
            )
        self._should_exit = True
        self.destroy()

    def _directory_env_overrides(self):
        return {
            "WERZATSONG_DATABASE_DIR": self.config_data.get("db_dir", DEFAULT_DB_DIR),
            "WERZATSONG_LOGS_DIR": self.config_data.get("log_dir", DEFAULT_LOG_DIR),
        }

    # ------------------------------------------------------------------
    # Full UI (CASE 2)
    # ------------------------------------------------------------------

    def _build_full_ui(self):
        outer = ttk.Frame(self, padding=(8, 8, 8, 12))
        outer.pack(fill="both", expand=True)

        # The action bar is packed (side="bottom") before the scrollable body below, so it
        # always keeps its own requested space at the bottom of the window: Tk's pack manager
        # carves cavity space in call order, so packing it first here guarantees it never gets
        # squeezed out even if the body's content (e.g. both collapsible sections expanded at
        # once, or a shorter window) would otherwise overflow the available height.
        self._build_action_bar(outer)

        body = self._build_scrollable_body(outer)
        self._build_console_section(body)
        self._build_env_section(body)
        self._build_directories_section(body)

        bottom = ttk.Frame(body)
        bottom.pack(fill="x", pady=(0, 6))
        bottom.columnconfigure(0, weight=1)
        bottom.columnconfigure(1, weight=2)
        self._build_modes_section(bottom)
        self._build_advanced_section(bottom)

        self._enable_body_mousewheel()
        self._enable_entry_shortcuts()

    def _build_scrollable_body(self, parent):
        """Wraps everything between the header and the action bar in a scrollable area, so
        content that doesn't fit the current window height (both collapsible sections
        expanded at once, or a shorter window/taskbar) scrolls instead of clipping. When
        there's more room than the content needs, the inner frame is stretched to match the
        canvas's own height instead of just its natural size, so `expand=True` children
        (the console) still grow to fill the extra space exactly like before this changed."""
        container = ttk.Frame(parent)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, highlightthickness=0, bd=0)
        vscroll = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vscroll.set)
        canvas.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")

        inner = ttk.Frame(canvas)
        inner_id = canvas.create_window((0, 0), window=inner, anchor="nw")

        def sync_inner_size(_event=None):
            canvas.update_idletasks()
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            display_height = max(inner.winfo_reqheight(), canvas_height)
            canvas.itemconfig(inner_id, width=canvas_width, height=display_height)
            canvas.configure(scrollregion=(0, 0, canvas_width, display_height))

        inner.bind("<Configure>", sync_inner_size)
        canvas.bind("<Configure>", sync_inner_size)

        self._body_canvas = canvas
        self._body_inner = inner
        self._sync_body_geometry = sync_inner_size
        return inner

    def _enable_body_mousewheel(self):
        """Lets the mouse wheel scroll the collapsible body from anywhere except the console
        (which keeps its own native scrolling, plus its Ctrl+Wheel zoom, untouched)."""
        canvas = self._body_canvas

        def on_wheel(event):
            canvas.yview_scroll(-1 if event.delta > 0 else 1, "units")
            return "break"

        def bind_tree(widget):
            if widget is self.console:
                return
            widget.bind("<MouseWheel>", on_wheel, add="+")
            for child in widget.winfo_children():
                bind_tree(child)

        bind_tree(self._body_inner)

    def _build_console_section(self, parent):
        wrapper = tk.Frame(parent, height=180)
        wrapper.pack(fill="both", expand=True, pady=(0, 6))
        wrapper.pack_propagate(False)
        self._console_wrapper = wrapper

        frame = ttk.LabelFrame(wrapper, padding=6)
        self._add_text_widget(frame, "console_labelframe")
        frame.pack(fill="both", expand=True)
        self._init_console(frame)

    def _create_collapsible_section(self, parent, title_key, default_expanded=False):
        """
        Creates a custom collapsible section.
        Bypasses the Tkinter LabelFrame labelwidget bug by using a dedicated header frame.
        """
        # 1. Master container for this entire section
        container = ttk.Frame(parent)
        container.pack(fill="x", pady=(0, 6))

        # 2. Header Frame: Label on the Left, Button on the Right
        header = ttk.Frame(container)
        header.pack(fill="x")

        self._add_text_widget(ttk.Label(header, text=""), title_key).pack(side="left")

        toggle_btn = ttk.Button(header, width=10)
        toggle_btn.pack(side="right")

        # 3. Content Frame: A LabelFrame without text to maintain the bordered box look
        content_frame = ttk.LabelFrame(container, padding=8)

        # 4. Initial state setup
        if default_expanded:
            content_frame.pack(fill="x", pady=(4, 0))
            toggle_btn.config(text=self._tr("collapse_btn"))
        else:
            toggle_btn.config(text=self._tr("expand_btn"))

        # 5. Safe Toggle Logic
        def toggle():
            if content_frame.winfo_manager():  # If visible, hide it
                content_frame.pack_forget()
                toggle_btn.config(text=self._tr("expand_btn"))
            else:                              # If hidden, show it
                content_frame.pack(fill="x", pady=(4, 0))
                toggle_btn.config(text=self._tr("collapse_btn"))
            sync = getattr(self, "_sync_body_geometry", None)
            if sync is not None:
                try:
                    sync()
                except tk.TclError:
                    pass

        toggle_btn.config(command=toggle)

        # Store for language updates
        self._toggle_buttons.append((toggle_btn, content_frame, default_expanded))

        return content_frame

    def _build_env_section(self, parent):
        content_frame = self._create_collapsible_section(
            parent,
            title_key="api_keys_webhook",
            default_expanded=False
        )

        content_frame.columnconfigure(1, weight=1)

        for row, (key, label_key) in enumerate(ENV_FIELD_ROWS):
            self._add_text_widget(ttk.Label(content_frame, text=""), label_key).grid(row=row, column=0, sticky="w", pady=2)

            var = tk.StringVar()
            self.env_vars[key] = var
            var.trace_add("write", self._make_env_trace(key))

            show_btn = ttk.Button(content_frame, text=self._tr("show_btn"), command=lambda k=key: self._toggle_env_show(k))
            show_btn.grid(row=row, column=1, sticky="w", padx=6)

            value_frame = ttk.Frame(content_frame)
            entry = ttk.Entry(value_frame, textvariable=var, width=46)
            entry.pack(side="left", padx=(0, 6))
            hide_btn = ttk.Button(value_frame, text=self._tr("hide_btn"), command=lambda k=key: self._toggle_env_show(k))
            hide_btn.pack(side="left")
            self.env_hide_buttons[key] = hide_btn
            value_frame.grid(row=row, column=1, sticky="w", padx=6)
            value_frame.grid_remove()

            self.env_show_buttons[key] = show_btn
            self.env_show_frames[key] = value_frame
            self.show_state[key] = False

    def _build_directories_section(self, parent):
        frame = self._create_collapsible_section(
            parent,
            title_key="directories",
            default_expanded=False
        )
        self._directories_frame = frame

        self.dir_vars = {}
        for row, (key, label_key) in enumerate(DIRECTORY_ROWS):
            self._add_text_widget(ttk.Label(frame, text=""), label_key).grid(row=row, column=0, sticky="w", pady=2)
            var = tk.StringVar(value=self.config_data.get(key, ""))
            self.dir_vars[key] = var
            var.trace_add("write", self._make_dir_trace(key))
            ttk.Entry(frame, textvariable=var, width=40).grid(row=row, column=1, sticky="ew", padx=6)
            self._add_text_widget(ttk.Button(frame, command=lambda k=key: self._open_directory(k)),
                                  "open_btn").grid(row=row, column=2, padx=3)
            self._add_text_widget(ttk.Button(frame, command=lambda k=key: self._browse_directory(k)),
                                  "browse_btn").grid(row=row, column=3, padx=3)

    def _add_help_button(self, frame, row, key, column=0):
        """Small "?" button placed to the left of an advanced setting, opening a short
        explanation popup for it (see _show_setting_help / advanced_setting_explanations_English.json)."""
        btn = ttk.Button(frame, text="?", width=2,
                         command=lambda: self._show_setting_help(key))
        btn.grid(row=row, column=column, sticky="w", padx=(0, 3), pady=2)

    def _show_setting_help(self, key):
        explanation = self.setting_explanations.get(key, self._tr("no_explanation"))
        top = ThemedToplevel(self)
        top.title(self._tr("setting_info_title"))
        top.resizable(False, False)
        top.transient(self)

        frame = ttk.Frame(top, padding=15)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text=explanation, wraplength=320, justify="left").pack()
        self._add_text_widget(ttk.Button(frame, command=top.destroy),
                              "close_btn").pack(pady=(12, 0))
        top.grab_set()

    def _show_selection_help_menu(self):
        """The single "?" button next to the Select Songs.../Select PKLZ Folders... buttons
        opens this small chooser instead of each button carrying its own separate "?" (which
        used to leave one button stranded far to the right of an empty stretchy column). Picking
        either option opens the normal _show_setting_help(key) popup on top of this one; Close
        just dismisses the chooser."""
        top = ThemedToplevel(self)
        top.title(self._tr("selection_help_title"))
        top.resizable(False, False)
        top.transient(self)

        frame = ttk.Frame(top, padding=15)
        frame.pack(fill="both", expand=True)
        self._add_text_widget(
            ttk.Button(frame, command=lambda: self._show_setting_help("song_selection_help")),
            "select_songs_btn"
        ).pack(fill="x", pady=2)
        self._add_text_widget(
            ttk.Button(frame, command=lambda: self._show_setting_help("pklz_folder_selection_help")),
            "select_pklz_folders_btn"
        ).pack(fill="x", pady=2)
        self._add_text_widget(ttk.Button(frame, command=top.destroy),
                              "close_btn").pack(fill="x", pady=(12, 0))
        top.grab_set()

    def _build_modes_section(self, parent):
        frame = ttk.LabelFrame(parent, padding=8)
        self._add_text_widget(frame, "search_modes")
        frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8))
        self._search_modes_frame = frame

        self.var_mode_mb = tk.BooleanVar(value=self.config_data["mode_musicbrainz"])
        self.var_mode_audiotag = tk.BooleanVar(value=self.config_data["mode_audiotag"])
        self.var_mode_shazam = tk.BooleanVar(value=self.config_data["mode_shazam"])
        self.var_mode_audfprint = tk.BooleanVar(value=self.config_data["mode_audfprint"])

        self._add_text_widget(ttk.Checkbutton(frame, variable=self.var_mode_mb,
                                              command=self._flush_immediately),
                              "musicbrainz_check").pack(anchor="w", pady=2)
        self._add_text_widget(ttk.Checkbutton(frame, variable=self.var_mode_audiotag,
                                              command=self._flush_immediately),
                              "audiotag_check").pack(anchor="w", pady=2)
        self._add_text_widget(ttk.Checkbutton(frame, variable=self.var_mode_shazam,
                                              command=self._flush_immediately),
                              "shazam_check").pack(anchor="w", pady=2)
        self._add_text_widget(ttk.Checkbutton(frame, variable=self.var_mode_audfprint,
                                              command=self._flush_immediately),
                              "audfprint_check").pack(anchor="w", pady=2)

    def _build_advanced_section(self, parent):
        outer = ttk.LabelFrame(parent, padding=4)
        self._add_text_widget(outer, "advanced_settings")
        outer.grid(row=0, column=1, sticky="nsew")

        notebook = ttk.Notebook(outer)
        notebook.pack(fill="both", expand=True)
        self._advanced_notebook = notebook

        self._build_general_tab(notebook)
        self._build_tempo_tab(notebook)
        self._build_audfprint_tab(notebook)
        self._build_musicbrainz_tab(notebook)
        self._build_audiotag_tab(notebook)
        self._build_discord_tab(notebook)
        self._build_hash_tables_tab(notebook)
        self._build_logs_tab(notebook)
        self._build_env_tab(notebook)

        # Tab requested-heights are only known once Tk has laid the UI out at
        # least once, so autosize setup is deferred to after the first idle cycle.
        self._advanced_tab_content_heights = []
        self._advanced_min_content_height = 0
        self.after(100, self._setup_advanced_autosize)

    def _setup_advanced_autosize(self):
        """Measures each Advanced Settings tab's natural content height, records
        the smallest one as the notebook's floor height, then installs the
        tab-change handler that resizes the notebook to match whichever tab is
        currently selected. The floor is additionally raised to at least the
        Search Modes frame's own height, so a short tab never makes the whole
        row collapse below what the frame beside it needs."""
        notebook = getattr(self, "_advanced_notebook", None)
        if notebook is None:
            return
        try:
            self.update_idletasks()
        except tk.TclError:
            return

        tab_ids = notebook.tabs()
        if not tab_ids:
            return

        heights = []
        for tab_id in tab_ids:
            frame = notebook.nametowidget(tab_id)
            try:
                frame.update_idletasks()
                heights.append(frame.winfo_reqheight())
            except tk.TclError:
                heights.append(0)

        if not any(heights):
            return

        modes_height = 0
        modes_frame = getattr(self, "_search_modes_frame", None)
        if modes_frame is not None:
            try:
                modes_frame.update_idletasks()
                modes_height = modes_frame.winfo_reqheight()
            except tk.TclError:
                modes_height = 0

        self._advanced_tab_content_heights = heights
        self._advanced_min_content_height = max(
            min(h for h in heights if h > 0),
            modes_height,
        )

        notebook.bind("<<NotebookTabChanged>>", self._on_advanced_tab_changed, add="+")
        self._on_advanced_tab_changed()

    def _on_advanced_tab_changed(self, event=None):
        """Grows or shrinks the Advanced Settings notebook so its pane area fits
        the currently selected tab's content, floored at the smallest tab's
        height (or the Search Modes frame's height, whichever is larger) so a
        short tab never collapses below a comfortable minimum.

        Re-measures the current tab live on every switch (rather than trusting
        the value captured at setup time) so language/theme changes that alter a
        tab's natural height are picked up the next time the user visits it."""
        notebook = getattr(self, "_advanced_notebook", None)
        heights = getattr(self, "_advanced_tab_content_heights", None)
        if notebook is None or not heights:
            return
        try:
            tab_id = notebook.select()
            current_index = notebook.index(tab_id)
            frame = notebook.nametowidget(tab_id)
        except (tk.TclError, KeyError):
            return
        if not (0 <= current_index < len(heights)):
            return

        try:
            frame.update_idletasks()
            target = frame.winfo_reqheight()
        except tk.TclError:
            target = heights[current_index]

        target = max(target, self._advanced_min_content_height)
        try:
            notebook.configure(height=target)
        except tk.TclError:
            pass

        # The notebook's height change alters the body's natural height, but the
        # canvas's scrollregion is only recomputed by _sync_body_geometry. Without
        # this call the modes/advanced row can grow past the visible area and the
        # scrollbar won't offer any way to reach it.
        sync = getattr(self, "_sync_body_geometry", None)
        if sync is not None:
            try:
                self.update_idletasks()
                sync()
            except tk.TclError:
                pass

    def _build_general_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=8)
        notebook.add(frame, text=self._tr("general_tab"))
        self._notebook_tabs.append((notebook, frame, "general_tab"))
        frame.columnconfigure(2, weight=1)

        # Song Selection / PKLZ Folder Selection: replace the old "Mark all audio files as
        # processed in" buttons (which overwrote PROCESSED.txt wholesale) with two dialogs, one
        # per-song, one per-PKLZ-subfolder. Both buttons sit side by side in their own row,
        # above Scan Mode, with a single combined "?" button to their left: the popup it opens
        # lets the user pick which of the two explanations to read (see
        # _show_selection_help_menu), rather than duplicating a separate "?" button per
        # selection button, which used to leave one of the two buttons stranded far to the
        # right of an empty stretchy column.
        help_btn = ttk.Button(frame, text="?", width=2, command=self._show_selection_help_menu)
        help_btn.grid(row=0, column=0, sticky="w", padx=(0, 3), pady=2)

        selection_frame = ttk.Frame(frame)
        selection_frame.grid(row=0, column=1, columnspan=2, sticky="w", padx=4)
        self._add_text_widget(ttk.Button(selection_frame, command=self._open_song_selection_menu),
                              "select_songs_btn").pack(side="left", padx=(0, 6))
        self._add_text_widget(ttk.Button(selection_frame, command=self._open_pklz_selection_menu),
                              "select_pklz_folders_btn").pack(side="left")
        # What is currently selected, right where the selecting happens: without it the only
        # way to know was to reopen the dialog and wait for the database to be walked.
        # Filled from the summary saved alongside the selection, so it costs no disk access.
        self.selection_summary_label = ttk.Label(selection_frame, foreground="#888888")
        self.selection_summary_label.pack(side="left", padx=(8, 0))
        _Tooltip(self.selection_summary_label, self._selection_summary_tooltip)
        self._refresh_selection_summary_label()

        # Scan Mode: the reworked replacement for the old boolean generate_different_tempos
        # checkbox, now a three-way choice deciding which search modes actually run this
        # session. See the "scan_mode" explanation key in advanced_setting_explanations_*.json
        # (behind the "?" button here) for the full semantics of each option.
        self._add_help_button(frame, 1, "scan_mode")
        self._add_text_widget(ttk.Label(frame, text=""), "scan_mode_label").grid(row=1, column=1, sticky="w", pady=2)

        self.var_scan_mode = tk.StringVar(value=self.config_data.get("scan_mode", "quick"))
        self.var_scan_mode.trace_add("write", self._make_simple_trace())

        scan_mode_frame = ttk.Frame(frame)
        scan_mode_frame.grid(row=1, column=2, sticky="w", padx=4)
        self._add_text_widget(ttk.Radiobutton(scan_mode_frame, variable=self.var_scan_mode, value="quick"),
                              "scan_mode_quick").pack(side="left", padx=2)
        self._add_text_widget(ttk.Radiobutton(scan_mode_frame, variable=self.var_scan_mode, value="long"),
                              "scan_mode_long").pack(side="left", padx=2)
        self._add_text_widget(ttk.Radiobutton(scan_mode_frame, variable=self.var_scan_mode, value="both"),
                              "scan_mode_both").pack(side="left", padx=2)

        self._add_help_button(frame, 2, "theme_mode")
        self._add_text_widget(ttk.Label(frame, text=""), "theme_label").grid(row=2, column=1, sticky="w", pady=2)

        self.var_theme_mode = tk.StringVar(value=self.config_data.get("theme_mode", "System"))
        self.var_theme_mode.trace_add("write", self._make_theme_trace())

        theme_frame = ttk.Frame(frame)
        theme_frame.grid(row=2, column=2, sticky="w", padx=4)
        self._add_text_widget(ttk.Radiobutton(theme_frame, variable=self.var_theme_mode, value="Light"),
                              "light_theme").pack(side="left", padx=2)
        self._add_text_widget(ttk.Radiobutton(theme_frame, variable=self.var_theme_mode, value="Dark"),
                              "dark_theme").pack(side="left", padx=2)
        self._add_text_widget(ttk.Radiobutton(theme_frame, variable=self.var_theme_mode, value="System"),
                              "system_theme").pack(side="left", padx=2)

        # Language selection
        self._add_help_button(frame, 3, "language")
        self._add_text_widget(ttk.Label(frame, text=""), "language_label").grid(row=3, column=1, sticky="w", pady=2)

        lang_frame = ttk.Frame(frame)
        lang_frame.grid(row=3, column=2, sticky="w", padx=4)
        self._add_text_widget(ttk.Radiobutton(lang_frame, variable=self.var_language, value="English"),
                              "english_lang").pack(side="left", padx=2)
        self._add_text_widget(ttk.Radiobutton(lang_frame, variable=self.var_language, value="Italiano"),
                              "italiano_lang").pack(side="left", padx=2)
        self._add_text_widget(ttk.Radiobutton(lang_frame, variable=self.var_language, value="Français"),
                              "français_lang").pack(side="left", padx=2)
        self._add_text_widget(ttk.Radiobutton(lang_frame, variable=self.var_language, value="Português"),
                              "português_lang").pack(side="left", padx=2)

    def _change_language(self, lang):
        if lang not in ("English", "Italiano", "Français", "Português"):
            return
        if lang == self.language:
            return
        self.language = lang
        self.config_data["language"] = lang
        self.setting_explanations = load_setting_explanations(lang)
        self.gui_strings = load_gui_strings(lang)
        self._set_all_texts()
        self._save_config_to_disk()

    def _build_audfprint_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=8)
        notebook.add(frame, text=self._tr("audfprint_tab"))
        self._notebook_tabs.append((notebook, frame, "audfprint_tab"))
        frame.columnconfigure(2, weight=1)

        # Picking specific PKLZ subfolders now happens through the "Select PKLZ Folders..."
        # button on the General tab (see _open_pklz_selection_menu), not here: that dialog can
        # select several subfolders at once (this tab's old checkbox only ever supported one),
        # and its own "?" help button explains the multi-target regeneration trade-off.
        self._add_help_button(frame, 0, "thread_count")
        self.var_use_threads = tk.BooleanVar(value=self.config_data["use_custom_thread_count"])
        self._add_text_widget(ttk.Checkbutton(frame, variable=self.var_use_threads,
                                               command=self._flush_immediately),
                              "thread_count_check").grid(row=0, column=1, sticky="w", pady=2)
        self.var_thread_count = tk.StringVar(value=self.config_data["custom_thread_count_value"])
        self.var_thread_count.trace_add("write", self._make_simple_trace())
        ttk.Entry(frame, textvariable=self.var_thread_count, width=6).grid(row=0, column=2, sticky="w", padx=4)

        self._add_help_button(frame, 1, "search_depth")
        self.var_use_search_depth = tk.BooleanVar(value=self.config_data["use_custom_search_depth"])
        self._add_text_widget(ttk.Checkbutton(frame, variable=self.var_use_search_depth,
                                               command=self._flush_immediately),
                              "search_depth_check").grid(row=1, column=1, sticky="w", pady=2)
        self.var_search_depth = tk.StringVar(value=str(self.config_data["custom_search_depth_value"]))
        self.var_search_depth.trace_add("write", self._make_simple_trace())
        ttk.Entry(frame, textvariable=self.var_search_depth, width=6).grid(row=1, column=2, sticky="w", padx=4)

    def _build_musicbrainz_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=8)
        notebook.add(frame, text=self._tr("musicbrainz_tab"))
        self._notebook_tabs.append((notebook, frame, "musicbrainz_tab"))
        frame.columnconfigure(2, weight=1)

        self._add_help_button(frame, 0, "musicbrainz_duration_range")
        self.var_use_mb_duration = tk.BooleanVar(value=self.config_data["custom_musicbrainz_duration_range"])
        self._add_text_widget(ttk.Checkbutton(frame, variable=self.var_use_mb_duration,
                                               command=self._flush_immediately),
                              "duration_range_check").grid(row=0, column=1, sticky="w", pady=2)

        duration_frame = ttk.Frame(frame)
        duration_frame.grid(row=0, column=2, sticky="w", padx=4)
        self.var_mb_duration_min = tk.StringVar(value=str(self.config_data["custom_musicbrainz_duration_range_minvalue"]))
        self.var_mb_duration_min.trace_add("write", self._make_simple_trace())
        self.var_mb_duration_max = tk.StringVar(value=str(self.config_data["custom_musicbrainz_duration_range_maxvalue"]))
        self.var_mb_duration_max.trace_add("write", self._make_simple_trace())

        ttk.Label(duration_frame, text='"').pack(side="left")
        ttk.Entry(duration_frame, textvariable=self.var_mb_duration_min, width=6).pack(side="left", padx=2)
        ttk.Label(duration_frame, text=":").pack(side="left")
        ttk.Entry(duration_frame, textvariable=self.var_mb_duration_max, width=6).pack(side="left", padx=2)
        ttk.Label(duration_frame, text='"').pack(side="left")

        self._add_help_button(frame, 1, "musicbrainz_extension")
        self.var_use_mb_extension = tk.BooleanVar(value=self.config_data["custom_musicbrainz_extension"])
        self._add_text_widget(ttk.Checkbutton(frame, variable=self.var_use_mb_extension,
                                               command=self._flush_immediately),
                              "extension_check").grid(row=1, column=1, sticky="w", pady=2)
        self.var_mb_extension = tk.StringVar(value=str(self.config_data["custom_musicbrainz_extension_value"]))
        self.var_mb_extension.trace_add("write", self._make_simple_trace())
        ttk.Entry(frame, textvariable=self.var_mb_extension, width=6).grid(row=1, column=2, sticky="w", padx=4)

    def _build_audiotag_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=8)
        notebook.add(frame, text=self._tr("audiotag_tab"))
        self._notebook_tabs.append((notebook, frame, "audiotag_tab"))
        frame.columnconfigure(2, weight=1)

        self._add_help_button(frame, 0, "audiotag_cooldown")
        self._add_text_widget(ttk.Label(frame, text=""), "cooldown_label").grid(row=0, column=1, sticky="w", pady=2)
        cooldown_frame = ttk.Frame(frame)
        cooldown_frame.grid(row=0, column=2, sticky="w", padx=4)
        self.var_audiotag_cooldown_min = tk.StringVar(value=str(self.config_data["custom_audiotag_cooldown_min_value"]))
        self.var_audiotag_cooldown_min.trace_add("write", self._make_simple_trace())
        self.var_audiotag_cooldown_max = tk.StringVar(value=str(self.config_data["custom_audiotag_cooldown_max_value"]))
        self.var_audiotag_cooldown_max.trace_add("write", self._make_simple_trace())
        ttk.Entry(cooldown_frame, textvariable=self.var_audiotag_cooldown_min, width=6).pack(side="left", padx=2)
        ttk.Label(cooldown_frame, text=":").pack(side="left")
        ttk.Entry(cooldown_frame, textvariable=self.var_audiotag_cooldown_max, width=6).pack(side="left", padx=2)

        self._add_help_button(frame, 1, "audiotag_rotate_after")
        self._add_text_widget(ttk.Label(frame, text=""), "rotate_after_tracks_label").grid(row=1, column=1, sticky="w", pady=2)
        self.var_audiotag_rotate_after = tk.StringVar(value=str(self.config_data["custom_audiotag_rotate_after_tracks_value"]))
        self.var_audiotag_rotate_after.trace_add("write", self._make_simple_trace())
        ttk.Entry(frame, textvariable=self.var_audiotag_rotate_after, width=6).grid(row=1, column=2, sticky="w", padx=4)

        self._add_help_button(frame, 2, "audiotag_pause_seconds")
        self._add_text_widget(ttk.Label(frame, text=""), "pause_seconds_label").grid(row=2, column=1, sticky="w", pady=2)
        self.var_audiotag_pause_seconds = tk.StringVar(value=str(self.config_data["custom_audiotag_pause_seconds_value"]))
        self.var_audiotag_pause_seconds.trace_add("write", self._make_simple_trace())
        ttk.Entry(frame, textvariable=self.var_audiotag_pause_seconds, width=6).grid(row=2, column=2, sticky="w", padx=4)

        self._add_help_button(frame, 3, "audiotag_min_duration")
        self._add_text_widget(ttk.Label(frame, text=""), "min_duration_label").grid(row=3, column=1, sticky="w", pady=2)
        self.var_audiotag_min_duration = tk.StringVar(value=str(self.config_data["custom_audiotag_min_duration_value"]))
        self.var_audiotag_min_duration.trace_add("write", self._make_simple_trace())
        ttk.Entry(frame, textvariable=self.var_audiotag_min_duration, width=6).grid(row=3, column=2, sticky="w", padx=4)

        self.var_audiotag_multi_key = tk.BooleanVar(value=self.config_data["audiotag_use_multiple_keys"])
        self._add_text_widget(
            ttk.Button(frame, command=self._open_audiotag_multi_key_dialog),
            "use_multiple_audiotag_keys_check"
        ).grid(row=4, column=0, columnspan=2, sticky="w", pady=(8, 2), padx=4)

    def _ask_audiotag_key(self, initial_value="", edit_mode=False):
        """Custom prompt dialog for adding or editing an AudioTag API key. Replaces
        simpledialog.askstring so that (a) its Entry gets exactly the same
        Ctrl+A/C/V/X/Y/Z shortcuts and right-click context menu as every other
        Entry in the app, and (b) its buttons use the app's own translated
        labels instead of simpledialog's hardcoded English "OK"/"Cancel".

        Returns the entered string (stripped) when confirmed, or None when
        cancelled / closed / left blank."""
        result = {"value": None}
        top = ThemedToplevel(self)
        top.title(self._tr("edit_key_prompt_title" if edit_mode else "add_key_prompt_title"))
        top.resizable(False, False)
        top.transient(self)

        frame = ttk.Frame(top, padding=15)
        frame.pack(fill="both", expand=True)

        self._add_text_widget(
            ttk.Label(frame, text=""),
            "edit_key_prompt_msg" if edit_mode else "add_key_prompt_msg"
        ).pack(anchor="w", pady=(0, 6))

        var = tk.StringVar(value=initial_value)
        entry = ttk.Entry(frame, textvariable=var, width=50)
        entry.pack(fill="x")
        # The class-level fallback in _enable_entry_shortcuts only fires for
        # widgets that already existed when it ran; this dialog's Entry is
        # created on demand, so bind it explicitly here using the same
        # helper that method stored on self.
        bind_shortcuts = getattr(self, "_bind_entry_widget_shortcuts", None)
        if bind_shortcuts is not None:
            bind_shortcuts(entry)

        def confirm(*_args):
            result["value"] = var.get().strip()
            top.destroy()

        def cancel(*_args):
            result["value"] = None
            top.destroy()

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(12, 0))
        # "OK" is intentionally hardcoded: it's the same in all four languages
        # the app supports and reads as a button, not as a translated word.
        ttk.Button(btn_frame, text="OK", command=confirm).pack(side="right", padx=2)
        self._add_text_widget(ttk.Button(btn_frame, command=cancel),
                              "cancel_btn").pack(side="right", padx=2)

        top.bind("<Return>", confirm)
        top.bind("<Escape>", cancel)
        top.protocol("WM_DELETE_WINDOW", cancel)

        entry.focus_set()
        entry.select_range(0, "end")
        entry.icursor("end")

        top.grab_set()
        self.wait_window(top)
        return result["value"]

    def _open_audiotag_multi_key_dialog(self):
        """Small modal window holding everything that used to be the second half of
        the AudioTag tab: the [?] explanation, the "use multiple keys" toggle, and
        the key list editor. Keeping it out of the notebook tab is what allows the
        AudioTag tab to be roughly the same height as every other settings tab."""
        top = ThemedToplevel(self)
        top.title(self._tr("audiotag_tab"))
        top.transient(self)
        top.geometry("560x460")
        top.minsize(460, 400)

        frame = ttk.Frame(top, padding=10)
        frame.pack(fill="both", expand=True)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(3, weight=1)

        check_row = ttk.Frame(frame)
        check_row.grid(row=0, column=0, columnspan=2, sticky="w", pady=2)
        self._add_help_button(check_row, 0, "audiotag_multi_key")
        self._add_text_widget(
            ttk.Checkbutton(check_row, variable=self.var_audiotag_multi_key,
                            command=self._on_toggle_audiotag_multi_key),
            "use_multiple_audiotag_keys_check"
        ).grid(row=0, column=1, sticky="w")

        ttk.Separator(frame, orient="horizontal").grid(row=1, column=0, columnspan=2, sticky="ew", pady=(10, 6))

        self._add_text_widget(ttk.Label(frame, text=""), "audiotag_keys_list_label").grid(
            row=2, column=0, sticky="w")
        self._add_text_widget(
            ttk.Checkbutton(frame, variable=self._audiotag_show_keys,
                            command=self._refresh_audiotag_keys_listbox),
            "show_keys_check"
        ).grid(row=2, column=1, sticky="e")

        list_container = ttk.Frame(frame)
        list_container.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(2, 4))
        list_container.columnconfigure(0, weight=1)
        list_container.rowconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(list_container, orient="vertical")
        self.audiotag_keys_listbox = tk.Listbox(list_container, height=8,
                                                 yscrollcommand=scrollbar.set,
                                                 exportselection=False)
        scrollbar.config(command=self.audiotag_keys_listbox.yview)
        self.audiotag_keys_listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=4, column=0, columnspan=2, sticky="w", pady=(2, 0))
        self._add_text_widget(ttk.Button(btn_frame, command=self._add_audiotag_key),
                              "add_key_btn").pack(side="left", padx=(0, 4))
        self._add_text_widget(ttk.Button(btn_frame, command=self._edit_selected_audiotag_key),
                              "edit_key_btn").pack(side="left", padx=(0, 4))
        self._add_text_widget(ttk.Button(btn_frame, command=self._remove_selected_audiotag_key),
                              "remove_key_btn").pack(side="left")

        back_frame = ttk.Frame(frame)
        back_frame.grid(row=5, column=0, columnspan=2, sticky="e", pady=(12, 0))
        self._add_text_widget(ttk.Button(back_frame, command=top.destroy),
                              "close_btn").pack(side="right")

        self._refresh_audiotag_keys_listbox()

        # The listbox only exists while this dialog is open. Clear the reference
        # the moment the window is destroyed so the rest of the AudioTag helpers
        # (_refresh_audiotag_keys_listbox, _remove_selected_audiotag_key) don't
        # try to talk to a destroyed widget afterwards.
        def _on_destroy(event):
            if event.widget is top:
                self.audiotag_keys_listbox = None
        top.bind("<Destroy>", _on_destroy, add="+")

        top.grab_set()

    def _on_toggle_audiotag_multi_key(self):
        if self.var_audiotag_multi_key.get():
            messagebox.showwarning(self._tr("multi_key_warning_title"), self._tr("multi_key_warning_msg"))
        self._flush_immediately()

    def _refresh_audiotag_keys_listbox(self):
        listbox = getattr(self, "audiotag_keys_listbox", None)
        if listbox is None:
            return
        try:
            if not listbox.winfo_exists():
                return
        except tk.TclError:
            return
        show_full = self._audiotag_show_keys.get()
        listbox.delete(0, "end")
        for entry in self.audiotag_keys_data.get("keys", []):
            key = entry.get("key", "")
            if show_full:
                display_key = key
            else:
                display_key = f"****{key[-4:]}" if len(key) >= 4 else "****"
            status = entry.get("status", "ok")
            tracks_used = entry.get("tracksUsed", 0)
            status_label = self._tr(f"audiotag_status_{status}")
            listbox.insert("end", f"{display_key}: {tracks_used} {self._tr('tracks_used_suffix')}, {status_label}")

    def _add_audiotag_key(self):
        new_key = self._ask_audiotag_key()
        if not new_key:
            return
        keys = self.audiotag_keys_data.setdefault("keys", [])
        if any(entry.get("key") == new_key for entry in keys):
            return
        keys.append({"key": new_key, "tracksUsed": 0, "status": "ok",
                     "lastError": None, "lastUsedAt": None})
        save_audiotag_keys(self.audiotag_keys_data)
        self._refresh_audiotag_keys_listbox()

    def _edit_selected_audiotag_key(self):
        listbox = getattr(self, "audiotag_keys_listbox", None)
        if listbox is None:
            return
        try:
            if not listbox.winfo_exists():
                return
        except tk.TclError:
            return
        selection = listbox.curselection()
        if not selection:
            return
        keys = self.audiotag_keys_data.get("keys", [])
        index = selection[0]
        if not (0 <= index < len(keys)):
            return
        entry_data = keys[index]
        old_key = entry_data.get("key", "")
        new_key = self._ask_audiotag_key(initial_value=old_key, edit_mode=True)
        if new_key is None or not new_key or new_key == old_key:
            return
        if any(other is not entry_data and other.get("key") == new_key for other in keys):
            return
        entry_data["key"] = new_key
        entry_data["tracksUsed"] = 0
        entry_data["status"] = "ok"
        entry_data["lastError"] = None
        entry_data["lastUsedAt"] = None
        save_audiotag_keys(self.audiotag_keys_data)
        self._refresh_audiotag_keys_listbox()
        listbox.selection_set(index)

    def _remove_selected_audiotag_key(self):
        listbox = getattr(self, "audiotag_keys_listbox", None)
        if listbox is None:
            return
        try:
            if not listbox.winfo_exists():
                return
        except tk.TclError:
            return
        selection = listbox.curselection()
        if not selection:
            return
        keys = self.audiotag_keys_data.get("keys", [])
        index = selection[0]
        if 0 <= index < len(keys):
            del keys[index]
            if self.audiotag_keys_data.get("activeIndex", 0) >= len(keys):
                self.audiotag_keys_data["activeIndex"] = 0
            save_audiotag_keys(self.audiotag_keys_data)
            self._refresh_audiotag_keys_listbox()

    def _build_discord_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=8)
        notebook.add(frame, text=self._tr("discord_tab"))
        self._notebook_tabs.append((notebook, frame, "discord_tab"))
        frame.columnconfigure(2, weight=1)

        self._add_help_button(frame, 0, "custom_webhook_name")
        self.var_use_custom_name = tk.BooleanVar(value=self.config_data["use_custom_webhook_name"])
        self._add_text_widget(ttk.Checkbutton(frame, variable=self.var_use_custom_name,
                                               command=self._flush_immediately),
                              "custom_name_check").grid(row=0, column=1, sticky="w", pady=2)
        self.var_custom_name = tk.StringVar(value=self.config_data["custom_webhook_name_value"])
        self.var_custom_name.trace_add("write", self._make_simple_trace())
        ttk.Entry(frame, textvariable=self.var_custom_name).grid(row=0, column=2, sticky="ew", padx=4)

        self._add_help_button(frame, 1, "custom_webhook_image")
        self.var_use_custom_image = tk.BooleanVar(value=self.config_data["use_custom_webhook_image"])
        self._add_text_widget(ttk.Checkbutton(frame, variable=self.var_use_custom_image,
                                               command=self._flush_immediately),
                              "custom_image_check").grid(row=1, column=1, sticky="w", pady=2)
        self.var_custom_image = tk.StringVar(value=self.config_data["custom_webhook_image_link"])
        self.var_custom_image.trace_add("write", self._make_simple_trace())
        ttk.Entry(frame, textvariable=self.var_custom_image).grid(row=1, column=2, sticky="ew", padx=4)

    def _build_env_tab(self, notebook):
        """Tab that lets the user choose the command format for Python, FFmpeg and Node."""
        frame = ttk.Frame(notebook, padding=8)
        notebook.add(frame, text=self._tr("env_tab"))
        self._notebook_tabs.append((notebook, frame, "env_tab"))
        frame.columnconfigure(2, weight=1)

        def get_full_path(cmd_name):
            path = shutil.which(cmd_name)
            if not path:
                path = cmd_name
            return f'"{path}"'

        rows = [
            (
                "PYTHON_COMMAND",
                "python_command_label",
                "python",
                sys.executable,
                "use_python_btn",
                "use_python_fullpath_btn",
                "python_command"
            ),
            (
                "FFMPEG_COMMAND",
                "ffmpeg_command_label",
                "ffmpeg",
                get_full_path("ffmpeg"),
                "use_ffmpeg_btn",
                "use_ffmpeg_fullpath_btn",
                "ffmpeg_command"
            ),
            (
                "NODE_COMMAND",
                "node_command_label",
                "node",
                get_full_path("node"),
                "use_node_btn",
                "use_node_fullpath_btn",
                "node_command"
            ),
        ]

        for row_idx, (env_key, label_key, simple, full, simple_btn_key, full_btn_key, help_key) in enumerate(rows):
            self._add_help_button(frame, row_idx, help_key, column=0)

            self._add_text_widget(ttk.Label(frame, text=""), label_key).grid(
                row=row_idx, column=1, sticky="w", pady=2, padx=(3, 6)
            )

            btn_frame = ttk.Frame(frame)
            btn_frame.grid(row=row_idx, column=2, sticky="w", padx=4)

            # Uses _add_text_widget for both buttons so they get registered and translated
            btn_simple = self._add_text_widget(ttk.Button(btn_frame), simple_btn_key)
            btn_simple.config(command=lambda k=env_key, v=simple: self._set_env_command(k, v))
            btn_simple.pack(side="left", padx=2)

            btn_full = self._add_text_widget(ttk.Button(btn_frame), full_btn_key)
            btn_full.config(command=lambda k=env_key, v=full: self._set_env_command(k, v))
            btn_full.pack(side="left", padx=2)

    def _build_hash_tables_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=8)
        notebook.add(frame, text=self._tr("hash_tables_tab"))
        self._notebook_tabs.append((notebook, frame, "hash_tables_tab"))
        frame.columnconfigure(2, weight=1)

        self._add_help_button(frame, 0, "hash_tables_dir")
        self._add_text_widget(ttk.Label(frame, text=""), "hash_tables_dir_label").grid(
            row=0, column=1, sticky="w", pady=2, padx=(3, 6))

        var = tk.StringVar(value=self.config_data.get("hash_tables_dir", DEFAULT_HASH_TABLES_DIR))
        self.dir_vars["hash_tables_dir"] = var
        var.trace_add("write", self._make_dir_trace("hash_tables_dir"))
        ttk.Entry(frame, textvariable=var, width=40).grid(row=0, column=2, sticky="ew", padx=6)
        self._add_text_widget(ttk.Button(frame, command=lambda: self._open_directory("hash_tables_dir")),
                            "open_btn").grid(row=0, column=3, padx=3)
        self._add_text_widget(ttk.Button(frame, command=lambda: self._browse_directory("hash_tables_dir")),
                            "browse_btn").grid(row=0, column=4, padx=3)

        self._add_help_button(frame, 1, "create_hash_tables_explanation")
        self.var_create_pklz_ht = tk.BooleanVar(
            value=self.config_data.get("create_pklz_hash_tables_on_load_val", False))
        self._add_text_widget(
            ttk.Checkbutton(frame, variable=self.var_create_pklz_ht,
                            command=self._flush_immediately),
            "create_pklz_hash_tables_on_load"
        ).grid(row=1, column=1, columnspan=3, sticky="w", pady=2, padx=(3, 0))

    def _build_logs_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=8)
        notebook.add(frame, text=self._tr("logs_tab"))
        self._notebook_tabs.append((notebook, frame, "logs_tab"))
        frame.columnconfigure(2, weight=1)

        self._add_help_button(frame, 0, "console_logs_dir")
        self._add_text_widget(ttk.Label(frame, text=""), "console_logs_dir_label").grid(
            row=0, column=1, sticky="w", pady=2, padx=(3, 6))

        console_logs_default = self.config_data.get("console_logs_dir", DEFAULT_CONSOLE_LOGS_DIR)
        # Display-only drive-letter normalization: Windows is case-insensitive for paths, so
        # "c:\..." and "C:\..." point at the exact same folder, but every other default
        # directory here happens to render as "C:\...". Uppercases just the drive letter for
        # visual consistency. The change also persists (via the StringVar's own trace) into
        # config.json, which is harmless because the path is identical either way.
        if len(console_logs_default) >= 2 and console_logs_default[1] == ":":
            console_logs_default = console_logs_default[0].upper() + console_logs_default[1:]

        var = tk.StringVar(value=console_logs_default)
        self.dir_vars["console_logs_dir"] = var
        var.trace_add("write", self._make_dir_trace("console_logs_dir"))
        ttk.Entry(frame, textvariable=var, width=40).grid(row=0, column=2, sticky="ew", padx=6)
        self._add_text_widget(ttk.Button(frame, command=lambda: self._open_directory("console_logs_dir")),
                            "open_btn").grid(row=0, column=3, padx=3)
        self._add_text_widget(ttk.Button(frame, command=lambda: self._browse_directory("console_logs_dir")),
                            "browse_btn").grid(row=0, column=4, padx=3)

        self._add_help_button(frame, 1, "print_console_to_log")
        self._add_text_widget(
            ttk.Button(frame, command=self._save_console_log),
            "print_console_to_log_btn"
        ).grid(row=1, column=1, columnspan=3, sticky="w", pady=2, padx=(3, 0))

        self._add_text_widget(
            ttk.Button(frame, command=self._open_crash_logs_file),
            "open_crash_logs_btn"
        ).grid(row=2, column=0, columnspan=4, sticky="w", pady=2)

        self._logs_tab_frame = frame

    def _build_tempo_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=8)
        notebook.add(frame, text=self._tr("long_mode_tab"))
        self._notebook_tabs.append((notebook, frame, "long_mode_tab"))
        frame.columnconfigure(2, weight=1)

        # Whether Long Mode runs at all this session is now decided by the Scan Mode switch on
        # the General tab (see _build_general_tab / self.var_scan_mode), not by a checkbox
        # here: this tab now only controls which variations get generated when it does run.
        self._add_help_button(frame, 0, "negative_tempo_array")
        self._add_text_widget(ttk.Label(frame, text=""), "negative_tempo_label").grid(row=0, column=1, sticky="w", pady=2)
        self.var_negative_tempos = tk.StringVar(value=format_tempo_list(self.config_data["negative_tempo_array"]))
        self.var_negative_tempos.trace_add("write", self._make_simple_trace())
        ttk.Entry(frame, textvariable=self.var_negative_tempos).grid(row=0, column=2, sticky="ew", pady=2)

        self._add_help_button(frame, 1, "positive_tempo_array")
        self._add_text_widget(ttk.Label(frame, text=""), "positive_tempo_label").grid(row=1, column=1, sticky="w", pady=2)
        self.var_positive_tempos = tk.StringVar(value=format_tempo_list(self.config_data["positive_tempo_array"]))
        self.var_positive_tempos.trace_add("write", self._make_simple_trace())
        ttk.Entry(frame, textvariable=self.var_positive_tempos).grid(row=1, column=2, sticky="ew", pady=2)

    def _build_action_bar(self, parent):
        bar = ttk.Frame(parent)
        bar.pack(fill="x")
        # self._add_text_widget(ttk.Label(bar, foreground="#666666"), "settings_auto_save").pack(side="left")
        self._logo_header_img = self._load_logo_photo(5)  # 250 / 5 = 50x50
        ttk.Label(bar, image=self._logo_header_img).pack(side="left", padx=(0, 10))
        self._add_text_widget(ttk.Label(bar, font=("Segoe UI", 18, "bold")),
                            "header_app_name").pack(side="left")
        self._add_text_widget(ttk.Button(bar, command=self._open_credits),
                            "credits_button").pack(side="left", padx=(15, 0))

        right = ttk.Frame(bar)
        right.pack(side="right")
        self.btn_add_pklz = ttk.Button(right, command=lambda: self._add_files_flow("pklz"))
        self._add_text_widget(self.btn_add_pklz, "add_pklz_btn")
        self.btn_add_pklz.pack(side="left", padx=4)
        self.btn_add_audio = ttk.Button(right, command=lambda: self._add_files_flow("audio"))
        self._add_text_widget(self.btn_add_audio, "add_audio_btn")
        self.btn_add_audio.pack(side="left", padx=4)
        self._add_text_widget(ttk.Button(right, command=self._open_processed_folder),
                              "processed_files_btn").pack(side="left", padx=4)
        self.btn_force_stop = tk.Button(right, command=self._on_force_stop_clicked,
                                         fg="#b91c1c", font=("Segoe UI", 9, "bold"), state="disabled")
        self._add_text_widget(self.btn_force_stop, "force_stop_btn")
        self.btn_force_stop.pack(side="left", padx=(12, 0))
        self.btn_start = tk.Button(right, command=self._on_start_clicked,
                                    fg="#1a56db", font=("Segoe UI", 9, "bold"))
        self._add_text_widget(self.btn_start, "start_btn")
        self.btn_start.pack(side="left", padx=(4, 0))

    # ------------------------------------------------------------------
    # Console widget (interactive terminal emulation)
    # ------------------------------------------------------------------

    def _init_console(self, parent):
        self.console_font_size = CONSOLE_FONT_DEFAULT
        self.console = ScrolledText(parent, wrap="word", height=11, bg="#111111", fg="#e6e6e6",
                                     insertbackground="#e6e6e6",
                                     font=(CONSOLE_FONT_FAMILY, self.console_font_size), undo=False)
        self.console.pack(fill="both", expand=True)
        self.console.mark_set("input_start", "end")
        self.console.mark_gravity("input_start", "left")
        # Copy / Select All / right-click context menu
        self.console.bind("<Button-3>", self._console_context_menu)
        # Ctrl+X -> copy (never cut)
        self.console.bind("<Control-x>", self._console_copy_event)
        self.console.bind("<Control-X>", self._console_copy_event)
        # Ctrl+A -> select all
        self.console.bind("<Control-a>", self._console_select_all_event)
        self.console.bind("<Control-A>", self._console_select_all_event)
        # Return, BackSpace, Key
        self.console.bind("<Return>", self._console_return)
        self.console.bind("<BackSpace>", self._console_backspace)
        self.console.bind("<Key>", self._console_key_press)
        # Zoom: Ctrl+Wheel or Ctrl+Plus/Minus resize the console font, without touching
        # plain scrolling (a different event sequence, so it's untouched) or the generic
        # <Key> handling above (these are more specific bindings, so they take precedence).
        self.console.bind("<Control-MouseWheel>", self._console_zoom_wheel)
        self.console.bind("<Control-plus>", self._console_zoom_in)
        self.console.bind("<Control-equal>", self._console_zoom_in)
        self.console.bind("<Control-KP_Add>", self._console_zoom_in)
        self.console.bind("<Control-minus>", self._console_zoom_out)
        self.console.bind("<Control-KP_Subtract>", self._console_zoom_out)
        self.console.bind("<Control-0>", self._console_zoom_reset)
        self.console.bind("<Control-KP_0>", self._console_zoom_reset)
        # Colors mirror assets/utils/messages.js's chalk palette (cyan/greenBright/yellow/
        # redBright/gray), tuned as concrete hex values for this console's fixed dark
        # background (#111111), used both for subprocess output (werzatsong.js's own
        # colored console lines) and, via _console_severity_for_message, the app's own
        # [INFO]/[SUCCESS]/etc. log lines.
        self.console.tag_configure("console_info", foreground="#56b6c2")
        self.console.tag_configure("console_success", foreground="#98c379")
        self.console.tag_configure("console_warning", foreground="#e5c07b")
        self.console.tag_configure("console_error", foreground="#e06c75")
        self.console.tag_configure("console_empty", foreground="#7f848e")
        self.after(40, self._pump_console_queue)

    def _set_console_font_size(self, size):
        new_size = max(CONSOLE_FONT_MIN, min(CONSOLE_FONT_MAX, size))
        if new_size == getattr(self, "console_font_size", CONSOLE_FONT_DEFAULT):
            return

        old_font = tkfont.Font(family=CONSOLE_FONT_FAMILY, size=self.console_font_size)
        new_font = tkfont.Font(family=CONSOLE_FONT_FAMILY, size=new_size)
        old_line_h = max(1, old_font.metrics("linespace"))
        new_line_h = max(1, new_font.metrics("linespace"))
        try:
            old_lines = int(self.console.cget("height"))
        except (tk.TclError, ValueError):
            old_lines = 11
        new_lines = max(2, round(old_lines * old_line_h / new_line_h))

        self.console_font_size = new_size
        self.console.configure(font=(CONSOLE_FONT_FAMILY, new_size), height=new_lines)

    def _console_zoom_wheel(self, event):
        self._set_console_font_size(self.console_font_size + (1 if event.delta > 0 else -1))
        return "break"

    def _console_zoom_in(self, _event=None):
        self._set_console_font_size(self.console_font_size + 1)
        return "break"

    def _console_zoom_out(self, _event=None):
        self._set_console_font_size(self.console_font_size - 1)
        return "break"

    def _console_zoom_reset(self, _event=None):
        self._set_console_font_size(CONSOLE_FONT_DEFAULT)
        return "break"

    def _console_key_press(self, event):
        if event.keysym in NAV_KEYSYMS:
            return None
        running = self.active_process is not None and self.active_process.poll() is None
        if not running:
            return "break"
        try:
            before_start = self.console.compare(tk.INSERT, "<", "input_start")
        except tk.TclError:
            before_start = False
        if before_start:
            self.console.mark_set(tk.INSERT, tk.END)
        return None

    def _console_backspace(self, event):
        running = self.active_process is not None and self.active_process.poll() is None
        if not running:
            return "break"
        try:
            at_or_before = self.console.compare(tk.INSERT, "<=", "input_start")
        except tk.TclError:
            at_or_before = True
        if at_or_before:
            return "break"
        return None

    def _console_return(self, event):
        running = self.active_process is not None and self.active_process.poll() is None
        if not running:
            return "break"
        # Strip stray whitespace/CR that can sneak in from pasted text (e.g. a webhook URL
        # copied with a trailing space or \r): node's readline.trim()s its side too, but an
        # embedded \r in the middle of the line would otherwise still break strict $ -anchored
        # regexes like the webhook/API key validators.
        line = self.console.get("input_start", "end-1c").strip()
        self.console.insert("end", "\n")
        self.console.mark_set("input_start", "end")
        self.console.see("end")
        proc = self.active_process
        try:
            if proc is not None and proc.stdin is not None:
                proc.stdin.write((line + "\n").encode("utf-8", errors="replace"))
                proc.stdin.flush()
        except Exception:
            pass
        return "break"

    def _insert_console_text(self, text):
        """Renders subprocess/log output into the console, translating ANSI SGR color
        codes (from chalk in werzatsong.js, or this app's own _log()) into the matching
        Tk tag configured in _init_console. Any other/unrecognized ANSI escape sequence
        (cursor movement, erase line, etc, e.g. from npm/pip output) is silently dropped
        without applying a tag, same as the console's old plain-text-only behavior for
        anything that isn't specifically a recognized color code. Not expected to handle
        a color sequence split across two separate calls (e.g. across two 4096-byte
        subprocess reads): the old strip_ansi()-based code had the same latent limitation
        for this rare edge case, so this isn't a regression."""
        pos = 0
        current_tag = None
        for match in ANSI_ESCAPE_RE.finditer(text):
            start, end = match.span()
            if start > pos:
                segment = text[pos:start]
                if current_tag:
                    self.console.insert("end", segment, current_tag)
                else:
                    self.console.insert("end", segment)
            params, final = match.group(1), match.group(2)
            if final == "m":
                for code in (params.split(";") if params else [""]):
                    if code in CONSOLE_COLOR_TAGS:
                        current_tag = CONSOLE_COLOR_TAGS[code]
                    elif code in CONSOLE_RESET_CODES:
                        current_tag = None
                    # any other SGR code (bold, other colors, etc.) is ignored: it doesn't
                    # change current_tag, matching the "unrecognized -> dropped" rule above
            pos = end
        if pos < len(text):
            segment = text[pos:]
            if current_tag:
                self.console.insert("end", segment, current_tag)
            else:
                self.console.insert("end", segment)

    def _console_severity_for_message(self, message):
        """Maps one of this app's own log messages (already translated by _tr) to a
        console color tag, by matching its leading "[TAG]" against the *current
        language's own* tag_* values, so this keeps working for any future language
        with no hardcoded English/Italian words here. Returns None if the message has no
        leading tag, or the tag isn't one of the recognized severities."""
        match = LEADING_TAG_RE.match(message)
        if not match:
            return None
        word = match.group(1)
        for key, tag in (
            ("tag_success", "console_success"),
            ("tag_done", "console_success"),
            ("tag_info", "console_info"),
            ("tag_start", "console_info"),
            ("tag_gen", "console_info"),
            ("tag_gen_progress", "console_info"),
            ("tag_warning", "console_warning"),
            ("tag_error", "console_error"),
            ("tag_gen_error", "console_error"),
        ):
            if word == self._tr(key):
                return tag
        return None

    def _pump_console_queue(self):
        try:
            while True:
                text = self.console_queue.get_nowait()
                at_bottom = self._console_is_at_bottom()
                self._insert_console_text(text)
                self.console.mark_set("input_start", "end")
                if at_bottom:
                    self.console.see("end")
        except queue.Empty:
            pass
        self.after(40, self._pump_console_queue)

    def _log(self, message):
        message = message.rstrip("\n")
        severity_tag = self._console_severity_for_message(message)
        if severity_tag:
            message = f"\x1b[{CONSOLE_TAG_TO_SGR[severity_tag]}m{message}\x1b[39m"
        self.console_queue.put(message + "\n")

    def _run_console_command(self, cmd, cwd, extra_env=None):
        """Blocking, only ever call this from a background worker thread."""
        full_env = os.environ.copy()
        # chalk (used by assets/utils/messages.js) auto-disables color when stdout isn't
        # a real terminal, which is always the case here since stdout is piped for the
        # embedded console below. FORCE_COLOR overrides that. setdefault so an explicit
        # user override already present in os.environ always wins.
        full_env.setdefault("FORCE_COLOR", "1")
        if extra_env:
            full_env.update({k: str(v) for k, v in extra_env.items()})
        try:
            process = subprocess.Popen(
                cmd, cwd=cwd, env=full_env,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                creationflags=CREATIONFLAGS
            )
        except Exception as e:
            self._log(self._tr("log_launch_error", error=e))
            return -1

        self.active_process = process
        _track_pid(process.pid)
        try:
            fd = process.stdout.fileno()
            while True:
                try:
                    chunk = os.read(fd, 4096)
                except OSError:
                    break
                if not chunk:
                    break
                self.console_queue.put(chunk.decode("utf-8", errors="replace"))
            process.wait()
        finally:
            _untrack_pid(process.pid)
            self.active_process = None

        self.after(0, self._reload_env_from_disk)
        self.after(0, self._reload_audiotag_keys_from_disk)
        return process.returncode

    # ------------------------------------------------------------------
    # Sync engine: config.json <-> .env <-> webhook.js <-> GUI
    # ------------------------------------------------------------------

    def _set_var_silently(self, var, value):
        self._suppress_trace = True
        try:
            var.set(value)
        finally:
            self._suppress_trace = False

    def _make_simple_trace(self):
        def handler(*_args):
            if self._suppress_trace:
                return
            self._schedule_flush()
        return handler

    def _make_dir_trace(self, _key):
        def handler(*_args):
            if self._suppress_trace:
                return
            self._schedule_flush()
        return handler

    def _make_env_trace(self, key):
        def handler(*_args):
            if self._suppress_trace:
                return
            self._env_dirty_keys.add(key)
            self.env_data[key] = self.env_vars[key].get()
            self._schedule_flush()
        return handler

    def _make_theme_trace(self):
        def handler(*_args):
            if self._suppress_trace:
                return
            self._schedule_flush()
            apply_theme_to_gui(self, self.var_theme_mode.get())
        return handler

    def _schedule_flush(self, *_args):
        if self._flush_after_id is not None:
            try:
                self.after_cancel(self._flush_after_id)
            except Exception:
                pass
        self._flush_after_id = self.after(350, self._flush_now)

    def _flush_immediately(self):
        if self._flush_after_id is not None:
            try:
                self.after_cancel(self._flush_after_id)
            except Exception:
                pass
            self._flush_after_id = None
        self._flush_now()

    def _flush_now(self):
        self._flush_after_id = None
        self._sync_widgets_to_config()
        self._recompute_command()
        self._save_config_to_disk()
        self._sync_webhook_js()
        self._maybe_flush_env()

    @staticmethod
    def _parse_int_field(text, min_v, max_v, fallback):
        """Parses a UI Entry's text as a plain non-negative integer within [min_v, max_v];
        falls back to the given value (typically the currently-stored config value) on
        any non-digit text or out-of-range number, mirroring how custom_thread_count_value
        is already validated."""
        text = (text or "").strip()
        if not text.isdigit():
            return fallback
        value = int(text)
        if value < min_v or value > max_v:
            return fallback
        return value

    def _sync_widgets_to_config(self):
        c = self.config_data
        c["mode_musicbrainz"] = bool(self.var_mode_mb.get())
        c["mode_audiotag"] = bool(self.var_mode_audiotag.get())
        c["mode_shazam"] = bool(self.var_mode_shazam.get())
        c["mode_audfprint"] = bool(self.var_mode_audfprint.get())
        # scan_mode is backed by a long-lived widget (the radio group in the General tab), so
        # it goes through the ordinary debounced flush like every other setting here. This is
        # unlike add_pklz_action/add_audio_action, which are written directly by their modal
        # dialogs' own trace callbacks (see _prompt_files_or_folder): those widgets only exist
        # while their dialog is open, so there is nothing for this method to read.
        c["scan_mode"] = self.var_scan_mode.get()
        c["negative_tempo_array"] = parse_tempo_list(self.var_negative_tempos.get(),
                                                      c.get("negative_tempo_array", NEGATIVE_TEMPO_DEFAULT))
        c["positive_tempo_array"] = parse_tempo_list(self.var_positive_tempos.get(),
                                                      c.get("positive_tempo_array", POSITIVE_TEMPO_DEFAULT))
        c["use_custom_webhook_name"] = bool(self.var_use_custom_name.get())
        c["custom_webhook_name_value"] = self.var_custom_name.get()
        c["use_custom_webhook_image"] = bool(self.var_use_custom_image.get())
        c["custom_webhook_image_link"] = self.var_custom_image.get()
        c["use_custom_thread_count"] = bool(self.var_use_threads.get())
        thread_val = self.var_thread_count.get().strip()
        c["custom_thread_count_value"] = thread_val if thread_val.isdigit() else c.get("custom_thread_count_value", "4")
        c["use_custom_search_depth"] = bool(self.var_use_search_depth.get())
        c["custom_search_depth_value"] = str(self._parse_int_field(
            self.var_search_depth.get(), SEARCH_DEPTH_MIN, SEARCH_DEPTH_MAX,
            int(c.get("custom_search_depth_value", SEARCH_DEPTH_DEFAULT))))
        c["custom_musicbrainz_duration_range"] = bool(self.var_use_mb_duration.get())
        c["custom_musicbrainz_duration_range_minvalue"] = self._parse_int_field(
            self.var_mb_duration_min.get(), MUSICBRAINZ_DURATION_MIN, MUSICBRAINZ_DURATION_MAX,
            MUSICBRAINZ_DURATION_MIN_DEFAULT)
        c["custom_musicbrainz_duration_range_maxvalue"] = self._parse_int_field(
            self.var_mb_duration_max.get(), MUSICBRAINZ_DURATION_MIN, MUSICBRAINZ_DURATION_MAX,
            MUSICBRAINZ_DURATION_MAX_DEFAULT)
        c["custom_musicbrainz_extension"] = bool(self.var_use_mb_extension.get())
        c["custom_musicbrainz_extension_value"] = self._parse_int_field(
            self.var_mb_extension.get(), MUSICBRAINZ_EXTENSION_MIN, MUSICBRAINZ_EXTENSION_MAX,
            MUSICBRAINZ_EXTENSION_DEFAULT)
        c["audiotag_use_multiple_keys"] = bool(self.var_audiotag_multi_key.get())
        c["custom_audiotag_cooldown_min_value"] = self._parse_int_field(
            self.var_audiotag_cooldown_min.get(), AUDIOTAG_COOLDOWN_MIN, AUDIOTAG_COOLDOWN_MAX,
            AUDIOTAG_COOLDOWN_MIN_DEFAULT)
        c["custom_audiotag_cooldown_max_value"] = self._parse_int_field(
            self.var_audiotag_cooldown_max.get(), AUDIOTAG_COOLDOWN_MIN, AUDIOTAG_COOLDOWN_MAX,
            AUDIOTAG_COOLDOWN_MAX_DEFAULT)
        c["custom_audiotag_rotate_after_tracks_value"] = self._parse_int_field(
            self.var_audiotag_rotate_after.get(), AUDIOTAG_ROTATE_AFTER_MIN, AUDIOTAG_ROTATE_AFTER_MAX,
            AUDIOTAG_ROTATE_AFTER_DEFAULT)
        c["custom_audiotag_pause_seconds_value"] = self._parse_int_field(
            self.var_audiotag_pause_seconds.get(), AUDIOTAG_PAUSE_SECONDS_MIN, AUDIOTAG_PAUSE_SECONDS_MAX,
            AUDIOTAG_PAUSE_SECONDS_DEFAULT)
        c["custom_audiotag_min_duration_value"] = self._parse_int_field(
            self.var_audiotag_min_duration.get(), AUDIOTAG_MIN_DURATION_MIN, AUDIOTAG_MIN_DURATION_MAX,
            AUDIOTAG_MIN_DURATION_DEFAULT)
        c["theme_mode"] = self.var_theme_mode.get()
        c["language"] = self.var_language.get()
        c["create_pklz_hash_tables_on_load_val"] = bool(self.var_create_pklz_ht.get())
        for key in ("input_dir", "db_dir", "log_dir", "hash_tables_dir", "console_logs_dir"):
            value = self.dir_vars[key].get().strip()
            c[key] = value or default_config()[key]
        c["envfile_dir"] = ENV_FILE
        c["envfile_example_dir"] = ENV_EXAMPLE_FILE

    def _recompute_command(self):
        self.config_data["WERZATSONG_CMD"] = compute_werzatsong_cmd(
            self.config_data, pklz_folder_override=self._runtime_pklz_folder)

    def _save_config_to_disk(self):
        if self._suppress_config_saves:
            # During orchestration temporarily a runtime-only state could be held (the additional-
            # modes toggles, the PKLZ folder override) in config_data that must never land in
            # config.json. Skipping the write here is intentional; _run_pipeline's finally
            # block restores the real values before this flag is ever cleared.
            return
        save_config(self.config_data)

    def _sync_webhook_js(self):
        sync_webhook_js(self.config_data)

    # ------------------------------------------------------------------
    # Processed songs / PKLZ selection (assets/listsProcessed/*.json)
    # ------------------------------------------------------------------

    def _processed_songs_path(self, mode):
        return PROCESSED_SONGS_QUICK_FILE if mode == "quick" else PROCESSED_SONGS_LONG_FILE

    def _processed_json_input_dir_mismatch(self, path):
        """Returns (mismatch_bool, stored_input_dir) for the processed-songs JSON at `path`.
        mismatch_bool is True only when the file exists, is a well-formed dict, has a
        non-empty stored input_dir, and that input_dir differs (case-insensitively, path-
        normalized) from the currently configured one. Shared by _load_processed_songs,
        _save_processed_songs, and _rewrite_processed_json_extensions so all three consult
        exactly the same guard, per the "input_dir mismatch" edge case."""
        existing = load_json_file(path, None)
        if not isinstance(existing, dict):
            return False, ""
        stored_input_dir = existing.get("input_dir") or ""
        if not stored_input_dir:
            return False, ""
        current_input_dir = self.config_data.get("input_dir", DEFAULT_INPUT_DIR)
        mismatch = (os.path.normcase(os.path.normpath(stored_input_dir))
                    != os.path.normcase(os.path.normpath(current_input_dir)))
        return mismatch, stored_input_dir

    def _load_processed_songs(self, mode):
        """Returns (processed_set, input_dir_mismatch_bool) for the given mode ("quick" or
        "long"). If the JSON's stored input_dir differs from the currently configured one, the
        processed list is ignored (an empty set is returned instead), so a song should never be treated
        as already scanned just because it happens to share a relative path with something
        scanned under a different input folder. A [WARNING]-tagged line is logged via _log()
        every single time this is called on a mismatched file, not just once per session: the
        one-shot user-facing prompt lives in _on_start_clicked, not here."""
        path = self._processed_songs_path(mode)
        data = load_json_file(path, None)
        mismatch, stored_input_dir = self._processed_json_input_dir_mismatch(path)
        if mismatch:
            current_input_dir = self.config_data.get("input_dir", DEFAULT_INPUT_DIR)
            self._log(self._tr("log_input_dir_mismatch_read", file=path,
                                old_dir=stored_input_dir, new_dir=current_input_dir))
            return set(), True
        # A file that exists but failed to parse (or parsed to something other than a dict)
        # comes back as None from load_json_file: treat it the same as "missing", but log a
        # warning so a corrupt JSON on disk doesn't silently masquerade as "nothing processed
        # yet" without a trace in the console.
        if data is None and os.path.exists(path):
            self._log(self._tr("invalid_processed_json", file=path))
        processed_list = data.get("processed") if isinstance(data, dict) else None
        if not isinstance(processed_list, list):
            processed_list = []
        return set(processed_list), False

    def _save_processed_songs(self, mode, processed_set):
        """Atomically writes the processed-songs JSON for `mode`. Refuses to overwrite a file
        whose stored input_dir differs from the current one (logging a [WARNING]-tagged line
        via _log() every time the refusal happens): the stored paths may still be valid
        relative to that file's own input_dir (e.g. the user moved the input folder and will
        move it back), and blindly overwriting it with only this session's completions would
        destroy that history. The one-shot Tk prompt in _on_start_clicked offers to reset the
        file instead. Also prunes entries that no longer exist on disk, but only when the write
        actually proceeds (i.e. only when the mismatch check passes). Returns True/False."""
        path = self._processed_songs_path(mode)
        mismatch, stored_input_dir = self._processed_json_input_dir_mismatch(path)
        current_input_dir = self.config_data.get("input_dir", DEFAULT_INPUT_DIR)
        if mismatch:
            self._log(self._tr("log_input_dir_mismatch_write", file=path,
                                old_dir=stored_input_dir, new_dir=current_input_dir))
            return False
        pruned = {rel for rel in processed_set if os.path.exists(os.path.join(current_input_dir, rel))}
        data = {"version": 1, "mode": mode, "input_dir": current_input_dir, "processed": sorted(pruned)}
        return atomic_write_json(path, data)

    def _load_pklz_selection(self):
        """Returns (use_full_database, folders, files, db_dir_mismatch_bool). Missing/malformed
        JSON falls back to "use the full database". A mismatched database_dir (the folder
        moved, or db_dir was reconfigured) does not block anything: the stored names are
        still tried relative to the *current* db_dir, since PKLZ paths are typically still
        valid after such a move, and there is no data-loss risk either way, so unlike the
        processed-songs mismatch there is no reset prompt here, just a log warning.

        Version 1 of the file only had "folders"; "files" (individual .pklz selections) was
        added in version 2 and simply reads as empty from an older file."""
        default = {"version": 2, "database_dir": "", "use_full_database": True,
                   "folders": [], "files": []}
        data = load_json_file(PKLZ_FOLDERS_FILE, None)
        if not isinstance(data, dict):
            if data is None and os.path.exists(PKLZ_FOLDERS_FILE):
                self._log(self._tr("invalid_pklz_json", file=PKLZ_FOLDERS_FILE))
            data = default

        def string_list(value):
            return [v for v in value if isinstance(v, str)] if isinstance(value, list) else []

        use_full = bool(data.get("use_full_database", True))
        folders = string_list(data.get("folders"))
        files = string_list(data.get("files"))
        stored_db_dir = data.get("database_dir") or ""
        current_db_dir = self.config_data.get("db_dir", DEFAULT_DB_DIR)
        mismatch = bool(stored_db_dir) and (os.path.normcase(os.path.normpath(stored_db_dir))
                                             != os.path.normcase(os.path.normpath(current_db_dir)))
        if mismatch:
            self._log(self._tr("log_db_dir_mismatch", file=PKLZ_FOLDERS_FILE,
                                old_dir=stored_db_dir, new_dir=current_db_dir))
        return use_full, folders, files, mismatch

    def _save_pklz_selection(self, use_full, folders, files=()):
        current_db_dir = self.config_data.get("db_dir", DEFAULT_DB_DIR)
        data = {"version": 2, "database_dir": current_db_dir,
                "use_full_database": bool(use_full),
                "folders": list(folders), "files": list(files)}
        return atomic_write_json(PKLZ_FOLDERS_FILE, data)

    def _apply_pklz_staging(self, db_dir, use_full, folders, files, progress=None):
        """reconcile_pklz_staging() with the console kept informed. Returns how many .pklz
        files sit in ___TEMP afterwards, which is what a staged scan will actually search
        (0 with use_full). Safe to call from a worker thread: _log is queue-based."""
        if not os.path.isdir(db_dir):
            return 0

        def on_plan(to_temp, to_db):
            if use_full:
                if to_db:
                    self._log(self._tr("log_pklz_restore_all", count=to_db))
            elif to_temp or to_db:
                self._log(self._tr("log_pklz_staging_start", to_temp=to_temp, to_db=to_db))

        result = reconcile_pklz_staging(db_dir, use_full, folders, files,
                                        on_plan=on_plan, progress=progress)
        for kind, rel, detail in result["problems"]:
            if kind == "conflict":
                self._log(self._tr("log_pklz_staging_conflict", file=rel))
            else:
                self._log(self._tr("log_pklz_staging_error", file=rel, error=detail))
        if result["moved_in"] or result["moved_out"] or result["problems"]:
            self._log(self._tr("log_pklz_staging_done", to_temp=result["moved_in"],
                                to_db=result["moved_out"], errors=len(result["problems"])))
        return result["staged_after"]

    def _migrate_legacy_processed_file(self):
        """One-time migration from the old single PROCESSED.txt (bare "path", "path|quick", or
        "path|long" lines) to the two new processed-songs JSON files. Called once from
        __init__, after self.gui_strings is loaded (so the log line is localized) but before
        the UI is built.

        Atomicity of the two writes, as a unit: a naive "write Quick JSON, then write Long
        JSON" sequence could leave the two files in a half-migrated state if the process dies
        (or the disk fills) between the two os.replace() calls. To avoid that, both files are
        staged first (atomic_write_json_staged, which only writes the .tmp file) and only then
        committed with two back-to-back os.replace() calls (atomic_replace_staged).

        Recovery note, worth keeping as a comment so a future maintainer does not "fix" this:
        if this launch's SECOND os.replace() fails after the first one already succeeded, the
        legacy PROCESSED.txt is still on disk (it is only ever renamed after BOTH replaces
        succeed, see below). On the next launch, the "do both JSONs already exist" check below
        will either find Long missing (and safely re-migrate from the still-present legacy
        file, overwriting the stale partial Quick JSON with an identical fresh one) or find
        Long present-but-stale (in which case the early-return path below renames the legacy
        file to .migrated.bak and leaves the stale Long JSON alone). Either outcome is safe:
        no state where data is lost is reachable, since the legacy file is only ever removed
        (via rename) once both JSONs are confirmed written.
        """
        quick_exists = os.path.exists(PROCESSED_SONGS_QUICK_FILE)
        long_exists = os.path.exists(PROCESSED_SONGS_LONG_FILE)
        legacy_exists = os.path.exists(LEGACY_PROCESSED_FILE)

        if quick_exists and long_exists:
            if legacy_exists:
                try:
                    os.replace(LEGACY_PROCESSED_FILE, LEGACY_PROCESSED_FILE + ".migrated.bak")
                except Exception:
                    pass
            return

        if not legacy_exists:
            return

        input_dir = self.config_data.get("input_dir", DEFAULT_INPUT_DIR)
        quick_processed = set()
        long_processed = set()
        try:
            with open(LEGACY_PROCESSED_FILE, "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
        except Exception as e:
            self._log(self._tr("log_migration_read_error", error=e))
            return

        for line in lines:
            if line.endswith("|quick"):
                quick_processed.add(line[: -len("|quick")])
            elif line.endswith("|long"):
                long_processed.add(line[: -len("|long")])
            else:
                quick_processed.add(line)
                long_processed.add(line)

        quick_data = {"version": 1, "mode": "quick", "input_dir": input_dir,
                      "processed": sorted(quick_processed)}
        long_data = {"version": 1, "mode": "long", "input_dir": input_dir,
                     "processed": sorted(long_processed)}

        quick_staged = atomic_write_json_staged(PROCESSED_SONGS_QUICK_FILE, quick_data)
        long_staged = atomic_write_json_staged(PROCESSED_SONGS_LONG_FILE, long_data)

        if not (quick_staged and long_staged):
            for path in (PROCESSED_SONGS_QUICK_FILE, PROCESSED_SONGS_LONG_FILE):
                tmp_path = path + ".tmp"
                try:
                    if os.path.exists(tmp_path):
                        os.remove(tmp_path)
                except Exception:
                    pass
            self._log(self._tr("log_migration_write_error"))
            return

        if not atomic_replace_staged(PROCESSED_SONGS_QUICK_FILE):
            self._log(self._tr("log_migration_write_error"))
            return
        if not atomic_replace_staged(PROCESSED_SONGS_LONG_FILE):
            self._log(self._tr("log_migration_write_error"))
            return

        try:
            os.replace(LEGACY_PROCESSED_FILE, LEGACY_PROCESSED_FILE + ".migrated.bak")
        except Exception:
            pass

        self._log(self._tr("log_migration_success", count=len(lines)))

    def _maybe_flush_env(self):
        if self.is_running:
            self.pending_env = True
        else:
            self._write_env_now()

    def _write_env_now(self):
        if write_env_file(ENV_FILE, self.env_data):
            self.pending_env = False
            self._env_dirty_keys.clear()

    def _reload_env_from_disk(self):
        disk_env = parse_env_file(ENV_FILE)
        if not disk_env:
            return
        changed_shown = False
        for key, value in disk_env.items():
            if key in REQUIRED_ENV_KEYS and key in self._env_dirty_keys:
                continue
            if self.env_data.get(key) != value:
                self.env_data[key] = value
                if self.show_state.get(key):
                    changed_shown = True
        if changed_shown:
            for key in REQUIRED_ENV_KEYS:
                if self.show_state.get(key) and key in self.env_vars:
                    self._set_var_silently(self.env_vars[key], self.env_data.get(key, ""))

    def _reload_audiotag_keys_from_disk(self):
        """Re-reads audiotag_keys.json after a scan, so per-key usage counts/status that the
        Node side just updated (see assets/utils/audiotagKeys.js) show up in the key list
        editor without needing to reopen Advanced Settings."""
        self.audiotag_keys_data = load_audiotag_keys()
        self._refresh_audiotag_keys_listbox()

    def _toggle_env_show(self, key):
        self.show_state[key] = not self.show_state.get(key, False)
        if self.show_state[key]:
            self._set_var_silently(self.env_vars[key], self.env_data.get(key, ""))
            self.env_show_frames[key].grid()
            self.env_show_buttons[key].grid_remove()
        else:
            self.env_show_frames[key].grid_remove()
            self.env_show_buttons[key].grid()
        sync = getattr(self, "_sync_body_geometry", None)
        if sync is not None:
            try:
                sync()
            except tk.TclError:
                pass

    # ------------------------------------------------------------------
    # Directories
    # ------------------------------------------------------------------

    def _open_directory(self, key):
        path = self.dir_vars[key].get().strip() or self.config_data.get(key)
        if not path:
            return
        try:
            os.makedirs(path, exist_ok=True)
            os.startfile(path)
        except Exception as e:
            messagebox.showerror(self._tr("error_title"), self._tr("dir_open_error", error=e))

    def _browse_directory(self, key):
        current = self.dir_vars[key].get().strip() or self.config_data.get(key) or CUR_FOLDER
        initial = current if os.path.isdir(current) else CUR_FOLDER
        chosen = filedialog.askdirectory(title=self._tr("dir_select_title"), initialdir=initial)
        if not chosen:
            return
        self._set_var_silently(self.dir_vars[key], os.path.normpath(chosen))
        self._flush_immediately()

    # ------------------------------------------------------------------
    # Credits
    # ------------------------------------------------------------------

    def _load_logo_photo(self, subsample):
        img = tk.PhotoImage(file=LOGO_FILE)
        if subsample and subsample > 1:
            img = img.subsample(subsample, subsample)
        return img

    def _open_credits(self):
        top = ThemedToplevel(self)
        top.title(self._tr("credits_title"))
        top.resizable(False, False)
        top.transient(self)

        frame = ttk.Frame(top, padding=15)
        frame.pack(fill="both", expand=True)

        self._credits_logo_img = self._load_logo_photo(2)  # 250 / 2 = 125x125
        ttk.Label(frame, image=self._credits_logo_img).grid(row=0, column=0, rowspan=2, padx=(0, 15), sticky="n")
        self._add_text_widget(ttk.Label(frame, font=("Segoe UI", 13, "bold")),
                              "credits_title").grid(row=0, column=1, sticky="w")

        text = tk.Text(frame, width=46, height=7, wrap="word", borderwidth=0, highlightthickness=0)
        text.grid(row=1, column=1, sticky="w")
        text.tag_configure("bold", font=("Segoe UI", 9, "bold"))

        def add_credit(bold_part, rest):
            text.insert("end", bold_part, ("bold",))
            text.insert("end", rest + "\n\n")

        add_credit(self._tr("credits_line1"), self._tr("credits_line1_rest"))
        add_credit(self._tr("credits_line2"), self._tr("credits_line2_rest"))
        add_credit(self._tr("credits_line3"), self._tr("credits_line3_rest"))
        text.configure(state="disabled")

        self._add_text_widget(ttk.Button(frame, command=top.destroy),
                              "close_btn").grid(row=2, column=0, columnspan=2, pady=(10, 0))
        top.grab_set()

# ------------------------------------------------------------------
# Song Selection / PKLZ Folder Selection dialogs
# ------------------------------------------------------------------

    def _open_song_selection_menu(self):
        """Opens the Song Selection dialog: a searchable, sortable tree of input_dir with
        a Quick/Long checkbox per song, a Filetype column, and a Files/Size column
        (aggregated up through folders). Mirrors the PKLZ Selection dialog's UX.
        Saves two processed-songs JSON files (the unchecked = processed/excluded set)
        plus the combined Song summary used by the General tab's summary label."""
        input_dir = self.config_data.get("input_dir", DEFAULT_INPUT_DIR)
        if not os.path.exists(input_dir):
            messagebox.showerror(self._tr("error_title"), self._tr("input_dir_not_found", dir=input_dir))
            return

        all_files = {}
        for root, dirs, files in os.walk(input_dir):
            if TEMP_STAGING_DIRNAME in dirs:
                dirs.remove(TEMP_STAGING_DIRNAME)
            for file in files:
                if os.path.splitext(file)[1].lower() in AUDIO_EXTENSIONS:
                    full_path = os.path.join(root, file)
                    rel = os.path.relpath(full_path, input_dir)
                    try:
                        all_files[rel] = os.path.getsize(full_path)
                    except OSError:
                        all_files[rel] = 0

        if not all_files:
            messagebox.showinfo(self._tr("info_title"), self._tr("no_audio_files_found", dir=input_dir))
            return

        quick_processed, _ = self._load_processed_songs("quick")
        long_processed, _ = self._load_processed_songs("long")

        file_state = {
            rel: {"quick": rel not in quick_processed, "long": rel not in long_processed}
            for rel in all_files
        }

        class _SongNode:
            __slots__ = ("name", "rel", "is_file", "ext", "size", "count", "children", "parent")

            def __init__(self, name, rel, is_file, ext="", size=0, parent=None):
                self.name = name
                self.rel = rel
                self.is_file = is_file
                self.ext = ext
                self.size = size
                self.count = 1 if is_file else 0
                self.children = {}
                self.parent = parent

        root_node = _SongNode("", "", False)
        all_nodes = []
        for rel, size in all_files.items():
            parts = rel.split(os.sep)
            node = root_node
            accum = ""
            for i, part in enumerate(parts):
                accum = part if not accum else os.path.join(accum, part)
                is_file = (i == len(parts) - 1)
                child = node.children.get(part)
                if child is None:
                    if is_file:
                        ext = os.path.splitext(part)[1].lower().lstrip(".")
                        child = _SongNode(part, accum, True, ext=ext, size=size, parent=node)
                    else:
                        child = _SongNode(part, accum, False, parent=node)
                    node.children[part] = child
                    all_nodes.append(child)
                node = child
            walker = node.parent
            while walker is not None and walker is not root_node:
                walker.size += size
                walker.count += 1
                walker = walker.parent

        top = ThemedToplevel(self)
        top.title(self._tr("song_selection_title"))
        top.transient(self)
        top.geometry("860x620")
        top.minsize(640, 420)

        self._add_text_widget(
            ttk.Label(top, wraplength=820, justify="left", padding=(10, 8, 10, 0)),
            "song_selection_both_modes_note"
        ).pack(fill="x")

        var_search = tk.StringVar()

        search_row = ttk.Frame(top, padding=(10, 6, 10, 0))
        search_row.pack(fill="x")
        self._add_text_widget(ttk.Label(search_row, text=""), "pklz_search_label").pack(side="left")
        search_entry = ttk.Entry(search_row, textvariable=var_search)
        search_entry.pack(side="left", fill="x", expand=True, padx=(6, 6))
        self._add_text_widget(ttk.Button(search_row, command=lambda: var_search.set("")),
                              "pklz_search_clear_btn").pack(side="left")

        tree_frame = ttk.Frame(top, padding=(10, 6, 10, 0))
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(tree_frame,
                            columns=("quick", "long", "filetype", "count", "size"),
                            show="tree headings")
        tree.column("#0", width=250, stretch=True)
        tree.column("quick", width=80, anchor="center", stretch=False)
        tree.column("long", width=80, anchor="center", stretch=False)
        tree.column("filetype", width=70, anchor="center", stretch=False)
        tree.column("count", width=60, anchor="e", stretch=False)
        tree.column("size", width=90, anchor="e", stretch=False)

        vscroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vscroll.set)
        tree.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")

        CHECKED, UNCHECKED, PARTIAL = "☑", "☐", "▣"
        SEARCH_RESULT_LIMIT = 400

        node_to_item = {}
        item_to_node = {}
        sort_state = {"key": "name", "desc": False}

        def glyph_for(checked):
            return CHECKED if checked else UNCHECKED

        def folder_tristate(node, mode):
            total = 0
            checked = 0

            def walk(n):
                nonlocal total, checked
                if n.is_file:
                    total += 1
                    if file_state[n.rel][mode]:
                        checked += 1
                else:
                    for c in n.children.values():
                        walk(c)

            walk(node)
            if total == 0 or checked == 0:
                return "unchecked"
            if checked == total:
                return "checked"
            return "partial"

        def sort_key(node):
            key = sort_state["key"]
            if key in ("quick", "long"):
                if node.is_file:
                    order = 0 if file_state[node.rel][key] else 2
                else:
                    order = {"checked": 0, "partial": 1, "unchecked": 2}[folder_tristate(node, key)]
                return (order, node.name.casefold())
            if key == "filetype":
                return (node.is_file, node.ext, node.name.casefold())
            if key == "count":
                return (-node.count, node.name.casefold())
            if key == "size":
                return (-node.size, node.name.casefold())
            return (node.is_file, node.name.casefold())

        def sorted_children(node):
            children = sorted(node.children.values(), key=sort_key)
            if sort_state["desc"]:
                children.reverse()
            return children

        def row_values(node):
            if node.is_file:
                state = file_state[node.rel]
                return (glyph_for(state["quick"]), glyph_for(state["long"]),
                        node.ext, "", format_size(node.size))
            glyph_map = {"checked": CHECKED, "unchecked": UNCHECKED, "partial": PARTIAL}
            return (glyph_map[folder_tristate(node, "quick")],
                    glyph_map[folder_tristate(node, "long")],
                    "", f"{node.count:,}", format_size(node.size))

        def insert_node(parent_item, node):
            iid = tree.insert(parent_item, "end", text=node.name, values=row_values(node), open=True)
            node_to_item[node] = iid
            item_to_node[iid] = node
            if not node.is_file:
                for child in sorted_children(node):
                    insert_node(iid, child)

        def rebuild_tree():
            tree.delete(*tree.get_children(""))
            node_to_item.clear()
            item_to_node.clear()
            for child in sorted_children(root_node):
                insert_node("", child)

        def update_summary():
            quick_count = 0
            long_count = 0
            total_count = 0
            total_bytes = 0
            for rel, state in file_state.items():
                in_q = state["quick"]
                in_l = state["long"]
                if in_q:
                    quick_count += 1
                if in_l:
                    long_count += 1
                if in_q or in_l:
                    total_count += 1
                    total_bytes += all_files.get(rel, 0)
            if total_count == 0:
                summary_label.config(text=self._tr("song_summary_empty"))
                return
            summary_label.config(text=self._tr("song_summary_selection",
                count=total_count, quick=quick_count, long=long_count,
                size=format_size(total_bytes)))

        def refresh_visible_glyphs():
            for iid, node in list(item_to_node.items()):
                if not tree.exists(iid):
                    continue
                tree.item(iid, values=row_values(node))
            update_summary()

        def set_subtree(node, mode, value):
            if node.is_file:
                file_state[node.rel][mode] = value
            else:
                for child in node.children.values():
                    set_subtree(child, mode, value)

        def toggle(node, mode):
            if node.is_file:
                set_subtree(node, mode, not file_state[node.rel][mode])
            else:
                new_value = folder_tristate(node, mode) != "checked"
                set_subtree(node, mode, new_value)
            refresh_visible_glyphs()

        def on_tree_click(event):
            if tree.identify_region(event.x, event.y) != "cell":
                return
            col = tree.identify_column(event.x)
            node = item_to_node.get(tree.identify_row(event.y))
            if node is None:
                return
            if col == "#1":
                toggle(node, "quick")
            elif col == "#2":
                toggle(node, "long")

        tree.bind("<Button-1>", on_tree_click)

        def select_all(mode, value):
            for child in root_node.children.values():
                set_subtree(child, mode, value)
            refresh_visible_glyphs()

        # ---- search ---------------------------------------------------------
        def apply_search(*_args):
            needle = var_search.get().strip().casefold()
            if not needle:
                rebuild_tree()
                return
            tree.delete(*tree.get_children(""))
            node_to_item.clear()
            item_to_node.clear()
            hits = [n for n in all_nodes if needle in n.rel.casefold()]
            hits.sort(key=sort_key)
            if sort_state["desc"]:
                hits.reverse()
            shown = hits[:SEARCH_RESULT_LIMIT]
            for node in shown:
                iid = tree.insert("", "end", text=node.rel, values=row_values(node), open=False)
                node_to_item[node] = iid
                item_to_node[iid] = node
            if len(hits) > len(shown):
                tree.insert("", "end",
                            text=self._tr("pklz_search_truncated",
                                          shown=len(shown), total=len(hits)),
                            values=("", "", "", "", ""), tags=("disabled",))
            tree.tag_configure("disabled", foreground="#888888")

        var_search.trace_add("write", apply_search)

        # ---- sorting --------------------------------------------------------
        def sort_by(key):
            if sort_state["key"] == key:
                sort_state["desc"] = not sort_state["desc"]
            else:
                sort_state["key"] = key
                sort_state["desc"] = False
            update_headings()
            if var_search.get().strip():
                apply_search()
            else:
                rebuild_tree()

        def update_headings():
            arrow = " ▼" if sort_state["desc"] else " ▲"
            for key, label_key in (("name", "file_column"), ("quick", "quick_column"),
                                   ("long", "long_column"), ("filetype", "song_filetype_column"),
                                   ("count", "pklz_files_column"), ("size", "pklz_size_column")):
                text = self._tr(label_key) + (arrow if sort_state["key"] == key else "")
                tree.heading("#0" if key == "name" else key, text=text,
                             command=(lambda k=key: sort_by(k)))

        update_headings()

        # ---- buttons + save -------------------------------------------------
        btn_frame = ttk.Frame(top, padding=(10, 0, 10, 6))
        btn_frame.pack(fill="x")
        self._add_text_widget(ttk.Button(btn_frame, command=lambda: select_all("quick", True)),
                              "select_all_quick_btn").pack(side="left", padx=2)
        self._add_text_widget(ttk.Button(btn_frame, command=lambda: select_all("quick", False)),
                              "clear_quick_btn").pack(side="left", padx=2)
        self._add_text_widget(ttk.Button(btn_frame, command=lambda: select_all("long", True)),
                              "select_all_long_btn").pack(side="left", padx=2)
        self._add_text_widget(ttk.Button(btn_frame, command=lambda: select_all("long", False)),
                              "clear_long_btn").pack(side="left", padx=2)

        summary_label = ttk.Label(top, padding=(10, 6, 10, 0), foreground="#888888")
        summary_label.pack(fill="x")

        action_frame = ttk.Frame(top, padding=(10, 0, 10, 10))
        action_frame.pack(fill="x")

        def do_save():
            quick_checked = {rel for rel, state in file_state.items() if state["quick"]}
            long_checked = {rel for rel, state in file_state.items() if state["long"]}
            self._save_song_selection(quick_checked, long_checked)
            self._refresh_selection_summary_label()
            top.destroy()

        self._add_text_widget(ttk.Button(action_frame, command=do_save),
                              "save_btn").pack(side="right", padx=2)
        self._add_text_widget(ttk.Button(action_frame, command=top.destroy),
                              "cancel_btn").pack(side="right", padx=2)

        rebuild_tree()
        update_summary()
        search_entry.focus_set()

        top.protocol("WM_DELETE_WINDOW", top.destroy)
        top.grab_set()

    def _save_song_selection(self, quick_checked, long_checked):
        """quick_checked/long_checked: the full relative paths (from the Song Selection
        dialog) that are checked, i.e. candidates for that mode. Saves the complement
        (the files that are NOT checked, meaning already processed or deliberately
        excluded) to each mode's JSON, then writes the combined Song summary used by
        the General tab's summary label and its hover tooltip. Fully-checked folders
        are collapsed in the summary (replacing the individual files under them), so
        the tooltip lists folders where it makes sense, exactly like the PKLZ side."""
        input_dir = self.config_data.get("input_dir", DEFAULT_INPUT_DIR)
        all_files = {}
        for root, dirs, files in os.walk(input_dir):
            if TEMP_STAGING_DIRNAME in dirs:
                dirs.remove(TEMP_STAGING_DIRNAME)
            for file in files:
                if os.path.splitext(file)[1].lower() in AUDIO_EXTENSIONS:
                    full = os.path.join(root, file)
                    rel = os.path.relpath(full, input_dir)
                    try:
                        all_files[rel] = os.path.getsize(full)
                    except OSError:
                        all_files[rel] = 0

        all_rel = set(all_files.keys())
        # Save the processed-songs JSONs (the user's actual scan-state change), but
        # do NOT gate the summary save on their results. The summary is a display
        # hint about what the user picked in this dialog, and it must stay accurate
        # even when both processed-songs writes are refused (e.g. both JSONs are
        # stuck in input_dir mismatch state).
        self._save_processed_songs("quick", all_rel - quick_checked)
        self._save_processed_songs("long", all_rel - long_checked)

        selected = quick_checked | long_checked

        def mode_of(rel):
            in_q = rel in quick_checked
            in_l = rel in long_checked
            if in_q and in_l:
                return "both"
            return "quick" if in_q else "long"

        # Aggregate counters for the summary line.
        filetypes = {}
        bytes_total = 0
        for rel in selected:
            ext = os.path.splitext(rel)[1].lower().lstrip(".")
            filetypes[ext] = filetypes.get(ext, 0) + 1
            bytes_total += all_files.get(rel, 0)

        # Collapse fully-checked folders into single tooltip rows.
        full_folders = compute_fully_checked_folders(all_rel, selected)
        covered = set()
        names = []
        for folder in full_folders:
            prefix = folder + os.sep
            folder_q = folder_l = False
            for rel in selected:
                if rel == folder or rel.startswith(prefix):
                    covered.add(rel)
                    m = mode_of(rel)
                    if m in ("quick", "both"):
                        folder_q = True
                    if m in ("long", "both"):
                        folder_l = True
            if folder_q and folder_l:
                mode = "both"
            elif folder_q:
                mode = "quick"
            else:
                mode = "long"
            names.append([folder, mode])
        for rel in sorted(selected):
            if rel in covered:
                continue
            names.append([rel, mode_of(rel)])

        summary = {
            "all_selected": selected == all_rel,
            "count": len(selected),
            "quick_count": len(quick_checked),
            "long_count": len(long_checked),
            "filetypes": filetypes,
            "bytes": bytes_total,
            "names": names[:12],
            "names_total": len(names),
        }
        self._save_selection_summary_part("songs", summary)

    def _open_pklz_selection_menu(self):
        """Opens the PKLZ Selection dialog: a lazily-expanded tree of the Audfprint database
        with a checkbox on every folder AND every individual .pklz file, letting a scan be
        restricted to any subset instead of always searching the whole database.

        Saving writes PKLZ_FOLDERS_FILE and then physically stages the selection into
        database/___TEMP (see reconcile_pklz_staging): Audfprint can only be aimed at a
        folder, so an arbitrary selection has to be gathered into one. The moves happen on
        Save rather than on each click because ticking a single folder here can mean tens of
        thousands of files (this database's largest holds 12,414), and doing that work per
        keystroke would freeze the dialog and leave half-moved state behind whenever someone
        changed their mind. The scan re-applies the same reconcile before it runs, so the
        staging folder always ends up agreeing with what was saved.

        Everything is built around the database being large: 30,000+ files is far more than a
        Treeview will accept at once, so folders start collapsed and their children are only
        inserted the first time they are opened."""
        db_dir = self.config_data.get("db_dir", DEFAULT_DB_DIR)
        if not os.path.exists(db_dir):
            messagebox.showerror(self._tr("error_title"), self._tr("pklz_folder_missing", dir=db_dir))
            return

        files_index, _staged_now = scan_pklz_database(db_dir)
        if not files_index:
            messagebox.showinfo(self._tr("info_title"), self._tr("no_pklz_folders_found", dir=db_dir))
            return

        class _PklzNode:
            __slots__ = ("name", "rel", "children", "parent", "is_file", "size", "count")

            def __init__(self, name, rel, parent=None, is_file=False, size=0):
                self.name = name
                self.rel = rel
                self.children = {}
                self.parent = parent
                self.is_file = is_file
                self.size = size          # own size for a file, aggregate for a folder
                self.count = 1 if is_file else 0   # .pklz files at or under this node

        proot = _PklzNode("", "")
        all_nodes = []
        for rel, size in files_index.items():
            parts = rel.split(os.sep)
            node = proot
            accum = ""
            for part in parts[:-1]:
                accum = part if not accum else os.path.join(accum, part)
                child = node.children.get(part)
                if child is None:
                    child = _PklzNode(part, accum, node)
                    node.children[part] = child
                    all_nodes.append(child)
                node = child
            leaf = _PklzNode(parts[-1], rel, node, is_file=True, size=size)
            node.children[parts[-1]] = leaf
            all_nodes.append(leaf)
            # Roll the file's size and its own count up through every ancestor, so a folder
            # row can state what selecting it actually costs without walking the disk again.
            walker = node
            while walker is not None and walker is not proot:
                walker.size += size
                walker.count += 1
                walker = walker.parent

        use_full, saved_folders, saved_files, _db_mismatch = self._load_pklz_selection()
        known_folders = {n.rel for n in all_nodes if not n.is_file}
        selected_folders = {f for f in saved_folders if f in known_folders}
        selected_files = {f for f in saved_files if f in files_index}

        top = ThemedToplevel(self)
        top.title(self._tr("pklz_folder_selection_title"))
        top.transient(self)
        top.geometry("760x600")
        top.minsize(560, 420)

        var_use_full = tk.BooleanVar(value=use_full)
        var_search = tk.StringVar()

        header = ttk.Frame(top, padding=(10, 10, 10, 0))
        header.pack(fill="x")
        ttk.Checkbutton(header, variable=var_use_full, text=self._tr("use_full_database_check"),
                        command=lambda: refresh_enabled()).pack(anchor="w")

        search_row = ttk.Frame(top, padding=(10, 6, 10, 0))
        search_row.pack(fill="x")
        self._add_text_widget(ttk.Label(search_row, text=""), "pklz_search_label").pack(side="left")
        search_entry = ttk.Entry(search_row, textvariable=var_search)
        search_entry.pack(side="left", fill="x", expand=True, padx=(6, 6))
        self._add_text_widget(ttk.Button(search_row, command=lambda: var_search.set("")),
                              "pklz_search_clear_btn").pack(side="left")

        tree_frame = ttk.Frame(top, padding=(10, 6, 10, 0))
        tree_frame.pack(fill="both", expand=True)

        tree = ttk.Treeview(tree_frame, columns=("selected", "count", "size"),
                            show="tree headings")
        tree.column("#0", width=380, stretch=True)
        tree.column("selected", width=54, anchor="center", stretch=False)
        tree.column("count", width=80, anchor="e", stretch=False)
        tree.column("size", width=96, anchor="e", stretch=False)

        vscroll = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vscroll.set)
        tree.pack(side="left", fill="both", expand=True)
        vscroll.pack(side="right", fill="y")

        # Three states, because per-file selection makes "some of this folder" reachable:
        # a folder whose subtree is partly picked is neither checked nor unchecked.
        CHECKED, UNCHECKED, PARTIAL = "☑", "☐", "▣"
        LAZY_MARKER = "__lazy__"
        SEARCH_RESULT_LIMIT = 400

        node_to_item = {}
        item_to_node = {}
        # (column key, descending). Name ascending is the default the tree is built in.
        sort_state = {"key": "name", "desc": False}

        def is_ancestor_of(anc, node):
            n = node.parent
            while n is not None and n is not proot:
                if n is anc:
                    return True
                n = n.parent
            return False

        def build_selection_except(excluded):
            """Returns (folders, files) covering everything in the tree except `excluded`
            and its descendants. Used the first time the user unchecks a single row while
            'Use full database' is checked."""
            folders = set()
            files = set()

            def walk(parent):
                for child in parent.children.values():
                    if child is excluded:
                        continue
                    if is_ancestor_of(child, excluded):
                        walk(child)
                    else:
                        if child.is_file:
                            files.add(child.rel)
                        else:
                            folders.add(child.rel)

            walk(proot)
            return folders, files

        def covered_by_ancestor(node):
            anc = node.parent
            while anc is not None and anc is not proot:
                if anc.rel in selected_folders:
                    return True
                anc = anc.parent
            return False

        def subtree_has_selection(node):
            if node.is_file:
                return node.rel in selected_files
            if node.rel in selected_folders:
                return True
            return any(subtree_has_selection(child) for child in node.children.values())

        def subtree_fully_selected(node):
            """True when every .pklz file at or under `node` is selected, whether
            that is via the node itself or an ancestor being in selected_folders,
            or via every individual descendant file being in selected_files. Used so
            a folder whose files have all been clicked one by one still reads as
            fully selected, exactly like the Song Selection dialog already does."""
            if node.is_file:
                return node.rel in selected_files or covered_by_ancestor(node)
            if node.rel in selected_folders or covered_by_ancestor(node):
                return True
            if not node.children:
                return False
            return all(subtree_fully_selected(child) for child in node.children.values())

        def glyph_for(node):
            if node.is_file:
                return CHECKED if (node.rel in selected_files or covered_by_ancestor(node)) else UNCHECKED
            if node.rel in selected_folders or covered_by_ancestor(node):
                return CHECKED
            if subtree_fully_selected(node):
                return CHECKED
            return PARTIAL if subtree_has_selection(node) else UNCHECKED

        def sort_key(node):
            key = sort_state["key"]
            if key == "selected":
                order = {CHECKED: 0, PARTIAL: 1, UNCHECKED: 2}[glyph_for(node)]
                return (order, node.name.casefold())
            if key == "count":
                return (-node.count, node.name.casefold())
            if key == "size":
                return (-node.size, node.name.casefold())
            # Folders before files at the same level, then alphabetically: a flat mix of the
            # two is much harder to scan in a folder holding hundreds of shards.
            return (node.is_file, node.name.casefold())

        def sorted_children(node):
            children = sorted(node.children.values(), key=sort_key)
            if sort_state["desc"]:
                children.reverse()
            return children

        def row_values(node):
            return (glyph_for(node),
                    f"{node.count:,}" if not node.is_file else "",
                    format_size(node.size))

        def insert_node(parent_item, node):
            iid = tree.insert(parent_item, "end", text=node.name, values=row_values(node),
                              open=False)
            node_to_item[node] = iid
            item_to_node[iid] = node
            if node.children:
                # A placeholder child is what makes the expand arrow appear without paying
                # for the subtree: it is swapped for the real rows on first open.
                tree.insert(iid, "end", iid=f"{iid}::lazy", text="", values=("", "", ""),
                            tags=(LAZY_MARKER,))
            return iid

        def populate(item):
            node = item_to_node.get(item)
            if node is None:
                return
            children = tree.get_children(item)
            if not (len(children) == 1 and children[0].endswith("::lazy")):
                return  # already real
            tree.delete(children[0])
            for child in sorted_children(node):
                insert_node(item, child)

        def on_open(_event=None):
            populate(tree.focus())

        tree.bind("<<TreeviewOpen>>", on_open)

        def rebuild_tree():
            """Full repaint of the top level. Only ever inserts the roots; everything deeper
            comes back through populate() as the user expands it again."""
            tree.delete(*tree.get_children(""))
            node_to_item.clear()
            item_to_node.clear()
            for child in sorted_children(proot):
                insert_node("", child)

        def refresh_visible_glyphs():
            """Repaints only rows that currently exist in the widget. When 'Use full
            database' is checked, every row shows as checked and none are greyed out,
            so the user can click a specific row to start editing the selection."""
            full = var_use_full.get()
            for iid, node in list(item_to_node.items()):
                if not tree.exists(iid):
                    continue
                if full:
                    tree.set(iid, "selected", CHECKED)
                    tree.item(iid, tags=())
                else:
                    tree.set(iid, "selected", glyph_for(node))
                    tree.item(iid, tags=("disabled",) if covered_by_ancestor(node) else ())
            tree.tag_configure("disabled", foreground="#888888")
            update_summary()

        def clear_descendants(node):
            for child in node.children.values():
                selected_folders.discard(child.rel)
                selected_files.discard(child.rel)
                clear_descendants(child)

        def clear_ancestors(node):
            anc = node.parent
            while anc is not None and anc is not proot:
                selected_folders.discard(anc.rel)
                anc = anc.parent

        def toggle_node(node):
            # Same rule as before, now covering files too: picking a parent supersedes (and
            # visually disables) everything under it, and picking something inside clears the
            # broader choice above it. Siblings stay independent.
            if covered_by_ancestor(node):
                return
            if node.is_file:
                if node.rel in selected_files:
                    selected_files.discard(node.rel)
                else:
                    clear_ancestors(node)
                    selected_files.add(node.rel)
            else:
                # A folder is "effectively checked" if it, an ancestor, or every single
                # descendant file is selected. Clicking such a folder unchecks the whole
                # subtree (dropping the folder's own explicit entry if it had one); otherwise
                # it checks the folder explicitly. Without this, a folder whose files were
                # all clicked individually would LOOK checked but clicking it would silently
                # re-add it as an explicit selection instead of toggling it off.
                if node.rel in selected_folders or subtree_fully_selected(node):
                    selected_folders.discard(node.rel)
                    clear_descendants(node)
                else:
                    clear_ancestors(node)
                    clear_descendants(node)
                    selected_folders.add(node.rel)
            refresh_visible_glyphs()

        def is_all_selected():
            resolved = selected_pklz_set(files_index, selected_folders, selected_files)
            return len(resolved) == len(files_index)

        def on_click(event):
            if tree.identify_region(event.x, event.y) != "cell":
                return
            if tree.identify_column(event.x) != "#1":
                return
            node = item_to_node.get(tree.identify_row(event.y))
            if node is None:
                return

            # First click while "Use full database" is checked: convert the implicit
            # "everything" selection into an explicit one that covers everything
            # *except* this node, then uncheck the full-database option.
            if var_use_full.get():
                folders, files = build_selection_except(node)
                selected_folders.clear()
                selected_folders.update(folders)
                selected_files.clear()
                selected_files.update(files)
                var_use_full.set(False)
                refresh_enabled()
                return

            toggle_node(node)

            # If everything is now (again) covered, switch back to full-database mode,
            # which means the scan uses the plain database root and no --folder flag.
            # This runs the full selected_pklz_set() walk once per click; at 30k files
            # that is ~50-100ms, which is fine for a user-driven click. A top-level-only
            # shortcut would be wrong: a user can individually check every file in every
            # folder without ever ticking a top-level folder, and that is still
            # "everything selected" logically.
            if is_all_selected():
                var_use_full.set(True)
                selected_folders.clear()
                selected_files.clear()
                refresh_enabled()
            else:
                refresh_visible_glyphs()

        tree.bind("<Button-1>", on_click)

        # ---- search -------------------------------------------------------------
        # Searching abandons the tree for a flat result list: matches can sit anywhere in a
        # three-level structure, and expanding every branch that happens to contain one is
        # both slow and unreadable. Each hit shows its full relative path instead.
        def apply_search(*_args):
            needle = var_search.get().strip().casefold()
            if not needle:
                rebuild_tree()
                refresh_visible_glyphs()
                return
            tree.delete(*tree.get_children(""))
            node_to_item.clear()
            item_to_node.clear()
            hits = [n for n in all_nodes if needle in n.rel.casefold()]
            hits.sort(key=sort_key)
            if sort_state["desc"]:
                hits.reverse()
            shown = hits[:SEARCH_RESULT_LIMIT]
            for node in shown:
                iid = tree.insert("", "end", text=node.rel, values=row_values(node), open=False)
                node_to_item[node] = iid
                item_to_node[iid] = node
            if len(hits) > len(shown):
                tree.insert("", "end", text=self._tr("pklz_search_truncated",
                                                     shown=len(shown), total=len(hits)),
                            values=("", "", ""), tags=("disabled",))
            refresh_visible_glyphs()

        var_search.trace_add("write", apply_search)

        # ---- sorting ------------------------------------------------------------
        def sort_by(key):
            if sort_state["key"] == key:
                sort_state["desc"] = not sort_state["desc"]
            else:
                sort_state["key"] = key
                sort_state["desc"] = False
            update_headings()
            if var_search.get().strip():
                apply_search()
            else:
                rebuild_tree()
                refresh_visible_glyphs()

        def update_headings():
            arrow = " ▼" if sort_state["desc"] else " ▲"
            for key, label_key in (("name", "file_column"), ("selected", "pklz_selected_column"),
                                   ("count", "pklz_files_column"), ("size", "pklz_size_column")):
                text = self._tr(label_key) + (arrow if sort_state["key"] == key else "")
                tree.heading("#0" if key == "name" else key, text=text,
                             command=(lambda k=key: sort_by(k)))

        update_headings()

        # ---- summary + actions --------------------------------------------------
        summary_label = ttk.Label(top, padding=(10, 6, 10, 0))
        summary_label.pack(fill="x")

        def current_selection_stats():
            resolved = selected_pklz_set(files_index, selected_folders, selected_files)
            return len(resolved), sum(files_index[r] for r in resolved)

        def collapsed_view():
            """Returns (names, folders_count, files_count) for the *display* view of
            the tree, not the raw storage. A folder whose every .pklz is selected
            -- whether the user ticked the folder itself or every file inside it
            one by one -- collapses to a single folder entry, and its files are
            not counted separately. Both the in-dialog summary label and the saved
            summary (used by the General tab's tooltip) go through this, so they
            always agree."""
            names = []
            folders = 0
            files = 0

            def walk(node):
                nonlocal folders, files
                if subtree_fully_selected(node):
                    if node.is_file:
                        files += 1
                    else:
                        folders += 1
                    names.append(node.rel)
                    return
                if node.is_file:
                    return
                for child in sorted(node.children.values(),
                                    key=lambda n: (n.is_file, n.name.casefold())):
                    walk(child)

            for child in sorted(proot.children.values(),
                                key=lambda n: (n.is_file, n.name.casefold())):
                walk(child)
            return names, folders, files

        def update_summary():
            if var_use_full.get():
                summary_label.config(text=self._tr(
                    "pklz_summary_full", count=len(files_index),
                    size=format_size(sum(files_index.values()))))
                return
            count, size = current_selection_stats()
            _, folders_shown, files_shown = collapsed_view()
            summary_label.config(text=self._tr(
                "pklz_summary_selection", folders=folders_shown,
                files=files_shown, count=count, size=format_size(size)))

        def refresh_enabled():
            state = "disabled" if var_use_full.get() else "normal"
            search_entry.config(state=state)
            btn_deselect.config(state=state)
            refresh_visible_glyphs()

        action_frame = ttk.Frame(top, padding=(10, 8, 10, 10))
        action_frame.pack(fill="x")

        def deselect_all():
            selected_folders.clear()
            selected_files.clear()
            refresh_visible_glyphs()

        btn_deselect = self._add_text_widget(
            ttk.Button(action_frame, command=deselect_all), "pklz_deselect_all_btn")
        btn_deselect.pack(side="left")

        def do_save():
            use_full_val = var_use_full.get()
            if not use_full_val and not selected_folders and not selected_files:
                messagebox.showwarning(self._tr("warning_title"), self._tr("pklz_selection_required"))
                return

            display_names, display_folders, display_files = (( [], 0, 0 ) if use_full_val
                                                            else collapsed_view())

            folders_out = sorted(selected_folders) if not use_full_val else []
            files_out = sorted(selected_files) if not use_full_val else []
            count, size = (len(files_index), sum(files_index.values())) if use_full_val \
                else current_selection_stats()

            summary = {"use_full": use_full_val, "folders": display_folders,
                       "files": display_files, "count": count, "bytes": size,
                       "names": display_names[:12], "names_total": len(display_names)}
            self._save_pklz_selection(use_full_val, folders_out, files_out)
            self._save_selection_summary_part("pklz", summary)
            self._refresh_selection_summary_label()
            top.destroy()
            self._stage_pklz_selection_async(db_dir, use_full_val, folders_out, files_out)

        self._add_text_widget(ttk.Button(action_frame, command=do_save),
                              "save_btn").pack(side="right", padx=2)
        self._add_text_widget(ttk.Button(action_frame, command=top.destroy),
                              "cancel_btn").pack(side="right", padx=2)

        rebuild_tree()
        refresh_enabled()
        search_entry.focus_set()

        top.protocol("WM_DELETE_WINDOW", top.destroy)
        top.grab_set()

    def _stage_pklz_selection_async(self, db_dir, use_full, folders, files):
        """Moves .pklz files between the database and database/___TEMP to match a
        just-saved selection, on a worker thread behind a small modal progress window.

        Threaded because a selection can span tens of thousands of files; the window is
        modal because the database must not be re-selected or scanned while it is being
        rearranged. Every UI touch from the worker goes through self.after()."""
        # Planned first, on this thread, purely to decide whether a window is warranted: the
        # walk is ~2s at 30,000 files and the common case (nothing changed) shows nothing.
        files_index, staged = scan_pklz_database(db_dir)
        wanted = set() if use_full else selected_pklz_set(files_index, folders, files)
        pending = len(wanted - staged) + len(staged - wanted)
        if pending == 0:
            return

        win = ThemedToplevel(self)
        win.title(self._tr("pklz_staging_title"))
        win.transient(self)
        win.resizable(False, False)
        frame = ttk.Frame(win, padding=16)
        frame.pack(fill="both", expand=True)
        label = ttk.Label(frame, text=self._tr("pklz_staging_progress", done=0, total=pending))
        label.pack(anchor="w")
        bar = ttk.Progressbar(frame, mode="determinate", maximum=pending, length=340)
        bar.pack(fill="x", pady=(8, 0))
        win.grab_set()
        win.protocol("WM_DELETE_WINDOW", lambda: None)  # closing mid-move would orphan files

        state = {"last": 0.0}

        def on_progress(done, total):
            # Throttled: a per-file UI update across 12,000 files costs more than the moves.
            now = time.time()
            if done == total or now - state["last"] >= 0.1:
                state["last"] = now
                self.after(0, lambda d=done, t=total: (
                    bar.config(value=d),
                    label.config(text=self._tr("pklz_staging_progress", done=d, total=t))))

        def worker():
            try:
                self._apply_pklz_staging(db_dir, use_full, folders, files, progress=on_progress)
            finally:
                self.after(0, win.destroy)

        threading.Thread(target=worker, daemon=True).start()

    def _open_processed_folder(self):
        """Opens PROCESSED_DIR (assets/listsProcessed/) in Explorer. Replaces the old
        _open_processed_file, which opened the single PROCESSED.txt file directly: there are
        now two JSON files plus the PKLZ selection JSON, so a folder is the right target."""
        try:
            os.makedirs(PROCESSED_DIR, exist_ok=True)
            os.startfile(PROCESSED_DIR)
        except Exception as e:
            messagebox.showerror(self._tr("error_title"), self._tr("processed_file_open_error", error=e))

    # ------------------------------------------------------------------
    # Combined Song + PKLZ selection summary
    # ------------------------------------------------------------------

    def _load_selection_summary(self):
        data = load_json_file(SELECTION_SUMMARY_FILE, None)
        return data if isinstance(data, dict) else {}

    def _save_selection_summary_part(self, part, part_data):
        data = self._load_selection_summary()
        data["version"] = 1
        data[part] = part_data
        atomic_write_json(SELECTION_SUMMARY_FILE, data)

    def _refresh_selection_summary_label(self):
        """Updates the one-line description of the current Song and PKLZ selections
        shown beside the Select buttons on the General tab. Reads the summary saved
        at dialog-save time (assets/listsProcessed/selection-summary.json) rather than
        walking the database or the input folder, so opening the app costs nothing.
        The placeholder is shown until at least one of the two dialogs has been saved."""
        label = getattr(self, "selection_summary_label", None)
        if label is None:
            return
        data = self._load_selection_summary()
        songs = data.get("songs") if isinstance(data.get("songs"), dict) else None
        pklz = data.get("pklz") if isinstance(data.get("pklz"), dict) else None
        if songs is None and pklz is None:
            label.config(text=self._tr("selection_summary_placeholder"))
            return

        songs = songs or {}
        pklz = pklz or {}

        songs_count = songs.get("count", 0) or 0
        songs_all = bool(songs.get("all_selected", False))
        pklz_use_full = bool(pklz.get("use_full", True)) if "use_full" in pklz else True
        pklz_folders = pklz.get("folders", 0) or 0
        pklz_files = pklz.get("files", 0) or 0
        pklz_count = pklz.get("count", 0) or 0
        song_filetypes = songs.get("filetypes") or {}
        song_bytes = songs.get("bytes", 0) or 0
        pklz_bytes = pklz.get("bytes", 0) or 0

        if songs_all:
            songs_part = self._tr("selection_summary_all_songs")
        else:
            songs_part = self._tr("selection_summary_songs", count=songs_count)

        if pklz_use_full:
            pklz_part = self._tr("selection_summary_full_pklz")
        else:
            pklz_part = self._tr("selection_summary_pklz",
                                 folders=pklz_folders, files=pklz_files)

        # The bracketed breakdown only adds information when at least one side
        # is a non-trivial partial selection.
        show_brackets = (not songs_all and songs_count > 0) or (not pklz_use_full)
        bracket = ""
        if show_brackets:
            parts = []
            for ext in sorted(song_filetypes.keys()):
                parts.append(f"{song_filetypes[ext]} {ext.upper()}(s)")
            if not pklz_use_full:
                parts.append(f"{pklz_count} PKLZ(s)")
            parts.append(format_size(song_bytes + pklz_bytes))
            bracket = " [" + ", ".join(parts) + "]"

        label.config(text=f"{songs_part}, {pklz_part}{bracket}.")

    def _selection_summary_tooltip(self):
        """Hover text for the summary label. Returns a list of (text, is_bold) rows
        so the Songs: / Fingerprints: headers can be bold, or "" to suppress the
        tooltip entirely when there is nothing concrete to list."""
        data = self._load_selection_summary()
        songs = data.get("songs") if isinstance(data.get("songs"), dict) else {}
        pklz = data.get("pklz") if isinstance(data.get("pklz"), dict) else {}

        songs_all = bool(songs.get("all_selected", False))
        songs_count = songs.get("count", 0) or 0
        pklz_use_full = bool(pklz.get("use_full", True)) if "use_full" in pklz else True

        lines = []

        if not songs_all and songs_count > 0:
            lines.append((self._tr("selection_summary_songs_section"), True))
            names = songs.get("names") or []
            total = songs.get("names_total", len(names))
            for entry in names:
                if isinstance(entry, (list, tuple)) and len(entry) >= 2:
                    name, mode = entry[0], entry[1]
                else:
                    name, mode = str(entry), "both"
                if mode == "both":
                    mode_text = self._tr("selection_summary_mode_both")
                elif mode == "quick":
                    mode_text = self._tr("selection_summary_mode_quick")
                else:
                    mode_text = self._tr("selection_summary_mode_long")
                lines.append((f"{name} ({mode_text})", False))
            if total > len(names):
                lines.append((self._tr("pklz_summary_more", count=total - len(names)), False))

        if not pklz_use_full:
            lines.append((self._tr("selection_summary_fingerprints_section"), True))
            names = pklz.get("names") or []
            total = pklz.get("names_total", len(names))
            for name in names:
                lines.append((str(name), False))
            if total > len(names):
                lines.append((self._tr("pklz_summary_more", count=total - len(names)), False))

        return lines if lines else ""

# ------------------------------------------------------------------
# Add pklz / audio files
# ------------------------------------------------------------------

    def _prompt_files_or_folder(self, title_key, config_key, show_pklz_link=False, show_song_databases_btn=False):
        """
        title_key:  translation key for the dialog title.
        config_key: config.json key that stores this dialog's copy/move preference. Either
                    "add_pklz_action" (for Add PKLZ Files...) or "add_audio_action" (for Add
                    Audio Files...). This helper only reads and writes this one key; it does
                    not know or care which button opened it. The value written here is what
                    _copy_items_worker() later reads to decide whether to delete the source
                    after copying.
        show_pklz_link: whether to show the public PKLZ database link.
        show_song_databases_btn: whether to show the "Download Song Databases..." button.
        """
        result = {"choice": None}
        top = ThemedToplevel(self)
        top.title(self._tr(title_key))
        top.resizable(False, False)
        top.transient(self)

        ttk.Label(top, text=self._tr("add_files_choice_msg", title=self._tr(title_key)),
                  padding=(15, 15, 15, 5)).pack()
        btns = ttk.Frame(top, padding=(15, 5, 15, 15))
        btns.pack()

        def pick(choice):
            result["choice"] = choice
            top.destroy()

        ttk.Button(btns, text=self._tr("select_files_btn"), command=lambda: pick("files")).pack(side="left", padx=5)
        ttk.Button(btns, text=self._tr("select_folder_btn"), command=lambda: pick("folder")).pack(side="left", padx=5)
        ttk.Button(btns, text=self._tr("cancel_btn"), command=lambda: pick(None)).pack(side="left", padx=5)

        if show_pklz_link:
            def _open_pklz_databases_window():
                db_top = ThemedToplevel(top)
                db_top.title(self.gui_strings.get("public_pklz_databases_btn",
                                                  "Public PKLZ Databases..."))
                db_top.resizable(False, False)
                db_top.transient(top)

                db_btns = ttk.Frame(db_top, padding=(20, 20, 20, 20))
                db_btns.pack()

                ttk.Button(db_btns, text=self._tr("public_pklz_link"),
                           command=lambda: webbrowser.open(PUBLIC_PKLZ_DATABASE_URL)).pack(fill="x", pady=5)

                ttk.Button(db_btns, text=self._tr("public_pklz_link_alt"),
                           command=lambda: webbrowser.open(PUBLIC_PKLZ_DATABASE_URL_ALT)).pack(fill="x", pady=5)

                ttk.Button(db_btns, text=self._tr("cancel_btn"),
                           command=db_top.destroy).pack(fill="x", padx=5)

                db_top.grab_set()

            tk.Button(
                top,
                text=self.gui_strings.get("public_pklz_databases_btn", "Public PKLZ Databases..."),
                command=_open_pklz_databases_window,
                fg="#1a56db",
                activeforeground="#1a56db",
                font=("Segoe UI", 10, "bold"),
                cursor="hand2",
            ).pack(pady=(0, 15))

            fingerprint_gui_btn = tk.Button(
                top,
                text=self._tr("get_fingerprinting_gui_btn"),
                command=lambda: webbrowser.open(FINGERPRINTING_GUI_URL),
                fg="#1a56db",
                activeforeground="#1a56db",
                font=("Segoe UI", 10, "bold"),
                cursor="hand2",
            )
            fingerprint_gui_btn.pack(pady=(0, 15))

        if show_song_databases_btn:
            def _open_databases_window():
                db_top = ThemedToplevel(top)
                db_top.title(self._tr("download_song_databases_btn"))
                db_top.resizable(False, False)
                db_top.transient(top)

                db_btns = ttk.Frame(db_top, padding=(20, 20, 20, 20))
                db_btns.pack()

                ttk.Button(db_btns, text=self._tr("lostwave_italia_link"), 
                           command=lambda: webbrowser.open(LOSTWAVE_ITALIA_SONGS_URL)).pack(fill="x", pady=5)
                
                ttk.Button(db_btns, text=self._tr("french_lostwaves_link"), 
                           command=lambda: webbrowser.open(FRENCH_LOSTWAVE_SONGS_URL)).pack(fill="x", pady=5)
                
                ttk.Button(db_btns, text=self._tr("user_qlostwave_uploads_link"), 
                           command=lambda: webbrowser.open(USER_QLOSTWAVE_UPLOADS_URL)).pack(fill="x", pady=5)
                
                ttk.Button(db_btns, text=self._tr("cancel_btn"), command=db_top.destroy).pack(fill="x", padx=5)

                db_top.grab_set()

            tk.Button(
                top,
                text=self._tr("download_song_databases_btn"),
                command=_open_databases_window,
                fg="#1a56db",
                activeforeground="#1a56db",
                font=("Segoe UI", 10, "bold"),
                cursor="hand2",
            ).pack(pady=(0, 15))

        # Seed the radio group's initial state from config_data. validate_config() has already
        # guaranteed the key exists and holds "copy" or "move", so the .get() default here is a
        # belt-and-suspenders fallback rather than the primary path.
        action_var = tk.StringVar(value=self.config_data.get(config_key, "move"))

        action_frame = ttk.LabelFrame(top, padding=10)
        self._add_text_widget(action_frame, "add_files_action_label")
        action_frame.pack(padx=15, pady=(0, 15), fill="x")

        # Move first: it's the default, and reading top-to-bottom the user sees the default
        # option first.
        self._add_text_widget(
            ttk.Radiobutton(action_frame, variable=action_var, value="move"),
            "add_files_action_move",
        ).pack(anchor="w", pady=2)

        self._add_text_widget(
            ttk.Radiobutton(action_frame, variable=action_var, value="copy"),
            "add_files_action_copy",
        ).pack(anchor="w", pady=2)

        # Persist on every toggle, not on dialog close: the user can dismiss the dialog with
        # Cancel at any time, and the preference should survive that, matching how the rest of
        # the app's settings behave (auto-save on change).
        #
        # IMPORTANT: do NOT "simplify" this callback. _persist_action writes ONLY to
        # self.config_data[config_key] and then calls _save_config_to_disk(). It must NOT call
        # action_var.set(...) (that would re-fire the trace, potentially in a loop, and is not
        # needed here) and must NOT go through _schedule_flush() / _flush_now() /
        # _sync_widgets_to_config() (those paths walk long-lived widgets that do not include
        # this dialog's radio buttons, since the dialog is created and destroyed on demand).
        # The two direct writes above are the entire contract.
        def _persist_action(*_args):
            self.config_data[config_key] = action_var.get()
            self._save_config_to_disk()
        action_var.trace_add("write", _persist_action)

        top.protocol("WM_DELETE_WINDOW", lambda: pick(None))
        top.grab_set()
        top.wait_window(top)
        return result["choice"]

    def _add_files_flow(self, kind):
        if kind == "pklz":
            title_key = "add_pklz_title"
            show_pklz_link = True
            show_song_databases_btn = False
            filetypes = [("PKLZ files", "*.pklz")]
            config_key = "add_pklz_action"
        else:
            title_key = "add_audio_title"
            show_pklz_link = False
            show_song_databases_btn = True
            filetypes = [("Audio files", "*.mp3 *.wav *.flac *.m4a")]
            config_key = "add_audio_action"

        choice = self._prompt_files_or_folder(
            title_key,
            config_key,
            show_pklz_link=show_pklz_link,
            show_song_databases_btn=show_song_databases_btn
        )

        if choice is None:
            return

        items = []
        if choice == "files":
            items = list(filedialog.askopenfilenames(title=self._tr(title_key), filetypes=filetypes))
        elif choice == "folder":
            folder = filedialog.askdirectory(title=self._tr("select_folder_title"))
            if folder:
                items = [folder]

        if not items:
            return

        dest_dir = self.config_data["db_dir"] if kind == "pklz" else self.config_data["input_dir"]
        self.btn_add_pklz.configure(state="disabled")
        self.btn_add_audio.configure(state="disabled")
        threading.Thread(target=self._copy_items_worker, args=(items, dest_dir, kind), daemon=True).start()

    def _copy_items_worker(self, items, dest_dir, kind):
        error = None
        action_key = "add_pklz_action" if kind == "pklz" else "add_audio_action"
        action = self.config_data.get(action_key, "move")
        try:
            os.makedirs(dest_dir, exist_ok=True)
            dest_label = "database" if kind == "pklz" else "input"
            create_hashes = (kind == "pklz"
                            and self.config_data.get("create_pklz_hash_tables_on_load_val", False))
            for item in items:
                name = os.path.basename(item.rstrip("\\/"))
                if action == "move":
                    self._log(self._tr("move_start", name=name, dest=dest_label))
                else:
                    self._log(self._tr("copy_start", name=name, dest=dest_label))

                copy_ok = False
                try:
                    if os.path.isdir(item):
                        shutil.copytree(item, os.path.join(dest_dir, name), dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, os.path.join(dest_dir, name))
                    copy_ok = True
                except Exception as e:
                    if action == "move":
                        self._log(self._tr("move_copy_error", name=name, error=e))
                    else:
                        self._log(self._tr("copy_error", name=name, error=e))

                if not copy_ok:
                    continue

                # The hash-table listing step reads the SOURCE path, so it must run before any
                # delete below (move mode deletes the source once it's done).
                if create_hashes:
                    if os.path.isdir(item):
                        self._write_hash_table_listings_for_folder(item, name)
                    else:
                        self._write_hash_table_listing_for_file(item)

                if action == "move":
                    if self._is_safe_to_delete_source(item, dest_dir):
                        try:
                            if os.path.isdir(item):
                                shutil.rmtree(item)
                            else:
                                os.remove(item)
                        except Exception as e:
                            self._log(self._tr("move_delete_error", name=name, error=e))
                    else:
                        self._log(self._tr("move_delete_skipped", name=name))
                    # Phrased as "Added", not "Moved": the delete half above can be
                    # independently skipped or fail, and "Added" reads correctly either way,
                    # instead of contradicting a following move_delete_skipped/move_delete_error
                    # line ("Moved 'foo' ... but didn't delete 'foo'" would read as a bug).
                    self._log(self._tr("move_success", name=name))
                else:
                    self._log(self._tr("copy_success", name=name))
        except Exception as e:
            error = str(e)
        self.after(0, self._on_copy_finished, error, action)

    def _on_copy_finished(self, error=None, action="copy"):
        self.btn_add_pklz.configure(state="normal")
        self.btn_add_audio.configure(state="normal")
        if error:
            messagebox.showerror(self._tr("copy_failed_title"), error)
        elif action == "move":
            messagebox.showinfo(self._tr("copy_finished_title"), self._tr("move_finished_msg"))
        else:
            messagebox.showinfo(self._tr("copy_finished_title"), self._tr("copy_finished_msg"))

    @staticmethod
    def _is_safe_to_delete_source(src, dest_dir):
        """Returns True only if it is safe to delete `src` after having copied it into
        `dest_dir`. Two dangerous configurations must be refused:

          (1) `src` is the same as, or lives inside, `dest_dir`. Deleting it would remove the
              freshly-copied data (or the destination folder itself).

          (2) `dest_dir` lives inside `src`. Deleting `src` would recursively wipe out the
              destination along with everything else.

        The comparisons are done on os.path.abspath-normalized paths, anchored with a trailing
        separator on the "container" side so that e.g. C:\\data\\input is not mistaken for a
        prefix of C:\\data\\input_backup.

        Both sides are additionally passed through os.path.normcase, because on Windows
        filesystem paths are case-insensitive: C:\\Users\\me\\Input and c:\\users\\me\\input are
        the same folder, but os.path.abspath does not normalize case, so a case-only difference
        would otherwise slip past the equality and prefix checks below. normcase is a no-op on
        POSIX, so this is safe to apply unconditionally.

        Symlinks are not resolved via os.path.realpath(). On Windows this is a non-issue, and
        on POSIX a source that is a symlink into the destination can still be deleted safely
        (deleting the symlink itself does not touch the target). If this ever needs to run on
        POSIX with realpath semantics, add realpath() on both sides before comparing."""
        src_abs = os.path.normcase(os.path.abspath(src))
        dst_abs = os.path.normcase(os.path.abspath(dest_dir))
        if src_abs == dst_abs:
            return False
        src_with_sep = src_abs + os.sep
        dst_with_sep = dst_abs + os.sep
        if src_with_sep.startswith(dst_with_sep):
            return False
        if dst_with_sep.startswith(src_with_sep):
            return False
        return True

    # ------------------------------------------------------------------
    # Hash table creation (create_pklz_hash_tables_on_load_val)
    # ------------------------------------------------------------------

    def _write_hash_table_listing_for_file(self, pklz_path):
        base_name = os.path.splitext(os.path.basename(pklz_path))[0]
        hash_tables_dir = self.config_data.get("hash_tables_dir", DEFAULT_HASH_TABLES_DIR)
        output_path = os.path.join(hash_tables_dir, f"{base_name}_hash_table.txt")
        self._write_hash_table_listing(pklz_path, output_path)

    def _write_hash_table_listings_for_folder(self, folder_path, top_name):
        hash_tables_dir = self.config_data.get("hash_tables_dir", DEFAULT_HASH_TABLES_DIR)
        for root, dirs, files in os.walk(folder_path):
            dirs.sort()
            files.sort()
            for file in files:
                if not file.lower().endswith(".pklz"):
                    continue
                full_path = os.path.join(root, file)
                rel = os.path.relpath(root, folder_path)
                if rel == ".":
                    out_dir = os.path.join(hash_tables_dir, top_name)
                else:
                    out_dir = os.path.join(hash_tables_dir, top_name, rel)
                base_name = os.path.splitext(file)[0]
                output_path = os.path.join(out_dir, f"{base_name}_hash_table.txt")
                self._write_hash_table_listing(full_path, output_path)

    def _write_hash_table_listing(self, pklz_path, output_path):
        """Loads a source .pklz file with audfprint's own HashTable and writes a plain-text
        listing of its contents (all the audio files it contains, and how many hashes each
        one contributed). Runs on the background worker thread started by _copy_items_worker,
        so any failure is logged (never raised)."""
        self._log(self._tr("log_hash_table_listing_writing", file=os.path.basename(pklz_path)))
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # IMPORTANT: audfprint's own modules use BARE imports internally (see audfprint.py's
            # `import hash_table`, `import audfprint_analyze`, `import stft`, `import audio_read`)
            # and are meant to be run with the audfprint folder itself on sys.path. This matters
            # for two independent reasons:
            #   1) Loading hash_table.py as a top-level module (rather than as the package
            #      submodule "audfprint.hash_table") matches how audfprint.py itself does it.
            #   2) The .pklz files on disk were serialized by a script that ran that way, so
            #      pickle stores the class as "hash_table.HashTable" (bare). If only
            #      registered "audfprint.hash_table" was registered, unpickling would fail with
            #      "No module named 'hash_table'" even though the module is physically present.
            audfprint_libs_dir = os.path.join(ASSETS_FOLDER, "libs", "audfprint")
            if audfprint_libs_dir not in sys.path:
                sys.path.insert(0, audfprint_libs_dir)

            hash_table_module = importlib.import_module("hash_table")
            HashTable = hash_table_module.HashTable

            # Compatibility shim: .pklz files created with numpy 2.x store class
            # references under "numpy._core.*", but numpy 1.x only exposes "numpy.core.*".
            # Aliasing the 2.x paths to the 1.x equivalents in sys.modules before
            # unpickling lets an old numpy installation load newer pickles.
            # (numpy >= 2.0 already aliases "numpy.core" -> "numpy._core", so this is a
            # no-op there and the reverse direction just keeps working.)
            import numpy as _np
            if not hasattr(_np, "_core"):
                _aliases = {
                    "numpy._core": _np.core,
                    "numpy._core.multiarray": _np.core.multiarray,
                    "numpy._core.umath": _np.core.umath,
                    "numpy._core._multiarray_umath": _np.core._multiarray_umath,
                    "numpy._core.numerictypes": _np.core.numerictypes,
                }
                for _alias, _target in _aliases.items():
                    sys.modules.setdefault(_alias, _target)

            # Captures audfprint's own stdout for the duration of these two calls:
            #   - HashTable(filename=...) prints a "Read fprints for ..." summary line
            #   - HashTable.list()       prints one "<name> (<N> hashes)" line per contained file
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                hashtable = HashTable(filename=pklz_path)
                hashtable.list()

            with open(output_path, "w", encoding="utf-8", newline="\n") as f:
                f.write(buf.getvalue())

            self._log(self._tr("log_hash_table_listing_written", file=output_path))
        except Exception as e:
            self._log(self._tr("log_hash_table_listing_error",
                            file=os.path.basename(pklz_path), error=e))

    # ------------------------------------------------------------------
    # Processed files
    # ------------------------------------------------------------------

    def _save_console_log(self):
        """Dumps the current console widget's visible text to a timestamped file inside
        the configured console_logs_dir, then informs the user where it went."""
        console_logs_dir = (self.dir_vars["console_logs_dir"].get().strip()
                            if "console_logs_dir" in self.dir_vars
                            else self.config_data.get("console_logs_dir", DEFAULT_CONSOLE_LOGS_DIR))
        try:
            os.makedirs(console_logs_dir, exist_ok=True)
        except Exception as e:
            messagebox.showerror(self._tr("error_title"),
                                self._tr("console_log_save_error", error=e))
            return

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}_v{APP_VERSION}_WZSGUI_CLog.txt"
        filepath = os.path.join(console_logs_dir, filename)

        try:
            content = self.console.get("1.0", "end-1c")
            with open(filepath, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
        except Exception as e:
            messagebox.showerror(self._tr("error_title"),
                                self._tr("console_log_save_error", error=e))
            return

        messagebox.showinfo(self._tr("info_title"),
                            self._tr("console_log_saved_msg", path=filepath))

    def _open_crash_logs_file(self):
        """Opens WerZatSonGUI's own crash_logs.txt (the Tee'd stdout/stderr dump from
        startup). Completely independent from the console logs."""
        try:
            if not os.path.exists(CRASH_LOG_FILE):
                os.makedirs(os.path.dirname(CRASH_LOG_FILE), exist_ok=True)
                open(CRASH_LOG_FILE, "w", encoding="utf-8").close()
            os.startfile(CRASH_LOG_FILE)
        except Exception as e:
            messagebox.showerror(self._tr("error_title"),
                                self._tr("crash_log_open_error", error=e))

    def _save_force_stop_console_log(self):
        """Saves a snapshot of the current console contents to a specially-named
        'FORCE_STOP' log file, then writes a small marker file so the freshly
        relaunched instance can tell the user about it on startup (see
        _check_pending_force_stop_log). Returns the log path, or None on failure."""
        console_logs_dir = (self.dir_vars["console_logs_dir"].get().strip()
                            if "console_logs_dir" in self.dir_vars
                            else self.config_data.get("console_logs_dir", DEFAULT_CONSOLE_LOGS_DIR))
        try:
            os.makedirs(console_logs_dir, exist_ok=True)
        except Exception:
            return None

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{timestamp}_v{APP_VERSION}_FORCE_STOP_CLog.txt"
        filepath = os.path.join(console_logs_dir, filename)
        try:
            content = self.console.get("1.0", "end-1c")
            with open(filepath, "w", encoding="utf-8", newline="\n") as f:
                f.write(content)
        except Exception:
            return None

        try:
            with open(FORCE_STOP_LOG_MARKER_FILE, "w", encoding="utf-8") as f:
                json.dump({"log_path": filepath}, f)
        except Exception:
            pass
        return filepath

    def _check_pending_force_stop_log(self):
        """Called shortly after normal (case 2) boot. If the previous instance left a
        marker file announcing a force-stop console log, tells the user about it and
        clears the marker so the alert only appears once."""
        if not os.path.exists(FORCE_STOP_LOG_MARKER_FILE):
            return
        log_path = None
        try:
            with open(FORCE_STOP_LOG_MARKER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict):
                log_path = data.get("log_path")
        except Exception:
            pass
        try:
            os.remove(FORCE_STOP_LOG_MARKER_FILE)
        except Exception:
            pass
        if log_path and os.path.exists(log_path):
            messagebox.showinfo(
                self._tr("force_stop_log_saved_title"),
                self._tr("force_stop_log_saved_msg", path=log_path)
            )

    # ------------------------------------------------------------------
    # Start WerZatSong (ported temp/werzatsongrunner.py pipeline)
    # ------------------------------------------------------------------

    def _set_container_enabled(self, container, enabled):
        """Recursively enables/disables every interactive widget inside `container`. Used to
        grey out Directories / Search Modes / Advanced Settings while a scan is running.
        Tab switching itself is left alone: only the controls inside each tab are toggled."""
        state = "normal" if enabled else "disabled"
        ttk_state = ["!disabled"] if enabled else ["disabled"]
        for widget in container.winfo_children():
            classname = widget.winfo_class()
            if classname in ("TEntry", "TCheckbutton", "TButton", "TCombobox", "TSpinbox", "TRadiobutton"):
                try:
                    widget.state(ttk_state)
                except tk.TclError:
                    pass
            elif classname in ("Entry", "Button", "Checkbutton", "Spinbox", "Radiobutton"):
                try:
                    widget.configure(state=state)
                except tk.TclError:
                    pass
            self._set_container_enabled(widget, enabled)

    def _re_enable_logs_tab(self):
        """The Logs tab's controls (save console log, open crash logs, and the
        console_logs_dir picker) have to stay usable even while a scan is running,
        so this re-enablse just that subtree after _set_container_enabled has greyed
        out the rest of the Advanced notebook. The console widget itself lives
        outside the notebook and is already never disabled."""
        frame = getattr(self, "_logs_tab_frame", None)
        if frame is not None and frame.winfo_exists():
            self._set_container_enabled(frame, True)

    def _on_start_clicked(self):
        if self.is_running:
            return
        if not any([self.var_mode_mb.get(), self.var_mode_audiotag.get(),
                    self.var_mode_shazam.get(), self.var_mode_audfprint.get()]):
            messagebox.showwarning(self._tr("no_mode_selected"), self._tr("no_mode_selected_msg"))
            return

        try:
            self._sync_env_from_disk_force()
        except Exception as e:
            import traceback
            messagebox.showerror("Error in _sync_env_from_disk_force", traceback.format_exc())
            return

        try:
            self._flush_immediately()
        except Exception as e:
            import traceback
            messagebox.showerror("Error in _flush_immediately", traceback.format_exc())
            return

        # input_dir mismatch check, on the main thread, before the background worker starts: a
        # Tk messagebox must never be constructed off the main thread, and this is the one
        # place in the whole start flow that still runs on it. _orchestrate_pipeline (which
        # runs on the background worker) will call _load_processed_songs again later for the
        # actual scan, which is fine: that call only reads and logs, it never pops a dialog.
        # This prompt fires at most once per session per mode, tracked in
        # self._mismatch_prompted; the read-time [WARNING] log line, by contrast, is emitted by
        # _load_processed_songs on every single call, mismatched or not.
        for mode in ("quick", "long"):
            _processed, mismatch = self._load_processed_songs(mode)
            if not mismatch:
                self._processed_json_writable[mode] = True
                continue
            if mode in self._mismatch_prompted:
                continue
            self._mismatch_prompted.add(mode)
            path = self._processed_songs_path(mode)
            existing = load_json_file(path, {})
            old_dir = existing.get("input_dir", "") if isinstance(existing, dict) else ""
            new_dir = self.config_data.get("input_dir", DEFAULT_INPUT_DIR)
            reset = messagebox.askyesno(
                self._tr("input_dir_mismatch_prompt_title"),
                self._tr("input_dir_mismatch_prompt_msg", old=old_dir, new=new_dir),
            )
            if reset:
                existing_processed = existing.get("processed", []) if isinstance(existing, dict) else []
                if not isinstance(existing_processed, list):
                    existing_processed = []
                data = {"version": 1, "mode": mode, "input_dir": new_dir, "processed": existing_processed}
                atomic_write_json(path, data)
                self._processed_json_writable[mode] = True
            else:
                self._log(self._tr("log_input_dir_mismatch_kept", mode=mode))
                self._processed_json_writable[mode] = False

        self.is_running = True
        self.btn_start.configure(state="disabled")
        self.btn_add_pklz.configure(state="disabled")
        self.btn_add_audio.configure(state="disabled")
        self.btn_force_stop.configure(state="normal")
        self._set_container_enabled(self._directories_frame, False)
        self._set_container_enabled(self._search_modes_frame, False)
        self._set_container_enabled(self._advanced_notebook, False)
        self._re_enable_logs_tab()
        self._log("=" * 60)
        self._log(self._tr("log_starting"))
        self._log("=" * 60)
        threading.Thread(target=self._pipeline_worker, daemon=True).start()

    def _pipeline_worker(self):
        error = None
        try:
            self._orchestrate_pipeline()
        except PipelineAbort as e:
            self._log(self._tr("log_pipeline_abort", error=str(e)))
        except Exception as e:
            error = str(e)
            self._log(self._tr("log_unexpected_error", error=e))
        self.after(0, self._on_pipeline_finished, error)

    def _on_pipeline_finished(self, error=None):
        self.is_running = False
        self.btn_start.configure(state="normal")
        self.btn_add_pklz.configure(state="normal")
        self.btn_add_audio.configure(state="normal")
        self.btn_force_stop.configure(state="disabled")
        self._set_container_enabled(self._directories_frame, True)
        self._set_container_enabled(self._search_modes_frame, True)
        self._set_container_enabled(self._advanced_notebook, True)
        if self.pending_env:
            self._write_env_now()
        if error:
            messagebox.showerror(self._tr("pipeline_error_title"), self._tr("pipeline_error_msg", error=error))

    def _on_force_stop_clicked(self):
        if not self.is_running:
            return
        if not messagebox.askyesno(self._tr("force_stop_confirm_title"), self._tr("force_stop_confirm_msg")):
            return

        self._save_force_stop_console_log()
        self.btn_force_stop.configure(state="disabled")
        self._log(self._tr("log_force_stop"))
        threading.Thread(target=self._force_stop_worker, daemon=True).start()

    def _force_stop_worker(self):
        """Treats Force Stop exactly like the user force-closing WerZatSonGUI and reopening
        it: kill everything this run spawned, clean up whatever was left half-done, then
        relaunch. Runs in the background since killing/cleanup can take a moment: always
        ends in an attempted relaunch even if a cleanup step fails."""
        try:
            _kill_all_tracked_processes()
            try:
                input_dir = self.config_data.get("input_dir", DEFAULT_INPUT_DIR)
                force_clean_directory(INTERNAL_INPUT_FOLDER, recreate=False)
                force_clean_directory(INTERNAL_TEMP_FOLDER, recreate=False)
                force_clean_directory(os.path.join(input_dir, TEMP_STAGING_DIRNAME), recreate=False)
            except Exception:
                pass
        finally:
            self.after(0, self._relaunch_self)

    def _orchestrate_pipeline(self):
        """Replaces the old single-pass _run_pipeline body. Runs Quick and/or Long mode, once
        per selected PKLZ target, deferring every processed-songs commit until all targets for
        that mode have been attempted, so a song is only ever marked processed once every
        selected PKLZ target has actually had a chance at it (see _run_pipeline's
        commit_processed docstring). Always runs on the background worker thread
        (_pipeline_worker); the input_dir-mismatch prompt itself has already happened on the
        main thread, in _on_start_clicked, before this was ever called, and its outcome is
        already recorded in self._processed_json_writable."""
        config = self.config_data
        input_dir = config.get("input_dir", DEFAULT_INPUT_DIR)

        if not any([config.get("mode_musicbrainz"), config.get("mode_audiotag"),
                    config.get("mode_shazam"), config.get("mode_audfprint")]):
            raise PipelineAbort(self._tr("no_mode_selected_msg"))

        if not os.path.exists(input_dir):
            raise PipelineAbort(self._tr("input_dir_not_found", dir=input_dir))

        force_clean_directory(INTERNAL_INPUT_FOLDER, recreate=True)

        # The non-MP3-to-MP3 conversion (and its processed-JSON extension rewrite) must run,
        # and finish, BEFORE the Quick/Long processed sets are loaded below: a file renamed
        # song.wav -> song.mp3 here also has its processed-JSON entry rewritten in place (see
        # _rewrite_processed_json_extensions), and if the processed sets were loaded first,
        # that rewrite would land after the fact and the freshly-renamed song would look "never
        # processed" on every single run despite having already been completed under its old
        # extension. This ordering also matches the pre-rework code, which always converted
        # before ever reading the (then-single) PROCESSED.txt. Runs once per orchestration, not
        # once per PKLZ target per mode, so it does not walk input_dir N times over for no
        # reason.
        self._convert_non_mp3_files_to_mp3(input_dir)

        all_files = set()
        for root, dirs, files in os.walk(input_dir):
            if TEMP_STAGING_DIRNAME in dirs:
                dirs.remove(TEMP_STAGING_DIRNAME)
            dirs.sort()
            files.sort()
            for file in files:
                if os.path.splitext(file)[1].lower() in AUDIO_EXTENSIONS:
                    full_path = os.path.join(root, file)
                    all_files.add(os.path.relpath(full_path, input_dir))

        if not all_files:
            raise PipelineAbort(self._tr("no_audio_files", dir=input_dir))

        quick_processed, _ = self._load_processed_songs("quick")
        long_processed, _ = self._load_processed_songs("long")

        pending_quick = all_files - quick_processed
        pending_long = all_files - long_processed
        # quick_only: pending Quick, and either already done in Long or excluded from it.
        quick_only = pending_quick - pending_long
        # both_pending: pending in both modes at once.
        both_pending = pending_quick & pending_long

        scan_mode = config.get("scan_mode", "quick")
        if scan_mode == "quick":
            # Quick-only: process every pending Quick song, including ones also pending Long.
            # Long doesn't run this session, so its JSON is left untouched: a later "long" or
            # "both" session will still see those songs as pending Long.
            quick_batch = set(pending_quick)
            long_batch = set()
            include_original_ids = set()
        elif scan_mode == "long":
            # Long-only: process every pending Long song. both_pending songs have never had
            # their original scanned against this session's PKLZ target(s), so their original
            # is folded into the Long batch via include_original_ids.
            quick_batch = set()
            long_batch = set(pending_long)
            include_original_ids = set(both_pending)
        else:  # "both"
            # Both: Quick handles songs pending Quick but not Long. Songs pending both are
            # handled entirely inside the Long batch (original plus variations), so they never
            # enter the Quick loop and are never scanned twice.
            quick_batch = set(quick_only)
            long_batch = set(pending_long)
            include_original_ids = set(both_pending)

        if not quick_batch and not long_batch:
            raise PipelineAbort(self._tr("no_pending_songs_msg"))

        if config.get("mode_audfprint"):
            use_full, folders, files, _db_mismatch = self._load_pklz_selection()
            if not use_full and not folders and not files:
                raise PipelineAbort(self._tr("pklz_selection_required"))
            # Staging is re-applied at the start of every scan, not only when the dialog
            # saves: files added or hand-moved since, or a move interrupted mid-way, would
            # otherwise leave ___TEMP disagreeing with the saved selection and Audfprint
            # searching something other than what the user picked.
            db_dir = config.get("db_dir", DEFAULT_DB_DIR)
            staged_count = self._apply_pklz_staging(db_dir, use_full, folders, files)
            if use_full:
                pklz_targets = [""]
            else:
                if staged_count == 0:
                    raise PipelineAbort(self._tr("pklz_selection_empty_on_disk"))
                self._log(self._tr("log_pklz_target_staged", dir=pklz_staging_dir(db_dir),
                                    count=staged_count))
                # A single target whatever was selected: gathering the selection into one
                # folder is exactly what makes the old one-run-per-subfolder loop (and its
                # regenerate-every-variation-per-target cost) unnecessary.
                pklz_targets = [TEMP_STAGING_DIRNAME]
        else:
            # Audfprint disabled: a single "no-op" target, so the mode loop below still runs
            # exactly once per mode instead of needing a separate no-PKLZ code path.
            pklz_targets = [""]

        if len(pklz_targets) > 1 and scan_mode in ("long", "both") and long_batch:
            self._log(self._tr("log_long_mode_multi_target_warning", count=len(pklz_targets)))

        orig_mb = config.get("mode_musicbrainz")
        orig_at = config.get("mode_audiotag")
        orig_sz = config.get("mode_shazam")
        orig_suppress = self._suppress_config_saves
        # Held for the whole run: the per-target mode toggles and PKLZ folder override that
        # _run_pipeline flips into config_data are runtime-only and must never reach
        # config.json. See _save_config_to_disk.
        self._suppress_config_saves = True
        try:
            self._log(self._tr("log_found_files", count=len(all_files), mode=scan_mode.upper()))

            for mode in ("quick", "long"):
                mode_pending = quick_batch if mode == "quick" else long_batch
                if not mode_pending:
                    continue

                # additional_modes_done lives inside this loop iteration, not outside it, so
                # Quick and Long each get their own independent additional-modes pass: under
                # "both" they process disjoint song sets and each needs its own coverage.
                additional_modes_done = False
                completed_sets = []

                for pklz_target in pklz_targets:
                    folder_arg = "" if pklz_target == "" else pklz_target
                    run_additional_here = not additional_modes_done

                    completed = self._run_pipeline(
                        pending_files=mode_pending,
                        mode=mode,
                        additional_modes=run_additional_here,
                        pklz_folder_arg=folder_arg,
                        commit_processed=False,
                        include_original_ids=(include_original_ids if mode == "long" else None),
                    )
                    completed_sets.append(completed)

                    if run_additional_here and completed:
                        # First-successful-target rule (see the module notes on additional
                        # modes): the target's completed set only counts as "successful" here,
                        # so a target that loaded PKLZ files but crashed mid-scan does not
                        # falsely claim the additional-modes pass. The next target gets a
                        # chance instead.
                        additional_modes_done = True
                        if len(completed) < len(mode_pending):
                            # Known limitation: this is a per-target rule, not a per-song one.
                            # A target can succeed for some songs and fail for others; the
                            # failed songs get Audfprint coverage from later targets, but no
                            # additional-modes coverage until a later SESSION happens to pick
                            # them up on its own first successful target. This warning is the
                            # visible symptom of that gap.
                            self._log(self._tr(
                                "log_additional_modes_partial",
                                completed=len(completed),
                                total=len(mode_pending),
                                remaining=len(mode_pending) - len(completed),
                            ))

                final_completed = set.intersection(*completed_sets) if completed_sets else set()

                # This summary line is deliberately unconditional and always visible (not
                # gated behind a debug flag): it is the one place in the whole run that states,
                # in plain language, how many songs actually got marked done in this mode and
                # whether the write was even attempted. Without it, a silently-skipped write
                # (the "keep old file" branch of the input_dir mismatch prompt, or a mismatch
                # that was never prompted for because it was already recorded from an earlier
                # session) leaves no visible trace anywhere in the console, and the only symptom
                # is "songs I just scanned still show up as pending" the next time Select
                # Songs... is opened. See log_input_dir_mismatch_kept / log_input_dir_mismatch_write
                # for the matching root-cause lines this summary is meant to be read alongside.
                if self._processed_json_writable.get(mode, True):
                    existing_processed, _ = self._load_processed_songs(mode)
                    new_processed = existing_processed | final_completed
                    self._save_processed_songs(mode, new_processed)
                    self._log(self._tr("log_marked_processed", mode=mode, count=len(final_completed)))
                else:
                    self._log(self._tr("log_marked_processed_skipped", mode=mode, count=len(final_completed)))

                if mode == "long":
                    # A both-pending song's original was scanned as part of its Long batch
                    # entry (see include_original_ids / _generate_variations_into_pool): once
                    # it completes here, it is also Quick-done, so mark it in the Quick JSON at
                    # the same moment. Under scan_mode == "quick" this branch never runs
                    # (mode_pending for "long" is empty), so the Quick-only session correctly
                    # leaves the Long JSON untouched.
                    newly_quick_done = final_completed & include_original_ids
                    if newly_quick_done:
                        if self._processed_json_writable.get("quick", True):
                            existing_quick, _ = self._load_processed_songs("quick")
                            new_quick = existing_quick | newly_quick_done
                            self._save_processed_songs("quick", new_quick)
                            self._log(self._tr("log_marked_processed", mode="quick",
                                                count=len(newly_quick_done)))
                        else:
                            self._log(self._tr("log_marked_processed_skipped", mode="quick",
                                                count=len(newly_quick_done)))

            self._log("")
            self._log(self._tr("log_all_tasks_complete"))
        finally:
            config["mode_musicbrainz"] = orig_mb
            config["mode_audiotag"] = orig_at
            config["mode_shazam"] = orig_sz
            self._recompute_command()
            self._suppress_config_saves = orig_suppress

    def _run_pipeline(self, pending_files, mode, additional_modes=True, pklz_folder_arg="",
                      commit_processed=False, include_original_ids=None):
        """
        pending_files: the set of file IDs this pass should attempt. The orchestrator has
                       already walked input_dir, computed the mode's pending set, applied the
                       scan_mode filter, and done the include-original bookkeeping;
                       _run_pipeline does not re-walk input_dir.
        mode: "quick" or "long".
        additional_modes: whether MusicBrainz/AudioTag/Shazam should run on this pass.
        pklz_folder_arg: "" for full database, "<name>" for a specific subfolder.
        commit_processed: if True, _run_pipeline merges its returned completed set into the
                          on-disk processed JSON itself before returning. If False, the caller
                          is responsible for doing so, after all PKLZ targets have been
                          attempted. Defaults to False because the orchestrator is the only
                          real caller and it always defers; the True path is kept for
                          potential single-shot callers and for debugging.
        include_original_ids: only meaningful for mode == "long". The set of file IDs whose
                          Long-batch pool entry must also include the original unmodified audio
                          alongside its tempo/pitch variations. The orchestrator computes this
                          from scan_mode and the pending sets. None is treated as "empty set" so
                          quick-mode callers can omit it.

        Note on sys_temp_dir: because the orchestrator calls _run_pipeline once per PKLZ target
        per mode, a sys_temp_dir created inside _run_pipeline is created and destroyed once per
        target, matching the original code's per-call lifetime but now with one call per
        target. This is deliberate: it keeps all tempfile lifetimes scoped to a single target's
        work, so a failure mid-target cannot leak a system-temp directory into the next
        target's run, and it mirrors the original single-call behavior exactly. The cost is a
        mkdtemp/rmtree pair per target, which is negligible compared to the ffmpeg work done in
        that target.
        """
        orig_mb = self.config_data.get("mode_musicbrainz")
        orig_at = self.config_data.get("mode_audiotag")
        orig_sz = self.config_data.get("mode_shazam")
        orig_folder = self._runtime_pklz_folder

        # Additional-modes toggling and the PKLZ folder override both go through config_data
        # directly, not the tk.BooleanVars: compute_werzatsong_cmd() reads from config_data,
        # and _sync_widgets_to_config() (the only bridge from the GUI vars to config_data) is
        # not on this code path. Flipping the BooleanVars here would silently have no effect on
        # the command that actually runs.
        if not additional_modes:
            self.config_data["mode_musicbrainz"] = False
            self.config_data["mode_audiotag"] = False
            self.config_data["mode_shazam"] = False
        self._runtime_pklz_folder = pklz_folder_arg
        self._recompute_command()
        try:
            # sys_temp_dir is created and destroyed inside this call, so it lives for exactly
            # one PKLZ target's worth of work. See the docstring above for why this matches the
            # original behavior despite being called N times now.
            sys_temp_dir = tempfile.mkdtemp()
            try:
                input_dir = self.config_data.get("input_dir", DEFAULT_INPUT_DIR)
                temp_dir_path = os.path.join(input_dir, TEMP_STAGING_DIRNAME)
                processed_set, _mismatch = self._load_processed_songs(mode)
                if mode == "quick":
                    completed = self._run_quick_mode(pending_files, processed_set, temp_dir_path)
                else:
                    completed = self._run_long_mode(pending_files, processed_set, temp_dir_path,
                                                    sys_temp_dir, pklz_folder_arg,
                                                    include_original_ids or set())
                if commit_processed:
                    self._save_processed_songs(mode, processed_set | completed)
                return completed
            finally:
                force_clean_directory(sys_temp_dir, recreate=False)
        finally:
            self.config_data["mode_musicbrainz"] = orig_mb
            self.config_data["mode_audiotag"] = orig_at
            self.config_data["mode_shazam"] = orig_sz
            self._runtime_pklz_folder = orig_folder
            self._recompute_command()

    def _convert_non_mp3_files_to_mp3(self, input_dir):
        """Converts every non-mp3 audio file under input_dir to the highest-quality mp3
        ffmpeg can produce, replacing the original, and fixes up any processed-songs JSON
        entry that referenced the old path/extension so it keeps pointing at the right file
        (see _rewrite_processed_json_extensions). The conversion is atomic per file (encodes
        to a temp file, then renames, then deletes the original only on success), so an
        interrupted/force-stopped run never leaves a half-converted pair behind: the original
        stays untouched and any leftover temp file is cleaned up and retried on the next run."""
        if shutil.which("ffmpeg") is None:
            return  # let the rest of the pipeline surface the missing-ffmpeg error normally

        to_convert = []
        for root, dirs, files in os.walk(input_dir):
            if TEMP_STAGING_DIRNAME in dirs:
                dirs.remove(TEMP_STAGING_DIRNAME)
            dirs.sort()
            files.sort()
            for file in files:
                full_path = os.path.join(root, file)
                if file.endswith(CONVERTING_TMP_SUFFIX):
                    # Leftover from a previously-interrupted conversion: always safe to drop.
                    try:
                        os.remove(full_path)
                    except Exception:
                        pass
                    continue
                if os.path.splitext(file)[1].lower() in NON_MP3_AUDIO_EXTENSIONS:
                    to_convert.append(full_path)

        if not to_convert:
            return

        self._log(self._tr("log_convert_start", count=len(to_convert)))
        renamed = {}
        converted = 0
        for full_path in to_convert:
            old_rel = os.path.relpath(full_path, input_dir)
            base_path = os.path.splitext(full_path)[0]
            final_path = f"{base_path}.mp3"

            if os.path.exists(final_path):
                self._log(self._tr("log_convert_skip_exists", file=old_rel))
                continue

            temp_path = f"{full_path}{CONVERTING_TMP_SUFFIX}"
            self._log(self._tr("log_converting_to_mp3", file=old_rel))
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                # -f mp3 forces the output container/muxer explicitly: ffmpeg otherwise infers
                # it from temp_path's extension, which is ".converting.tmp", not a recognized
                # container: without this flag every single conversion fails immediately.
                cmd = ["ffmpeg", "-y", "-i", full_path, "-codec:a", "libmp3lame", "-qscale:a", "0",
                       "-f", "mp3", temp_path]
                run_tracked(cmd)
                os.replace(temp_path, final_path)
                os.remove(full_path)
                renamed[old_rel] = os.path.relpath(final_path, input_dir)
                converted += 1
            except Exception as e:
                self._log(self._tr("log_convert_error", file=old_rel, error=format_subprocess_error(e)))
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass

        if renamed:
            self._rewrite_processed_json_extensions(renamed)
        if converted:
            self._log(self._tr("log_convert_done", count=converted))

    def _rewrite_processed_json_extensions(self, renamed):
        """renamed: old relative path -> new relative path (same folder, .mp3 extension).
        Rewrites the "processed" array inside both mode JSONs so any entry that referenced an
        old (pre-conversion) path now points at the converted file instead. Respects the same
        input_dir mismatch guard as _save_processed_songs (via
        _processed_json_input_dir_mismatch): if a JSON's stored input_dir does not match the
        current one, the rewrite is skipped for that file and a [WARNING]-tagged line is
        logged, so a run under a mismatched input_dir can never corrupt a JSON whose paths
        refer to a different folder. The renamed files will simply be re-scanned on the next
        run under the correct input directory."""
        if not renamed:
            return
        current_input_dir = self.config_data.get("input_dir", DEFAULT_INPUT_DIR)
        for mode in ("quick", "long"):
            path = self._processed_songs_path(mode)
            mismatch, stored_input_dir = self._processed_json_input_dir_mismatch(path)
            if mismatch:
                self._log(self._tr("log_rewrite_extensions_skipped", file=path,
                                    old_dir=stored_input_dir, new_dir=current_input_dir))
                continue
            data = load_json_file(path, None)
            if not isinstance(data, dict):
                continue
            processed_list = data.get("processed")
            if not isinstance(processed_list, list):
                continue
            changed = False
            new_list = []
            for entry in processed_list:
                if entry in renamed:
                    new_list.append(renamed[entry])
                    changed = True
                else:
                    new_list.append(entry)
            if changed:
                data["processed"] = new_list
                data["input_dir"] = current_input_dir
                atomic_write_json(path, data)

    def _run_long_mode(self, all_targets, processed_set, temp_dir_path, sys_temp_dir,
                       pklz_folder_arg="", include_original_ids=None):
        """all_targets: relative-path IDs already selected by the orchestrator for this Long
        pass (scan_mode filtered, this PKLZ target's turn). processed_set: the mode's on-disk
        processed set, re-checked here defensively (a file already in it is skipped even if
        the caller's set math somehow included it), though the primary filtering now happens
        in _orchestrate_pipeline. pklz_folder_arg is not used directly here (it is already
        baked into WERZATSONG_CMD via the _runtime_pklz_folder mechanism in _run_pipeline); it
        is accepted for symmetry with the rest of the pipeline and to make the per-target
        nature of the call explicit at the call site. include_original_ids is the set of file
        IDs whose Long-batch pool entry must also include the original, unmodified audio file
        alongside its tempo/pitch variations (see _generate_variations_into_pool's
        include_original parameter); None is treated as an empty set. Returns a set of
        completed file IDs. Does not write to disk: the caller (_run_pipeline) owns
        committing, once every PKLZ target for this mode has been attempted."""
        include_original_ids = include_original_ids or set()
        input_dir = self.config_data.get("input_dir", DEFAULT_INPUT_DIR)
        pending_files = [(fid, os.path.join(input_dir, fid)) for fid in all_targets
                          if fid not in processed_set]

        if not pending_files:
            self._log(self._tr("log_no_pending_long"))
            return set()

        self._log(self._tr("log_pending_count_long", count=len(pending_files)))

        tempos = list(self.config_data.get("negative_tempo_array") or []) + \
            list(self.config_data.get("positive_tempo_array") or [])
        if not tempos:
            tempos = list(NEGATIVE_TEMPO_DEFAULT) + list(POSITIVE_TEMPO_DEFAULT)

        force_clean_directory(temp_dir_path, recreate=True)
        pool_dir = os.path.join(temp_dir_path, "pool")
        os.makedirs(pool_dir, exist_ok=True)

        # Rolling pool of not-yet-dispatched tempo variations (plus, for a both-pending song,
        # its original), in generation order, plus per-file progress so a file is only marked
        # completed once every one of its variations (and its original, if included) has
        # actually been included in a batch that _run_task reported as successful (returncode
        # 0). "dispatched" is only ever advanced AFTER a batch succeeds (see dispatch() below):
        # this is deliberate, and must not be moved back to "advance on send, gate only the
        # completed_ids update on the result". A song's variations very often span two batches
        # (40 default variations vs. VARIATION_CHUNK_SIZE=30), so advancing "dispatched"
        # unconditionally before the run would let a song whose first batch failed get marked
        # complete anyway, as soon as its second batch (containing only the remainder) happened
        # to succeed, even though part of its data was never actually scanned successfully.
        # Gating the advance itself on success closes that gap.
        pool = []
        progress = {}
        completed_ids = set()
        batch_counter = 0

        def dispatch(batch_items):
            nonlocal batch_counter
            batch_counter += 1
            batch_folder_name = f"long_batch_{batch_counter}"
            batch_folder_path = os.path.join(temp_dir_path, batch_folder_name)
            os.makedirs(batch_folder_path, exist_ok=True)
            for _, src_path in batch_items:
                shutil.move(src_path, os.path.join(batch_folder_path, os.path.basename(src_path)))

            self._log(self._tr("log_processing_long_batch", num=batch_counter, count=len(batch_items)))
            returncode = self._run_task(batch_folder_name, temp_dir_path)

            # A batch only counts as successfully finished when werzatsong.js itself exits 0.
            # This is a deliberate change from the pre-rework code, which committed
            # PROCESSED.txt lines unconditionally after _run_task returned, even on a crash or
            # out-of-memory nonzero exit: that silently marked songs as scanned when they never
            # actually were. Do not "fix" this back to unconditional: a nonzero exit here means
            # every file in this batch (fully or partially dispatched) stays pending and gets
            # regenerated from scratch on the next PKLZ target (and the next scan, if none
            # succeed).
            newly_completed = []
            if returncode == 0:
                counts_in_batch = {}
                for fid, _ in batch_items:
                    counts_in_batch[fid] = counts_in_batch.get(fid, 0) + 1
                for fid, count in counts_in_batch.items():
                    progress[fid]["dispatched"] += count
                    if progress[fid]["dispatched"] >= progress[fid]["total"]:
                        newly_completed.append(fid)
                completed_ids.update(newly_completed)

            self._log(self._tr("log_cleanup_temp"))
            force_clean_directory(batch_folder_path, recreate=False)
            for fid in newly_completed:
                self._log(self._tr("log_task_done", file=fid))

        for idx, (file_id, full_path) in enumerate(pending_files):
            is_last_file = (idx == len(pending_files) - 1)

            generated = self._generate_variations_into_pool(
                full_path, file_id, tempos, pool_dir, sys_temp_dir,
                include_original=(file_id in include_original_ids))
            progress[file_id] = {"total": len(generated), "dispatched": 0}
            for item in generated:
                pool.append((file_id, item))

            if not is_last_file:
                # More files are still coming: stick to plain batches of exactly
                # VARIATION_CHUNK_SIZE as the pool fills up, same as before.
                while len(pool) >= VARIATION_CHUNK_SIZE:
                    batch_items, pool = pool[:VARIATION_CHUNK_SIZE], pool[VARIATION_CHUNK_SIZE:]
                    dispatch(batch_items)
            else:
                # This is the last file: the true final remainder is now known, so rebalance
                # it instead of leaving a needlessly small trailing batch.
                batch_sizes = compute_batch_sizes(len(pool), VARIATION_CHUNK_SIZE, MAX_FILES_PER_BATCH_HARD_LIMIT)
                offset = 0
                for size in batch_sizes:
                    dispatch(pool[offset:offset + size])
                    offset += size
                pool = []

        force_clean_directory(temp_dir_path, recreate=False)
        return completed_ids

    def _run_quick_mode(self, pending_files, processed_set, temp_dir_path):
        """pending_files: relative-path IDs already selected by the orchestrator for this pass
        (already scan_mode filtered, already restricted to this PKLZ target's turn).
        processed_set: the mode's on-disk processed set, re-checked here defensively, same
        rationale as _run_long_mode. Returns a set of completed file IDs. Does not write to
        disk: the caller (_run_pipeline) owns committing."""
        input_dir = self.config_data.get("input_dir", DEFAULT_INPUT_DIR)
        pending = [fid for fid in pending_files if fid not in processed_set]

        if not pending:
            self._log(self._tr("log_no_pending"))
            return set()

        self._log(self._tr("log_pending_count", count=len(pending)))
        force_clean_directory(temp_dir_path, recreate=True)

        completed_ids = set()
        batch_sizes = compute_batch_sizes(len(pending), QUICK_BATCH_CHUNK_SIZE, MAX_FILES_PER_BATCH_HARD_LIMIT)
        total_batches = len(batch_sizes)
        offset = 0
        for batch_num, batch_size in enumerate(batch_sizes, start=1):
            batch = pending[offset:offset + batch_size]
            offset += batch_size

            batch_folder_name = "quick_batch"
            batch_folder_path = os.path.join(temp_dir_path, batch_folder_name)
            os.makedirs(batch_folder_path, exist_ok=True)

            for file_id in batch:
                full_path = os.path.join(input_dir, file_id)
                safe_filename = file_id.replace(os.sep, "___")
                shutil.copy2(full_path, os.path.join(batch_folder_path, safe_filename))

            self._log(self._tr("log_processing_batch", num=batch_num, total=total_batches))
            returncode = self._run_task(batch_folder_name, temp_dir_path)

            # See the matching comment in _run_long_mode's dispatch(): a batch only counts as
            # successfully finished when werzatsong.js itself exits 0. Do not "fix" this back
            # to unconditional; a nonzero exit here means the batch's songs stay pending and
            # are retried on the next PKLZ target (and the next scan, if none succeed).
            if returncode == 0:
                completed_ids.update(batch)

            self._log(self._tr("log_cleanup_temp"))
            force_clean_directory(batch_folder_path, recreate=False)
            self._log(self._tr("log_batch_done", num=batch_num))

        force_clean_directory(temp_dir_path, recreate=False)
        return completed_ids

    def _run_task(self, subfolder, source_root):
        """Runs werzatsong.js against one already-staged batch folder. Returns the process's
        return code (0 = success) so callers (_run_quick_mode / _run_long_mode) can gate
        whether this batch's files count as actually completed. Returns -1 for the "source
        folder missing" early-exit path, since that also means the batch never ran."""
        force_clean_directory(INTERNAL_INPUT_FOLDER, recreate=True)
        force_clean_directory(INTERNAL_TEMP_FOLDER, recreate=False)

        src = os.path.join(source_root, subfolder)
        if not os.path.exists(src):
            self._log(self._tr("log_source_folder_missing", path=src))
            return -1

        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(INTERNAL_INPUT_FOLDER, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, dirs_exist_ok=True)
            else:
                shutil.copy2(s, d)

        log_dir = self.config_data["log_dir"]
        os.makedirs(log_dir, exist_ok=True)
        before_logs = set(os.listdir(log_dir))

        start_time = datetime.now()
        self._log(self._tr("log_starting_task", subfolder=subfolder, time=start_time))
        cmd = self.config_data["WERZATSONG_CMD"]
        returncode = self._run_console_command(cmd, cwd=CUR_FOLDER, extra_env=self._directory_env_overrides())
        if returncode != 0:
            self._log(self._tr("log_werzatsong_exit", code=returncode))

        time.sleep(3)

        after_logs = set(os.listdir(log_dir))
        new_folders = [f for f in after_logs - before_logs if os.path.isdir(os.path.join(log_dir, f))]

        if not new_folders:
            self._log(self._tr("log_no_log_folder", subfolder=subfolder))
        else:
            new_folders.sort(key=lambda f: os.path.getctime(os.path.join(log_dir, f)))
            latest_log_folder = new_folders[-1]
            log_path = os.path.join(log_dir, latest_log_folder)
            self._log(self._tr("log_logs_saved", subfolder=subfolder, folder=latest_log_folder))
            for lf in os.listdir(log_path):
                self._log(f"   - {lf}")

        force_clean_directory(INTERNAL_INPUT_FOLDER, recreate=True)
        return returncode

    def _generate_variations_into_pool(self, input_file_path, file_id, tempos, pool_dir, sys_temp_dir,
                                       include_original=False):
        """Generates every tempo/pitch variation of one file directly into the shared rolling
        pool directory (used by _run_long_mode), returning the list of successfully-generated
        absolute paths. Filenames are prefixed by the file's own sanitized relative path
        (not just its basename), so two different input files that happen to share the same
        filename in different subfolders never collide while sitting in the same pool.

        include_original: when True, also copies the original, unmodified input file into the
        pool (a straight shutil.copy2, never an ffmpeg re-encode: the whole point of including
        it is to scan the file exactly as it is), under the same safe-id-based name the
        variations use as their prefix (e.g. "subdir___song.mp3"). This is used for a
        "both-pending" song (pending both Quick and Long, see _orchestrate_pipeline's
        scan_mode routing): since Long mode is about to include that song anyway, its original
        scan happens here, folded into the Long batch, instead of a separate Quick pass. The
        copy happens before the variation loop so a copy failure is reported immediately and
        in order, and so the per-variation progress counter below still reads as "N of M
        variations" (M = len(tempos)), not "N of M+1". The original's pool name never carries
        a "_t..._p..." suffix, so it can never collide with a variation's name."""
        filename = os.path.basename(input_file_path)

        if shutil.which("ffmpeg") is None:
            raise PipelineAbort(self._tr("ffmpeg_not_found"))

        self._log(self._tr("log_generating_variations", file=filename))

        safe_id = file_id.replace(os.sep, "___")
        base_name = os.path.splitext(safe_id)[0]

        generated = []
        if include_original:
            original_dest = os.path.join(pool_dir, safe_id)
            try:
                shutil.copy2(input_file_path, original_dest)
                generated.append(original_dest)
            except Exception as e:
                self._log(self._tr("log_gen_error", file=filename))
                self._log(str(e))

        tasks = [(input_file_path, tempo, pool_dir, base_name, sys_temp_dir) for tempo in tempos]

        results = [None] * len(tasks)
        errors = []
        completed = 0
        total = len(tasks)
        num_workers = max(1, (os.cpu_count() or 2) // 2)

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
            future_map = {executor.submit(process_single_variation, t): i for i, t in enumerate(tasks)}
            for future in concurrent.futures.as_completed(future_map):
                i = future_map[future]
                completed += 1
                ok, value = future.result()
                if ok:
                    results[i] = value
                else:
                    errors.append(value)
                self._log(self._tr("log_gen_progress", done=completed, total=total))

        generated.extend(path for path in results if path)
        if errors:
            self._log(self._tr("log_gen_error", file=filename))
            for e in errors[:5]:
                self._log(str(e))
        else:
            self._log(self._tr("log_gen_success", total=total, file=filename))
        return generated

    # ------------------------------------------------------------------
    # Console interactivity: copy / select all / right-click menu
    # ------------------------------------------------------------------

    def _console_is_at_bottom(self):
        """True when the console's viewport is showing the very last line."""
        try:
            return self.console.yview()[1] >= 0.9999
        except tk.TclError:
            return True

    def _console_copy(self):
        try:
            self.console.event_generate("<<Copy>>")
        except tk.TclError:
            pass

    def _console_select_all(self):
        try:
            self.console.tag_add("sel", "1.0", "end-1c")
            self.console.mark_set("insert", "1.0")
        except tk.TclError:
            pass

    def _console_copy_event(self, _event=None):
        # Ctrl+X on the console is treated exactly like Ctrl+C (never cuts).
        self._console_copy()
        return "break"

    def _console_select_all_event(self, _event=None):
        self._console_select_all()
        return "break"

    def _console_context_menu(self, event):
        menu = tk.Menu(self, tearoff=0)
        try:
            has_selection = bool(self.console.tag_ranges("sel"))
        except tk.TclError:
            has_selection = False

        menu.add_command(
            label=self.gui_strings.get("ctx_copy", "Copy"),
            command=self._console_copy,
            state="normal" if has_selection else "disabled"
        )
        menu.add_command(
            label=self.gui_strings.get("ctx_select_all", "Select All"),
            command=self._console_select_all
        )
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
        return "break"

    # ----------------------------------------------------------------------
    # Entry widgets: Cut / Copy / Paste / Select All (right-click + Ctrl+A)
    # ----------------------------------------------------------------------

    def _entry_select_all(self, widget):
        try:
            widget.selection_range(0, "end")
            widget.icursor("end")
        except tk.TclError:
            pass

    def _walk_widgets(self, widget):
        """Yields every widget in the tree, starting from `widget`."""
        yield widget
        for child in widget.winfo_children():
            yield from self._walk_widgets(child)

    def _enable_entry_shortcuts(self):
        """Wires up Cut/Copy/Paste/Select All/Undo/Redo for every Entry widget,
        via both keyboard shortcuts and a right-click context menu.

        Undo/redo are custom-built: tk.Entry/ttk.Entry have no native undo stack
        the way tk.Text does. We detect changes after each keystroke (via
        <KeyRelease>, which fires after the entry's own insertion handler) and
        push the *previous* value onto the undo stack, debounced so a fast
        typing burst collapses into a single undo step. A new edit after an
        undo clears the redo branch (standard editor behaviour).

        Bound per-widget at install time (widget bindings are checked before
        class bindings, and each returns "break" so the class fallback doesn't
        double-fire). The class-level bindings are registered afterwards as a
        safety net for any Entry created later.

        Must be called AFTER every Entry in the UI has been created (see
        _build_full_ui), because the widget tree is walked once."""
        if getattr(self, "_entry_undo_installed", False):
            return
        self._entry_undo_installed = True
        self._entry_undo_state = {}

        MAX_UNDO_STEPS = 200
        UNDO_DEBOUNCE_SECONDS = 0.7

        def get_state(entry):
            state = self._entry_undo_state.get(entry)
            if state is None:
                state = {
                    "undo": [],
                    "redo": [],
                    "last_value": None,
                    "last_time": 0.0,
                    "restoring": False,
                }
                self._entry_undo_state[entry] = state
            return state

        def _read_value(entry):
            try:
                return entry.get()
            except tk.TclError:
                return None

        def _write_value(entry, value):
            """Rewrite the entry's content. Returns True on success, False on failure."""
            try:
                entry.delete(0, "end")
                entry.insert(0, value)
                entry.icursor("end")
                entry.selection_clear()
                return True
            except tk.TclError:
                return False

        def _record_change(entry):
            """Compare the entry's current content to what was last observed. If it
            changed, and we're outside the debounce window, push the *previous*
            value onto the undo stack. Called from <KeyRelease> (fires after the
            entry's built-in insertion handler, so `entry.get()` is up-to-date)
            and from <<Paste>> / <<Cut>> hooks."""
            if not entry.winfo_exists():
                return
            state = get_state(entry)
            if state["restoring"]:
                return  # we're the ones rewriting the entry; ignore it
            current = _read_value(entry)
            if current is None:
                return
            last = state["last_value"]
            if last is None:
                # First observation: just record the baseline, nothing to push.
                state["last_value"] = current
                state["last_time"] = time.time()
                return
            if current == last:
                return  # no actual text change (modifier key, arrow, click, etc.)
            now = time.time()
            if now - state["last_time"] >= UNDO_DEBOUNCE_SECONDS:
                # Start of a fresh burst: push the value that was shown *before*
                # this burst began.
                if not state["undo"] or state["undo"][-1] != last:
                    state["undo"].append(last)
                    if len(state["undo"]) > MAX_UNDO_STEPS:
                        state["undo"].pop(0)
                state["redo"].clear()
            state["last_value"] = current
            state["last_time"] = now

        # -- event handlers -------------------------------------------------

        def on_key_release(event):
            _record_change(event.widget)

        def on_focus_in(event):
            """Reset the baseline whenever the user focuses an entry, so undo
            never reaches back into the previous focus session."""
            entry = event.widget
            if not entry.winfo_exists():
                return
            state = get_state(entry)
            state["undo"].clear()
            state["redo"].clear()
            state["last_value"] = _read_value(entry)
            state["last_time"] = 0.0

        def do_undo(entry):
            if not entry.winfo_exists():
                self._entry_undo_state.pop(entry, None)
                return
            state = get_state(entry)
            if not state["undo"]:
                return  # nothing to undo: silently do nothing

            previous = _read_value(entry)
            if previous is None:
                return  # can't read current content: abort rather than corrupt history

            target = state["undo"][-1]
            state["restoring"] = True
            try:
                if not _write_value(entry, target):
                    # Mutation failed: put the widget back how it was. The undo
                    # value stays on the stack so a retry can still succeed.
                    _write_value(entry, previous)
                    return
                # Only now, after a successful mutation, is it safe to consume
                # the history entry and record where it came from.
                state["undo"].pop()
                if not state["redo"] or state["redo"][-1] != previous:
                    state["redo"].append(previous)
                    if len(state["redo"]) > MAX_UNDO_STEPS:
                        state["redo"].pop(0)
                state["last_value"] = target
            finally:
                state["restoring"] = False
            # Force the next keystroke to snapshot as a fresh burst, rather than
            # being debounced into the pre-undo one.
            state["last_time"] = 0.0

        def do_redo(entry):
            if not entry.winfo_exists():
                self._entry_undo_state.pop(entry, None)
                return
            state = get_state(entry)
            if not state["redo"]:
                return  # nothing to redo: silently do nothing

            previous = _read_value(entry)
            if previous is None:
                return

            target = state["redo"][-1]
            state["restoring"] = True
            try:
                if not _write_value(entry, target):
                    _write_value(entry, previous)
                    return  # redo value stays on the stack for a retry
                state["redo"].pop()
                if not state["undo"] or state["undo"][-1] != previous:
                    state["undo"].append(previous)
                    if len(state["undo"]) > MAX_UNDO_STEPS:
                        state["undo"].pop(0)
                state["last_value"] = target
            finally:
                state["restoring"] = False
            state["last_time"] = 0.0

        def on_undo(event):
            do_undo(event.widget)
            return "break"

        def on_redo(event):
            do_redo(event.widget)
            return "break"

        def on_select_all(event):
            self._entry_select_all(event.widget)
            return "break"

        def show_context_menu(event):
            widget = event.widget
            state = get_state(widget)
            menu = tk.Menu(widget, tearoff=0)

            menu.add_command(
                label=self.gui_strings.get("ctx_undo", "Undo"),
                command=lambda w=widget: do_undo(w),
                state=("normal" if state["undo"] else "disabled"),
            )
            menu.add_command(
                label=self.gui_strings.get("ctx_redo", "Redo"),
                command=lambda w=widget: do_redo(w),
                state=("normal" if state["redo"] else "disabled"),
            )
            menu.add_separator()
            menu.add_command(label=self.gui_strings.get("ctx_cut", "Cut"),
                            command=lambda w=widget: w.event_generate("<<Cut>>"))
            menu.add_command(label=self.gui_strings.get("ctx_copy", "Copy"),
                            command=lambda w=widget: w.event_generate("<<Copy>>"))
            menu.add_command(label=self.gui_strings.get("ctx_paste", "Paste"),
                            command=lambda w=widget: w.event_generate("<<Paste>>"))
            menu.add_separator()
            menu.add_command(label=self.gui_strings.get("ctx_select_all", "Select All"),
                            command=lambda w=widget: self._entry_select_all(w))

            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()
            return "break"

        # -- per-widget binding helper (kept on self so dialogs created later,
        # such as _ask_audiotag_key, can apply the same shortcuts to their own
        # freshly-created Entry without waiting for the class fallback to fire) --
        def bind_entry_widget(widget):
            widget.bind("<Button-3>", show_context_menu, add="+")
            widget.bind("<Control-a>", on_select_all, add="+")
            widget.bind("<Control-A>", on_select_all, add="+")
            widget.bind("<Control-z>", on_undo, add="+")
            widget.bind("<Control-Z>", on_undo, add="+")
            widget.bind("<Control-y>", on_redo, add="+")
            widget.bind("<Control-Y>", on_redo, add="+")
            # <KeyRelease> (not <KeyPress>): the entry's own insertion handler
            # runs on KeyPress, so at KeyRelease time the new value is already
            # in the widget and can be compared to the previous observation.
            widget.bind("<KeyRelease>", on_key_release, add="+")
            widget.bind("<FocusIn>", on_focus_in, add="+")
            # Seeds the baseline right now, so the very first keystroke after
            # creation (before any FocusIn has fired) is still undoable.
            try:
                get_state(widget)["last_value"] = widget.get()
            except tk.TclError:
                pass

        self._bind_entry_widget_shortcuts = bind_entry_widget

        # -- per-widget bindings (primary path) -----------------------------
        for widget in self._walk_widgets(self):
            if widget.winfo_class() not in ("Entry", "TEntry"):
                continue
            bind_entry_widget(widget)

        # -- class-level fallback (for any Entry created later) -------------
        for cls in ("TEntry", "Entry"):
            self.bind_class(cls, "<Control-z>", on_undo, add="+")
            self.bind_class(cls, "<Control-Z>", on_undo, add="+")
            self.bind_class(cls, "<Control-y>", on_redo, add="+")
            self.bind_class(cls, "<Control-Y>", on_redo, add="+")
            self.bind_class(cls, "<Control-a>", on_select_all, add="+")
            self.bind_class(cls, "<Control-A>", on_select_all, add="+")
            self.bind_class(cls, "<KeyRelease>", on_key_release, add="+")
            self.bind_class(cls, "<Button-3>", show_context_menu, add="+")

    # ------------------------------------------------------------------
    # Shutdown
    # ------------------------------------------------------------------

    def _on_close(self):
        if self.is_running:
            if not messagebox.askyesno(self._tr("scan_running_title"), self._tr("scan_running_close_msg")):
                return
            # Kills the full process tree for anything still tracked (the node console
            # command and any in-flight ffmpeg calls), not just the immediate child: a plain
            # .terminate() here used to be able to leave orphaned worker processes behind.
            _kill_all_tracked_processes()
        if self.pending_env:
            self._write_env_now()
        self.destroy()


def main():
    app = WerZatSongGUI()
    theme_mode = app.config_data.get("theme_mode", "System")
    apply_theme_to_gui(app, theme_mode)
    setup_theme_listener(app)
    if getattr(app, "_should_exit", False):
        return
    app.mainloop()


if __name__ == "__main__":
    main()