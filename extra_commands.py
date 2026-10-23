import asyncio
import datetime
import json
import random
import urllib.request

import discord
from discord import app_commands
from discord.ext import commands as ext_commands

STARTED_AT = datetime.datetime.now(datetime.timezone.utc)
WARNINGS: dict[int, list[str]] = {}

GUIDE: dict[str, dict[str, str]] = {
    "help": {"cat": "شرح", "short": "يعرض أقسام الأوامر.", "how": "اكتب `/help`."},
    "guide": {"cat": "شرح", "short": "يشرح أمر معيّن بالتفصيل.", "how": "اكتب `/guide` واختر اسم الأمر من القائمة."},
    "commands": {"cat": "شرح", "short": "يعرض كل الأوامر مجمّعة.", "how": "اكتب `/commands`."},
    "ping": {"cat": "معلومات", "short": "سرعة استجابة البوت.", "how": "`/ping`"},
    "botinfo": {"cat": "معلومات", "short": "معلومات عن البوت ووقت تشغيله.", "how": "`/botinfo`"},
    "uptime": {"cat": "معلومات", "short": "كم صار للبوت شغال.", "how": "`/uptime`"},
    "userinfo": {"cat": "معلومات", "short": "معلومات عضو.", "how": "`/userinfo member:`"},
    "member": {"cat": "معلومات", "short": "تفاصيل عضو من السيرفر.", "how": "`/member user:`"},
    "serverinfo": {"cat": "معلومات", "short": "إحصائيات السيرفر.", "how": "`/serverinfo`"},
    "avatar": {"cat": "معلومات", "short": "صورة العضو.", "how": "`/avatar member:`"},
    "banner": {"cat": "معلومات", "short": "بنر العضو إن وجد.", "how": "`/banner member:`"},
    "icon": {"cat": "معلومات", "short": "أيقونة السيرفر.", "how": "`/icon`"},
    "id": {"cat": "معلومات", "short": "يعرض آيدي عضو أو روم.", "how": "`/id member:` أو `/id channel:`"},
    "channelinfo": {"cat": "معلومات", "short": "معلومات الروم الحالي.", "how": "`/channelinfo`"},
    "roleinfo": {"cat": "معلومات", "short": "معلومات رتبة.", "how": "`/roleinfo role:`"},
    "roles": {"cat": "معلومات", "short": "قائمة رتب السيرفر.", "how": "`/roles`"},
    "emojis": {"cat": "معلومات", "short": "قائمة إيموجي السيرفر.", "how": "`/emojis`"},
    "boosters": {"cat": "معلومات", "short": "من يعزّز السيرفر.", "how": "`/boosters`"},
    "membercount": {"cat": "معلومات", "short": "عدد الأعضاء والبوتات.", "how": "`/membercount`"},
    "mods": {"cat": "معلومات", "short": "الأعضاء اللي عندهم إدارة.", "how": "`/mods`"},
    "bots": {"cat": "معلومات", "short": "البوتات في السيرفر.", "how": "`/bots`"},
    "permissions": {"cat": "معلومات", "short": "صلاحيات عضو في الروم.", "how": "`/permissions member:`"},
    "firstmessage": {"cat": "معلومات", "short": "أول رسالة في الروم.", "how": "`/firstmessage`"},
    "invite": {"cat": "معلومات", "short": "يصنع دعوة مؤقتة.", "how": "`/invite` يحتاج صلاحية إنشاء دعوات."},
    "scan": {"cat": "إدارة", "short": "يفحص صلاحيات البوت وإعداد السيرفر.", "how": "`/scan` للإدارة."},
    "clear": {"cat": "إدارة", "short": "يحذف 1 إلى 100 رسالة.", "how": "`/clear amount:20`"},
    "clearall": {"cat": "إدارة", "short": "يمسح الروم بعد تأكيد.", "how": "`/clearall` ثم تأكيد."},
    "purgeuser": {"cat": "إدارة", "short": "يحذف رسائل عضو معيّن من آخر 100.", "how": "`/purgeuser member:`"},
    "ban": {"cat": "إدارة", "short": "يحظر عضو.", "how": "`/ban member: reason:`"},
    "unban": {"cat": "إدارة", "short": "يفك الحظر بالآيدي.", "how": "`/unban user_id:`"},
    "softban": {"cat": "إدارة", "short": "حظر ثم فك فوري لمسح الرسائل.", "how": "`/softban member:`"},
    "kick": {"cat": "إدارة", "short": "يطرد عضو.", "how": "`/kick member:`"},
    "timeout": {"cat": "إدارة", "short": "إسكات بالدقائق.", "how": "`/timeout member: minutes:`"},
    "untimeout": {"cat": "إدارة", "short": "يفك التايم أوت.", "how": "`/untimeout member:`"},
    "warn": {"cat": "إدارة", "short": "يعطي تحذير (ذاكرة مؤقتة).", "how": "`/warn member: reason:`"},
    "warnings": {"cat": "إدارة", "short": "يعرض تحذيرات عضو.", "how": "`/warnings member:`"},
    "nickname": {"cat": "إدارة", "short": "يغيّر لقب عضو.", "how": "`/nickname member: name:`"},
    "addrole": {"cat": "إدارة", "short": "يعطي رتبة.", "how": "`/addrole member: role:`"},
    "removerole": {"cat": "إدارة", "short": "يشيل رتبة.", "how": "`/removerole member: role:`"},
    "lock": {"cat": "إدارة", "short": "يقفل الروم.", "how": "`/lock`"},
    "unlock": {"cat": "إدارة", "short": "يفتح الروم.", "how": "`/unlock`"},
    "hide": {"cat": "إدارة", "short": "يخفي الروم عن الأعضاء.", "how": "`/hide`"},
    "unhide": {"cat": "إدارة", "short": "يظهر الروم.", "how": "`/unhide`"},
    "slowmode": {"cat": "إدارة", "short": "الوضع البطيء بالثواني.", "how": "`/slowmode seconds:5`"},
    "topic": {"cat": "إدارة", "short": "يغيّر موضوع الروم.", "how": "`/topic text:`"},
    "say": {"cat": "إدارة", "short": "يرسل البوت رسالة.", "how": "`/say message:`"},
    "announce": {"cat": "إدارة", "short": "إعلان بإيمبد.", "how": "`/announce title: text:`"},
    "poll": {"cat": "أدوات", "short": "تصويت سريع.", "how": "`/poll question: خيار1 خيار2` افصل الخيارات بـ |"},
    "remind": {"cat": "أدوات", "short": "تذكير بعد دقائق.", "how": "`/remind minutes:10 text:`"},
    "choose": {"cat": "أدوات", "short": "يختار من قائمة.", "how": "`/choose options: أ | ب | ج`"},
    "reverse": {"cat": "أدوات", "short": "يعكس النص.", "how": "`/reverse text:`"},
    "embed": {"cat": "أدوات", "short": "يرسل إيمبد مخصص.", "how": "`/embed title: desc:`"},
    "timestamp": {"cat": "أدوات", "short": "وقت ديسكورد منسّق.", "how": "`/timestamp`"},
    "calc": {"cat": "أدوات", "short": "نسبة مئوية.", "how": "`/calc part: total:`"},
    "add": {"cat": "أدوات", "short": "جمع رقمين.", "how": "`/add a: b:`"},
    "subtract": {"cat": "أدوات", "short": "طرح رقمين.", "how": "`/subtract a: b:`"},
    "multiply": {"cat": "أدوات", "short": "ضرب رقمين.", "how": "`/multiply a: b:`"},
    "divide": {"cat": "أدوات", "short": "قسمة رقمين.", "how": "`/divide a: b:`"},
    "randomcolor": {"cat": "أدوات", "short": "لون عشوائي.", "how": "`/randomcolor`"},
    "enlarge": {"cat": "أدوات", "short": "يكبّر إيموجي مخصص.", "how": "`/enlarge emoji:`"},
    "base64": {"cat": "أدوات", "short": "تشفير أو فك Base64.", "how": "`/base64 mode:encode text:`"},
    "mock": {"cat": "أدوات", "short": "نص متداخل حروف.", "how": "`/mock text:`"},
    "clap": {"cat": "أدوات", "short": "يحط 👏 بين الكلمات.", "how": "`/clap text:`"},
    "spoiler": {"cat": "أدوات", "short": "يخفي النص كحرق.", "how": "`/spoiler text:`"},
    "coinflip": {"cat": "تسلية", "short": "عملة.", "how": "`/coinflip`"},
    "dice": {"cat": "تسلية", "short": "نرد.", "how": "`/dice sides:6`"},
    "rps": {"cat": "تسلية", "short": "حجر ورقة مقص.", "how": "`/rps choice:`"},
    "eightball": {"cat": "تسلية", "short": "كرة الحظ.", "how": "`/eightball question:`"},
    "joke": {"cat": "تسلية", "short": "نكتة قصيرة.", "how": "`/joke`"},
    "fact": {"cat": "تسلية", "short": "معلومة عشوائية.", "how": "`/fact`"},
    "advice": {"cat": "تسلية", "short": "نصيحة عشوائية.", "how": "`/advice`"},
    "rate": {"cat": "تسلية", "short": "تقييم شيء من 100.", "how": "`/rate thing:`"},
    "ship": {"cat": "تسلية", "short": "نسبة توافق بين شخصين.", "how": "`/ship one: two:`"},
    "compliment": {"cat": "تسلية", "short": "مجاملة.", "how": "`/compliment member:`"},
    "hug": {"cat": "تسلية", "short": "حضن.", "how": "`/hug member:`"},
    "pat": {"cat": "تسلية", "short": "ربتة.", "how": "`/pat member:`"},
    "slap": {"cat": "تسلية", "short": "صفعة مزاح.", "how": "`/slap member:`"},
    "iq": {"cat": "تسلية", "short": "ذكاء مزحي.", "how": "`/iq member:`"},
    "howcool": {"cat": "تسلية", "short": "كم الشخص كول.", "how": "`/howcool member:`"},
}


