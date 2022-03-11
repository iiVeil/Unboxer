from tkinter import N
import discord
from discord.ext import tasks, commands
from pymongo import MongoClient
import random
import datetime
import ast
import asyncio
from bson.objectid import ObjectId
import string
import time
import json
import math
import discord
import logging
import traceback


logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
"""
TODO: 
Mass Case Opening

"""

client = commands.Bot(command_prefix=";",
                      activity=discord.Game(f"(;) 1.0.1 | iiVeil#0001"))
client.remove_command("help")
dataclient = MongoClient()
start_time = time.time()
db = dataclient["Unboxer"]


client.casesP = {
    "Operation Wildfire Case": 0.35,
    "Operation Hydra Case": 10.86,
    "Spectrum Case": 0.75,
    "Operation Bravo Case": 39,
    "eSports 2013 Case": 30.75,
    "eSports 2014 Summer Case": 3.52,
    "eSports 2013 Winter Case": 4.40,
    "CS:GO Weapon Case 2": 7.74,
    "CS:GO Weapon Case 3": 3.88,
    "CS:GO Weapon Case": 49.45,
    "Falchion Case": 0.26,
    "Chroma 2 Case": 0.50,
    "Operation Breakout Weapon Case": 2.43,
    "Huntsman Weapon Case": 3.88,
    "Winter Offensive Weapon Case": 3.96,
    "Operation Vanguard Weapon Case": 0.77,
    "Revolver Case": 0.16,
    "Chroma Case": 0.82,
    "Shadow Case": 0.25,
    "Chroma 3 Case": 0.28,
    "Gamma Case": 0.54,
    "Gamma 2 Case": 0.58,
    "Shattered Web Case": 1.22,
    "CS20 Case": 0.15,
    "Glove Case": 2.22,
    "Danger Zone Case": 0.07,
    "Horizon Case": 0.12,
    "Spectrum 2 Case": 0.40,
    "Clutch Case": 0.16,
    "Operation Broken Fang Case": 0.81,
    "Snakebite Case": 0.10,
    "Dreams & Nightmares Case": 1.29,
    "Operation Riptide Case": 0.59,
    "Fracture Case": 0.07,
    "Operation Phoenix Weapon Case": 0.99,
    "Prisma Case": 0.08,
    "Prisma 2 Case": 0.06
}

client.drop_chance = [["special", 0.5], ["red", 1.5],
                      ["pink", 8], ["purple", 45], ["blue", 100]]
client.open_markets = []
client.market = []
client.opening = []
client.money_generated = 0
client.cases = json.load(open("cases.json", "r"))
client.knives = json.load(open("knives.json", "r"))
client.weapons = json.load(open("weapons.json", "r"))
client.trading = []
client.floats = {
    "Battle Scarred": .68,
    "Well Worn": .39,
    "Field Tested": .18,
    "Minimal Wear": .07,
    "Factory New": 0
}
client.emoji = {
    "colors": {
        "special": "<:gold:947713920158810112>",
        "red": "<:red:947713920196567081>",
        "pink": "<:pink:947713919911362594>",
        "purple": "<:purple:947713920133644298>",
        "blue": "<:blue:947713920267870339>",
        "gray": "<:gray:947714215609765968>"
    },
    "cases": {
        "Operation Wildfire Case": "<:operationwildfire:947712972325793843>",
        "Operation Hydra Case": "<:operationhydra:947712972581658624>",
        "Spectrum Case": "<:spectrum:947712972346777673>",
        "Operation Bravo Case": "<:operationbravo:947712972015411241>",
        "eSports 2013 Case": "<:esports2013:947712971973460028>",
        "eSports 2014 Summer Case": "<:esports2014:947712971285626930>",
        "eSports 2013 Winter Case": "<:esports2013winter:947712971038154832>",
        "CS:GO Weapon Case 2": "<:weaponcase2:947712971486937118>",
        "CS:GO Weapon Case 3": "<:weaponcase3:947712968131506236>",
        "CS:GO Weapon Case": "<:weaponcase:947712967892422686>",
        "Falchion Case": "<:falchion:947712972430643281>",
        "Chroma 2 Case": "<:chroma2:947712972397113399>",
        "Operation Breakout Weapon Case": "<:operationbreakout:947712971507916881>",
        "Huntsman Weapon Case": "<:huntsman:947712972443254824>",
        "Winter Offensive Weapon Case": "<:winteroffensive:947712972552294400>",
        "Operation Vanguard Weapon Case": "<:vanguard:947716097669476412>",
        "Revolver Case": "<:revolver:947712972350959657>",
        "Chroma Case": "<:chroma:947712972652937296>",
        "Shadow Case": "<:shadow:947712972564877352>",
        "Chroma 3 Case": "<:chroma3:947712972720074803>",
        "Gamma Case": "<:gamma:947716534074212362>",
        "Gamma 2 Case": "<:gamma2:692096260043440228>",
        "Shattered Web Case": "<:shatteredweb:947712972279648277>",
        "CS20 Case": "<:cs20:947712972732657705>",
        "Glove Case": "<:glove:947712972652949614>",
        "Danger Zone Case": "<:dangerzone:947712971864440864>",
        "Horizon Case": "<:horizon:947712972824916018>",
        "Spectrum 2 Case": "<:spectrum2:947712972363554818>",
        "Clutch Case": "<:clutch:947712972703297536>",
        "Operation Broken Fang Case": "<:operationbrokenfang:947712971503710228>",
        "Snakebite Case": "<:snakebite:947712972606816276>",
        "Dreams & Nightmares Case": "<:dreamsandnightmares:947712972560662579>",
        "Operation Riptide Case": "<:operationriptide:947712972451610655>",
        "Fracture Case": "<:fracture:947712972657164389>",
        "Operation Phoenix Weapon Case": "<:operationphoenix:947712972426469467>",
        "Prisma Case": "<:prisma:947718025262563340>",
        "Prisma 2 Case": "<:prisma2:947712971730219039>"
    }
}
client.loops_ran = 1


@tasks.loop(seconds=60.0)
async def run_money_loop():
    print(f"Loop Count: {client.loops_ran}")
    for guild in client.guilds:
        for voice_channel in guild.voice_channels:
            for user in voice_channel.members:
                if db.stats.find_one({"user": user.id}) != None:
                    stats = db.stats.find_one({"user": user.id})
                    if stats["pendingMoney"] < stats["maxPendingMoney"]:
                        if (user.voice.self_mute == False and user.voice.mute == False):
                            client.money_generated += stats["moneyPer10seconds"]*6
                            stats["pendingMoney"] += stats["moneyPer10seconds"]*6
                            db.stats.replace_one({"user": user.id}, stats)
                            print(f"Added money to {user.name}")
    client.loops_ran += 1


@run_money_loop.error
async def loop_error(self, error):
    formatted = "".join(
        traceback.format_exception(type(error), error, error.__traceback__)
    )
    print(formatted)


async def user_data(ctx):
    if db.userdata.find_one({"user": ctx.author.id}) == None:
        start = time.time()
        await ctx.author.send("Hey! You arent registered in our system, let us set up your data before you do anything!\n\nThis is a **ONE TIME** action, you should never see this again.")
        dataStats = {
            "user": ctx.author.id,
            # SEPERATOR [=]
            # [0] = Weapon Name
            # [1] = Rarity
            # [2] = Float
            "lastMessage": 0,
            "moneyPer10seconds": 0.01,
            "massUnlocked": False,
            "casesOpened": 0,
            "maxPendingMoney": 1.00,
            "pendingMoney": 0.0,
            "currentMoney": 0,
            "highestOverall": 0,
            "totalMoneySpent": 0,
            "Specials": 0,
            "Knives": 0,
            "Gloves": 0,
            "Reds": 0,
            "Pinks": 0,
            "Purples": 0,
            "Blues": 0,
            "Grays": 0
        }
        dataInv = {
            "user": ctx.author.id,
            "items": [],
            "universalKeys": 0,
            "cases": {
                # [KEYS, CASES]
                "Operation Wildfire Case": [0, 0],
                "Operation Hydra Case": [0, 0],
                "Spectrum Case": [0, 0],
                "Operation Bravo Case": [0, 0],
                "eSports 2013 Case": [0, 0],
                "eSports 2014 Summer Case": [0, 0],
                "eSports 2013 Winter Case": [0, 0],
                "CS:GO Weapon Case 2": [0, 0],
                "CS:GO Weapon Case 3": [0, 0],
                "CS:GO Weapon Case": [0, 0],
                "Falchion Case": [0, 0],
                "Chroma 2 Case": [0, 0],
                "Operation Breakout Weapon Case": [0, 0],
                "Huntsman Weapon Case": [0, 0],
                "Winter Offensive Weapon Case": [0, 0],
                "Operation Vanguard Weapon Case": [0, 0],
                "Revolver Case": [0, 0],
                "Chroma Case": [0, 0],
                "Shadow Case": [0, 0],
                "Chroma 3 Case": [0, 0],
                "Gamma Case": [0, 0],
                "Gamma 2 Case": [0, 0],
                "Shattered Web Case": [0, 0],
                "CS20 Case": [0, 0],
                "Glove Case": [0, 0],
                "Danger Zone Case": [0, 0],
                "Horizon Case": [0, 0],
                "Spectrum 2 Case": [0, 0],
                "Clutch Case": [0, 0],
                "Operation Broken Fang Case": [0, 0],
                "Snakebite Case": [0, 0],
                "Dreams & Nightmares Case": [0, 0],
                "Operation Riptide Case": [0, 0],
                "Fracture Case": [0, 0],
                "Operation Phoenix Weapon Case": [0, 0],
                "Prisma Case": [0, 0],
                "Prisma 2 Case": [0, 0]
            }
        }
        db.userdata.insert_one({"user": ctx.author.id})
        db.stats.insert_one(dataStats)
        db.inventory.insert_one(dataInv)
        db.dailies.insert_one(
            {"user": ctx.author.id, "claimed": False, "claimedAt": None})
        end = time.time()
        difference = int(round(end - start))
        text = str(datetime.timedelta(seconds=difference))
        await ctx.author.send(f"We finished up, Have fun opening cases! [Completed in {text}]")
    else:
        return

# []           Events             [] #


@client.event
async def on_ready():
    run_money_loop.start()
    print("Setup!")


@client.event
async def on_message(message):
    if db.banned.find_one({"id": message.author.id}) == None and message.author.bot == False and message.channel.type != discord.ChannelType.private:
        ctx = await client.get_context(message)
        if db.userdata.find_one({"user": message.author.id}) != None:
            if not ctx.valid:
                data = db.stats.find_one({"user": message.author.id})
                data["lastMessage"] = time.time()
                db.stats.replace_one({"user": message.author.id}, data)
        if ctx.valid:
            for item in client.open_markets:
                if item[1] == message.author.id:
                    m = await ctx.send(f"Close your current market session with the \"❌\" emoji! <@{message.author.id}>")
                    await asyncio.sleep(2)
                    await message.delete()
                    await m.delete()
                    return
#            if message.author.id == 300307874725494784:
            await client.process_commands(message)
#            else:
#                await ctx.send("Bot is in maintenance mode.")
    else:
        return

# []           Commands             [] #


