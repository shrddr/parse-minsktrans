# -*- coding: utf-8 -*-
"""
Created on Mon Oct 07 11:38:45 2013

@author: user

http://www.minsktrans.by/city/minsk/routes.txt
http://www.minsktrans.by/city/minsk/stops.txt
http://www.minsktrans.by/city/minsk/times.txt
"""

import csv

LOCAL = True


inf = 'stops.txt'
stops = []

with open(inf, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in reader:
        stops.append(row)
        
sterms = stops[0]        
stops = stops[1:]
ss = {}

id = 0
for s in stops:
    if (len(s[0]) > 0): id = int(s[0]) #some have empty id
    ss[id] = s[1:]
    ln = float(s[6])/100000
    la = float(s[7])/100000
    if (ln+la > 0):             #some have zero coords
        ss[id].append(ln) #9
        ss[id].append(la) #10
        ss[id].append(0) #11
        
print('{} stops'.format(len(ss)))
#ss = stopid-based dictionary + zero usage




inf = 'times.txt'
times = []

with open(inf, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        times.append(row)
        
tterms = times[0]
times = times[1:]

usage = {} #per friday+saturday
       
for t in times:
    id = int(t[0])         
    t.pop(0)
    count = 0
    for number in t:
        if (len(number) < 1): break #until ,,
        count += 1
    usage[id] = count

print('{} route timetables'.format(len(times)))    
#usage = routeid based dictionary holding carcount    
    
    



inf = 'routes.txt'
routes = []

with open(inf, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in reader:
        routes.append(row)
        
#routes[54][14] = stoplist
print('{} routes'.format(len(routes)))
        
rterms = routes[0]
routes = routes[1:]

rs = {}

stoplists = []

id = '?'
for r in routes: 
    if (len(r[12]) > 0):
        id = int(r[12])
        r.pop(12)
        rs[id] = r
        
        stops = r[13].split(',') #stop list
        stoplists.append(stops)
        
        for s in stops:
            if (len(s) > 0):
                sid = int(s)
                try:
                    ss[sid][11] += usage[id] #increment each stop usage with this route car count
                except:
                    1
                
        
                
              

#rs[routeid][13] = stops
    

 
    

lng = []
lat = []
weight = []

for k in ss:
    try:
        if (ss[k][11] > 1):
            lng.append(ss[k][9])
            lat.append(ss[k][10])
            weight.append(ss[k][11])
    except:
        1

graph = {}
# startid => [ endid=>count, endid=count, ...]

for stoplist in stoplists:
    segs = zip(stoplist[:-1], stoplist[1:])
    for seg in segs:
        start = int(seg[0])
        end = int(seg[1])
        
        if start in graph:
            1
        else:
            graph[start] = {}
            
        if end in graph[start]:
            graph[start][end] += 1
        else:
            graph[start][end] = 1

segs = []
#[ [ [startx,y], [endx,y] ],
#  [],
#]
segweights = []
  
for startid in graph:
    for endid in graph[startid]:
        try:
            segs.append([
                         [ ss[startid][9], ss[startid][10] ],
                         [ ss[endid][9], ss[endid][10] ]
                        ]) 
            segweights.append(graph[startid][endid])
        except:
            print(startid)
            print(ss[startid])





import math
import matplotlib.pyplot as plt
import numpy as np

import matplotlib as mpl

class nlcmap(mpl.colors.LinearSegmentedColormap): 
    name = 'nlcmap'
    
    def __init__(self, cmap, levels):
        self.cmap = cmap
        # @MRR: Need to add N for backend
        self.N = cmap.N
        self.monochrome = self.cmap.monochrome
        self.levels = np.asarray(levels, dtype='float64')
        self._x = self.levels / self.levels.max()
        self._y = np.linspace(0.0, 1.0, len(self.levels))
    
    #@MRR Need to add **kw for 'bytes'
    def __call__(self, xi, alpha=1.0, **kw):
        """docstring for fname"""
        # @MRR: Appears broken? 
        # It appears something's wrong with the
        # dimensionality of a calculation intermediate
        #yi = stineman_interp(xi, self._x, self._y)
        yi = np.interp(xi, self._x, self._y)
        return self.cmap(yi, alpha)


    

    
    


cx = 27.555
cy = 53.9
rad = 0.09 #y-deg

cmap = mpl.colors.LinearSegmentedColormap.from_list('bgyr-gamma','gyr')
#cmap_nonlin = colors.LinearSegmentedColormap.from_list('bgyr-gamma','bgyr',gamma=0.15)
sc = plt.scatter(lng, lat, s=50, c=weight, cmap=cmap, norm=mpl.colors.LogNorm())
plt.axis([cx-rad/math.cos(math.radians(cy)), cx+rad/math.cos(math.radians(cy)), cy-rad, cy+rad])

plt.colorbar()















segweights = np.array(segweights, float)
segweights /= segweights.max()
segweights = np.sqrt(segweights)

fig = plt.figure(figsize=(15,20))

ax = plt.axes()
plt.axis([cx-rad/math.cos(math.radians(cy)), cx+rad/math.cos(math.radians(cy)), cy-rad, cy+rad])
cm = plt.get_cmap('jet')

line_segments = mpl.collections.LineCollection(segs,
                                linewidths    = 0.4,
                                colors        = [cmap(w) for w in segweights],
                                linestyle = 'solid')
ax.add_collection(line_segments)
ax.set_title('')
plt.show()


#from matplotlib.backends.backend_pdf import PdfPages
#pp = PdfPages('multipage.pdf')
#pp.savefig()
#pp.close()