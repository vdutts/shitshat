import reflex as rx
from app.states.yak_state import YakState, Comment
from app.components.post_card import post_card


def comment_card(comment: Comment) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.image(
                src=f"https://api.dicebear.com/9.x/initials/svg?seed={comment['id']}",
                class_name="h-8 w-8 rounded-full bg-gray-200",
            ),
            rx.el.div(
                rx.el.p(comment["content"], class_name="text-sm text-gray-800"),
                rx.el.p(comment["created_at"], class_name="text-xs text-gray-500 mt-1"),
                class_name="flex-1",
            ),
        ),
        class_name="flex items-start gap-3 p-4 border-b border-gray-100",
    )


def create_comment_form() -> rx.Component:
    return rx.el.div(
        rx.el.textarea(
            placeholder="Add a comment...",
            on_change=YakState.set_new_comment_content,
            max_length=150,
            class_name="w-full h-24 p-3 text-sm text-gray-800 bg-white rounded-lg border border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all duration-200 placeholder-gray-400 resize-none",
            default_value=YakState.new_comment_content,
        ),
        rx.el.div(
            rx.el.p(
                f"{YakState.comment_char_count} / 150",
                class_name=rx.cond(
                    YakState.comment_char_count > 150,
                    "text-xs font-medium text-red-500",
                    "text-xs font-medium text-gray-500",
                ),
            ),
            rx.el.button(
                "Comment",
                on_click=lambda: YakState.add_comment(YakState.post_detail["id"]),
                disabled=YakState.is_comment_invalid,
                class_name="""
                    px-5 py-2 bg-teal-500 text-white font-semibold rounded-full text-sm
                    hover:bg-teal-600 transition-colors shadow-[0px_1px_3px_rgba(0,0,0,0.12)] 
                    disabled:bg-gray-300 disabled:cursor-not-allowed disabled:shadow-none
                """,
            ),
            class_name="flex justify-between items-center mt-2",
        ),
        class_name="p-4 bg-gray-50 border-t border-gray-200",
    )


def post_detail_view() -> rx.Component:
    return rx.el.div(
        rx.cond(
            YakState.post_detail,
            rx.el.div(
                post_card(YakState.post_detail, is_link=False),
                rx.el.div(
                    rx.el.h3(
                        "Comments",
                        class_name="text-lg font-bold text-gray-800 px-4 pt-4 pb-2",
                    ),
                    rx.foreach(YakState.post_detail["comments"], comment_card),
                    class_name="bg-white rounded-lg shadow-[0px_1px_3px_rgba(0,0,0,0.12)] mt-4 overflow-hidden",
                ),
                class_name="flex flex-col gap-4",
            ),
            rx.el.div(
                rx.el.div(
                    class_name="h-24 w-full bg-gray-200 rounded-lg animate-pulse"
                ),
                rx.el.p(
                    "Loading post or post not found...",
                    class_name="text-center text-gray-500 mt-4",
                ),
                class_name="p-4",
            ),
        ),
        class_name="container mx-auto max-w-2xl px-4 py-8",
    )


def post_detail() -> rx.Component:
    return rx.el.main(
        rx.el.header(
            rx.el.div(
                rx.link(
                    rx.el.div(
                        rx.icon("arrow_left", class_name="h-6 w-6 text-gray-600"),
                        rx.el.p(
                            "Back to Feed", class_name="font-semibold text-gray-700"
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    href="/",
                ),
                class_name="container mx-auto flex items-center justify-start px-4",
            ),
            class_name="w-full py-4 bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-40 shadow-[0px_4px_8px_rgba(0,0,0,0.05)]",
        ),
        post_detail_view(),
        rx.cond(
            YakState.post_detail,
            rx.el.div(create_comment_form(), class_name="sticky bottom-0 z-10"),
        ),
        class_name="font-['Poppins'] bg-gray-50 min-h-screen",
    )