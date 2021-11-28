from dotenv import load_dotenv
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext)

import machine_core
import os
import logging

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(
    format="%(asctime)s - " "%(name)s - " "%(levelname)s - " "%(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

bot = machine_core.PizzaBoy()


def start(update: Update, context: CallbackContext) -> None:
    """Отправте /start для активации бота."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        f"Здравствуйте, {user.mention_markdown_v2()}\!\n"
        f"Готовы заказать вкуснейшую пиццу? 😉\n"
        f"Тогда поехали /order"
    )


def order(update: Update, context: CallbackContext) -> None:
    """Для начала заказа введите /order"""
    bot.start()
    keyboard = [
        [
            InlineKeyboardButton("🥘Большую", callback_data="большую"),
            InlineKeyboardButton("🍕Маленькую", callback_data="маленькую"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Какую Вы хотите пиццу? Большую или маленькую?",
        reply_markup=reply_markup
    )


def message_handler(update: Update, context: CallbackContext) -> None:
    """Функция отвечающяя за изменение состояния
    и атрибутов класса стейт-машины"""
    query = update.callback_query

    query.answer()

    if bot.state == "pizza_size":
        if query.data in ("большую", "маленькую"):
            bot.set_pizza_size(query.data)
            bot.next()
            keyboard = [
                [
                    InlineKeyboardButton(
                        "💵Наличными",
                        callback_data="наличными"
                    ),
                    InlineKeyboardButton(
                        "💳Онлайн",
                        callback_data="онлайн"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                text="Как Вы будете платить?", reply_markup=reply_markup
            )
        else:
            update.message.reply_text("Два варианта: большую / маленькую.")
    elif bot.state == "pay_method":
        if query.data in ("наличными", "онлайн"):
            bot.set_pay_method(query.data)
            bot.next()
            keyboard = [
                [
                    InlineKeyboardButton("✅Да", callback_data="да"),
                    InlineKeyboardButton("❌Нет", callback_data="нет"),
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            query.edit_message_text(
                f"Вы будете {bot.get_pizza_size()} пиццу, " 
                f"оплата - {bot.get_pay_method()}?",
                reply_markup=reply_markup,
            )
        else:
            update.message.reply_text(
                "Конечно есть много вариантов оплаты, "
                "и первыми биткойнами покупали пиццу, "
                "но сейчас мы принимает только наличными или онлайн."
            )
    elif bot.state == "confirm":
        if query.data == "да":
            bot.done()
            bot.end()
            query.edit_message_text(
                "Спасибо за Ваш заказ! Ждем Вас снова у нас 👋"
            )
        elif query.data == "нет":
            bot.cancel()
            bot.end()
            query.edit_message_text(
                "Оу! 😔 Вам что-то не понравилось?\nВаш заказ отменен.\n"
                "Давайте снова создадим заказ /order?"
            )
        else:
            update.message.reply_text("Два варианта: да / нет.")
    else:
        update.message.reply_text(
            "Что то пошло не так! Давайте снова создадим заказ /order?"
        )


def cancel(update: Update, context: CallbackContext) -> None:
    """Функция отменяющяя весь заказ /cancel"""
    if bot.state != "waiting":
        bot.cancel()
        bot.end()
        bot.set_pizza_size_none()
        bot.set_pay_method_none()
        update.message.reply_text("Заказ отменён")
    else:
        update.message.reply_text(
            "Что бы что-то отменить,\nнадо сначала заказать. 😏\n"
            "Давайте сделаем заказ /order?"
        )


def main() -> None:
    """Запуск бота."""
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("order", order))
    dispatcher.add_handler(CommandHandler("cancel", cancel))
    dispatcher.add_handler(CallbackQueryHandler(message_handler))

    updater.start_polling()

    updater.idle()
