import os
import time
from telegram import Update, Chat
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# تحديد التوكن الخاص بك
TOKEN = "7825459511:AAFonYRpG_V9TLIRkzxGIGXVLxCpEHSbb5E"

# تحديد مسار المجلد الذي سيتم حفظ الصور فيه
folder_name = "self_destruct_images"
folder_path = os.path.join(os.getcwd(), folder_name)

# المجلد لتخزين الرسائل الخاصة والمجموعة
private_messages_folder = "private_messages"
group_messages_folder = "group_messages"

# التحقق إذا كان المجلد موجودًا، وإذا لم يكن، يتم إنشاؤه
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

if not os.path.exists(private_messages_folder):
    os.makedirs(private_messages_folder)

if not os.path.exists(group_messages_folder):
    os.makedirs(group_messages_folder)

# معرفات المجموعات الخاصة بالمستخدمين
user_group_ids = {}

# دالة لحفظ الصور المرسلة وتدميرها بعد وقت محدد
async def save_self_destruct_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        # الحصول على أكبر صورة من الصور المرسلة
        photo = update.message.photo[-1]
        file = await photo.get_file()

        # تحديد المسار الكامل لحفظ الصورة
        file_path = os.path.join(folder_path, f"{file.file_id}.jpg")
        
        # تنزيل الصورة وحفظها
        await file.download(file_path)

        # إظهار رسالة للمستخدم بعد حفظ الصورة
        await update.message.reply_text(f"تم حفظ الصورة في {file_path}. ستدمج بعد وقت قليل.")

        # الانتظار لمدة محددة ثم حذف الصورة (تدمير ذاتي)
        await time.sleep(10)  # 10 ثواني على سبيل المثال

        # حذف الصورة من المجلد
        if os.path.exists(file_path):
            os.remove(file_path)
            await update.message.reply_text(f"تم تدمير الصورة بعد مرور الوقت المحدد.")
        else:
            await update.message.reply_text(f"حدث خطأ أثناء حذف الصورة.")

# دالة لحفظ الرسائل الخاصة في مجموعة مخصصة
async def save_private_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    message = update.message.text

    # إذا لم يكن للمستخدم مجموعة خاصة، يتم إنشاء مجموعة
    if user_id not in user_group_ids:
        # إنشاء مجموعة جديدة للمستخدم (هنا سنحتاج إلى معرف المجموعة)
        # على سبيل المثال يمكن إضافة رقم تعريف المجموعة الخاصة بالمستخدم
        user_group_ids[user_id] = "YOUR_GROUP_ID"  # تحديد المعرف الفعلي للمجموعة الخاصة

    # إرسال الرسالة إلى المجموعة الخاصة للمستخدم
    chat_id = user_group_ids[user_id]
    await context.bot.send_message(chat_id=chat_id, text=f"رسالة خاصة من {update.message.from_user.first_name}: {message}")
    
    await update.message.reply_text("تم إرسال رسالتك إلى المجموعة الخاصة.")

# دالة لحفظ الرسائل التي تحتوي على ذكر شخص في مجموعة
async def save_group_message_with_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # التحقق إذا كانت الرسالة تحتوي على ذكر شخص
    if update.message.entities:
        for entity in update.message.entities:
            if entity.type == "mention":
                message = update.message.text
                user_id = update.message.from_user.id
                
                # إذا لم يكن للمستخدم مجموعة خاصة، يتم إنشاء مجموعة
                if user_id not in user_group_ids:
                    user_group_ids[user_id] = "YOUR_GROUP_ID"  # تحديد المعرف الفعلي للمجموعة الخاصة

                # إرسال الرسالة إلى المجموعة الخاصة للمستخدم
                chat_id = user_group_ids[user_id]
                await context.bot.send_message(chat_id=chat_id, text=f"رسالة مع ذكر من {update.message.from_user.first_name}: {message}")
                
                await update.message.reply_text("تم إرسال الرسالة إلى المجموعة الخاصة.")

# دالة لعرض الأوامر
async def show_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands_text = """
⋆ـ┄─┄┄─┄┄ـ⋆
• .m1  ➪ اوامــر اليوتـيوب والتـرفيـه
• .m2  ➪ اوامــر الذكـاء الاصـطنـاعي
• .m3  ➪ اوامــر الـوقتــي
• .m4  ➪ اوامــر المجمــوعــه
• .m5  ➪ اوامــر الخــاص
• .m6  ➪ اوامــر المـسح و النـسخ
• .m7  ➪ اوامــر المـيمـز والاختصارات
• .m8  ➪ اوامــر الـانتحـال و الارسال
• .m9  ➪ اوامــر التسليـه والتحشيش
• .m10 ➪ اوامــر التـقليد والمحاكاة
• .m11 ➪ اوامــر النشــر التلقــائي 
• .m12 ➪ اوامــر الاشتــراك الاجبــاري 
• .m13 ➪ اوامــر الـذاتيــة و المـقيد
• .m14 ➪ اوامــر الـخطـوط والترجمة 
• .m15 ➪ اوامــر الـنطق والتـحميل
• .m16 ➪ اوامــر الحماية والتحويل
• .m17 ➪ اوامــر التنصيب الـداخلي
• .m18 ➪ اوامــر الصيد والتشكير 
• .m19 ➪ اوامــر التجميع التلقــائي
• .m20 ➪ اوامــر حماية المجموعة 
• .m21 ➪ اوامــر التخصيص و التعيين
• .m22 ➪ اوامــر المسابقات و المراقبة 
• .m23 ➪ اوامــر التفليش والاضـافة
• .m24 ➪ اوامــر الابــلاغ الـداخلي 
• .m25 ➪ اوامــر الـعـاب و وعــد  
• .m26 ➪ اوامــر الـوهـمـي و الجلسات
"""
    await update.message.reply_text(commands_text)

# دالة بداية البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"أهلاً بك {update.effective_user.first_name}! أرسل لي صورة لحفظها أو اكتب .m1 لعرض الأوامر.")

# دالة لعرض أوامر .m1
async def m1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m1_commands = """
    • .يوتيوب  ➪ البحث عن فيديوهات
    • .موسيقى  ➪ تشغيل الموسيقى
    • .ترفيه  ➪ مرح وتحفيز
    """
    await update.message.reply_text(m1_commands)

# إعداد التطبيق الخاص بالبوت
app = ApplicationBuilder().token(TOKEN).build()

# إضافة المعالج للأوامر
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("m1", m1))  # تعديل هنا لاستخدام m1 بدلاً من م1
app.add_handler(CommandHandler("m2", show_commands))  # عرض جميع الأوامر عند الكتابة .m2
app.add_handler(MessageHandler(filters.PHOTO, save_self_destruct_image))
app.add_handler(MessageHandler(filters.TEXT, save_private_message))  # حفظ الرسائل الخاصة
app.add_handler(MessageHandler(filters.TEXT, save_group_message_with_mention))  # حفظ الرسائل مع ذكر في المجموعة

# تشغيل البوت
app.run_polling()