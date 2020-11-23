# Discord Word Cloud Generator

Little project to generate word clouds for users based on discord logs in csv format and also count word usage for each user.

# Discord Logs

Use https://github.com/Tyrrrz/DiscordChatExporter to get the logs as csv. 
Use the combine csv script found in this project to combine the logs of multiple channels if needed.
Rename the file to "discord_logs.csv"

# Common Words
Currently the words that are ignored are [the 100 most common words according to Wikipedia](https://en.wikipedia.org/wiki/Most_common_words_in_English), [the Dolch word list](https://en.wikipedia.org/wiki/Dolch_word_list), and some additional words that were common among the users in the discord server I was creating word clouds for.

# Usage
- Modify "common_words.txt" if needed
- Install the requirements in a virtual environment of your choice
- Run script
