import reflex as rx
from app.states.yak_state import YakState, Post


def vote_button(post_id: str, direction: int, user_vote: int) -> rx.Component:
    is_active = user_vote == direction
    icon_name = rx.cond(direction == 1, "arrow_up", "arrow_down")
    active_color = rx.cond(direction == 1, "text-teal-500", "text-red-500")
    return rx.el.button(
        rx.icon(
            tag=icon_name,
            class_name=rx.cond(
                is_active,
                f"{active_color} transition-colors duration-200",
                "text-gray-400 group-hover:text-gray-600 transition-colors duration-200",
            ),
        ),
        on_click=lambda: YakState.handle_vote(post_id, direction),
        class_name="p-2 rounded-full group transition-all duration-200",
    )


def post_card_menu(post: Post) -> rx.Component:
    return rx.radix.dropdown_menu.root(
        rx.radix.dropdown_menu.trigger(
            rx.el.button(
                rx.icon("send_horizontal", class_name="text-gray-500"),
                class_name="p-1 rounded-full hover:bg-gray-100",
            )
        ),
        rx.radix.dropdown_menu.content(
            rx.radix.dropdown_menu.item(
                rx.el.div(
                    rx.icon("flag", class_name="h-4 w-4 mr-2"),
                    "Report Post",
                    class_name="flex items-center text-sm text-gray-700",
                ),
                on_click=lambda: YakState.report_post(post["id"]),
                class_name="hover:bg-gray-100 cursor-pointer",
            ),
            rx.cond(
                post["is_owner"],
                rx.radix.dropdown_menu.item(
                    rx.el.div(
                        rx.icon("trash_2", class_name="h-4 w-4 mr-2 text-red-500"),
                        "Delete Post",
                        class_name="flex items-center text-sm text-red-500",
                    ),
                    on_click=lambda: YakState.delete_post(post["id"]),
                    class_name="hover:bg-red-50 cursor-pointer",
                ),
                rx.fragment(),
            ),
            class_name="bg-white shadow-lg rounded-lg border border-gray-100 p-1",
        ),
    )


def post_card(post: Post, is_link: bool = True) -> rx.Component:
    card_content = rx.el.div(
        rx.el.div(
            vote_button(post["id"], 1, post["user_vote"]),
            rx.el.p(
                post["votes"], class_name="text-lg font-bold text-gray-800 tabular-nums"
            ),
            vote_button(post["id"], -1, post["user_vote"]),
            class_name="flex flex-col items-center justify-center bg-gray-50 rounded-xl p-2",
        ),
        rx.el.div(
            rx.el.p(
                post["content"],
                class_name="text-base text-gray-800 font-medium leading-relaxed",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("map_pin", class_name="h-4 w-4 text-gray-400 mr-1"),
                    rx.el.p(
                        "South Lake Union",
                        class_name="text-xs text-gray-500 font-semibold",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.icon(
                        "message-square", class_name="h-4 w-4 text-gray-400 mr-1.5"
                    ),
                    rx.el.p(
                        post["comments"].length().to_string(),
                        class_name="text-xs text-gray-500 font-semibold",
                    ),
                    rx.el.p(
                        post["created_at"],
                        class_name="text-xs text-gray-500 font-semibold ml-4",
                    ),
                    post_card_menu(post),
                    class_name="flex items-center gap-4",
                ),
                class_name="flex justify-between items-center mt-4",
            ),
            class_name="flex flex-col justify-between w-full h-full",
        ),
        class_name="""
            flex items-start gap-4 p-4 bg-white rounded-lg 
            shadow-[0px_1px_3px_rgba(0,0,0,0.12)] hover:shadow-[0px_4px_8px_rgba(0,0,0,0.15)] 
            transition-shadow duration-300 w-full
        """,
    )
    return rx.cond(
        is_link,
        rx.link(card_content, href=f"/post/{post['id']}", width="100%"),
        card_content,
    )