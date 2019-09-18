##Creates each individual page of the add/edit wizard
##
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

import wx,string,os
import wx.wizard as wiz
from calcs import DectoDMS,DMStoDec
from numpy import array
import wx.lib.agw.floatspin as FS
import  wx.lib.imagebrowser    as  ib

from mylists import con,otypes

cdict = dict(list(zip(con[:,0],con[:,1])))
abbrdict = dict(list(zip(con[:,1],con[:,0])))
typdict=dict(list(zip(otypes[:,0],otypes[:,1])))
#----------------------------------------------------------------------

def makePageTitle(wizPg, title):
    sizer = wx.BoxSizer(wx.VERTICAL)
    wizPg.SetSizer(sizer)
    title = wx.StaticText(wizPg, -1, title)
    title.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
    sizer.Add(title, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    sizer.Add(wx.StaticLine(wizPg, -1), 0, wx.EXPAND|wx.ALL, 5)
    return sizer

#----------------------------------------------------------------------

class TitlePage(wiz.WizardPageSimple):
    def __init__(self, parent, title):
        wiz.WizardPageSimple.__init__(self, parent)
        self.sizer = makePageTitle(self, title)

#---------------------------------------------------------------------------

class NameValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)

    def Clone(self):
        return NameValidator()

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()
        
        if len(val) > 1:
            return True
        else:
            wx.Bell()
            wx.MessageBox("Invalid input. Input a name and catalog ID.")
            return False
    def TransferToWindow(self):
        return True # Prevent wxDialog from complaining.

    def TransferFromWindow(self):
        return True # Prevent wxDialog from complaining.


#----------------------------------------------------------------------

