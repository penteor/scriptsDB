from dateutil.rrule import *
from dateutil.parser import *
from datetime import *

# http://labix.org/python-dateutil#head-1f7c5d0c956a96f26aa1de60b861f4d58180c1dd

start= parse("05/01/2021")   # Third Sunday in May 2021
until = parse("05/30/2021")   # until MM/dd/YYYY


recurring_daily = rrule(DAILY, dtstart=start, until=until)
recurring_days_interval = rrule(DAILY, dtstart=start, until=until, interval=2)


recurring_weekly = rrule(WEEKLY, dtstart=start, until=until)
recurring_weeks_interval = rrule(WEEKLY, dtstart=start, until=until, interval=2)
# Weekly on Tuesday and Thursday, wkst - week start
recurring_weekdays = rrule(WEEKLY, dtstart=start, until=until, wkst=SU, byweekday=(TU,TH))
# Every other week on Tuesday and Thursday
recurring_weekdays_interval = rrule(WEEKLY, dtstart=start, until=until, wkst=SU, byweekday=(TU,TH), interval=2)
# Monthly on the 1st Friday
recurring_monthly_day = rrule(MONTHLY, dtstart=start, until=until, wkst=SU, byweekday=FR(1))
# Every other month on the 1st and last Sunday of the month
recurring_monthly_days_interval = rrule(MONTHLY, dtstart=start, until=until, wkst=SU, byweekday=(SU(1), SU(-1)), interval=2)
# Monthly on the second to last Monday of the month
list(rrule(MONTHLY, dtstart=start, until=until, byweekday=MO(-2)))
# Monthly on the third to the last day of the month
list(rrule(MONTHLY, dtstart=start, until=until, bymonthday=-3))
# Monthly on the 2nd and 15th of the month
list(rrule(MONTHLY, dtstart=start, until=until, bymonthday=(2,15)))
# Monthly on the first and last day of the month
list(rrule(MONTHLY, dtstart=start, until=until, bymonthday=(-1,1,)))

all_dates_time = map(str,recurring_monthly_days_interval)
#only_days = [d.strftime('%d/%m/%Y') for d in recurring[::2]]

print(all_dates_time)



#https://towardsdatascience.com/scheduling-all-kinds-of-recurring-jobs-with-python-b8784c74d5dc