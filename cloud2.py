import os
import datetime
import pandas as pd
from sklearn.cluster import KMeans
from pandas import Series,DataFrame
import pygal

application=Flask(__name__)
app=application


@app.route('/')
def index():
        return render_template("index.html")

@app.route('/upload',methods=['POST'])
def upload():
        cdict = {}
        f1 = request.files['file1']
        col1=request.form['col1']
        col2=request.form['col2']
        nclusters = int(request.form['nclusters'])
                
        #processing starts
        eq = pd.read_csv(f1.filename)
        tf2 = DataFrame(eq,columns=([col1,col2]))        
        tf2 = tf2.dropna()        
        time1 = datetime.datetime.now()
        kmeans_model = KMeans(n_clusters=nclusters, random_state=1).fit(tf2)
        labels = kmeans_model.labels_
        clustercenters = kmeans_model.cluster_centers_
        inertia = kmeans_model.inertia_
        print('labels' ,labels)
        print('clustercenters' ,clustercenters)
        print('inertia',inertia)       
        ind = 0
        for i in range(len(labels)):
            l = []
            ll = []
            lll = []
            try:
                ts2s = tf2.ix[ind]
                ind = ind + 1
            except KeyError:
                #continue
                ind = ind + 1
                flag = 1
                while (flag == 1):
                    try:
                        ts2s = tf2.ix[ind]
                        flag = 0
                        ind = ind + 1
                    except KeyError:
                        ind = ind + 1
            tf2d = ts2s.to_dict()
            l1 = tf2d[col1]
            l2 = tf2d[col2]
            l.append(l1)
            l.append(l2)
            ll.append(l)

            for j in range(nclusters):
                if labels[i] == j:
                    jstr = "'" +str(j)  + "'"
                    try:
                        a = (cdict[jstr])
                        a.append(l)
                        cdict[jstr] = a
                    except KeyError:
                        lll.append(l)
                        cdict[jstr] = lll
                    break        

        ld = len(cdict)      
        # to calculate no of data points
        cp = []
        for k,v in cdict.items():
            cc = cdict[k]          
            cp.append(len(cc))      

        time2 = datetime.datetime.now()
        timet = time2 - time1
        cps = []
        cps = cp.sort()
        
        #creating bar chart
        bar_chart = pygal.Bar()  # Then create a bar graph object
        bar_chart.add('no of cluster  points', cp)
        bar_chart.render_to_file('nxy12_barchart.svg')

        # creating bar chart
        bar_chart = pygal.Bar()  # Then create a bar graph object
        #bar_chart.add('no of cluster  points', cp)
        for k in range(len(cp)):
            strk = "'" + str(k) + "-" +str( cp[k]) + "'"
            bar_chart.add(strk, cp[k])

        bar_chart.render_to_file('nxy12a_barchart.svg')

        #creating chart
        xy_chart = pygal.XY(stroke=False)
        xy_chart.title = 'Correlation Here'
        for k in range(ld):
            strk = "'" +str(k) +"'"
            xy_chart.add(strk, cdict[strk])

        xy_chart.render_to_file('nxy10_chart.svg')

        # creating chart for centroids
        xy_chart = pygal.XY(stroke=False)
        xy_chart.title = 'Correlation Here2'
        for k in range(nclusters):
            strk = "'" + str(k) + "'"
            xy_chart.add(strk, clustercenters[k])

        xy_chart.render_to_file('nxy11_chart.svg')

        results = "\n no of clusters= " +str(ld)  +"\n centroids are= " +str(clustercenters)  + "\n no of cluster points = " +str(cp) +" time need to run = " +str(timet)
        return render_template("upload.html",results=results)


if __name__== "__main__":
        app.run(host="ec2-aws")


