month_day_list = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def tommorow(date):
    year = int(date["year"])
    month = int(date["month"])
    day = int(date["day"])

    if year % 4 == 0:
        month_day_list[2] = 29
    if year % 100 == 0:
        month_day_list[2] = 28
    if year % 400 == 0:
        month_day_list[2] = 29

    day += 1

    if day == month_day_list[month] + 1:
        month += 1
        day = 1
    elif day > month_day_list[month] + 1:
        print("?????")
        return

    if month  ==  13:
        year += 1
        month = 1
        day = 1

    date = {}
    date["year"] = year
    date["month"] = month
    date["day"] = day

    return date