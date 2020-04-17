import datetime
def generate_year():
    start = 2015
    list = []
    for a in range(5):
        start=start+1
        list.append(start)
    return list

def generate_mon():
    mon = {0: 'Январь', 1: 'Февраль', 2: 'Март', 3: 'Апрель', 4: 'Май', 5: 'Июнь', 6: 'Июль', 7: 'Август',
           8: 'Сентябрь', 9: 'Октябрь', 10: 'Ноябрь', 11: 'Декабрь'}
    return mon

def generate_day(year,mon):
    days = []
    if year%4 == 0 and mon == 'Февраль':
        days = [i for i in range(1,30)]
    else:
        days = [i for i in range(1,32)]
    return days
def difference(dt,dt1):
    l_dt = dt.split('-')
    l_dt1 = dt1.split('-')
    dt_ = datetime.datetime(int(l_dt[0]),int(l_dt[1]),int(l_dt[2]))
    dt__ = datetime.datetime(int(l_dt1[0]), int(l_dt1[1]), int(l_dt1[2]))
    if dt_<dt__:
        return True
    else:
        return False