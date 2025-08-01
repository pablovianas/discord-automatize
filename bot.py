import os
import re
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

from app.db.db import check_if_user_exists, create_connection, save_user
from app.external_api.cademi import get_user_data
from app.utils.utils import manage_user

load_dotenv()

# Configura o bot com as intents necessárias
intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True  # Se precisar de acesso ao conteúdo de mensagens
bot = commands.Bot(command_prefix="!", intents=intents)

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN", None)

# IDs das roles (substitua pelos IDs reais do seu servidor)
DISCORD_NOOB_ROLE_ID = os.getenv("DISCORD_NOOB_ROLE_ID", "")
DISCORD_STUDENT_ROLE_ID = os.getenv("DISCORD_STUDENT_ROLE_ID", "")
DISCORD_CLASSROOM_ROLE_ID = os.getenv("DISCORD_CLASSROOM_ROLE_ID", "")

# Evento para quando o bot estiver pronto
@bot.event
async def on_ready():
    print(f"Bot está online como {bot.user}!")
    await create_connection()  # Cria a conexão com o banco de dados

    try:
        synced = await bot.tree.sync()
        print(f"Comandos sincronizados: {synced}")
    except Exception as e:
        print(f"Erro ao sincronizar comandos: {e}")


# Evento para atribuir a role "noob" ao entrar
@bot.event
async def on_member_join(member):
    guild = member.guild
    noob_role = discord.utils.get(guild.roles, id=DISCORD_NOOB_ROLE_ID)
    if noob_role:
        await member.add_roles(noob_role)
        print(f"Role 'noob' atribuída a {member.name}#{member.discriminator}")


# Classe para o modal do formulário
class VerifyModal(discord.ui.Modal, title="Formulário de Verificação"):
    def __init__(self):
        super().__init__()
        self.name = discord.ui.TextInput(
            label="Nome Completo", placeholder="Digite seu nome completo", required=True
        )
        self.email = discord.ui.TextInput(
            label="E-mail", placeholder="Digite seu e-mail", required=True
        )
        self.add_item(self.name)
        self.add_item(self.email)

    async def on_submit(self, interaction: discord.Interaction):
        email_valido = re.match(r"[^@]+@[^@]+\.[^@]+", self.email.value)

        if not email_valido:
            await interaction.response.send_message("E-mail enviado está no formato inválido! Por favor, tente novamente.", ephemeral=True)
            return

        if await check_if_user_exists(interaction.user.id):
            await interaction.response.send_message(
                "Você já está verificado! Acesse os canais da comunidade.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            f"Verificação recebida!\nNome: {self.name.value}\nE-mail: {self.email.value}\n"
            "Aguarde a confirmação do suporte. Obrigado!",
            ephemeral=True,
        )

        user = get_user_data(self.email.value)  # Chama a API externa para obter dados do usuário

        if user:
            await interaction.followup.send(
                f"Usuário encontrado: {self.name.value}. Acesso concedido!",
                ephemeral=True,
            )
         
            nome_cademi = user['data']['usuario']['nome']
            email_cademi = user['data']['usuario']['email']
            id_cademi = user['data']['usuario']['id']
            cademi_user_created_at = user['data']['usuario']['criado_em']

            await manage_user(interaction, DISCORD_NOOB_ROLE_ID, DISCORD_STUDENT_ROLE_ID, DISCORD_CLASSROOM_ROLE_ID, nome_cademi)
            
            await save_user(interaction, nome_cademi=nome_cademi, email_cademi=email_cademi, id_cademi=id_cademi, cademi_user_created_at=cademi_user_created_at)

        else:
            await interaction.followup.send(
                "Usuário não encontrado. Verifique seu e-mail e tente novamente.",
                ephemeral=True,
            )


# Classe do botão
class VerifyButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)  # Timeout None para o botão não expirar

    @discord.ui.button(
        label="LIBERAR MEU ACESSO",
        style=discord.ButtonStyle.success,
        custom_id="verify_button",
    )
    async def verify_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        modal = VerifyModal()
        await interaction.response.send_modal(modal)


# Comando /verificar
@app_commands.command(
    name="verificar", description="Inicia o processo de verificação no servidor."
)
async def verificar(interaction: discord.Interaction):
    view = VerifyButton()
    await interaction.response.send_message(
        content="**VOCÊ ESTÁ NA SALA DE ESPERA DA COMUNIDADE EXCLUSIVA DE ALUNOS DO DEVQUEST ❤️**\n\n"
        "Essa sala serve para confirmarmos sua matrícula, antes de liberarmos o acesso ao resto da comunidade.\n\n"
        "**INSTRUÇÕES PARA RECEBER O ACESSO À COMUNIDADE COMPLETA:**\n"
        "1 - Clique no botão 'LIBERAR MEU ACESSO'\n"
        "2 - Preencha os dados solicitados\n"
        "3 - Envie o formulário\n\n"
        "Se seu e-mail for encontrado no sistema, você terá acesso a todos os canais dessa comunidade exclusiva!\n\n"
        "Qualquer dúvida ou dificuldade entre em contato com o nosso suporte no canal suporte-ao-aluno.\n\n",
        view=view,
    )


# Adiciona o comando ao bot
bot.tree.add_command(verificar)

# Inicia o bot
if DISCORD_BOT_TOKEN is None:
    raise ValueError("O token do Discord não foi encontrado. Verifique a variável de ambiente DISCORD_BOT_TOKEN.")

bot.run(DISCORD_BOT_TOKEN)
