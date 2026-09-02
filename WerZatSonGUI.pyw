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
    from tkinter import ttk, filedialog, messagebox
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
    f"You may have multiple Python installations.\n"
    f"Make sure to install all the requirements, by running the following command in cmd or PowerShell (which you can copy from the crash_logs.txt file):\n\n"
    f"{python_executable} -m pip install -r {pyw_folder}\\requirements.txt\n\n"
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
            
            # Create a hidden main window so we just get the popup
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
LOGO_FILE = os.path.join(ASSETS_FOLDER, "logo.png")
WEBHOOK_JS_FILE = os.path.join(ASSETS_FOLDER, "utils", "webhook.js")
SETTING_EXPLANATIONS_FILE_ENGLISH = os.path.join(ASSETS_FOLDER, "localizations", "advanced_setting_explanations_English.json")
SETTING_EXPLANATIONS_FILE_ITALIANO = os.path.join(ASSETS_FOLDER, "localizations", "advanced_setting_explanations_Italiano.json")
GUI_STRINGS_FILE_ENGLISH = os.path.join(ASSETS_FOLDER, "localizations", "gui_strings_English.json")
GUI_STRINGS_FILE_ITALIANO = os.path.join(ASSETS_FOLDER, "localizations", "gui_strings_Italiano.json")
INTERNAL_INPUT_FOLDER = os.path.join(ASSETS_FOLDER, "input")
INTERNAL_TEMP_FOLDER = os.path.join(ASSETS_FOLDER, "temp")
PROCESSED_FILE = os.path.join(CUR_FOLDER, "PROCESSED.txt")
TEMP_STAGING_DIRNAME = "___TEMP"

DEFAULT_INPUT_DIR = os.path.join(CUR_FOLDER, "db_inputs")
DEFAULT_DB_DIR = os.path.join(ASSETS_FOLDER, "database")
DEFAULT_LOG_DIR = os.path.join(CUR_FOLDER, "logs")

PUBLIC_PKLZ_DATABASE_URL = "https://wzs.cosine.club/"
LOSTWAVE_ITALIA_SONGS_URL = "https://drive.google.com/drive/folders/1S0Tj-PrdKzUc1jZ4c2feUGcyBABLdaEy"
FRENCH_LOSTWAVE_SONGS_URL = "https://drive.google.com/drive/folders/1NLVjBYXNdWy_kxp21Npds6T3F6QpA520"

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
VARIATION_CHUNK_SIZE = 20
QUICK_BATCH_CHUNK_SIZE = 20
# werzatsong.js's own MAX_FILES_PER_SEARCH: a single search/scan must never exceed this,
# but batches should otherwise stick to VARIATION_CHUNK_SIZE/QUICK_BATCH_CHUNK_SIZE (see
# compute_batch_sizes below).
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
# (cursor movement, erase line, etc. - e.g. from npm/pip) is silently dropped without
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

DEFAULT_WEBHOOK_USERNAME = "WerZatSong"
DEFAULT_WEBHOOK_AVATAR = "https://cdn.discordapp.com/icons/1280127901852893244/ea65cd62d0824f7aab1f0bf751364818.webp"
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

CREATIONFLAGS = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
# Used to launch the first-time setup command in its own real console window (rather than
# piping stdin/stdout through our custom Tk console), so interactive prompts behave exactly
# like they would if the user typed the command directly into a terminal themselves.
NEW_CONSOLE_FLAG = subprocess.CREATE_NEW_CONSOLE if os.name == "nt" else 0


# ============================================================================================
# Config helpers
# ============================================================================================

def compute_werzatsong_cmd(config):
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
        if config.get("only_use_fingerprint_subfolder"):
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
        "mode_musicbrainz": True,
        "mode_audiotag": True,
        "mode_shazam": True,
        "mode_audfprint": True,
        "generate_different_tempos": False,
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
        "theme_mode": "System",
        "language": "English",
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
                     "generate_different_tempos", "only_use_fingerprint_subfolder",
                     "use_custom_webhook_name", "use_custom_webhook_image", "use_custom_thread_count",
                     "use_custom_search_depth", "custom_musicbrainz_duration_range", "custom_musicbrainz_extension"]
        for key in bool_keys:
            if isinstance(raw.get(key), bool):
                result[key] = raw[key]

        str_keys = ["fingerprint_subfolder_dirname", "custom_webhook_name_value", "custom_webhook_image_link"]
        for key in str_keys:
            value = raw.get(key)
            if isinstance(value, str) and value.strip():
                result[key] = value

        theme_val = raw.get("theme_mode")
        if isinstance(theme_val, str) and theme_val in ["Light", "Dark", "System"]:
            result["theme_mode"] = theme_val

        lang_val = raw.get("language")
        if isinstance(lang_val, str) and lang_val in ["English", "Italiano"]:
            result["language"] = lang_val

        for key in ["input_dir", "db_dir", "log_dir"]:
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
    file_path = SETTING_EXPLANATIONS_FILE_ITALIANO if language == "Italiano" else SETTING_EXPLANATIONS_FILE_ENGLISH
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


