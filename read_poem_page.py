import flet as ft
import random
from image_data import IMAGE_DATA


# Begin Read Poem View Class____________________________________________________________________________________________
class ReadPoemView(ft.UserControl):
    def __init__(self, poem_data: dict, image_data: dict = None) -> None:
        super().__init__()
        self.poem_title = poem_data["title"]
        self.poem_body = poem_data["body"]
        self.poem_tags = poem_data["tags"].split(", ")
        self.poem_alignment = poem_data["alignment"]
        self.poem_datetime = poem_data["datetime"]

        # Capitalize poem tags
        for i in range(len(self.poem_tags)):
            self.poem_tags[i] = self.poem_tags[i].capitalize()

        # Get image
        if image_data:
            self.image_data = image_data
        else:
            if "Love" in self.poem_tags:
                if random.randint(0, 1):
                    self.image_data = IMAGE_DATA[2]
                else:
                    self.image_data = IMAGE_DATA[3]
            elif "Heartbreak" in self.poem_tags:
                if random.randint(0, 1):
                    self.image_data = IMAGE_DATA[0]
                else:
                    self.image_data = IMAGE_DATA[1]
            elif "Sad" in self.poem_tags:
                self.image_data = IMAGE_DATA[4]
            elif "Sorrow" in self.poem_tags:
                self.image_data = IMAGE_DATA[4]
            else:
                self.image_data = IMAGE_DATA[random.randint(5, 9)]

        # Create poem tag containers
        self.tag_list = ft.Row(
            spacing=10,
            alignment=ft.MainAxisAlignment.CENTER,
            scroll=ft.ScrollMode.ADAPTIVE
        )
        for tag in self.poem_tags:
            tag_button = ft.Container(
                bgcolor=ft.colors.BLUE_GREY_900,  # 7A0000,
                border_radius=ft.BorderRadius(10, 10, 10, 10),
                height=40,
                padding=10,
                content=ft.Text(
                    value=tag,
                    color="white",
                    text_align=ft.TextAlign.CENTER
                )
            )
            self.tag_list.controls.append(tag_button)

    def build(self) -> ft.Container:
        ret_container = ft.Container(
            alignment=ft.alignment.center,
            image_src=self.image_data["url"],
            image_opacity=self.image_data["opacity"],
            bgcolor="white",  # ft.colors.GREY_200,
            border_radius=ft.border_radius.all(5),
            shadow=ft.BoxShadow(1.2, 5, ft.colors.GREY_500),
            margin=ft.Margin(5, 5, 5, 5),
            padding=ft.Padding(15, 10, 15, 10),
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Text(
                        value=self.poem_title,
                        text_align=ft.TextAlign.CENTER,
                        italic=True,
                        theme_style=ft.TextThemeStyle.DISPLAY_SMALL,
                        weight=ft.FontWeight.BOLD,
                        color="#925A15",  # 7A0000
                    ),
                    ft.Text(
                        value=self.poem_datetime,
                        text_align=ft.TextAlign.CENTER,
                        italic=True,
                        theme_style=ft.TextThemeStyle.LABEL_LARGE,
                        color=ft.colors.GREY_500,
                    ),
                    ft.Divider(thickness=0.2, color=ft.colors.GREY_400),
                    ft.Text(
                        self.poem_body,
                        # text_align=ft.TextAlign.START,
                        color=ft.colors.GREY_900,
                        weight=ft.FontWeight.W_400
                    ),
                    ft.Divider(thickness=0.2, color=ft.colors.GREY_400),
                    ft.Text(
                        value="Tags:",
                        text_align=ft.TextAlign.CENTER,
                        color=ft.colors.BLUE_GREY_900,  # 7A0000,
                        italic=True,
                        weight=ft.FontWeight.BOLD
                    ),
                    self.tag_list
                ]
            )
        )
        if self.poem_alignment.lower() == "left":
            ret_container.content.controls[3].text_align=ft.TextAlign.START
        elif self.poem_alignment.lower() == "center":
            ret_container.content.controls[3].text_align = ft.TextAlign.CENTER
        elif self.poem_alignment.lower() == "right":
            ret_container.content.controls[3].text_align = ft.TextAlign.END
        return ret_container

# End Read Poem View Class______________________________________________________________________________________________
