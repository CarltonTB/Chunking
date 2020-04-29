# Author: Carlton Brady
import re
import os


class DateEntityRecognizer:

    def __init__(self):
        self.date_expression = re.compile("(((([0-9]{1,2})[ ])?([Jj]une|[Jj]uly|[Aa]ugust|[Ss]eptember|[Oo]ctober|[Nn]ovember"
                                          "|[Dd]ecember|[Jj]anuary|[Ff]ebruary|[Mm]arch|[Aa]pril|[Mm]ay),?[ ][0-9]{4})|"
                                          "(([Jj]une|[Jj]uly|[Aa]ugust|[Ss]eptember|[Oo]ctober|[Nn]ovember"
                                          "|[Dd]ecember|[Jj]anuary|[Ff]ebruary|[Mm]arch|[Aa]pril|[Mm]ay)[ ]([0-9]{1,2}),?[ ]([0-9]{4})?))")

    def parse_files(self, files):
        count = 0
        for file_name in files:
            infile = open("wiki/" + file_name)
            lines = infile.readlines()
            outfile = open("results/" + file_name.replace(".txt", "") + "_results.txt", "w")
            for line in lines:
                match = self.date_expression.search(line)
                if match is not None:
                    print(match.group())
                    outfile.write(match.group())
                    outfile.write("\n")
                    count += 1
            infile.close()
        print("Count of date entities:", count)


def get_wiki_files():
    files = os.listdir(os.path.curdir+"/wiki")
    for file_name in files:
        if ".txt" not in file_name:
            files.remove(file_name)
    return files


if __name__ == "__main__":
    der = DateEntityRecognizer()
    der.parse_files(get_wiki_files())