@client.command(name="trade")
async def _trade_request_(ctx, a: discord.User = None):
    await user_data(ctx)
    try:
        if a == None:
            await ctx.send(embed=(await embed_gen("Invalid Arguments", "You need to specify a user, mention them! `;trade @someone`", "red")))
            return
        if a == ctx.author:
            await ctx.send(embed=(await embed_gen("Invalid Arguments", "You can't trade with yourself!", "red")))
            return
        send, receive = ctx.author, a
        m = await ctx.send(embed=(await embed_gen("Trade Request", f"{send.mention} wants to trade with {receive.mention}!\nReact to respond!", "orange")))

        def check(reaction, user):
            return user == receive and reaction.message.id == m.id
        await m.add_reaction('❌')
        await m.add_reaction('✅')
        try:
            reaction, user = await client.wait_for("reaction_add", check=check, timeout=30)
        except asyncio.TimeoutError:
            await m.edit(embed=(await embed_gen("Trade Declined", f"Trade request timed out.", "red")))
            return
        if str(reaction) == "❌":
            await m.edit(embed=(await embed_gen("Trade Declined", f"{receive.mention} has declined.", "orange")))
            return
        elif str(reaction) == "✅":
            for l in client.trading:
                if user.id in l or ctx.author.id in l:
                    await ctx.send("Someone is already in a trade!")
                    return
            client.trading.append([user.id, ctx.author.id])
            trade = [user.id, ctx.author.id]
            await m.remove_reaction("✅", user)
            offering = [[], []]
            cash = [0, 0]
            accepted = []
            while True:
                if send in accepted and receive in accepted:
                    data_send = db.inventory.find_one({"user": send.id})
                    data_send_stats = db.stats.find_one({"user": send.id})
                    data_receive = db.inventory.find_one({"user": receive.id})
                    data_receive_stats = db.stats.find_one(
                        {"user": receive.id})
                    data_send_stats["currentMoney"] -= cash[0]
                    data_receive_stats["currentMoney"] += cash[0]
                    data_receive_stats["currentMoney"] -= cash[1]
                    data_send_stats["currentMoney"] += cash[1]
                    for user in offering:
                        for item in user:
                            if offering.index(user) == 0:
                                # send -> receive
                                data_send['items'].remove(item)
                                data_receive['items'].append(item)
                                data = db.uuids.find_one(
                                    {"uuid": item.split('[=]')[3]})
                                data['owner'] = receive.id
                                db.uuids.replace_one(
                                    {"uuid": item.split('[=]')[3]}, data)
                            else:
                                # receive -> send
                                data_send['items'].append(item)
                                data_receive['items'].remove(item)
                                data = db.uuids.find_one(
                                    {"uuid": item.split('[=]')[3]})
                                data['owner'] = send.id
                                db.uuids.replace_one(
                                    {"uuid": item.split('[=]')[3]}, data)
                    db.inventory.replace_one({"user": send.id}, data_send)
                    db.inventory.replace_one(
                        {"user": receive.id}, data_receive)
                    db.stats.replace_one({"user": send.id}, data_send_stats)
                    db.stats.replace_one(
                        {"user": receive.id}, data_receive_stats)
                    await m.edit(content="Trade accepted.")
                    client.trading.remove(trade)
                    return
                messages = [
                    f"Cash Offering: **${cash[0]}**\n", f"Cash Offering: **${cash[1]}**\n"]
                for user in offering:
                    for item in user:
                        messages[offering.index(
                            user)] += f" {client.emoji['colors'][item.split('[=]')[1]]} **{item.split('[=]')[0]}** :: **{discord.utils.escape_markdown(item.split('[=]')[3])}**\n"
                embed = await embed_gen("Trade", f"", "green")
                embed.add_field(name=f"{send} is offering: ", inline=True,
                                value=None if messages[0] == "" else messages[0])
                embed.add_field(name=f"{receive} is offering: ", inline=True,
                                value=None if messages[1] == "" else messages[1])
                await m.edit(embed=embed)

                def check1(reaction, user):
                    return user == send or user == receive and reaction.message.id == m.id

                def check3(m):
                    return m.author == send or m.author == receive
                try:
                    done, pending = await asyncio.wait([client.wait_for('message', check=check3), client.wait_for('reaction_add', check=check1), client.wait_for('reaction_remove', check=check1)], timeout=120, return_when=asyncio.FIRST_COMPLETED)
                    finished = done.pop().result()
                    for future in pending:
                        future.cancel()
                except asyncio.TimeoutError:
                    await m.edit(content="**No action has been sent in the last 2 minutes this trade session has timed out.**")
                    client.trading.remove(trade)
                    return
                if isinstance(finished, discord.Message):
                    message = finished
                    stats = db.stats.find_one({"user": message.author.id})
                    if message.content.startswith("$"):
                        if stats["currentMoney"] >= float(message.content.strip("$")):
                            if message.author == send:
                                cash[0] += float(message.content.strip("$"))
                            elif message.author == receive:
                                cash[1] += float(message.content.strip("$"))
                    data = db.uuids.find_one({"uuid": message.content.strip()})
                    if data != None:
                        if data['owner'] == message.author.id:
                            if message.author == send:
                                if data["weapon"] not in offering[0]:
                                    offering[0].append(data['weapon'])
                                else:
                                    offering[0].remove(data['weapon'])
                            elif message.author == receive:
                                if data["weapon"] not in offering[1]:
                                    offering[1].append(data['weapon'])
                                else:
                                    offering[1].remove(data['weapon'])
                            await message.delete()
                        else:
                            await ctx.send(f"{message.author.mention} you do not own this item!", delete_after=3)
                            continue
                elif isinstance(finished[0], discord.Reaction):
                    reaction, user = finished[0], finished[1]
                    if str(reaction) == "❌":
                        await m.edit(content="**Ended.**")
                        for l in client.trading:
                            if user.id in l or ctx.author.id in l:
                                client.trading.remove(l)
                                return
                        return
                    if str(reaction) == "✅":
                        async for u in reaction.users():
                            if user == u:
                                accepted.append(user)
                                break
                            else:
                                if user in accepted:
                                    accepted.remove(user)
    except Exception:
        for l in client.trading:
            if user.id in l or ctx.author.id in l:
                client.trading.remove(l)
                return


@client.command(name="claim", aliases=["cash"])
async def _claim_pending_money(ctx):
    await user_data(ctx)
    data = db.stats.find_one({"user": ctx.author.id})
    if data["pendingMoney"] > 0.0:
        embed = await embed_gen("Pending Money", f"You have claimed {round(data['pendingMoney'], 2)} dollars.\nNew Balance: ${round(data['currentMoney'] + round(data['pendingMoney'], 2),2)}", "blue")
        data["currentMoney"] += round(data['pendingMoney'], 2)
        data["pendingMoney"] = 0.0
        db.stats.replace_one({"user": ctx.author.id}, data)
        await ctx.send(embed=embed)
    else:
        embed = await embed_gen("Pending Money", f"You can't claim yet!", "red")
        await ctx.send(embed=embed)


@client.command(name="market", aliases=["marketplace"])
async def _open_marketplace_(ctx, *, args="help"):
    await user_data(ctx)
    try:
        if [ctx.channel.id, ctx.author.id] not in client.open_markets:
            client.open_markets.append([ctx.channel.id, ctx.author.id])
        else:
            await ctx.send("A market is already open in this channel. Choose a different channel if you would like to search.")
            return
        if args == "help":
            embed = await embed_gen("Market Info", "Hey! You're missing some arguments, `;market keywords`\n\nFor some clarity, our search system uses keywords, for example you can say `;market awp m4 dragon` and it will return m4a4 dragon kings, and awp dragon lores!`", "blue")
            await ctx.send(embed=embed)
            if [ctx.channel.id, ctx.author.id] in client.open_markets:
                client.open_markets.remove([ctx.channel.id, ctx.author.id])
            return
        market_data = db.market.find({})
        paginator = commands.Paginator(prefix="", suffix="")
        words = {}
        for word in args.split(" "):
            words[word] = 0
        found = []
        for listing in market_data:
            for word in args.split(" "):
                if word.lower() in listing["skin"].split("[=]")[0].lower():
                    found.append([listing, listing["skin"].split("[=]")[0]])
                    words[word] += 1
                    break
        if len(found) == 0:
            await ctx.send("No results found for your search.")
            if ctx.channel.id in client.open_markets:
                client.open_markets.remove(ctx.channel.id)
            return

        def sortByAlpha(val):
            return val[1]

        def sortByTime(val):
            return val[0]['postedAt']

        def sortByPrice(val):
            return val[0]['price']

        def createTimeStamp(epoch):
            postTime = datetime.datetime.utcfromtimestamp(epoch)
            h = str(postTime.hour)
            m = str(postTime.minute)
            s = str(postTime.second)
            if len(str(postTime.hour)) < 2:
                h = f"0{h}"
            if len(str(postTime.minute)) < 2:
                m = f"0{m}"
            if len(str(postTime.second)) < 2:
                s = f"0{s}"
            return f"{postTime.month}/{postTime.day}/{postTime.year} "
        found.sort(key=sortByAlpha)
        paginator = commands.Paginator(prefix="", suffix="")
        index = 0
        for item in found:
            postTime = createTimeStamp(item[0]['postedAt'])
            paginator.add_line(
                f"{postTime} :: {client.emoji['colors'][item[0]['skin'].split('[=]')[1]]} **{item[1]}** :: {discord.utils.escape_markdown(item[0]['skin'].split('[=]')[3])} | **${item[0]['price']}**")
        embed = await embed_gen(f"Market | `{args}`", f"{paginator.pages[index]}", "blue")
        embed.set_footer(text=f'{index+1}/{len(paginator.pages)}')
        m = await ctx.send(embed=embed)
        await m.add_reaction('◀')
        await m.add_reaction('▶')
        await m.add_reaction('🔤')
        await m.add_reaction('💰')
        await m.add_reaction('⏲️')
        await m.add_reaction('↩')
        await m.add_reaction('❌')
        while True:
            reverse = False
            m = await ctx.channel.fetch_message(m.id)
            for r in m.reactions:
                if str(r) == "↩":
                    async for u in r.users():
                        if u == ctx.author:
                            reverse = True
                            break
            embed = await embed_gen(f"Market | `{args}`{' | ↩' if reverse else ''}", f"{paginator.pages[index]}", "blue")
            embed.set_footer(text=f'{index+1}/{len(paginator.pages)}')
            await m.edit(embed=embed)

            def check1(reaction, user):
                return user == ctx.author and reaction.message.id == m.id

            def check2(m):
                return m.author == ctx.message.author
            try:
                done, pending = await asyncio.wait([client.wait_for('message', check=check2), client.wait_for('reaction_add', check=check1)], timeout=120, return_when=asyncio.FIRST_COMPLETED)
                finished = done.pop().result()
                for future in pending:
                    future.cancel()
            except asyncio.TimeoutError:
                if ctx.channel.id in client.open_markets:
                    client.open_markets.remove(ctx.channel.id)
                return
            if isinstance(finished, discord.Message):
                message = finished
                itemB = []
                market_data = db.market.find({})
                for a in market_data:
                    if a['skin'].split('[=]')[3] == message.content.strip():
                        itemB = [message.content.strip(), a]
                        break
                    else:
                        itemB = ["Not found"]
                if itemB[0] == "Not found":
                    await ctx.send("Item is not on the market.", delete_after=4)
                    await message.delete()
                    continue
                if itemB[1]['user'] == ctx.author.id:
                    await ctx.send("You can't buy your own listing! You can check them with `;post list`", delete_after=4)
                    continue
                gun = db.uuids.find_one({"uuid": message.content.strip()})
                wearN = None
                for wear in client.floats:
                    if float(gun['weapon'].split('[=]')[2]) >= client.floats[wear]:
                        wearN = wear
                        break
                embed = await embed_gen("Confirmation Y/N", f"""`Heres some info on the item your about to buy.`\n**Skin:** {gun['weapon'].split('[=]')[0]}\n**Rarity:** {client.emoji['colors'][gun['weapon'].split('[=]')[1]]}\n**Original Owner:** {client.get_user(gun['user'])} ({gun['user']})\n**Current Owner:** {client.get_user(gun['owner'])} ({gun['owner']})\n**UUID:** {message.content.strip()}\n**Unboxed On:** {gun['time']}\n**Wear:** {gun['weapon'].split('[=]')[2]} ({wearN})""", "orange")
                await ctx.send(embed=embed)

                def check(m):
                    return m.author == ctx.author and m.channel == ctx.channel
                try:
                    resp = await client.wait_for("message", check=check, timeout=120)
                    if resp.content.lower() == "yes" or resp.content.lower() == "y":
                        await resp.delete()
                        data = db.stats.find_one({"user": ctx.author.id})
                        dataSeller = db.stats.find_one(
                            {"user": itemB[1]['user']})
                        if data["currentMoney"] >= itemB[1]['price']:
                            data["currentMoney"] -= itemB[1]['price']
                            dataSeller["currentMoney"] += itemB[1]['price']
                            data["totalMoneySpent"] += itemB[1]['price']
                            db.stats.replace_one({"user": ctx.author.id}, data)
                            db.stats.replace_one(
                                {"user": itemB[1]['user']}, dataSeller)
                            data = db.inventory.find_one(
                                {"user": ctx.author.id})
                            transfer = itemB[1]
                            data['items'].append(transfer['skin'])
                            db.inventory.replace_one(
                                {"user": ctx.author.id}, data)
                            data = db.uuids.find_one(
                                {"uuid": message.content.strip()})
                            data['owner'] = ctx.author.id
                            db.uuids.replace_one(
                                {"uuid": message.content.strip()}, data)
                            db.market.delete_one({"skin": transfer['skin']})
                            await ctx.send(embed=(await embed_gen("Bought!", f"You just bought a **{transfer['skin'].split('[=]')[0]}** for **${item[1]['price']}**\n`;item {transfer['skin'].split('[=]')[3]}` for more information!", "green")))
                            if [ctx.channel.id, ctx.author.id] in client.open_markets:
                                client.open_markets.remove(
                                    [ctx.channel.id, ctx.author.id])
                    else:
                        await resp.delete()
                        embed = await embed_gen("Operation Cancelled.", f"Nothing will change.", "red")
                        await m.edit(embed=embed)
                        if [ctx.channel.id, ctx.author.id] in client.open_markets:
                            client.open_markets.remove(
                                [ctx.channel.id, ctx.author.id])
                        return
                except asyncio.TimeoutError:
                    embed = await embed_gen("Operation Cancelled.", f"Nothing will change.", "red")
                    await m.edit(embed=embed)
                    if [ctx.channel.id, ctx.author.id] in client.open_markets:
                        client.open_markets.remove(
                            [ctx.channel.id, ctx.author.id])
                    return
                else:
                    await ctx.send("You don't have enough money to afford this!", delete_after=4)
                    continue
            elif isinstance(finished[0], discord.Reaction):
                m = await ctx.channel.fetch_message(m.id)
                for r in m.reactions:
                    if str(r) == "↩":
                        async for u in r.users():
                            if u == ctx.author:
                                reverse = True
                                break
                            else:
                                reverse = False
                reaction, user = finished[0], finished[1]
                if str(reaction) == '▶':
                    index += 1
                    if index > len(paginator.pages)-1:
                        index -= 1
                    await m.remove_reaction('▶', user)
                elif str(reaction) == '◀':
                    index -= 1
                    if index < 0:
                        index = 0
                    await m.remove_reaction('◀', user)
                elif str(reaction) == '⏲️':
                    paginator = commands.Paginator(prefix="", suffix="")
                    if reverse:
                        found.sort(key=sortByTime)
                    else:
                        found.sort(key=sortByTime, reverse=True)
                    for item in found:
                        postTime = createTimeStamp(item[0]['postedAt'])
                        paginator.add_line(
                            f"{postTime} :: {client.emoji['colors'][item[0]['skin'].split('[=]')[1]]} **{item[1]}** :: {item[0]['skin'].split('[=]')[3]} | **${item[0]['price']}**")
                    await m.remove_reaction('⏲️', user)
                elif str(reaction) == '💰':
                    paginator = commands.Paginator(prefix="", suffix="")
                    if reverse:
                        found.sort(key=sortByPrice, reverse=True)
                    else:
                        found.sort(key=sortByPrice)
                    for item in found:
                        postTime = createTimeStamp(item[0]['postedAt'])
                        paginator.add_line(
                            f"{postTime} :: {client.emoji['colors'][item[0]['skin'].split('[=]')[1]]} **{item[1]}** :: {item[0]['skin'].split('[=]')[3]} | **${item[0]['price']}**")
                    await m.remove_reaction('💰', user)
                elif str(reaction) == '🔤':
                    paginator = commands.Paginator(prefix="", suffix="")
                    if reverse:
                        found.sort(key=sortByAlpha, reverse=True)
                    else:
                        found.sort(key=sortByAlpha)
                    for item in found:
                        postTime = createTimeStamp(item[0]['postedAt'])
                        paginator.add_line(
                            f"{postTime} :: {client.emoji['colors'][item[0]['skin'].split('[=]')[1]]} **{item[1]}** :: {item[0]['skin'].split('[=]')[3]} | **${item[0]['price']}**")
                    await m.remove_reaction('🔤', user)
                elif str(reaction) == '❌':
                    if [ctx.channel.id, ctx.author.id] in client.open_markets:
                        client.open_markets.remove(
                            [ctx.channel.id, ctx.author.id])
                    return
    except Exception as e:
        if [ctx.channel.id, ctx.author.id] in client.open_markets:
            client.open_markets.remove([ctx.channel.id, ctx.author.id])
        print(e)
        return


