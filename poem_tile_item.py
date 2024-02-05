import flet as ft
import random
from collections import defaultdict
from image_data import IMAGE_DATA


# Default dictionary function
def default():
    return ""


# Begin Poem Item Class_________________________________________________________________________________________________
class PoemTileItem(ft.UserControl):
    def __init__(self, poem_data: dict, open_read_func, open_edit_func, delete_poem_func) -> None:
        super().__init__()
        self.poem_title = defaultdict(default)
        self.poem_title = poem_data["title"]
        self.poem_body = poem_data["body"]
        self.poem_tags = poem_data["tags"].split(", ")
        self.date_time = poem_data["datetime"]
        self.open_read_func = open_read_func
        self.open_edit_func = open_edit_func
        self.delete_poem_func = delete_poem_func

        # Capitalize all tags:
        for i in range(len(self.poem_tags)):
            self.poem_tags[i] = self.poem_tags[i].capitalize()

    def build(self) -> ft.Container:
        # Picking an image
        if "Love" in self.poem_tags:
            if random.randint(0, 1):
                image = IMAGE_DATA[2]
            else:
                image = IMAGE_DATA[3]
        elif "Heartbreak" in self.poem_tags:
            if random.randint(0, 1):
                image = IMAGE_DATA[0]
            else:
                image = IMAGE_DATA[1]
        elif "Sad" in self.poem_tags:
            image = IMAGE_DATA[4]
        else:
            image = IMAGE_DATA[random.randint(5, 9)]

        return ft.Container(
            data={"title": self.poem_title, "image": image},
            image_src=image['url'],
            image_fit=ft.ImageFit.SCALE_DOWN,
            image_opacity=image['opacity'],
            padding=15,
            bgcolor="White",
            gradient=ft.LinearGradient(["#FFFFFF", "#FDFFF9"]),
            ink=True,
            blur=ft.Blur(0.5, 0.5),
            border_radius=ft.border_radius.all(5),
            shadow=ft.BoxShadow(1.2, 5, ft.colors.GREY_500),
            # height=300,
            # width=300,
            on_click=self.open_read_func,
            content=ft.Column(
                scroll=ft.ScrollMode.ADAPTIVE,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(self.poem_title, theme_style=ft.TextThemeStyle.TITLE_LARGE,
                                    color=ft.colors.GREY_900, weight=ft.FontWeight.W_500)
                        ]
                    ),
                    ft.Text(self.date_time, color="#00000F"),
                    ft.Divider(thickness=0.3, color="#00000F"),
                    ft.Text(self.poem_body[:50].replace('\n', ' ') + "...", color=ft.colors.GREY_800),
                    ft.Divider(color="transparent", height=35),
                    ft.Text(f'Tags: {" ,".join(self.poem_tags)}', color="#BF9A40",  # ft.colors.GREY_700,
                            theme_style=ft.TextThemeStyle.LABEL_SMALL),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.IconButton(icon=ft.icons.DELETE,
                                          data=self.poem_title,
                                          icon_color=ft.colors.GREY_600,
                                          tooltip="Delete Poem",
                                          scale=1.3,
                                          on_click=self.delete_poem_func),
                            ft.IconButton(icon=ft.icons.EDIT_DOCUMENT,
                                          scale=1.3,
                                          data=self.poem_title,
                                          icon_color=ft.colors.GREY_600,
                                          tooltip="Edit Poem",
                                          on_click=self.open_edit_func)
                        ]
                    )
                ]
            )
        )
# End Poem View Class___________________________________________________________________________________________________
