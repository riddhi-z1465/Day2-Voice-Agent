import asyncio
import certifi
import os
# Fix SSL issue on Mac
os.environ["SSL_CERT_FILE"] = certifi.where()

from dotenv import load_dotenv
from livekit.plugins import deepgram
from livekit.agents import stt

load_dotenv(".env.local")

async def test_deepgram():
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        print("DEEPGRAM_API_KEY not found in .env.local")
        return

    print(f"Testing Deepgram with key: {api_key[:4]}...{api_key[-4:]}")
    
    try:
        # Try to initialize and connect
        stt_instance = deepgram.STT(model="nova-3")
        # We can't easily "test" it without audio, but initialization often checks auth or we can try a simple operation if the SDK supports it.
        # However, the error was in `_connect_ws`, which happens during operation.
        # Let's try to simulate what the agent does: create a stream.
        
        print("Deepgram STT initialized. Note: Actual connection usually happens on first audio frame or stream start.")
        print("If this script runs without immediate error, the SDK import and basic setup are correct.")
        print("To truly test connection, we might need to send a dummy frame, but that requires more setup.")
        
        # Let's try to verify the key by making a simple HTTP request to Deepgram API manually, 
        # as the SDK might wrap things tightly.
        import aiohttp
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Token {api_key}"}
            async with session.get("https://api.deepgram.com/v1/projects", headers=headers) as resp:
                if resp.status == 200:
                    print("Successfully authenticated with Deepgram API (HTTP check).")
                    data = await resp.json()
                    print(f"Projects accessible: {len(data.get('projects', []))}")
                else:
                    print(f"Failed to authenticate with Deepgram API. Status: {resp.status}")
                    print(await resp.text())

    except Exception as e:
        print(f"Error testing Deepgram: {e}")

if __name__ == "__main__":
    asyncio.run(test_deepgram())
