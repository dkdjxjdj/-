import random
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# --- KİŞİSEL BİLGİLERİN ---
TOKEN = "8339947987:AAG1ITZKKumasLJqCvDMtjjwlL45HwP-GYo"  # Senin Bot Token'ın
ADMIN_ID = 8534191173  # Senin Kullanıcı ID'n

# Veri tabanı (Geçici hafıza)
user_data = {} 
used_codes = set()
daily_claims = {}

# Havalı Giriş Mesajı
HOŞGELDİN_MESAJI = (
    "┏━━━━━━━━━━━━━━━━━━━━┓\n"
    "┃  𝗫𝗢𝗞#𝕊𝔸ℕ𝔸𝕃#𝕋𝕀̇𝕄  ┃\n"
    "┃   𝕂𝕌𝕄𝔸ℝ 𝔹𝕆𝕋𝕌ℕ𝔸    ┃\n"
    "┃    ℍ𝕆𝕊𝔾𝔼𝕃𝔻𝕀̇ℕ     ┃\n"
    "┗━━━━━━━━━━━━━━━━━━━━┛\n\n"
    "💰 Hesabına **10.000 KP** Tanımlandı!\n\n"
    "🎮 **KOMUTLAR:**\n"
    "🔹 /slot - Şansını Dene\n"
    "🔹 /gunluk - 5.000 KP Ödül\n"
    "🔹 /xok - 20.000 KP Hediye\n"
    "🔹 /liderlik - En Zenginler\n"
    "🔹 /profil - Bakiyeni Gör"
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in user_data:
        user_data[uid] = 10000  # Başlangıç 10k
    await update.message.reply_text(HOŞGELDİN_MESAJI)

async def gunluk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    bugun = datetime.date.today()
    if daily_claims.get(uid) == bugun:
        await update.message.reply_text("❌ Bugünlük ödülünü zaten aldın!")
    else:
        user_data[uid] = user_data.get(uid, 10000) + 5000
        daily_claims[uid] = bugun
        await update.message.reply_text(f"✅ 5.000 KP eklendi! Toplam: {user_data[uid]} KP")

async def xok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in used_codes:
        await update.message.reply_text("❌ XOK kodunu zaten kullandın!")
    else:
        user_data[uid] = user_data.get(uid, 10000) + 20000
        used_codes.add(uid)
        await update.message.reply_text("💎 **XOK#SANAL#TİM** Özel Hediyesi: 20.000 KP!")

async def slot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if user_data.get(uid, 0) < 1000:
        await update.message.reply_text("❌ En az 1000 KP lazım!")
        return
    kazanc = random.choice([-1000, -1000, 3000, 5000])
    user_data[uid] += kazanc
    msg = "🎉 KAZANDIN!" if kazanc > 0 else "💀 KAYBETTİN!"
    await update.message.reply_text(f"{msg}\nBakiyen: {user_data[uid]} KP")

async def liderlik(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not user_data:
        await update.message.reply_text("Kimse oynamadı.")
        return
    sirali = sorted(user_data.items(), key=lambda x: x[1], reverse=True)[:5]
    metin = "🏆 **LİDERLİK** 🏆\n"
    for i, (u_id, para) in enumerate(sirali, 1):
        metin += f"{i}. {u_id} - {para} KP\n"
    await update.message.reply_text(metin)

async def ver(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    try:
        target_id, miktar = int(context.args[0]), int(context.args[1])
        user_data[target_id] = user_data.get(target_id, 10000) + miktar
        await update.message.reply_text(f"✅ {target_id}'ye {miktar} KP verildi.")
    except:
        await update.message.reply_text("Kullanım: /ver ID Miktar")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gunluk", gunluk))
    app.add_handler(CommandHandler("xok", xok))
    app.add_handler(CommandHandler("slot", slot))
    app.add_handler(CommandHandler("liderlik", liderlik))
    app.add_handler(CommandHandler("ver", ver))
    app.run_polling()