class NamePage(wiz.WizardPageSimple):
    def __init__(self, parent,log, data=None):
        wiz.WizardPageSimple.__init__(self, parent)
        self.sizer = makePageTitle(self, "Object Names")
        self.log=log

        if data == None:
            data = ["","",""]

        namesizer = wx.BoxSizer(wx.HORIZONTAL)
        namelabel = wx.StaticText(self, -1, "Name*")
        self.nameEntry = wx.TextCtrl(self, -1, data[0], validator = NameValidator())
        namesizer.Add(namelabel,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        namesizer.Add(self.nameEntry,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        self.sizer.Add(namesizer,1, wx.ALIGN_CENTRE|wx.ALL, 5)

        IDsizer = wx.BoxSizer(wx.HORIZONTAL)
        IDlabel = wx.StaticText(self, -1, "Catalog ID*")
        self.IDEntry = wx.TextCtrl(self, -1, data[1], validator = NameValidator())
        IDsizer.Add(IDlabel,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        IDsizer.Add(self.IDEntry,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        self.sizer.Add(IDsizer,1, wx.ALIGN_CENTRE|wx.ALL, 5)

        OtherSizer = wx.BoxSizer(wx.HORIZONTAL)
        OtherLabel = wx.StaticText(self, -1, "Other Names")
        OtherLabel.SetHelpText("Enter names separated by commas")
        self.OtherEntry = wx.TextCtrl(self, -1, data[2])
        OtherSizer.Add(OtherLabel,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        OtherSizer.Add(self.OtherEntry,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        self.sizer.Add(OtherSizer,1, wx.ALIGN_CENTRE|wx.ALL, 5)

    def GetInput(self):
        name = self.nameEntry.GetValue()
        cID  = self.IDEntry.GetValue()
        other= self.OtherEntry.GetValue()
        self.log.write("Name: %s\nCatalog ID: %s\nOther names: %s"%(name,cID,other))
        return name,cID,other


#----------------------------------------------------------------------

class NumberPage(wiz.WizardPageSimple):
    def __init__(self, parent, log, data=None):
        wiz.WizardPageSimple.__init__(self, parent)
        self.sizer = makePageTitle(self, "Object Properties")
        self.log = log
        
        if data == None:
            data = ["GCl",6,"","",]
        
        ##Mag Ctrl
        MagSizer = wx.BoxSizer(wx.HORIZONTAL)
        MagLabel = wx.StaticText(self, -1, "Visual Magnitude*")

        self.MagEntry = FS.FloatSpin(self, -1, min_val=0, max_val=20,
                                       increment=0.1, value=data[1], agwStyle=FS.FS_LEFT)
        self.MagEntry.SetFormat("%f")
        self.MagEntry.SetDigits(1)
        MagSizer.Add(MagLabel,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        MagSizer.Add(self.MagEntry,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        self.sizer.Add(MagSizer,1, wx.ALIGN_CENTRE|wx.ALL, 5)

        ##Angular Size
        SizeSizer = wx.BoxSizer(wx.HORIZONTAL)
        SizeLabel = wx.StaticText(self, -1, "Angular Size (arcmin)*")
        SizeLabel.SetHelpText("Only digits, periods and 'x' are valid chars")
        self.SizeEntry = wx.TextCtrl(self, -1, str(data[2]), validator= SizeValidator())
        SizeSizer.Add(SizeLabel,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        SizeSizer.Add(self.SizeEntry,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        self.sizer.Add(SizeSizer,1, wx.ALIGN_CENTRE|wx.ALL, 5)

        ##Distance 
        DistSizer = wx.BoxSizer(wx.HORIZONTAL)
        DistLabel = wx.StaticText(self, -1, "Distance (Kly)*")
        DistLabel.SetHelpText("Enter only digits. Units are thousands of light years")
        self.DistEntry = wx.TextCtrl(self, -1, str(data[3]), validator= TxtDegreeValidator(1e10))
        DistSizer.Add(DistLabel,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        DistSizer.Add(self.DistEntry,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        self.sizer.Add(DistSizer,1, wx.ALIGN_CENTRE|wx.ALL, 5)

        ##Type Ctrl
        TypeSizer = wx.BoxSizer(wx.HORIZONTAL)
        TypeLabel = wx.StaticText(self, -1, "Type*")
        TypeLabel.SetHelpText("Select type from list")
        
        listabbr = otypes[:,1]
        intdict = dict(list(zip(listabbr,list(range(0,len(listabbr))))))
        self.TypeEntry = wx.ListBox(self, -1, size=(200, 100), choices=otypes[:,0], style=wx.LB_SINGLE)
        self.TypeEntry.SetSelection(intdict[data[0]])
        TypeSizer.Add(TypeLabel,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        TypeSizer.Add(self.TypeEntry,3, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        self.sizer.Add(TypeSizer,3, wx.ALIGN_CENTRE|wx.ALL, 5)

    def GetInput(self):
        mytype= typdict[self.TypeEntry.GetStringSelection()]
        mag = self.MagEntry.GetValue()
        size = self.SizeEntry.GetValue()
        dist = self.DistEntry.GetValue()
        self.log.write("Type: %s\n Mag: %.1f\n Size: %s\n Dist: %s"%(mytype, mag, size, dist) )
        return mytype, float(mag), size, float(dist)
  
#----------------------------------------------------------------------

class LocationPage(wiz.WizardPageSimple):
    def __init__(self, parent, log, data=None):
        wiz.WizardPageSimple.__init__(self, parent)
        self.sizer = makePageTitle(self, "Location")
        self.log = log

        if data == None:
            data = [[0,0,0],[0,0,0],"And"]
        else:
            data[0] = DectoDMS(data[0])
            data[1] = DectoDMS(data[1])

        ##Right Ascention spin controls
        RAsizer = wx.BoxSizer(wx.HORIZONTAL)
        RAlabel = wx.StaticText(self, -1, "Right Ascension*")
        self.RAEntryh = wx.SpinCtrl(self, -1, "", (30, 50))
        self.RAEntryh.SetRange(0,24)
        self.RAEntryh.SetValue(data[0][0])
        self.RAEntrym = wx.SpinCtrl(self, -1, "", (30, 50))
        self.RAEntrym.SetRange(0,60)
        self.RAEntrym.SetValue(data[0][1])
        self.RAEntrys = wx.SpinCtrl(self, -1, "", (30, 50))
        self.RAEntrys.SetRange(0,60)
        self.RAEntrys.SetValue(data[0][2])

        RAsizer.Add(RAlabel,2, wx.ALIGN_CENTRE|wx.ALL, 5)
        RAsizer.Add(self.RAEntryh,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        RAsizer.Add(self.RAEntrym,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        RAsizer.Add(self.RAEntrys,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        self.sizer.Add(RAsizer,1, wx.ALIGN_CENTRE|wx.ALL, 5)

        ##Declination spin controls
        DecSizer = wx.BoxSizer(wx.HORIZONTAL)
        DecLabel = wx.StaticText(self, -1, "Declination*")
        self.DecEntryh = wx.SpinCtrl(self, -1, "", (30, 50))
        self.DecEntryh.SetRange(-90,90)
        self.DecEntryh.SetValue(data[1][0])
        self.DecEntrym = wx.SpinCtrl(self, -1, "", (30, 50))
        self.DecEntrym.SetRange(0,60)
        self.DecEntrym.SetValue(data[1][1])
        self.DecEntrys = wx.SpinCtrl(self, -1, "", (30, 50))
        self.DecEntrys.SetRange(0,60)
        self.DecEntrys.SetValue(data[1][2])

        DecSizer.Add(DecLabel,2, wx.ALIGN_CENTRE|wx.ALL, 5)
        DecSizer.Add(self.DecEntryh,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        DecSizer.Add(self.DecEntrym,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        DecSizer.Add(self.DecEntrys,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        self.sizer.Add(DecSizer,1, wx.ALIGN_CENTRE|wx.ALL, 5)

        TypeSizer = wx.BoxSizer(wx.HORIZONTAL)
        TypeLabel = wx.StaticText(self, -1, "Constellation*")
        TypeLabel.SetHelpText("Select constellation from list")
        
        listcons = con[:,0]
        listcons.sort()
        ndict = dict(list(zip(listcons,list(range(0,len(listcons))))))

        myind = ndict[abbrdict[data[2]]]
        self.TypeEntry = wx.ListBox(self, -1, size=(120, 100), choices=listcons, style=wx.LB_SINGLE)
        self.TypeEntry.SetSelection(myind)
        TypeSizer.Add(TypeLabel,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        TypeSizer.Add(self.TypeEntry,2, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        self.sizer.Add(TypeSizer,3, wx.ALIGN_CENTRE|wx.ALL, 5)

    def GetInput(self):
        RA = DMStoDec([self.RAEntryh.GetValue(),self.RAEntrym.GetValue(),self.RAEntrys.GetValue()])
        dec = DMStoDec([self.DecEntryh.GetValue(),self.DecEntrym.GetValue(),self.DecEntrys.GetValue()])
        mycon= cdict[self.TypeEntry.GetStringSelection()]
        self.log.write("RA: %.2f\n Dec: %.2f\n Constln: %s"%(RA,dec,mycon) )
        return float(RA),float(dec),mycon
  
#----------------------------------------------------------------------

class TxtDegreeValidator(wx.PyValidator):
    def __init__(self,maxd):
        wx.PyValidator.__init__(self)
        self.maxd = maxd
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return TxtDegreeValidator(self.maxd)

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()
        pcount =0
        for x in val:
            if x == '.':
                pcount += 1
                if pcount > 1:
                    wx.Bell()
                    wx.MessageBox("Invalid input. Enter valid number of decimal points.")
                    return False
            if (x not in string.digits) and (x != '.'):
                wx.Bell()
                wx.MessageBox("Invalid input. Enter only digits.")
                return False
        if val== '':
            wx.Bell()
            wx.MessageBox("Invalid input. Must enter values.")
            return False
        if float(val)>self.maxd or float(val)<0:
            wx.Bell()
            wx.MessageBox("Invalid input. Exceeds max value.")
            return False
        return True

    def OnChar(self, event):
        key = event.GetKeyCode()
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255 or chr(key) == '.':
            event.Skip()
            return
        if chr(key) in string.digits or key == wx.WXK_SPACE or key ==wx.WXK_SUBTRACT:
            event.Skip()
            return
        if not wx.Validator_IsSilent():
            wx.Bell()
        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return

    def TransferToWindow(self):
        return True # Prevent wxDialog from complaining.

    def TransferFromWindow(self):
        return True # Prevent wxDialog from complaining.

#---------------------------------------------------------------------------

class SizeValidator(wx.PyValidator):
    def __init__(self):
        wx.PyValidator.__init__(self)
        self.Bind(wx.EVT_CHAR, self.OnChar)

    def Clone(self):
        return SizeValidator()

    def Validate(self, win):
        tc = self.GetWindow()
        val = tc.GetValue()
        pcount =0
        for x in val:
            if x == '.':
                pcount += 1
                if pcount > 2:
                    wx.Bell()
                    wx.MessageBox("Invalid input. Enter valid number of decimal points.")
                    return False
            if (x not in string.digits) and (x != 'x') and (x != '.'):
                wx.Bell()
                wx.MessageBox("Invalid input. Enter only digits and decimal points.")
                return False
        if val== '':
            wx.Bell()
            wx.MessageBox("Invalid input. Must enter values.")
            return False

        return True

    def OnChar(self, event):
        key = event.GetKeyCode()
        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return
        if chr(key) in string.digits or chr(key) == 'x' or chr(key) =='X' or key==46:
            event.Skip()
            return
        if not wx.Validator_IsSilent():
            wx.Bell()
        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return

    def TransferToWindow(self):
        return True # Prevent wxDialog from complaining.

    def TransferFromWindow(self):
        return True # Prevent wxDialog from complaining.

#---------------------------------------------------------------------------

class CommentPage(wiz.WizardPageSimple):
    def __init__(self, parent, log, data=None):
        wiz.WizardPageSimple.__init__(self, parent)
        self.sizer = makePageTitle(self, "Object Description")
        self.log = log
        
        if data == None:
            data = ["","",""]
        else:
            for i in range(0,3):
                if data[i] == None:
                    data[i] =""

        DescripSizer = wx.BoxSizer(wx.HORIZONTAL)
        DescripLabel = wx.StaticText(self, -1, "Description")
        self.DescripEntry = wx.TextCtrl(self, -1, data[0],style=wx.TE_MULTILINE)
        DescripSizer.Add(DescripLabel,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        DescripSizer.Add(self.DescripEntry,2, wx.EXPAND|wx.ALL, 5)
        
        self.sizer.Add(DescripSizer,10, wx.EXPAND|wx.ALL, 5)

        ComSizer = wx.BoxSizer(wx.HORIZONTAL)
        ComLabel = wx.StaticText(self, -1, "Observing comments")
        self.ComEntry = wx.TextCtrl(self, -1, data[1])
        ComSizer.Add(ComLabel,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        ComSizer.Add(self.ComEntry,2, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        self.sizer.Add(ComSizer,3, wx.ALIGN_CENTRE|wx.ALL, 5)

        LinkSizer = wx.BoxSizer(wx.HORIZONTAL)
        LinkLabel = wx.StaticText(self, -1, "Website URL")
        self.LinkEntry = wx.TextCtrl(self, -1, data[2])
        LinkSizer.Add(LinkLabel,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        LinkSizer.Add(self.LinkEntry,2, wx.ALIGN_CENTRE|wx.ALL, 5)
        
        self.sizer.Add(LinkSizer,3, wx.ALIGN_CENTRE|wx.ALL, 5)

    def GetInput(self):
        desc = self.DescripEntry.GetValue()
        comm = self.ComEntry.GetValue()
        link = self.LinkEntry.GetValue()
        self.log.write("Description:%s\nComments:%s\nURL:%s"%(desc,comm,link))
        return desc,comm,link
#---------------------------------------------------------------------------


class ImagePage(wiz.WizardPageSimple):
    def __init__(self, parent, log, data=None):
        wiz.WizardPageSimple.__init__(self, parent)
        self.sizer = makePageTitle(self, "Graphics")
        self.log = log

        if data == None:
            data = ["",""]

        ##Finding chart
        FCsizer = wx.BoxSizer(wx.HORIZONTAL)
        FClabel = wx.StaticText(self, -1, "Finding Chart")
        self.FCEntry = wx.TextCtrl(self, -1, data[0],style=wx.TE_MULTILINE)
        self.FCEntry.SetEditable(False)
        self.FCEntry.SetBackgroundColour((140,140,140))
        b = wx.Button(self, -1, "Browse for Finding Chart", (50,50))
        self.Bind(wx.EVT_BUTTON, self.GetFCPath, b)
        FCsizer.Add(FClabel,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        FCsizer.Add(self.FCEntry,3, wx.EXPAND|wx.HORIZONTAL, 5)
        
        self.sizer.Add(FCsizer,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.sizer.Add(b,0,wx.ALIGN_CENTRE|wx.ALL, 5)

        ##Image
        ImgSizer = wx.BoxSizer(wx.HORIZONTAL)
        ImgLabel = wx.StaticText(self, -1, "Image Location")
        self.ImgEntry = wx.TextCtrl(self, -1, data[1],style=wx.TE_MULTILINE)
        self.ImgEntry.SetEditable(False)
        self.ImgEntry.SetBackgroundColour((140,140,140))
        b = wx.Button(self, -1, "Browse for Image", (50,50))
        self.Bind(wx.EVT_BUTTON, self.GetImagePath, b)
        ImgSizer.Add(ImgLabel,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        ImgSizer.Add(self.ImgEntry,3, wx.EXPAND|wx.HORIZONTAL, 5)
        
        self.sizer.Add(ImgSizer,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.sizer.Add(b,0,wx.ALIGN_CENTRE|wx.ALL, 5)


    def GetImagePath(self, evt):
        fl_ext_types = (
            # display, filter
            ("All supported formats", "All"),
            ("BMP (*.bmp)", "*.bmp"),
            ("GIF (*.gif)", "*.gif"),
            ("PNG (*.png)", "*.png"),
            ("JPEG (*.jpg)", "*.jpg"),
            ("All Files", "*.*"),
            )
        # get current working directory
        dir = os.getcwd()
        # set the initial directory for the demo bitmaps
        initial_dir = dir
        # open the image browser dialog
        dlg = ib.ImageDialog(self, initial_dir)
        dlg.Centre()
        dlg.ChangeFileTypes(fl_ext_types)
        if dlg.ShowModal() == wx.ID_OK:
            # show the selected file
            mypath = dlg.GetFile()
            self.log.write("You Selected File: " + dlg.GetFile() )       
        else:
            self.log.write("You pressed Cancel\n")

        dlg.Destroy()
        self.ImgEntry.SetValue(mypath)

    def GetFCPath(self,evt):
        fl_ext_types = (
            # display, filter
            ("All supported formats", "All"),
            ("BMP (*.bmp)", "*.bmp"),
            ("GIF (*.gif)", "*.gif"),
            ("PNG (*.png)", "*.png"),
            ("JPEG (*.jpg)", "*.jpg"),
            ("PDF (*.pdf)", "*.pdf"),
            ("All Files", "*.*"),
            )
        # get current working directory
        dir = os.getcwd()
        # set the initial directory for the demo bitmaps
        initial_dir = dir
        # open the image browser dialog
        dlg = ib.ImageDialog(self, initial_dir)
        dlg.Centre()
        dlg.ChangeFileTypes(fl_ext_types)
        if dlg.ShowModal() == wx.ID_OK:
            # show the selected file
            mypath = dlg.GetFile()
            self.log.write("You Selected File: " + dlg.GetFile())     
        else:
            self.log.write("You pressed Cancel\n")

        dlg.Destroy()
        self.FCEntry.SetValue(mypath)

    def GetInput(self):
        image  = self.ImgEntry.GetValue()
        fc_path= self.FCEntry.GetValue()
        self.log.write("Finding chart:%s\nImage: %s\n"%(fc_path,image) )
        return fc_path,image
