import discord
import asyncio
from datetime import datetime
from config import CATEGORY_ID, CANAL_LOGS_ID, NOME_CARGO_SUPORTE
from database import executar_query
from utils import gerar_token, gerar_relatorio_txt

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Abrir Atendimento", style=discord.ButtonStyle.primary, custom_id="open_ticket")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild, user = interaction.guild, interaction.user
        category = guild.get_channel(CATEGORY_ID)

        token_atendimento = gerar_token()
        while executar_query("SELECT id FROM chamados WHERE token = %s", (token_atendimento,), fetchone=True):
            token_atendimento = gerar_token()

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        channel_name = f"chat-{token_atendimento.lower()}"
        ticket_channel = await category.create_text_channel(name=channel_name, overwrites=overwrites)

        executar_query(
            "INSERT INTO chamados (token, usuario_id, usuario_nome, canal_id) VALUES (%s, %s, %s, %s)",
            (token_atendimento, user.id, str(user), ticket_channel.id), commit=True
        )

        embed = discord.Embed(
            title=f"Atendimento Iniciado - {token_atendimento}",
            description=f"Ola {user.mention}, descreva seu problema. Aguarde um atendente.",
            color=discord.Color.blue()
        )

        await ticket_channel.send(embed=embed, view=TicketControlView(token_atendimento))
        await interaction.response.send_message(f"Atendimento criado: {ticket_channel.mention}", ephemeral=True)

class TicketControlView(discord.ui.View):
    def __init__(self, token_atendimento=None):
        super().__init__(timeout=None)
        self.token_atendimento = token_atendimento

    @discord.ui.button(label="Assumir Atendimento", style=discord.ButtonStyle.success, custom_id="claim_ticket")
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        staff = interaction.user
        e_admin = staff.guild_permissions.administrator
        tem_cargo = discord.utils.get(staff.roles, name=NOME_CARGO_SUPORTE) is not None

        if not (e_admin or tem_cargo):
            await interaction.response.send_message("[Erro] Acesso restrito ao Suporte/Admin.", ephemeral=True)
            return

        resultado = executar_query("SELECT usuario_id FROM chamados WHERE canal_id = %s", (interaction.channel.id,), fetchone=True)
        if resultado and resultado[0] == staff.id:
            await interaction.response.send_message("[Erro] Voce nao pode assumir seu proprio chamado.", ephemeral=True)
            return

        executar_query(
            "UPDATE chamados SET atendente_id = %s, atendente_nome = %s, status = 'EM_ANDAMENTO' WHERE canal_id = %s AND status = 'ABERTO'",
            (staff.id, str(staff), interaction.channel.id), commit=True
        )

        button.disabled = True
        await interaction.response.edit_message(view=self)
        await interaction.followup.send(f"Atendimento assumido por {staff.mention}")

    @discord.ui.button(label="Encerrar Chat", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        staff = interaction.user
        resultado = executar_query("SELECT usuario_id, token FROM chamados WHERE canal_id = %s", (interaction.channel.id,), fetchone=True)

        if not resultado:
            await interaction.response.send_message("[Erro] Falha ao localizar chamado.", ephemeral=True)
            return

        usuario_id, token = resultado
        e_admin = staff.guild_permissions.administrator
        tem_cargo = discord.utils.get(staff.roles, name=NOME_CARGO_SUPORTE) is not None
        e_dono = usuario_id == staff.id

        if not (e_admin or tem_cargo or e_dono):
            await interaction.response.send_message("[Erro] Sem permissao para fechar este atendimento.", ephemeral=True)
            return

        executar_query("UPDATE chamados SET status = 'FECHADO', data_fechamento = %s WHERE canal_id = %s", (datetime.now(), interaction.channel.id), commit=True)
        await interaction.response.send_message("Encerrando atendimento e gerando relatorio...")

        buffer, filename = gerar_relatorio_txt(token)
        if buffer:
            canal_logs = interaction.guild.get_channel(CANAL_LOGS_ID)
            if canal_logs:
                await canal_logs.send(f"**Relatorio de Atendimento** - Token: `{token}`", file=discord.File(buffer, filename=filename))
                buffer.seek(0)

            try:
                cliente = await interaction.client.fetch_user(usuario_id)
                await cliente.send(f"Seu atendimento `{token}` foi encerrado. O relatorio esta em anexo:", file=discord.File(buffer, filename=filename))
            except Exception:
                pass

        await asyncio.sleep(4)
        await interaction.channel.delete()