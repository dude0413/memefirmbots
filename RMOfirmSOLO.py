from package.config import *
from package2.config import *
from package3.config import *
from currentStats import merged_list, names_merged_list
import time, random, os, datetime, argparse
version = '1.0'

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--bot_used', help='you know what to do...')
args = parser.parse_args()

for bot_name in names_merged_list:
    if str(args.bot_used) == bot_name:
        location = names_merged_list.index(bot_name)
        bot = merged_list[location]
    else:
        continue
percentage_of_balance_invested = float(0.9)

subreddit = bot.subreddit('MemeEconomy')
now = datetime.datetime.now()
# Setting up Files #
log_file_name = str(now.strftime('%m.%d') + '..' + str(random.randint(1,100)) + '.txt')
log_file = open(log_file_name, 'w')
invested_file_name = 'investedin.txt'
if os.path.isfile(invested_file_name) == True:
    print('Found the file')
else:
    invested_file = open(invested_file_name, 'w+')
# Add the post_ids to the file #
def append_to_invested_file(post_id):
    with open(invested_file_name, 'a') as I:
        I.write(post_id + '\n')
# Log function #
def log(input, bot_used=my_bot):
    now = datetime.datetime.now()
    message = str(bot_used.user.me()) + ': ' + str(input) + '\n' + str(now.strftime('%m-%d %H:%M:%S'))
    print(message)
    with open(log_file_name, 'a') as l:
        l.write(message + '\n\n')

# Finds the balance, invests into the post, and uses the log function to document #
def invest(post_id, bot_name):
    # Configure each bot #
    # Get balance #
    inbox_comment_reply_list = []
    for item in bot_name.inbox.comment_replies(limit=10):
        body = item.body
        warning_words = ['Firm:', 'The', 'Hey', 'You', "Couldn't", "Successfully"]
        if item.author == "MemeInvestor_bot":
            if not any(word in body.split(' ', 1)[0] for word in warning_words):
                if not 'Overlords' in body.split(' ', 1)[-1]:
                    inbox_comment_reply_list.append(body)
    inbox_message = inbox_comment_reply_list[0]
    message_breakdown = inbox_message.split(" ")

    balance = int(message_breakdown[-2].replace("**", "").replace(",", ""))
    # Invest and upvote post#
    log(str(bot_name.user.me()) + ' has found a post and has upvoted it')
    investment_submission = bot_name.submission(post_id)
    investment_submission.upvote()
    for comment in investment_submission.comments:
        if comment.author == 'MemeInvestor_bot':
            amount = round(balance * percentage_of_balance_invested)
            now = datetime.datetime.now()
            now_time = now.time()
            if now_time >= datetime.time(22, 30) and now_time <= datetime.time(6, 00):
                log('Investing with a lesser value because its nighttime', bot)
                amount = round(balance * (percentage_of_balance_invested / 3))
            else:
                try:
                    comment.reply('!invest ' + str(amount))
                    append_to_invested_file(post_id)
                    log(str(bot_name.user.me()) + ' has invested in ' + str(post_id) + ' with ' + str(amount) + ' memecoins')
                except praw.exceptions.APIException:
                    print('Got the rate limit, exiting now...')
                    exit()
#    announcement_message = 'An algorithm-based firm supports this meme.'
    log('Investing into ' + str(post_id), bot_name)

while True:
    log('Entering Searching Mode with me...')
    # Tracking and Investing Mode - should take 1 hour #
    investment_boolean = False
    while investment_boolean == False:
        log('Searching...', bot)
        for submission in subreddit.new(limit=20):
            submission_id = submission.id
            # Open the investments txt file and see if the submission id is in there, if not, continue
            with open(invested_file_name) as r:
                for i, l in enumerate(r):
                    number_of_investments = i + 2
                    str_number_of_investments = str(number_of_investments)
                already_invested_investments = r.read().split('n')
                already_invested_investments = list(filter(None, already_invested_investments))
            if submission_id not in already_invested_investments and investment_boolean == False:
                submission_created_formatted = submission.created_utc
                submission_time = datetime.datetime.utcfromtimestamp(submission_created_formatted)
                age = (datetime.datetime.now() - submission_time)
                upvotes_on_post = submission.ups
                comments = submission.comments.list()
                number_of_comments = len(comments)
                submission_title = submission.title

                # If the post is less than 60 minutes old... #
                # More than 25 minutes old #
                time_boolean_twenty_five_old = age > datetime.timedelta(minutes=25)
                # Less than 60 minutes old #
                time_boolean_sixty = age < datetime.timedelta(minutes=60)
                # Less than 10 minutes old #
                time_boolean_ten = age < datetime.timedelta(minutes=10)
                qualification_message = 'The post qualified because it was... '
                if time_boolean_twenty_five_old == False and upvotes_on_post > 45:
                    invest(submission_id, bot)
                    log(qualification_message + 'Less than 25 minutes old and had more than 35 upvotes.')
                    investment_boolean = True
                elif time_boolean_sixty == True and time_boolean_twenty_five_old == True and 100 > upvotes_on_post > 55:
                    invest(submission_id, bot)
                    log(qualification_message + 'Less than 60 minutes old and had between 100 and 55 upvotes.')
                    investment_boolean = True
                elif time_boolean_ten == True and upvotes_on_post > 25:
                    invest(submission_id, bot)
                    log(qualification_message + 'Less than 10 minutes old and had more than 25 upvotes.')
                    investment_boolean = True
                else:
                    continue
            else:
                continue
    # Wait 4 hours and 1 minute to get the rewards for each of the bots #
    log('Done with the investment cycle, going into diagnostics...')
    time.sleep(14430)

    # Diagnostics mode #
    # For every bot, copy and paste the final thing into the log file #
    inbox_comment_reply_list = []
    for item in bot.inbox.comment_replies(limit=10):
        if item.author == "MemeInvestor_bot":
            inbox_comment_reply_list.append(item.body)
    log(inbox_comment_reply_list[0], bot)
