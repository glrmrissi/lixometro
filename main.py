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
    0: "Times: <@&ID_DO_ROLE_FINANCEIRO> e <@&ID_DO_ROLE_ATENDIMENTO>",
    1: "Time: <@&ID_DO_ROLE_PARALEGAL>",
    2: "Times: <@&ID_DO_ROLE_DEV> e <@&ID_DO_ROLE_PRODUTO>",
    3: "Times: <@&ID_DO_ROLE_COMERCIAL> e <@&ID_DO_ROLE_MARKETING>",
    4: "Time: <@&ID_DO_ROLE_OPERACIONAL>"
}

async def enviar_lembrete():
    canal = bot.get_channel(CANAL_ID)
    hoje = datetime.datetime.now(TZ).weekday()
    if hoje in times_do_lixo:  # Só envia se for dia útil
        await canal.send(
            f"🗑️ Olá! Hoje é dia de recolher o lixo às **13:30**.\nResponsáveis: {times_do_lixo[hoje]}"
        )

@tasks.loop(minutes=1)
async def checar_horario():
    agora = datetime.datetime.now(TZ)
    # Verifica se é 13:30
    if agora.hour == 9 and agora.minute == 00:
        await enviar_lembrete()

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    checar_horario.start()

bot.run(TOKEN)
