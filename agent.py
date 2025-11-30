from dotenv import load_dotenv
import os
import asyncio
from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import google, noise_cancellation
from prompts import AGENT_INSTRUCTION, SESSION_INSTRUCTION
from tools import get_weather, search_web, send_email

load_dotenv()

class MobileAssistant(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions=AGENT_INSTRUCTION,
            llm=google.beta.realtime.RealtimeModel(
                voice="Aoede",
                temperature=0.8,
            ),
            tools=[
                get_weather,
                search_web,
                send_email
            ],
        )

async def mobile_entrypoint(ctx: agents.JobContext):
    """Mobile-optimized entrypoint with better error handling"""
    try:
        # Initialize session with mobile-friendly settings
        session = AgentSession()
        
        await session.start(
            room=ctx.room,
            agent=MobileAssistant(),
            room_input_options=RoomInputOptions(
                video_enabled=False,  # Disable video for mobile optimization
                audio_enabled=True,
                noise_cancellation=noise_cancellation.BVC(),
            ),
        )

        await ctx.connect()
        
        # Mobile-friendly greeting
        await session.generate_reply(
            instructions=SESSION_INSTRUCTION,
        )
        
        # Keep the connection alive
        while True:
            await asyncio.sleep(10)
            
    except Exception as e:
        print(f"Mobile assistant error: {e}")
        # Attempt reconnection
        await asyncio.sleep(5)
        await mobile_entrypoint(ctx)

if __name__ == "__main__":
    # Mobile-optimized worker options
    mobile_options = agents.WorkerOptions(
        entrypoint_fnc=mobile_entrypoint,
        # Better for mobile connections
        reconnect_timeout=30,
        max_retries=5
    )
    agents.cli.run_app(mobile_options)