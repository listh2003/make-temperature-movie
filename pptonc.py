import iris

def main():
   mon = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
   
   yr1 = 2040
   yrn = 2101
   
   for year in range(yr1, yrn):
     for month in mon:
       name = 'bh456a.p5' + str(year) + month
       ppfile = name + '.pp'
     
       data = iris.load_cube(ppfile)
     
       ncfile = name + '.nc'
       print ncfile
     
       iris.save(data, ncfile)
     
if __name__ == '__main__':
    main()

