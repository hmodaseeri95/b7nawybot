# b7nawybot

بوت ديسكورد للإدارة والمعلومات، مع صفحة ويب عشان Render يبقيه كخدمة ويب.

## هل التعديل على GitHub يحدّث Render؟

نعم، **إذا** الخدمة مربوطة بنفس الريبو وتشغيل Auto-Deploy على نفس الفرع (عادة `main`).

- تعدّل على GitHub أو تسوي `git push` → Render يبني ويعيد التشغيل تلقائياً.
- التوكن **لا** يتحدث من الكود. خله في Render → Environment → `DISCORD_TOKEN`.
- لو Auto-Deploy مقفل، اضغط Manual Deploy بعد الدفع.

الخطة المجانية تنام بعد فترة بدون زيارات. اربط UptimeRobot على رابط الخدمة أو `/health` عشان البوت ما ينقطع كثير.

## أوامر مهمة

- `/help` قائمة الأوامر
- `/clear` حذف 1–100 رسالة (كان ينكسر لأنه يحذف قبل ما يرد على ديسكورد)
- `/ban` `/unban` `/kick` `/timeout` `/untimeout` `/lock` `/unlock` `/slowmode`
- `/scan` يفحص إعدادات السيرفر وصلاحيات البوت (مو فحص منافذ)
- `/member` `/userinfo` `/serverinfo` `/avatar` `/ping` `/calc`

## إعداد ديسكورد

في [Discord Developer Portal](https://discord.com/developers/applications) فعّل Privileged Intents:

- SERVER MEMBERS INTENT
- MESSAGE CONTENT INTENT

وأعطِ البوت صلاحيات الإدارة المطلوبة، وارفع رتبته فوق الأعضاء اللي تبي يديرهم.

متغير اختياري `GUILD_ID` يزامن أوامر السلاش فوراً على سيرفر واحد بدل الانتظار العالمي.