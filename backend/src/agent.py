import logging
import os
import certifi
import json
from typing import List, Annotated

# Fix SSL issue on Mac
os.environ["SSL_CERT_FILE"] = certifi.where()

from dotenv import load_dotenv
from livekit.agents import (
    Agent,
    AgentSession,
    JobContext,
    JobProcess,
    MetricsCollectedEvent,
    RoomInputOptions,
    WorkerOptions,
    cli,
    metrics,
    tokenize,
    llm,
    function_tool,
    RunContext
)
from livekit.plugins import murf, silero, google, deepgram, noise_cancellation
from livekit.plugins.turn_detector.multilingual import MultilingualModel

logger = logging.getLogger("agent")

load_dotenv(".env.local")

import time
from generate_order_html import generate_html

def save_order_to_file(drinkType: str, size: str, milk: str, extras: List[str], name: str):
    order_data = {
        "drinkType": drinkType,
        "size": size,
        "milk": milk,
        "extras": extras,
        "name": name
    }
    logger.info(f"Saving order: {order_data}")
    
    orders_dir = "orders"
    os.makedirs(orders_dir, exist_ok=True)
    
    timestamp = int(time.time())
    filename = f"{orders_dir}/order_{timestamp}.json"
    
    with open(filename, "w") as f:
        json.dump(order_data, f, indent=2)
        
    # Generate HTML visualization
    html_filename = f"{orders_dir}/order_{timestamp}.html"
    generate_html(order_data, html_filename)
    
    return "Order saved successfully."

class BaristaAgent(Agent):
    def __init__(self) -> None:
        super().__init__(
            instructions="""You are a friendly and knowledgeable barista at a premium coffee shop.
            Your goal is to take the customer's order efficiently while maintaining a warm and welcoming demeanor.
            
            You must collect the following information for every order:
            1. Drink Type (e.g., Latte, Cappuccino, Americano)
            2. Size (e.g., Small, Medium, Large)
            3. Milk Preference (e.g., Whole, Oat, Almond, Soy, None)
            4. Extras (e.g., Vanilla Syrup, Extra Shot, Sugar, None)
            5. Customer Name

            Ask clarifying questions one by one or in small groups to gather this information. 
            Do not assume any values. If the user doesn't specify, ask.
            
            Once you have ALL the required information, you MUST use the `submit_order` tool to save the order.
            After submitting, confirm to the user that their order has been placed.
            
            Keep your responses concise and conversational. Avoid long monologues.
            """,
        )

    @function_tool
    async def submit_order(
        self, 
        context: RunContext,
        drinkType: Annotated[str, "The type of coffee drink (e.g., Latte, Cappuccino)"],
        size: Annotated[str, "The size of the drink (Small, Medium, Large)"],
        milk: Annotated[str, "The type of milk (Whole, Oat, Almond, etc.)"],
        extras: Annotated[List[str], "List of any extras (Syrups, etc.) or empty list if none"],
        name: Annotated[str, "The customer's name"]
    ):
        """Submit the order to the system."""
        save_order_to_file(drinkType, size, milk, extras, name)
        return "Order submitted successfully."


def prewarm(proc: JobProcess):
    proc.userdata["vad"] = silero.VAD.load()


async def entrypoint(ctx: JobContext):
    # Logging setup
    ctx.log_context_fields = {
        "room": ctx.room.name,
    }

    # Set up a voice AI pipeline
    session = AgentSession(
        stt=deepgram.STT(model="nova-3"),
        llm=google.LLM(
                model="gemini-2.5-flash",
            ),
        tts=murf.TTS(
                voice="en-US-matthew", 
                style="Conversation",
                tokenizer=tokenize.basic.SentenceTokenizer(min_sentence_len=2),
                text_pacing=True
            ),
        turn_detection=MultilingualModel(),
        vad=ctx.proc.userdata["vad"],
        preemptive_generation=True,
    )

    usage_collector = metrics.UsageCollector()

    @session.on("metrics_collected")
    def _on_metrics_collected(ev: MetricsCollectedEvent):
        metrics.log_metrics(ev.metrics)
        usage_collector.collect(ev.metrics)

    async def log_usage():
        summary = usage_collector.get_summary()
        logger.info(f"Usage: {summary}")

    ctx.add_shutdown_callback(log_usage)

    # Start the session
    await session.start(
        agent=BaristaAgent(),
        room=ctx.room,
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
    )

    await ctx.connect()


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=prewarm))