@client.command(name="post")
async def _post_to_market_(ctx, id=None, price=None):
    await user_data(ctx)
    if id == None:
        embed = await embed_gen("Invalid Arguments!", "`;post id price` -> Post a skin on the market\n`;post list` -> View all your skin posts.", "red")
        await ctx.send(embed=embed)
        return
    if id == "list":
        posts = db.market.find({"user": ctx.author.id})
        message = ""
        wearN = None
        for post in posts:
            for wear in client.floats:
                if float(post['skin'].split('[=]')[2]) >= client.floats[wear]:
                    wearN = wear
                    break
            message += f"{post['skin'].split('[=]')[0]} : {wearN}\n> Posted on {datetime.datetime.utcfromtimestamp(post['postedAt'])}\n > {time.strftime('%Hh %Mm %Ss ago', time.gmtime(post['postedAt']))}"
        embed = await embed_gen("Market Listings", message, "green")
        return
    if len(dict(db.market.find({"user": ctx.author.id}))) >= 5:
        await ctx.send("You can't have more than 5 active market posts!")
        return
    if price == None:
        embed = await embed_gen("Invalid Arguments!", "`You're missing a price!` ;post id price`", "red")
        await ctx.send(embed=embed)
        return
    try:
        price = int(price.replace(",", ""))
    except ValueError:
        price = float(price.replace(",", ""))
    if price <= 0:
        await ctx.send("You can't put an item up for 0 dollars!")
        return
    selling = False
    unboxed = True
    for item in db.inventory.find_one({"user": ctx.author.id})["items"]:
        if item.split("[=]")[3] == id:
            if db.uuids.find_one({"uuid": id}) != None:
                selling = item
            else:
                unboxed = False
    if not unboxed:
        embed = await embed_gen("You can't post this weapon", "This weapon is NOT registered in the unbox database.", "red")
        await ctx.send(embed=embed)
        return
    if not selling:
        embed = await embed_gen("No weapon found.", "Theres no weapon with this ID in your inventory!", "red")
        await ctx.send(embed=embed)
        return
    wearN = None
    for wear in client.floats:
        if float(selling.split('[=]')[2]) >= client.floats[wear]:
            wearN = wear
            break
    embed = await embed_gen("Confirmation Y/N", f"Are you sure you would like to post your `{selling.split('[=]')[0]}` for $`{price:,}`?\n\n**Item Data:**\n**Wear:** {selling.split('[=]')[2]} ({wearN})\n**Rarity:** {client.emoji['colors'][selling.split('[=]')[1]]}", "orange")
    m = await ctx.send(embed=embed)

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
    try:
        resp = await client.wait_for("message", check=check, timeout=120)
        if resp.content.lower() == "yes" or resp.content.lower() == "y":
            await resp.delete()
            userInv = db.inventory.find_one({"user": ctx.author.id})
            for item in userInv["items"]:
                if selling.split("[=]")[3] == item.split("[=]")[3]:
                    userInv["items"].remove(item)
            db.inventory.replace_one({"user": ctx.author.id}, userInv)
            db.market.insert_one(
                {"user": ctx.author.id, "skin": selling, "postedAt": time.time(), "price": price})
            embed = await embed_gen("Successfully posted!", f"We successfully posted your `{selling.split('[=]')[0]}` @ ${price:,}", "green")
            await m.edit(embed=embed)
            return
        else:
            await resp.delete()
            embed = await embed_gen("Operation Cancelled.", f"Your item will NOT be posted.", "red")
            await m.edit(embed=embed)
    except asyncio.TimeoutError:
        embed = await embed_gen("Operation Cancelled.", f"Your item will NOT be posted.", "red")
        await m.edit(embed=embed)


@client.command(name="item")
async def _gun_info_(ctx, id=None):
    await user_data(ctx)
    if db.uuids.find_one({"uuid": id}) == None:
        embed = await embed_gen("No weapon found.", "This weapon was not found in our unbox database.", "red")
        await ctx.send(embed=embed)
        return
    gun = db.uuids.find_one({"uuid": id})
    wearN = None
    for wear in client.floats:
        if float(gun['weapon'].split('[=]')[2]) >= client.floats[wear]:
            wearN = wear
            break
    info = calculate_price(id)
    embed = await embed_gen("Gun info", f"**Skin:** {gun['weapon'].split('[=]')[0]}\n**Rarity:** {client.emoji['colors'][gun['weapon'].split('[=]')[1]]}\n**Original Owner:** {client.get_user(gun['user'])} ({gun['user']})\n**Current Owner:** {client.get_user(gun['owner']) if gun['owner'] != None else 'Sold!'} ({gun['owner']})\n**UUID:** {discord.utils.escape_markdown(id)}\n**Unboxed On:** {gun['time']}\n**Wear:** {gun['weapon'].split('[=]')[2]} ({wearN})\n**Roll:** {gun['roll']}\n**Appraisal:** {info[0]}", "green")
    await ctx.send(embed=embed)


@client.command(name="give")
async def _give_stuff_(ctx, type=None):
    await user_data(ctx)
    if ctx.author.id != 300307874725494784:
        embed = await embed_gen(f"Permission Denied", f"You are not an admin, therefore not able to give yourself consumables. For any questions please refer to `iiVeil#0001`", "red")
        await ctx.author.send(embed=embed)
        return
    if type == None:
        await ctx.send("No type.")
        return
    elif type == "keys" or type == "key":
        data = db.inventory.find_one({"user": ctx.author.id})
        for case in data["cases"]:
            data["cases"][case][0] += 10
        db.inventory.replace_one({"user": ctx.author.id}, data)
    elif type == "cases" or type == "case":
        data = db.inventory.find_one({"user": ctx.author.id})
        for case in data["cases"]:
            data["cases"][case][1] += 10
        db.inventory.replace_one({"user": ctx.author.id}, data)
    elif type == "null":
        data = db.inventory.find_one({"user": ctx.author.id})
        for case in data["cases"]:
            data["cases"][case][1] = 0
            data["cases"][case][0] = 0
        db.inventory.replace_one({"user": ctx.author.id}, data)


