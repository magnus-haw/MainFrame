#Celestial Mechanics library
###Written by Magnus Haw
###Created Aug 23, 2012
###Last edited Sept 16, 2012

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

from numpy import array,tan,cos,sin,pi,arange
from math import acos,atan2,asin,degrees,radians
import time


def sind(x):
    return sin(radians(x))

def cosd(x):
    return cos(radians(x))

def currentJD():
    t = time.gmtime()
    dmyhms = [t.tm_mday,t.tm_mon,t.tm_year,t.tm_hour,t.tm_min,t.tm_sec]
    return UTtoJD(dmyhms)

def DectoDMS(decdeg):
    decdeg = float(decdeg)
    m = (abs(decdeg)%1.)*60.
    s = (m%1)*60.
    return array([int(decdeg),int(m),s])

def DMStoDec(dms):
    dms[0] = float(dms[0])
    dms[1] = float(dms[1])
    dms[2] = float(dms[2])
    val = abs(dms[0]) + abs(dms[1]/60.) + abs(dms[2]/3600.)
    if dms[0] <0:
        val *= -1.
    return val
    

#Calculates integer julian day
def getJ0(dmyhms):
    J0 =  367*dmyhms[2]
    J0 -= int(7.*(dmyhms[2]+int((dmyhms[1]+9)/12.))/4.)
    J0 += int(275.*dmyhms[1]/9.)
    J0 += dmyhms[0]+1721013.5
    return J0

#Converts UT to JD
def UTtoJD(dmyhms):#day,month,year,hours,mins,secs
    deciTime=(dmyhms[3]) + (dmyhms[4]/60.) + (dmyhms[5]/3600.)
    J0 = getJ0(dmyhms)
    JD = J0 + deciTime/24.
    return JD

#Converts local time to JD
def LTtoJD(dmyhms,longit):
    date = dmyhms.copy()
    offset = int(-longit/15.)
    date[3] += offset
    return UTtoJD(date)

#calculates gregorian date (UT) from JD
#adapted from: http://www.davidgsimpson.com/software/jd2greg_f90.txt
def JDtoUT(JD):
    JD = JD + 0.5
    Z = int(JD)
    F = JD - Z

    if (Z < 2299161):
        A = Z
    else:
        ALPHA = int((Z-1867216.25)/36524.25)
        A = Z + 1 + ALPHA - ALPHA/4.

    B = A + 1524.
    C = int((B-122.1)/365.25)
    D = int(365.25*C)
    E = int((B-D)/30.6001)

    DAY = B - D - int(30.6001*E) + F

    ##Find Month
    if (E < 14):
        M = E - 1
    else:
        M = E - 13
    if (M > 2):
        Y = C - 4716
    else:
        Y = C - 4715

    ##Find time
    h = ((DAY%1)*24.)
    m = (h%1)*60.
    s = (m%1)*60.

    return [int(DAY), M, Y, int(h), int(m), s]

def JDtoLT(JD,longit):
    LT = JDtoUT(JD)
    offset = int(longit/15.)
    LT[3]+=offset
    if LT[3] > 24:
        LT[0] +=1
    if LT[3] < 0:
        LT[0] -=1
    LT[3] = (LT[3])%24
    return LT

##Finds Greenwich mean sidereal time in degrees
def JDtoGMST(JD):
    #Find the Julian Date of the previous midnight, JD0
    JDmin = int(JD)-.5
    JDmax = int(JD)+.5
    if JD > JDmin:
        JD0 = JDmin
    if JD > JDmax:
        JD0 = JDmax
    H = (JD-JD0)*24       #Time in hours past previous midnight
    D = JD - 2451545.0     #Compute the number of days since J2000
    D0 = JD0 - 2451545.0   #Compute the number of days since J2000
    T = D/36525.           #Compute the number of centuries since J2000
    #Calculate GMST in hours (0h to 24h) ... then convert to degrees
    GMST = ((6.697374558 + 0.06570982441908*D0  + 1.00273790935*H + 0.000026*(T**2.))%24)*15.
    return GMST

##Finds Greenwich apparent sideareal time in hours
def JDtoGAST(JD):
    #THETAm is the mean siderial time in degrees
    THETAm = JDtoGMST(JD)

    #Compute the number of centuries since J2000
    T = (JD - 2451545.0)/36525.

    #Mean obliquity of the ecliptic (EPSILONm)
    # see http://www.cdeagle.com/ccnum/pdf/demogast.pdf equation 3
    # also see Vallado, Fundamentals of Astrodynamics and Applications, second edition.
    #pg. 214 EQ 3-53
    EPSILONm = 23.439291 - 0.0130111*T - 1.64e-7*(T**2.) + 5.04e-7*(T**3.)

    #Nutations in obliquity and longitude (degrees)
    # see http://www.cdeagle.com/ccnum/pdf/demogast.pdf equation 4
    L = 280.4665 + 36000.7698*T
    dL = 218.3165 + 481267.8813*T
    OMEGA = 125.04452 - 1934.136261*T

    #Calculate nutations using the following two equations:
    # see http://www.cdeagle.com/ccnum/pdf/demogast.pdf equation 5
    dPSI = -17.20*sind(OMEGA) - 1.32*sind(2*L) - .23*sind(2.*dL) + .21*sind(2*OMEGA)
    dEPSILON = 9.20*cosd(OMEGA) + .57*cosd(2.*L) + .10*cosd(2.*dL) - .09*cosd(2*OMEGA)

    #Convert the units from arc-seconds to degrees
    dPSI = dPSI*(1/3600.)
    dEPSILON = dEPSILON*(1/3600.)

    #(GAST) Greenwhich apparent sidereal time expression in degrees
    # see http://www.cdeagle.com/ccnum/pdf/demogast.pdf equation 1
    GAST = (THETAm + dPSI*cosd(EPSILONm+dEPSILON))%360

    return GAST/15.

