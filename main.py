import httpx,requests, gc,discord,time,calendar, traceback,threading, socks, random, json, tracemalloc, asyncio; from discord.utils import get;from discord import Member; from dotenv import load_dotenv; from discord.ext import commands
tracemalloc.start()

def get_members():
    config_file = open("members.json","r", encoding="utf8")
    configx = config_file.read()
    config_file.close()
    return configx

def get_config():
    config_file = open("config.json","r", encoding="utf8")
    configx = config_file.read()
    config_file.close()
    return configx

def get_prefix():
    config_file = get_config()
    config = json.loads(config_file)
    prefix = config['bot_config']["prefix"] 
    return prefix
    
config_file = get_config()
config = json.loads(config_file)
prefix = config['bot_config']["prefix"]
# token = config['bot_config']["token"]
token = getenv("TOKEN")

queue = []

load_dotenv()
intents = discord.Intents().all()
bot = commands.AutoShardedBot(command_prefix=get_prefix(), help_command=None, intents=intents)

def init():
    loop = asyncio.get_event_loop()
    loop.create_task(bot.run(token))
    threading.Thread(target=loop.run_forever).start()


@bot.command()
async def stock(ctx):
 if ctx.channel.type != discord.ChannelType.private:
        filefile = open('ttoken_follow.txt')
        fnum_lines = sum(1 for line in filefile)
        filefile.close()
        filefile = open('ttoken_spam.txt')
        snum_lines = sum(1 for line in filefile)
        filefile.close()
        embed=discord.Embed(title="Stock",color=16777215, description=f"Twitch Stock:\n \nSpam: **{snum_lines}**\nFollow: **{fnum_lines}** ")
        await ctx.send(embed=embed)
    
    
def get_id(user):

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"',
        'Accept-Language': 'en-US',
        'sec-ch-ua-mobile': '?0',
        'Client-Version': '7b9843d8-1916-4c86-aeb3-7850e2896464',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
        'Content-Type': 'text/plain;charset=UTF-8',
        'Client-Session-Id': '51789c1a5bf92c65',
        'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
        'X-Device-Id': 'xH9DusxeZ5JEV7wvmL8ODHLkDcg08Hgr',
        'sec-ch-ua-platform': '"Windows"',
        'Accept': '*/*',
        'Origin': 'https://www.twitch.tv',
        'Sec-Fetch-Site': 'same-site',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://www.twitch.tv/',
    }
    data = '[{"operationName": "WatchTrackQuery","variables": {"channelLogin": "'+user+'","videoID": null,"hasVideoID": false},"extensions": {"persistedQuery": {"version": 1,"sha256Hash": "38bbbbd9ae2e0150f335e208b05cf09978e542b464a78c2d4952673cd02ea42b"}}}]'
    try:
        response = httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data)
        id = response.json()[0]['data']['user']['id']
        return id
    except:
        return None

        
@bot.command()
async def help(ctx):
    print("x")
    config_file = get_config()
    json_object = json.loads(config_file)
    prefix = json_object['bot_config']["prefix"]
    print(f'{ctx.author} | {ctx.author.id} -> {prefix}help')
    if ctx.channel.type != discord.ChannelType.private:
            embed = discord.Embed(color=16777215)
            embed.add_field(name='Help', value=f'`{prefix}help`', inline=True)
            embed.add_field(name='Clear', value=f'`{prefix}clear`', inline=True)
            embed.add_field(name='Twitch Followers', value=f'`{prefix}tfollow (channel)`', inline=True)
            embed.add_field(name='Twitch Friend Requests', value=f'`{prefix}tfriend (channel)`', inline=True)
            embed.add_field(name='Twitch Spam', value=f'`{prefix}tspam (channel) (text)`', inline=True)
            embed.add_field(name='Stock', value=f'`{prefix}stock twitch`', inline=True)
            embed.add_field(name='Free Rank Bronze', value=f'`{prefix}bronze`', inline=True)
            
            await ctx.send(embed=embed)


@bot.command()
async def clear(ctx):
    print(f'{ctx.author} | {ctx.author.id} -> {bot.command_prefix}clear')
    if ctx.channel.type != discord.ChannelType.private:
        if ctx.author.guild_permissions.administrator:
            await ctx.channel.purge(limit=None)
            await ctx.send('😎')
        else:
            await ctx.message.delete()

