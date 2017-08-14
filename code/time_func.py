def time_convert(mytime, myunit='s'):
    #if type(mytime).__name__ <> 'list': mytime=[mytime]
    myTimestr = []
    #for time in mytime:
    for k in xrange(len(mytime)):  
        q1=qa.quantity(mytime[k],myunit)
        time1=qa.time(q1,form='ymd')
        myTimestr.append(time1)
    return myTimestr
