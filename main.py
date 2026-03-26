from telegram import Update
from telegram.ext import Updater, Filters, CommandHandler, CallbackContext, MessageHandler
import os
import re
import instaloader


TOKEN = "your_token_here"
L = instaloader.Instaloader(
    download_comments=False,
    download_video_thumbnails=False,
    save_metadata=False,
)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("Salom 👋\n\n"
                              "Siz instagram url ni yuboring men sizga vidio formatda olib beraman 😁")
    return


def short_cut(url: str):
    match = re.search(r"instagram\.com/(?:reel|p|tv)/([^/?]+)", url)
    return match.group(1) if match else None


def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    if "instagram.com" not in text:
        update.message.reply_text("Linkni to'g'ri yuboring!")

    shortcode = short_cut(text)
    if not shortcode:
        update.message.reply_text("Linkda xatolik bor!")
        return
    try:
        update.message.reply_text("Video yuklanmoqda...")

        post = instaloader.Post.from_shortcode(L.context, shortcode)
        L.download_post(post, target="download")

        for file in os.listdir("download"):
            if file.endswith(".mp4"):
                path = f"download/{file}"
                update.message.reply_video(video=open(path, "rb"))
                os.remove(path)
            elif file.endswith(".jpg"):
                path = f"download/{file}"
                update.message.reply_photo(photo=open(path, "rb"))
                os.remove(path)


        update.message.reply_text("Tayyor !")

    except Exception as e:
        update.message.reply_text("Video olishda xatolik bor !")
        print(e)


def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~ Filters.command, handle_message))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
