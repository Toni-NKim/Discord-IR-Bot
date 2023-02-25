import discord
from discord.ext import commands
from news_update import fetch_ir, alt_fetch_ir

#Bot token
bot_token = 'MTA3ODY3MzI3MzgwNzcyMDY0NQ.GQihde.t4Sq4Xwfc9yUDtLXZM7pjiTt4UEC12R3uug3cA'

#Set up bot
intents = discord.Intents.all()
intents.messages = True
bot = commands.Bot(command_prefix='$', case_insensitive=True, intents=intents)


#String to add in front of links if https not present
net_default = 'https://'

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name='Money Never Sleeps'))

@bot.command(name='안녕')
async def Hi(ctx):
    await ctx.send('```안녕하세요. 저는 IR 자료를 긁어와 보여주는 봇입니다. 기업명 앞에 $를 붙이고 메시지를 보내보세요.```')
    await bot.process_commands(ctx) 

#Fetch Joby News
@bot.command(aliases=['조비'])
async def Joby(ctx):
    ir_url = 'https://ir.jobyaviation.com/news-events/press-releases'
    soup = fetch_ir(ir_url)
    
    #Select newest article
    newest = soup.select_one('.media-body')
    ir_link = soup.select_one('.media-body > h2 > a').get('href')
    
    #Make a list containing date, title and link
    elements = [element.text.strip() for element in newest if element.text != '\n']
    elements.append(ir_link)
    
    #Assign values from the list and send the message
    date, title, link = [i for i in elements]
    await ctx.send(f'{date}\n{title}\n{link}')
    await bot.process_commands(ctx)

#Fetch Lucid news
@bot.command(aliases=['루시드'])
async def Lucid(ctx):
    soup = fetch_ir('https://ir.lucidmotors.com/press-releases')

    newest = soup.select_one('.nir-widget--list > div > div > div')
    link = net_default + 'ir.lucidmotors.com' + soup.select_one('.nir-widget--list > div > div > div > h4 > a').get('href') + '/'

    # #Make a list containing date, title and link
    elements = [element.text.strip() for element in newest if element.text != '\n']
    elements.append(link)
    
    #Assign values from the list and send the message
    date, title, link = [i for i in elements]
    await ctx.send(f'{date}\n{title}\n{link}')
    await bot.process_commands(ctx)

#Fetch NVIDIA news
@bot.command(aliases=['엔비디아'])
async def NVIDIA(ctx):
    soup = alt_fetch_ir('https://blogs.nvidia.com/')

    newest = soup.select('div > div > div > article > div')
    articles = []

    for item in newest:
        for sub in item.select('div > div > a'):
            link = sub.get('href')
            title = sub.get('title')
            if 'category' not in link:
                articles.append([link, title])
    
    #Assign values from the list and send the message
    for item in articles:
        link, title = item[0], item[1]
        await ctx.send(f'{title}\n{link}')
    await bot.process_commands(ctx)

# @bot.command(aliases=['아이온큐'])
# async def IonQ(ctx):
#     ir_url = 'https://investors.ionq.com/news/default.aspx'
#     soup = fetch_ir(ir_url)
    
#     #Select newest article
#     newest = soup.select_one('.module_item')
#     link = soup.select_one('.module_item > .module_headline-link > a').get('href')
    
#     #Make a list containing date, title and link
#     elements = [element.text.strip() for element in newest if element.text != '\n']
#     elements.append(link)
    
#     #Assign values from the list and send the message
#     date, title, link = [i for i in elements]
#     await ctx.send(f'{date}\n{title}\n{link}')
#     await bot.process_commands(ctx)

bot.run(bot_token)