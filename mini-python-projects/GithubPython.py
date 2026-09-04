import tkinter as tk
import webbrowser
import os

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False



WINDOW_TITLE = "Github python"
GITHUB_LINK = "https://github.com/k2782-suka"
LOGO_FILE = "lucky_patcher.png"

BACKGROUND_COLOR = "#020b05"
GREEN_COLOR = "#00ff55"
DARK_GREEN_COLOR = "#063d1b"
BRIGHT_GREEN_COLOR = "#39ff75"
WHITE_COLOR = "#ffffff"

FONT_NAME = "Courier New"



def open_github(event=None):
    webbrowser.open(GITHUB_LINK)



root = tk.Tk()

root.title(WINDOW_TITLE)
root.geometry("850x600")
root.minsize(650, 450)
root.configure(bg=BACKGROUND_COLOR)



top_frame = tk.Frame(
    root,
    bg=DARK_GREEN_COLOR,
    highlightbackground=GREEN_COLOR,
    highlightcolor=GREEN_COLOR,
    highlightthickness=2
)

top_frame.pack(
    side="top",
    fill="x",
    padx=25,
    pady=(20, 10)
)


welcome_text = (
    "Привет!\n"
    "Спасибо за то, что используешь\n"
    "мои Python-проекты!"
)


welcome_label = tk.Label(
    top_frame,
    text=welcome_text,
    bg=DARK_GREEN_COLOR,
    fg=BRIGHT_GREEN_COLOR,
    font=(FONT_NAME, 18, "bold"),
    justify="center",
    pady=18
)

welcome_label.pack(
    fill="both",
    expand=True
)


content_frame = tk.Frame(
    root,
    bg=BACKGROUND_COLOR
)

content_frame.pack(
    fill="both",
    expand=True,
    padx=25,
    pady=10
)



info_label = tk.Label(
    content_frame,
    text=(
        ">>> КСТАТИ\n"
        ">>> ЕЩЕ\n"
        ">>> МОИ GITHUB ПРОЕКТЫ\n"
        ">>> СЛЕВА СНИЗУ"
    ),
    bg=BACKGROUND_COLOR,
    fg=GREEN_COLOR,
    font=(FONT_NAME, 13),
    justify="left"
)

info_label.pack(
    pady=(15, 10)
)


logo_label = None
logo_image = None


if PIL_AVAILABLE and os.path.exists(LOGO_FILE):

    try:
        image = Image.open(LOGO_FILE)

        image.thumbnail((230, 230))

        logo_image = ImageTk.PhotoImage(image)

        logo_label = tk.Label(
            content_frame,
            image=logo_image,
            bg=BACKGROUND_COLOR
        )

        logo_label.image = logo_image
        logo_label.pack(pady=10)

    except Exception:
        logo_label = tk.Label(
            content_frame,
            text="[ Ошибка загрузки логотипа ]",
            bg=BACKGROUND_COLOR,
            fg=GREEN_COLOR,
            font=(FONT_NAME, 12)
        )

        logo_label.pack(pady=30)

elif not PIL_AVAILABLE:

    logo_label = tk.Label(
        content_frame,
        text=(
            "[ Для отображения картинки установи Pillow ]\n"
            "Команда: pip install pillow"
        ),
        bg=BACKGROUND_COLOR,
        fg=GREEN_COLOR,
        font=(FONT_NAME, 12),
        justify="center"
    )

    logo_label.pack(pady=30)

else:

    logo_label = tk.Label(
        content_frame,
        text=(
            "[ Файл lucky_patcher.png не найден ]\n"
            "Положи картинку рядом с программой"
        ),
        bg=BACKGROUND_COLOR,
        fg=GREEN_COLOR,
        font=(FONT_NAME, 12),
        justify="center"
    )

    logo_label.pack(pady=30)



bottom_frame = tk.Frame(
    root,
    bg=BACKGROUND_COLOR
)

bottom_frame.pack(
    side="bottom",
    fill="x",
    padx=25,
    pady=20
)


github_label = tk.Label(
    bottom_frame,
    text=GITHUB_LINK,
    bg=DARK_GREEN_COLOR,
    fg=BRIGHT_GREEN_COLOR,
    font=(FONT_NAME, 12, "underline"),
    cursor="hand2",
    padx=10,
    pady=8
)

github_label.pack(
    side="left"
)


# Нажатие на ссылку
github_label.bind(
    "<Button-1>",
    open_github
)


def link_enter(event):
    github_label.config(
        fg=WHITE_COLOR
    )


def link_leave(event):
    github_label.config(
        fg=BRIGHT_GREEN_COLOR
    )


github_label.bind(
    "<Enter>",
    link_enter
)

github_label.bind(
    "<Leave>",
    link_leave
)


version_label = tk.Label(
    bottom_frame,
    text="Python Project",
    bg=BACKGROUND_COLOR,
    fg=DARK_GREEN_COLOR,
    font=(FONT_NAME, 10)
)

version_label.pack(
    side="right"
)


root.mainloop()
