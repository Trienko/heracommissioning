from casa import table as tb
obstablename="/home/trienko/HERA/software/casa-release-4.7.1-el7/data/geodetic/Observatories/"
tb.open(obstablename,nomodify=False)
paperi =(tb.getcol("Name")=="PAPER_SA").nonzero()[0]
tb.copyrows(obstablename,startrowin=paperi,startrowout=-1,nrow=1)
tb.putcell("Name",tb.nrows()-1,"HERA")
tb.close()