import csv


def main():
    with open("studentsList.csv", "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        data = [row for row in reader]
        print(data)


if __name__ == "__main__":
    main()
