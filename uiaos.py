
import curses
import ast
from datetime import datetime
import getpass
import json
import os
import re
import random
import shutil
import struct
import subprocess
import sys
import termios
import urllib.error
import urllib.parse
import urllib.request
import webbrowser
import zlib

# ==============================
# PYOS - PYTHON OPERATING SYSTEM
# ==============================

APPS = [
    "FILES",
    "PYTHON",
    "STORE",
    "GAMES",
    "GALLERY",
    "ACCOUNT",
    "SETTINGS"
]
STORE_APPS = [
    {
        "id": "may_tinh",
        "name": "May tinh",
        "category": "Cong cu",
        "description": "Cong cu tinh toan co ban",
        "size": "0.1 MB",
        "source": """first = float(input("So thu nhat: "))
operation = input("Phep tinh (+, -, *, /): ")
second = float(input("So thu hai: "))
if operation == "+":
    result = first + second
elif operation == "-":
    result = first - second
elif operation == "*":
    result = first * second
elif operation == "/":
    result = first / second
else:
    raise ValueError("Phep tinh khong hop le")
print("Ket qua:", result)
""",
    },
    {
        "id": "ghi_chu",
        "name": "Ghi chu",
        "category": "Tien ich",
        "description": "Luu ghi chu ca nhan",
        "size": "0.2 MB",
        "source": """from pathlib import Path

notes_path = Path.home() / "PYOS" / "notes.txt"
notes_path.parent.mkdir(parents=True, exist_ok=True)
note = input("Nhap ghi chu: ")
with notes_path.open("a", encoding="utf-8") as notes_file:
    notes_file.write(note + "\\n")
print("Da luu ghi chu")
""",
    },
    {
        "id": "doan_so",
        "name": "Doan so",
        "category": "Tro choi",
        "description": "Tro choi doan so don gian",
        "size": "0.1 MB",
        "source": """import random

answer = random.randint(1, 10)
guess = int(input("Doan mot so tu 1 den 10: "))
if guess == answer:
    print("Chinh xac!")
else:
    print("Chua dung. So dung la", answer)
""",
    },
]
FILES_ROOT = os.path.abspath(os.path.expanduser("~/PYOS/files"))
STORE_ROOT = os.path.abspath(os.path.expanduser("~/PYOS/apps"))
STORE_CATALOG_URL = "https://raw.githubusercontent.com/uiahubUI/Script/refs/heads/main/Python%20store"
WALL_ROOT = os.path.abspath(os.path.expanduser("~/PYOS/wall"))
PYOS_ROOT = os.path.abspath(os.path.expanduser("~/PYOS"))
ACCOUNT_FILE = os.path.join(PYOS_ROOT, "account.json")
SETTINGS_FILE = os.path.join(PYOS_ROOT, "settings.json")
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tif", ".tiff"}
DEFAULT_SETTINGS = {
    "accent": "Cyan",
    "boot_animation": True,
    "show_datetime": True,
    "desktop_code_animation": False,
    "quick_commands": {"gpt": "https://chatgpt.com"},
}
ACCENT_COLORS = {
    "Cyan": curses.COLOR_CYAN,
    "Green": curses.COLOR_GREEN,
    "Yellow": curses.COLOR_YELLOW,
    "Magenta": curses.COLOR_MAGENTA,
}
ACCENT_COLOR_PAIR = 20
PAINT_RGB = [
    (18, 30, 48),
    (240, 98, 110),
    (255, 171, 91),
    (247, 222, 141),
    (93, 193, 168),
    (88, 154, 222),
    (163, 128, 226),
    (239, 240, 230),
]
PAINT_CURSES_COLORS = [
    curses.COLOR_BLACK,
    curses.COLOR_RED,
    curses.COLOR_YELLOW,
    curses.COLOR_GREEN,
    curses.COLOR_CYAN,
    curses.COLOR_BLUE,
    curses.COLOR_MAGENTA,
    curses.COLOR_WHITE,
]
BOOT_LINES = [
    ">>> def boot_pyos():",
    "...     terminal.initialize()",
    "...     files.mount('~/PYOS/files')",
    "[  OK  ] Filesystem ready",
    "...     apps = load_applications()",
    "[  OK  ] 7 applications loaded",
    "...     store.connect(mode='demo')",
    "[ INFO ] Store running offline",
    "...     keyboard.enable()",
    "[  OK  ] Keyboard input ready",
    "...     desktop.render()",
    "[  OK  ] Desktop panels ready",
    "...     start_desktop()",
    ">>> boot_pyos()",
    "[PYOS] Desktop ready_",
]
DESKTOP_STREAM_LINES = [
    "...     input_state = keyboard.poll({tick})",
    "...     task = scheduler.run({tick})",
    "...     frame = renderer.compose({tick})",
    "[  OK  ] Frame {tick} synchronized",
    "...     files.refresh_index({tick})",
    "...     apps.update_status({tick})",
    "...     graphics.flush({tick})",
    "[ INFO ] Update desktop {tick}",
    "...     memory.collect({tick})",
    "...     desktop.render_frame({tick})",
    "...     window = panels.refresh({tick})",
    "...     event = keys.consume({tick})",
    "...     jobs = scheduler.poll({tick})",
    "...     cache = files.update({tick})",
    "...     theme = settings.apply({tick})",
    "...     frame = graphics.present({tick})",
    "...     focus = desktop.select({tick})",
    "...     status = services.check({tick})",
    "...     cursor = terminal.blink({tick})",
    "...     image = gallery.load({tick})",
    "...     command = quick_launch({tick})",
    "...     notes = storage.sync({tick})",
    "...     menu = apps.render({tick})",
    "...     pixels = canvas.draw({tick})",
    "...     session = account.read({tick})",
    "...     queue = scheduler.next({tick})",
    "...     config = settings.read({tick})",
    "...     log = system.append({tick})",
    "...     task = process.update({tick})",
    "...     pane = desktop.compose({tick})",
    "...     sound = audio.check({tick})",
    "...     index = files.scan({tick})",
    "...     network = link.status({tick})",
    "...     memory_state = memory.inspect({tick})",
    "...     screen = terminal.refresh({tick})",
    "...     catalog = store.refresh({tick})",
    "...     event = mouse.poll({tick})",
    "...     output = renderer.flush({tick})",
    "...     panel = info.update({tick})",
    "...     state = keyboard.decode({tick})",
    "...     ready = system.check({tick})",
    "[ INFO ] Desktop cycle {tick}",
]


def get_default_account_name():
    return os.environ.get("USER") or getpass.getuser() or "User"


def load_account_name():
    try:
        with open(ACCOUNT_FILE, "r", encoding="utf-8") as account_file:
            name = json.load(account_file).get("display_name")
    except (OSError, ValueError, TypeError):
        return get_default_account_name()
    if isinstance(name, str) and name.strip() and len(name) <= 32 and all(char.isprintable() for char in name):
        return name.strip()
    return get_default_account_name()


def save_account_name(name):
    name = name.strip()
    if not name or len(name) > 32 or not all(char.isprintable() for char in name):
        return False, "Ten khong hop le"
    try:
        os.makedirs(PYOS_ROOT, exist_ok=True)
        with open(ACCOUNT_FILE, "w", encoding="utf-8") as account_file:
            json.dump({"display_name": name}, account_file, ensure_ascii=False, indent=2)
    except OSError:
        return False, "Khong the luu ho so"
    return True, "Da cap nhat ten"


def get_default_settings():
    settings = DEFAULT_SETTINGS.copy()
    settings["quick_commands"] = DEFAULT_SETTINGS["quick_commands"].copy()
    return settings


def normalize_quick_command(name, url):
    if not isinstance(name, str) or not isinstance(url, str):
        return None
    name = name.strip().casefold()
    url = url.strip()
    if (
        not name
        or len(name) > 24
        or not name.isascii()
        or not all(character.isalnum() or character in "-_" for character in name)
        or not url
        or len(url) > 2048
        or any(not character.isprintable() or character.isspace() for character in url)
    ):
        return None
    try:
        parsed_url = urllib.parse.urlsplit(url)
        if (
            parsed_url.scheme.casefold() not in ("http", "https")
            or not parsed_url.hostname
            or parsed_url.username is not None
            or parsed_url.password is not None
        ):
            return None
    except ValueError:
        return None
    return name, url


def load_settings():
    settings = get_default_settings()
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as settings_file:
            saved_settings = json.load(settings_file)
    except (OSError, ValueError, TypeError):
        return settings
    if not isinstance(saved_settings, dict):
        return settings
    if saved_settings.get("accent") in ACCENT_COLORS:
        settings["accent"] = saved_settings["accent"]
    for key in ("boot_animation", "show_datetime", "desktop_code_animation"):
        if isinstance(saved_settings.get(key), bool):
            settings[key] = saved_settings[key]
    saved_commands = saved_settings.get("quick_commands")
    if isinstance(saved_commands, dict):
        commands = {}
        for name, url in saved_commands.items():
            normalized = normalize_quick_command(name, url)
            if normalized and normalized[0] not in commands and len(commands) < 20:
                commands[normalized[0]] = normalized[1]
        settings["quick_commands"] = commands
    return settings


def save_settings(settings):
    try:
        os.makedirs(PYOS_ROOT, exist_ok=True)
        with open(SETTINGS_FILE, "w", encoding="utf-8") as settings_file:
            json.dump(settings, settings_file, ensure_ascii=False, indent=2)
    except OSError:
        return False
    return True


def apply_accent_color(settings):
    if not curses.has_colors():
        return curses.A_NORMAL
    try:
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(ACCENT_COLOR_PAIR, ACCENT_COLORS[settings["accent"]], -1)
        return curses.color_pair(ACCENT_COLOR_PAIR)
    except curses.error:
        return curses.A_NORMAL


def get_desktop_layout(stdscr):
    height, width = stdscr.getmaxyx()
    main_y = 3
    apps_y = height - 6
    left_x = 1
    left_width = (width - 3) * 2 // 3
    right_x = left_x + left_width + 1
    return {
        "height": height,
        "width": width,
        "main_y": main_y,
        "main_height": apps_y - main_y - 1,
        "left_x": left_x,
        "left_width": left_width,
        "right_x": right_x,
        "right_width": width - right_x - 1,
        "apps_y": apps_y,
        "apps_width": width - 2,
    }


