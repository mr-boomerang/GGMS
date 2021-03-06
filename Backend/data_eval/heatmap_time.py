import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import sys
import mysql.connector
from mysql.connector import Error


bin_num = []
weight = []
lat = []
long = []
hist_data = []
time = []
date = []
day_analysis = np.zeros(13)
weekly_analysis = np.zeros(7)

hmp_x = []
hmp_y = []
data = []
def main():
    conn = None

    try:
        conn = mysql.connector.connect(host='localhost',
                                       database='grievance_data',
                                       user='root',
                                       password='password')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM grievances")
        rows = cursor.fetchall()
        for row in rows:
            bin_num.append(row[1])
            weight.append(row[3])
            lat.append(float(row[6]))
            long.append(float(row[7]))
            date.append(int(row[4]))
            time.append(row[5])

        start = sys.argv[1]
        end = sys.argv[2]
        i = 0
        for x in time:
            if(start <= x and end >= x):
                x = float((round(lat[i],4)-74.02)*100)
                y = float((round(long[i],4)-74.02)*100)
                print(x)
                hmp_x.append(x)
                hmp_y.append(y)
                data.append(weight[i])
            i+=1



        heatmap, xedges, yedges = np.histogram2d(hmp_x, hmp_y)
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

        print(hmp_x)
        # Plot heatmap
        plt.clf()
        plt.ylabel('y')
        plt.xlabel('x')
        plt.imshow(heatmap, extent=extent)
        #plt.plot(hmp_x,hmp_y)
        plt.savefig('./data_eval/heatmap_time.png')


    except Error as e:
        print(rows)
    finally:
        cursor.close()
        conn.close()

if __name__=="__main__":
    main()
