import os
import sys


def main():
    if len(sys.argv) != 3:
        print("Please enter file name with channel IDs and your token.")
        sys.exit()

    file_name = sys.argv[1]
    TOKEN = sys.argv[2]
    CHANNELID = ""
    CWD = os.getcwd()

    with open(file_name, "r") as f:
        for line in f:
            CHANNELID = line.strip()
            os.system(
                f"docker run --rm -v {CWD}:/app/out tyrrrz/discordchatexporter:stable export -t {TOKEN} -c {CHANNELID} -f csv"
            )


if __name__ == "__main__":
    main()
