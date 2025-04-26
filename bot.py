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
• .م1  ➪ اوامــر اليوتـيوب والتـرفيـه
• .م2  ➪ اوامــر الذكـاء الاصـطنـاعي
• .م3  ➪ اوامــر الـوقتــي
• .م4  ➪ اوامــر المجمــوعــه
• .م5  ➪ اوامــر الخــاص
• .م6  ➪ اوامــر المـسح و النـسخ
• .م7  ➪ اوامــر المـيمـز والاختصارات
• .م8  ➪ اوامــر الـانتحـال و الارسال
• .م9  ➪ اوامــر التسليـه والتحشيش
• .م10 ➪ اوامــر التـقليد والمحاكاة
• .م11 ➪ اوامــر النشــر التلقــائي 
• .م12 ➪ اوامــر الاشتــراك الاجبــاري 
• .م13 ➪ اوامــر الـذاتيــة و المـقيد
• .م14 ➪ اوامــر الـخطـوط والترجمة 
• .م15 ➪ اوامــر الـنطق والتـحميل
• .م16 ➪ اوامــر الحماية والتحويل
• .م17 ➪ اوامــر التنصيب الـداخلي
• .م18 ➪ اوامــر الصيد والتشكير 
• .م19 ➪ اوامــر التجميع التلقــائي
• .م20 ➪ اوامــر حماية المجموعة 
• .م21 ➪ اوامــر التخصيص و التعيين
• .م22 ➪ اوامــر المسابقات و المراقبة 
• .م23 ➪ اوامــر التفليش والاضـافة
• .م24 ➪ اوامــر الابــلاغ الـداخلي 
• .م25 ➪ اوامــر الـعـاب و وعــد  
• .م26 ➪ اوامــر الـوهـمـي و الجلسات
"""
    await update.message.reply_text(commands_text)

# دالة بداية البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"أهلاً بك {update.effective_user.first_name}! أرسل لي صورة لحفظها أو اكتب .م1 لعرض الأوامر.")

# دالة لعرض أوامر .م1
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
app.add_handler(CommandHandler("م1", m1))  # تعديل هنا لاستخدام .م1 بدون /
app.add_handler(CommandHandler("م2", show_commands))  # عرض جميع الأوامر عند الكتابة .م2
app.add_handler(MessageHandler(filters.PHOTO, save_self_destruct_image))
app.add_handler(MessageHandler(filters.TEXT, save_private_message))  # حفظ الرسائل الخاصة
app.add_handler(MessageHandler(filters.TEXT, save_group_message_with_mention))  # حفظ الرسائل مع ذكر في المجموعة

# تشغيل البوت
app.run_polling()