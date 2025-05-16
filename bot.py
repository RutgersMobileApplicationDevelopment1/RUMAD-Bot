import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import discord
from env import env

# --- simple health‐check HTTP server on port ---
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b'OK')

def run_health_server():
    httpd = HTTPServer(('0.0.0.0', env['PORT']), HealthHandler)
    httpd.serve_forever()

# start HTTP server in background
threading.Thread(target=run_health_server, daemon=True).start()


# --- discord bot ---
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Messages "Hello!" when a user sends "$hello"
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(env["BOT_TOKEN"])