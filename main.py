from telegram import Update
from telegram.ext import  Application, CommandHandler,filters, MessageHandler, CallbackContext

import time
import random as r


TOKEN='use your telegram bot token here'
Bot_name="Speedy"
My_telegram_bot="http://t.me/SpeedTyperBot"


async def start(update: Update, context: CallbackContext) -> None:
   await update.message.reply_text(f"Hey there! I am Speedy, I'll help you to know your typing speed.\n\n"
                                   " To use this bot, follow these steps: \n"
                                   " 1.Use /generate command to get the required input you need to type.\n"
                                   " 2. Start typing your input and get your typing speed.\n ")
   
   

    
async def generate_typing_prompt(update: Update, context: CallbackContext) -> None:
    test=["the quick brown fox jumps over the lazy dog sphinx of black quartz, judge my vow five hexing wizard bots jump quickly,pack my box with five dozen liquor jugs."," jiving crazy fox nymph grabs quick waltz quick brown foxes jump over the lazy dog",
    "lazy dog jumps over the quick brown fox jackdaws love my big sphinx of quartz mr. jock, tv quiz phd, bags few lynx quick wafting zephyrs vex bold jim going round above the world garden looks beautiful",
    "five big quacking zephyrs jolt my wax bed the five boxing wizards jump quickly the quick onyx goblin jumps over the lazy dwarf helping out there also a good work happily ever after",
    "quartz glyph job vex'd cwm finks quick zephyrs blow, vexing daft jim my girl wove six dozen plaid jackets before she quitquick zephyrs blow going out works more ring and roses"," vexing daft jim my girl wove six dozen plaid jackets before she quit cwm fjord bank glyphs vext quiz glyphs quietly joke on the zephyrs the jay, pig, fox, zebra, and my wolves quack sphinx of black quartz, judge my vow how razorback-jumping frogs can level six piqued gymnasts"]
    r.shuffle(test)
    test1 = r.choice(test)
    context.user_data['start_time'] = int(round(time.time()))
    context.user_data['prompt'] = test1
    await update.message.reply_text(f"Type the following text:\n\n{test1}")


def count_wpm(text, time_taken, paratest, usertest):
    words = text.split()
    num_words = len(words)
    
    if paratest and usertest:
        num_mistakes = mistake(paratest, usertest)
        num_correct_words = num_words - num_mistakes
        wpm = (num_correct_words / time_taken) * 60
    else:
        wpm = (num_words / time_taken) * 60
    
    return wpm


def mistake(paratest, usertest):
    error = 0
    para_lines = paratest.splitlines()
    user_lines = usertest.splitlines()
    min_lines = min(len(para_lines), len(user_lines))
    for i in range(min_lines):
        para_words = para_lines[i].split()
        user_words = user_lines[i].split()
        min_words = min(len(para_words), len(user_words))
        for j in range(min_words):
            if para_words[j] != user_words[j]:
                error += 1
    return error


def accuracy(paratest, usertest):
    para_words = paratest.split()
    user_words = usertest.split()
    total_words = max(len(para_words), len(user_words))
    
    if total_words == 0:
        return 100.0  # Both strings are empty, consider it 100% accurate
    
    num_correct_words = sum(1 for pw, uw in zip(para_words, user_words) if pw == uw)
    acc = num_correct_words / total_words
    acc_perc = acc * 100
    return acc_perc

async def measure_wpm(update: Update, context: CallbackContext):
    start_time=context.user_data['start_time']
    testinput=update.message.text
    end_time= int(round(time.time()))
    
    prompt=context.user_data['prompt']
    time_taken = end_time - start_time

    check =accuracy(prompt, testinput)
    wpm =count_wpm(testinput, time_taken,prompt,testinput)

    try:
        if testinput is not None:
            num_mistakes = mistake(prompt, testinput)
            if num_mistakes > 0:
                await update.message.reply_text(
                    "Looks like you made a few errors in your text that's why your accuracy goes down.\n\nNo worries! Review your input for mistakes, and we'll try again.\n\nPractice makes a person perfect."
                )
            await update.message.reply_text(f"Your accuracy is: {round(check)}\nTotal words per minute is: {round(wpm)}")
            await update.message.reply_text(f"Thank you for using speedy! Have a nice day!")

    except:
        await update.message.reply_text(f"Please start again! There must be some mistakes in the input you provided")


async def error(update: Update, context: CallbackContext):
    print(f"Update {update} caused error {context.error}")

print("starting bot")
app=Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("generate", generate_typing_prompt))

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,measure_wpm))

app.add_error_handler(error)

print("polling...")
app.run_polling()