def draw_desktop(stdscr, selected, active_view="DESKTOP", desktop_lines=None, quick_mode=False):
    layout = get_desktop_layout(stdscr)
    height = layout["height"]
    width = layout["width"]
    settings = load_settings()
    accent = apply_accent_color(settings)
    stdscr.erase()

    if height < 22 or width < 64:
        stdscr.addnstr(0, 0, "Terminal too small (minimum 64x22)", width - 1)
        stdscr.refresh()
        return False

    username = load_account_name()
    title = "PYOS"
    welcome = f"Welcome, {username}"
    stdscr.addnstr(0, max(0, (width - len(title)) // 2), title, width - 1, accent | curses.A_BOLD)
    stdscr.addnstr(1, max(0, (width - len(welcome)) // 2), welcome, width - 1)
    stdscr.hline(2, 1, curses.ACS_HLINE, width - 2, accent)

    main_frame = curses.newwin(
        layout["main_height"], layout["left_width"], layout["main_y"], layout["left_x"]
    )
    main_frame.box()
    main_frame.addnstr(0, 2, f" {active_view} ", layout["left_width"] - 4, accent)

    info_frame = curses.newwin(
        layout["main_height"], layout["right_width"], layout["main_y"], layout["right_x"]
    )
    info_frame.box()
    info_frame.addnstr(0, 2, " THONG TIN ", layout["right_width"] - 4, accent)
    info_content = curses.newwin(
        layout["main_height"] - 2,
        layout["right_width"] - 2,
        layout["main_y"] + 1,
        layout["right_x"] + 1,
    )
    now = datetime.now()
    info_lines = [f"Nguoi dung: {username}"]
    if settings["show_datetime"]:
        info_lines.extend((f"Ngay: {now:%d/%m/%Y}", f"Gio: {now:%H:%M:%S}"))
    info_lines.extend((
        f"Muc: {active_view}",
        f"File: {len(get_file_entries(FILES_ROOT, FILES_ROOT)[0])}",
        f"App Store: {len(get_installed_store_apps())}",
    ))
    for row, line in enumerate(info_lines):
        if row < layout["main_height"] - 2:
            info_content.addnstr(row, 0, line, layout["right_width"] - 2)

    apps_frame = curses.newwin(4, layout["apps_width"], layout["apps_y"], 1)
    apps_frame.box()
    apps_frame.addstr(0, 2, " UNG DUNG ", accent)
    column_count = 3
    slot_width = (layout["apps_width"] - 2) // column_count
    last_row_start = (len(APPS) - 1) // column_count * column_count
    last_row_count = len(APPS) - last_row_start
    for index, app in enumerate(APPS):
        label = f"[{app}]"
        attributes = (curses.A_REVERSE | accent) if index == selected else curses.A_NORMAL
        row, column = divmod(index, column_count)
        if row == last_row_start // column_count and last_row_count < column_count:
            column += (column_count - last_row_count) // 2
        apps_frame.addnstr(row + 1, 1 + column * slot_width, label, slot_width, attributes)

    if quick_mode:
        footer = "Nhap lenh  ENTER: Chay  ESC: Huy"
    elif active_view == "DESKTOP":
        footer = "ARROWS: App  ENTER: Mo  CTRL+X: Lenh nhanh  ESC: Thoat"
    else:
        footer = "ESC: Quay lai Desktop"
    stdscr.addnstr(height - 1, 2, footer, width - 4)
    stdscr.noutrefresh()
    main_frame.noutrefresh()
    info_frame.noutrefresh()
    info_content.noutrefresh()
    apps_frame.noutrefresh()
    curses.doupdate()

    if active_view == "DESKTOP":
        content = curses.newwin(
            layout["main_height"] - 2,
            layout["left_width"] - 2,
            layout["main_y"] + 1,
            layout["left_x"] + 1,
        )
        lines = BOOT_LINES if desktop_lines is None else desktop_lines
        visible_lines = lines[-(layout["main_height"] - 2):]
        for row, line in enumerate(visible_lines):
            content.addnstr(row, 0, line, layout["left_width"] - 2, accent | curses.A_BOLD)
        content.noutrefresh()
        curses.doupdate()
    return True


def draw_boot_animation(stdscr, selected):
    if not load_settings()["boot_animation"]:
        draw_desktop(stdscr, selected)
        return
    for line_count in range(1, len(BOOT_LINES) + 1):
        if not draw_desktop(stdscr, selected, desktop_lines=BOOT_LINES[:line_count]):
            return
        curses.napms(110)


def get_file_entries(current_directory, root_directory):
    entries = []

    if current_directory != root_directory:
        entries.append(("..", True, True))

    directories = []
    files = []

    try:
        with os.scandir(current_directory) as directory_entries:
            for entry in directory_entries:
                try:
                    is_directory = entry.is_dir(follow_symlinks=False)
                except OSError:
                    continue

                item = (entry.name, is_directory, False)
                if is_directory:
                    directories.append(item)
                else:
                    files.append(item)
    except FileNotFoundError:
        return entries, ""
    except OSError:
        return entries, "Khong the doc thu muc"

    directories.sort(key=lambda item: item[0].casefold())
    files.sort(key=lambda item: item[0].casefold())
    entries.extend(directories)
    entries.extend(files)
    return entries, ""


def get_gallery_images(root_directory):
    image_paths = []
    for current_directory, directories, filenames in os.walk(root_directory, followlinks=False):
        directories[:] = [
            name for name in directories
            if not os.path.islink(os.path.join(current_directory, name))
        ]
        for filename in filenames:
            file_path = os.path.join(current_directory, filename)
            if (
                os.path.splitext(filename)[1].casefold() in IMAGE_EXTENSIONS
                and not os.path.islink(file_path)
            ):
                image_paths.append(os.path.relpath(file_path, root_directory))
    return sorted(image_paths, key=str.casefold)


def copy_image_to_wall(source_path):
    source_path = os.path.abspath(source_path)
    if os.path.commonpath((FILES_ROOT, source_path)) != FILES_ROOT:
        return False, "Anh phai nam trong FILES"
    if (
        os.path.islink(source_path)
        or not os.path.isfile(source_path)
        or os.path.splitext(source_path)[1].casefold() not in IMAGE_EXTENSIONS
    ):
        return False, "File khong phai anh hop le"

    destination_path = os.path.join(WALL_ROOT, os.path.basename(source_path))
    if os.path.exists(destination_path):
        return False, "Anh nay da co trong WALL"

    try:
        os.makedirs(WALL_ROOT, exist_ok=True)
        shutil.copy2(source_path, destination_path)
    except FileExistsError:
        return False, "Anh nay da co trong WALL"
    except OSError:
        return False, "Khong the them anh vao WALL"
    return True, f"Da them anh: {os.path.basename(source_path)}"


def get_image_extension(image_data):
    if image_data.startswith(b"\x89PNG\r\n\x1a\n"):
        return ".png"
    if image_data.startswith(b"\xff\xd8\xff"):
        return ".jpg"
    if image_data.startswith((b"GIF87a", b"GIF89a")):
        return ".gif"
    if image_data.startswith(b"BM"):
        return ".bmp"
    if image_data.startswith(b"RIFF") and image_data[8:12] == b"WEBP":
        return ".webp"
    if image_data.startswith((b"II*\x00", b"MM\x00*")):
        return ".tiff"
    return ""


def download_wall_image(url):
    url = url.strip()
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme not in ("http", "https") or not parsed_url.netloc:
        return None, "Can URL anh HTTP hoac HTTPS"

    request = urllib.request.Request(url, headers={"User-Agent": "PYOS Gallery/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            content_length = response.headers.get("Content-Length")
            if content_length and int(content_length) > 15 * 1024 * 1024:
                return None, "Anh qua lon (toi da 15 MB)"
            image_data = response.read(15 * 1024 * 1024 + 1)
    except (urllib.error.URLError, TimeoutError, OSError, ValueError):
        return None, "Khong tai duoc anh tu URL"

    if len(image_data) > 15 * 1024 * 1024:
        return None, "Anh qua lon (toi da 15 MB)"
    extension = get_image_extension(image_data)
    if not extension:
        return None, "URL khong chua anh duoc ho tro"

    raw_name = os.path.basename(urllib.parse.unquote(parsed_url.path))
    name_stem = os.path.splitext(raw_name)[0]
    safe_stem = "".join(character for character in name_stem if character.isalnum() or character in "-_.")
    safe_stem = safe_stem.strip("._")[:60] or "web-image"
    filename = safe_stem + extension
    try:
        os.makedirs(WALL_ROOT, exist_ok=True)
        path = os.path.join(WALL_ROOT, filename)
        suffix = 2
        while os.path.exists(path):
            path = os.path.join(WALL_ROOT, f"{safe_stem}-{suffix}{extension}")
            suffix += 1
        with open(path, "xb") as image_file:
            image_file.write(image_data)
    except OSError:
        return None, "Khong the luu anh vao WALL"
    return path, f"Da tai anh: {os.path.basename(path)}"


def png_chunk(chunk_type, data):
    return (
        struct.pack(">I", len(data))
        + chunk_type
        + data
        + struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
    )


def save_wall_drawing(filename, pixels):
    filename = filename.strip()
    if not filename or os.path.basename(filename) != filename or "\0" in filename:
        return None, "Ten anh khong hop le"
    if not filename.casefold().endswith(".png"):
        filename += ".png"

    path = os.path.join(WALL_ROOT, filename)
    if os.path.exists(path):
        return None, "Ten anh da ton tai"

    scale = 16
    width = len(pixels[0]) * scale
    height = len(pixels) * scale
    raw_image = bytearray()
    for row in pixels:
        pixel_row = b"".join(bytes(PAINT_RGB[color]) * scale for color in row)
        for _ in range(scale):
            raw_image.extend(b"\x00" + pixel_row)

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png_data = (
        b"\x89PNG\r\n\x1a\n"
        + png_chunk(b"IHDR", header)
        + png_chunk(b"IDAT", zlib.compress(raw_image))
        + png_chunk(b"IEND", b"")
    )
    try:
        os.makedirs(WALL_ROOT, exist_ok=True)
        with open(path, "xb") as image_file:
            image_file.write(png_data)
    except FileExistsError:
        return None, "Ten anh da ton tai"
    except OSError:
        return None, "Khong the luu anh vao WALL"
    return path, f"Da tao anh: {filename}"


def create_empty_file(current_directory, filename):
    filename = filename.strip()
    if (
        not filename
        or filename in (".", "..")
        or os.path.basename(filename) != filename
        or "\0" in filename
    ):
        return False, "Ten file khong hop le"

    file_path = os.path.join(current_directory, filename)
    try:
        os.makedirs(current_directory, exist_ok=True)
        with open(file_path, "x", encoding="utf-8"):
            pass
    except FileExistsError:
        return False, "File da ton tai"
    except OSError:
        return False, "Khong the tao file"

    return True, f"Da tao: {filename}"


def new_file_dialog(stdscr):
    height, width = stdscr.getmaxyx()
    dialog_height = 7
    dialog_width = min(50, width - 4)
    top = (height - dialog_height) // 2
    left = (width - dialog_width) // 2
    dialog = curses.newwin(dialog_height, dialog_width, top, left)
    dialog.keypad(True)

    filename = ""
    max_length = dialog_width - 8

    while True:
        dialog.erase()
        dialog.box()
        dialog.addstr(0, 2, " NEW FILE ")
        dialog.addstr(2, 2, "Ten file moi:")
        dialog.addnstr(3, 2, f"> {filename}", dialog_width - 4)
        dialog.addstr(5, 2, "ENTER: Tao   ESC: Huy")
        dialog.move(3, min(dialog_width - 2, 4 + len(filename)))
        dialog.refresh()

        key = dialog.get_wch()
        if key in (10, 13, curses.KEY_ENTER, "\n", "\r"):
            return filename.strip() or None
        if key in (27, "\x1b"):
            return None
        if key in (curses.KEY_BACKSPACE, 127, 8, "\x7f", "\b"):
            filename = filename[:-1]
        elif isinstance(key, str) and key.isprintable() and len(filename) < max_length:
            filename += key


def confirm_delete_dialog(stdscr, filename):
    height, width = stdscr.getmaxyx()
    dialog_height = 7
    dialog_width = min(60, width - 4)
    top = (height - dialog_height) // 2
    left = (width - dialog_width) // 2
    dialog = curses.newwin(dialog_height, dialog_width, top, left)
    dialog.keypad(True)
    dialog.box()
    dialog.addnstr(1, 2, "Ban chac chan muon xoa file nay?", dialog_width - 4)
    dialog.addnstr(3, 2, filename, dialog_width - 4)
    dialog.addnstr(5, 2, "Y: Xoa   N/ESC: Huy", dialog_width - 4)
    dialog.refresh()
    key = dialog.getch()
    return key in (ord("y"), ord("Y"))


def save_editor_file(file_path, lines):
    try:
        with open(file_path, "w", encoding="utf-8") as source_file:
            source_file.write("\n".join(lines) + "\n")
    except OSError:
        return False
    return True


def validate_store_catalog(apps):
    required_fields = ("id", "name", "category", "description", "size", "source")
    if not isinstance(apps, list) or not apps or len(apps) > 50:
        return None

    validated_apps = []
    seen_ids = set()
    for app in apps:
        if not isinstance(app, dict) or any(not isinstance(app.get(key), str) for key in required_fields):
            return None
        app_id = app["id"]
        if (
            not app_id
            or len(app_id) > 64
            or not app_id.isascii()
            or not all(character.isalnum() or character in "-_" for character in app_id)
            or app_id in seen_ids
            or len(app["source"]) > 256 * 1024
        ):
            return None
        if "maintenance" in app and not isinstance(app["maintenance"], bool):
            return None
        seen_ids.add(app_id)
        validated_app = {key: app[key] for key in required_fields}
        if "maintenance" in app:
            validated_app["maintenance"] = app["maintenance"]
        validated_apps.append(validated_app)
    return validated_apps


def refresh_store_catalog():
    global STORE_APPS
    request = urllib.request.Request(
        STORE_CATALOG_URL,
        headers={"User-Agent": "PYOS Store/1.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            if urllib.parse.urlsplit(response.geturl()).hostname != "raw.githubusercontent.com":
                return False
            content = response.read(1024 * 1024 + 1)
        if len(content) > 1024 * 1024:
            return False
        module = ast.parse(content.decode("utf-8"))
        assignments = [
            node for node in module.body
            if isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "STORE_APPS"
                for target in node.targets
            )
        ]
        if len(assignments) != 1:
            return False
        catalog = validate_store_catalog(ast.literal_eval(assignments[0].value))
        if catalog is None:
            return False
    except (OSError, TimeoutError, UnicodeDecodeError, SyntaxError, ValueError, TypeError, urllib.error.URLError):
        return False

    STORE_APPS = catalog
    return True


def get_installed_store_apps():
    installed_apps = []
    for app in STORE_APPS:
        file_path = os.path.join(STORE_ROOT, app["id"], "main.py")
        if os.path.isfile(file_path) and not os.path.islink(file_path):
            installed_apps.append((app, file_path))
    return installed_apps


def get_python_apps():
    installed_by_id = {
        app["id"]: file_path for app, file_path in get_installed_store_apps()
    }
    return [
        (app, installed_by_id.get(app["id"]))
        for app in STORE_APPS
        if app.get("maintenance") or app["id"] in installed_by_id
    ]


def uninstall_store_app(app):
    app_directory = os.path.abspath(os.path.join(STORE_ROOT, app["id"]))
    if os.path.commonpath((STORE_ROOT, app_directory)) != STORE_ROOT:
        return False, "Thu muc cai dat khong hop le"
    if os.path.islink(app_directory):
        return False, "Thu muc cai dat khong hop le"
    if not os.path.isdir(app_directory):
        return False, "Ung dung chua duoc cai dat"

    try:
        shutil.rmtree(app_directory)
    except OSError:
        return False, "Go cai dat that bai"
    return True, "Go cai dat thanh cong"


def install_store_app(app):
    if app.get("maintenance"):
        return False, "Ung dung dang bao tri"

    app_directory = os.path.join(STORE_ROOT, app["id"])
    file_path = os.path.join(app_directory, "main.py")
    if os.path.isfile(file_path) and not os.path.islink(file_path):
        return False, "Ung dung da duoc tai"

    try:
        os.makedirs(app_directory, exist_ok=True)
        with open(file_path, "x", encoding="utf-8") as app_file:
            app_file.write(app["source"])
    except FileExistsError:
        return False, "Ung dung da duoc tai"
    except OSError:
        return False, "Tai that bai"
    return True, "Tai thanh cong"


def append_console_output(output_lines, text):
    text = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", text)
    text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\t", "    ")
    text = "".join(character for character in text if character == "\n" or character.isprintable())
    if not output_lines:
        output_lines.append("")
    parts = text.split("\n")
    output_lines[-1] += parts[0]
    output_lines.extend(parts[1:])
    del output_lines[:-500]


def run_python_file(stdscr, file_path, selected_app):
    absolute_path = os.path.abspath(file_path)
    try:
        process = subprocess.Popen(
            [sys.executable, "-u", absolute_path],
            cwd=os.path.dirname(absolute_path),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=0,
        )
        os.set_blocking(process.stdout.fileno(), False)
    except OSError as error:
        return f"Khong the chay file: {error}"

    output_lines = [""]
    input_buffer = ""
    try:
        curses.curs_set(0)
    except curses.error:
        pass

    try:
        while True:
            while True:
                try:
                    output = os.read(process.stdout.fileno(), 4096)
                except BlockingIOError:
                    break
                except OSError:
                    break
                if not output:
                    break
                append_console_output(output_lines, output.decode("utf-8", errors="replace"))

            return_code = process.poll()
            running = return_code is None
            status_message = (
                "Nhap input, ENTER: Gui  ESC: Dung"
                if running
                else f"Ket thuc; ma thoat {return_code}  ENTER/ESC: Ve"
            )

            if draw_desktop(stdscr, selected_app, "PYTHON"):
                layout = get_desktop_layout(stdscr)
                window_height = layout["main_height"] - 2
                window_width = layout["left_width"] - 2
                window = curses.newwin(
                    window_height,
                    window_width,
                    layout["main_y"] + 1,
                    layout["left_x"] + 1,
                )
                window.erase()
                window.addnstr(0, 0, f"FILE: {os.path.basename(absolute_path)}", window_width)
                visible_rows = window_height - 3
                for row, line in enumerate(output_lines[-visible_rows:]):
                    window.addnstr(1 + row, 0, line, window_width)
                input_label = f"> {input_buffer}" if running else ""
                window.addnstr(window_height - 2, 0, input_label, window_width)
                window.addnstr(window_height - 1, 0, status_message, window_width)
                window.refresh()

            stdscr.timeout(50)
            try:
                key = stdscr.get_wch()
            except curses.error:
                key = None
            finally:
                stdscr.timeout(-1)

            if key is None:
                continue
            if key in (27, "\x1b"):
                if process.poll() is None:
                    process.terminate()
                    try:
                        process.wait(timeout=0.5)
                    except subprocess.TimeoutExpired:
                        process.kill()
                        process.wait()
                    return "Da dung file"
                return f"Chay xong; ma thoat {process.returncode}"
            if process.poll() is not None:
                if key in (10, 13, curses.KEY_ENTER, "\n", "\r"):
                    if running:
                        continue
                    return f"Chay xong; ma thoat {process.returncode}"
                continue
            if key in (10, 13, curses.KEY_ENTER, "\n", "\r"):
                output_lines.append(f"> {input_buffer}")
                output_lines.append("")
                try:
                    process.stdin.write((input_buffer + "\n").encode("utf-8"))
                    process.stdin.flush()
                except OSError:
                    append_console_output(output_lines, "\nKhong the gui input\n")
                input_buffer = ""
            elif key in (curses.KEY_BACKSPACE, 8, 127, "\x7f", "\b"):
                input_buffer = input_buffer[:-1]
            elif isinstance(key, str) and key.isprintable() and len(input_buffer) < 256:
                input_buffer += key
    finally:
        if process.poll() is None:
            process.terminate()
            try:
                process.wait(timeout=0.5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
        process.stdin.close()
        process.stdout.close()


def show_gallery_image(stdscr, image_path):
    if not (os.environ.get("KITTY_WINDOW_ID") or os.environ.get("TERM") == "xterm-kitty"):
        return "Can chay GALLERY trong Kitty terminal"

    kitten = shutil.which("kitten")
    kitty = shutil.which("kitty")
    if kitten:
        icat = [kitten, "icat"]
        clear_image = [kitten, "icat", "--clear", "--silent"]
    elif kitty:
        icat = [kitty, "+kitten", "icat"]
        clear_image = [kitty, "+kitten", "icat", "--clear", "--silent"]
    else:
        return "Khong tim thay Kitty icat"

    layout = get_desktop_layout(stdscr)
    place = (
        f"{layout['left_width'] - 4}x{layout['main_height'] - 4}"
        f"@{layout['left_x'] + 2}x{layout['main_y'] + 2}"
    )
    curses.def_prog_mode()
    curses.endwin()
    try:
        result = subprocess.run(
            [*icat, "--place", place, "--align", "center", "--scale-up=no", "--hold", image_path],
            check=False,
        )
        if result.returncode == 0:
            return "Da dong xem anh"
        return "Kitty khong the hien anh nay"
    except OSError:
        return "Khong the chay Kitty icat"
    finally:
        subprocess.run(clear_image, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        curses.reset_prog_mode()


def choose_image_from_files(stdscr, selected_app):
    current_directory = FILES_ROOT
    selected_index = 0
    offset = 0

    while True:
        if not draw_desktop(stdscr, selected_app, "GALLERY"):
            if stdscr.getch() == 27:
                return None
            continue

        layout = get_desktop_layout(stdscr)
        window_height = layout["main_height"] - 2
        window_width = layout["left_width"] - 2
        visible_rows = window_height - 4
        entries, _ = get_file_entries(current_directory, FILES_ROOT)
        entries = [
            entry for entry in entries
            if entry[1] or entry[2] or (
                os.path.splitext(entry[0])[1].casefold() in IMAGE_EXTENSIONS
                and not os.path.islink(os.path.join(current_directory, entry[0]))
            )
        ]
        if selected_index >= len(entries):
            selected_index = max(0, len(entries) - 1)
        if selected_index < offset:
            offset = selected_index
        elif selected_index >= offset + visible_rows:
            offset = selected_index - visible_rows + 1

        window = curses.newwin(
            window_height,
            window_width,
            layout["main_y"] + 1,
            layout["left_x"] + 1,
        )
        relative_directory = os.path.relpath(current_directory, FILES_ROOT)
        path_label = "Chon anh tu FILES" if relative_directory == "." else relative_directory
        window.addnstr(0, 0, path_label, window_width)
        if entries:
            for row, item_index in enumerate(
                range(offset, min(offset + visible_rows, len(entries)))
            ):
                name, is_directory, is_parent = entries[item_index]
                label = "[DIR] .." if is_parent else f"[DIR] {name}/" if is_directory else name
                attributes = curses.A_REVERSE if item_index == selected_index else curses.A_NORMAL
                window.addnstr(1 + row, 0, label, window_width, attributes)
        else:
            window.addnstr(2, 0, "Khong co anh trong FILES", window_width)
        window.addnstr(window_height - 2, 0, "UP/DOWN: Chon  ENTER: Mo/Chon  ESC: Huy", window_width)
        window.refresh()

        key = stdscr.getch()
        if key == 27:
            return None
        if key == curses.KEY_UP and entries:
            selected_index = max(0, selected_index - 1)
        elif key == curses.KEY_DOWN and entries:
            selected_index = min(len(entries) - 1, selected_index + 1)
        elif key in (10, 13, curses.KEY_ENTER) and entries:
            name, is_directory, is_parent = entries[selected_index]
            if is_parent:
                current_directory = os.path.dirname(current_directory)
                selected_index = 0
                offset = 0
            elif is_directory:
                target_directory = os.path.abspath(os.path.join(current_directory, name))
                if os.path.commonpath((FILES_ROOT, target_directory)) == FILES_ROOT:
                    current_directory = target_directory
                    selected_index = 0
                    offset = 0
            else:
                return os.path.join(current_directory, name)


def wall_image_name_dialog(stdscr):
    height, width = stdscr.getmaxyx()
    dialog_height = 7
    dialog_width = min(50, width - 4)
    top = (height - dialog_height) // 2
    left = (width - dialog_width) // 2
    dialog = curses.newwin(dialog_height, dialog_width, top, left)
    dialog.keypad(True)
    filename = ""

    while True:
        dialog.erase()
        dialog.box()
        dialog.addstr(0, 2, " SAVE PNG ")
        dialog.addstr(2, 2, "Ten anh moi:")
        dialog.addnstr(3, 2, f"> {filename}", dialog_width - 4)
        dialog.addstr(5, 2, "ENTER: Luu  ESC: Huy")
        dialog.move(3, min(dialog_width - 2, 4 + len(filename)))
        dialog.refresh()

        key = dialog.get_wch()
        if key in (10, 13, curses.KEY_ENTER, "\n", "\r"):
            return filename.strip() or None
        if key in (27, "\x1b"):
            return None
        if key in (curses.KEY_BACKSPACE, 127, 8, "\x7f", "\b"):
            filename = filename[:-1]
        elif isinstance(key, str) and key.isprintable() and len(filename) < dialog_width - 8:
            filename += key


def wall_web_url_dialog(stdscr):
    height, width = stdscr.getmaxyx()
    dialog_height = 7
    dialog_width = min(60, width - 4)
    top = (height - dialog_height) // 2
    left = (width - dialog_width) // 2
    dialog = curses.newwin(dialog_height, dialog_width, top, left)
    dialog.keypad(True)
    url = ""

    while True:
        dialog.erase()
        dialog.box()
        dialog.addstr(0, 2, " DOWNLOAD IMAGE ")
        dialog.addstr(2, 2, "Paste direct image URL:")
        visible_url = url[-(dialog_width - 8):]
        dialog.addnstr(3, 2, f"> {visible_url}", dialog_width - 4)
        dialog.addstr(5, 2, "ENTER: Tai  ESC: Huy")
        dialog.move(3, min(dialog_width - 2, 4 + len(visible_url)))
        dialog.refresh()

        key = dialog.get_wch()
        if key in (10, 13, curses.KEY_ENTER, "\n", "\r"):
            return url.strip() or None
        if key in (27, "\x1b"):
            return None
        if key in (curses.KEY_BACKSPACE, 127, 8, "\x7f", "\b"):
            url = url[:-1]
        elif isinstance(key, str) and key.isprintable() and len(url) < 2048:
            url += key


def create_wall_image(stdscr, selected_app):
    canvas_width = 22
    canvas_height = 10
    pixels = [[0 for _ in range(canvas_width)] for _ in range(canvas_height)]
    cursor_x = 0
    cursor_y = 0
    selected_color = 1
    status_message = "Mui ten ve  C mau  E gom  X xoa het  S luu"
    erase_mode = False
    color_mode = False
    color_labels = ["Nen", "Do", "Vang", "Kem", "Xanh la", "Lam", "Tim", "Trang"]

    try:
        if curses.has_colors():
            curses.start_color()
            for pair_id, terminal_color in enumerate(PAINT_CURSES_COLORS, start=1):
                curses.init_pair(pair_id, terminal_color, terminal_color)
            color_mode = True
    except curses.error:
        color_mode = False

    while True:
        if not draw_desktop(stdscr, selected_app, "GALLERY"):
            if stdscr.getch() == 27:
                return None
            continue

        layout = get_desktop_layout(stdscr)
        window_height = layout["main_height"] - 2
        window_width = layout["left_width"] - 2
        visible_width = min(canvas_width, max(3, (window_width - 2) // 2))
        visible_height = min(canvas_height, max(3, window_height - 5))
        cursor_x = min(cursor_x, visible_width - 1)
        cursor_y = min(cursor_y, visible_height - 1)
        window = curses.newwin(
            window_height,
            window_width,
            layout["main_y"] + 1,
            layout["left_x"] + 1,
        )
        window.addnstr(0, 0, "NEW IMAGE - WALL", window_width)

        for row in range(visible_height):
            for column in range(visible_width):
                pixel_color = pixels[row][column]
                if color_mode:
                    cell = "  "
                    attributes = curses.color_pair(pixel_color + 1)
                else:
                    cell = ("  ", "##", "++", "**", "==", "@@", "oo", "[]")[pixel_color]
                    attributes = curses.A_NORMAL
                if row == cursor_y and column == cursor_x:
                    cell = "[]"
                    attributes = curses.A_REVERSE | curses.A_BOLD
                window.addstr(1 + row, column * 2, cell, attributes)

        palette_y = 1 + visible_height
        window.addnstr(palette_y, 0, f"Mau: {color_labels[selected_color]} (C doi)", window_width)
        brush_label = "GOM" if erase_mode else "VE"
        window.addnstr(window_height - 3, 0, f"Mui ten: {brush_label} lien tuc  SPACE: diem", window_width)
        window.addnstr(window_height - 2, 0, "C: Mau E: Gom X: Xoa het S: Luu", window_width)
        window.addnstr(window_height - 1, 0, status_message, window_width)
        window.refresh()

        key = stdscr.getch()
        if key == 27:
            return None
        if key == curses.KEY_UP:
            pixels[cursor_y][cursor_x] = 0 if erase_mode else selected_color
            cursor_y = max(0, cursor_y - 1)
            pixels[cursor_y][cursor_x] = 0 if erase_mode else selected_color
        elif key == curses.KEY_DOWN:
            pixels[cursor_y][cursor_x] = 0 if erase_mode else selected_color
            cursor_y = min(visible_height - 1, cursor_y + 1)
            pixels[cursor_y][cursor_x] = 0 if erase_mode else selected_color
        elif key == curses.KEY_LEFT:
            pixels[cursor_y][cursor_x] = 0 if erase_mode else selected_color
            cursor_x = max(0, cursor_x - 1)
            pixels[cursor_y][cursor_x] = 0 if erase_mode else selected_color
        elif key == curses.KEY_RIGHT:
            pixels[cursor_y][cursor_x] = 0 if erase_mode else selected_color
            cursor_x = min(visible_width - 1, cursor_x + 1)
            pixels[cursor_y][cursor_x] = 0 if erase_mode else selected_color
        elif key == ord(" "):
            pixels[cursor_y][cursor_x] = 0 if erase_mode else selected_color
            status_message = "Da xoa pixel" if erase_mode else "Da ve pixel"
        elif key in (ord("c"), ord("C")):
            selected_color = selected_color % (len(PAINT_RGB) - 1) + 1
            erase_mode = False
            status_message = f"Mau: {color_labels[selected_color]}"
        elif key in (ord("e"), ord("E")):
            erase_mode = not erase_mode
            status_message = "Da bat gom" if erase_mode else "Da tat gom"
        elif key in (ord("x"), ord("X")):
            pixels = [[0 for _ in range(canvas_width)] for _ in range(canvas_height)]
            status_message = "Da xoa toan bo canvas"
        elif key in (ord("s"), ord("S")):
            filename = wall_image_name_dialog(stdscr)
            if filename is None:
                status_message = "Da huy luu anh"
                continue
            image_path, status_message = save_wall_drawing(filename, pixels)
            if image_path:
                return image_path


def gallery_screen(stdscr, selected_app):
    selected_index = 0
    offset = 0
    status_message = "N:Tao W:Web I:FILES D:Xoa"
    try:
        os.makedirs(WALL_ROOT, exist_ok=True)
    except OSError:
        status_message = "Khong the tao ~/PYOS/wall"

    while True:
        if not draw_desktop(stdscr, selected_app, "GALLERY"):
            if stdscr.getch() == 27:
                return
            continue

        layout = get_desktop_layout(stdscr)
        window_height = layout["main_height"] - 2
        window_width = layout["left_width"] - 2
        visible_rows = window_height - 5
        image_paths = get_gallery_images(WALL_ROOT)
        if selected_index >= len(image_paths):
            selected_index = max(0, len(image_paths) - 1)
        if selected_index < offset:
            offset = selected_index
        elif selected_index >= offset + visible_rows:
            offset = selected_index - visible_rows + 1

        window = curses.newwin(
            window_height,
            window_width,
            layout["main_y"] + 1,
            layout["left_x"] + 1,
        )
        window.addnstr(0, 0, "Anh trong ~/PYOS/wall", window_width)
        if image_paths:
            for row, item_index in enumerate(
                range(offset, min(offset + visible_rows, len(image_paths)))
            ):
                image_name = "".join(
                    character if character.isprintable() else "?"
                    for character in image_paths[item_index]
                )
                attributes = curses.A_REVERSE if item_index == selected_index else curses.A_NORMAL
                window.addnstr(1 + row, 0, image_name, window_width, attributes)
        else:
            window.addnstr(2, 0, "WALL trong - N: Tao  W: Web", window_width)

        window.addnstr(window_height - 3, 0, "UP/DOWN: Chon  N: Tao  W: Web", window_width)
        window.addnstr(window_height - 2, 0, "I: FILES  D: Xoa  ENTER: Xem  ESC: Ve", window_width)
        window.addnstr(window_height - 1, 0, status_message, window_width)
        window.refresh()

        key = stdscr.getch()
        if key == 27:
            return
        if key == curses.KEY_UP and image_paths:
            selected_index = max(0, selected_index - 1)
        elif key == curses.KEY_DOWN and image_paths:
            selected_index = min(len(image_paths) - 1, selected_index + 1)
        elif key in (ord("n"), ord("N")):
            image_path = create_wall_image(stdscr, selected_app)
            if image_path:
                image_paths = get_gallery_images(WALL_ROOT)
                selected_index = image_paths.index(os.path.relpath(image_path, WALL_ROOT))
                status_message = f"Da tao: {os.path.basename(image_path)}"
        elif key in (ord("i"), ord("I")):
            source_path = choose_image_from_files(stdscr, selected_app)
            if source_path:
                added, status_message = copy_image_to_wall(source_path)
                if added:
                    image_paths = get_gallery_images(WALL_ROOT)
                    selected_index = image_paths.index(os.path.basename(source_path))
        elif key in (ord("w"), ord("W")):
            url = wall_web_url_dialog(stdscr)
            if url:
                image_path, status_message = download_wall_image(url)
                if image_path:
                    image_paths = get_gallery_images(WALL_ROOT)
                    selected_index = image_paths.index(os.path.relpath(image_path, WALL_ROOT))
        elif key in (ord("d"), ord("D")):
            if not image_paths:
                status_message = "Khong co anh de xoa"
            else:
                image_path = image_paths[selected_index]
                if confirm_delete_dialog(stdscr, os.path.basename(image_path)):
                    try:
                        os.remove(os.path.join(WALL_ROOT, image_path))
                        status_message = f"Da xoa: {os.path.basename(image_path)}"
                        selected_index = max(0, selected_index - 1)
                    except OSError:
                        status_message = "Khong the xoa anh"
                else:
                    status_message = "Da huy xoa"
        elif key in (10, 13, curses.KEY_ENTER) and image_paths:
            file_path = os.path.join(WALL_ROOT, image_paths[selected_index])
            status_message = show_gallery_image(stdscr, file_path)


def confirm_uninstall_dialog(stdscr, app_name):
    height, width = stdscr.getmaxyx()
    dialog_height = 7
    dialog_width = min(60, width - 4)
    top = (height - dialog_height) // 2
    left = (width - dialog_width) // 2
    dialog = curses.newwin(dialog_height, dialog_width, top, left)
    dialog.keypad(True)
    dialog.box()
    dialog.addnstr(1, 2, "Go cai dat ung dung nay?", dialog_width - 4)
    dialog.addnstr(3, 2, app_name, dialog_width - 4)
    dialog.addnstr(5, 2, "Y: Go cai dat   N/ESC: Huy", dialog_width - 4)
    dialog.refresh()
    return dialog.getch() in (ord("y"), ord("Y"))


def python_run_screen(stdscr, selected_app):
    selected_index = 0
    offset = 0
    status_message = "Chon file Python de chay"

    while True:
        if not draw_desktop(stdscr, selected_app, "PYTHON"):
            if stdscr.getch() == 27:
                return
            continue

        layout = get_desktop_layout(stdscr)
        window_height = layout["main_height"] - 2
        window_width = layout["left_width"] - 2
        visible_rows = window_height - 4
        python_apps = get_python_apps()
        if selected_index >= len(python_apps):
            selected_index = max(0, len(python_apps) - 1)

        if selected_index < offset:
            offset = selected_index
        elif selected_index >= offset + visible_rows:
            offset = selected_index - visible_rows + 1

        window = curses.newwin(
            window_height,
            window_width,
            layout["main_y"] + 1,
            layout["left_x"] + 1,
        )
        if python_apps:
            for row, item_index in enumerate(
                range(offset, min(offset + visible_rows, len(python_apps)))
            ):
                app, _ = python_apps[item_index]
                name = "".join(
                    character if character.isprintable() else "?"
                    for character in app["name"]
                )
                if app.get("maintenance"):
                    name = f"{name} [BAO TRI]"
                attributes = curses.A_REVERSE if item_index == selected_index else curses.A_NORMAL
                window.addnstr(1 + row, 0, name, window_width, attributes)
        else:
            message = "Chua tai ung dung nao tu STORE"
            window.addnstr(1, 0, message, window_width)

        window.addnstr(window_height - 2, 0, "ENTER: Chay  U: Go cai dat  ESC: Ve", window_width)
        window.addnstr(window_height - 1, 0, status_message, window_width)
        window.refresh()

        key = stdscr.getch()
        if key == 27:
            return
        if key == curses.KEY_UP and python_apps:
            selected_index = max(0, selected_index - 1)
        elif key == curses.KEY_DOWN and python_apps:
            selected_index = min(len(python_apps) - 1, selected_index + 1)
        elif key in (10, 13, curses.KEY_ENTER) and python_apps:
            app, file_path = python_apps[selected_index]
            if app.get("maintenance"):
                status_message = f"{app['name']} dang bao tri"
            elif file_path:
                status_message = run_python_file(stdscr, file_path, selected_app)
        elif key in (ord("u"), ord("U")):
            if not python_apps:
                status_message = "Khong co ung dung de go"
                continue

            app, file_path = python_apps[selected_index]
            if not file_path:
                status_message = "Ung dung chua duoc tai"
                continue
            if confirm_uninstall_dialog(stdscr, app["name"]):
                removed, status_message = uninstall_store_app(app)
                if removed:
                    selected_index = max(0, selected_index - 1)
            else:
                status_message = "Da huy go cai dat"


def python_editor(stdscr, file_path, selected_app):
    try:
        with open(file_path, "r", encoding="utf-8") as source_file:
            lines = source_file.read().splitlines()
    except (OSError, UnicodeError):
        return "Khong the mo file bang UTF-8"

    if not lines:
        lines = [""]

    cursor_y = 0
    cursor_x = 0
    scroll_y = 0
    status_message = "San sang"
    curses.curs_set(1)
    terminal_fd = sys.stdin.fileno()
    terminal_settings = termios.tcgetattr(terminal_fd)
    editor_settings = terminal_settings.copy()
    editor_settings[0] &= ~termios.IXON
    termios.tcsetattr(terminal_fd, termios.TCSANOW, editor_settings)

    while True:
        if not draw_desktop(stdscr, selected_app, "PYTHON"):
            key = stdscr.get_wch()
            if key == "\x1b":
                termios.tcsetattr(terminal_fd, termios.TCSANOW, terminal_settings)
                curses.curs_set(0)
                return ""
            continue

        layout = get_desktop_layout(stdscr)
        editor_height = layout["main_height"] - 2
        editor_width = layout["left_width"] - 2
        visible_rows = editor_height - 4

        if cursor_y < scroll_y:
            scroll_y = cursor_y
        elif cursor_y >= scroll_y + visible_rows:
            scroll_y = cursor_y - visible_rows + 1

        editor_window = curses.newwin(
            editor_height,
            editor_width,
            layout["main_y"] + 1,
            layout["left_x"] + 1,
        )
        editor_window.addnstr(0, 0, os.path.basename(file_path), editor_width)
        for row in range(visible_rows):
            line_index = scroll_y + row
            if line_index < len(lines):
                editor_window.addnstr(row + 1, 0, lines[line_index], editor_width)

        editor_window.addnstr(editor_height - 2, 0, "Ctrl+S: Luu  F5: Chay  ESC: Ve", editor_width)
        editor_window.addnstr(editor_height - 1, 0, status_message, editor_width)
        editor_window.move(cursor_y - scroll_y + 1, min(cursor_x, editor_width - 1))
        editor_window.refresh()

        key = stdscr.get_wch()
        if key == "\x1b":
            termios.tcsetattr(terminal_fd, termios.TCSANOW, terminal_settings)
            curses.curs_set(0)
            return ""
        if key in ("\x13", 19):
            if save_editor_file(file_path, lines):
                status_message = "Da luu thanh cong"
            else:
                status_message = "Luu that bai"
        elif key == curses.KEY_F5:
            if not save_editor_file(file_path, lines):
                status_message = "Luu that bai; chua chay"
                continue
            status_message = run_python_file(stdscr, file_path, selected_app)
            curses.curs_set(1)
        elif key == curses.KEY_UP:
            cursor_y = max(0, cursor_y - 1)
            cursor_x = min(cursor_x, len(lines[cursor_y]))
        elif key == curses.KEY_DOWN:
            cursor_y = min(len(lines) - 1, cursor_y + 1)
            cursor_x = min(cursor_x, len(lines[cursor_y]))
        elif key == curses.KEY_LEFT:
            if cursor_x:
                cursor_x -= 1
            elif cursor_y:
                cursor_y -= 1
                cursor_x = len(lines[cursor_y])
        elif key == curses.KEY_RIGHT:
            if cursor_x < len(lines[cursor_y]):
                cursor_x += 1
            elif cursor_y < len(lines) - 1:
                cursor_y += 1
                cursor_x = 0
        elif key in (curses.KEY_BACKSPACE, 127, 8):
            if cursor_x:
                lines[cursor_y] = lines[cursor_y][:cursor_x - 1] + lines[cursor_y][cursor_x:]
                cursor_x -= 1
            elif cursor_y:
                cursor_x = len(lines[cursor_y - 1])
                lines[cursor_y - 1] += lines.pop(cursor_y)
                cursor_y -= 1
        elif key == curses.KEY_DC:
            if cursor_x < len(lines[cursor_y]):
                lines[cursor_y] = lines[cursor_y][:cursor_x] + lines[cursor_y][cursor_x + 1:]
            elif cursor_y < len(lines) - 1:
                lines[cursor_y] += lines.pop(cursor_y + 1)
        elif key in (10, 13, curses.KEY_ENTER, "\n", "\r"):
            lines.insert(cursor_y + 1, lines[cursor_y][cursor_x:])
            lines[cursor_y] = lines[cursor_y][:cursor_x]
            cursor_y += 1
            cursor_x = 0
        elif isinstance(key, str) and key.isprintable():
            lines[cursor_y] = lines[cursor_y][:cursor_x] + key + lines[cursor_y][cursor_x:]
            cursor_x += len(key)


def store_screen(stdscr, selected_app):
    selected_index = 0
    status_message = (
        "GitHub Raw da cap nhat"
        if refresh_store_catalog()
        else "Khong ket noi duoc; dung catalog gan nhat"
    )

    while True:
        height, width = stdscr.getmaxyx()
        if height < 22 or width < 64:
            stdscr.clear()
            stdscr.addstr(0, 0, "Terminal too small!")
            stdscr.refresh()
            if stdscr.getch() == 27:
                return
            continue

        if not draw_desktop(stdscr, selected_app, "STORE"):
            continue

        layout = get_desktop_layout(stdscr)
        window_height = layout["main_height"] - 2
        window_width = layout["left_width"] - 2
        installed_apps = {app["id"] for app, _ in get_installed_store_apps()}

        window = curses.newwin(
            window_height,
            window_width,
            layout["main_y"] + 1,
            layout["left_x"] + 1,
        )
        window.addnstr(0, 0, "App tu GitHub Raw", window_width)

        for index, app in enumerate(STORE_APPS):
            if app.get("maintenance"):
                state = "BAO TRI"
            else:
                state = "DA TAI" if app["id"] in installed_apps else "CAI DAT"
            label = f"{app['name']:<14} {app['category']:<10} {app['size']:<8} [{state}]"
            attributes = curses.A_REVERSE if index == selected_index else curses.A_NORMAL
            window.addnstr(2 + index, 0, label, window_width, attributes)

        app = STORE_APPS[selected_index]
        window.addnstr(window_height - 4, 0, f"Mo ta: {app['description']}", window_width)
        window.addnstr(window_height - 3, 0, f"Nhom: {app['category']}  Size: {app['size']}", window_width)
        window.addnstr(window_height - 2, 0, "UP/DOWN: Chon  ENTER: Cai dat  ESC: Ve", window_width)
        window.addnstr(window_height - 1, 0, status_message, window_width)
        window.refresh()

        key = stdscr.getch()
        if key == 27:
            return
        if key == curses.KEY_UP:
            selected_index = max(0, selected_index - 1)
            status_message = "Chon ung dung va nhan ENTER de cai dat"
        elif key == curses.KEY_DOWN:
            selected_index = min(len(STORE_APPS) - 1, selected_index + 1)
            status_message = "Chon ung dung va nhan ENTER de cai dat"
        elif key in (10, 13, curses.KEY_ENTER):
            app = STORE_APPS[selected_index]
            _, status_message = install_store_app(app)
            status_message = f"{status_message}: {app['name']}"


def draw_game_panel(stdscr, selected_app, title):
    if not draw_desktop(stdscr, selected_app, "GAMES"):
        return None

    layout = get_desktop_layout(stdscr)
    window_height = layout["main_height"] - 2
    window_width = layout["left_width"] - 2
    window = curses.newwin(
        window_height,
        window_width,
        layout["main_y"] + 1,
        layout["left_x"] + 1,
    )
    window.erase()
    window.addnstr(0, 0, title, window_width)
    return window, window_height, window_width


def games_screen(stdscr, selected_app):
    games = ("Doan so", "Ran san moi")
    selected_index = 0

    while True:
        panel = draw_game_panel(stdscr, selected_app, "GAME CAI SAN")
        if panel is None:
            if stdscr.getch() == 27:
                return
            continue

        window, window_height, window_width = panel
        for index, name in enumerate(games):
            attributes = curses.A_REVERSE if index == selected_index else curses.A_NORMAL
            window.addnstr(2 + index, 0, name, window_width, attributes)
        description = "Nhap so tu 1 den 10" if selected_index == 0 else "Dung mui ten de dieu khien ran"
        window.addnstr(window_height - 4, 0, description, window_width)
        window.addnstr(window_height - 2, 0, "UP/DOWN: Chon  ENTER: Choi  ESC: Ve", window_width)
        window.refresh()

        key = stdscr.getch()
        if key == 27:
            return
        if key == curses.KEY_UP:
            selected_index = max(0, selected_index - 1)
        elif key == curses.KEY_DOWN:
            selected_index = min(len(games) - 1, selected_index + 1)
        elif key in (10, 13, curses.KEY_ENTER):
            if selected_index == 0:
                guess_number_game(stdscr, selected_app)
            else:
                snake_game(stdscr, selected_app)


def guess_number_game(stdscr, selected_app):
    while True:
        answer = random.randint(1, 10)
        guess = ""
        attempts = 0
        message = "Nhap mot so tu 1 den 10"
        won = False

        while True:
            panel = draw_game_panel(stdscr, selected_app, "DOAN SO")
            if panel is None:
                if stdscr.getch() == 27:
                    return
                continue

            window, window_height, window_width = panel
            window.addnstr(2, 0, "So cua ban: " + guess, window_width)
            window.addnstr(window_height - 4, 0, f"So lan doan: {attempts}", window_width)
            hint = "Chinh xac! N: Choi lai  ESC: Ve" if won else "0-9: Nhap  ENTER: Doan  ESC: Ve"
            window.addnstr(window_height - 2, 0, hint, window_width)
            window.addnstr(window_height - 1, 0, message, window_width)
            window.refresh()

            key = stdscr.getch()
            if key == 27:
                return
            if won:
                if key in (ord("n"), ord("N")):
                    break
                continue
            if key in (10, 13, curses.KEY_ENTER):
                if not guess:
                    message = "Hay nhap mot so"
                    continue
                value = int(guess)
                if not 1 <= value <= 10:
                    message = "Chi nhap so tu 1 den 10"
                    guess = ""
                    continue
                attempts += 1
                if value == answer:
                    won = True
                    message = "Ban da doan dung!"
                else:
                    message = "So can tim lon hon" if value < answer else "So can tim nho hon"
                    guess = ""
            elif key in (curses.KEY_BACKSPACE, 8, 127):
                guess = guess[:-1]
            elif ord("0") <= key <= ord("9") and len(guess) < 2:
                guess += chr(key)


def make_snake_food(board_height, board_width, snake):
    occupied = set(snake)
    empty_cells = [
        (row, column)
        for row in range(board_height)
        for column in range(board_width)
        if (row, column) not in occupied
    ]
    return random.choice(empty_cells) if empty_cells else None


def step_snake(snake, direction, food, board_height, board_width):
    head_row = snake[0][0] + direction[0]
    head_column = snake[0][1] + direction[1]
    next_head = (head_row, head_column)
    if not (0 <= head_row < board_height and 0 <= head_column < board_width):
        return snake, food, False, False

    eating = next_head == food
    occupied = snake if eating else snake[:-1]
    if next_head in occupied:
        return snake, food, False, False

    next_snake = [next_head, *snake]
    if not eating:
        next_snake.pop()
        return next_snake, food, False, True
    return next_snake, make_snake_food(board_height, board_width, next_snake), True, True


def snake_game(stdscr, selected_app):
    while True:
        panel = draw_game_panel(stdscr, selected_app, "RAN SAN MOI")
        if panel is None:
            if stdscr.getch() == 27:
                return
            continue
        _, window_height, window_width = panel
        board_height = window_height - 6
        board_width = window_width - 2
        if board_height < 3 or board_width < 6:
            window, _, _ = panel
            window.addnstr(2, 0, "Khung game qua nho", window_width)
            window.addnstr(window_height - 1, 0, "ESC: Ve", window_width)
            window.refresh()
            if stdscr.getch() == 27:
                return
            continue

        while True:
            center_row = board_height // 2
            center_column = board_width // 2
            snake = [
                (center_row, center_column),
                (center_row, center_column - 1),
                (center_row, center_column - 2),
            ]
            direction = (0, 1)
            food = make_snake_food(board_height, board_width, snake)
            score = 0
            alive = True

            while True:
                panel = draw_game_panel(stdscr, selected_app, f"RAN SAN MOI  DIEM: {score}")
                if panel is None:
                    if stdscr.getch() == 27:
                        stdscr.timeout(-1)
                        return
                    continue
                window, window_height, window_width = panel
                board_top = 1
                board_bottom = board_top + board_height + 1
                window.hline(board_top, 1, curses.ACS_HLINE, board_width)
                window.hline(board_bottom, 1, curses.ACS_HLINE, board_width)
                window.vline(board_top + 1, 0, curses.ACS_VLINE, board_height)
                window.vline(board_top + 1, window_width - 1, curses.ACS_VLINE, board_height)
                window.addch(board_top, 0, curses.ACS_ULCORNER)
                window.addch(board_top, window_width - 1, curses.ACS_URCORNER)
                window.addch(board_bottom, 0, curses.ACS_LLCORNER)
                window.addch(board_bottom, window_width - 1, curses.ACS_LRCORNER)
                for index, (row, column) in enumerate(snake):
                    character = "@" if index == 0 else "o"
                    window.addch(board_top + 1 + row, 1 + column, character)
                if food is not None:
                    window.addch(board_top + 1 + food[0], 1 + food[1], "*")
                message = "Thang! N: Choi lai  ESC: Ve" if food is None else "Dung! N: Choi lai  ESC: Ve"
                window.addnstr(window_height - 2, 0, "Arrows: Dieu khien ran", window_width)
                if not alive or food is None:
                    window.addnstr(window_height - 1, 0, message, window_width)
                window.refresh()

                stdscr.timeout(120 if alive and food is not None else -1)
                key = stdscr.getch()
                stdscr.timeout(-1)
                if key == 27:
                    return
                if not alive or food is None:
                    if key in (ord("n"), ord("N")):
                        break
                    continue

                directions = {
                    curses.KEY_UP: (-1, 0),
                    curses.KEY_DOWN: (1, 0),
                    curses.KEY_LEFT: (0, -1),
                    curses.KEY_RIGHT: (0, 1),
                }
                next_direction = directions.get(key)
                if next_direction and next_direction != (-direction[0], -direction[1]):
                    direction = next_direction

                snake, food, ate_food, alive = step_snake(
                    snake, direction, food, board_height, board_width
                )
                if ate_food:
                    score += 1


def draw_files_window(
    stdscr,
    selected_app,
    selected_file,
    current_directory,
    entries,
    offset,
    error_message,
    status_message,
):
    if not draw_desktop(stdscr, selected_app, "FILES"):
        return

    layout = get_desktop_layout(stdscr)
    window_height = layout["main_height"] - 2
    window_width = layout["left_width"] - 2
    window = curses.newwin(
        window_height,
        window_width,
        layout["main_y"] + 1,
        layout["left_x"] + 1,
    )

    relative_directory = os.path.relpath(current_directory, FILES_ROOT)
    path_label = "~/PYOS/files" if relative_directory == "." else f"~/PYOS/files/{relative_directory}"
    window.addnstr(0, 0, path_label, window_width)

    visible_rows = window_height - 4
    if not entries:
        message = error_message or "( Chua co file nao )"
        window.addnstr(window_height // 2, max(0, (window_width - len(message)) // 2), message, window_width)
    else:
        for row, item_index in enumerate(range(offset, min(offset + visible_rows, len(entries)))):
            name, is_directory, is_parent = entries[item_index]
            display_name = "".join(character if character.isprintable() else "?" for character in name)
            if is_parent:
                label = "[DIR] .."
            elif is_directory:
                label = f"[DIR] {display_name}/"
            else:
                label = f"      {display_name}"

            attributes = curses.A_REVERSE if item_index == selected_file else curses.A_NORMAL
            window.addnstr(2 + row, 0, label, window_width, attributes)

    new_file_hint = "N: New  D: Delete"
    back_hint = "ESC: Back"
    if status_message:
        window.addnstr(window_height - 2, 0, status_message, window_width)
    window.addnstr(window_height - 1, 0, f"{new_file_hint}   {back_hint}", window_width)

    window.refresh()


def files_screen(stdscr, selected):
    current_directory = FILES_ROOT
    selected_index = 0
    offset = 0
    status_message = ""

    while True:
        height, width = stdscr.getmaxyx()

        if height < 22 or width < 64:
            stdscr.clear()
            stdscr.addnstr(0, 0, "Terminal too small (minimum 64x22)", width - 1)
            stdscr.refresh()
            key = stdscr.getch()
            if key == 27:
                return
            continue

        entries, error_message = get_file_entries(current_directory, FILES_ROOT)
        if selected_index >= len(entries):
            selected_index = max(0, len(entries) - 1)

        visible_rows = get_desktop_layout(stdscr)["main_height"] - 6
        if selected_index < offset:
            offset = selected_index
        elif selected_index >= offset + visible_rows:
            offset = selected_index - visible_rows + 1

        draw_files_window(
            stdscr,
            selected,
            selected_index,
            current_directory,
            entries,
            offset,
            error_message,
            status_message,
        )
        key = stdscr.getch()

        if key in (27, ord("x"), ord("X")):
            return

        if key in (ord("n"), ord("N")):
            filename = new_file_dialog(stdscr)
            if filename is not None:
                created, status_message = create_empty_file(current_directory, filename)
                if created:
                    entries, _ = get_file_entries(current_directory, FILES_ROOT)
                    for index, entry in enumerate(entries):
                        if entry[0] == filename:
                            selected_index = index
                            break

        elif key in (ord("d"), ord("D")):
            if not entries:
                status_message = "Khong co file de xoa"
            else:
                name, is_directory, is_parent = entries[selected_index]
                if is_directory or is_parent:
                    status_message = "Hay chon mot file de xoa"
                elif confirm_delete_dialog(stdscr, name):
                    file_path = os.path.join(current_directory, name)
                    try:
                        os.remove(file_path)
                        status_message = f"Da xoa: {name}"
                        selected_index = max(0, selected_index - 1)
                    except OSError:
                        status_message = "Khong the xoa file"
                else:
                    status_message = "Da huy xoa"

        elif key == curses.KEY_UP and entries:
            selected_index = max(0, selected_index - 1)
            status_message = ""

        elif key == curses.KEY_DOWN and entries:
            selected_index = min(len(entries) - 1, selected_index + 1)
            status_message = ""

        elif key in (10, 13, curses.KEY_ENTER) and entries:
            name, is_directory, is_parent = entries[selected_index]
            if is_parent:
                current_directory = os.path.dirname(current_directory)
                selected_index = 0
                offset = 0
            elif is_directory:
                target_directory = os.path.abspath(os.path.join(current_directory, name))
                if os.path.commonpath((FILES_ROOT, target_directory)) == FILES_ROOT:
                    current_directory = target_directory
                    selected_index = 0
                    offset = 0
            elif not os.path.islink(os.path.join(current_directory, name)):
                status_message = python_editor(stdscr, os.path.join(current_directory, name), selected)
                curses.curs_set(0)


def placeholder_screen(stdscr, selected, app, message=None):
    while True:
        if not draw_desktop(stdscr, selected, app):
            if stdscr.getch() == 27:
                return
            continue

        layout = get_desktop_layout(stdscr)
        window = curses.newwin(
            layout["main_height"] - 2,
            layout["left_width"] - 2,
            layout["main_y"] + 1,
            layout["left_x"] + 1,
        )
        display_message = message or f"{app} chua duoc trien khai"
        window.addnstr(0, 0, display_message, layout["left_width"] - 2)
        window.addnstr(2, 0, "ESC: Quay lai Desktop", layout["left_width"] - 2)
        window.refresh()
        if stdscr.getch() == 27:
            return


def account_name_dialog(stdscr, current_name):
    height, width = stdscr.getmaxyx()
    dialog_height = 7
    dialog_width = min(50, width - 4)
    top = (height - dialog_height) // 2
    left = (width - dialog_width) // 2
    dialog = curses.newwin(dialog_height, dialog_width, top, left)
    dialog.keypad(True)
    name = current_name

    while True:
        dialog.erase()
        dialog.box()
        dialog.addstr(0, 2, " DISPLAY NAME ")
        dialog.addstr(2, 2, "Ten hien thi:")
        dialog.addnstr(3, 2, f"> {name}", dialog_width - 4)
        dialog.addstr(5, 2, "ENTER: Luu  ESC: Huy")
        dialog.move(3, min(dialog_width - 2, 4 + len(name)))
        dialog.refresh()

        key = dialog.get_wch()
        if key in (10, 13, curses.KEY_ENTER, "\n", "\r"):
            return name.strip() or None
        if key in (27, "\x1b"):
            return None
        if key in (curses.KEY_BACKSPACE, 127, 8, "\x7f", "\b"):
            name = name[:-1]
        elif isinstance(key, str) and key.isprintable() and len(name) < 32:
            name += key


def account_screen(stdscr, selected):
    status_message = "Ten hien thi duoc luu tren may nay"

    while True:
        if not draw_desktop(stdscr, selected, "ACCOUNT"):
            if stdscr.getch() == 27:
                return
            continue

        layout = get_desktop_layout(stdscr)
        window_height = layout["main_height"] - 2
        window_width = layout["left_width"] - 2
        window = curses.newwin(
            window_height,
            window_width,
            layout["main_y"] + 1,
            layout["left_x"] + 1,
        )
        window.addnstr(0, 0, "HO SO NGUOI DUNG", window_width)
        window.addnstr(2, 0, f"Ten hien thi: {load_account_name()}", window_width)
        window.addnstr(4, 0, "Ho so cuc bo; khong co dang nhap that", window_width)
        window.addnstr(window_height - 2, 0, "ENTER: Doi ten  ESC: Ve", window_width)
        window.addnstr(window_height - 1, 0, status_message, window_width)
        window.refresh()

        key = stdscr.getch()
        if key == 27:
            return
        if key in (10, 13, curses.KEY_ENTER):
            name = account_name_dialog(stdscr, load_account_name())
            if name is None:
                status_message = "Da huy"
            else:
                _, status_message = save_account_name(name)


def text_input_dialog(stdscr, title, prompt, initial="", max_length=128):
    height, width = stdscr.getmaxyx()
    dialog_height = 8
    dialog_width = min(70, width - 4)
    top = (height - dialog_height) // 2
    left = (width - dialog_width) // 2
    dialog = curses.newwin(dialog_height, dialog_width, top, left)
    dialog.keypad(True)
    value = initial

    while True:
        dialog.erase()
        dialog.box()
        dialog.addnstr(0, 2, f" {title} ", dialog_width - 4)
        dialog.addnstr(2, 2, prompt, dialog_width - 4)
        visible_value = value[-(dialog_width - 8):]
        dialog.addnstr(4, 2, f"> {visible_value}", dialog_width - 4)
        dialog.addnstr(6, 2, "ENTER: Xac nhan  ESC: Huy", dialog_width - 4)
        dialog.move(4, min(dialog_width - 2, 4 + len(visible_value)))
        dialog.refresh()

        key = dialog.get_wch()
        if key in (10, 13, curses.KEY_ENTER, "\n", "\r"):
            return value.strip()
        if key in (27, "\x1b"):
            return None
        if key in (curses.KEY_BACKSPACE, 8, 127, "\x7f", "\b"):
            value = value[:-1]
        elif isinstance(key, str) and key.isprintable() and len(value) < max_length:
            value += key


def quick_command_dialog(stdscr, name="", url=""):
    command_name = text_input_dialog(stdscr, "LENH NHANH", "Tu khoa (vd: gpt, yt)", name, 24)
    if command_name is None:
        return None
    command_url = text_input_dialog(stdscr, "LENH NHANH", "Dia chi HTTP/HTTPS", url, 2048)
    if command_url is None:
        return None
    return command_name, command_url


def confirm_quick_command_delete(stdscr, command_name):
    height, width = stdscr.getmaxyx()
    dialog_height = 7
    dialog_width = min(60, width - 4)
    top = (height - dialog_height) // 2
    left = (width - dialog_width) // 2
    dialog = curses.newwin(dialog_height, dialog_width, top, left)
    dialog.keypad(True)
    dialog.box()
    dialog.addnstr(1, 2, "Xoa lenh nhanh nay?", dialog_width - 4)
    dialog.addnstr(3, 2, command_name, dialog_width - 4)
    dialog.addnstr(5, 2, "Y: Xoa  N/ESC: Huy", dialog_width - 4)
    dialog.refresh()
    return dialog.getch() in (ord("y"), ord("Y"))


def quick_commands_screen(stdscr, selected, settings):
    commands = settings["quick_commands"]
    selected_index = 0
    offset = 0
    status_message = "A: Them  ENTER: Sua  D: Xoa"

    while True:
        if not draw_desktop(stdscr, selected, "LENH NHANH"):
            if stdscr.getch() == 27:
                return "Da huy"
            continue

        layout = get_desktop_layout(stdscr)
        window_height = layout["main_height"] - 2
        window_width = layout["left_width"] - 2
        visible_rows = max(1, window_height - 5)
        command_names = list(commands)
        if selected_index >= len(command_names):
            selected_index = max(0, len(command_names) - 1)
        if selected_index < offset:
            offset = selected_index
        elif selected_index >= offset + visible_rows:
            offset = selected_index - visible_rows + 1

        window = curses.newwin(
            window_height,
            window_width,
            layout["main_y"] + 1,
            layout["left_x"] + 1,
        )
        window.addnstr(0, 0, "Tu khoa -> dia chi web", window_width)
        if command_names:
            for row, item_index in enumerate(
                range(offset, min(offset + visible_rows, len(command_names)))
            ):
                name = command_names[item_index]
                label = f"{name} -> {commands[name]}"
                attributes = curses.A_REVERSE if item_index == selected_index else curses.A_NORMAL
                window.addnstr(1 + row, 0, label, window_width, attributes)
        else:
            window.addnstr(2, 0, "Chua co lenh nhanh", window_width)
        window.addnstr(window_height - 3, 0, "A: Them  ENTER: Sua  D: Xoa", window_width)
        window.addnstr(window_height - 2, 0, "Chi mo dia chi HTTP/HTTPS  ESC: Ve", window_width)
        window.addnstr(window_height - 1, 0, status_message, window_width)
        window.refresh()

        key = stdscr.getch()
        if key == 27:
            return status_message
        if key == curses.KEY_UP and command_names:
            selected_index = max(0, selected_index - 1)
        elif key == curses.KEY_DOWN and command_names:
            selected_index = min(len(command_names) - 1, selected_index + 1)
        elif key in (ord("a"), ord("A")):
            if len(commands) >= 20:
                status_message = "Chi duoc toi da 20 lenh"
                continue
            result = quick_command_dialog(stdscr)
            if result is None:
                status_message = "Da huy"
                continue
            normalized = normalize_quick_command(*result)
            if not normalized:
                status_message = "Tu khoa hoac dia chi khong hop le"
            elif normalized[0] in commands:
                status_message = "Tu khoa da ton tai"
            else:
                commands[normalized[0]] = normalized[1]
                selected_index = len(commands) - 1
                status_message = "Da them lenh nhanh"
                if not save_settings(settings):
                    status_message = "Khong the luu cai dat"
        elif key in (10, 13, curses.KEY_ENTER) and command_names:
            old_name = command_names[selected_index]
            result = quick_command_dialog(stdscr, old_name, commands[old_name])
            if result is None:
                status_message = "Da huy"
                continue
            normalized = normalize_quick_command(*result)
            if not normalized:
                status_message = "Tu khoa hoac dia chi khong hop le"
            elif normalized[0] != old_name and normalized[0] in commands:
                status_message = "Tu khoa da ton tai"
            else:
                del commands[old_name]
                commands[normalized[0]] = normalized[1]
                selected_index = list(commands).index(normalized[0])
                status_message = "Da cap nhat lenh nhanh"
                if not save_settings(settings):
                    status_message = "Khong the luu cai dat"
        elif key in (ord("d"), ord("D")) and command_names:
            name = command_names[selected_index]
            if confirm_quick_command_delete(stdscr, name):
                del commands[name]
                selected_index = max(0, selected_index - 1)
                status_message = "Da xoa lenh nhanh"
                if not save_settings(settings):
                    status_message = "Khong the luu cai dat"
            else:
                status_message = "Da huy xoa"


def settings_screen(stdscr, selected):
    settings = load_settings()
    selected_index = 0
    status_message = "Cai dat tu dong luu"
    setting_labels = (
        "Mau nhan",
        "Hoat anh khoi dong",
        "Ngay gio trong THONG TIN",
        "Lenh nhanh",
        "Code chay Desktop",
    )

    while True:
        if not draw_desktop(stdscr, selected, "SETTINGS"):
            if stdscr.getch() == 27:
                return
            continue

        layout = get_desktop_layout(stdscr)
        window_height = layout["main_height"] - 2
        window_width = layout["left_width"] - 2
        window = curses.newwin(
            window_height,
            window_width,
            layout["main_y"] + 1,
            layout["left_x"] + 1,
        )
        values = (
            settings["accent"],
            "BAT" if settings["boot_animation"] else "TAT",
            "BAT" if settings["show_datetime"] else "TAT",
            f"{len(settings['quick_commands'])} lenh",
            "BAT" if settings["desktop_code_animation"] else "TAT",
        )
        window.addnstr(0, 0, "CAI DAT PYOS", window_width)
        for index, (label, value) in enumerate(zip(setting_labels, values)):
            attributes = curses.A_REVERSE if index == selected_index else curses.A_NORMAL
            window.addnstr(2 + index, 0, f"{label}: {value}", window_width, attributes)
        window.addnstr(window_height - 3, 0, "ARROWS: Chon  ENTER: Mo/Doi", window_width)
        window.addnstr(window_height - 2, 0, "R: Khoi phuc mac dinh  ESC: Ve", window_width)
        window.addnstr(window_height - 1, 0, status_message, window_width)
        window.refresh()

        key = stdscr.getch()
        if key == 27:
            return
        if key == curses.KEY_UP:
            selected_index = max(0, selected_index - 1)
        elif key == curses.KEY_DOWN:
            selected_index = min(len(setting_labels) - 1, selected_index + 1)
        elif key in (ord("r"), ord("R")):
            settings = get_default_settings()
            status_message = (
                "Da khoi phuc mac dinh"
                if save_settings(settings)
                else "Khong the luu cai dat"
            )
        elif key in (curses.KEY_LEFT, curses.KEY_RIGHT, 10, 13, curses.KEY_ENTER):
            if selected_index == 3:
                if key in (10, 13, curses.KEY_ENTER):
                    status_message = quick_commands_screen(stdscr, selected, settings)
                    if not save_settings(settings):
                        status_message = "Khong the luu cai dat"
                continue
            if selected_index == 0:
                color_names = list(ACCENT_COLORS)
                color_index = color_names.index(settings["accent"])
                direction = -1 if key == curses.KEY_LEFT else 1
                settings["accent"] = color_names[(color_index + direction) % len(color_names)]
                status_message = f"Mau nhan: {settings['accent']}"
            else:
                setting_key = {
                    1: "boot_animation",
                    2: "show_datetime",
                    4: "desktop_code_animation",
                }[selected_index]
                settings[setting_key] = not settings[setting_key]
                status_message = f"{setting_labels[selected_index]}: {'BAT' if settings[setting_key] else 'TAT'}"

            if not save_settings(settings):
                status_message = "Khong the luu cai dat"
        elif key in (ord("s"), ord("S")):
            status_message = "Da luu" if save_settings(settings) else "Khong the luu cai dat"


def quick_launch(stdscr, selected):
    command = ""
    status_message = ""

    while True:
        prompt_lines = BOOT_LINES[:-1] + [f"[PYOS] Desktop ready_ {command}_"]
        if status_message:
            prompt_lines.append(status_message)
        if not draw_desktop(stdscr, selected, desktop_lines=prompt_lines, quick_mode=True):
            if stdscr.getch() == 27:
                return
            continue

        key = stdscr.get_wch()
        if key in (27, "\x1b"):
            return
        if key in (10, 13, curses.KEY_ENTER, "\n", "\r"):
            url = load_settings()["quick_commands"].get(command.strip().casefold())
            if url:
                opened, status_message = open_url(url)
                if opened:
                    return
                status_message = f"[ERROR] {status_message}"
            else:
                status_message = "[ERROR] Lenh chua co; them trong SETTINGS"
            command = ""
        elif key in (curses.KEY_BACKSPACE, 127, 8, "\x7f", "\b"):
            command = command[:-1]
        elif isinstance(key, str) and key.isprintable() and len(command) < 32:
            command += key


def open_url(url):
    chrome_paths = [
        shutil.which("google-chrome"),
        shutil.which("google-chrome-stable"),
        "/opt/google/chrome/google-chrome",
        "/opt/google/chrome/chrome",
    ]
    for chrome_path in dict.fromkeys(path for path in chrome_paths if path):
        if not os.path.isfile(chrome_path) or not os.access(chrome_path, os.X_OK):
            continue
        try:
            subprocess.Popen(
                [chrome_path, "--new-window", url],
                start_new_session=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return True, "Da mo dia chi trong Chrome"
        except OSError:
            continue

    try:
        if webbrowser.open_new(url):
            return True, "Da mo dia chi trong trinh duyet"
    except webbrowser.Error:
        pass
    return False, "Khong tim thay trinh duyet de mo dia chi"


def main(stdscr):
    curses.curs_set(0)
    stdscr.keypad(True)
    curses.mousemask(curses.ALL_MOUSE_EVENTS)

    selected = 0
    draw_boot_animation(stdscr, selected)
    desktop_lines = BOOT_LINES.copy()
    stream_index = 0

    while True:
        if not draw_desktop(stdscr, selected, desktop_lines=desktop_lines):
            if stdscr.getch() == 27:
                break
            continue

        if load_settings()["desktop_code_animation"]:
            stdscr.timeout(240)
            key = stdscr.getch()
            stdscr.timeout(-1)
            if key == -1:
                line_template = DESKTOP_STREAM_LINES[stream_index % len(DESKTOP_STREAM_LINES)]
                desktop_lines.append(line_template.format(tick=stream_index + 1))
                stream_index += 1
                del desktop_lines[:-80]
                continue
        else:
            key = stdscr.getch()

        if key in (24, "\x18"):
            quick_launch(stdscr, selected)

        elif key in (curses.KEY_RIGHT, curses.KEY_DOWN):
            selected = min(len(APPS) - 1, selected + 1)

        elif key in (curses.KEY_LEFT, curses.KEY_UP):
            selected = max(0, selected - 1)

        elif key in (10, 13, curses.KEY_ENTER):
            app = APPS[selected]

            if app == "FILES":
                files_screen(stdscr, selected)
            elif app == "PYTHON":
                python_run_screen(stdscr, selected)
            elif app == "STORE":
                store_screen(stdscr, selected)
            elif app == "GAMES":
                games_screen(stdscr, selected)
            elif app == "GALLERY":
                gallery_screen(stdscr, selected)
            elif app == "ACCOUNT":
                account_screen(stdscr, selected)
            elif app == "SETTINGS":
                settings_screen(stdscr, selected)
            else:
                placeholder_screen(stdscr, selected, app)

        elif key == 27:
            break


if __name__ == "__main__":
    curses.wrapper(main)

