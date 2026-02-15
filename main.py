from dataclasses import dataclass, field
import flet as ft


@ft.observable
@dataclass
class Message:
    author: str
    msg: str


@ft.observable
@dataclass
class App:
    messages: list[Message] = field(default_factory=list)

    def add_message(self, author: str, msg: str) -> None:
        self.messages.append(Message(author, msg))


@ft.component
def Title() -> ft.Text:
    return ft.Text("Make your own Chat Application with Ollama and Langchain",
                    color=ft.Colors.SECONDARY,
                    size=24,
                    text_align=ft.MainAxisAlignment.CENTER,
                    weight=ft.FontWeight.BOLD
                    )

@ft.component
def MessageForm(add_message: callable) -> ft.Column:
    msg, set_msg = ft.use_state('')
    
    def on_click(e: ft.Event) -> None:
        if msg.strip():
            add_message("me", msg)
            set_msg("")
    
    return ft.Column(
        controls=[
            ft.TextField(value=msg,
                         label="Type your message",
                         multiline=True,
                         expand=True,
                         on_change= lambda e: set_msg(e.control.value),
                        ),
            ft.Row(
                ft.OutlinedButton("Submit",
                              style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
                              on_click=on_click,
                        ),
                alignment=ft.MainAxisAlignment.END
            )
            
        ]
    )

@ft.component
def MessageView(msg: Message) -> ft.Row:
    
    
    return ft.Row(
        controls=[
            ft.Text(f"{msg.author}:"),
            ft.Text(msg.msg),
        ] if msg.author == "me"
        else [
            ft.Text(msg.msg),
            ft.Text(f":{msg.author}"),
        ],
        alignment=ft.MainAxisAlignment.END if msg.author == 'bot' else ft.MainAxisAlignment.START
    )

@ft.component
def AppBar(page: ft.Page, set_search: callable, search: bool) -> ft. AppBar:
    icon, set_icon = ft.use_state(ft.Icons.LIGHT_MODE)
    mode, set_mode = ft.use_state(ft.ThemeMode.LIGHT)
    
    def icon_toggle(e):
        if icon == ft.Icons.LIGHT_MODE:
            set_icon(ft.Icons.DARK_MODE)
            page.theme_mode = ft.ThemeMode.DARK
        else:
            set_icon(ft.Icons.LIGHT_MODE)
            set_mode(ft.ThemeMode.LIGHT)
            page.theme_mode = ft.ThemeMode.LIGHT

    return ft.AppBar(
                leading=ft.Icon(ft.Icons.AUTO_AWESOME),
                title=ft.Text("CHATBOT"),
                actions=[
                    ft.IconButton(ft.Icons.SEARCH, on_click=lambda e: set_search(not search)),
                    ft.IconButton(icon, on_click=icon_toggle, margin=ft.Margin.only(right=5)),
                ],
                bgcolor=ft.Colors.SURFACE_CONTAINER,
    
)

@ft.component
def AppView(page: ft.Page) -> ft.View:
    app, _ = ft.use_state(
        App(
            messages=[Message('me', 'Hello'),
                      Message('bot', 'Hello, how can I help you?'),
                      Message('me', 'Hello'),
                      Message('bot', 'Hello, how can I help you?')
                      ]
        )
    )
    search, set_search = ft.use_state(False)
    return ft.View(
            controls=[
                ft.SearchBar(bar_hint_text="Search...", visible=search),
                Title(),
                MessageForm(app.add_message),
                ft.Divider(),
                *[MessageView(msg) for msg in app.messages]
            ],
        appbar=AppBar(page, set_search, search),
        padding=ft.Padding.all(20),
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        
    )


def main(page: ft.Page):
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.GREEN)
    page.theme_mode = ft.ThemeMode.LIGHT
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.TEAL_ACCENT)
    

    page.title = "Chat App"
    page.render_views(lambda: AppView(page))

if __name__ == "__main__":
    ft.run(main)
