import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from database import executar_query
from views import TicketView, TicketControlView
from utils import gerar_relatorio_txt

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot ativo como {bot.user}")
    bot.add_view(TicketView())
    bot.add_view(TicketControlView())

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    result = executar_query("SELECT token FROM chamados WHERE canal_id = %s AND status != 'FECHADO'", (message.channel.id,), fetchone=True)
    if result:
        executar_query(
            "INSERT INTO mensagens_chamados (token, autor_id, autor_nome, conteudo) VALUES (%s, %s, %s, %s)",
            (result[0], message.author.id, str(message.author), message.content), commit=True
        )

    await bot.process_commands(message)

@bot.command()
@commands.has_permissions(administrator=True)
async def relatorio(ctx, token: str):
    buffer, filename = gerar_relatorio_txt(token.upper())
    if not buffer:
        await ctx.send(f"[Erro] Nenhum registro encontrado para o token `{token}`.")
        return
    await ctx.send(f"**Relatorio do Atendimento `{token.upper()}`:**", file=discord.File(buffer, filename=filename))

@bot.command()
@commands.has_permissions(administrator=True)
async def painel(ctx):
    embed = discord.Embed(
        title="Central de Suporte via Token",
        description="Clique abaixo para abrir um atendimento.",
        color=discord.Color.dark_purple()
    )
    await ctx.send(embed=embed, view=TicketView())

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)