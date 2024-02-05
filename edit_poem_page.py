import flet as ft
from datetime import datetime
from collections import defaultdict


# Default dictionary function
def default():
    return ""


# Begin Edit Poem View Class____________________________________________________________________________________________
class EditPoemView(ft.UserControl):
    def __init__(self, poem_data: dict = None) -> None:
        super().__init__()
        self.poem_data = defaultdict(default)
        self.poem_data["datetime"] = f'{datetime.utcnow().strftime("%A %d %b %Y")} - {datetime.now().strftime("%H:%M")}'
        if poem_data:
            self.poem_data = poem_data

        self.alignment = "left"

        # Declaration of poem body text field for easy access later
        self.poem_field = ft.TextField(value=self.poem_data['body'], multiline=True, label="Poem",
                                       focused_border_color="#BF9A40", border_width=0.9, focused_border_width=1.5,
                                       border_color=ft.colors.GREY_400, color=ft.colors.GREY_800,
                                       label_style=ft.TextStyle(color="#7A0000", weight=ft.FontWeight.BOLD),
                                       width=1000, autocorrect=True, capitalization=ft.TextCapitalization.SENTENCES,
                                       text_style=ft.TextStyle(16, weight=ft.FontWeight.W_500),
                                       selection_color="#BF9A40", on_change=self.changed)
        if self.poem_data["alignment"].lower() == "left":
            self.poem_field.text_align = ft.TextAlign.START
        elif self.poem_data["alignment"].lower() == "center":
            self.poem_field.text_align = ft.TextAlign.CENTER
        elif self.poem_data["alignment"].lower() == "right":
            self.poem_field.text_align = ft.TextAlign.END

        self.poem_title_field = ft.TextField(value=self.poem_data['title'], multiline=False, label="Title",
                                             focused_border_color="#BF9A40", border_width=0.9, focused_border_width=1.5,
                                             border_color=ft.colors.GREY_400, color=ft.colors.GREY_800,
                                             label_style=ft.TextStyle(color="#7A0000", weight=ft.FontWeight.BOLD),
                                             width=1000, text_style=ft.TextStyle(16, weight=ft.FontWeight.W_500),
                                             on_change=self.changed)
        self.poem_datetime_field = ft.TextField(value=self.poem_data['datetime'], read_only=True,
                                                color=ft.colors.GREY_600,
                                                label_style=ft.TextStyle(color="#7A0000", weight=ft.FontWeight.BOLD),
                                                border_width=1, border_color=ft.colors.GREY_400, label="Date and Time",
                                                width=1000,
                                                text_style=ft.TextStyle(16, weight=ft.FontWeight.W_500))
        self.poem_tags_field = ft.TextField(value=self.poem_data['tags'], multiline=False, border_width=0.9,
                                            label="Tags", focused_border_color="#BF9A40",
                                            helper_text="Separate tags with commas",
                                            border_color=ft.colors.GREY_400, focused_border_width=1.5,
                                            color=ft.colors.GREY_800,
                                            helper_style=ft.TextStyle(color=ft.colors.GREY_500),
                                            label_style=ft.TextStyle(color="#7A0000", weight=ft.FontWeight.BOLD),
                                            width=1000, text_style=ft.TextStyle(16, weight=ft.FontWeight.W_500),
                                            on_change=self.changed)

        # Keep track of changes
        self.modified = False

    # Event handlers
    def change_alignment(self, alignment: str):
        if alignment.lower() == 'left':
            self.poem_field.text_align = ft.TextAlign.LEFT
            self.alignment = "left"
            self.modified = True
        elif alignment.lower() == 'center':
            self.poem_field.text_align = ft.TextAlign.CENTER
            self.alignment = "center"
            self.modified = True
        elif alignment.lower() == 'right':
            self.poem_field.text_align = ft.TextAlign.RIGHT
            self.alignment = "right"
            self.modified = True
        self.update()

    def changed(self, e) -> None:
        self.modified = True

    def is_modified(self) -> bool:
        return self.modified

    def saved(self):
        self.modified = False

    def build(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                spacing=30,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Divider(color="transparent"),
                    self.poem_title_field,
                    self.poem_datetime_field,
                    self.poem_field,
                    self.poem_tags_field,
                    ft.Divider(color="transparent")
                ]
            )
        )

# End Edit Poem View Class______________________________________________________________________________________________
