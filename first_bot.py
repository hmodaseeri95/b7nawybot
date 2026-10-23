import asyncio
import datetime
import logging
import os
from threading import Thread

import discord
from discord import app_commands
from discord.ext import commands
from flask import Flask, render_template

from extra_commands import GUIDE, register as register_extra_commands

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("b7nawybot")

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/health")
def health():
    return {"status": "ok", "bot": getattr(bot.user, "name", None)}, 200


def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, use_reloader=False)


intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)
register_extra_commands(bot)


def is_text_channel(channel) -> bool:
    return isinstance(channel, (discord.TextChannel, discord.Thread))


def moderation_block_reason(
    actor: discord.Member,
    target: discord.Member,
    me: discord.Member,
) -> str | None:
    if target.id == actor.id:
        return "ما تقدر تطبق الأمر على نفسك."
    if target.id == me.id:
        return "ما أقدر أطبق الأمر على نفسي."
    if target.id == actor.guild.owner_id:
        return "ما ينفع تطبيق الأمر على صاحب السيرفر."
    if target.top_role >= me.top_role:
        return "رتبة هذا العضو أعلى من رتبتي أو مساوية لها. ارفع رتبة البوت فوقه."
    if actor.id != actor.guild.owner_id and target.top_role >= actor.top_role:
        return "رتبة هذا العضو أعلى من رتبتك أو مساوية لها."
    return None


async def safe_followup(interaction: discord.Interaction, content: str, ephemeral: bool = True):
    if interaction.response.is_done():
        await interaction.followup.send(content, ephemeral=ephemeral)
    else:
        await interaction.response.send_message(content, ephemeral=ephemeral)


@bot.event
async def on_ready():
    log.info("Logged in as %s (%s)", bot.user, bot.user.id if bot.user else "?")
    try:
        guild_id = os.environ.get("GUILD_ID")
        if guild_id:
            guild = discord.Object(id=int(guild_id))
            bot.tree.copy_global_to(guild=guild)
            synced = await bot.tree.sync(guild=guild)
            log.info("Synced %s guild commands to %s", len(synced), guild_id)
        else:
            synced = await bot.tree.sync()
            log.info("Synced %s global commands", len(synced))
    except Exception:
        log.exception("Failed to sync slash commands")
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="/guide")
    )


@bot.tree.error
async def on_app_command_error(
    interaction: discord.Interaction, error: app_commands.AppCommandError
):
    if isinstance(error, app_commands.MissingPermissions):
        missing = ", ".join(error.missing_permissions)
        await safe_followup(interaction, f"ما عندك صلاحية: `{missing}`")
        return
    if isinstance(error, app_commands.BotMissingPermissions):
        missing = ", ".join(error.missing_permissions)
        await safe_followup(interaction, f"البوت ناقصه صلاحية: `{missing}`")
        return
    if isinstance(error, app_commands.CommandOnCooldown):
        await safe_followup(interaction, f" Slow down. جرّب بعد {error.retry_after:.1f} ثانية.")
        return
    log.exception("Slash command error: %s", error)
    await safe_followup(interaction, "صار خطأ غير متوقع. جرّب مرة ثانية بعد شوي.")


@bot.command(name="count_below")
@commands.has_permissions(manage_messages=True)
async def count_below(ctx: commands.Context):
    if not ctx.message.reference:
        await ctx.reply("رد على رسالة ثم اكتب `!count_below`.")
        return

    try:
        replied = await ctx.channel.fetch_message(ctx.message.reference.message_id)
    except discord.NotFound:
        await ctx.reply("ما لقيت الرسالة اللي رديت عليها.")
        return

    count = 0
    async for _ in ctx.channel.history(limit=500, after=replied):
        count += 1

    actual = max(count - 1, 0)
    extra = ""
    if count >= 500:
        extra = "\nتنبيه: وقفت العد عند 500 رسالة."
    await ctx.reply(
        f"فيه **{actual}** رسالة تحت الرسالة المحددة.\n"
        f"للحذف استخدم `/clear` بعدد مناسب (حد أقصى 100 في كل مرة).{extra}"
    )