@bot.command()
async def tfollow(ctx, arg):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel =json_object['bot_config']["twitch_channel"]
    if ctx.channel.id == int(genchannel):
        role_config = json.loads(config_file)['tfollow']
        for role_name in role_config:
            filefile = open("config.json","r", encoding="utf8")
            follow_count = json.loads(filefile.read())['tfollow'][role_name]
            filefile.close()
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:
                target_id = get_id(arg)
                if target_id == None:
                    embed=discord.Embed(color=6546546, description=f"➣ **ERROR** Invalid username {arg}")
                    await ctx.send(embed=embed, delete_after=5)
                    break
                else:
                    None
                filefile = open('ttoken_follow.txt')
                num_lines = sum(1 for line in filefile)
                filefile.close()
                
                filefile = open('ttoken_follow.txt', 'r')
                tokens = filefile.read().splitlines()
                filefile.close()
                
                if num_lines < follow_count:
                    
                    embed=discord.Embed(color=16777215, description=f"Adding **{num_lines}** follows to **{arg}**")
                    await ctx.send(embed=embed)
                    
                    caunt_to_follow = num_lines
                else:
                    
                    embed=discord.Embed(color=16777215, description=f"Adding **{follow_count}** Twitch Follows to **{arg}**")
                    await ctx.send(embed=embed)
                
                    caunt_to_follow = follow_count

                    
                class Follow():
                    sent = 0
                        
                def start_follow():

                        
                    for i in range(caunt_to_follow):
                        
                        try:
                            ttoken = tokens[i]
                            
                            payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]'
                            headers = {
                                            "Authorization": f"OAuth {ttoken}",
                                            "Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                                            "Content-Type": "application/json"
                                        }
                            
                            response = httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                        
                            
                            try:
                                if response.json()[0]['data']['followUser']['error']:
                                    with open("ttoken_follow.txt", "r") as f:
                                        lines = f.readlines()
                                    with open("ttoken_follow.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != ttoken:
                                                f.write(line)
                                                f.close()
                            except:
                                None
                            try:
                                
                                if response.json()[0]['error'] == "Unauthorized":
                                    with open("ttoken_follow.txt", "r") as f:
                                        lines = f.readlines()
                                        f.close()
                                    with open("ttoken_follow.txt", "w") as f:
                                        for line in lines:
                                            if line.strip("\n") != ttoken:
                                                f.write(line)
                                                f.close()
                            except:
                                None
                            try:
                                
                                if response.json()[0]['data']['followUser']['follow'] == None:
                                        None
                            except:
                                None
                            try:
                                if response.json()[0]['data']['followUser']['follow']['user']:
                                    Follow.sent = Follow.sent + 1
                            except:
                                None   
                        except:
                            None
                x = threading.Thread(target=start_follow)
                x.start()
                break
                

@bot.command()
async def tspam(ctx, arg1, *, args):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel = json_object['bot_config']["twitch_channel"]  
    if ctx.channel.id == int(genchannel): 
        role_config = json.loads(config_file)['tspam']
        for role_name in role_config:
            spam_count = json_object['tspam'][role_name]
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:    
                xfile = open('ttoken_spam.txt')
                num_lines = sum(1 for line in xfile)
                xfile.close()
                target_id = get_id(arg1)
                if target_id == None:
                    break
                else:
                    None
                def start_spam():
                    for i in range(20):
                        try:
                            filefile = open("ttoken_spam.txt")
                            ttoken = random.choice(filefile.read().splitlines())
                            filefile.close()
                            try:
                                payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"'+target_id+'\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]'
                                headers = {"Authorization": f"OAuth {ttoken}","Client-Id": 'kimne78kx3ncx6brgo4mv6wki5h1ko',"Content-Type": "application/json"}
                                httpx.post('https://gql.twitch.tv/gql', data=payload, headers=headers)
                            except:
                                None
                            def test_proxy():
                                while True:
                                    try:
                                        proxyfile = open("proxy.txt","r")
                                        proxy = random.choice(proxyfile.read().splitlines())
                                        proxyfile.close()
                                        session = requests.Session()
                                        proxies = {"https": f"http://{proxy}"}
                                        session.get("https://twitch.tv",proxies=proxies, timeout=5)
                                        return proxy
                                    except:
                                        None
                            headers = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36",'Authorization':f'OAuth {ttoken}'}
                            response = httpx.get("https://id.twitch.tv/oauth2/validate",headers=headers).json()
                            token_name = response['login']
                            proxy = test_proxy().split(":")
                            print(proxy)
                            s = socks.socksocket()
                            s.set_proxy(socks.HTTP, proxy[0],int(proxy[1]))
                            s.connect(("irc.chat.twitch.tv", 6667))
                            s.send("PASS {}\r\n".format("oauth:" + ttoken).encode("utf8"))
                            s.send("NICK {}\r\n".format(token_name).encode("utf8"))
                            s.send('CAP REQ :twitch.tv/membership\r\n'.encode('utf-8'))
                            s.send('CAP REQ :twitch.tv/commands twitch.tv/tags\r\n'.encode('utf-8'))
                            s.send("JOIN {}\r\n".format(arg1).encode("utf8"))
                            s.send(('PRIVMSG #' + arg1 + f' :/me {args} \r\n').encode('utf8'))
                            s.close()
                        except Exception as e:
                            print(e)
                            
                if num_lines < spam_count:
                    x = num_lines
                else:
                    x = spam_count
                            
                embed=discord.Embed(color=16777215, description=f"Sending **{x}** messages to **{arg1}**")
                await ctx.send(embed=embed)
                try:
                    for i in range(x):

                        threading.Thread(target=start_spam).start()
                except:
                    None
                break


            
@bot.command()
async def treport(ctx, arg):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel = json_object['bot_config']["twitch_channel"]
    
                
    if ctx.channel.id == int(genchannel): 
        
        role_config = json.loads(config_file)['treport']
        for role_name in role_config:
            spam_count = json.loads(config_file)['treport'][role_name]
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:    
                
                num_lines = sum(1 for line in open('ttoken_follow.txt'))
                target_id = get_id(arg)
                if target_id == None:
                    embed=discord.Embed(color=16777215, description=f"➣ **ERROR** Invalid username {arg}")
                    await ctx.send(embed=embed, delete_after=5)
                    break
                else:
                    None
                
                def start_spam(ttoken):
                    xcc = open("report.txt","r")
                    reportndescription = random.choice(xcc.read().splitlines())
                    xcc.close()
                    try:
                        headers = {
                            'Connection': 'keep-alive',
                            'Pragma': 'no-cache',
                            'Cache-Control': 'no-cache',
                            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                            'Accept-Language': 'en-US',
                            'sec-ch-ua-mobile': '?0',
                            'Client-Version': 'fde6b5a8-2aa2-45b1-85d5-5036951737cc',
                            'Authorization': f'OAuth {ttoken}',
                            'Content-Type': 'text/plain;charset=UTF-8',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
                            'Client-Session-Id': '32193c1413662035',
                            'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                            'X-Device-Id': 'O1MrFLwPyZ2byJzoLFT0K5XNlORNRQ9F',
                            'sec-ch-ua-platform': '"Windows"',
                            'Accept': '*/*',
                            'Origin': 'https://www.twitch.tv',
                            'Sec-Fetch-Site': 'same-site',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Dest': 'empty',
                            'Referer': 'https://www.twitch.tv/',
                        }

                        data = '[{"operationName":"ReportUserModal_ReportUser","variables":{"input":{"description":"report context: USER_REPORT\\n\\nvideo > terrorism_mass_violence\\n\\ndescription: '+reportndescription+'","reason":"terrorism_mass_violence","content":"LIVESTREAM_REPORT","contentID":"","extra":"","targetID":"'+target_id+'","wizardPath":["video","terrorism_mass_violence"]}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"dd2b8f6a76ee54aff685c91537fd75814ffdc732a74d3ae4b8f2474deabf26fc"}}}]'

                        httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data).text

                    except:
                        None
                            
                            
                embed=discord.Embed(color=16777215, description=f"Sending **{spam_count}** reports to **{arg}**")
                await ctx.send(embed=embed)
                if num_lines < spam_count:
                    x = num_lines
                else:
                    x = spam_count
                    
                try:
                    
                    for i in range(x):
                        c = open("ttoken_follow.txt")
                        ttoken = random.choice(c.read().splitlines())
                        threading.Thread(target=start_spam,args=(ttoken,)).start()
                        c.close()
                        
                except:
                    None
                break
    