@client.command(name="daily")
async def _claim_daily_(ctx):
    await user_data(ctx)
    now = time.time()
    data = db.dailies.find_one({"user": ctx.author.id})
    dataStats = db.stats.find_one({"user": ctx.author.id})
    dataInv = db.inventory.find_one({"user": ctx.author.id})
    rew = None
    if data["claimed"]:
        if (now - data["claimedAt"]) >= 86400:
            ran = random.randint(0, 100)
            for i, j in enumerate([["Universal Keys", 5], ["Money", 100]]):
                if ran < j[1]:
                    if j[0] == "Universal Keys":
                        dataInv["universalKeys"] += 5
                        rew = [5, "Universal Keys"]
                    elif j[0] == "Money":
                        am = random.uniform(1.00, 5.00)
                        dataStats["currentMoney"] += int(
                            (am * 100) + 0.5) / float(100)
                        rew = [int((am * 100) + 0.5) / float(100), "Money"]
                    break
            data["claimedAt"] = time.time()
            data["claimed"] = True
            db.dailies.replace_one({"user": ctx.author.id}, data)
            db.stats.replace_one({"user": ctx.author.id}, dataStats)
            db.inventory.replace_one({"user": ctx.author.id}, dataInv)
            m = ""
            if rew[1] == "Money":
                m = f"{rew[0]} dollars"
            elif rew[1] == "Universal Keys":
                m = f"{rew[0]} Universal Keys"
            ex = f'New Balance: ${round(dataStats["currentMoney"],2)}'
            embed = await embed_gen("Claimed!", f"You claimed {m}!\n{ex if 'dollars' in m else ''}", "blue")
            await ctx.send(embed=embed)
            return
        else:
            embed = await embed_gen("You already claimed today!", f"You need to wait {time.strftime('%H hours %M minutes & %S seconds', time.gmtime(abs((data['claimedAt']+86400)-now)))} until claiming again.", "red")
            await ctx.send(embed=embed)
            return
    else:
        ran = random.randint(0, 100)
        for i, j in enumerate([["Universal Keys", 5], ["Money", 100]]):
            if ran < j[1]:
                if j[0] == "Universal Keys":
                    dataInv["universalKeys"] += 1
                    rew = [1, "Universal Key"]
                elif j[0] == "Money":
                    am = random.uniform(0.00, 2.50)
                    dataStats["currentMoney"] += int(
                        (am * 100) + 0.5) / float(100)
                    rew = [int((am * 100) + 0.5) / float(100), "Money"]
                break
        data["claimedAt"] = time.time()
        data["claimed"] = True
        db.dailies.replace_one({"user": ctx.author.id}, data)
        db.stats.replace_one({"user": ctx.author.id}, dataStats)
        db.inventory.replace_one({"user": ctx.author.id}, dataInv)
        m = ""
        if rew[1] == "Money":
            m = f"{rew[0]} dollars"
        elif rew[1] == "Universal Keys":
            m = f"{rew[0]} Universal Keys"
        embed = await embed_gen("Claimed!", f"You claimed {m}!", "blue")
        await ctx.send(embed=embed)


@client.command(name="profile")
async def _open_profile_(ctx, page="stats"):
    await user_data(ctx)
    l = ["stats", "inventory"]
    if page not in l:
        page = "stats"
    dataStats = db.stats.find_one({"user": ctx.author.id})
    MENUpages = {
        "stats": [f"{client.emoji['cases']['Spectrum Case']} Total Cases Opened: {dataStats['casesOpened']}\n:clock1: Pending Money: {round(dataStats['pendingMoney'], 2)} ({round(dataStats['moneyPer10seconds'],2)}/10s)\n:moneybag: Money: {math.floor(dataStats['currentMoney']*100)/100}\n:money_with_wings: Total Money Spent: {round(dataStats['totalMoneySpent'],2)}\n {client.emoji['colors']['special']} Specials Unboxed: {dataStats['Specials']}\n     > Knives: {dataStats['Knives']}\n    > Gloves: {dataStats['Gloves']}\n {client.emoji['colors']['red']} Reds Unboxed: {dataStats['Reds']}\n {client.emoji['colors']['pink']} Pinks Unboxed: {dataStats['Pinks']}\n {client.emoji['colors']['purple']} Purples Unboxed: {dataStats['Purples']}\n {client.emoji['colors']['blue']} Blues Unboxed: {dataStats['Blues']}\n"],
        "inventory": []
    }
    reactions = ["📈", "🛄"]
    data = db.inventory.find_one({"user": ctx.author.id})
    paginator = commands.Paginator(prefix="", suffix="")
    for item in data["items"]:
        emoji = client.emoji["colors"][item.split('[=]')[1]]
        paginator.add_line(f"{emoji} {item.split('[=]')[0]}")
    MENUpages["inventory"] = paginator.pages.copy()
    embed = await embed_gen(f"Stats", f"{MENUpages['stats'][0]}", "blue")
    embed.set_footer(text=f'PAGE 1/1')
    m = await ctx.send(embed=embed)
    for reaction in reactions:
        await m.add_reaction(reaction)
    active_page = page
    index = 0
    while True:
        if active_page == "stats":
            embed = await embed_gen(f"Stats", f"{MENUpages['stats'][0]}", "blue")
            embed.set_footer(text=f'PAGE {index+1}/1 | STATS | {ctx.author}')
            await m.edit(embed=embed)
        else:
            paginator = commands.Paginator(prefix="", suffix="")
            for item in data["items"]:
                emoji = client.emoji["colors"][item.split('[=]')[1]]
                paginator.add_line(
                    f"{emoji} {item.split('[=]')[0]} :: ID: {discord.utils.escape_markdown(item.split('[=]')[3])}")
            MENUpages["inventory"] = paginator.pages.copy()
            try:
                embed = await embed_gen(f"Inventory", f"{MENUpages['inventory'][index]}", "blue")
                embed.set_footer(
                    text=f'PAGE {index+1}/{len(MENUpages["inventory"])} | INVENTORY | {ctx.author}')
            except IndexError:
                embed = await embed_gen(f"Inventory", f"No items yet!", "blue")
                embed.set_footer(
                    text=f'PAGE {index}/0 | INVENTORY | {ctx.author}')
            await m.edit(embed=embed)
            await m.add_reaction("◀")
            await m.add_reaction("▶")
            await m.add_reaction("🔡")

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == m.id
        try:
            reaction, user2 = await client.wait_for('reaction_add', timeout=120, check=check)
        except asyncio.TimeoutError:
            break
        if str(reaction) == "📈":
            active_page = "stats"
            await m.remove_reaction("◀", client.user)
            await m.remove_reaction("▶", client.user)
            await m.remove_reaction("🔡", client.user)
            await m.remove_reaction("📈", ctx.author)
            index = 0
        elif str(reaction) == "🛄":
            active_page = "inventory"
            await m.add_reaction("◀")
            await m.add_reaction("▶")
            await m.add_reaction("🔡")
            await m.remove_reaction("🛄", ctx.author)
            index = 0
        elif active_page == "inventory" and str(reaction) == "◀":
            index -= 1
            if index < 0:
                index = 0
            await m.remove_reaction("◀", ctx.author)
        elif active_page == "inventory" and str(reaction) == "▶":
            index += 1
            if index > len(MENUpages["inventory"]):
                index = len(MENUpages["inventory"])-1
            await m.remove_reaction("▶", ctx.author)
        elif active_page == "inventory" and str(reaction) == "🔡":
            def check2(m):
                return m.author == ctx.author
            m2 = await ctx.send("What page would you like to go to?")
            try:
                rep = await client.wait_for('message', timeout=120, check=check2)
            except asyncio.TimeoutError:
                return
            try:
                if int(rep.content) > 0 and int(rep.content) < len(MENUpages["inventory"]):
                    index = int(rep.content)
            except Exception:
                await ctx.send("Please input a valid page number", delete_after=3)
            await m2.delete()
            await rep.delete()
            await m.remove_reaction("🔡", ctx.author)


@client.command(name="inv", aliases=["inventory"])
async def _open_inv_(ctx):
    await _open_profile_(ctx, page="inventory")


@client.command(name="simulate")
async def _simulate_case_opening(ctx, amount=0):
    if amount > 200:
        embed = await embed_gen(f"Case Simulation", f"Do to performace reasons, you cant simulate more than 200 cases at once.", "red")
        await ctx.send(embed=embed)
        return
    if amount > 0:
        output = {
            "special": 0,
            "red": 0,
            "pink": 0,
            "purple": 0,
            "blue": 0
        }
        while amount > 0:
            num = random.uniform(0.0, 100.0)
            for y, x in enumerate([["special", 0.4], ["red", 1], ["pink", 8], ["purple", 45], ["blue", 100]]):
                if num <= x[1]:
                    output[x[0]] += 1
                    break
            amount -= 1
        embed = await embed_gen(f"Case Simulation", f"You would've unboxed...\n{client.emoji['colors']['blue']} {output['blue']} blues\n{client.emoji['colors']['purple']} {output['purple']} purples\n{client.emoji['colors']['pink']} {output['pink']} pinks\n{client.emoji['colors']['red']} {output['red']} reds\n{client.emoji['colors']['special']} {output['special']} specials", "blue")
        await ctx.send(embed=embed)


