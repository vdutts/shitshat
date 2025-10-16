import reflex as rx
from app.states.yak_state import YakState


def create_post_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.trigger(
            rx.el.button(
                rx.icon("copy", class_name="h-6 w-6"),
                class_name="""
                    fixed bottom-6 right-6 z-40 h-14 w-14 rounded-full bg-teal-500 text-white 
                    flex items-center justify-center shadow-[0px_6px_10px_rgba(0,0,0,0.15)] 
                    hover:bg-teal-600 hover:shadow-[0px_8px_16px_rgba(0,0,0,0.2)] 
                    active:shadow-[0px_2px_4px_rgba(0,0,0,0.2)]
                    transition-all duration-300 ease-in-out
                """,
            )
        ),
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.radix.primitives.dialog.title(
                            "What's on your mind?",
                            class_name="text-xl font-bold text-gray-800",
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                rx.icon("x", class_name="text-gray-500"),
                                class_name="p-1 rounded-full hover:bg-gray-100 transition-colors",
                            )
                        ),
                        class_name="flex justify-between items-center pb-3 border-b border-gray-200 mb-4",
                    ),
                    rx.el.textarea(
                        placeholder="Share your anonymous thoughts...",
                        on_change=YakState.set_new_post_content,
                        max_length=200,
                        class_name="w-full h-32 p-3 text-base text-gray-800 bg-gray-50 rounded-lg border border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-transparent transition-all duration-200 placeholder-gray-400 resize-none",
                        default_value=YakState.new_post_content,
                    ),
                    rx.el.div(
                        rx.el.p(
                            rx.cond(
                                YakState.char_count > 200,
                                f"{YakState.char_count} / 200",
                                f"{YakState.char_count} / 200",
                            ),
                            class_name=rx.cond(
                                YakState.char_count > 200,
                                "text-sm font-medium text-red-500",
                                "text-sm font-medium text-gray-500",
                            ),
                        ),
                        rx.radix.primitives.dialog.close(
                            rx.el.button(
                                "Post",
                                on_click=YakState.create_post,
                                disabled=YakState.is_post_invalid,
                                class_name="""
                                    px-6 py-2 bg-teal-500 text-white font-semibold rounded-full 
                                    hover:bg-teal-600 transition-colors shadow-[0px_1px_3px_rgba(0,0,0,0.12)] 
                                    disabled:bg-gray-300 disabled:cursor-not-allowed disabled:shadow-none
                                """,
                            )
                        ),
                        class_name="flex justify-between items-center mt-3",
                    ),
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white p-6 rounded-xl shadow-xl w-full max-w-lg z-50",
            ),
        ),
        open=YakState.show_create_dialog,
        on_open_change=YakState.set_show_create_dialog,
    )