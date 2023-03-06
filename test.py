from revChatGPT.V3 import Chatbot

bot = Chatbot(api_key='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')

while True:
    promo = input('You: ')
    bot_response = bot.ask_stream(promo, 'user')
    print('Bot: ', end='')
    for data in bot_response:
        print(data, end='', flush=True)
    print()