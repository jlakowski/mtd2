#!/usr/bin/python

import appindicator
import pynotify
import gtk
import urllib2
import json
import bus
import datetime
import dateutil.parser


a = appindicator.Indicator('bus_indicator', 'headlogo.svg', appindicator.CATEGORY_APPLICATION_STATUS)
a.set_status( appindicator.STATUS_ACTIVE )
#make the menu
m = gtk.Menu()
ci = gtk.MenuItem( 'Check' )
qi = gtk.MenuItem( 'Quit' )

m.append(ci)
m.append(qi)

a.set_menu(m)
ci.show()
qi.show()
global timear
def checkBuses(item):
        
        # TODO get rid of duplicates                                                      

        #http://youtu.be/8cdrJA3PbEw                                                      
        #http://xmodulo.com/how-to-parse-json-string-in-python.html                       
        response = urllib2.urlopen('http://developer.cumtd.com/api/v2.2/json/GetStopTimesByStop?stop_id=GRN2ND&key=df3b74de7191467e8a8529501cf5462d')
        json_data = response.read()

        #print json_data                                                                  
        decoded = json.loads(json_data)

        buses =[]

        currenttime = datetime.datetime.now()
        flag = True
        for i in range(len(decoded['stop_times'])):
            try:
                    timear = dateutil.parser.parse(decoded['stop_times'][i]['arrival_time'])
            except:
                    pass
                        
            dirar = decoded['stop_times'][i]['trip']['direction']
            routear = decoded['stop_times'][i]['trip']['route_id']
            
            b = bus.bus(routear, timear, dirar)

            buses.append(b)

            if( timear > currenttime and flag):
                    indstart = i
                    flag = False
        
        time = []
        route = []
        for k in range(indstart, indstart + 3):

                time.append(buses[k].time.time())
                route.append(buses[k].route + buses[k].direction)

        # show the notification message
        # TODO CHANGE this to show 5 buses
        pynotify.init('bus_indicator')
        n = pynotify.Notification(
                '<b>CUMTD Buses @ Green and Second</b>',
                'time: %s   route: %s \n time: %s  route: %s' %(time[0], route[0], time[1], route[2]),
                'notification-message-im')
        n.show()

ci.connect('activate', checkBuses)

def quit(item):
        gtk.main_quit()

qi.connect('activate', quit)

gtk.main()
