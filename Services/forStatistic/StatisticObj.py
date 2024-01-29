import db.database as db
import datetime
from dateutil.relativedelta import relativedelta
from plotnine import ggplot, aes, geom_line, theme, element_text
import pandas as pd

class StatisticObj:
    def __init__(self):
        pass

    def get_file_name_and_count_statistic(self, start: datetime.datetime, end: datetime.datetime, user_id: str, by:str = "day", filtr:str = None):
        Y = []
        X = []
        total = 0
        list_event = db.get_events_by_datetime(start, end, filtr)
        count = 0
        current = start
        while (current.date() < end.date()):
            # print(X, "\n", Y, "\n", current)
            for i in list_event:
                if by == "day":
                    if current.date() == i.date_event.date():
                        count += 1
                        total += 1
                    else:
                        X.append(str(current.date()))
                        Y.append(count)
                        count = 0
                        current = current + datetime.timedelta(days=1)
                elif by == "month":
                    if current.date().month == i.date_event.date().month and current.date().year == i.date_event.date().year:
                        count += 1
                        total += 1
                    else:
                        X.append(str(current.date()))
                        Y.append(count)
                        count = 0
                        current = current + relativedelta(months=1)
                elif by == "year":
                    print("Curent", current.date().year)
                    print("EVENT", i.date_event.date().year)
                    if current.date().year == i.date_event.date().year:
                        count += 1
                        total += 1
                    else:
                        X.append(str(current.date()))
                        Y.append(count)
                        count = 0
                        current = current + relativedelta(years=1)
            if count != 0:
                if by == "day":
                    X.append(str(current.date()))
                    Y.append(count)
                    count = 0
                    current = current + datetime.timedelta(days=1)
                elif by == "month":
                    X.append(str(current.date()))
                    Y.append(count)
                    count = 0
                    current = current + relativedelta(months=1)
                elif by == "year":
                    X.append(str(current.date()))
                    Y.append(count)
                    count = 0
                    current = current + relativedelta(years=1)
        if count != 0:
            X.append(str(current.date()))
            Y.append(count)
        data = pd.DataFrame({
            'Дата': X,
            'Підписки': Y
        })
        chart = ggplot(data, aes(x='Дата', y='Підписки', group=1)) + geom_line() + theme(
            axis_text_x=element_text(angle=90))
        chart.save("tmp_stat/"+user_id+".png", dpi=300)
        return "tmp_stat/"+user_id+".png", total