@count_below.error
async def count_below_error(ctx: commands.Context, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.reply("تحتاج صلاحية Manage Messages.")
        return
    await ctx.reply(f"ما قدرت أعد الرسائل: {error}")


@bot.tree.command(name="help", description="قائمة أوامر البوت")
async def help_command(interaction: discord.Interaction):
    embed = discord.Embed(
        title="أوامر البوت",
        description=(
            f"عدد الأوامر: **{len(GUIDE)}**\n"
            "كل القائمة: `/commands`\n"
            "شرح أمر واحد: `/guide` واختر الاسم.\n"
            "عد الرسائل بالرد: `!count_below`"
        ),
        color=discord.Color.blurple(),
    )
    embed.add_field(name="شرح", value="`/help` `/guide` `/commands`", inline=False)
    embed.add_field(name="إدارة", value="`/clear` `/clearall` `/ban` `/kick` `/timeout` `/warn` `/lock`", inline=False)
    embed.add_field(name="معلومات", value="`/ping` `/userinfo` `/serverinfo` `/botinfo`", inline=False)
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="scan", description="فحص إعدادات السيرفر والصلاحيات")
@app_commands.checks.has_permissions(manage_guild=True)
async def scan(interaction: discord.Interaction):
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("هذا الأمر للسيرفرات فقط.", ephemeral=True)
        return

    me = guild.me
    needed = {
        "Manage Messages": me.guild_permissions.manage_messages,
        "Ban Members": me.guild_permissions.ban_members,
        "Kick Members": me.guild_permissions.kick_members,
        "Moderate Members": me.guild_permissions.moderate_members,
        "Manage Channels": me.guild_permissions.manage_channels,
        "View Audit Log": me.guild_permissions.view_audit_log,
    }
    missing = [name for name, ok in needed.items() if not ok]
    role_ok = bool(me.top_role and me.top_role.position > 1)

    embed = discord.Embed(title=f"فحص سيرفر {guild.name}", color=discord.Color.teal())
    embed.add_field(name="الأعضاء", value=str(guild.member_count), inline=True)
    embed.add_field(name="مستوى التحقق", value=str(guild.verification_level), inline=True)
    embed.add_field(name="رتبة البوت", value=me.top_role.mention if me.top_role else "—", inline=True)
    embed.add_field(
        name="صلاحيات البوت الناقصة",
        value="لا يوجد" if not missing else "\n".join(f"- {item}" for item in missing),
        inline=False,
    )
    embed.add_field(
        name="ملاحظة الرتب",
        value="رتبة البوت مرتفعة كفاية." if role_ok else "ارفع رتبة البوت فوق الأعضاء اللي تبي تديرهم.",
        inline=False,
    )
    await interaction.response.send_message(embed=embed, ephemeral=True)


@bot.tree.command(name="member", description="عرض معلومات عضو من السيرفر")
async def member_info(interaction: discord.Interaction, user: discord.Member):
    embed = discord.Embed(title=f"عضو: {user.display_name}", color=user.color or discord.Color.blue())
    embed.set_thumbnail(url=user.display_avatar.url)
    embed.add_field(name="الاسم", value=str(user), inline=True)
    embed.add_field(name="الآيدي", value=str(user.id), inline=True)
    embed.add_field(name="بوت؟", value="نعم" if user.bot else "لا", inline=True)
    if user.joined_at:
        embed.add_field(name="انضم", value=discord.utils.format_dt(user.joined_at, "f"), inline=False)
    embed.add_field(name="أنشأ الحساب", value=discord.utils.format_dt(user.created_at, "f"), inline=False)
    roles = [role.mention for role in user.roles if role != interaction.guild.default_role][-10:]
    embed.add_field(name="الرتب", value=" ".join(reversed(roles)) or "بدون رتب", inline=False)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="clear", description="حذف عدد معين من الرسائل (1-100)")