@bot.command()
async def tfriend(ctx, arg):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel = json_object['bot_config']["twitch_channel"]  

    if ctx.channel.id == int(genchannel): 
        role_config = json.loads(config_file)['tfriend']
        for role_name in role_config:
            spam_count = json.loads(config_file)['tfriend'][role_name]
            role_id = discord.utils.get(ctx.guild.roles, name=role_name)
            if role_id in ctx.author.roles:    
                filefile = open('ttoken_follow.txt')
                num_lines = sum(1 for line in filefile)
                filefile.close()
                target_id = get_id(arg)
                if target_id == None:
                    embed=discord.Embed(color=16777215, description=f"➣ **ERROR** Invalid username {arg}")
                    await ctx.send(embed=embed, delete_after=5)
                    break
                else:
                    None
                
                
                def start_spam(ttoken):
                    
                    try:
                        headers = {
                            'Connection': 'keep-alive',
                            'Pragma': 'no-cache',
                            'Cache-Control': 'no-cache',
                            'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                            'Accept-Language': 'en-US',
                            'sec-ch-ua-mobile': '?0',
                            'Client-Version': 'fde6b5a8-2aa2-45b1-85d5-5036951737cc',
                            'Authorization': f'OAuth {ttoken}',
                            'Content-Type': 'text/plain;charset=UTF-8',
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36',
                            'Client-Session-Id': '99ef7e05659bbca4',
                            'Client-Id': 'kimne78kx3ncx6brgo4mv6wki5h1ko',
                            'X-Device-Id': 'O1MrFLwPyZ2byJzoLFT0K5XNlORNRQ9F',
                            'sec-ch-ua-platform': '"Windows"',
                            'Accept': '*/*',
                            'Origin': 'https://www.twitch.tv',
                            'Sec-Fetch-Site': 'same-site',
                            'Sec-Fetch-Mode': 'cors',
                            'Sec-Fetch-Dest': 'empty',
                            'Referer': 'https://www.twitch.tv/',
                        }

                        data = '[{"operationName":"FriendButton_CreateFriendRequest","variables":{"input":{"targetID":"'+target_id+'"}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"380d8b19fcffef2fd8654e524444055dbca557d71968044115849d569d24129a"}}}]'

                        httpx.post('https://gql.twitch.tv/gql', headers=headers, data=data)

                    except:
                        None 
                embed=discord.Embed(color=16777215, description=f"Sending **{spam_count}** friends to **{arg}**")
                await ctx.send(embed=embed)
                if num_lines < spam_count:
                    x = num_lines
                else:
                    x = spam_count
                try:
                    for i in range(x):
                        xx = open("ttoken_follow.txt").read()
                        ttoken = random.choice(xx.splitlines())
                        threading.Thread(target=start_spam,args=(ttoken,)).start()
                except:
                    None
                break


@bot.command()
async def bronze(ctx):
 if ctx.channel.type != discord.ChannelType.private:
    config_file = get_config()
    json_object = json.loads(config_file)
    genchannel = json_object['bot_config']["twitch_channel"]
    embed=discord.Embed(title="Free Bronze",color=16777215, description=f"**set .gg/JTG in status, you will automatically get a rank Bronze**")
    await ctx.send(embed=embed)




@bot.event
async def on_member_update(before, after):
    role_id = 922780377427353640
    role = get(before.guild.roles, id=role_id)
    if '.gg/JTG' in str(before.activities):
      if '.gg/JTG' in str(after.activities):
        pass
      else:
        await after.remove_roles(role)
        channel = bot.get_channel(933209028010577940)
        embed=discord.Embed(description=f"Bronze has been removed from {after.mention}", color=discord.Color.red())
        await channel.send(embed=embed)

    if '.gg/JTG' in str(after.activities):
        await after.add_roles(role)
        channel = bot.get_channel(933209028010577940)
        embed=discord.Embed(description=f"{after.mention} has claimed Bronze!", color=discord.Color.green())
        await channel.send(embed=embed)

bot.run(token)
