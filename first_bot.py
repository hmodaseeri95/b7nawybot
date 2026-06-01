import discord
from discord import app_commands
from discord.ext import commands
import socket
import requests
import os
from flask import Flask, render_template
from threading import Thread
import datetime # تمت إضافته لخصائص التايم أوت

# إعداد الويب (الكود الأصلي)
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# إعداد البوت (الكود الأصلي)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'=== المساعد السيبراني {bot.user} يعمل الآن ===')

# ==========================================
# 🎯 الأمر المخصص الجديد: عد الرسائل للحذف
# ==========================================
@bot.command(name="count_below")
async def count_below(ctx):
    # للتحقق من أن المستخدم قام بعمل Reply على رسالة
    if not ctx.message.reference:
        await ctx.reply("⚠️ يرجى الرد (Reply) على رسالة وكتابة هذا الأمر لمعرفة عدد الرسائل تحتها.")
        return

    try:
        # جلب الرسالة الأصلية التي تم الرد عليها
        replied_message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        
        count = 0
        # حساب كل الرسائل التي أتت بعد تلك الرسالة
        async for msg in ctx.channel.history(limit=None, after=replied_message):
            count += 1
            
        # نطرح 1 (وهي رسالة الأمر !count_below التي كتبتها أنت للتو) لكي نعطيك العدد الدقيق للرسائل المقصودة
        actual_count = count - 1 if count > 0 else 0
        
        await ctx.reply(f"⬇️ يوجد **{actual_count}** رسالة تحت الرسالة المحددة.\n💡 تلميح: إذا أردت حذف هذه الرسائل مع الرسالة المحددة، استخدم الأمر: `/clear {actual_count + 1}`")
    except Exception as e:
        await ctx.reply(f"❌ حدث خطأ أثناء الحساب: {e}")

# ==========================================
# 📦 الأوامر الأصلية الخاصة بك (بدون أي تعديل)
# ==========================================
@bot.tree.command(name="scan", description="فحص المنافذ")
async def scan(interaction: discord.Interaction, target_ip: str):
    await interaction.response.send_message(f"جارٍ فحص `{target_ip}`...")

@bot.tree.command(name="osint", description="جمع معلومات النطاق")
async def osint(interaction: discord.Interaction, domain: str):
    await interaction.response.send_message(f"جاري جلب بيانات `{domain}`...")

# حذف الرسائل بعدد معين
@bot.tree.command(name="clear", description="حذف عدد معين من الرسائل")
@app_commands.checks.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(f"✅ تم حذف {amount} رسالة.", ephemeral=True)

# حاسبة النسبة المئوية
@bot.tree.command(name="calc", description="حساب النسبة المئوية: كم X من Y؟")
async def calc(interaction: discord.Interaction, part: float, total: float):
    percentage = (part / total) * 100
    await interaction.response.send_message(f"📊 النسبة هي: {percentage:.2f}%")


# ==========================================
# 🌟 الإضافات الجديدة (أشهر خصائص البوتات العالمية)
# ==========================================

# --- 1. أوامر الإدارة المتقدمة (Moderation) ---

@bot.tree.command(name="ban", description="حظر عضو من السيرفر")
@app_commands.checks.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = "لا يوجد سبب"):
    await member.ban(reason=reason)
    await interaction.response.send_message(f"🔨 تم حظر {member.mention} بنجاح | السبب: {reason}")

@bot.tree.command(name="kick", description="طرد عضو من السيرفر")
@app_commands.checks.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = "لا يوجد سبب"):
    await member.kick(reason=reason)
    await interaction.response.send_message(f"👢 تم طرد {member.mention} بنجاح | السبب: {reason}")

@bot.tree.command(name="timeout", description="إسكات (تايم أوت) لعضو لمدة معينة")
@app_commands.checks.has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, minutes: int, reason: str = "لا يوجد سبب"):
    duration = datetime.timedelta(minutes=minutes)
    await member.timeout(duration, reason=reason)
    await interaction.response.send_message(f"⏱️ تم إعطاء تايم أوت لـ {member.mention} لمدة {minutes} دقيقة | السبب: {reason}")

@bot.tree.command(name="lock", description="قفل الروم الحالي لمنع الأعضاء من الكتابة")
@app_commands.checks.has_permissions(manage_channels=True)
async def lock(interaction: discord.Interaction):
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=False)
    await interaction.response.send_message("🔒 تم قفل هذه الروم بنجاح.")

@bot.tree.command(name="unlock", description="فتح الروم الحالي للسماح بالكتابة")
@app_commands.checks.has_permissions(manage_channels=True)
async def unlock(interaction: discord.Interaction):
    await interaction.channel.set_permissions(interaction.guild.default_role, send_messages=True)
    await interaction.response.send_message("🔓 تم فتح هذه الروم بنجاح.")

# --- 2. أوامر المعلومات والخدمات (Utility & Info) ---

@bot.tree.command(name="ping", description="معرفة سرعة استجابة البوت (البنج)")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 بونق! سرعة الاستجابة الحالية هي: `{latency}ms`")

@bot.tree.command(name="userinfo", description="عرض معلومات مفصلة عنك أو عن عضو آخر")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(title=f"معلومات المستخدم: {member.display_name}", color=discord.Color.blue())
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="الاسم", value=member.name, inline=True)
    embed.add_field(name="الآيدي (ID)", value=member.id, inline=True)
    embed.add_field(name="تاريخ الانضمام للسيرفر", value=member.joined_at.strftime("%Y-%m-%d"), inline=False)
    embed.add_field(name="تاريخ إنشاء الحساب", value=member.created_at.strftime("%Y-%m-%d"), inline=False)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="serverinfo", description="عرض إحصائيات ومعلومات السيرفر")
async def serverinfo(interaction: discord.Interaction):
    guild = interaction.guild
    embed = discord.Embed(title=f"معلومات سيرفر {guild.name}", color=discord.Color.green())
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name="صاحب السيرفر", value=guild.owner.mention, inline=True)
    embed.add_field(name="عدد الأعضاء", value=guild.member_count, inline=True)
    embed.add_field(name="تاريخ الإنشاء", value=guild.created_at.strftime("%Y-%m-%d"), inline=False)
    embed.add_field(name="عدد الرومات", value=len(guild.channels), inline=True)
    embed.add_field(name="عدد الرتب", value=len(guild.roles), inline=True)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="avatar", description="تكبير وعرض الصورة الشخصية لعضو")
async def avatar(interaction: discord.Interaction, member: discord.Member = None):
    member = member or interaction.user
    embed = discord.Embed(title=f"الصورة الشخصية لـ {member.display_name}", color=discord.Color.purple())
    embed.set_image(url=member.display_avatar.url)
    await interaction.response.send_message(embed=embed)

# ==========================================
# تشغيل النظامين معاً (الكود الأصلي)
# ==========================================
if __name__ == "__main__":
    t = Thread(target=run_web)
    t.start()
    bot.run(os.environ['DISCORD_TOKEN'])