def _http_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "b7nawybot"})
    with urllib.request.urlopen(req, timeout=8) as resp:
        return json.loads(resp.read().decode("utf-8"))


def register(bot: ext_commands.Bot):
    tree = bot.tree

    async def guide_complete(interaction: discord.Interaction, current: str):
        current = current.lower()
        matches = [name for name in sorted(GUIDE) if current in name]
        return [app_commands.Choice(name=name, value=name) for name in matches[:25]]

    @tree.command(name="guide", description="شرح تفصيلي لأي أمر")
    @app_commands.describe(command="اسم الأمر بدون /")
    @app_commands.autocomplete(command=guide_complete)
    async def guide(interaction: discord.Interaction, command: str):
        item = GUIDE.get(command.lower())
        if not item:
            await interaction.response.send_message("ما أعرف هذا الأمر. جرّب `/commands`.", ephemeral=True)
            return
        embed = discord.Embed(title=f"/{command}", color=discord.Color.green())
        embed.add_field(name="القسم", value=item["cat"], inline=True)
        embed.add_field(name="وش يسوي", value=item["short"], inline=False)
        embed.add_field(name="كيف تستخدمه", value=item["how"], inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tree.command(name="commands", description="كل أوامر البوت")
    async def commands_list(interaction: discord.Interaction):
        groups: dict[str, list[str]] = {}
        for name, item in GUIDE.items():
            groups.setdefault(item["cat"], []).append(f"`/{name}`")
        embed = discord.Embed(
            title=f"كل الأوامر ({len(GUIDE)})",
            description="للتفاصيل: `/guide`",
            color=discord.Color.blurple(),
        )
        for cat, names in groups.items():
            embed.add_field(name=cat, value=" ".join(names), inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tree.command(name="botinfo", description="معلومات البوت")
    async def botinfo(interaction: discord.Interaction):
        embed = discord.Embed(title="b7nawybot", color=discord.Color.green())
        embed.add_field(name="السيرفرات", value=str(len(bot.guilds)), inline=True)
        embed.add_field(name="الأوامر", value=str(len(GUIDE)), inline=True)
        embed.add_field(name="البنج", value=f"{round(bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="التشغيل منذ", value=discord.utils.format_dt(STARTED_AT, "R"), inline=False)
        await interaction.response.send_message(embed=embed)

    @tree.command(name="uptime", description="مدة تشغيل البوت")
    async def uptime(interaction: discord.Interaction):
        await interaction.response.send_message(f"شغال من {discord.utils.format_dt(STARTED_AT, 'R')}")

    @tree.command(name="banner", description="بنر عضو")
    async def banner(interaction: discord.Interaction, member: discord.Member | None = None):
        member = member or interaction.user
        user = await bot.fetch_user(member.id)
        if not user.banner:
            await interaction.response.send_message("ما عنده بنر.", ephemeral=True)
            return
        embed = discord.Embed(title=f"بنر {member.display_name}", color=discord.Color.purple())
        embed.set_image(url=user.banner.url)
        await interaction.response.send_message(embed=embed)

    @tree.command(name="icon", description="أيقونة السيرفر")
    async def icon(interaction: discord.Interaction):
        if not interaction.guild or not interaction.guild.icon:
            await interaction.response.send_message("ما فيه أيقونة.", ephemeral=True)
            return
        embed = discord.Embed(title=interaction.guild.name, color=discord.Color.green())
        embed.set_image(url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed)

    @tree.command(name="id", description="آيدي عضو أو روم")
    async def show_id(
        interaction: discord.Interaction,
        member: discord.Member | None = None,
        channel: discord.abc.GuildChannel | None = None,
    ):
        parts = [f"أنت: `{interaction.user.id}`"]
        if member:
            parts.append(f"{member.mention}: `{member.id}`")
        if channel:
            parts.append(f"{channel.mention}: `{channel.id}`")
        if interaction.guild:
            parts.append(f"السيرفر: `{interaction.guild.id}`")
        await interaction.response.send_message("\n".join(parts), ephemeral=True)

    @tree.command(name="channelinfo", description="معلومات الروم")
    async def channelinfo(interaction: discord.Interaction):
        ch = interaction.channel
        embed = discord.Embed(title="معلومات الروم", color=discord.Color.teal())
        embed.add_field(name="الاسم", value=getattr(ch, "mention", str(ch)), inline=True)
        embed.add_field(name="الآيدي", value=f"`{ch.id}`", inline=True)
        embed.add_field(name="النوع", value=ch.__class__.__name__, inline=True)
        created = getattr(ch, "created_at", None)
        if created:
            embed.add_field(name="الإنشاء", value=discord.utils.format_dt(created, "F"), inline=False)
        await interaction.response.send_message(embed=embed)

    @tree.command(name="roleinfo", description="معلومات رتبة")
    async def roleinfo(interaction: discord.Interaction, role: discord.Role):
        embed = discord.Embed(title=role.name, color=role.color or discord.Color.blue())
        embed.add_field(name="الآيدي", value=f"`{role.id}`", inline=True)
        embed.add_field(name="الأعضاء", value=str(len(role.members)), inline=True)
        embed.add_field(name="المنشن", value="نعم" if role.mentionable else "لا", inline=True)
        embed.add_field(name="الإنشاء", value=discord.utils.format_dt(role.created_at, "D"), inline=False)
        await interaction.response.send_message(embed=embed)

    @tree.command(name="roles", description="رتب السيرفر")
    async def roles(interaction: discord.Interaction):
        guild = interaction.guild
        names = [role.mention for role in reversed(guild.roles) if role != guild.default_role][:40]
        await interaction.response.send_message(" ".join(names) or "ما فيه رتب.", ephemeral=True)

    @tree.command(name="emojis", description="إيموجي السيرفر")
    async def emojis(interaction: discord.Interaction):
        em = list(interaction.guild.emojis)[:40]
        text = " ".join(str(e) for e in em) or "ما فيه إيموجي."
        await interaction.response.send_message(text, ephemeral=True)

    @tree.command(name="boosters", description="المعززون")
    async def boosters(interaction: discord.Interaction):
        people = interaction.guild.premium_subscribers
        text = "\n".join(m.mention for m in people[:30]) or "ما فيه عزز."
        await interaction.response.send_message(
            f"المستوى: {interaction.guild.premium_tier}\nالعزز: {interaction.guild.premium_subscription_count}\n{text}"
        )

    @tree.command(name="membercount", description="عدد الأعضاء")
    async def membercount(interaction: discord.Interaction):
        humans = sum(1 for m in interaction.guild.members if not m.bot)
        bots_n = sum(1 for m in interaction.guild.members if m.bot)
        await interaction.response.send_message(
            f"الكل: **{interaction.guild.member_count}** · بشر: **{humans}** · بوتات: **{bots_n}**"
        )

    @tree.command(name="mods", description="قائمة المشرفين")
    async def mods(interaction: discord.Interaction):
        mods_list = [
            m.mention
            for m in interaction.guild.members
            if m.guild_permissions.manage_guild or m.guild_permissions.administrator
        ][:25]
        await interaction.response.send_message(" ".join(mods_list) or "ما لقيت.", ephemeral=True)

    @tree.command(name="bots", description="بوتات السيرفر")
    async def bots_cmd(interaction: discord.Interaction):
        names = [m.mention for m in interaction.guild.members if m.bot][:30]
        await interaction.response.send_message(" ".join(names) or "ما فيه بوتات.", ephemeral=True)

    @tree.command(name="permissions", description="صلاحيات عضو هنا")
    async def permissions(interaction: discord.Interaction, member: discord.Member | None = None):
        member = member or interaction.user
        perms = interaction.channel.permissions_for(member)
        important = [
            "manage_messages",
            "ban_members",
            "kick_members",
            "manage_channels",
            "administrator",
            "mention_everyone",
        ]
        lines = [f"{'✅' if getattr(perms, name) else '❌'} `{name}`" for name in important]
        await interaction.response.send_message("\n".join(lines), ephemeral=True)

    @tree.command(name="firstmessage", description="أول رسالة في الروم")
    async def firstmessage(interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        msg = None
        async for item in interaction.channel.history(limit=1, oldest_first=True):
            msg = item
        if not msg:
            await interaction.followup.send("ما لقيت رسائل.", ephemeral=True)
            return
        await interaction.followup.send(f"أول رسالة: {msg.jump_url}", ephemeral=True)

    @tree.command(name="invite", description="إنشاء دعوة")
    @app_commands.checks.has_permissions(create_instant_invite=True)
    @app_commands.checks.bot_has_permissions(create_instant_invite=True)
    async def invite(interaction: discord.Interaction):
        link = await interaction.channel.create_invite(max_age=3600, max_uses=5, unique=True)
        await interaction.response.send_message(f"دعوة ساعة واحدة / 5 استخدامات:\n{link}", ephemeral=True)

    @tree.command(name="purgeuser", description="حذف رسائل عضو من آخر 100")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def purgeuser(interaction: discord.Interaction, member: discord.Member):
        await interaction.response.defer(ephemeral=True)
        deleted = await interaction.channel.purge(limit=100, check=lambda m: m.author.id == member.id)
        await interaction.followup.send(f"انحذف **{len(deleted)}** رسالة من {member.mention}.", ephemeral=True)

    @tree.command(name="softban", description="حظر ثم فك فوري")
    @app_commands.checks.has_permissions(ban_members=True)
    @app_commands.checks.bot_has_permissions(ban_members=True)
    async def softban(interaction: discord.Interaction, member: discord.Member, reason: str = "سوفت بان"):
        await member.ban(reason=reason, delete_message_days=1)
        await interaction.guild.unban(member)
        await interaction.response.send_message(f"تم سوفت بان {member.mention}.")

    @tree.command(name="warn", description="تحذير عضو")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = "بدون سبب"):
        WARNINGS.setdefault(member.id, []).append(f"{interaction.user}: {reason}")
        await interaction.response.send_message(
            f"تحذير لـ {member.mention} ({len(WARNINGS[member.id])}) | {reason}"
        )

    @tree.command(name="warnings", description="عرض التحذيرات")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def warnings(interaction: discord.Interaction, member: discord.Member):
        items = WARNINGS.get(member.id, [])
        text = "\n".join(f"{i+1}. {w}" for i, w in enumerate(items[-10:])) or "ما عنده تحذيرات."
        await interaction.response.send_message(text, ephemeral=True)

    @tree.command(name="nickname", description="تغيير لقب عضو")
    @app_commands.checks.has_permissions(manage_nicknames=True)
    @app_commands.checks.bot_has_permissions(manage_nicknames=True)
    async def nickname(interaction: discord.Interaction, member: discord.Member, name: str):
        await member.edit(nick=name[:32])
        await interaction.response.send_message(f"لقب {member.mention} صار **{name[:32]}**.")

    @tree.command(name="addrole", description="إعطاء رتبة")
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    async def addrole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        await member.add_roles(role, reason=str(interaction.user))
        await interaction.response.send_message(f"أعطيت {member.mention} رتبة {role.mention}.")

    @tree.command(name="removerole", description="إزالة رتبة")
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.bot_has_permissions(manage_roles=True)
    async def removerole(interaction: discord.Interaction, member: discord.Member, role: discord.Role):
        await member.remove_roles(role, reason=str(interaction.user))
        await interaction.response.send_message(f"شلت {role.mention} من {member.mention}.")

    @tree.command(name="hide", description="إخفاء الروم")
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    async def hide(interaction: discord.Interaction):
        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message("روم نصي فقط.", ephemeral=True)
            return
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.view_channel = False
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("تم إخفاء الروم.")

    @tree.command(name="unhide", description="إظهار الروم")
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    async def unhide(interaction: discord.Interaction):
        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message("روم نصي فقط.", ephemeral=True)
            return
        overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
        overwrite.view_channel = True
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
        await interaction.response.send_message("تم إظهار الروم.")

    @tree.command(name="topic", description="تغيير موضوع الروم")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def topic(interaction: discord.Interaction, text: str):
        if not isinstance(interaction.channel, discord.TextChannel):
            await interaction.response.send_message("روم نصي فقط.", ephemeral=True)
            return
        await interaction.channel.edit(topic=text[:1024])
        await interaction.response.send_message("تم تحديث الموضوع.")

    @tree.command(name="announce", description="إعلان بإيمبد")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def announce(interaction: discord.Interaction, title: str, text: str):
        embed = discord.Embed(title=title[:256], description=text[:4000], color=discord.Color.green())
        embed.set_footer(text=f"من {interaction.user}")
        await interaction.response.send_message(embed=embed)

    @tree.command(name="poll", description="تصويت")
    async def poll(interaction: discord.Interaction, question: str, options: str):
        parts = [p.strip() for p in options.split("|") if p.strip()][:9]
        if len(parts) < 2:
            await interaction.response.send_message("اكتب خيارين على الأقل مفصولين بـ |", ephemeral=True)
            return
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
        body = "\n".join(f"{emojis[i]} {part}" for i, part in enumerate(parts))
        embed = discord.Embed(title=question[:256], description=body, color=discord.Color.blurple())
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        for i in range(len(parts)):
            await message.add_reaction(emojis[i])

    @tree.command(name="remind", description="تذكير بعد دقائق")
    async def remind(interaction: discord.Interaction, minutes: app_commands.Range[int, 1, 720], text: str):
        await interaction.response.send_message(f"بأذكّرك بعد **{minutes}** دقيقة.", ephemeral=True)

        async def later():
            await asyncio.sleep(minutes * 60)
            try:
                await interaction.followup.send(f"تذكير {interaction.user.mention}: {text[:300]}", ephemeral=True)
            except discord.HTTPException:
                pass

        asyncio.create_task(later())

    @tree.command(name="choose", description="اختيار عشوائي")
    async def choose(interaction: discord.Interaction, options: str):
        parts = [p.strip() for p in options.replace(",", "|").split("|") if p.strip()]
        if len(parts) < 2:
            await interaction.response.send_message("اكتب خيارين مفصولين بـ |", ephemeral=True)
            return
        await interaction.response.send_message(f"اختار: **{random.choice(parts)}**")

    @tree.command(name="reverse", description="عكس نص")
    async def reverse(interaction: discord.Interaction, text: str):
        await interaction.response.send_message(text[::-1][:1800])

    @tree.command(name="embed", description="إيمبد مخصص")
    async def embed_cmd(interaction: discord.Interaction, title: str, desc: str):
        embed = discord.Embed(title=title[:256], description=desc[:4000], color=discord.Color.green())
        await interaction.response.send_message(embed=embed)

    @tree.command(name="timestamp", description="وقت ديسكورد الحالي")
    async def timestamp(interaction: discord.Interaction):
        now = discord.utils.utcnow()
        await interaction.response.send_message(
            f"{discord.utils.format_dt(now, 'F')}\nكود: `<t:{int(now.timestamp())}:F>`",
            ephemeral=True,
        )

    @tree.command(name="add", description="جمع")
    async def add(interaction: discord.Interaction, a: float, b: float):
        await interaction.response.send_message(f"{a} + {b} = **{a + b}**")

    @tree.command(name="subtract", description="طرح")
    async def subtract(interaction: discord.Interaction, a: float, b: float):
        await interaction.response.send_message(f"{a} - {b} = **{a - b}**")

    @tree.command(name="multiply", description="ضرب")
    async def multiply(interaction: discord.Interaction, a: float, b: float):
        await interaction.response.send_message(f"{a} × {b} = **{a * b}**")

    @tree.command(name="divide", description="قسمة")
    async def divide(interaction: discord.Interaction, a: float, b: float):
        if b == 0:
            await interaction.response.send_message("ما ينفع القسمة على صفر.", ephemeral=True)
            return
        await interaction.response.send_message(f"{a} ÷ {b} = **{a / b}**")

    @tree.command(name="randomcolor", description="لون عشوائي")
    async def randomcolor(interaction: discord.Interaction):
        value = random.randint(0, 0xFFFFFF)
        color = discord.Color(value)
        embed = discord.Embed(title=f"#{value:06X}", color=color)
        await interaction.response.send_message(embed=embed)

    @tree.command(name="enlarge", description="تكبير إيموجي")
    async def enlarge(interaction: discord.Interaction, emoji: str):
        custom = discord.PartialEmoji.from_str(emoji)
        if custom.id:
            url = f"https://cdn.discordapp.com/emojis/{custom.id}.{'gif' if custom.animated else 'png'}"
            embed = discord.Embed(color=discord.Color.green())
            embed.set_image(url=url)
            await interaction.response.send_message(embed=embed)
            return
        await interaction.response.send_message("أرسل إيموجي سيرفر مخصص.", ephemeral=True)

    @tree.command(name="base64", description="Base64")
    @app_commands.describe(mode="encode أو decode")
    @app_commands.choices(mode=[
        app_commands.Choice(name="encode", value="encode"),
        app_commands.Choice(name="decode", value="decode"),
    ])
    async def base64_cmd(interaction: discord.Interaction, mode: app_commands.Choice[str], text: str):
        import base64

        try:
            if mode.value == "encode":
                result = base64.b64encode(text.encode()).decode()
            else:
                result = base64.b64decode(text.encode()).decode()
        except Exception:
            await interaction.response.send_message("ما قدرت أحوّل النص.", ephemeral=True)
            return
        await interaction.response.send_message(f"```{result[:1800]}```")

    @tree.command(name="mock", description="نص متداخل")
    async def mock(interaction: discord.Interaction, text: str):
        out = "".join(ch.upper() if i % 2 else ch.lower() for i, ch in enumerate(text))
        await interaction.response.send_message(out[:1800])

    @tree.command(name="clap", description="👏 بين الكلمات")
    async def clap(interaction: discord.Interaction, text: str):
        await interaction.response.send_message(" 👏 ".join(text.split())[:1800])

    @tree.command(name="spoiler", description="إخفاء كنص محروق")
    async def spoiler(interaction: discord.Interaction, text: str):
        await interaction.response.send_message(f"||{text[:1800]}||")

    @tree.command(name="coinflip", description="عملة")
    async def coinflip(interaction: discord.Interaction):
        await interaction.response.send_message(random.choice(["وجه", "كتابة"]))

    @tree.command(name="dice", description="نرد")
    async def dice(interaction: discord.Interaction, sides: app_commands.Range[int, 2, 100] = 6):
        await interaction.response.send_message(f"النتيجة: **{random.randint(1, sides)}** / {sides}")

    @tree.command(name="rps", description="حجر ورقة مقص")
    @app_commands.choices(choice=[
        app_commands.Choice(name="حجر", value="حجر"),
        app_commands.Choice(name="ورقة", value="ورقة"),
        app_commands.Choice(name="مقص", value="مقص"),
    ])
    async def rps(interaction: discord.Interaction, choice: app_commands.Choice[str]):
        bot_pick = random.choice(["حجر", "ورقة", "مقص"])
        wins = {("حجر", "مقص"), ("ورقة", "حجر"), ("مقص", "ورقة")}
        if choice.value == bot_pick:
            result = "تعادل"
        elif (choice.value, bot_pick) in wins:
            result = "فزت"
        else:
            result = "خسرت"
        await interaction.response.send_message(f"أنت {choice.value} · البوت {bot_pick} · **{result}**")

    @tree.command(name="eightball", description="كرة الحظ")
    async def eightball(interaction: discord.Interaction, question: str):
        answers = ["نعم", "لا", "يمكن", "بعدين", "أكيد", "مستحيل", "اسأل بعد شوي", "الإشارات تقول نعم"]
        await interaction.response.send_message(f"**{question[:200]}**\n{random.choice(answers)}")

    @tree.command(name="joke", description="نكتة")
    async def joke(interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            data = await asyncio.to_thread(_http_json, "https://official-joke-api.appspot.com/random_joke")
            await interaction.followup.send(f"{data.get('setup')}\n**{data.get('punchline')}**")
        except Exception:
            await interaction.followup.send("ما قدرت أجيب نكتة الحين.")

    @tree.command(name="fact", description="معلومة")
    async def fact(interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            data = await asyncio.to_thread(
                _http_json, "https://uselessfacts.jsph.pl/api/v2/facts/random?language=en"
            )
            await interaction.followup.send(data.get("text", "ما قدرت."))
        except Exception:
            await interaction.followup.send("ما قدرت أجيب معلومة الحين.")

    @tree.command(name="advice", description="نصيحة")
    async def advice(interaction: discord.Interaction):
        await interaction.response.defer()
        try:
            data = await asyncio.to_thread(_http_json, "https://api.adviceslip.com/advice")
            await interaction.followup.send(data.get("slip", {}).get("advice", "خذ نفس."))
        except Exception:
            await interaction.followup.send("خذ نفس وكمل.")

    @tree.command(name="rate", description="تقييم من 100")
    async def rate(interaction: discord.Interaction, thing: str):
        await interaction.response.send_message(f"**{thing[:80]}** تقييمه: **{random.randint(0, 100)}/100**")

    @tree.command(name="ship", description="توافق")
    async def ship(interaction: discord.Interaction, one: discord.Member, two: discord.Member):
        score = random.randint(1, 100)
        await interaction.response.send_message(f"{one.mention} + {two.mention} = **{score}%**")

    @tree.command(name="compliment", description="مجاملة")
    async def compliment(interaction: discord.Interaction, member: discord.Member | None = None):
        member = member or interaction.user
        lines = ["وجودك يرفع السيرفر", "ذوقك واضح", "شخص مرتب", "تستاهل خير"]
        await interaction.response.send_message(f"{member.mention} {random.choice(lines)}")

    @tree.command(name="hug", description="حضن")
    async def hug(interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f"{interaction.user.mention} حضن {member.mention}")

    @tree.command(name="pat", description="ربتة")
    async def pat(interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f"{interaction.user.mention} ربت على {member.mention}")

    @tree.command(name="slap", description="صفعة مزاح")
    async def slap(interaction: discord.Interaction, member: discord.Member):
        await interaction.response.send_message(f"{interaction.user.mention} صفع {member.mention} بمزاح")

    @tree.command(name="iq", description="ذكاء مزحي")
    async def iq(interaction: discord.Interaction, member: discord.Member | None = None):
        member = member or interaction.user
        await interaction.response.send_message(f"IQ {member.mention}: **{random.randint(70, 160)}** (مزح)")

    @tree.command(name="howcool", description="كم كول")
    async def howcool(interaction: discord.Interaction, member: discord.Member | None = None):
        member = member or interaction.user
        await interaction.response.send_message(f"{member.mention} كول بنسبة **{random.randint(1, 100)}%**")
