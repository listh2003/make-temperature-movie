import iris

def convert_montly():
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

     
def convert_daily():
   
   dirname = 'gpp_chlrphyl_1850/'
   for month in range(1, 13):
     for day in range(1, 31, 10):
       name = 'bk179a.p61850{:02d}{:02d}'.format(month,day)
       ppfile = dirname + name + '.pp'
       
       data = iris.load(ppfile)
       
       ncfile1 = dirname + 'chlrphyl/' + name + '.nc'
       ncfile2 = dirname + 'gpp/' + name + '.nc'      
       
       iris.save(data[0], ncfile1)
       iris.save(data[1], ncfile2) 


def main():
   convert_daily()
   
        
if __name__ == '__main__':
    main()

