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
async def punir(ctx, member: discord.Member, *, reason=None):
    user = member
    await open_account(member)
    users = await get_bank_data()
    punicoes = users[str(user.id)]["punicoes"]
    users[str(user.id)]["punicoes"] += 1
    with open("bank.json", "w") as f:
        json.dump(users, f)
    if punicoes > 1:
        await member.kick(reason=reason)
        await ctx.send(f'{member.mention} foi expulso(a) por ter levado mais de 2 avisos.\n')
    else:
        punLen = users[str(user.id)]["punicoes"]
        await ctx.send(f'Punição adicionada com sucesso ao usuário {member.mention}. O mesmo atualmente está com {punLen} avisos!   ')


async def open_account(user):
    users = await get_bank_data()
    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["punicoes"] = 0
    with open("bank.json", "w") as f:
        json.dump(users, f)
    return True

async def get_bank_data():
    with open("bank.json", "r") as f:
        users = json.load(f)
    return users


async def update_bank(user, change=0, mode="punicoes"):
    users = await get_bank_data()
    users[str(user.id)][mode] += change
    with open("bank.json", "w") as f:
        json.dump(users, f)
    bal = [users[str(user.id)]["punicoes"]]
    return bal

client.run('seu token aqui')