@client.command(name="open")
async def _open_case_(ctx, arg=None):
    try:
        await user_data(ctx)
        if ctx.author.id in client.opening:
            await ctx.send(f"You're already opening a case!", delete_after=4)
            return
        client.opening.append(ctx.author.id)
        conv = {}
        dataCases = []
        data = db.inventory.find_one({"user": ctx.author.id})
        paginator = commands.Paginator(prefix="", suffix="")
        callIndex = 0
        actual_case = None
        for case in data["cases"]:
            if data["cases"][case][1] > 0 or data["cases"][case][0] > 0:
                callIndex += 1
                dataCases.append(case)
                paginator.add_line(
                    f"{callIndex}.) {case} | :key:: {data['cases'][case][0]} | {client.emoji['cases'][case]}: {data['cases'][case][1]}")
                conv[case] = callIndex
        index = 0
        if len(paginator.pages) == 0:
            embed = await embed_gen("You don't have any cases!", f"You don't have any cases! Go get some!", "red")
            await ctx.send(embed=embed)
            client.opening.remove(ctx.author.id)
            return
        embed = await embed_gen("What kind of case would you like to open? (select by index or name)", f"{paginator.pages[index]}", "blue")
        m = await ctx.send(embed=embed)
        case_found = False
        if len(paginator.pages) > 1:
            while True:
                if case_found:
                    break
                embed = await embed_gen("What kind of case would you like to open? (select by index or name)", f"{paginator.pages[index]}", "blue")
                embed.set_footer(text=f'{index+1}/{len(paginator.pages)}')
                await m.edit(embed=embed)
                await m.add_reaction('◀')
                await m.add_reaction('▶')

                def check1(reaction, user):
                    return user == ctx.author and reaction.message.id == m.id

                def check2(m):
                    return m.author == ctx.message.author
                try:
                    done, pending = await asyncio.wait([client.wait_for('message', check=check2), client.wait_for('reaction_add', check=check1)], timeout=120, return_when=asyncio.FIRST_COMPLETED)
                    finished = done.pop().result()
                    for future in pending:
                        future.cancel()
                except asyncio.TimeoutError:
                    if ctx.author.id in client.opening:
                        client.opening.remove(ctx.author.id)
                    break
                if isinstance(finished, discord.Message):
                    message = finished
                    if ctx.valid:
                        if ctx.author.id in client.opening:
                            client.opening.remove(ctx.author.id)
                        return
                    if message.content.lower() == "quit":
                        if ctx.author.id in client.opening:
                            client.opening.remove(ctx.author.id)
                        return
                    try:
                        if (int(message.content)) <= len(dataCases) and (int(message.content)) > 0:
                            actual_case = dataCases[int(message.content)-1]
                            case_found = True

                        else:
                            await ctx.send("Invalid case index. (You can also use the full name of the case)", delete_after=3)
                        await message.delete()
                    except Exception:
                        if message.content in dataCases:
                            actual_case = message.content
                            case_found = True
                        else:
                            await ctx.send("Invalid case name. (You can also use the index next to the case.)", delete_after=3)
                        await message.delete()
                elif isinstance(finished[0], discord.Reaction):
                    reaction = finished[0]
                    user = finished[1]
                    if str(reaction) == '▶':
                        index += 1
                        if index > len(paginator.pages)-1:
                            index -= 1
                        await m.remove_reaction('▶', user)
                    elif str(reaction) == '◀':
                        index -= 1
                        if index < 0:
                            index = 0
                        await m.remove_reaction('◀', user)
                    elif str(reaction) == '🔡':
                        r = await ctx.send('Input page number to go to.')
                        try:
                            message = await client.wait_for('message', timeout=120, check=check2)
                        except asyncio.TimeoutError:
                            return
                        if message.content.isdigit() == True:
                            if int(message.content) > len(paginator.pages):
                                pass
                            elif int(message.content) <= 0:
                                pass
                            else:
                                index = int(message.content) - 1
                            await r.delete()
                            await message.delete()
                        await m.remove_reaction('🔡', user)
        else:
            while True:
                if case_found:
                    break
                try:
                    def check3(m):
                        return m.author == ctx.message.author
                    message2 = await client.wait_for('message', check=check3, timeout=120)
                except asyncio.TimeoutError:
                    if ctx.author.id in client.opening:
                        client.opening.remove(ctx.author.id)
                    break
                if message2.content.lower() == "quit":
                    if ctx.author.id in client.opening:
                        client.opening.remove(ctx.author.id)
                    return
                if message2.content in dataCases:
                    actual_case = message2.content
                    case_found = True
                else:
                    if message2.content.isdigit():
                        if int(message2.content) <= len(dataCases) and (int(message2.content)) > 0:
                            actual_case = dataCases[int(message2.content)-1]
                            case_found = True
            await message2.delete()
        if not case_found:
            await ctx.send(f"Session timed out <@{ctx.author.id}>", delete_after=3)
            return
        data = db.inventory.find_one({"user": ctx.author.id})
        dStats = db.stats.find_one({"user": ctx.author.id})
        univ = False
        if data["cases"][actual_case][1] < 1:
            embed = await embed_gen(f"No cases of that type.", f"You don't seem to have any {actual_case}'s", "red")
            await m.edit(embed=embed)
            await m.remove_reaction('◀', client.user)
            await m.remove_reaction('▶', client.user)
            client.opening.remove(ctx.author.id)
            return
        elif data["cases"][actual_case][0] < 1:
            if arg != "mass":
                if data["universalKeys"] > 0:
                    embed = await embed_gen(f"Hold on!", f"You're about to use a universal key! Are you sure you want to do this?", "orange")
                    await m.edit(embed=embed)

                    def check4(m):
                        return m.author == ctx.message.author
                    try:
                        resp = await client.wait_for('message', timeout=120, check=check4)
                    except asyncio.TimeoutError:
                        return
                    if resp.content.lower() == "yes" or resp.content.lower() == "y":
                        univ = True
                        pass
                    else:
                        embed = await embed_gen(f"Cancelled action.", f"No universal keys will be used.", "blue")
                        await m.edit(embed=embed)
                        return
                else:
                    embed = await embed_gen(f"No keys of that type.", f"You don't seem to have any keys for the {actual_case}", "red")
                    await m.edit(embed=embed)
                    await m.remove_reaction('◀', client.user)
                    await m.remove_reaction('▶', client.user)
                    client.opening.remove(ctx.author.id)
                    return
            else:
                embed = await embed_gen(f"No keys of that type.", f"You don't seem to have any keys for the {actual_case}", "red")
                await m.edit(embed=embed)
                await m.remove_reaction('◀', client.user)
                await m.remove_reaction('▶', client.user)
                client.opening.remove(ctx.author.id)
                return
        await m.remove_reaction('◀', client.user)
        await m.remove_reaction('▶', client.user)

        async def gatherWeapon(actual_case):
            #    Y            X
            # (INDEX, [RARITY, CHANCE])
            num = random.uniform(0.0, 100.0)
            for y, x in enumerate(client.drop_chance):
                if num <= x[1]:
                    gun = random.choice(client.cases[actual_case][x[0]])
                    org = f"{gun}"
                    if gun.lower() == "knife":
                        k_type = random.choice(list(client.knives.keys()))
                        gun = f"{k_type} " + \
                            random.choice(client.knives[k_type])
                    wear = random.uniform(0.000000000, 1.000000000)
                    data = db.inventory.find_one({"user": ctx.author.id})
                    dataStats = db.stats.find_one({"user": ctx.author.id})
                    cv = {"special": "Specials", "red": "Reds",
                          "pink": "Pinks", "purple": "Purples", "blue": "Blues"}
                    dataStats["casesOpened"] += 1
                    dataStats[cv[x[0]]] += 1
                    if org.lower() == "knife":
                        dataStats["Knives"] += 1
                    elif org.lower() == "gloves":
                        dataStats["Gloves"] += 1

                    def generateID():
                        chars = [
                            "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "0123456789", "-&_"]
                        generatedID = ""
                        for i in range(10):
                            generatedID += random.choice(random.choice(chars))
                        return generatedID

                    gid = generateID()
                    while db.uuids.find_one({"uuid": gid}) != None:
                        gid = generateID()
                    if db.uuids.find_one({"uuid": gid}) != None:
                        await ctx.send("We had a problem generating a unique id for your unbox, You have been giving your case and key back.")
                        return
                    today = datetime.datetime.today()

                    stattrak = False
                    if random.randint(0, 100) < 5:
                        stattrak = True

                    db.uuids.insert_one({"roll": num, "owner": ctx.author.id, "user": ctx.author.id, "weapon": f"{'[StatTrak] ' if stattrak else ''}{gun}[=]{x[0]}[=]{wear}[=]{gid}",
                                         "uuid": gid, "time": f"{today.month}/{today.day}/{today.year} @ {time.strftime('%H:%M:%S', time.gmtime(time.time()))} UTC"})
                    data["items"].append(
                        f"{'[StatTrak] ' if stattrak else ''}{gun}[=]{x[0]}[=]{wear}[=]{gid}")
                    data["cases"][actual_case][1] -= 1
                    if not univ:
                        data["cases"][actual_case][0] -= 1
                    else:
                        data["universalKeys"] -= 1
                    db.inventory.replace_one({"user": ctx.author.id}, data)
                    db.stats.replace_one({"user": ctx.author.id}, dataStats)
                    #     F
                    # (WEAR)
                    for _, f in enumerate(client.floats):
                        condition = f
                        if wear > client.floats[f]:
                            break
                    if x[0] == "special":
                        db.unboxed_knives.insert_one(
                            {"uuid": gid, "case": actual_case})
                    info = calculate_price(gid)

                    case_val = client.casesP[actual_case] + 2.50
                    profit = round(info[0]-case_val, 2)
                    if profit > 0:
                        profit = f"+${profit}"
                    else:
                        profit = f"-${abs(profit)}"

                    # create if first log
                    if db.log.find_one({"user": ctx.author.id}) == None:
                        db.log.insert_one(
                            {"user": ctx.author.id, "history": []})

                    logs = db.log.find_one({"user": ctx.author.id})

                    # clear space
                    if len(logs["history"]) >= 10:
                        del logs["history"][0]

                    # add new log
                    logs["history"].append(
                        [f"{'[StatTrak] ' if stattrak else ''}{gun}[=]{x[0]}[=]{wear}[=]{gid}", profit])

                    db.log.replace_one({"user": ctx.author.id}, logs)

                    return f"{client.emoji['colors'][x[0]]} {'[StatTrak] ' if stattrak else ''}{gun} @ {condition} :: {discord.utils.escape_markdown(gid)} \n({profit})\n"
        if arg == "mass" and dStats["massUnlocked"]:
            nums = [data["cases"][actual_case][0],
                    data["cases"][actual_case][1]]
            if nums[0] > 0 and nums[1] > 0:
                howMany = min(nums)
                selec = int(f"{howMany}")
            else:
                await m.edit(embed=(await embed_gen("Unable to open!", "You don't have the required cases and keys for this! Make sure you have atleast 1 key and 1 case.", "red")))
                return
            s = ''
            if howMany > 5:
                howMany = 5
                selec = 5
            while howMany > 0:
                s += (await gatherWeapon(actual_case))
                howMany -= 1
            embed = await embed_gen(f"Opening. | {ctx.author}", f"Rolling {selec} {actual_case}'s.", "red")
            await m.edit(embed=embed)
            await asyncio.sleep(1)
            embed = await embed_gen(f"Opening.. | {ctx.author}", f"Rolling {selec} {actual_case}'s..", "orange")
            await m.edit(embed=embed)
            await asyncio.sleep(1)
            embed = await embed_gen(f"Opening... | {ctx.author}", f"Rolling {selec} {actual_case}'s...", "green")
            await m.edit(embed=embed)
            await asyncio.sleep(1)
            em = await embed_gen(f"Opened {selec} {actual_case}'s", s, "green")
            await m.edit(embed=em)
        else:
            embed = await embed_gen(f"Opening. | {ctx.author}", f"Rolling {actual_case}.", "red")
            await m.edit(embed=embed)
            await asyncio.sleep(1)
            embed = await embed_gen(f"Opening.. | {ctx.author}", f"Rolling {actual_case}..", "orange")
            await m.edit(embed=embed)
            await asyncio.sleep(1)
            embed = await embed_gen(f"Opening... | {ctx.author}", f"Rolling {actual_case}...", "green")
            await m.edit(embed=embed)
            await asyncio.sleep(1)
            em = await embed_gen(f"Opened {actual_case}", (await gatherWeapon(actual_case)), "green")
            await m.edit(embed=em)
        client.opening.remove(ctx.author.id)
    except Exception as e:
        print(e)
        await ctx.send("An error has occured try again!", delete_after=4)
        if ctx.author.id in client.opening:
            client.opening.remove(ctx.author.id)
        return


@client.command(name="store", aliases=["shop"])
async def _open_store_menu_(ctx, cat=None):
    await user_data(ctx)
    categories = {"upgrades": "UPGRADES", "cases": "CASES", "keys": "KEYS"}
    if cat == None or cat.lower() not in categories:
        embed = await embed_gen("Invalid category.", "Invalid category. The categories are: keys, cases, or upgrades\n`;shop category`", "red")
        await ctx.send(embed=embed)
        return
    if cat.lower() == "upgrades":
        data = db.stats.find_one({"user": ctx.author.id})
        pages = [f"1.) `Increase Max Pending Money (+$1):` **${round(math.pow( data['maxPendingMoney'], 1.5 ),2) + 7}**\n\n2.) `Increase rate of money generation (+$.01):` **${round(math.pow( data['moneyPer10seconds']*100, 1.75 ),2) + 7}**\n\n{'3.) `Unlock mass case unboxing:` **$800**' if not data['massUnlocked'] else ''}"]
        purchases = {1: "maxPending", 2: "per10", 3: "massUnboxing"}
        m = await ctx.send(embed=(await embed_gen("Shop", pages[0], "green")))

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        try:
            resp = await client.wait_for("message", check=check, timeout=120)
        except asyncio.TimeoutError:
            await m.edit(content="**Shop session timed out**")
            return
        if resp.content.isdigit():
            buy = int(resp.content)
            if buy in purchases:
                if buy == 1:
                    if data["currentMoney"] >= (round(math.pow(data['maxPendingMoney'], 1.5), 2) + 7):
                        data["currentMoney"] -= (
                            round(math.pow(data['maxPendingMoney'], 1.5), 2) + 7)
                        data["maxPendingMoney"] += 1
                        data["totalMoneySpent"] += (
                            round(math.pow(data['maxPendingMoney'], 1.5), 2) + 7)
                        db.stats.replace_one({"user": ctx.author.id}, data)
                        await resp.delete()
                        await m.edit(content=f"Purchase successful! `{round(data['maxPendingMoney'] - 1, 2)}` -> `{round(data['maxPendingMoney'], 2)}`\n New Balance: ${round(data['currentMoney'], 2)}", embed=None)
                        return
                    else:
                        await m.edit(content="**You dont have enough money!**")
                        await resp.delete()
                elif buy == 2:
                    if data['currentMoney'] >= (round(math.pow(data['moneyPer10seconds']*100, 1.75), 2) + 7):
                        data["currentMoney"] -= (
                            round(math.pow(data['moneyPer10seconds']*100, 1.75), 2) + 7)
                        data["moneyPer10seconds"] += .01
                        data["totalMoneySpent"] += (
                            round(math.pow(data['moneyPer10seconds']*100, 1.75), 2) + 7)
                        db.stats.replace_one({"user": ctx.author.id}, data)
                        await resp.delete()
                        await m.edit(content=f"Purchase successful! `{data['moneyPer10seconds'] -.01}` -> `{round(data['moneyPer10seconds'], 2)}`\n New Balance: ${round(data['currentMoney'], 2)}", embed=None)
                        return
                    else:
                        await m.edit(content="**You dont have enough money!**")
                        await resp.delete()
                elif buy == 3 and not data['massUnlocked']:
                    if data['currentMoney'] >= 800:
                        data["currentMoney"] -= 800
                        data["massUnlocked"] = True
                        data["totalMoneySpent"] += 800
                        db.stats.replace_one({"user": ctx.author.id}, data)
                        await resp.delete()
                        await m.edit(content=f"Purchase successful! Mass unbox unlocked!\n New Balance: ${round(data['currentMoney'], 2)}", embed=None)
                        return
                    else:
                        await m.edit(content="**You dont have enough money!**")
                        await resp.delete()
        else:
            await ctx.send("Please input a valid number!", delete_after=3)
    elif cat.lower() == "cases":
        purchases = {}
        num = 1
        paginator = commands.Paginator(prefix="", suffix="")
        inv, stats = db.inventory.find_one(
            {"user": ctx.author.id}), db.stats.find_one({"user": ctx.author.id})
        for case in client.casesP:
            purchases[num] = [case, client.casesP[case]]
            num += 1
        for i in purchases:
            paginator.add_line(
                f"{i}.) `{purchases[i][0]}`:: **${purchases[i][1]}**")
        index = 0
        embed = await embed_gen("What kind of case would you like to buy? (Select by index). Type \"quit\" to exit this selection.", f"{paginator.pages[index]}", "blue")
        embed.set_footer(text=f'{index+1}/{len(paginator.pages)}')
        m = await ctx.send(embed=embed)

        def check1(reaction, user):
            return user == ctx.author and reaction.message.id == m.id

        def check2(m):
            return m.author == ctx.message.author
        while True:
            embed = await embed_gen("What kind of case would you like to buy? (select by index). Type \"quit\" to exit this selection.", f"{paginator.pages[index]}", "blue")
            embed.set_footer(text=f'{index+1}/{len(paginator.pages)}')
            await m.edit(embed=embed)
            await m.add_reaction('◀')
            await m.add_reaction('▶')
            try:
                done, pending = await asyncio.wait([client.wait_for('message', check=check2), client.wait_for('reaction_add', check=check1)], timeout=120, return_when=asyncio.FIRST_COMPLETED)
                finished = done.pop().result()
                for future in pending:
                    future.cancel()
            except asyncio.TimeoutError:
                break
            if isinstance(finished, discord.Message):
                message = finished
                if message.content.lower() == "quit":
                    return
                elif message.content.isdigit():
                    if int(message.content) in purchases:
                        case = purchases[int(message.content)][0]
                        count = 1
                        embed = await embed_gen("How many?", f"How many {case}'s would you like to buy?. Type \"quit\" to exit this selection.", "blue")
                        await m.edit(embed=embed)
                        await message.delete()
                        try:
                            r = await client.wait_for("message", check=check2, timeout=30)
                        except asyncio.TimeoutError:
                            await m.edit(content="Timed out.")
                            return
                        if r.content.isdigit():
                            if int(r.content) > 0:
                                count = int(r.content)
                                if stats['currentMoney'] >= (client.casesP[case] * count):
                                    inv["cases"][case][1] += count
                                    stats['currentMoney'] -= (
                                        client.casesP[case] * count)
                                    stats["totalMoneySpent"] += (
                                        client.casesP[case] * count)
                                    db.stats.replace_one(
                                        {"user": ctx.author.id}, stats)
                                    db.inventory.replace_one(
                                        {"user": ctx.author.id}, inv)
                                    await m.edit(content=f"Successfully purchased!\n New Balance: ${round(stats['currentMoney'], 2)}")
                                    await r.delete()
                                    return
                                else:
                                    await m.edit(content="You dont have enough money for this!")
                                    return
                            else:
                                await m.edit(content="Invalid amount! Please retry!")
                                return
                        else:
                            await m.edit(content="Invalid amount! Please retry!")
                            return

                await message.delete()
            elif isinstance(finished[0], discord.Reaction):
                reaction = finished[0]
                user = finished[1]
                if str(reaction) == '▶':
                    index += 1
                    if index > len(paginator.pages)-1:
                        index -= 1
                    await m.remove_reaction('▶', user)
                elif str(reaction) == '◀':
                    index -= 1
                    if index < 0:
                        index = 0
                    await m.remove_reaction('◀', user)
                elif str(reaction) == '🔡':
                    r = await ctx.send('Input page number to go to.')
                    try:
                        message = await client.wait_for('message', timeout=120, check=check2)
                    except asyncio.TimeoutError:
                        return
                    if message.content.isdigit() == True:
                        if int(message.content) > len(paginator.pages):
                            pass
                        elif int(message.content) <= 0:
                            pass
                        else:
                            index = int(message.content) - 1
                        await r.delete()
                        await message.delete()
                    await m.remove_reaction('🔡', user)
    elif cat.lower() == "keys":
        purchases = {}
        num = 1
        paginator = commands.Paginator(prefix="", suffix="")
        inv, stats = db.inventory.find_one(
            {"user": ctx.author.id}), db.stats.find_one({"user": ctx.author.id})
        for case in client.casesP:
            purchases[num] = case
            num += 1
        for i in purchases:
            paginator.add_line(f"{i}.) `{purchases[i]} Key`:: **$2.50**")
        index = 0
        embed = await embed_gen("What kind of key would you like to buy? (Select by index). Type \"quit\" to exit this selection.", f"{paginator.pages[index]}", "blue")
        embed.set_footer(text=f'{index+1}/{len(paginator.pages)}')
        m = await ctx.send(embed=embed)

        def check1(reaction, user):
            return user == ctx.author and reaction.message.id == m.id

        def check2(m):
            return m.author == ctx.message.author
        while True:
            embed = await embed_gen("What kind of key would you like to buy? (select by index). Type \"quit\" to exit this selection.", f"{paginator.pages[index]}", "blue")
            embed.set_footer(text=f'{index+1}/{len(paginator.pages)}')
            await m.edit(embed=embed)
            await m.add_reaction('◀')
            await m.add_reaction('▶')
            try:
                done, pending = await asyncio.wait([client.wait_for('message', check=check2), client.wait_for('reaction_add', check=check1)], timeout=120, return_when=asyncio.FIRST_COMPLETED)
                finished = done.pop().result()
                for future in pending:
                    future.cancel()
            except asyncio.TimeoutError:
                break
            if isinstance(finished, discord.Message):
                message = finished
                if message.content.lower() == "quit":
                    return
                elif message.content.isdigit():
                    if int(message.content) in purchases:
                        case = purchases[int(message.content)]
                        count = 1
                        embed = await embed_gen("How many?", f"How many {case} Keys would you like to buy?", "blue")
                        await m.edit(embed=embed)
                        await message.delete()
                        try:
                            r = await client.wait_for("message", check=check2, timeout=30)
                        except asyncio.TimeoutError:
                            await m.edit(content="Timed out.")
                            return
                        if r.content.isdigit():
                            if int(r.content) > 0:
                                count = int(r.content)
                                if stats['currentMoney'] >= (2.50 * count):
                                    inv["cases"][case][0] += count
                                    stats['currentMoney'] -= (2.50 * count)
                                    stats["totalMoneySpent"] += (2.50 * count)
                                    db.stats.replace_one(
                                        {"user": ctx.author.id}, stats)
                                    db.inventory.replace_one(
                                        {"user": ctx.author.id}, inv)
                                    await m.edit(content=f"Successfully purchased!\n New Balance: ${round(stats['currentMoney'], 2)}")
                                    await r.delete()
                                    return
                                else:
                                    await m.edit(content="You dont have enough money for this!")
                                    return
                            else:
                                await m.edit(content="Invalid amount! Please retry!")
                                return
                        else:
                            await m.edit(content="Invalid amount! Please retry!")
                            return

                await message.delete()
            elif isinstance(finished[0], discord.Reaction):
                reaction = finished[0]
                user = finished[1]
                if str(reaction) == '▶':
                    index += 1
                    if index > len(paginator.pages)-1:
                        index -= 1
                    await m.remove_reaction('▶', user)
                elif str(reaction) == '◀':
                    index -= 1
                    if index < 0:
                        index = 0
                    await m.remove_reaction('◀', user)
                elif str(reaction) == '🔡':
                    r = await ctx.send('Input page number to go to.')
                    try:
                        message = await client.wait_for('message', timeout=120, check=check2)
                    except asyncio.TimeoutError:
                        return
                    if message.content.isdigit() == True:
                        if int(message.content) > len(paginator.pages):
                            pass
                        elif int(message.content) <= 0:
                            pass
                        else:
                            index = int(message.content) - 1
                        await r.delete()
                        await message.delete()
                    await m.remove_reaction('🔡', user)


@client.command(name="info")
async def _see_bot_info_(ctx):
    await user_data(ctx)
    await ctx.message.delete()
    current_time = time.time()
    difference = int(round(current_time - start_time))
    text = str(datetime.timedelta(seconds=difference))
    message = f"""

    Odds are based off of Perfect World, the chinese edition of CS:GO.

    This bot is still in HEAVY development any bugs you come across please report with ;bug.

    **Scheduled updates for any bugs will be at 12pm & 8pm EST**
    # of guilds: {len(client.guilds)}

    Uptime: {text}
    Money generated this session: {client.money_generated}

    CHANGELOG:
    Item prices updated: 2/28/2022
	8 new cases added


    """
    embed = await embed_gen("Unboxer Statistics", message, "blue")
    await ctx.send(embed=embed)


@client.command(name="bug")
async def _bug_report_(ctx, *, bug: str = None):
    await user_data(ctx)
    await ctx.message.delete()
    if bug == None:
        embed = await embed_gen("Bug reports", "Missing body text `;bug <bug>`", "red")
        await ctx.send(embed=embed)
        return
    now = datetime.datetime.now()
    db.bugs.insert_one({"body": bug, "user": ctx.author.id, "date": f"{now.month}/{now.day}/{now.year}",
                        "time": f"{now.hour}:{now.minute}:{now.second}"})
    embed = await embed_gen("Bug reports", "Succesfully sent in bug report.", "green")
    await ctx.send(embed=embed)


@client.command(name="help")
async def _get_help_(ctx):
    await user_data(ctx)
    message = """
    **<>:required** **[]:optional**
    
    **Any selection menu can be exited with 'quit'**
    
    `;trade <@User>` : Send a trade request to a user.
    `;sell <weaponID>` : Sell a weapon, prices are based off of rarity, wear, and the case you unboxed it from.
    `;claim` : Claim the pending money you earned from chatting or talking in a vc.
    `;market [keywords]` : Search the community market for listings.
    `;post <weaponID> <price>` : Posts a weapon from your inventory to the community market.
    `;item <weaponID>` : Allows you to get a detailed description on a weapon.
    `;daily` : Claim your daily reward.
    `;profile` : Open your profile to view things like money, pending money, and other in depth statistics.
    `;inv` : Shortcut to inventory which is normally displayed in `;profile`
    `;simulate <1-200>` : Simulate rolling cases for free to see what you would have gotten.
    `;open [mass]` : Start unboxing a case. Adding the \"mass\" argument will allow you to unbox multiple cases at once; assuming you have the upgrade from the shop.
    `;shop <category>` : Search the store to buy cases, keys, and upgrades.
    `;info` : See some info on the bot.
    `;flip` <amount> [heads/tails]` : Gamble up to $20 on a coinflip, defaults to heads.
    `;rates` : Displays drop rates and price calculations for items.
    `;log` : A list of your last 10 case openings, showing profit, condition and weapon.
    `;help` : Open this page. 
    

    """
    await ctx.author.send(embed=(await embed_gen("Unboxer Help Page", message, "blue")))
    await ctx.message.delete()


@client.command(name="rates", aliases=["prices"])
async def _drop_rates_(ctx):
    await user_data(ctx)
    await ctx.send("```ini\ncv = case value\n         Multipliers          |     Drop Rates\n    [cv/2] Blue               |        55  % \n    [(cv/1.25)+1.25] Purple   |        37  %\n    [(cv*2)+2.50] Pink        |        6.5 %\n    [(cv*4.3)+5] Red          |        1   %\n    [(cv*8)+10] Special       |        .5  %\n----------------------------------------------------\nv = value after color multipliers\n         Multipliers          |       Ranges     |    Drop Rates\n    [v*.65]  Battle Scarred   |    .68 ->   1    |       32%\n    [v*1]    Well Worn        |    .39 -> .68    |       29%\n    [v*1.75] Field Tested     |    .18 -> .44    |       26%  \n    [v*2.5]  Minimal Wear     |    .07 -> .18    |       11%\n    [v*4.3]  Factory New      |      0 -> .07    |        7%\n----------------------------------------------------\nv = value after color & wear\n         Multipliers          |     Drop Rates\n    [v*1.1] StatTrak          |        5  %\n```")


def calculate_price(weapon: str = None):
    item = db.uuids.find_one({"uuid": weapon})
    rarity = item["weapon"].split("[=]")[1]
    wear = float(item["weapon"].split("[=]")[2])
    name = item["weapon"].split("[=]")[0]
    found = False
    if "[StatTrak] " in name:
        name = name[11:]
        stattrak = True
    else:
        stattrak = False
    for case in client.cases:
        for rarity in client.cases[case]:

            if name in client.cases[case][rarity]:
                inCase = case
                found = True
            if found:
                break
        if found:
            break
    if rarity == "blue":
        value = client.casesP[inCase] / 2
    elif rarity == "purple":
        value = client.casesP[inCase] / 1.25
        value += 1.25
    elif rarity == "pink":
        value = client.casesP[inCase] * 2
        value += 2.50
    elif rarity == "red":
        value = client.casesP[inCase] * 4.3
        value += 5
    elif rarity == "special":
        value = client.casesP[db.unboxed_knives.find_one({"uuid": weapon})[
            "case"]] * 8
        value += 10
    if stattrak:
        value *= 1.35
    wears = {.68: .65, .39: 1, .18: 1.75, .07: 2.5, 0: 4.3}
    for num in wears:
        if wear > num:
            value *= wears[num]
            break
    return [round(value, 2), name, wear]


def get_wear(weapon: str = None):
    item = db.uuids.find_one({"uuid": weapon})
    for condition in client.floats:
        if float(item["weapon"].split("[=]")[2]) > client.floats[condition]:
            return condition


@client.command(name="sell")
async def _sell_items_(ctx, weapon=None):
    await user_data(ctx)
    if weapon == None:
        await ctx.send("```ini\n[1] Select an item to sell!\n```")
        return
    item = db.uuids.find_one({"uuid": weapon})
    stats = db.stats.find_one({"user": ctx.author.id})
    rarities = {
        "blue": "blue", "purple": "purple", "pink": "pink", "red": "red", "special": "special",
        "blues": "blue", "purples": "purple", "pinks": "pink", "reds": "red", "specials": "special"
    }
    if weapon not in rarities:
        if item != None and item["owner"] == ctx.author.id:
            inv = db.inventory.find_one({"user": ctx.author.id})
            inv["items"].remove(item["weapon"])
            info = calculate_price(weapon)
            stats["currentMoney"] += info[0]
            m = await ctx.send(f"```ini\n[1] Are you sure you would like to sell {info[1]} @ {info[2]} for ${info[0]}?\n```")

            def check(m):
                return m.author == ctx.author
            try:
                r = await client.wait_for("message", check=check, timeout=120)
            except Exception:
                m.edit("```ini\n[1] Timeout.\n```")
                return
            if r.content.lower() == "y" or r.content.lower() == "yes":
                db.stats.replace_one({"user": ctx.author.id}, stats)
                db.inventory.replace_one({"user": ctx.author.id}, inv)
                item["owner"] = None
                db.uuids.replace_one({"uuid": item["uuid"]}, item)
                await m.edit(content=f"```ini\n[1] You have sold {info[1]} @ {info[2]} for ${info[0]}\n[2] New Balance: ${round(stats['currentMoney'],2)}\n```")
            else:
                await m.edit(content=f"```ini\n[1] Item will not be sold.```")
    else:
        inv = db.inventory.find_one({"user": ctx.author.id})
        stats = db.stats.find_one({"user": ctx.author.id})
        sell_these = []
        total = 0
        for item in inv['items']:
            if item.split("[=]")[1] == rarities[weapon].lower():
                sell_these.append(item)
        for item in sell_these:
            info = calculate_price(item.split("[=]")[3])
            inv["items"].remove(item)
            total += (info[0])
        m = await ctx.send(f"```ini\n[1] Are you sure you would like to sell {len(sell_these)} {rarities[weapon]}s for ${total}?\n```")

        def check(m):
            return m.author == ctx.author
        try:
            r = await client.wait_for("message", check=check, timeout=120)
        except Exception:
            m.edit("Timeout.")
            return
        if r.content.lower() == "y" or r.content.lower() == "yes":
            db.inventory.replace_one({"user": ctx.author.id}, inv)
            stats['currentMoney'] += total
            db.stats.replace_one({"user": ctx.author.id}, stats)
            for items in sell_these:
                item = db.uuids.find_one({"uuid": items.split("[=]")[3]})
                item["owner"] = None
                item = db.uuids.replace_one({"item": item["uuid"]}, item)
            await m.edit(content=f"```ini\n[1] You have sold {len(sell_these)} {rarities[weapon]}s for ${round(total, 2)}\n[2] New Balance: ${round(stats['currentMoney'],2)}\n```")
        else:
            await m.edit(content=f"```ini\n[1] Items will not be sold.\n```")


def isFloat(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def isInt(string):
    return string.isdigit()


@client.command(name="flip")
async def _flip_gamble(ctx, amount: str = None, call: str = "heads" if random.randint(0, 1) == 0 else "tails"):
    await user_data(ctx)
    if isFloat(amount) or isInt(string):
        amount = float(amount)
        user = db.stats.find_one({"user": ctx.author.id})
        if user["currentMoney"] < amount:
            await ctx.send(f"```ini\n[1] You dont have ${amount}\n```")
            return
        if amount > 20.00:
            await ctx.send("```ini\n[1] You can't bet more than $20\n```")
            return
        sides = ["heads", "tails"]
        roll = random.randint(0, 100)
        if roll > 50:
            won = 0
        else:
            won = 1
        if call.lower() == sides[won]:
            await ctx.send(f"```ini\n[1] You won ${amount}!\n[2] Roll: {roll}\n[3] Called: {call}\n```")
            user["currentMoney"] += amount
        else:
            await ctx.send(f"```ini\n[1] You lost ${amount}.\n[2] Roll: {roll}\n[3] Called: {call}\n```")
            user["currentMoney"] -= amount
        db.stats.replace_one({"user": user["user"]}, user)


@client.command(name="upgrade")
async def _upgrade_gamble_(ctx, weapon: str = None):

    return


@client.command(name="log", aliases=["history"])
async def _case_log_(ctx, user: discord.User = None):
    await user_data(ctx)
    if user == None:
        user = ctx.author
    if db.log.find_one({"user": user.id}) == None:
        await ctx.send("```ini\n[1] They haven't opened any cases yet!\n```")
        return
    logs = db.log.find_one({"user": user.id})
    message = "  [               Case Log (Last 10)               ]\n"
    lines = 1
    for log in reversed(logs["history"]):
        message += f"[{lines}] {log[0].split('[=]')[0]} @ {get_wear(log[0].split('[=]')[3])} | [{log[1]}]\n"
        lines += 1
    await ctx.send(f"```ini\n{message}\n```")
    return


# []           Administration             [] #


@client.command(name="reload")
async def _reload_bot_(ctx):
    if db.admins.find_one({"user": ctx.author.id}) == None:
        embed = await embed_gen(f"Permission Denied", f"You are not an admin, therefore not able to reload the bot. For any questions please refer to `iiVeil#0001`", "red")
        await ctx.author.send(embed=embed)
        return
    await client.logout()
    await client.login(open("token.txt", "r").read())
    print("Reload Complete")


@client.command(name="wipeinv")
async def _wipe_inventory_(ctx, user: discord.User = None):
    if db.admins.find_one({"user": ctx.author.id}) == None:
        embed = await embed_gen(f"Permission Denied", f"You are not an admin, therefore not able to wipe inventories. For any questions please refer to `iiVeil#0001`", "red")
        await ctx.author.send(embed=embed)
        return
    if user == None:
        await ctx.send("No user specified!")
        return
    if db.inventory.find_one({"user": user.id}) == None:
        await ctx.send(f"No user data found for <@{user.id}>")
        return
    dataInv = {
        "user": ctx.author.id,
        "items": [],
        "cases": {
            # [KEYS, CASES]
            "Operation Wildfire Case": [0, 0],
            "Operation Hydra Case": [0, 0],
            "Spectrum Case": [0, 0],
            "Operation Bravo Case": [0, 0],
            "eSports 2013 Case": [0, 0],
            "eSports 2014 Summer Case": [0, 0],
            "eSports 2013 Winter Case": [0, 0],
            "CS:GO Weapon Case 2": [0, 0],
            "CS:GO Weapon Case 3": [0, 0],
            "CS:GO Weapon Case": [0, 0],
            "Falchion Case": [0, 0],
            "Chroma 2 Case": [0, 0],
            "Operation Breakout Weapon Case": [0, 0],
            "Huntsman Weapon Case": [0, 0],
            "Winter Offensive Weapon Case": [0, 0],
            "Operation Vanguard Weapon Case": [0, 0],
            "Revolver Case": [0, 0],
            "Chroma Case": [0, 0],
            "Shadow Case": [0, 0],
            "Chroma 3 Case": [0, 0],
            "Gamma Case": [0, 0],
            "Gamma 2 Case": [0, 0],
            "Shattered Web Case": [0, 0],
            "CS20 Case": [0, 0],
            "Glove Case": [0, 0],
            "Danger Zone Case": [0, 0],
            "Horizon Case": [0, 0],
            "Spectrum 2 Case": [0, 0],
            "Clutch Case": [0, 0]
        }
    }
    db.inventory.replace_one({"user": user.id}, dataInv)
    await ctx.send("Done.")


@client.command(name="wipedata")
async def _wipe_data_(ctx, user: discord.User = None):
    if db.admins.find_one({"user": ctx.author.id}) == None:
        embed = await embed_gen(f"Permission Denied", f"You are not an admin, therefore not able to wipe user data. For any questions please refer to `iiVeil#0001`", "red")
        await ctx.author.send(embed=embed)
        return
    if user == None:
        await ctx.send("No user specified!")
        return
    if db.userdata.find_one({"user": user.id}) == None:
        await ctx.send(f"No user data found for <@{user.id}>")
        return
    db.userdata.delete_one({"user": user.id})
    db.stats.delete_one({"user": user.id})
    db.inventory.delete_one({"user": user.id})
    db.dailies.delete_one({"user": user.id})
    await ctx.send("Done.")


@client.command(name="refresh")
async def _reload_weapon_data(ctx):
    if db.admins.find_one({"user": ctx.author.id}) == None:
        embed = await embed_gen(f"Permission Denied", f"You are not an admin, therefore not able to refresh weapon data. For any questions please refer to `iiVeil#0001`", "red")
        await ctx.author.send(embed=embed)
        return
    client.cases = json.load(open("cases.json", "r"))
    client.knives = json.load(open("knives.json", "r"))
    client.weapons = json.load(open("weapons.json", "r"))
    embed = await embed_gen(f"Completed", f"Successfully refreshed weapon & case data.", "green")
    await ctx.author.send(embed=embed)


def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


@client.command(name='eval')
async def eval_fn(ctx, *, cmd):
    if ctx.message.author.id != 300307874725494784:
        return
    fn_name = "_eval_expr"
    cmd = cmd.strip("` ")
    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
    body = f"async def {fn_name}():\n{cmd}"
    parsed = ast.parse(body)
    body = parsed.body[0].body

    insert_returns(body)
    env = {
        'client': client,
        'discord': discord,
        'commands': commands,
        'ctx': ctx,
        'db': db,
        "ObjectId": ObjectId,
        '__import__': __import__
    }
    exec(compile(parsed, filename="<ast>", mode="exec"), env)
    result = (await eval(f"{fn_name}()", env))
    print(result)


@client.command(name="close")
async def _end_session_(ctx):
    if ctx.author.id != 300307874725494784:
        return
    await client.close()


@client.command(name="viewdb")
async def show_databases(ctx, database):
    if db.admins.find_one({"user": ctx.author.id}) == None:
        embed = await embed_gen(f"Permission Denied", f"You are not an admin, therefore not able to view databases. For any questions please refer to `iiVeil#0001`", "red")
        await ctx.author.send(embed=embed)
        return
    if database == "?":
        await ctx.send(f"{db.list_collection_names()}")
        return
    paginator = commands.Paginator(prefix="", suffix="")
    numfound = 0
    if database in db.list_collection_names():
        for item in db[f"{database}"].find():
            paginator.add_line(f"{numfound+1} | {item}\n")
            numfound += 1
    page = 0
    embed = await embed_gen(f"Found {numfound} entries.", f"{paginator.pages[page]}", "blue")
    embed.set_footer(text=f'{page+1}/{len(paginator.pages)}')
    m = await ctx.send(embed=embed)
    await m.add_reaction('◀')
    await m.add_reaction('▶')
    await m.add_reaction('🔡')
    while True:
        embed = await embed_gen(f"Found {numfound} entries.", f"{paginator.pages[page]}", "blue")
        embed.set_footer(text=f'{page+1}/{len(paginator.pages)}')
        await m.edit(embed=embed)

        def check(reaction, user):
            return user == ctx.author and reaction.message.id == m.id
        try:
            reaction, user2 = await client.wait_for('reaction_add', timeout=120, check=check)
        except asyncio.TimeoutError:
            break
        if str(reaction) == '▶':
            page += 1
            if page > len(paginator.pages)-1:
                page -= 1
            await m.remove_reaction('▶', user2)
        elif str(reaction) == '◀':
            page -= 1
            if page < 0:
                page = 0
            await m.remove_reaction('◀', user2)
        elif str(reaction) == '🔡':
            r = await ctx.send('Input page number to go to.')

            def check2(m):
                return m.author == ctx.message.author
            try:
                message = await client.wait_for('message', check=check2)
            except asyncio.TimeoutError:
                return
            if message.content.isdigit() == True:
                if int(message.content) > len(paginator.pages):
                    pass
                elif int(message.content) <= 0:
                    pass
                else:
                    page = int(message.content) - 1
                await r.delete()
                await message.delete()
            await m.remove_reaction('🔡', user2)


@client.command("insert")
async def _insert_db_(ctx, database: str = None, *, data: str = None):
    await ctx.message.delete()
    if db.admins.find_one({"user": ctx.author.id}) == None:
        embed = await embed_gen(f"Permission Denied", f"You are not an admin, therefore not able to insert into databases. For any questions please refer to `iiVeil#0001`", "red")
        await ctx.author.send(embed=embed)
        return
    if database == "?":
        await ctx.send(f"{db.list_collection_names()}")
        return
    post_id = db[database].insert_one(ast.literal_eval(data)).inserted_id
    await ctx.send(f"Done. | {post_id}")


@client.command("delete")
async def _delete_db_(ctx, database: str = None, *, objid: str = None):
    await ctx.message.delete()
    if db.admins.find_one({"user": ctx.author.id}) == None:
        embed = await embed_gen(f"Permission Denied", f"You are not an admin, therefore not able to delete databases. For any questions please refer to `iiVeil#0001`", "red")
        await ctx.author.send(embed=embed)
        return
    if database == "?":
        await ctx.send(f"{db.list_collection_names()}")
        return
    if database in db.list_collection_names():
        db[database].delete_one({"_id": ObjectId(f'{objid}')})
        await ctx.send(f"Done.")


@client.command(name="ban")
async def _bot_ban_(ctx, id: int = None):
    await ctx.message.delete()
    if db.admins.find_one({"user": ctx.author.id}) == None:
        embed = await embed_gen(f"Permission Denied", f"You are not an admin, therefore not able to ban users. For any questions please refer to `iiVeil#0001`", "red")
        await ctx.author.send(embed=embed)
        return
    if db.admins.find_one({"user": id}) != None:
        embed = await embed_gen(f"Permission Denied", f"You can not ban an admin.", "red")
        await ctx.author.send(embed=embed)
        return
    m = await ctx.send(f"Are you sure you would like to ban {client.get_user(id)}?")

    def check(m):
        return m.author == ctx.author
    resp = await client.wait_for("message", check=check)
    if resp.content.lower() == "yes":
        db.banned.insert_one({"id": id})
        await m.edit(content=f"Banned {client.get_user(id)}.")
        try:
            await client.get_user(id).send("You have been banned by an admin. Contact `iiVeil#0001` for more details.")
        except:
            pass
        await resp.delete()
        return


@client.command(name="unban")
async def _bot_unban_(ctx, id: int = None):
    await ctx.message.delete()
    if db.admins.find_one({"user": ctx.author.id}) == None:
        embed = await embed_gen(f"Permission Denied", f"You are not an admin, therefore not able to unban users. For any questions please refer to `iiVeil#0001`", "red")
        await ctx.author.send(embed=embed)
        return
    m = await ctx.send(f"Are you sure you would like to unban {client.get_user(id)}?")

    def check(m):
        return m.author == ctx.author
    resp = await client.wait_for("message", check=check)
    if resp.content.lower() == "yes":
        db.banned.delete_one({"id": id})
        await m.edit(content=f"Unbanned {client.get_user(id)}.")
        try:
            await client.get_user(id).send("You have been unbanned by an admin.")
        except:
            pass
        await resp.delete()
        return


@client.command(name="push-db-multi")
async def _push_database_update_(ctx, database: str = None, *, data: str = None):
    if db.admins.find_one({"user": ctx.author.id}) == None:
        embed = await embed_gen(f"Permission Denied", f"You are not an admin, therefore not able to push a database update. For any questions please refer to `iiVeil#0001`", "red")
        await ctx.author.send(embed=embed)
        return
    if database == "?":
        await ctx.send(f"{db.list_collection_names()}")
        return
    if database in db.list_collection_names():
        num_changed = 0
        data = ast.literal_eval(data)
        start_time = time.time()
        for data_set in db[database].find():
            num_changed += 1
            for key in data:
                data_set[key] = data[key]
        db[database].replace_one({"_id": data_set["_id"]}, data_set)
        await ctx.send(f"Successfully completed push in {round(time.time()-start_time, 2)} seconds. Which affected {num_changed} entries.")


@client.command(name="push-db-single")
async def _push_database_update_single_(ctx, database: str = None, objid: str = None, *, data: str = None):
    if db.admins.find_one({"user": ctx.author.id}) == None:
        embed = await embed_gen(f"Permission Denied", f"You are not an admin, therefore not able to push a database update. For any questions please refer to `iiVeil#0001`", "red")
        await ctx.author.send(embed=embed)
        return
    if database == "?":
        await ctx.send(f"{db.list_collection_names()}")
        return
    if database in db.list_collection_names():
        start_time = time.time()
        data = ast.literal_eval(data)
        data_set = db[database].find_one({"_id": ObjectId(objid)})
        for key in data:
            data_set[key] = data[key]
        db[database].replace_one({"_id": data_set["_id"]}, data_set)
        await ctx.send(f"Successfully completed push in {round(time.time()-start_time, 2)} seconds. Which affected 1 entries.")


@client.command(name="update-cases")
async def _update_cases_(ctx):
    if db.admins.find_one({"user": ctx.author.id}) == None:
        embed = await embed_gen(f"Permission Denied", f"You are not an admin, therefore not able to update cases. For any questions please refer to `iiVeil#0001`", "red")
        await ctx.author.send(embed=embed)
        return
    cases = ["Operation Wildfire Case", "Operation Hydra Case", "Spectrum Case", "Operation Bravo Case", "eSports 2013 Case", "eSports 2014 Summer Case", "eSports 2013 Winter Case", "CS:GO Weapon Case 2", "CS:GO Weapon Case 3", "CS:GO Weapon Case", "Falchion Case", "Chroma 2 Case", "Operation Breakout Weapon Case", "Huntsman Weapon Case", "Winter Offensive Weapon Case", "Operation Vanguard Weapon Case",
             "Revolver Case", "Chroma Case", "Shadow Case", "Chroma 3 Case", "Gamma Case", "Gamma 2 Case", "Shattered Web Case", "CS20 Case", "Glove Case", "Danger Zone Case", "Horizon Case", "Spectrum 2 Case", "Clutch Case", "Operation Broken Fang Case", "Snakebite Case", "Dreams & Nightmares Case", "Operation Riptide Case", "Fracture Case", "Operation Phoenix Weapon Case", "Prisma Case", "Prisma 2 Case"]
    for data_set in db["inventory"].find():
        print("hi")
        for case in cases:
            print("hi2")
            if case not in data_set["cases"]:
                print("hi3")
                data_set["cases"][case] = [0, 0]
        db["inventory"].replace_one({"_id": data_set["_id"]}, data_set)
    await ctx.send("Done.")


async def embed_gen(title, description, colorr):
    colours = {
        "red": 0xEE192D,
        "blue": 0x197ee3,
        "green": 0x15fb00,
        "purple": 0x6e00fb,
        "magenta": 0xf90871,
        "gold": 0xffba08,
        "orange": 0xfb8b00,
    }
    today = datetime.datetime.today()
    color = colours[colorr]
    embed = discord.Embed(color=color, title=title, description=description)
    hour = today.hour
    minute = today.minute
    second = today.second
    if len(str(hour)) == 1:
        hour = f'0{hour}'
    if len(str(minute)) == 1:
        minute = f'0{minute}'
    if len(str(second)) == 1:
        second = f'0{second}'
    embed.set_footer(
        text=f"COMMAND EXECUTED | {today.month}/{today.day}/{today.year} - {hour}:{minute}:{second}")
    return embed


client.run(open("token.txt", "r").read())