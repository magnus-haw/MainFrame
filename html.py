# create html for pdf viewing

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

from shutil import copy
from string import lower
import sys

def MakeHtml(fname,bname='graphics/finding_charts/'):
    if fname[-3:] == 'pdf':
        mycmd = "embed"
        wdht  = 'width="825" height="1150"'
    elif lower(fname[-3:]) == 'jpg' or lower(fname[-3:]) == 'png' or lower(fname[-3:]) == 'bmp' or lower(fname[-3:]) == 'gif':
        mycmd = "img"
        wdht = ''
    html = '''<!DOCTYPE HTML>
<html>
<body>

<%s src="%s" %s>

</body>
</html>'''%(mycmd,"src_images/"+fname,wdht)
    fn = fname[0:-3]+"html" 
    fout = open(bname+fn,'w')
    fout.write(html)
    fout.close()
    return fn


def StoreImage(path):
##    try:
    if path.split("/")[-3] == "graphics" and path.split("/")[-2]== "images":
        pass
    else:
        copy(path,"graphics/images/")
    return "graphics/images/" + path.split("/")[-1]
##    except:
##        print "Unexpected error:", sys.exc_info()[0],'\n'
##        return "graphics/none.jpg"

def StoreFC(path):
##    try:
    if path.split("/")[-4] == "graphics" and path.split("/")[-3]== "finding_charts" and path.split("/")[-2]== "src_images":
        pass
    else:
        copy(path,'graphics/finding_charts/src_images/')
    fname = path.split("/")[-1]
    fn = MakeHtml(fname)
    return 'graphics/finding_charts/'+fn
##    except:
##        print "Unexpected error:", sys.exc_info()[0],'\n'
##        return "graphics/none.html"
