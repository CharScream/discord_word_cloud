"""
TODO: For 2023
1. Look into only grabbing content from current year.
2. refactor? Run time trash
3. Specific channel integration
"""
import pandas as pd
from operator import itemgetter
from wordcloud import WordCloud
from typing import List, Tuple, Set
import dateparser

CHAT_LOG_FILE = "./data/discord_logs.csv"
COMMON_WORD_FILE = "common_words.txt"
IGNORED_USERS_FILE = "ignored_users.txt"
OUTPUT_FILE_EXTENSION = "csv"


def get_word_set_from_file(file_name: str, comment_character: str = "~") -> Set[str]:
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
            cleaned_line = line.lower().replace(",", "").split()
            for word in cleaned_line:
                word_set.add(word)
    return word_set


def get_user_word_dictionary_from_csv_with_years(
    file_name: str, user_ignore_list: set, aggregate: bool = False
) -> dict[str, dict[int, dict[str, int]]]:
    """
    :param file_name: csv file with discord logs
    :param user_ignore_list: file with list of users to ignore
    :return: a dictionary in the form of {username : {year : {word : count}}}
    """
    df = pd.read_csv(file_name)
    df2 = df.loc[:, ["Author", "Date", "Content"]]
    special_characters_pattern = r"[^A-Za-z'0-9:@ ]"

    df2.replace(
        to_replace=special_characters_pattern, value=" ", inplace=True, regex=True
    )

    user_word_count_dictionary = {}
    common_word_set = get_word_set_from_file(COMMON_WORD_FILE)
    for row in df2.itertuples(index=False):
        if pd.isna(row.Content):
            continue

        if aggregate:
            user = "_server"
        else:
            user = row.Author.strip().split()[0]
            if user.lower() in user_ignore_list:
                continue

        if user not in user_word_count_dictionary:
            user_word_count_dictionary[user] = {}

        current_author_dictionary = user_word_count_dictionary[user]

        year = dateparser.parse(row.Date).year

        # want to store our words in here
        if year not in current_author_dictionary:
            current_author_dictionary[year] = {}

        # remove lower here so we can have correctly formatted emotes
        for word in row.Content.replace('""', "").split():
            # ignores single letter artifacts from emotes
            if word.lower() in common_word_set or len(word) == 1:
                continue
            # shadowing because fuck it
            # we assume words wrapped in : are emotes, all other words are made lower case
            if word[0] != ":" or word[-1] != ":":
                word = word.lower()

            if word not in current_author_dictionary[year]:
                current_author_dictionary[year][word] = 1
                continue

            current_author_dictionary[year][word] += 1

    return user_word_count_dictionary


def make_word_cloud(
    word_dict: dict, user: str, max_words: int = 3000, year: int = None
) -> None:
    if not word_dict:
        return
    if year:
        year = f"-{year}"
    word_cloud = WordCloud(scale=10, background_color="white", max_words=max_words)
    word_cloud.generate_from_frequencies(word_dict)
    word_cloud.to_file(f"clouds/{user}{year}-word-cloud.jpg")


def get_sorted_word_count_list_from_word_dictionary(
    word_dictionary: dict, count_index: int = 1
) -> List[Tuple[str, int]]:
    word_list = [(word, count) for word, count in word_dictionary.items()]
    word_list.sort(key=itemgetter(count_index), reverse=True)
    return word_list


def write_yearly_word_counts_to_files(
    user_word_dict_of_lists: dict[int, dict[list[tuple[str, int]]]]
) -> None:
    for user, years in user_word_dict_of_lists.items():
        for year, word_list in years.items():
            with open(f"data/{user}-{year}.{OUTPUT_FILE_EXTENSION}", "w") as f:
                f.write(f"word,count\n")
                for pair in word_list:
                    f.write(f"{pair[0]},{pair[1]}\n")


def create_aggregates() -> None:
    global_counts = get_user_word_dictionary_from_csv_with_years(
        file_name=CHAT_LOG_FILE, user_ignore_list=set(), aggregate=True
    )

    global_word_list = {}
    global_word_list["_server"] = {}

    for year, word_dict in global_counts["_server"].items():
        make_word_cloud(user="SERVER", word_dict=word_dict, year=year)
        global_word_list["_server"][
            year
        ] = get_sorted_word_count_list_from_word_dictionary(word_dict)

    write_yearly_word_counts_to_files(global_word_list)


def create_clouds_and_lists() -> None:
    user_word_count_dict_by_years = get_user_word_dictionary_from_csv_with_years(
        file_name=CHAT_LOG_FILE,
        user_ignore_list=get_word_set_from_file(IGNORED_USERS_FILE),
    )

    user_word_list_years = {}

    for user, years in user_word_count_dict_by_years.items():
        user_word_list_years[user] = {}
        if years:
            for year, word_dict in years.items():
                if year:
                    make_word_cloud(user=user, word_dict=word_dict, year=year)
                    user_word_list_years[user][
                        year
                    ] = get_sorted_word_count_list_from_word_dictionary(word_dict)

    write_yearly_word_counts_to_files(user_word_list_years)


def main():
    create_clouds_and_lists()
    create_aggregates()


if __name__ == "__main__":
    main()
