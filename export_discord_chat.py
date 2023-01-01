import os
import sys
import glob
import pandas as pd


def combine_pdfs() -> None:
    file_names = [i for i in glob.glob("*.csv")]
    new_csv = pd.concat([pd.read_csv(f) for f in file_names])
    new_csv.to_csv("discord_logs.csv", index=False, encoding="utf-8-sig")


def main():
    if len(sys.argv) != 3:
        print("Please enter file name with channel IDs and your token.")
        sys.exit()

    file_name = sys.argv[1]
    TOKEN = sys.argv[2]

    CWD = os.getcwd()
    with open(file_name, "r") as f:
        os.chdir("./data")
        for line in f:
            CHANNELID = line.strip()
            os.system(
                f"docker run --rm -v {CWD}/data:/out tyrrrz/discordchatexporter:stable export -t {TOKEN} -c {CHANNELID} -f csv"
            )
    combine_pdfs()


if __name__ == "__main__":
    main()
