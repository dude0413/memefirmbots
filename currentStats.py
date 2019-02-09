from package.config import *
from package2.config import *
from package3.config import *
merged_list = team_1_bot_list + team_2_bot_list + team_3_bot_list
money_list = []
for bot in merged_list:
    inbox_comment_reply_list = []
    for item in bot.inbox.comment_replies(limit=10):
        body = item.body
        warning_words = ['Firm:', 'The', 'Hey', 'You']
        if item.author == "MemeInvestor_bot":
            if not any(word in body.split(' ', 1)[0] for word in warning_words):
                inbox_comment_reply_list.append(body)
    inbox_message = inbox_comment_reply_list[0]
    message_breakdown = inbox_message.split(" ")

    balance = int(message_breakdown[-2].replace("**", "").replace(",", ""))
    money_list.append(balance)
    print(str(bot.user.me()) + ': ' + str(balance) + ' memecoins')

print('\n' + str(sum(money_list)) + ' memecoins total')