def apply_theme_to_gui(root, theme_mode="System"):
    if theme_mode == "Light":
        target_theme = "light"
    elif theme_mode == "Dark":
        target_theme = "dark"
    else:
        target_theme = darkdetect.theme()

    sv_ttk.set_theme(target_theme)
    version = sys.getwindowsversion()

    if version.major == 10 and version.build >= 22000:
        # Sets the title bar color to the background color on Windows 11 for better appearance
        pywinstyles.change_header_color(root, "#1c1c1c" if target_theme == "dark" else "#fafafa")
    elif version.major == 10:
        pywinstyles.apply_style(root, "dark" if target_theme == "dark" else "normal")

        # Updates the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
        root.wm_attributes("-alpha", 0.99)
        root.wm_attributes("-alpha", 1)


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
        self.env_vars = {}
        self.env_show_frames = {}
        self.env_show_buttons = {}
        self.env_hide_buttons = {}
        self._env_dirty_keys = set()
        self.env_data = {}
        self._pending_processed_lines = []

        # Translation related
        self._text_widgets = []  # (widget, key, kwargs)
        self._notebook_tabs = []  # (notebook, tab_id, key)
        self._toggle_buttons = []  # (button, content_frame, default_expanded)
        self._env_toggle_buttons = []  # (button, key)

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
        # Update window title
        if hasattr(self, '_is_first_time_setup') and self._is_first_time_setup:
            self.title(self._tr("first_time_setup_title"))
        else:
            self.title(self._tr("app_title"))

    def _change_language(self, lang):
        if lang not in ("English", "Italiano"):
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
        self._set_all_texts()  # Ensure all texts are set after building

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
        frame = ttk.LabelFrame(parent, padding=6)
        self._add_text_widget(frame, "console_labelframe")
        frame.pack(fill="both", expand=True, pady=(0, 6))
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
        top = tk.Toplevel(self)
        top.title(self._tr("setting_info_title"))
        top.resizable(False, False)
        top.transient(self)

        frame = ttk.Frame(top, padding=15)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text=explanation, wraplength=320, justify="left").pack()
        self._add_text_widget(ttk.Button(frame, command=top.destroy),
                              "close_btn").pack(pady=(12, 0))
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
        self._build_discord_tab(notebook)

    def _build_general_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=8)
        notebook.add(frame, text=self._tr("general_tab"))
        self._notebook_tabs.append((notebook, frame, "general_tab"))
        frame.columnconfigure(2, weight=1)

        self._add_help_button(frame, 0, "mark_all_audio_files_as_processed")
        self._add_text_widget(ttk.Label(frame, text=""), "mark_all_audio_label").grid(row=0, column=1, sticky="w", pady=2)

        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=0, column=2, sticky="w", padx=4)
        self._add_text_widget(ttk.Button(btn_frame, command=lambda: self._mark_all_processed("quick")),
                              "quick_mode_btn").pack(side="left", padx=2)
        self._add_text_widget(ttk.Button(btn_frame, command=lambda: self._mark_all_processed("long")),
                              "long_mode_btn").pack(side="left", padx=2)
        self._add_text_widget(ttk.Button(btn_frame, command=lambda: self._mark_all_processed("both")),
                              "both_modes_btn").pack(side="left", padx=2)

        self._add_help_button(frame, 1, "theme_mode")
        self._add_text_widget(ttk.Label(frame, text=""), "theme_label").grid(row=1, column=1, sticky="w", pady=2)

        self.var_theme_mode = tk.StringVar(value=self.config_data.get("theme_mode", "System"))
        self.var_theme_mode.trace_add("write", self._make_theme_trace())

        theme_frame = ttk.Frame(frame)
        theme_frame.grid(row=1, column=2, sticky="w", padx=4)
        self._add_text_widget(ttk.Radiobutton(theme_frame, variable=self.var_theme_mode, value="Light"),
                              "light_theme").pack(side="left", padx=2)
        self._add_text_widget(ttk.Radiobutton(theme_frame, variable=self.var_theme_mode, value="Dark"),
                              "dark_theme").pack(side="left", padx=2)
        self._add_text_widget(ttk.Radiobutton(theme_frame, variable=self.var_theme_mode, value="System"),
                              "system_theme").pack(side="left", padx=2)

        # Language selection
        self._add_help_button(frame, 2, "language")
        self._add_text_widget(ttk.Label(frame, text=""), "language_label").grid(row=2, column=1, sticky="w", pady=2)

        lang_frame = ttk.Frame(frame)
        lang_frame.grid(row=2, column=2, sticky="w", padx=4)
        self._add_text_widget(ttk.Radiobutton(lang_frame, variable=self.var_language, value="English"),
                              "english_lang").pack(side="left", padx=2)
        self._add_text_widget(ttk.Radiobutton(lang_frame, variable=self.var_language, value="Italiano"),
                              "italiano_lang").pack(side="left", padx=2)

    def _change_language(self, lang):
        if lang not in ("English", "Italiano"):
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

        self._add_help_button(frame, 0, "fingerprint_subfolder")
        self.var_use_subfolder = tk.BooleanVar(value=self.config_data["only_use_fingerprint_subfolder"])
        self._add_text_widget(ttk.Checkbutton(frame, variable=self.var_use_subfolder,
                                               command=self._flush_immediately),
                              "use_subfolder_check").grid(row=0, column=1, sticky="w", pady=2)
        self.var_subfolder_name = tk.StringVar(value=self.config_data["fingerprint_subfolder_dirname"])
        self.var_subfolder_name.trace_add("write", self._make_simple_trace())
        ttk.Entry(frame, textvariable=self.var_subfolder_name, width=20).grid(row=0, column=2, sticky="ew", padx=4)
        self._add_text_widget(ttk.Button(frame, command=self._browse_subfolder),
                              "browse_btn").grid(row=0, column=3, sticky="w")

        self._add_help_button(frame, 1, "thread_count")
        self.var_use_threads = tk.BooleanVar(value=self.config_data["use_custom_thread_count"])
        self._add_text_widget(ttk.Checkbutton(frame, variable=self.var_use_threads,
                                               command=self._flush_immediately),
                              "thread_count_check").grid(row=1, column=1, sticky="w", pady=2)
        self.var_thread_count = tk.StringVar(value=self.config_data["custom_thread_count_value"])
        self.var_thread_count.trace_add("write", self._make_simple_trace())
        ttk.Entry(frame, textvariable=self.var_thread_count, width=6).grid(row=1, column=2, sticky="w", padx=4)

        self._add_help_button(frame, 2, "search_depth")
        self.var_use_search_depth = tk.BooleanVar(value=self.config_data["use_custom_search_depth"])
        self._add_text_widget(ttk.Checkbutton(frame, variable=self.var_use_search_depth,
                                               command=self._flush_immediately),
                              "search_depth_check").grid(row=2, column=1, sticky="w", pady=2)
        self.var_search_depth = tk.StringVar(value=str(self.config_data["custom_search_depth_value"]))
        self.var_search_depth.trace_add("write", self._make_simple_trace())
        ttk.Entry(frame, textvariable=self.var_search_depth, width=6).grid(row=2, column=2, sticky="w", padx=4)

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

    def _build_tempo_tab(self, notebook):
        frame = ttk.Frame(notebook, padding=8)
        notebook.add(frame, text=self._tr("long_mode_tab"))
        self._notebook_tabs.append((notebook, frame, "long_mode_tab"))
        frame.columnconfigure(2, weight=1)

        self._add_help_button(frame, 0, "generate_different_tempos")
        self.var_gen_tempos = tk.BooleanVar(value=self.config_data["generate_different_tempos"])
        self._add_text_widget(ttk.Checkbutton(frame, variable=self.var_gen_tempos,
                                               command=self._flush_immediately),
                              "enable_long_mode_check").grid(row=0, column=1, columnspan=2, sticky="w", pady=2)

        self._add_help_button(frame, 1, "negative_tempo_array")
        self._add_text_widget(ttk.Label(frame, text=""), "negative_tempo_label").grid(row=1, column=1, sticky="w", pady=2)
        self.var_negative_tempos = tk.StringVar(value=format_tempo_list(self.config_data["negative_tempo_array"]))
        self.var_negative_tempos.trace_add("write", self._make_simple_trace())
        ttk.Entry(frame, textvariable=self.var_negative_tempos).grid(row=1, column=2, sticky="ew", pady=2)

        self._add_help_button(frame, 2, "positive_tempo_array")
        self._add_text_widget(ttk.Label(frame, text=""), "positive_tempo_label").grid(row=2, column=1, sticky="w", pady=2)
        self.var_positive_tempos = tk.StringVar(value=format_tempo_list(self.config_data["positive_tempo_array"]))
        self.var_positive_tempos.trace_add("write", self._make_simple_trace())
        ttk.Entry(frame, textvariable=self.var_positive_tempos).grid(row=2, column=2, sticky="ew", pady=2)

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
        self._add_text_widget(ttk.Button(right, command=self._open_processed_file),
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
    # Mark all as PROCESSED logic
    # ------------------------------------------------------------------

    def _mark_all_processed(self, mode):
        input_dir = self.config_data.get("input_dir", DEFAULT_INPUT_DIR)
        if not os.path.exists(input_dir):
            messagebox.showerror(self._tr("error_title"),
                                 self._tr("input_dir_not_found", dir=input_dir))
            return

        all_targets = []
        for root, dirs, files in os.walk(input_dir):
            if TEMP_STAGING_DIRNAME in dirs:
                dirs.remove(TEMP_STAGING_DIRNAME)

            dirs.sort()
            files.sort()

            for file in files:
                if os.path.splitext(file)[1].lower() in AUDIO_EXTENSIONS:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, input_dir)
                    all_targets.append(rel_path)

        if not all_targets:
            messagebox.showinfo(self._tr("info_title"), self._tr("mark_all_no_audio"))
            return

        try:
            os.makedirs(os.path.dirname(os.path.abspath(PROCESSED_FILE)), exist_ok=True)
            with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
                for rel_path in all_targets:
                    if mode == "quick":
                        f.write(f"{rel_path}|quick\n")
                    elif mode == "long":
                        f.write(f"{rel_path}|long\n")
                    elif mode == "both":
                        f.write(f"{rel_path}|long\n{rel_path}|quick\n")
            messagebox.showinfo(self._tr("success_title"),
                                self._tr("mark_all_success", count=len(all_targets), mode=mode.title()))
        except Exception as e:
            messagebox.showerror(self._tr("error_title"),
                                 self._tr("mark_all_error", error=e))

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
        # background (#111111) - used both for subprocess output (werzatsong.js's own
        # colored console lines) and, via _console_severity_for_message, this app's own
        # [INFO]/[SUCCESS]/etc. log lines.
        self.console.tag_configure("console_info", foreground="#56b6c2")
        self.console.tag_configure("console_success", foreground="#98c379")
        self.console.tag_configure("console_warning", foreground="#e5c07b")
        self.console.tag_configure("console_error", foreground="#e06c75")
        self.console.tag_configure("console_empty", foreground="#7f848e")
        self.after(40, self._pump_console_queue)

    def _set_console_font_size(self, size):
        self.console_font_size = max(CONSOLE_FONT_MIN, min(CONSOLE_FONT_MAX, size))
        self.console.configure(font=(CONSOLE_FONT_FAMILY, self.console_font_size))

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
        without applying a tag - same as the console's old plain-text-only behavior for
        anything that isn't specifically a recognized color code. Not expected to handle
        a color sequence split across two separate calls (e.g. across two 4096-byte
        subprocess reads) - the old strip_ansi()-based code had the same latent limitation
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
        language's own* tag_* values - so this keeps working for any future language
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
                self._insert_console_text(text)
                self.console.mark_set("input_start", "end")
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
        # embedded console below - FORCE_COLOR overrides that. setdefault so an explicit
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
        c["generate_different_tempos"] = bool(self.var_gen_tempos.get())
        c["negative_tempo_array"] = parse_tempo_list(self.var_negative_tempos.get(),
                                                      c.get("negative_tempo_array", NEGATIVE_TEMPO_DEFAULT))
        c["positive_tempo_array"] = parse_tempo_list(self.var_positive_tempos.get(),
                                                      c.get("positive_tempo_array", POSITIVE_TEMPO_DEFAULT))
        c["only_use_fingerprint_subfolder"] = bool(self.var_use_subfolder.get())
        c["fingerprint_subfolder_dirname"] = self.var_subfolder_name.get().strip() or "default_subdir"
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
        c["theme_mode"] = self.var_theme_mode.get()
        c["language"] = self.var_language.get()
        for key in ("input_dir", "db_dir", "log_dir"):
            value = self.dir_vars[key].get().strip()
            c[key] = value or default_config()[key]
        c["envfile_dir"] = ENV_FILE
        c["envfile_example_dir"] = ENV_EXAMPLE_FILE

    def _recompute_command(self):
        self.config_data["WERZATSONG_CMD"] = compute_werzatsong_cmd(self.config_data)

    def _save_config_to_disk(self):
        save_config(self.config_data)

    def _sync_webhook_js(self):
        sync_webhook_js(self.config_data)

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

    def _toggle_env_show(self, key):
        self.show_state[key] = not self.show_state.get(key, False)
        if self.show_state[key]:
            self._set_var_silently(self.env_vars[key], self.env_data.get(key, ""))
            self.env_show_frames[key].grid()
            self.env_show_buttons[key].grid_remove()
        else:
            self.env_show_frames[key].grid_remove()
            self.env_show_buttons[key].grid()

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

    def _browse_subfolder(self):
        base = self.config_data.get("db_dir") or DEFAULT_DB_DIR
        os.makedirs(base, exist_ok=True)
        chosen = filedialog.askdirectory(initialdir=base, title=self._tr("select_fingerprint_subdir_title"))
        if not chosen:
            return
        base_norm = os.path.normpath(base)
        chosen_norm = os.path.normpath(chosen)
        try:
            rel = os.path.relpath(chosen_norm, base_norm)
        except ValueError:
            rel = None
        if not rel or rel.startswith("..") or os.path.isabs(rel):
            messagebox.showwarning(self._tr("warning_title"), self._tr("invalid_subdir_msg"))
            return
        self._set_var_silently(self.var_subfolder_name, rel)
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
        top = tk.Toplevel(self)
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
    # Add pklz / audio files
    # ------------------------------------------------------------------

    def _prompt_files_or_folder(self, title_key, show_pklz_link=False, show_lostwave_italia_link=False, show_french_lostwaves_link=False):
        result = {"choice": None}
        top = tk.Toplevel(self)
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
            link = tk.Label(top, text=self._tr("public_pklz_link"), fg="#1a56db", cursor="hand2",
                             font=("Segoe UI", 9, "underline"))
            link.pack(pady=(0, 15))
            link.bind("<Button-1>", lambda _event: webbrowser.open(PUBLIC_PKLZ_DATABASE_URL))

        if show_lostwave_italia_link:
            link = tk.Label(top, text=self._tr("lostwave_italia_link"), fg="#1a56db", cursor="hand2",
                             font=("Segoe UI", 9, "underline"))
            link.pack(pady=(0, 15))
            link.bind("<Button-1>", lambda _event: webbrowser.open(LOSTWAVE_ITALIA_SONGS_URL))

        if show_french_lostwaves_link:
            link = tk.Label(top, text=self._tr("french_lostwaves_link"), fg="#1a56db", cursor="hand2",
                            font=("Segoe UI", 9, "underline"))
            link.pack(pady=(0, 15))
            link.bind("<Button-1>", lambda _event: webbrowser.open(FRENCH_LOSTWAVE_SONGS_URL))

        top.protocol("WM_DELETE_WINDOW", lambda: pick(None))
        top.grab_set()
        top.wait_window(top)
        return result["choice"]

    def _add_files_flow(self, kind):
        if kind == "pklz":
            title_key = "add_pklz_title"
            show_pklz_link = True
            show_lostwave_italia_link = False
            show_french_lostwaves_link = False
            filetypes = [("PKLZ files", "*.pklz")]
        else:
            title_key = "add_audio_title"
            show_pklz_link = False
            show_lostwave_italia_link = True
            show_french_lostwaves_link = True
            filetypes = [("Audio files", "*.mp3 *.wav *.flac *.m4a")]
        choice = self._prompt_files_or_folder(
            title_key,
            show_pklz_link=show_pklz_link,
            show_lostwave_italia_link=show_lostwave_italia_link,
            show_french_lostwaves_link=show_french_lostwaves_link
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
        try:
            os.makedirs(dest_dir, exist_ok=True)
            dest_label = "database" if kind == "pklz" else "input"
            for item in items:
                name = os.path.basename(item.rstrip("\\/"))
                self._log(self._tr("copy_start", name=name, dest=dest_label))
                try:
                    if os.path.isdir(item):
                        shutil.copytree(item, os.path.join(dest_dir, name), dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, os.path.join(dest_dir, name))
                    self._log(self._tr("copy_success", name=name))
                except Exception as e:
                    self._log(self._tr("copy_error", name=name, error=e))
        except Exception as e:
            error = str(e)
        self.after(0, self._on_copy_finished, error)

    def _on_copy_finished(self, error=None):
        self.btn_add_pklz.configure(state="normal")
        self.btn_add_audio.configure(state="normal")
        if error:
            messagebox.showerror(self._tr("copy_failed_title"), error)
        else:
            messagebox.showinfo(self._tr("copy_finished_title"), self._tr("copy_finished_msg"))

    # ------------------------------------------------------------------
    # Processed files
    # ------------------------------------------------------------------

    def _open_processed_file(self):
        if not os.path.exists(PROCESSED_FILE):
            try:
                os.makedirs(os.path.dirname(os.path.abspath(PROCESSED_FILE)), exist_ok=True)
                open(PROCESSED_FILE, "w", encoding="utf-8").close()
            except Exception as e:
                messagebox.showerror(self._tr("error_title"), self._tr("processed_file_error", error=e))
                return
        try:
            os.startfile(PROCESSED_FILE)
        except Exception as e:
            messagebox.showerror(self._tr("error_title"), self._tr("processed_file_open_error", error=e))

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

    def _on_start_clicked(self):
        if self.is_running:
            return
        if not any([self.var_mode_mb.get(), self.var_mode_audiotag.get(),
                    self.var_mode_shazam.get(), self.var_mode_audfprint.get()]):
            messagebox.showwarning(self._tr("no_mode_selected"), self._tr("no_mode_selected_msg"))
            return

        self._flush_immediately()
        self.is_running = True
        self.btn_start.configure(state="disabled")
        self.btn_add_pklz.configure(state="disabled")
        self.btn_add_audio.configure(state="disabled")
        self.btn_force_stop.configure(state="normal")
        self._set_container_enabled(self._directories_frame, False)
        self._set_container_enabled(self._search_modes_frame, False)
        self._set_container_enabled(self._advanced_notebook, False)
        self._log("=" * 60)
        self._log(self._tr("log_starting"))
        self._log("=" * 60)
        threading.Thread(target=self._pipeline_worker, daemon=True).start()

    def _pipeline_worker(self):
        error = None
        try:
            self._run_pipeline()
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
                self._rollback_pending_processed_lines()
            except Exception:
                pass
            try:
                input_dir = self.config_data.get("input_dir", DEFAULT_INPUT_DIR)
                force_clean_directory(INTERNAL_INPUT_FOLDER, recreate=False)
                force_clean_directory(INTERNAL_TEMP_FOLDER, recreate=False)
                force_clean_directory(os.path.join(input_dir, TEMP_STAGING_DIRNAME), recreate=False)
            except Exception:
                pass
        finally:
            self.after(0, self._relaunch_self)

    def _rollback_pending_processed_lines(self):
        """Removes any PROCESSED.txt line(s) that were written (or about to be written) for
        whatever was in flight when a run gets interrupted, so the next run picks those files
        back up instead of treating them as already searched. Safe to call even if nothing
        was pending."""
        pending = self._pending_processed_lines
        if not pending:
            return
        try:
            if os.path.exists(PROCESSED_FILE):
                with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
                    lines = [line.rstrip("\n") for line in f]
                pending_set = set(pending)
                kept_lines = [line for line in lines if line.strip() not in pending_set]
                if len(kept_lines) != len(lines):
                    with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
                        f.write("\n".join(kept_lines) + ("\n" if kept_lines else ""))
        except Exception:
            pass
        finally:
            self._pending_processed_lines = []

    def _run_pipeline(self):
        config = self.config_data
        input_dir = config["input_dir"]
        mode = "long" if config.get("generate_different_tempos") else "quick"

        if not os.path.exists(input_dir):
            raise PipelineAbort(self._tr("input_dir_not_found", dir=input_dir))

        if not os.path.exists(PROCESSED_FILE):
            os.makedirs(os.path.dirname(os.path.abspath(PROCESSED_FILE)), exist_ok=True)
            open(PROCESSED_FILE, "w", encoding="utf-8").close()

        force_clean_directory(INTERNAL_INPUT_FOLDER, recreate=True)

        # The very first thing a scan does: convert any non-mp3 audio file to mp3 in place
        # (replacing the original) and fix up PROCESSED.txt's extensions to match, so
        # werzatsong.js (which only ever recognizes .mp3) and everything below only ever has
        # to deal with one format. Must run before PROCESSED.txt is read below.
        self._convert_non_mp3_files_to_mp3(input_dir)

        with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
            processed_set = set(line.strip() for line in f if line.strip())

        temp_dir_path = os.path.join(input_dir, TEMP_STAGING_DIRNAME)

        all_targets = []
        for root, dirs, files in os.walk(input_dir):
            if TEMP_STAGING_DIRNAME in dirs:
                dirs.remove(TEMP_STAGING_DIRNAME)

            dirs.sort()
            files.sort()

            for file in files:
                if os.path.splitext(file)[1].lower() in AUDIO_EXTENSIONS:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, input_dir)
                    all_targets.append((rel_path, full_path))

        if not all_targets:
            raise PipelineAbort(self._tr("no_audio_files", dir=input_dir))

        self._log(self._tr("log_found_files", count=len(all_targets), mode=mode.upper()))

        sys_temp_dir = tempfile.mkdtemp()
        try:
            if mode == "long":
                self._run_long_mode(all_targets, processed_set, temp_dir_path, sys_temp_dir)
            else:
                self._run_quick_mode(all_targets, processed_set, temp_dir_path)
        finally:
            force_clean_directory(sys_temp_dir, recreate=False)

        self._log("")
        self._log(self._tr("log_all_tasks_complete"))

    def _convert_non_mp3_files_to_mp3(self, input_dir):
        """Converts every non-mp3 audio file under input_dir to the highest-quality mp3
        ffmpeg can produce, replacing the original, and fixes up any PROCESSED.txt line that
        referenced the old path/extension so it keeps pointing at the right file. The
        conversion is atomic per file (encodes to a temp file, then renames, then deletes the
        original only on success), so an interrupted/force-stopped run never leaves a
        half-converted pair behind: the original stays untouched and any leftover temp file
        is cleaned up and retried on the next run."""
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
                # container - without this flag every single conversion fails immediately.
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
            self._rewrite_processed_extensions(renamed)
        if converted:
            self._log(self._tr("log_convert_done", count=converted))

    @staticmethod
    def _rewrite_processed_extensions(renamed):
        """renamed: old relative path -> new relative path (same folder, .mp3 extension).
        Rewrites every PROCESSED.txt line (bare "path", "path|quick", or "path|long") that
        referenced an old path so it points at the converted file instead."""
        if not os.path.exists(PROCESSED_FILE):
            return
        try:
            with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
                lines = [line.rstrip("\n") for line in f]
        except Exception:
            return

        changed = False
        new_lines = []
        for line in lines:
            stripped = line.strip()
            if not stripped:
                new_lines.append(line)
                continue
            if stripped.endswith("|quick") or stripped.endswith("|long"):
                path_part, _, suffix = stripped.rpartition("|")
            else:
                path_part, suffix = stripped, None
            if path_part in renamed:
                new_path = renamed[path_part]
                new_lines.append(f"{new_path}|{suffix}" if suffix else new_path)
                changed = True
            else:
                new_lines.append(line)

        if changed:
            try:
                with open(PROCESSED_FILE, "w", encoding="utf-8") as f:
                    f.write("\n".join(new_lines) + ("\n" if new_lines else ""))
            except Exception:
                pass

    def _run_long_mode(self, all_targets, processed_set, temp_dir_path, sys_temp_dir):
        pending_files = [(fid, path) for fid, path in all_targets
                          if f"{fid}|long" not in processed_set and fid not in processed_set]

        if not pending_files:
            self._log(self._tr("log_no_pending_long"))
            return

        self._log(self._tr("log_pending_count_long", count=len(pending_files)))

        tempos = list(self.config_data.get("negative_tempo_array") or []) + \
            list(self.config_data.get("positive_tempo_array") or [])
        if not tempos:
            tempos = list(NEGATIVE_TEMPO_DEFAULT) + list(POSITIVE_TEMPO_DEFAULT)

        force_clean_directory(temp_dir_path, recreate=True)
        pool_dir = os.path.join(temp_dir_path, "pool")
        os.makedirs(pool_dir, exist_ok=True)

        # Rolling pool of not-yet-dispatched tempo variations, in generation order, plus
        # per-file progress so a file is only marked processed once *every* one of its
        # variations has actually been included in a successfully-dispatched batch (its
        # tail may end up merged into the next file's batch - see compute_batch_sizes).
        pool = []
        progress = {}
        batch_counter = 0

        def dispatch(batch_items):
            nonlocal batch_counter
            batch_counter += 1
            batch_folder_name = f"long_batch_{batch_counter}"
            batch_folder_path = os.path.join(temp_dir_path, batch_folder_name)
            os.makedirs(batch_folder_path, exist_ok=True)
            for _, src_path in batch_items:
                shutil.move(src_path, os.path.join(batch_folder_path, os.path.basename(src_path)))

            counts_in_batch = {}
            for fid, _ in batch_items:
                counts_in_batch[fid] = counts_in_batch.get(fid, 0) + 1
            newly_completed = []
            for fid, count in counts_in_batch.items():
                progress[fid]["dispatched"] += count
                if progress[fid]["dispatched"] >= progress[fid]["total"]:
                    newly_completed.append(fid)

            self._log(self._tr("log_processing_long_batch", num=batch_counter, count=len(batch_items)))
            # Only the files that become fully complete as a result of *this* batch are
            # written to PROCESSED.txt, and only after _run_task returns: if Force Stop kills
            # the run mid-batch, nothing here has been committed yet, so every file involved
            # (fully or partially) simply gets regenerated from scratch on the next run.
            pending_lines = [f"{fid}|long" for fid in newly_completed]
            self._pending_processed_lines = pending_lines
            self._run_task(batch_folder_name, temp_dir_path)

            if pending_lines:
                with open(PROCESSED_FILE, "a", encoding="utf-8") as f:
                    for line in pending_lines:
                        f.write(f"{line}\n")
                for line in pending_lines:
                    processed_set.add(line)
            self._pending_processed_lines = []

            self._log(self._tr("log_cleanup_temp"))
            force_clean_directory(batch_folder_path, recreate=False)
            for fid in newly_completed:
                self._log(self._tr("log_task_done", file=fid))

        for idx, (file_id, full_path) in enumerate(pending_files):
            is_last_file = (idx == len(pending_files) - 1)

            generated = self._generate_variations_into_pool(full_path, file_id, tempos, pool_dir, sys_temp_dir)
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

    def _run_quick_mode(self, all_targets, processed_set, temp_dir_path):
        pending_files = [(fid, path) for fid, path in all_targets
                          if f"{fid}|quick" not in processed_set and fid not in processed_set]

        if not pending_files:
            self._log(self._tr("log_no_pending"))
            return

        self._log(self._tr("log_pending_count", count=len(pending_files)))
        force_clean_directory(temp_dir_path, recreate=True)

        batch_sizes = compute_batch_sizes(len(pending_files), QUICK_BATCH_CHUNK_SIZE, MAX_FILES_PER_BATCH_HARD_LIMIT)
        total_batches = len(batch_sizes)
        offset = 0
        for batch_num, batch_size in enumerate(batch_sizes, start=1):
            batch = pending_files[offset:offset + batch_size]
            offset += batch_size

            batch_folder_name = "quick_batch"
            batch_folder_path = os.path.join(temp_dir_path, batch_folder_name)
            os.makedirs(batch_folder_path, exist_ok=True)

            for file_id, full_path in batch:
                safe_filename = file_id.replace(os.sep, "___")
                shutil.copy2(full_path, os.path.join(batch_folder_path, safe_filename))

            self._log(self._tr("log_processing_batch", num=batch_num, total=total_batches))
            # Quick mode only writes these lines to disk AFTER _run_task succeeds below, so
            # there's nothing to roll back yet if Force Stop fires here: this is tracked
            # anyway for symmetry with long mode, in case that ordering ever changes.
            self._pending_processed_lines = [f"{file_id}|quick" for file_id, _ in batch]
            self._run_task(batch_folder_name, temp_dir_path)

            with open(PROCESSED_FILE, "a", encoding="utf-8") as f:
                for file_id, _ in batch:
                    f.write(f"{file_id}|quick\n")
            self._pending_processed_lines = []

            self._log(self._tr("log_cleanup_temp"))
            force_clean_directory(batch_folder_path, recreate=False)
            self._log(self._tr("log_batch_done", num=batch_num))

        force_clean_directory(temp_dir_path, recreate=False)

    def _run_task(self, subfolder, source_root):
        force_clean_directory(INTERNAL_INPUT_FOLDER, recreate=True)
        force_clean_directory(INTERNAL_TEMP_FOLDER, recreate=False)

        src = os.path.join(source_root, subfolder)
        if not os.path.exists(src):
            self._log(self._tr("log_source_folder_missing", path=src))
            return

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

    def _generate_variations_into_pool(self, input_file_path, file_id, tempos, pool_dir, sys_temp_dir):
        """Generates every tempo/pitch variation of one file directly into the shared rolling
        pool directory (used by _run_long_mode), returning the list of successfully-generated
        absolute paths. Filenames are prefixed by the file's own sanitized relative path
        (not just its basename), so two different input files that happen to share the same
        filename in different subfolders never collide while sitting in the same pool."""
        filename = os.path.basename(input_file_path)

        if shutil.which("ffmpeg") is None:
            raise PipelineAbort(self._tr("ffmpeg_not_found"))

        self._log(self._tr("log_generating_variations", file=filename))

        safe_id = file_id.replace(os.sep, "___")
        base_name = os.path.splitext(safe_id)[0]

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

        generated = [path for path in results if path]
        if errors:
            self._log(self._tr("log_gen_error", file=filename))
            for e in errors[:5]:
                self._log(str(e))
        else:
            self._log(self._tr("log_gen_success", total=total, file=filename))
        return generated

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