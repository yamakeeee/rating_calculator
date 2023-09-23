import requests
import datetime
import math
import sys


def time_parser(time: str):
    year, month, day = time.split("-")
    return int(year), int(month), int(day.split("T")[0])


def is_in_period(year, month, day, period):
    now = datetime.datetime.now()
    last = now + datetime.timedelta(weeks=-period*4)
    if year > last.year:
        return True
    elif year < last.year:
        return False
    if month > last.month:
        return True
    elif month < last.month:
        return False
    if day >= last.day:
        return True
    else:
        return False


def calculate_rating(rated_contests, period):
    sm = 0
    bunbo = 0
    for i in range(len(rated_contests)):
        performance = rated_contests[i][3]
        sm += math.pow(2, performance/800)*math.pow(0.9, i+1)
        bunbo += math.pow(0.9, i+1)
    rating = 800 * math.log(sm/bunbo, 2)
    print(f"period = {period} month")
    print(f"rated contest num = {len(rated_contests)}")
    print(f"rating = {rating}")


def main():
    user_name = sys.argv[1]
    period = int(sys.argv[2])
    url = f"https://atcoder.jp/users/{user_name}/history/json"
    response = requests.get(url)
    user_info = response.json()
    rated_contests = []
    for info in user_info:
        year, month, day = time_parser(info["EndTime"])
        if info["IsRated"] and is_in_period(year, month, day, period):
            rated_contests.append([year, month, day, info["Performance"]])
    rated_contests.sort()
    rated_contests.reverse()
    if len(rated_contests) == 0:
        print("no rated contest")
        exit(0)
    calculate_rating(rated_contests, period)


if __name__ == "__main__":
    main()
