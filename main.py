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
roles = {
    "financeiro": 1142089190050365510,
    "atendimento": 1255507654436978878,
    "paralegal": 1142114484819865742,
    "dev": 1142088423390326934,
    "produto": 1313606989456084992,
    "cs": 1318209546820391013,
    "comercial": 1142089078947446856,
    "marketing": 1142088996105756712,
    "operacional": 1142088914253910117,
}

times_do_lixo = {
   0: f"Times: <@&{roles['financeiro']}> e <@&{roles['atendimento']}>",
    1: f"Time: <@&{roles['paralegal']}>",
    2: f"Times: <@&{roles['dev']}>, <@&{roles['produto']}> e <@&{roles['cs']}>",
    3: f"Times: <@&{roles['comercial']}> e <@&{roles['marketing']}>",
    4: f"Time: <@&{roles['operacional']}>",
}

imagens_do_lixo = {
    0: "https://ocp.news/wp-content/uploads/2025/04/CORO.jpg",   # Segunda
    1: "https://super.abril.com.br/wp-content/uploads/2017/03/preto-no-branco-a-explicac3a7c3a3o-cientc3adfica-para-as-cores-do-panda.png?crop=1&resize=1212,909",    # Terça
    2: "https://static.nationalgeographicbrasil.com/files/styles/image_3200/public/nationalgeographic2683012_0.webp?w=760&h=507",          # Quarta
    3: "https://static.ndmais.com.br/2021/12/lagarto-teiu.jpg",    # Quinta
    4: "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTFH9G93CHQUJBFhUdhYu-HZpd9tlpLLQtqwQ&s",  # Sexta
}

async def enviar_lembrete():
    canal = bot.get_channel(CANAL_ID)
    hoje = datetime.datetime.now(TZ).weekday()
    if hoje in times_do_lixo:
        embed = discord.Embed(
            title="🗑️ Lembrete de Lixo",
            description=(
                f"Hoje é dia de recolher o lixo às **13:30**.\n\n"
                f"Responsáveis: {times_do_lixo[hoje]}"
            ),
            color=discord.Color.dark_purple()
        )


@tasks.loop(minutes=1)
async def checar_horario():
    agora = datetime.datetime.now(TZ)
    # Verifica se é 13:30
    if agora.hour == 15 and agora.minute == 20:
        await enviar_lembrete()

@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    checar_horario.start()

bot.run(TOKEN)
