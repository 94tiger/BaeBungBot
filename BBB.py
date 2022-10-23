import discord
from discord import app_commands
from pytz import timezone
from datetime import datetime
import random
import logging
# import openpyxl
import game_stat
import gegle
import config


logging.basicConfig(level=logging.INFO, filename="log.log", filemode="a",
                    format="[%(asctime)s] [%(levelname)-8s] %(message)s",
                    datefmt='%Y-%m-%d %H:%M:%S')


def time_now():
    now = datetime.now(timezone('Asia/Seoul'))
    return now


class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents = discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        logging.info(f'{self.user}이 시작되었습니다')  #  봇이 시작하였을때 터미널에 뜨는 말
        game = discord.Game('배붕봇')          # ~~ 하는중
        await self.change_presence(status=discord.Status.idle, activity=game)


client = aclient()
tree = app_commands.CommandTree(client)
interaction: discord.Interaction


# 명령어 확인
@tree.command(name = '명령어', description='봇 명령어 안내')
async def 명령어(interaction: discord.Interaction):
    command_msg = ("```md\n"
                   "# 기본\n"
                   "* /명령어 - 봇 명령어 안내\n"
                   "* /정보 - 멤버 자신의 정보를 보여줍니다.\n"
                   "# 선택 \n"
                   "* /골라 [1 2 3 ...] - 1,2,3랜덤 선택\n"
                   "* /뭐먹지 - 메뉴 랜덤 \n"
                   "* /주사위 [굴릴 주사위]\n"
                   "# 기능 \n"
                   # "* /경마 [1 2 3 ...] - 1 2 3 경마 \n"/
                   # "* /전적 [배그아이디] [솔로|듀오|스쿼드|1솔로|1듀오|1스쿼드] - 배그 전적 검색 (dak.gg 기준 / 갱신 x)\n"
                   # "* /배그 [배그아이디] [솔로|듀오|스쿼드] - 배그 전적 검색 (pubg.op.gg 기준 / 갱신 o)\n"
                   "* /롤 [롤아이디] - 롤 전적 검색 (fow.kr 기준 / 갱신 x)\n"
                   "* /롤체 [롤체아이디] - 롤체 전적 검색 (lolchess.gg 기준 / 갱신 x)\n"
                   # "# /커뮤니티\n"
                   "* /념글 [힛갤|이슈줌|중갤|롤갤|돌갤|야갤] - 최신 개념글 목록\n"
                   "* /개드립 - 최신 개드립 목록 \n"
                   # "# 서버 \n"
                   # "* /해제 - 지옥 탈출"
                   "```")
    await interaction.response.send_message(command_msg, ephemeral = True)
    logging.info(f"{interaction.user.display_name} - 명령어 사용 ")


# @tree.command(name = '시간', description='시간')
# async def 시간(interaction):
#     now = time_now()
#     await interaction.response.send_message(now, ephemeral = False)


@tree.command(name = '정보', description='멤버 자신의 정보를 보여줍니다.')
async def 정보(interaction):
    # member: discord.Member
    # Discord 가입일
    # print(member.joined_at)
    joined_at = interaction.user.joined_at.strftime("%Y년 %m월 %d일 %R")

    # 서버 가입일
    created_at = interaction.user.created_at.strftime("%Y년 %m월 %d일 %R")

    # 역할 리스트
    roles = interaction.user.roles
    role_list = ' '
    for i in roles:
        if i.name != "@everyone":
            role_list += str(i.mention) + " "

    embed_userinfo = discord.Embed(color=0xdc6363)
    embed_userinfo.set_thumbnail(url=interaction.user.avatar)
    embed_userinfo.add_field(name="Discord 가입일", value=created_at, inline=True)
    embed_userinfo.add_field(name="서버 가입일", value=joined_at, inline=True)
    embed_userinfo.add_field(name="역할", value=role_list, inline=False)

    await interaction.response.send_message(embed=embed_userinfo, ephemeral=False)
    logging.info(f"{interaction.user.display_name} - 정보 사용 ")


@tree.command(name='골라', description='입력한 항목중에서 무작위로 한개를 골라줍니다.')
@app_commands.describe(항목='항목을 입력하세요. (공백으로 구분합니다.)')
async def 골라(interaction: discord.Interaction, 항목: str):
    choice = str(항목).split(" ")
    choiceNum = random.randint(0, len(choice) - 1)
    choiceResult = choice[choiceNum]
    await interaction.response.send_message("`" +interaction.user.display_name + "`님의 선택은 __**" + choiceResult + "**__ 입니다.", ephemeral=False)
    # await ctx.send("`" + ctx.author.display_name + "`님의 선택은 __**" + choiceResult + "**__ 입니다.")
    logging.info(f"{interaction.user.display_name} - 골라 사용 - {choiceResult} of {choice}")


@tree.command(name='뭐먹지', description='음식 메뉴를 골라줍니다.')
async def 뭐먹지(interaction : discord.Interaction):
    food = config.food
    food_choice = food.split(" ")
    food_num = random.randint(0, len(food_choice) - 1)
    food_result = food_choice[food_num]
    print(food_result)
    await interaction.response.send_message(food_result)
    logging.info(f"{interaction.user.display_name} - 뭐먹지 사용 - {food_result}")


