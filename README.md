# memefirmbots
MemeFirmBots is an automation script for the subreddit /r/MemeEconomy. The subreddit consists of Redditors submitting posts and then based on how many people invest in the post, the price of the post changes. More investments raises the price of the post (earlier versions of /r/MemeEconomy at least). /memefirmbots is my attempt to use this information to automate an entire firm of bots using one script. 
## Current Files:

**RMOeconfirm.py** - the main script. Controls all the bots when deployed.

**RMOfirmSOLO.py** - if you wanna automate only one of the bots

**currentFirmStats.py** - gets the amount of memecoins each bot has and adds them together

**sh files** - these are just be being lazy and being able to loop through each of the bots specifically. It got a little difficult with how the Reddit API works so restarting the script completely each time was a solution.
