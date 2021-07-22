import discord
from discord.ext import commands, tasks
from discord.ext.commands import cooldown, BucketType, CommandOnCooldown, BadArgument, CommandNotFound, \
    MaxConcurrencyReached
import asyncio
import random
from random import randint
import json
import time
import datetime
from PIL import Image
from io import BytesIO
import requests


client = commands.Bot(command_prefix='.')
IGNORE_EXCEPTIONS = (CommandNotFound, BadArgument)

@client.event
async def on_ready():
    canal = client.get_channel(844557756598059008)
    await canal.send('Fui iniciado com sucesso!')

@client.event
async def on_command_error(ctx, exc):
    if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
        pass
    elif isinstance(exc, CommandOnCooldown):
        #await ctx.send(f"Este comando está com cooldown. Tente novamente em {exc.retry_after:,.2f} segundos.")
        tempo = exc.retry_after/3600
        await ctx.send(f"Você já coletou seus **Songs** hoje! Tente novamente em **{tempo:,.2f}** horas.")
    elif isinstance(exc, MaxConcurrencyReached):
        await ctx.send(
            f"Este comando está sendo utilizado por outro membro no momento, aguarde um pouco {ctx.author.mention}.")



@client.command()
async def procurado(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    wanted = Image.open("wanted.jpg")

    asset = user.avatar_url_as(size= 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((250,250))

    wanted.paste(pfp, (110,240))    #primeiro: quanto menos, mais pra esquerda

    wanted.save("profile.jpg")

    await ctx.send(file= discord.File("profile.jpg"))

def nomeDoInvocador(x):
    return x

@client.command()
async def lol(ctx, x):
    resposta = nomeDoInvocador(x)
    json = requests.get(
        f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{resposta}?api_key=RGAPI-0e78e7af-9011-4444-9a3d-5d690040bbd7').text
    json = json[1:]
    json = json[:-1]
    for obj in json.split('{"name":'):
        pVirgula = obj.find(',')
        if pVirgula == -1: continue

        dict = {"name": obj[:pVirgula]}

        lToken = ''
        for token in obj[pVirgula:].split(','):
            arr = token.split(':')
            if len(arr) < 2:
                if len(arr[0].strip()) > 0:
                    dict[lToken] = dict[lToken] + ", " + arr[0]
                continue

            lToken = arr[0]
            dict[lToken] = arr[1]
        embed1 = discord.Embed(title=f"Informações do jogador: " + dict['"name"'],
                                description="Nível no LoL: " + dict['"summonerLevel"'],
                                color=0x0b77ea)
        await ctx.send(embed=embed1)

def avCustos(x: float, y: float):
    return x / y *100

def ahCustos(x: float, y: float):
    return (x / y -1)*100

@client.command()
async def av(ctx, x: float, y: float):
    await ctx.send('Insira primeiro o valor do item, e depois o valor da base de cálculo.')
    resposta = avCustos(x, y)
    await ctx.send(f'A porcentagem do AV é de: {resposta}%')

@client.command()
async def ah(ctx, x: float, y: float):
    await ctx.send('Insira primeiro o valor atual do item, e depois o valor do item no período anterior.')
    resposta = ahCustos(x, y)
    await ctx.send(f'A porcentagem do AH é de: {resposta}%')

@client.command()
async def peladona(ctx, user: discord.Member = None):
    if user == None:
        user = ctx.author
    wanted = Image.open("meme.png")

    asset = user.avatar_url_as(size= 128)
    data = BytesIO(await asset.read())
    pfp = Image.open(data)

    pfp = pfp.resize((35,35))
    pfp2 = pfp.resize((38, 38))

    wanted.paste(pfp, (35,230))    #primeiro: quanto menos, mais pra esquerda    segundo: quanto menos, mais pra cima
    wanted.paste(pfp2, (160, 230))

    wanted.save("meme2.png")

    await ctx.send(file= discord.File("meme2.png"))

@client.command()
async def roladas(ctx, member: discord.Member):
    rola = randint(0,100)
    if rola == 0:
        embed = discord.Embed(title=f"Quantas roladas o {member.display_name} já ganhou?",
                              description=f"{member.mention} É o cara mais hétero que já vi! Nunca ganhou uma rolada na cara!",
                              color=0x0b77ea)
        await ctx.send(embed=embed)
    else:
        embed2 = discord.Embed(title=f"Quantas roladas o {member.display_name} já ganhou?",
                              description=f"O viado do {member.mention} ganhou **{rola}** roladas na cara!",
                              color=0x0b77ea)
        await ctx.send(embed=embed2)



@client.command()
@cooldown(1, 86400, BucketType.user)
async def songs(ctx):
    if ctx.channel.id == 841451082654810125:
        user = ctx.author
        await open_account(ctx.author)
        users = await get_bank_data()
        songs = random.randrange(700, 3000)
        await ctx.send(f'Você conseguiu **{songs}** Songs hoje! Volte amanhã para coletar mais.')
        users[str(user.id)]["carteira"] += songs
        with open("bank.json", "w") as f:
            json.dump(users, f)
    else:
        await ctx.send(f'Você não pode usar comandos aqui, {ctx.author.mention}!')

@client.command(aliases=['banco'])
async def conta(ctx):
    if ctx.channel.id == 841451082654810125:
        user = ctx.author
        await open_account(ctx.author)
        users = await get_bank_data()

        walletAmount = users[str(user.id)]["carteira"]

        em = discord.Embed(title=f"Quantidade de Songs de {ctx.author.name} ", color=discord.Color.green())
        em.add_field(name=":musical_note:  Songs: ", value=walletAmount)
        await ctx.send(embed=em)
    else:
        await ctx.send(f'Você não pode usar comandos aqui, {ctx.author.mention}!')

@client.command()
async def doar(ctx):
    if ctx.channel.id == 841451082654810125:
        user = ctx.author
        await open_account(ctx.author)
        users = await get_bank_data()
        dinheiro = users[str(user.id)]["carteira"]
        await ctx.send(f'Você doou sua fortuna de {dinheiro},00 R$ com sucesso!')
        users[str(user.id)]["carteira"] -= dinheiro
        with open("bank.json", "w") as f:
            json.dump(users, f)
    else:
        await ctx.send(f'Você não pode usar comandos aqui, {ctx.author.mention}!')

async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["carteira"] = 0
    with open("bank.json", "w") as f:
        json.dump(users, f)
    return True

async def get_bank_data():
    with open("bank.json", "r") as f:
        users = json.load(f)
    return users

async def update_bank(user, change=0, mode="carteira"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("bank.json", "w") as f:
        json.dump(users, f)
    bal = [users[str(user.id)]["carteira"]]
    return bal






client.run('ODI2NDk0NDk5MDgwNjM0Mzc5.YGNS_A.EmOloLMr48jKtLKOp2tcQyN5t6g')
