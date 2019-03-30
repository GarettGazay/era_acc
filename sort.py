import csv
import glob
import re
import time

#////////////////////////////////////////

### ERA SORTING + ACCOUNTING SOFTWARE ###

#////////////////////////////////////////


# read data from all the ERA files
era_data = []
path = glob.glob('*.csv')
for i in path:
    print('DATA FROM ',i)
    # Read in 835 pre sorted file
    with open(i,'r') as era_read_file:
            csv_reader = csv.reader(era_read_file)
            next(era_read_file)
            for row in csv_reader:
                era_data.append(row)
# print(era_data[0])
# exit()
print('####### ',i,' #######')
time.sleep(1)
# Remove all milage data from era_data list
for line in era_data:
    if line[4] == 'A0380':
        era_data.remove(line)


# Format dates
for line in era_data:
    x = re.sub(r'/','-', line[1])
    x = x.split('-')
    month,day,year = x[0],x[1],x[2]
    line[1] = year+'-'+month+'-'+day
    line[2] = year+'-'+month+'-'+day

# Format names
for line in era_data:
    x = line[0].split('.')
    first = x[1].lower()
    last = x[0].lower()
    line[0] = first
    line[6] = last

# Read data from all roster files in directory
roster_data = []
path = glob.glob('roster_files/*.csv')
for i in path:
    # print('DATA FROM ',i)
    # Read in 835 pre sorted file
    with open(i,'r') as roster_read_file:
            csv_reader = csv.reader(roster_read_file)
            next(roster_read_file)
            for row in csv_reader:
                roster_data.append(row)
for line in roster_data:
    first = line[0].lower()
    last = line[1].lower()
    line[0] = first
    line[1] = last

# Compare roster_data to era_data (names and dates to include drivers)
# Submit final era_data into final_list for writing to file

# Write result to file
with open('output/era_trips.csv','w', newline='') as new_file:
    csv_writer = csv.writer(new_file, delimiter=',')
    headers = ['name','start_date','end_date','charges','procedure_code','claim_paid','','check_number','driver1','driver2']
    csv_writer.writerow(headers)
    #Roster compare data
    for i in roster_data:
        for j in era_data:
            r_first = i[0]
            r_first = re.sub(r' ','', r_first)
            r_last =  i[1]
            r_last = re.sub(r' ','', r_last)
            r_date = i[11]
            r_date = re.sub(r' ','', r_date)
            r_driver1 = i[22]
            r_driver2 = i[23]

            e_first = j[0]
            e_first = re.sub(r' ','', e_first)
            e_last = j[6]
            e_last = re.sub(r' ','', e_last)
            e_date = j[1]
            e_date = re.sub(r' ','', e_date)

            # Remove all special characters from strings
            r_first = re.sub('[^A-Za-z0-9]+', '', r_first)
            r_last = re.sub('[^A-Za-z0-9]+', '', r_last)
            e_first = re.sub('[^A-Za-z0-9]+', '', e_first)
            e_last = re.sub('[^A-Za-z0-9]+', '', e_last)

            # Re spell certain names
            if r_last == "cortez" and r_first == 'augstin':
                r_last = 'cortes'
                r_first = 'agustin'

            if r_last == 'conseco':
                r_last = 'canseco'



            # If no special cases check for normal length names
            if r_first[:3] == e_first[:3] and r_last[:3] == e_last[:3] and r_date == e_date:
                csv_writer.writerow([e_last+' '+e_first,j[1],j[2],j[3],j[4],j[5],'',j[7],r_driver1,r_driver2, ])
                print('written to file: ', j)

            # check for particularly troublesome names
            if r_first[:2] == 'an' and r_last[:2] == 'to' and e_first[:2] == 'an' and e_last[:2] == 'to' and r_date == e_date:
                csv_writer.writerow([e_last+' '+e_first,j[1],j[2],j[3],j[4],j[5],'',j[7],r_driver1,r_driver2, ])
                print('special case: ',r_first,r_last ,' and ', e_first,e_last)

            if  r_first[:2] == 'fe' and r_last[:3] == 'rod' and e_first[:2] == 'fe' and e_last[:3] == 'rod' and r_date == e_date:
                csv_writer.writerow([e_last+' '+e_first,j[1],j[2],j[3],j[4],j[5],'',j[7],r_driver1,r_driver2, ])
                print('special case: ',r_first,r_last ,' and ', e_first,e_last)