#Calculates local sidereal time based on JD and longitude
def JDtoLST(JD, longit):
    GAST = JDtoGAST(JD)
    LST = (GAST + longit/15.)%24
    
    return LST

# finds time above given altitude
# all inputs are in degrees
def time_above(dec, alt, lat):
    #print dec,alt,lat

    lat *= pi/180.
    alt *= pi/180.
    dec *= pi/180.

    if lat >= 0:  
        if dec >= pi/2. - lat + alt:
            return 24.
        elif dec <= -pi/2. + lat + alt:
            return 0.
        else:
            #print (sin(alt)-sin(lat)*sin(dec))/(cos(lat)*cos(dec))
            h = acos((sin(alt)-sin(lat)*sin(dec))/(cos(lat)*cos(dec)))
            time = (2.*h*180./pi/15.)
            return time
    if lat < 0:
        if dec <= (-pi/2. - lat - alt):
            return 24.
        elif dec >= (pi/2. + lat - alt):
            return 0.
        else:
            #print (sin(alt)-sin(lat)*sin(dec))/(cos(lat)*cos(dec))
            h = acos((sin(alt)-sin(lat)*sin(dec))/(cos(lat)*cos(dec)))
            time = (2.*h*180./pi/15.)
            return time

# Calculates position of sun in RA, dec
def get_sunpos(JD):
    d = JD - 2451545.0 # days since J2000
    q = (280.461 + 0.9856474 * d)%360 #Mean longitude of Sun
    g = (357.528 + 0.9856003 * d)%360 #Mean anomaly of Sun
    L = q + 1.915*sin(radians(g)) + 0.020*sin(2*radians(g))
    e = 23.439 - 0.00000036*d #ecliptic orientation

    RA = atan2( cos(radians(e)) * sin(radians(L)), cos(radians(L)))
    RA = (RA*180./pi/15.)%24
    dec = asin( sin(radians(e))*sin(radians(L)))
    dec *= 180./pi

    return RA,dec

#Returns rise and set times of object viewed from given long,lat
def get_rise_set(JD,RA,dec,longit,lat,alt=0):
    LST = JDtoLST(JD, longit)
    HA = LST - RA
    T = time_above(dec,alt,lat)/24. # time above alt in days

    cross_merid = JD - HA/24.

    Rise = cross_merid - T/2.
    Set  = cross_merid + T/2.
    
    return JDtoLT(Rise,longit)[3:], JDtoLT(Set,longit)[3:]

#finds overlap in hours of two intervals (a,b) and (c,d)
def get_overlap(a,b,c,d,per=24.):
    total =0
    intervals =[]
    if a>=b:
        b+=per
    if c>=d:
        d+=per

    if b-a==per:
        intervals.append([c,d%per])
        return d-c, intervals
    if d-c==per:
        intervals.append([a,b%per])
        return b-a, intervals

    start1 = min(a,c)
    if start1 == a:
        end1   = b
        start2 = c
        end2   = d
    else:
        start2 = a
        end2   = b
        end1   = d

    if end1 < start2:
        total += 0
        if end2 > start1 + per:
            intervals.append([start1,end2%per])
            return end2-(start1+per),intervals
        else:
            return 0,intervals
    else:
        if end2 < end1:
            intervals.append([start2,end2%per])
            return end2-start2, intervals
        else:
            total+= end1-start2
            intervals.append([start2,end1%per])
            if end2 > start1 + per:
                total +=end2-(start1+per)
                intervals.append([start1,end2%per])
            return total,intervals

def get_dark_overlap(JD,RA,dec,longit,lat,alt=25):
    sRA,sdec=get_sunpos(JD)
    sr,ss = get_rise_set(JD,sRA,sdec,longit,lat,0)
    sun_rise = sr[0]+ sr[1]/60. + sr[2]/3600.
    sun_set  = ss[0]+ ss[1]/60. + ss[2]/3600.

    r,s = get_rise_set(JD,RA,dec,longit,lat,alt)
    obj_rise = r[0]+ r[1]/60. + r[2]/3600.
    obj_set  = s[0]+ s[1]/60. + s[2]/3600.

    return get_overlap(obj_rise,obj_set, sun_set,sun_rise)

def get_obs_overlap(JD,RA,dec,longit,lat,alt=25,late=23):
    sRA,sdec=get_sunpos(JD)
    sr,ss = get_rise_set(JD,sRA,sdec,longit,lat,0)
    sun_set  = ss[0]+ ss[1]/60. + ss[2]/3600.

    r,s = get_rise_set(JD,RA,dec,longit,lat,alt)
    obj_rise = r[0]+ r[1]/60. + r[2]/3600.
    obj_set  = s[0]+ s[1]/60. + s[2]/3600.
##    print "rise: ",obj_rise
##    print "set: ",obj_set

    timeup = get_overlap(obj_rise,obj_set, sun_set,late)
    return timeup
    
 
#Bryce Longitude and Latitude
Bryce_long = -(112 + 14/60. + 8/3600.)
Bryce_lat  = 37 + 28/60. + 18/3600.

#---------------------------------------------------------------------------

if __name__ == '__main__':
    JD  = currentJD()
    RA  = 12.3663888889
    dec = 58.0891666667
    ov1  = get_obs_overlap(JD,RA,dec,Bryce_long,Bryce_lat,alt=5,late=23)
    ov2  = get_obs_overlap(JD,RA,dec,Bryce_long,Bryce_lat,alt=25,late=23)
    
    print(ov1)
    print(ov2)
#---------------------------------------------------------------------------

