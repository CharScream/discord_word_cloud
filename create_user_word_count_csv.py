import pandas as pd
from operator import itemgetter
from wordcloud import WordCloud

CHAT_LOG_FILE = "discord_logs.csv"
COMMON_WORD_FILE = "common_words.txt"
IGNORED_USERS_FILE = "ignored_users.txt"
OUTPUT_FILE_EXTENSION = "csv"


def get_word_set_from_file(file_name: str, comment_character: str = "~") -> set:
    """
    :param comment_character: the character used to ignore a line in the file
    :param file_name: name of the file in the path
    :return: a set of words
    """
    word_set = set()
    with open(file_name) as f:
        for line in f:
            if line[0] == comment_character:
                continue
            cleaned_line = line.strip().lower().replace(",", "").split()
            for word in cleaned_line:
                word_set.add(word)
    return word_set


def get_user_word_dictionary_from_csv(file_name: str, user_ignore_list: set) -> dict:
    """
    :param file_name: csv file with discord logs
    :param user_ignore_list: file with list of users to ignore
    :return: a dictionary in the form of {username : word_dictionary: {word : count}}
    """
    df = pd.read_csv(file_name)
    df2 = df.loc[:, ["Author", "Content"]]

    special_characters_pattern = r"[^A-Za-z'0-9 ]"
    df2.replace(
        to_replace=special_characters_pattern, value=" ", inplace=True, regex=True
    )

    user_word_count_dictionary = {}
    common_word_set = get_word_set_from_file(COMMON_WORD_FILE)
    for row in df2.itertuples(index=False):
        # hack to ignore nan in the dataframe
        if type(row.Content) is float:
            continue

        user = row.Author.strip().split()[0]

        if user.lower() in user_ignore_list:
            continue

        if user not in user_word_count_dictionary:
            user_word_count_dictionary[user] = {}

        current_author_dictionary = user_word_count_dictionary[user]

        for word in row.Content.replace('""', "").lower().split():
            # ignores single letter artifacts from emotes
            if word in common_word_set or len(word) == 1:
                continue
            if word not in current_author_dictionary:
                current_author_dictionary[word] = 0
            current_author_dictionary[word] += 1

    return user_word_count_dictionary


def make_word_cloud(word_dict: dict, user: str, max_words: int = 3000) -> None:
    word_cloud = WordCloud(scale=10, background_color="white", max_words=max_words)
    word_cloud.generate_from_frequencies(word_dict)
    word_cloud.to_file(f"clouds/{user}-word-cloud.jpg")


def get_sorted_word_count_list_from_word_dictionary(
    word_dictionary: dict, count_index: int = 1
) -> list:
    """
    :returns: list of tuples in the form of (word, wordcount)
    """
    word_list = [(word, count) for word, count in word_dictionary.items()]
    word_list.sort(key=itemgetter(count_index), reverse=True)
    return word_list


def write_word_counts_to_files(user_word_dict_of_lists: dict) -> None:
    for user, word_list in user_word_dict_of_lists.items():
        with open(f"data/{user}.{OUTPUT_FILE_EXTENSION}", "w") as f:
            f.write(f"word,count\n")
            for pair in word_list:
                f.write(f"{pair[0]},{pair[1]}\n")


def main():
    user_word_count_dictionary = get_user_word_dictionary_from_csv(
        CHAT_LOG_FILE, get_word_set_from_file(IGNORED_USERS_FILE)
    )

    user_word_list = {}

    for user, word_dict in user_word_count_dictionary.items():
        make_word_cloud(word_dict, user)
        user_word_list[user] = get_sorted_word_count_list_from_word_dictionary(
            word_dict
        )

    write_word_counts_to_files(user_word_list)


if __name__ == "__main__":
    main()