@app_commands.describe(amount="عدد الرسائل للحذف، من 1 إلى 100")
@app_commands.checks.has_permissions(manage_messages=True)
@app_commands.checks.bot_has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
    if not is_text_channel(interaction.channel):
        await interaction.response.send_message("هذا الأمر للشات النصي فقط.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(f"تم حذف **{len(deleted)}** رسالة.", ephemeral=True)


class ConfirmClearAll(discord.ui.View):
    def __init__(self, author_id: int):
        super().__init__(timeout=30)
        self.author_id = author_id
        self.confirmed: bool | None = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("هذا الزر مو لك.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="تأكيد مسح الروم", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, _button: discord.ui.Button):
        self.confirmed = True
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(content="جاري مسح الروم...", view=self)
        self.stop()

    @discord.ui.button(label="إلغاء", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, _button: discord.ui.Button):
        self.confirmed = False
        for item in self.children:
            item.disabled = True
        await interaction.response.edit_message(content="تم إلغاء المسح.", view=self)
        self.stop()


@bot.tree.command(name="clearall", description="مسح كل رسائل الروم الحالي")
@app_commands.checks.has_permissions(manage_messages=True)
@app_commands.checks.bot_has_permissions(manage_messages=True)
async def clearall(interaction: discord.Interaction):
    if not is_text_channel(interaction.channel):
        await interaction.response.send_message("هذا الأمر للشات النصي فقط.", ephemeral=True)
        return

    view = ConfirmClearAll(interaction.user.id)
    await interaction.response.send_message(
        "هذا بيمسح **كل رسائل الروم**. الرسائل الأقدم من 14 يوم تنحذف واحدة واحدة وقد تاخذ وقت.\n"
        "تأكد إنك في الروم الصح، بعدين اضغط تأكيد.",
        view=view,
        ephemeral=True,
    )
    await view.wait()
    if view.confirmed is not True:
        return

    channel = interaction.channel
    deleted_count = 0
    old_count = 0

    while True:
        batch = await channel.purge(limit=100)
        if not batch:
            break
        deleted_count += len(batch)
        if deleted_count >= 5000:
            await interaction.followup.send(
                f"وقفت عند **{deleted_count}** رسالة عشان ما يطول الأمر زيادة. شغّل `/clearall` مرة ثانية لإكمال الباقي.",
                ephemeral=True,
            )
            return
        await asyncio.sleep(1)

    leftovers = [message async for message in channel.history(limit=100)]
    while leftovers:
        for message in leftovers:
            try:
                await message.delete()
                old_count += 1
            except discord.HTTPException:
                continue
            await asyncio.sleep(0.7)
            if deleted_count + old_count >= 5000:
                await interaction.followup.send(
                    f"تم حذف **{deleted_count + old_count}** رسالة ووقفت عند الحد. شغّل `/clearall` مرة ثانية لإكمال الباقي.",
                    ephemeral=True,
                )
                return
        leftovers = [message async for message in channel.history(limit=100)]

    total = deleted_count + old_count
    await interaction.followup.send(f"تم مسح الروم. انحذف **{total}** رسالة.", ephemeral=True)


@bot.tree.command(name="calc", description="حساب النسبة المئوية: كم part من total؟")
@app_commands.describe(part="الجزء", total="الكل")
async def calc(interaction: discord.Interaction, part: float, total: float):
    if total == 0:
        await interaction.response.send_message("ما ينفع القسمة على صفر.", ephemeral=True)
        return
    percentage = (part / total) * 100
    await interaction.response.send_message(f"النسبة: **{percentage:.2f}%**")


@bot.tree.command(name="ban", description="حظر عضو من السيرفر")
@app_commands.describe(member="العضو", reason="السبب", delete_days="حذف رسائله لآخر كم يوم (0-7)")
@app_commands.checks.has_permissions(ban_members=True)
@app_commands.checks.bot_has_permissions(ban_members=True)
async def ban(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str = "لا يوجد سبب",
    delete_days: app_commands.Range[int, 0, 7] = 0,
):
    block = moderation_block_reason(interaction.user, member, interaction.guild.me)
    if block:
        await interaction.response.send_message(block, ephemeral=True)
        return
    await member.ban(reason=reason, delete_message_days=delete_days)
    await interaction.response.send_message(f"تم حظر {member.mention} | السبب: {reason}")


@bot.tree.command(name="unban", description="إلغاء حظر عضو بالآيدي")
@app_commands.describe(user_id="آيدي المستخدم المحظور")
@app_commands.checks.has_permissions(ban_members=True)
@app_commands.checks.bot_has_permissions(ban_members=True)
async def unban(interaction: discord.Interaction, user_id: str):
    if not user_id.isdigit():
        await interaction.response.send_message("أرسل آيدي رقمي صحيح.", ephemeral=True)
        return
    user = discord.Object(id=int(user_id))
    try:
        await interaction.guild.unban(user)
    except discord.NotFound:
        await interaction.response.send_message("هذا المستخدم مو محظور أو الآيدي غلط.", ephemeral=True)
        return
    await interaction.response.send_message(f"تم إلغاء الحظر عن `{user_id}`.")


@bot.tree.command(name="kick", description="طرد عضو من السيرفر")
@app_commands.describe(member="العضو", reason="السبب")
@app_commands.checks.has_permissions(kick_members=True)
@app_commands.checks.bot_has_permissions(kick_members=True)
async def kick(
    interaction: discord.Interaction,
    member: discord.Member,
    reason: str = "لا يوجد سبب",
):
    block = moderation_block_reason(interaction.user, member, interaction.guild.me)
    if block:
        await interaction.response.send_message(block, ephemeral=True)
        return
    await member.kick(reason=reason)
    await interaction.response.send_message(f"تم طرد {member.mention} | السبب: {reason}")


@bot.tree.command(name="timeout", description="إسكات عضو لمدة بالدقائق")
@app_commands.describe(member="العضو", minutes="المدة بالدقائق (1 إلى 40320 = 28 يوم)", reason="السبب")
@app_commands.checks.has_permissions(moderate_members=True)
@app_commands.checks.bot_has_permissions(moderate_members=True)
async def timeout(
    interaction: discord.Interaction,
    member: discord.Member,
    minutes: app_commands.Range[int, 1, 40320],
    reason: str = "لا يوجد سبب",
):
    block = moderation_block_reason(interaction.user, member, interaction.guild.me)
    if block:
        await interaction.response.send_message(block, ephemeral=True)
        return
    until = discord.utils.utcnow() + datetime.timedelta(minutes=minutes)
    await member.timeout(until, reason=reason)
    await interaction.response.send_message(
        f"تايم أوت لـ {member.mention} لمدة **{minutes}** دقيقة | السبب: {reason}"
    )


@bot.tree.command(name="untimeout", description="إزالة التايم أوت عن عضو")
@app_commands.checks.has_permissions(moderate_members=True)
@app_commands.checks.bot_has_permissions(moderate_members=True)
async def untimeout(interaction: discord.Interaction, member: discord.Member):
    await member.timeout(None)
    await interaction.response.send_message(f"تم فك التايم أوت عن {member.mention}.")


@bot.tree.command(name="lock", description="قفل الروم الحالي")
@app_commands.checks.has_permissions(manage_channels=True)
@app_commands.checks.bot_has_permissions(manage_channels=True)
async def lock(interaction: discord.Interaction):
    channel = interaction.channel
    if not isinstance(channel, discord.TextChannel):
        await interaction.response.send_message("هذا الأمر للرومات النصية فقط.", ephemeral=True)
        return
    overwrite = channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    await interaction.response.send_message("تم قفل الروم.")


@bot.tree.command(name="unlock", description="فتح الروم الحالي")
@app_commands.checks.has_permissions(manage_channels=True)
@app_commands.checks.bot_has_permissions(manage_channels=True)
async def unlock(interaction: discord.Interaction):
    channel = interaction.channel
    if not isinstance(channel, discord.TextChannel):
        await interaction.response.send_message("هذا الأمر للرومات النصية فقط.", ephemeral=True)
        return
    overwrite = channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    await interaction.response.send_message("تم فتح الروم.")


@bot.tree.command(name="slowmode", description="تعيين الوضع البطيء بالثواني (0 للإلغاء)")
@app_commands.describe(seconds="0 إلى 21600")
@app_commands.checks.has_permissions(manage_channels=True)
@app_commands.checks.bot_has_permissions(manage_channels=True)
async def slowmode(interaction: discord.Interaction, seconds: app_commands.Range[int, 0, 21600]):
    if not isinstance(interaction.channel, discord.TextChannel):
        await interaction.response.send_message("هذا الأمر للرومات النصية فقط.", ephemeral=True)
        return
    await interaction.channel.edit(slowmode_delay=seconds)
    if seconds == 0:
        await interaction.response.send_message("تم إلغاء الوضع البطيء.")
    else:
        await interaction.response.send_message(f"الوضع البطيء الآن **{seconds}** ثانية.")


@bot.tree.command(name="say", description="يرسل البوت رسالة في الروم (للإدارة)")
@app_commands.describe(message="النص")
@app_commands.checks.has_permissions(manage_messages=True)
async def say(interaction: discord.Interaction, message: str):
    if not is_text_channel(interaction.channel):
        await interaction.response.send_message("هذا الأمر للشات النصي فقط.", ephemeral=True)
        return
    await interaction.response.send_message("تم الإرسال.", ephemeral=True)
    await interaction.channel.send(message[:2000])


@bot.tree.command(name="ping", description="سرعة استجابة البوت")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"السرعة: `{latency}ms`")


@bot.tree.command(name="userinfo", description="معلومات عنك أو عن عضو آخر")
async def userinfo(interaction: discord.Interaction, member: discord.Member | None = None):
    target = member or interaction.user
    embed = discord.Embed(title=f"معلومات: {target.display_name}", color=discord.Color.blue())
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.add_field(name="الاسم", value=str(target), inline=True)
    embed.add_field(name="الآيدي", value=str(target.id), inline=True)
    if isinstance(target, discord.Member) and target.joined_at:
        embed.add_field(
            name="انضم للسيرفر",
            value=discord.utils.format_dt(target.joined_at, "D"),
            inline=False,
        )
    embed.add_field(
        name="إنشاء الحساب",
        value=discord.utils.format_dt(target.created_at, "D"),
        inline=False,
    )
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="serverinfo", description="معلومات السيرفر")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    if guild is None:
        await interaction.response.send_message("هذا الأمر للسيرفرات فقط.", ephemeral=True)
        return

    owner = guild.owner.mention if guild.owner else f"`{guild.owner_id}`"
    embed = discord.Embed(title=f"سيرفر {guild.name}", color=discord.Color.green())
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="المالك", value=owner, inline=True)
    embed.add_field(name="الأعضاء", value=str(guild.member_count), inline=True)
    embed.add_field(name="الإنشاء", value=discord.utils.format_dt(guild.created_at, "D"), inline=False)
    embed.add_field(name="الرومات", value=str(len(guild.channels)), inline=True)
    embed.add_field(name="الرتب", value=str(len(guild.roles)), inline=True)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="avatar", description="عرض الصورة الشخصية")
async def avatar(interaction: discord.Interaction, member: discord.Member | None = None):
    target = member or interaction.user
    embed = discord.Embed(title=f"أفاتار {target.display_name}", color=discord.Color.purple())
    embed.set_image(url=target.display_avatar.url)
    await interaction.response.send_message(embed=embed)


if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    if not token:
        raise SystemExit("DISCORD_TOKEN غير موجود. أضفه في متغيرات Render أو البيئة المحلية.")

    web_thread = Thread(target=run_web, daemon=True)
    web_thread.start()
    bot.run(token)
