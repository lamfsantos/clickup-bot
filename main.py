import os
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
from clickup_client import ClickUpClient

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CLICKUP_API_TOKEN = os.getenv("CLICKUP_API_TOKEN")
CLICKUP_LIST_ID = os.getenv("CLICKUP_LIST_ID")

if not all([DISCORD_TOKEN, CLICKUP_API_TOKEN, CLICKUP_LIST_ID]) or "seu_" in DISCORD_TOKEN:
    print("❌ Erro: Certifique-se de configurar DISCORD_TOKEN, CLICKUP_API_TOKEN e CLICKUP_LIST_ID no .env")
    exit(1)

# Inicializa o cliente do ClickUp
clickup = ClickUpClient(api_token=CLICKUP_API_TOKEN)

# Configura as intents do Discord (o que o bot tem permissão de ver)
intents = discord.Intents.default()

class ClickUpBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        # Sincroniza os slash commands com o servidor do Discord ao iniciar
        print("Sincronizando comandos slash...")
        await self.tree.sync()
        print("Comandos sincronizados com sucesso!")

    async def on_ready(self):
        print(f"✅ Bot conectado como {self.user} (ID: {self.user.id})")
        print("Pronto para receber comandos!")

bot = ClickUpBot()

@bot.tree.command(name="tarefa", description="Cria um novo card no ClickUp")
@app_commands.describe(
    nome="Título da tarefa",
    descricao="Descrição detalhada (opcional)"
)
async def criar_tarefa(interaction: discord.Interaction, nome: str, descricao: str = None):
    # O 'defer' avisa ao Discord que estamos processando a requisição.
    # Isso evita que o comando dê timeout se a API do ClickUp demorar um pouco.
    await interaction.response.defer(ephemeral=False)
    
    try:
        # Cria a task usando nossa classe base
        task = clickup.create_task(
            list_id=CLICKUP_LIST_ID,
            name=nome,
            description=descricao
        )
        
        task_url = task.get("url")
        
        # Cria um card (embed) visualmente bonito pro Discord
        embed = discord.Embed(
            title="✅ Tarefa Criada!",
            description=f"A tarefa **[{nome}]({task_url})** foi criada com sucesso no ClickUp.",
            color=discord.Color.brand_green()
        )
        
        if descricao:
            # Mostra uma prévia da descrição no Discord
            embed.add_field(name="Descrição", value=descricao[:1000] + ("..." if len(descricao) > 1000 else ""), inline=False)
            
        await interaction.followup.send(embed=embed)
        
    except Exception as e:
        print(f"Erro ao criar tarefa via comando: {e}")
        await interaction.followup.send("❌ Ocorreu um erro ao criar a tarefa. Verifique os logs do servidor.", ephemeral=True)

@bot.tree.command(name="help", description="Mostra o tutorial de uso do bot do ClickUp")
async def ajuda(interaction: discord.Interaction):
    embed = discord.Embed(
        title="🤖 Como usar o ClickUp Bot",
        description="Este bot permite criar tarefas no ClickUp diretamente pelo Discord de forma rápida e prática.",
        color=discord.Color.blue()
    )
    embed.add_field(
        name="Comando Principal",
        value="Use o comando **`/tarefa`** e preencha os campos:\n"
              "• `nome`: O título do card que vai aparecer no ClickUp *(obrigatório)*.\n"
              "• `descricao`: Os detalhes e contexto da tarefa *(opcional)*.\n\n"
              "O próprio Discord vai mostrar uma caixinha para preencher cada um dos campos assim que você começar a digitar `/tarefa`.",
        inline=False
    )
    embed.set_footer(text="Ao final, o bot responderá com o link para você acessar o card gerado no quadro.")
    
    # ephemeral=True faz a mensagem aparecer apenas para quem pediu a ajuda (não polui o chat de todo mundo)
    await interaction.response.send_message(embed=embed, ephemeral=True)

if __name__ == "__main__":
    print("🚀 Inicializando o Bot do Discord...")
    bot.run(DISCORD_TOKEN)
