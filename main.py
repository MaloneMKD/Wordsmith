import flet as ft
from poem_tile_item import PoemTileItem
from read_poem_page import ReadPoemView
from edit_poem_page import EditPoemView
from rhyme_finder import get_rhymes_rhymebrain
from db_operations import Database

database = Database()


# Begin Main Function___________________________________________________________________________________________________
def main(page: ft.Page) -> None:
    global current_view_type
    current_view_type = "Grid"

    global current_page
    current_page = "Home"

    global list_state
    list_state = "Collapsed"

    # Functions
    def show_rhyme_results(word, results) -> None:
        if word:
            text_items = [ft.Text(value=r) for r in results]
            text_items.insert(0, ft.Text(
                value=f"Words that rhyme with {word}:",
                text_align=ft.TextAlign.CENTER,
                theme_style=ft.TextThemeStyle.TITLE_SMALL,
                color="#BF9A40"
            ))

            dlg = ft.AlertDialog(
                title=ft.Text("Rhyme Utility", text_align=ft.TextAlign.CENTER),
                actions_alignment=ft.MainAxisAlignment.CENTER,
                content=ft.Container(
                    padding=ft.Padding(5, 0, 0, 0),
                    content=ft.ListView(
                        controls=text_items
                    )
                ),
                actions=[
                    ft.Text("Click outside the box to close", text_align=ft.TextAlign.CENTER, color="#BF9A40")
                ]
            )
            page.dialog = dlg
            dlg.open = True
            page.update()

    def align_text_left(e):
        epv = page.controls[1].content
        epv.change_alignment("left")
        e.control.icon_color = "#BF9A40"
        alignment_bar = page.controls[0].controls[1].controls[0].content
        alignment_bar.controls[1].icon_color = ft.colors.BLUE_GREY_900
        alignment_bar.controls[2].icon_color = ft.colors.BLUE_GREY_900
        page.update()

    def align_text_center(e):
        epv = page.controls[1].content
        epv.change_alignment("center")
        e.control.icon_color = "#BF9A40"
        alignment_bar = page.controls[0].controls[1].controls[0].content
        alignment_bar.controls[0].icon_color = ft.colors.BLUE_GREY_900
        alignment_bar.controls[2].icon_color = ft.colors.BLUE_GREY_900
        page.update()

    def align_text_right(e):
        epv = page.controls[1].content
        epv.change_alignment("right")
        e.control.icon_color = "#BF9A40"
        alignment_bar = page.controls[0].controls[1].controls[0].content
        alignment_bar.controls[0].icon_color = ft.colors.BLUE_GREY_900
        alignment_bar.controls[1].icon_color = ft.colors.BLUE_GREY_900
        page.update()

    def get_poem_list_view(filter_tags: list = None):
        panel = ft.ExpansionPanelList(
            elevation=8, divider_color="#FFFFFF", spacing=10, expand_icon_color=ft.colors.WHITE,
            expanded_header_padding=0)

        if filter_tags:
            # Get filtered data from database
            poem_data = database.get_filtered_data(filter_tags) or []
            for poem in poem_data:
                poem["image"] = None
                panel.controls.append(ft.ExpansionPanel(
                    bgcolor=ft.colors.BLUE_GREY_800,
                    can_tap_header=True,
                    header=ft.ListTile(
                        title=ft.Text(poem["title"], color=ft.colors.WHITE, weight=ft.FontWeight.BOLD,
                                      theme_style=ft.TextThemeStyle.TITLE_MEDIUM), data="Poem ID"),
                    content=ft.ListTile(
                        title=ft.Text(poem['tags'], color="#BF9A40",
                                      theme_style=ft.TextThemeStyle.TITLE_SMALL),
                        subtitle=ft.Text(poem["datetime"], color=ft.colors.WHITE,
                                         theme_style=ft.TextThemeStyle.BODY_SMALL),
                        trailing=ft.Row(
                            width=150,
                            controls=[
                                ft.IconButton(icon=ft.icons.READ_MORE, data=poem, on_click=open_read_poem_view,
                                              tooltip="Read Poem", icon_color="#BF9A40"),
                                ft.IconButton(icon=ft.icons.EDIT_DOCUMENT, data=poem["title"],
                                              on_click=open_edit_poem_view,
                                              tooltip="Edit Poem", icon_color="#BF9A40"),
                                ft.IconButton(icon=ft.icons.DELETE, data=poem["title"], on_click=delete_poem,
                                              tooltip="Delete Poem", icon_color="#BF9A40")
                            ]
                        )
                    )
                ))
        else:
            # Get data from database
            poem_data = database.get_all_data() or []
            for poem in poem_data:
                poem["image"] = None
                panel.controls.append(ft.ExpansionPanel(
                    bgcolor=ft.colors.BLUE_GREY_800,
                    header=ft.ListTile(title=ft.Text(poem["title"], color=ft.colors.WHITE, weight=ft.FontWeight.BOLD,
                                                     theme_style=ft.TextThemeStyle.TITLE_MEDIUM)),
                    content=ft.ListTile(
                        title=ft.Text(poem['tags'], color="#BF9A40",
                                      theme_style=ft.TextThemeStyle.TITLE_SMALL),
                        subtitle=ft.Text(poem["datetime"], color=ft.colors.WHITE,
                                         theme_style=ft.TextThemeStyle.BODY_SMALL),
                        trailing=ft.Row(
                            width=150,
                            controls=[
                                ft.IconButton(icon=ft.icons.READ_MORE, data=poem, on_click=open_read_poem_view,
                                              tooltip="Read Poem", icon_color="#BF9A40"),
                                ft.IconButton(icon=ft.icons.EDIT_DOCUMENT, data=poem["title"],
                                              on_click=open_edit_poem_view,
                                              tooltip="Edit Poem", icon_color="#BF9A40"),
                                ft.IconButton(icon=ft.icons.DELETE, data=poem["title"], on_click=delete_poem,
                                              tooltip="Delete Poem", icon_color="#BF9A40")
                            ]
                        )
                    )
                ))
        return panel

    def get_poem_grid_view(filter_tags: list = None) -> ft.Container:
        if filter_tags:
            # Get filtered data from database
            poem_data = database.get_filtered_data(filter_tags) or []
            poem_controls = []
            for poem in poem_data:
                poem_controls.append(PoemTileItem(poem,
                                                  open_read_func=open_read_poem_view,
                                                  open_edit_func=open_edit_poem_view,
                                                  delete_poem_func=delete_poem))
        else:
            # Get data from database
            poem_data = database.get_all_data() or []
            poem_controls = [PoemTileItem(poem,
                                          open_read_func=open_read_poem_view,
                                          open_edit_func=open_edit_poem_view,
                                          delete_poem_func=delete_poem) for poem in poem_data]

        main_grid = ft.ResponsiveRow(alignment=ft.MainAxisAlignment.START,
                                     vertical_alignment=ft.CrossAxisAlignment.CENTER)
        for poem in poem_controls:
            main_grid.controls.append(ft.Column(col={"xs": 12, "sm": 6, "md": 4, "lg": 3}, controls=[poem]))

        return ft.Container(alignment=ft.alignment.center_right, content=main_grid)

    def display_filtered(tag_list):
        global current_page
        current_page = "Home"

        global current_view_type

        # Capitalize all tags
        for i in range(len(tag_list)):
            tag_list[i] = tag_list[i].title()

        page.controls.clear()
        bar = ft.Container(
            bgcolor="#C2B19C",
            width=1900,
            height=60,
            padding=ft.Padding(25, 0, 25, 0),
            border_radius=10,
            alignment=ft.alignment.center,
            content=ft.Text(f"Poems that contain the tag(s): {' ,'.join(tag_list)}", color="#FFFFFF",
                            weight=ft.FontWeight.W_500, theme_style=ft.TextThemeStyle.BODY_LARGE)
        )
        if current_view_type == "Grid":
            page.controls.append(bar)
            page.controls.append(get_poem_grid_view(tag_list))
        elif current_view_type == "List":
            global list_state
            list_state = "Collapsed"
            page.appbar.actions[0].icon = ft.icons.EXPAND_MORE
            page.appbar.actions[0].text = "Expand all"

            page.controls.append(bar)
            page.controls.append(get_poem_list_view(tag_list))
        reveal_back_button()
        if page.dialog:  # If there is a dialog open close it
            close_page_dialog(None)
        page.update()

    def get_home_page_menu(view_type: str = "Grid") -> ft.ResponsiveRow:
        search_bar = ft.Row(
            controls=[
                ft.TextField(hint_text="Search tags", expand=True, bgcolor=ft.colors.BLUE_GREY_900, border_radius=5,
                             helper_text="Separate tags with a comma and space"),
                ft.IconButton(icon=ft.icons.SEARCH, scale=1.2, icon_color=ft.colors.BLUE_GREY_900,
                              on_click=lambda _: display_filtered(search_bar.controls[0].value.split(", ")))
            ]
        )

        return ft.ResponsiveRow(
            controls=[
                ft.Column(
                    col={"xs": 11, "sm": 4, "md": 2},
                    controls=[ft.ElevatedButton(
                        text="New Poem", icon=ft.icons.NOTE_ADD, bgcolor=ft.colors.BLUE_GREY_900, color="white",
                        height=50, width=1200, on_click=open_new_poem_view, style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=5)
                        )
                    )]),
                ft.Column(
                    col={"xs": 11, "sm": 6, "md": 2},
                    controls=[ft.Dropdown(
                        value=view_type, filled=True, bgcolor=ft.colors.BLUE_GREY_900, color=ft.colors.WHITE,
                        height=65, width=800,
                        border_radius=5, prefix_icon=ft.icons.VIEW_LIST, border_color="transparent",
                        content_padding=5,
                        on_change=change_view_type,
                        options=[
                            ft.dropdown.Option("Grid"),
                            ft.dropdown.Option("List")]
                    )]),
                ft.Column(
                    col={"sm": 0, "md": 3},
                    controls=[ft.VerticalDivider()]
                ),
                ft.Column(
                    col={"sm": 11, "md": 4},
                    controls=[search_bar]
                ),
            ]
        )

    def get_read_page_menu() -> ft.Container:
        return ft.Container(
            bgcolor="#C2B19C",
            width=1900,
            height=60,
            padding=ft.Padding(25, 0, 25, 0),
            border_radius=10,
        )

    def back_button_clicked(e):
        global current_view_type
        global list_state

        if current_view_type == "List" and len(page.appbar.actions) == 1:
            page.appbar.actions.insert(0,
                                       ft.ElevatedButton(icon=ft.icons.EXPAND_MORE, text="Expand All",
                                                         on_click=expand_or_collapse_all, color="white",
                                                         bgcolor=ft.colors.BLUE_GREY_900,
                                                         style=ft.ButtonStyle(
                                                             shape=ft.RoundedRectangleBorder(radius=5))))
        elif current_view_type == "List" and len(page.appbar.actions) == 2:
            global list_state
            list_state = "Collapsed"
            page.appbar.actions[0].icon = ft.icons.EXPAND_MORE
            page.appbar.actions[0].text = "Expand all"

        if current_page == "Edit":
            epv = page.controls[1].content
            if epv.is_modified():
                dialog = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Confirm", color="#BF9A40"),
                    content=ft.Text(f"You have not saved your modifications, are you sure you want to leave?"),
                    actions=[
                        ft.TextButton("Yes", on_click=open_home_page, style=ft.ButtonStyle(color="#BF9A40")),
                        ft.TextButton("Cancel", on_click=close_page_dialog, style=ft.ButtonStyle(color="#BF9A40"))
                    ],
                    actions_alignment=ft.MainAxisAlignment.END
                )
                page.dialog = dialog
                dialog.open = True
                page.update()
            else:
                open_home_page(None)
        else:
            open_home_page(None)

    def open_home_page(e):
        global current_page
        current_page = "Home"

        global current_view_type

        page.controls.clear()
        page.controls.append(get_home_page_menu(current_view_type))
        if current_view_type == "Grid":
            page.controls.append(get_poem_grid_view())
        elif current_view_type == "List":
            page.controls.append(get_poem_list_view())

        if page.appbar.leading:
            page.appbar.leading.visible = False
        # page.floating_action_button.visible = False
        if page.dialog:  # If there is a dialog open close it
            close_page_dialog(None)
        page.update()

    def change_view_type(e):
        global list_state
        global current_view_type
        if e.control.value == "List" and e.control.value != current_view_type:
            page.controls.remove(page.controls[1])
            page.add(get_poem_list_view())
            page.appbar.actions.insert(0,
                                       ft.ElevatedButton(icon=ft.icons.EXPAND_MORE, text="Expand All", scale=0.95,
                                                         on_click=expand_or_collapse_all, color="white",
                                                         bgcolor=ft.colors.BLUE_GREY_900,
                                                         style=ft.ButtonStyle(
                                                             shape=ft.RoundedRectangleBorder(radius=5))))
            list_state = "Collapsed"
            page.appbar.actions[0].icon = ft.icons.EXPAND_MORE
            page.appbar.actions[0].text = "Expand all"
            page.appbar.title = ft.Text("(´•  •`)", no_wrap=True, color=ft.colors.WHITE,
                                        theme_style=ft.TextThemeStyle.TITLE_LARGE, weight=ft.FontWeight.W_500)
            current_view_type = "List"
        elif e.control.value == "Grid" and e.control.value != current_view_type:
            page.appbar.actions.remove(page.appbar.actions[0])
            page.appbar.title = ft.Text("(´•  •`) Wordsmith", no_wrap=True, color=ft.colors.WHITE,
                      theme_style=ft.TextThemeStyle.TITLE_LARGE, weight=ft.FontWeight.W_500)
            page.controls.remove(page.controls[1])
            page.add(get_poem_grid_view())
            current_view_type = "Grid"

        page.update()

    def expand_or_collapse_all(e):
        global list_state
        list_items = page.controls[1].controls

        if list_state == "Collapsed":
            for item in list_items:
                item.expanded = True
            list_state = "Expanded"
            page.appbar.actions[0].icon = ft.icons.LIST_SHARP
            page.appbar.actions[0].text = "Collapse all"
            page.update()
        elif list_state == "Expanded":
            for item in list_items:
                item.expanded = False
            list_state = "Collapsed"
            page.appbar.actions[0].icon = ft.icons.EXPAND_MORE
            page.appbar.actions[0].text = "Expand all"
            page.update()

    def get_edit_page_menu():
        search_bar = ft.Row(
            controls=[
                ft.TextField(
                    multiline=False, bgcolor=ft.colors.BLUE_GREY_900,
                    border_color=ft.colors.BLUE_GREY_900, hint_text="Words that rhyme with...", expand=True,
                    helper_text="Press enter or click search",
                    on_submit=lambda _: show_rhyme_results(search_bar.controls[0].value,
                                                           get_rhymes_rhymebrain(
                                                               search_bar.controls[0].value))
                ),
                ft.IconButton(icon=ft.icons.SEARCH, scale=1.2, icon_color=ft.colors.BLUE_GREY_900,
                              on_click=lambda _: show_rhyme_results(search_bar.controls[0].value,
                                                                    get_rhymes_rhymebrain(
                                                                        search_bar.controls[0].value)))
            ]
        )

        alignment_bar = ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.alignment.center,
            controls=[
                ft.IconButton(icon=ft.icons.ALIGN_HORIZONTAL_LEFT, icon_color="#BF9A40", on_click=align_text_left,
                              scale=0.9),
                ft.IconButton(icon=ft.icons.ALIGN_HORIZONTAL_CENTER, icon_color=ft.colors.BLUE_GREY_900,
                              on_click=align_text_center, scale=0.9),
                ft.IconButton(icon=ft.icons.ALIGN_HORIZONTAL_RIGHT, icon_color=ft.colors.BLUE_GREY_900,
                              on_click=align_text_right, scale=0.9),
            ]
        )

        save_button = ft.ElevatedButton(icon=ft.icons.SAVE, icon_color="#BF9A40", scale=1.2,
                                        on_click=save_poem, text="Save", color=ft.colors.WHITE)
        return ft.ResponsiveRow(
            # spacing=20,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Column(col={"xs": 12, "sm": 12, "md": 6}, controls=[
                    ft.Container(bgcolor="#FFFFFF", padding=ft.Padding(10, 0, 0, 0), content=search_bar)
                ]),
                ft.Column(col={"xs": 12, "sm": 6, "md": 3}, alignment=ft.alignment.center, controls=[
                    ft.Container(bgcolor="#FFFFFF", padding=ft.Padding(10, 0, 0, 0), content=alignment_bar)
                ]),
                ft.Column(col={"xs": 12, "sm": 6, "md": 3}, controls=[
                    ft.Container(bgcolor="#FFFFFF", padding=ft.Padding(20, 0, 0, 0), content=save_button)
                ]),
            ]
        )

    def save_poem(e):
        # Get the edit page view
        epv = page.controls[1].content

        # Gather poem data
        poem_data = {
            "title": epv.poem_title_field.value,
            "body": epv.poem_field.value,
            "tags": reformat_tags(epv.poem_tags_field.value),
            "alignment": epv.alignment,
            "datetime": epv.poem_datetime_field.value
        }

        # Check if poem exists:
        if database.get_poem(poem_data["title"]):
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirm", color="#BF9A40"),
                content=ft.Text(f"A poem with this name already exists. Would you like to overwrite it?"),
                actions=[
                    ft.TextButton("Yes", on_click=lambda _: update_poem(poem_data, epv),
                                  style=ft.ButtonStyle(color="#BF9A40")),
                    ft.TextButton("Cancel", on_click=close_page_dialog, style=ft.ButtonStyle(color="#BF9A40"))
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            page.dialog = dialog
            dialog.open = True
            page.update()
        else:
            # Tell the read poem view to prepare data for save
            epv.saved()
            database.save_poem_to_database(poem_data)
            dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Success", color="#BF9A40"),
                content=ft.Text("Poem saved successfully."),
                actions=[
                    ft.TextButton("Close", on_click=close_page_dialog, style=ft.ButtonStyle(color="#BF9A40"))
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            page.dialog = dialog
            dialog.open = True
            page.update()

    def update_poem(poem_data, epv):
        database.update_poem(poem_data)
        epv.saved()

        close_page_dialog(None)
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Success", color="#BF9A40"),
            content=ft.Text("Poem updated successfully."),
            actions=[
                ft.TextButton("Close", on_click=close_page_dialog, style=ft.ButtonStyle(color="#BF9A40"))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def reformat_tags(tags: str):
        tags = tags.title().strip().replace(' ', "")
        split_strings = tags.split(',')
        if len(split_strings) == 1:
            return tags
        full_string = ""
        for i in range(len(split_strings)):
            if i != len(split_strings) - 1:
                full_string += f"{split_strings[i]}, "
            else:
                full_string += split_strings[i]
        return full_string

    def open_read_poem_view(e) -> None:
        # Read poem view
        global current_page
        current_page = "Read"

        global current_view_type
        if current_view_type == "List":
            global list_state
            list_state = "Collapsed"
            page.appbar.actions[0].icon = ft.icons.EXPAND_MORE
            page.appbar.actions[0].text = "Expand all"
            page.appbar.actions.remove(page.appbar.actions[0])

        read_poem_view = ReadPoemView(database.get_poem(e.control.data["title"]), e.control.data["image"])
        page.controls.clear()
        # page.controls.append(get_read_page_menu())
        page.controls.append(ft.Container(image_repeat=ft.ImageRepeat.REPEAT, content=read_poem_view,
                                          image_src="assets/images/img-1.png", image_fit=ft.ImageFit.SCALE_DOWN,
                                          image_opacity=0.4))
        reveal_back_button()
        page.update()

    def open_edit_poem_view(e) -> None:
        # Edit poem view  read_test_poem
        global current_page
        current_page = "Edit"

        global current_view_type
        if current_view_type == "List":
            global list_state
            list_state = "Collapsed"
            page.appbar.actions[0].icon = ft.icons.EXPAND_MORE
            page.appbar.actions[0].text = "Expand all"
            page.appbar.actions.remove(page.appbar.actions[0])

        poem = database.get_poem(e.control.data)
        edit_poem_view = EditPoemView(poem)
        page.controls.clear()
        menu = get_edit_page_menu()
        if poem["alignment"].lower() == "center":
            menu.controls[1].controls[0].content.controls[0].icon_color = ft.colors.BLUE_GREY_900
            menu.controls[1].controls[0].content.controls[1].icon_color = "#BF9A40"
            menu.controls[1].controls[0].content.controls[2].icon_color = ft.colors.BLUE_GREY_900
        elif poem["alignment"].lower() == "right":
            menu.controls[1].controls[0].content.controls[0].icon_color = ft.colors.BLUE_GREY_900
            menu.controls[1].controls[0].content.controls[1].icon_color = ft.colors.BLUE_GREY_900
            menu.controls[1].controls[0].content.controls[2].icon_color = "#BF9A40"
        page.controls.append(menu)
        page.controls.append(ft.Container(image_repeat=ft.ImageRepeat.REPEAT, content=edit_poem_view,
                                          image_src="assets/images/img-1.png", image_fit=ft.ImageFit.SCALE_DOWN,
                                          image_opacity=0.3))
        reveal_back_button()
        page.update()

    def open_new_poem_view(e):
        global current_page
        current_page = "Edit"

        edit_poem_view = EditPoemView()
        page.controls.clear()
        page.controls.append(get_edit_page_menu())
        page.controls.append(ft.Container(image_repeat=ft.ImageRepeat.REPEAT, content=edit_poem_view,
                                          image_src="assets/images/img-1.png", image_fit=ft.ImageFit.SCALE_DOWN,
                                          image_opacity=0.3))
        # Add back button
        reveal_back_button()
        page.update()

    def reveal_back_button():
        # Add back button
        page.appbar.leading = ft.IconButton(
            icon=ft.icons.ARROW_BACK_SHARP, bgcolor="white",
            icon_color="#BF9A40", scale=0.8,
            height=35, on_click=back_button_clicked
        )

        # page.floating_action_button = ft.FloatingActionButton(
        #     bgcolor=ft.colors.BLUE_GREY_600,
        #     on_click=back_button_clicked,
        #     opacity=0.7,
        #     content=ft.Icon(name=ft.icons.ARROW_BACK, color="#BF9A40")
        # )
        # page.floating_action_button_location = ft.FloatingActionButtonLocation.MINI_END_DOCKED

    def delete_poem(e):
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirm", color="#BF9A40"),
            content=ft.Text(f"Are you sure you want to delete poem: {e.control.data}?"),
            actions=[
                ft.TextButton("Yes", data=e.control.data, on_click=delete_confirmed,
                              style=ft.ButtonStyle(color="#BF9A40")),
                ft.TextButton("Cancel", on_click=close_page_dialog, style=ft.ButtonStyle(color="#BF9A40"))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    def close_page_dialog(e):
        page.dialog.open = False
        page.update()

    def delete_confirmed(e):
        print(f"Performing deletion operations: {e.control.data}")
        database.delete_poem(e.control.data)
        page.dialog.open = False
        open_home_page(None)
        # page.update()

    def show_about_dialog(e):
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("About", color="#BF9A40"),
            content=ft.Text("""This app was created by: Malone Napier-Jameson.\n\nGit: https://github.com/MaloneMKD\n
            \nCode and contact information available on git.\nHappy Writing!""", ),
            actions=[
                ft.TextButton("Close", on_click=close_page_dialog, style=ft.ButtonStyle(color="#BF9A40"))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = dialog
        dialog.open = True
        page.update()

    # Data
    # Page configurations
    page.horizontal_alignment = "center"
    page.vertical_alignment = "start"
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = "white"

    # App bar
    page.appbar = ft.AppBar(
        title=ft.Text("(´•  •`) Wordsmith", no_wrap=True, color=ft.colors.WHITE,
                      theme_style=ft.TextThemeStyle.TITLE_LARGE, weight=ft.FontWeight.W_500),
        bgcolor="#BF9A40",
        toolbar_height=50,
        elevation=20,
        color='#000000',
        actions=[ft.IconButton(icon=ft.icons.INFO, icon_color="white", on_click=show_about_dialog, tooltip="About App")]
    )
    page.add(get_home_page_menu(), get_poem_grid_view())
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER


# End Main Function_____________________________________________________________________________________________________


if __name__ == '__main__':
    ft.app(target=main, assets_dir='assets')
