from calendar import HTMLCalendar
from .models import Training


class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    def formatday(self, day, trainings):
        trainings_per_day = trainings.filter(start_time__day=day)
        d = ''
        for training in trainings_per_day:
            d += f'<li><a href="training/{training.id}/">{training.title}</a></li>'

        if day != 0:
            return f'<td><span class="date">{day}</span><ul> {d} </ul></td>'
        return '<td></td>'

    def formatweek(self, theweek, trainings):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, trainings)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        trainings = Training.objects.filter(start_time__year=self.year, start_time__month=self.month)

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, trainings)}\n'
        return cal
