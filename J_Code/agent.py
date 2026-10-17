from dotenv import load_dotenv
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions, ChatContext, ChatMessage
from livekit.plugins import google, noise_cancellation

# Import your custom modules
from Jarvis_prompts import instructions_prompt, Reply_prompts
from Jarvis_google_search import google_search, get_current_datetime
from jarvis_get_whether import get_weather
from Jarvis_window_CTRL import open_app, close_app, folder_file
from Jarvis_file_opner import Play_file
from keyboard_mouse_CTRL import (
    move_cursor_tool, mouse_click_tool, scroll_cursor_tool, 
    type_text_tool, press_key_tool, swipe_gesture_tool, 
    press_hotkey_tool, control_volume_tool
)
from memory_loop import MemoryExtractor

load_dotenv()


class Assistant(Agent):
    def __init__(self, chat_ctx) -> None:
        super().__init__(chat_ctx = chat_ctx,
                        instructions=instructions_prompt,
                        llm=google.beta.realtime.RealtimeModel(voice="Charon"),
                        tools=[
                                google_search,
                                get_current_datetime,
                                get_weather,
                                open_app,
                                close_app,
                                folder_file,
                                Play_file,
                                move_cursor_tool,
                                mouse_click_tool,
                                scroll_cursor_tool,
                                type_text_tool,
                                press_key_tool,
                                press_hotkey_tool,
                                control_volume_tool,
                                swipe_gesture_tool]
                                )

async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        preemptive_generation=True
    )
    
    #getting the current memory chat
    current_ctx = session.history.items
    

    await session.start(
        room=ctx.room,
        agent=Assistant(chat_ctx=current_ctx), #sending currenet chat to llm in realtime
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC()
        ),
    )
    await session.generate_reply(
        instructions=Reply_prompts
    )
    conv_ctx = MemoryExtractor()
    await conv_ctx.run(current_ctx)
    


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

    