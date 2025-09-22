import os
import discord
from discord.ext import commands, tasks
import datetime
import asyncio
import pytz


TOKEN = os.getenv("TOKEN")
CANAL_ID = int(os.getenv("CANAL_ID"))

TZ = pytz.timezone("America/Sao_Paulo")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Dicionário com os times por dia da semana
# Segunda = 0 ... Domingo = 6
times_do_lixo = {
    0: "Times: **Financeiro** e **Atendimento**",
    1: "Time: **Paralegal**",
    2: "Times: **Devs** e **Produtos**",
    3: "Times: **Comercial** e **Marketing**",
    4: "Time: **Operacional**"
}

async def enviar_lembrete():
    canal = bot.get_channel(CANAL_ID)
    hoje = datetime.datetime.today(TZ).weekday()
    if hoje in times_do_lixo:  # Só envia se for dia útil
        await canal.send(
            f"🗑️ Olá! Hoje é dia de recolher o lixo às **13:30**.\nResponsáveis: {times_do_lixo[hoje]}"
        )

@tasks.loop(minutes=1)
async def checar_horario():
    agora = datetime.datetime.now(TZ)
    # Verifica se é 13:30
    if agora.hour == 15 and agora.minute == 38:
        await enviar_lembrete()

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    checar_horario.start()

bot.run(TOKEN)
