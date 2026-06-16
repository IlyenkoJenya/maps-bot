import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
)

import config
from data_manager import DataManager
from review_generator import generate_reviews

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

data_manager = DataManager(config.RECORDS_PATH, config.PHOTOS_DIR)


# ── shared keyboard builder ──────────────────────────────────────────────────

def _platform_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("2GIS", callback_data="platform:2gis"),
            InlineKeyboardButton("Google Maps", callback_data="platform:google"),
        ],
        [
            InlineKeyboardButton("Просто текст", callback_data="platform:text"),
        ],
    ])


# ── /start command ────────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    remaining = data_manager.remaining_count()
    remaining = data_manager.remaining_count()
    text = (
        f"📍 Где пишем отзыв?\n\n"
        f"1️⃣ короткий\n"
        f"2️⃣ средний\n"
        f"3️⃣ длинный\n\n"
        f"📸 Осталось фото: {remaining}"
    )
    await update.message.reply_text(text, reply_markup=_platform_keyboard())


# ── /review command ───────────────────────────────────────────────────────────

async def cmd_review(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    remaining = data_manager.remaining_count()
    text = (
        f"📍 Где пишем отзыв?\n\n"
        f"1️⃣ короткий\n"
        f"2️⃣ средний\n"
        f"3️⃣ длинный\n\n"
        f"📸 Осталось фото: {remaining}"
    )
    await update.message.reply_text(text, reply_markup=_platform_keyboard())


# ── platform button handler ───────────────────────────────────────────────────

async def on_platform_chosen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)

    platform = query.data.split(":")[1]
    text_only = platform == "text"

    if platform == "2gis":
        link = config.LINK_2GIS
        platform_name = "2GIS"
    elif platform == "google":
        link = config.LINK_GOOGLE_MAPS
        platform_name = "Google Maps"
    else:
        link = None
        platform_name = None

    filename, record = data_manager.get_random_record()
    if filename is None:
        await query.message.reply_text("Фотографии закончились. Нужно добавить новые.")
        return

    short, medium, long_ = await generate_reviews(record)

    if text_only:
        remaining = data_manager.remaining_count()
    else:
        remaining = data_manager.remaining_count() - 1

    if not text_only:
        photo_path = f"{config.PHOTOS_DIR}/{filename}"
        photo_caption = f"Ссылка на {platform_name}:\n{link}" if link else platform_name
        with open(photo_path, "rb") as photo_file:
            await query.message.reply_photo(photo=photo_file, caption=photo_caption)

    await query.message.reply_text(short)
    await query.message.reply_text(medium)
    await query.message.reply_text(long_)
    await query.message.reply_text("✅ Готово! Чтобы получить новый отзыв <b>нажми</b> /start", parse_mode="HTML")

    if not text_only:
        data_manager.delete_record(filename)
        logger.info("Использована запись %s. Осталось: %d", filename, remaining)
    else:
        logger.info("Текстовый режим — запись %s не удалена.", filename)


# ── /status command ───────────────────────────────────────────────────────────

async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    count = data_manager.remaining_count()
    await update.message.reply_text(f"Доступных фото для отзывов: {count}")


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    app = Application.builder().token(config.BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("review", cmd_review))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CallbackQueryHandler(on_platform_chosen, pattern=r"^platform:"))

    logger.info("Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
