# -*- coding: utf-8 -*-
#Database calls

##Copyright (C) 2012 Magnus Haw
##
##This program is free software: you can redistribute it and/or modify
##it under the terms of the GNU General Public License as published by
##the Free Software Foundation, either version 3 of the License, or
##(at your option) any later version.
##
##This program is distributed in the hope that it will be useful,
##but WITHOUT ANY WARRANTY; without even the implied warranty of
##MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##GNU General Public License for more details.
##
##You should have received a copy of the GNU General Public License
##along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sqlite3
from numpy import array,loadtxt
from calcs import *
from mylists import objectcols

#---------------------------------------------------------------------------

"""create table constellations (
        name            text not null,
        Abbr            char(3) not null primary key,
        RA              real not null,
        Dec             real not null,
        Area_sqdeg      real not null,
        description     text,
        image           text);      
"""

"""create table object_types (
        id              char(1) not null primary key,
        name            text not null,
        description     text,
        link            text
        );
"""

"""create table objects (
        name            text not null,
        id              varchar(8) not null primary key,
        type            char(1) not null references object_types(id),
        magnitude       real not null,
        size            real not null,
        distance_kly    real not null,
        constellation   char(3) not null references constellations(Abbr),
        RA              real not null,
        dec             real not null,
        finding_chart   text not null,
        image           text,
        description     text,
        other_names     text,
        link            text,
        comments        text
);

"""

"""create table defaults (
        name            text not null primary key,
        lat             real not null,
        long            real not null,
        late            INTEGER not null,
        lim             INTEGER not null,
        alt             INTEGER not null
);

"""

#---------------------------------------------------------------------------

def concatenate(mylist):
    if mylist == None:
        return ''
    mystr =mylist[0]
    for i in range(1,len(mylist)):
        mystr += ','+str(mylist[i])
    return mystr

def format_cond(listcond):
    mystr =listcond[0]
    for i in range(1,len(listcond)):
        mystr += ' and '+str(listcond[i])
    return mystr

def select(dname,table,columns=['*'],conditions=None,order=None,limit=None,offset=None):
    conn = sqlite3.connect(dname)
    c = conn.cursor()
    mycmd = "SELECT "+concatenate(columns)+" FROM "+table
    if conditions != None:
        mycmd += " WHERE "+format_cond(conditions)
    if order != None:
        mycmd += " ORDER BY " + order
    if limit != None:
        mycmd += " LIMIT " + str(limit)
    if offset != None:
        mycmd += " OFFSET " + str(offset)
    mycmd +=';'
    print mycmd
    c.execute(mycmd)
    data = c.fetchall()
    c.close()
    conn.close()
    return array(data)

def alter_cell(dname,table,value,column,rowid,refcol):
    mycmd = 'UPDATE '+table+' SET ' + column + '=? WHERE '+refcol+'='+'"'+rowid+'"'+';'
    conn = sqlite3.connect(dname)
    c = conn.cursor()
    print mycmd
    c.execute(mycmd,value)
    conn.commit()
    c.close()
    conn.close()

def add_row(dname,table,myrow):
    conn = sqlite3.connect(dname)
    c = conn.cursor()
    mycmd = "insert into "+table+" values (?"
    for i in range(1,len(myrow)):
        mycmd += ',?'
    mycmd += ')'
    #print myrow
    
    c.execute(mycmd,myrow)
    conn.commit()
    c.close()
    conn.close()

def update_row(dname,table,rowid,myrow,columns,refcol='id'):
    oldvalues = select(dname,table,conditions=["%s='%s'"%(refcol,rowid)],columns=columns)[0]
    for c in range(0,len(columns)):
        if oldvalues[c] != myrow[c]:
            alter_cell(dname,table,[myrow[c]],columns[c],rowid,refcol)

def select_visible_objects(dname,JD,longit=Bryce_long,lat=Bryce_lat,alt=25,late=None):
    objs = select(dname, 'objects')
    vis_objs = []
    for i in range(0,len(objs)):
        #print objs[i][7:9]
        RA = objs[i][7]
        dec= objs[i][8]
        if late == None:
            t_up,intervals = get_dark_overlap(JD,RA,dec,longit,lat,alt)
        else:
            t_up,intervals = get_obs_overlap(JD,RA,dec,longit,lat,alt,late)
            #print objs[i][0], t_up,intervals
        if t_up > .4:
            vis_objs.append(objs[i])
    return array(vis_objs)

def update_visible(dname,JD,longit=Bryce_long,lat=Bryce_lat,alt=30,late=None):
    data = select_visible_objects(dname,JD,longit,lat,alt,late)
    conn = sqlite3.connect(dname)
    c = conn.cursor()
    c.execute('DELETE FROM vobjects WHERE name like "%"')
    conn.commit()
    c.close()
    conn.close()
    for i in range(0,len(data)):
        add_row(dname,'vobjects',data[i])

def get_vis_constellations(dname,JD,longit=Bryce_long,lat=Bryce_lat,alt=15,late=None):
    objs = select(dname, 'constellations')
    vis_objs = []
    for i in range(0,len(objs)):
        RA = objs[i][2]
        dec= objs[i][3]
        if late == None:
            t_up,intervals = get_dark_overlap(JD,RA,dec,longit,lat,alt)
        else:
            t_up,intervals = get_obs_overlap(JD,RA,dec,longit,lat,alt,late)
        if t_up > .5:
            vis_objs.append(objs[i])
    return array(vis_objs)

def execute_script(dname,mycmd):
    conn = sqlite3.connect(dname)
    c = conn.cursor()
    c.executescript(mycmd)
    conn.commit()
    c.close()
    conn.close()
    
dname = 'Bryce_outreach.db'

#---------------------------------------------------------------------------

if __name__ == '__main__':
    data = select(dname,'objects',conditions=["name like '%Cat%'"])
    print data
    ##for itemid in data:
    ##    myid = itemid[0]
    ##    fc   = itemid[1]
    ##    value=[fc.lstrip('/')]
    ##    alter_cell(dname,'objects',value,'finding_chart',myid,'id')

    #update_visible(dname,currentJD(),alt=30,late=23)
    #cs = get_vis_constellations(dname,currentJD(),late=22,alt=30)
    #print cs,len(cs)

#---------------------------------------------------------------------------
