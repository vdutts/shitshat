import reflex as rx
from app.states.yak_state import YakState
from app.components.post_card import post_card
from app.components.create_post_dialog import create_post_dialog
from app.db.database import create_db_and_tables
from app.pages.post_detail import post_detail


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.icon("waves", class_name="h-8 w-8 text-teal-500"),
                rx.el.h1("SLU Yak", class_name="text-2xl font-bold text-gray-800"),
                class_name="flex items-center gap-3",
            ),
            rx.el.div(
                rx.el.p("Peek Score", class_name="text-xs text-gray-500"),
                rx.el.div(
                    rx.icon("gem", class_name="h-4 w-4 text-purple-500"),
                    rx.el.p(
                        YakState.peek_score,
                        class_name="font-bold text-lg text-purple-600",
                    ),
                    class_name="flex items-center gap-1.5",
                ),
                class_name="text-right",
            ),
            class_name="container mx-auto flex items-center justify-between px-4",
        ),
        class_name="w-full py-4 bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-40 shadow-[0px_4px_8px_rgba(0,0,0,0.05)]",
    )


def sort_tabs() -> rx.Component:
    def tab_button(name: str, sort_key: str) -> rx.Component:
        is_active = YakState.sort_by == sort_key
        return rx.el.button(
            name,
            on_click=lambda: YakState.set_sort_by(sort_key),
            class_name=rx.cond(
                is_active,
                "px-4 py-2 font-semibold text-white bg-teal-500 rounded-full transition-all duration-300",
                "px-4 py-2 font-semibold text-gray-600 bg-gray-100 hover:bg-gray-200 rounded-full transition-all duration-300",
            ),
        )

    return rx.el.div(
        tab_button("Hot", "hot"),
        tab_button("New", "new"),
        class_name="flex items-center gap-2",
    )


def index() -> rx.Component:
    return rx.el.main(
        header(),
        rx.el.div(
            rx.el.div(sort_tabs(), class_name="flex justify-center mb-6"),
            rx.el.div(
                rx.foreach(YakState.posts, post_card), class_name="flex flex-col gap-4"
            ),
            class_name="container mx-auto max-w-2xl px-4 py-8",
        ),
        create_post_dialog(),
        class_name="font-['Poppins'] bg-gray-50 min-h-screen",
    )


@rx.event
def on_load_and_create_db():
    create_db_and_tables()
    return [YakState.load_posts, YakState.clear_post_detail]


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/", on_load=on_load_and_create_db)
app.add_page(post_detail, route="/post/[post_id]", on_load=YakState.get_post_by_id)