# 롤 전적 확인
@tree.command(name='롤', description='롤 전적을 보여줍니다. (fow기반)')
@app_commands.describe(닉네임='소환사명')
async def 롤(interaction : discord.Interaction, 닉네임: str):
    now = time_now()

    stat = game_stat.get_lol_stat3(닉네임)
    # [계정상태, 프로필이미지링크, 티어아이콘링크, 순위, 랭크타입, 현재티어, 점수, 승급전, 승패승률]

    embed_stat = discord.Embed(color=0xdc6363, timestamp=now)
    # 대체 이미지 https://opgg-static.akamaized.net/images/site/about/img-logo-opgg.png
    if stat[0] == 0:
        embed_stat.set_author(name=닉네임, url="https://fow.kr/find/" + 닉네임)
        embed_stat.add_field(name="No User", value="그런 이름의 사용자는 없습니다.")
    else:
        embed_stat.set_author(name=닉네임, url="https://fow.kr/find/" + 닉네임, icon_url="https:" + stat[1])
        embed_stat.set_footer(text="from fow.kr", icon_url="https://z.fow.kr/fowkr_logo_small.png")
        if stat[0] == 2:
            embed_stat.set_thumbnail(url="https:" + stat[2])
            # embed_stat.add_field(name="소환사레벨", value=stat[2], inline=True)
            # embed_stat.add_field(name="랭크타입", value=stat[4], inline=True)
            embed_stat.add_field(name="현재티어", value=stat[5] + " " + stat[6], inline=False)
            embed_stat.add_field(name="순위", value=stat[3], inline=False)
            embed_stat.add_field(name="승패", value=stat[8], inline=False)
        elif stat[0] == 1:
            embed_stat.add_field(name="Unranked", value="랭크 전적이 존재하지 않는 유저입니다.")
    # embed_stat.add_field(name="최근전적", value=stat[0])

    await interaction.response.send_message(embed=embed_stat, ephemeral=False)
    logging.info(f"{interaction.user.display_name} - 롤 사용 - {닉네임}")



# 롤체 전적 확인
@tree.command(name='롤체', description='롤체 전적을 보여줍니다.')
@app_commands.describe(닉네임='소환사명')
async def 롤체(interaction : discord.Interaction, 닉네임: str):
    now = time_now()
    stat = game_stat.get_lolchess_stat(닉네임)
    # stat = [랭크유무, 프로필이미지링크, 티어아이콘링크, 티어, 승수, 승률, top4, top비율, 게임수, 평균등수]

    embed_stat = discord.Embed(color=0xdc6363, timestamp=now)
    embed_stat.set_author(name=닉네임, url="https://lolchess.gg/profile/kr/" + 닉네임, icon_url=stat[1])
    embed_stat.set_footer(text="from LOLCHESS.GG",
                          icon_url="https://lolchess.gg/images/leaderboards/ico-tier-placeholder.png")
    # 대체 이미지 https://opgg-static.akamaized.net/images/site/about/img-logo-opgg.png
    embed_stat.set_thumbnail(url=stat[2])
    if stat[0]:
        embed_stat.add_field(name="티어", value=stat[3], inline=False)
        embed_stat.add_field(name="승리", value=stat[4], inline=True)
        embed_stat.add_field(name="승률", value=stat[5], inline=True)
        embed_stat.add_field(name="TOP 4", value=stat[6], inline=True)
        embed_stat.add_field(name="TOP 4 비율", value=stat[7], inline=True)
        embed_stat.add_field(name="게임수", value=stat[8], inline=True)
        embed_stat.add_field(name="평균 등수", value=stat[9], inline=True)
    else:
        embed_stat.add_field(name="Unranked", value="랭크 전적이 존재하지 않는 유저입니다.")

    await interaction.response.send_message(embed=embed_stat, ephemeral=False)
    logging.info(f"{interaction.user.display_name} - 롤체 사용 - {닉네임}. {stat[3]}")


# 개념글 확인
@tree.command(name='념글', description='DCinside 개념글을 보여줍니다.')
@app_commands.describe(갤러리='검색할 DCinside 갤러리')
@app_commands.choices(갤러리=[
    discord.app_commands.Choice(name="힛갤", value="hit"),
    discord.app_commands.Choice(name="이슈줌", value="issuezoom"),
    discord.app_commands.Choice(name="중갤", value="aoegame"),
    discord.app_commands.Choice(name="돌갤", value="pebble"),
    discord.app_commands.Choice(name="야갤", value="baseball_new11"),
    discord.app_commands.Choice(name="롤갤", value="leagueoflegends4")
])
async def 념글(interaction: discord.Interaction, 갤러리: discord.app_commands.Choice[str]):
    gallery_str = 갤러리.value
    gallery_name = 갤러리.name

    gegl = gegle.get_gegle(gallery_str)
    gegl_value: str = ""
    for i in range(len(gegl)):
        gegl_value = gegl_value + "{}. [{} [{}]]({}) \n".format(i+1, gegl[i][0], gegl[i][1], gegl[i][2])
    embed_gegl = discord.Embed(color=0xdc6363)
    embed_gegl.add_field(name=gallery_name + " 개념글", value=gegl_value, inline=False)
    await interaction.response.send_message(embed=embed_gegl, ephemeral=False)
    logging.info(f"{interaction.user.display_name} - 념글 사용 - {갤러리}")


# 개드립 확인
@tree.command(name='개드립', description='Dogdrip.net 개드립을 보여줍니다.')
async def 개드립(interaction : discord.Interaction):
    try:
        gegl = gegle.get_dogdrip()
        gegl_value: str = ""
        for i in range(len(gegl)):
            gegl_value = gegl_value + "{}. [{} [{}]]({}) \n".format(i+1, gegl[i][0], gegl[i][1], gegl[i][2])
        embed_gegl = discord.Embed(color=0xdc6363)
        embed_gegl.add_field(name="개드립", value=gegl_value, inline=False)
        await interaction.response.send_message(embed=embed_gegl, ephemeral=False)
    except:
        await interaction.response.send_message("전송 실패", ephemeral=False)
    logging.info(f"{interaction.user.display_name} - 개드립 사용")
    

client.run(config.TOKEN1)

# TEST 용 토큰
# client.run(config.TOKEN1)