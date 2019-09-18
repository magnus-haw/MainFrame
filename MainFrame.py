#----------------------------------------------------------------------------
# Name:         MainFrame.py
# Purpose:      Astronomy Outreach: lists visible objects at a given lat, long
#
# Author:       Magnus Haw
#
# Created:      Sept 13. 2012
# Copyright:    (C) 2012 Magnus Haw
# Licence:      GNU GPL3
#----------------------------------------------------------------------------

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

import sys,os
import  wx
import  wx.lib.mixins.listctrl  as  listmix
from calcs import *
from DatabaseCalls import *
from numpy import zeros,shape,append
import  wx.lib.layoutf  as layoutf

from ListPanel import MyListCtrl,MyListCtrlPanel
from DisplayPanel import MyDisplayPanel
from LocationDialog import LocationDialog
from FilterDialog import FilterDialog

from AddEditWizard import AddEditWizard,mylog

from html import StoreImage,StoreFC

##Various static lists
TBFLAGS = ( wx.TB_HORIZONTAL
            | wx.NO_BORDER
            | wx.TB_FLAT
            | wx.TB_TEXT
            | wx.TB_HORZ_LAYOUT
            )

mnths = ['Jan','Feb','Mar','Apr','May','Jun','July','Aug','Sep','Oct','Nov','Dec']
months= dict(list(zip(mnths,list(range(1,13)))))
#---------------------------------------------------------------------------

#---------------------------------------------------------------------------

class MainFrame(wx.Frame):
    def __init__(self, parent, ID, title):
        wx.Frame.__init__(self, parent, ID, title, size=(1000, 700))
        self.log = mylog()
        print(os.getcwd())

        #Default selection settings
        dlist = select(dname,'defaults',conditions=["name=='default'"])[0]
        
        self.lat = float(dlist[1])
        self.long= float(dlist[2])
        self.JD  = currentJD()

        self.late= int(dlist[3])
        self.limit=int(dlist[4])
        self.conds=None
        self.alt  = int(dlist[5])

        self.UpdateData(False)
        
        #Initialize list panel
        self.listpanel = MyListCtrlPanel(self, sys.stdout,self.data)
        self.currentItem = 0

        #Initialize display panel
        self.displaypanel = MyDisplayPanel(self)
        self.displaypanel.setLink(self.data[self.currentItem][0],self.data[self.currentItem][-3])
        self.displaypanel.setText(self.data[self.currentItem][-5])
        self.displaypanel.setImage(self.data[self.currentItem][-6])
        self.displaypanel.setFChart(self.data[self.currentItem][-7])

        #Create Toolbar
        tb = self.CreateToolBar( TBFLAGS )
        sb = self.CreateStatusBar()

        #####Toolbar creation#####
        tsize = (24,24)
        new_bmp  = wx.ArtProvider.GetBitmap(wx.ART_NEW, wx.ART_TOOLBAR, tsize)
        open_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, wx.ART_TOOLBAR, tsize)
        copy_bmp = wx.ArtProvider.GetBitmap(wx.ART_COPY, wx.ART_TOOLBAR, tsize)
        paste_bmp= wx.ArtProvider.GetBitmap(wx.ART_PASTE, wx.ART_TOOLBAR, tsize)
        find_bmp = wx.ArtProvider.GetBitmap(wx.ART_FIND, wx.ART_TOOLBAR, tsize)
        save_bmp = wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, wx.ART_TOOLBAR, tsize)
        info_bmp = wx.ArtProvider.GetBitmap(wx.ART_INFORMATION, wx.ART_TOOLBAR, tsize)
        cross_bmp= wx.ArtProvider.GetBitmap(wx.ART_CROSS_MARK, wx.ART_TOOLBAR, tsize)
        
        tb.SetToolBitmapSize(tsize)

        dpID = wx.NewId()

        #date control
        tb.AddControl(wx.DatePickerCtrl(tb, dpID, size=(120,-1),
                                style = wx.DP_DROPDOWN
                                      | wx.DP_SHOWCENTURY
                                      | wx.DP_ALLOWNONE ) )
        self.Bind(wx.EVT_DATE_CHANGED, self.OnDateChanged, id=dpID)

        #location control
        tb.AddLabelTool(10, "Lat/Long", cross_bmp, shortHelp="Change location", longHelp="Set observer location")
        self.Bind(wx.EVT_TOOL, self.SetLatLong, id=10)
        self.Bind(wx.EVT_TOOL_RCLICKED, self.SetLatLong, id=10)

        tb.AddSeparator()

        #edit current item control
        tb.AddLabelTool(20, "Edit", open_bmp, shortHelp="Edit object", longHelp="Edit selected entry")
        self.Bind(wx.EVT_TOOL, self.EditItem, id=20)
        self.Bind(wx.EVT_TOOL_RCLICKED, self.EditItem, id=20)

        #add new item control
        tb.AddLabelTool(30, "Add", new_bmp, shortHelp="Add object",longHelp="Add object to database")
        self.Bind(wx.EVT_TOOL, self.AddItem, id=30)
        self.Bind(wx.EVT_TOOL_RCLICKED, self.AddItem, id=30)

        tb.AddSeparator()

        #filter settings control
        tb.AddLabelTool(40,"Filter",find_bmp,shortHelp="Filter settings", longHelp="Change filter settings for visible objects")
        self.Bind(wx.EVT_TOOL, self.SetFilters, id=40)
        self.Bind(wx.EVT_TOOL_RCLICKED, self.SetFilters, id=40)


        #Export control
        tool = tb.AddLabelTool(50, "Export", save_bmp,shortHelp="Export list to text")
        self.Bind(wx.EVT_TOOL, self.ExportTxt, id=50)
        self.Bind(wx.EVT_TOOL_RCLICKED, self.ExportTxt, id=50)

        tb.AddSeparator()

        self.Bind(wx.EVT_TOOL_RCLICKED, self.OnToolRClick) # Match all
        
        cbID = wx.NewId()

        #Quick filter by type
        quicksort = tb.AddControl(
            wx.ComboBox(tb, cbID, "All Types",
                        choices=["All Types", "Star System","Open Cluster", "Globular Cluster", "Galaxy", "Nebula"],
                        size=(150,-1), style=wx.CB_DROPDOWN))
        
        self.Bind(wx.EVT_COMBOBOX, self.OnCombo, id=cbID)

        tb.AddSeparator()

        # Final thing to do for a toolbar is call the Realize() method. This
        # causes it to render (more or less, that is).
        tb.Realize()
        
        #displaypanel constraints
        lc = wx.LayoutConstraints()
        lc.top.SameAs(self, wx.Top, 10)
        lc.left.SameAs(self, wx.Left, 10)
        lc.bottom.SameAs(self, wx.Bottom, 10)
        lc.right.PercentOf(self, wx.Right, 50)
        self.displaypanel.SetConstraints(lc)
        #listpanel constraints
        lc = wx.LayoutConstraints()
        lc.top.SameAs(self, wx.Top, 10)
        lc.right.SameAs(self, wx.Right, 10)
        lc.bottom.SameAs(self, wx.Bottom, 30)
        lc.left.RightOf(self.displaypanel, 10)
        self.listpanel.SetConstraints(lc)

        self.listpanel.SetBackgroundColour("BLUE")
        self.displaypanel.SetBackgroundColour("BLACK")

        self.SetAutoLayout(True)
        self.Layout()

        #Bind events to actions
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.listpanel.list)
        self.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.OnItemDeselected, self.listpanel.list)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnItemActivated, self.listpanel.list)
        self.Bind(wx.EVT_LIST_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.listpanel.list)

        # for wxMSW
        self.Bind(wx.EVT_COMMAND_RIGHT_CLICK, self.OnRightClick)

        # for wxGTK
        self.Bind(wx.EVT_RIGHT_UP, self.OnRightClick)


    def GetColumnText(self, index, col):
        item = self.listpanel.list.GetItem(index, col)
        return item.GetText()


    def OnItemSelected(self, event):
        ind = event.m_itemIndex
        itemID = self.GetColumnText(ind, 1)
        self.currentItem = int(self.dict[itemID][-1])
        ##print self.currentItem,itemID,ind
##        #print "OnItemSelected: %s, %s, %s, %s\n" %(self.currentItem,
##                            self.listpanel.list.GetItemText(self.currentItem),
##                            self.GetColumnText(self.currentItem, 1),
##                            self.GetColumnText(self.currentItem, 2))
        self.displaypanel.setFChart(self.data[self.currentItem][-7])
        ##print self.data[self.currentItem][-7]
        self.displaypanel.setImage(self.data[self.currentItem][-6])
        self.displaypanel.setText(self.data[self.currentItem][-5])
        self.displaypanel.setLink(self.data[self.currentItem][0],self.data[self.currentItem][-3])
        
        event.Skip()


    def OnItemDeselected(self, evt):
        item = evt.GetItem()
        ##print "OnItemDeselected: %d" % evt.m_itemIndex

    def OnItemActivated(self, event):
        self.currentItem = event.m_itemIndex
        ##print "OnItemActivated: %s\nTopItem: %s" %(self.listpanel.list.GetItemText(self.currentItem),self.listpanel.list.GetTopItem())

    def OnBeginEdit(self, event):
        ##print "OnBeginEdit"
        event.Veto()

    def OnRightClick(self, event):
        ##print "OnRightClick %s\n" % self.listpanel.list.GetItemText(self.currentItem)

        # only do this part the first time so the events are only bound once
        if not hasattr(self, "popupID1"):
            self.popupID1 = wx.NewId()
            self.popupID2 = wx.NewId()
            self.popupID3 = wx.NewId()
            self.popupID4 = wx.NewId()
            self.popupID5 = wx.NewId()
            self.popupID6 = wx.NewId()

            self.Bind(wx.EVT_MENU, self.OnPopupOne, id=self.popupID1)
            self.Bind(wx.EVT_MENU, self.OnPopupTwo, id=self.popupID2)
            self.Bind(wx.EVT_MENU, self.OnPopupThree, id=self.popupID3)
            self.Bind(wx.EVT_MENU, self.OnPopupFour, id=self.popupID4)
            self.Bind(wx.EVT_MENU, self.OnPopupFive, id=self.popupID5)
            self.Bind(wx.EVT_MENU, self.OnPopupSix, id=self.popupID6)

        # make a menu
        menu = wx.Menu()
        # add some items
        menu.Append(self.popupID1, "FindItem tests")
        menu.Append(self.popupID2, "Iterate Selected")
        menu.Append(self.popupID3, "ClearAll and repopulate")
        menu.Append(self.popupID4, "DeleteAllItems")
        menu.Append(self.popupID5, "GetItem")
        menu.Append(self.popupID6, "Edit")

        # Popup the menu.  If an item is selected then its handler
        # will be called before PopupMenu returns.
        self.PopupMenu(menu)
        menu.Destroy()


    def OnPopupOne(self, event):
        print("Popup one\n")
        #print "FindItem:", self.listpanel.list.FindItem(-1, "Roxette")
        #print "FindItemData:", self.listpanel.list.FindItemData(-1, 11)

    def OnPopupTwo(self, event):
        #print "Selected items:\n"
        index = self.listpanel.list.GetFirstSelected()

        while index != -1:
            #print "      %s: %s\n" % (self.listpanel.list.GetItemText(index),self.listpanel.list.GetColumnText(index, 1))
            index = self.listpanel.list.GetNextSelected(index)

    def OnPopupThree(self, event):
        #print "Popup three\n"
        self.listpanel.list.ClearAll()
        wx.CallAfter(self.listpanel.list.Populate)

    def OnPopupFour(self, event):
        self.listpanel.list.DeleteAllItems()

    def OnPopupFive(self, event):
        item = self.listpanel.list.GetItem(self.currentItem)
        #print item.m_text, item.m_itemId, self.GetItemData(self.currentItem)

    def OnPopupSix(self, event):
        self.listpanel.list.EditLabel(self.currentItem)


    def OnToolClick(self, event):
        print("tool %s clicked\n" % event.GetId())
        #tb = self.GetToolBar()
        #tb = event.GetEventObject()
        #tb.EnableTool(10, not tb.GetToolEnabled(10))

    def OnToolRClick(self, event):
        print("tool %s right-clicked\n" % event.GetId())

    def OnCombo(self, evt):
        #"All Types", "Star System","Open Cluster", "Globular Cluster", "Galaxy", "Nebula"
        ch = evt.GetString()
        #print "combobox item selected: %s\n" % ch
        if ch == 'All Types':
            self.conds = None
        elif ch == 'Open Cluster':
            self.conds = ['type="OCl"']
        elif ch == 'Globular Cluster':
            self.conds = ['type="GCl"']
        elif ch == 'Open Cluster':
            self.conds = ['type="OCl"']
        elif ch == 'Star System':
            self.conds = ['type="Bin" OR type="Other" OR type="Mul"']
        elif ch == 'Galaxy':
            self.conds = ['type like "%Gal"']
        elif ch == 'Nebula':
            self.conds = ['type like "%Neb"']
        self.UpdateData()
    

    def OnDateChanged(self,event):
        #print "OnDateChanged: %s\n" % event.GetDate()
        self.JD = event.GetDate().GetJulianDayNumber()
        #print self.JD
        self.UpdateData()

    def UpdateData(self,flag=True):
        update_visible(dname,self.JD,longit=self.long,lat=self.lat,alt=self.alt,late=self.late)
        mylist = select(dname, 'vobjects',order='magnitude',limit=self.limit,conditions=self.conds)

        #get data in useful forms
        objlist=[]
        for i in range(0,len(mylist)):
            objlist.append(append(mylist[i],i))
        origdata = array(objlist,dtype='object')

        #Data and default values
        objdata = dict(list(zip(list(range(0,len(origdata))),origdata)))
        #print "objdata",objdata
        IDdict = dict(list(zip(origdata[:,1],origdata)))
        self.data = objdata
        self.dict = IDdict
        if flag:
            self.listpanel.list.itemDataMap = objdata
            self.listpanel.list.Repopulate()

    ##Creates dialog box for Lat Long input
    ## dialog box class defined in LocationDialog.py
    def SetLatLong(self, evt):    
        dlg = LocationDialog(self, -1, "Location: Lat, Long", size=(300, 200),
                         style=wx.DEFAULT_DIALOG_STYLE,
                         useMetal=False,
                         )
        dlg.CenterOnScreen()

        if self.lat >= 0:
            dlg.latdirec.SetStringSelection('N')
        else:
            dlg.latdirec.SetStringSelection('S')
            
        deg = abs(self.lat)
        minu= (deg%1)*60.
        secs= (minu%1)*60.
        
        dlg.latd.SetValue(str(int(deg)))
        dlg.latm.SetValue(str(int(minu)))
        dlg.lats.SetValue(str(int(secs)))

        if self.long >= 0:
            dlg.longdirec.SetStringSelection('E')
        else:
            dlg.longdirec.SetStringSelection('W')
        
        deg = abs(self.long)
        minu= (deg%1)*60.
        secs= (minu%1)*60.
        
        dlg.longd.SetValue(str(int(deg)))
        dlg.longm.SetValue(str(int(minu)))
        dlg.longs.SetValue(str(int(secs)))

        val = dlg.ShowModal() # this does not return until the dialog is closed.
        mylat=None
        mylong=None
        if val == wx.ID_OK:
            mylat,mylong=dlg.GetLatLong()
            self.lat = mylat
            self.long=mylong
            #print "You pressed OK\n%s,%s"%(mylat,mylong)
            alter_cell(dname,'defaults',[mylat],'lat','default','name')
            alter_cell(dname,'defaults',[mylong],'long','default','name')
            self.UpdateData()
        else:
            print("You pressed Cancel\n")
        dlg.Destroy()

    ##Creates dialog box for filter settings
    ## filter settings class defined in FilterDialog.py
    def SetFilters(self,evt):
        dlg = FilterDialog(self, -1, "Filter Settings", size=(300, 200),
                         style=wx.DEFAULT_DIALOG_STYLE,
                         useMetal=False,
                         )
        dlg.CenterOnScreen()
        dlg.altCtrl.SetValue(self.alt)
        dlg.limCtrl.SetValue(self.limit)
        dlg.lateCtrl.SetValue(self.late)
        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
        mylat=None
        mylong=None
        if val == wx.ID_OK:
            #print "You pressed OK\n"
            alt,limit,late=dlg.GetAltLimLate()
            #print alt,limit,late
            self.late=late
            self.limit =limit
            self.alt = alt
            alter_cell(dname,'defaults',[alt],'alt','default','name')
            alter_cell(dname,'defaults',[limit],'lim','default','name')
            alter_cell(dname,'defaults',[late],'late','default','name')
            self.UpdateData()
        else:
            print("You pressed Cancel\n")
        dlg.Destroy()

    def EditItem(self, evt):
        ind = self.currentItem
        itemID = self.data[self.currentItem][1]
        row = select(dname,'objects',conditions=["id='%s'"%(itemID)])[0]
        initial_im = row[-5]
        initial_fc = row[-6]
        # Create the wizard and the pages
        wizard = AddEditWizard(self,self.log,itemData=row)
        if wizard.RunWizard(wizard.page1):
            name,cID,other      = wizard.page2.GetInput()
            RA, dec, mycon      = wizard.page3.GetInput()
            mytype,mag,size,dist= wizard.page4.GetInput()
            fc_path,image       = wizard.page5.GetInput()
            desc,comm,link      = wizard.page6.GetInput()
            if image == initial_im:
                pass
            else:
                image = StoreImage(image)
            if fc_path == initial_fc:
                pass
            else:
                fc_path = StoreFC(fc_path)

            myrow = [name,cID,mytype,mag,size,dist,mycon,RA,dec,fc_path,image,desc,other,link,comm]
            update_row(dname,'objects',itemID,myrow,objectcols)
            wx.MessageBox("Wizard completed successfully", "That's all folks!")
            self.UpdateData()
        else:
            wx.MessageBox("Wizard was cancelled", "That's all folks!")
        wizard.Destroy()

    def AddItem(self, evt):
        # Create the wizard and the pages
        wizard = AddEditWizard(self,self.log,itemData=None)
        if wizard.RunWizard(wizard.page1):
            name,cID,other      = wizard.page2.GetInput()
            RA, dec, mycon      = wizard.page3.GetInput()
            mytype,mag,size,dist= wizard.page4.GetInput()
            fc_path,image       = wizard.page5.GetInput()
            desc,comm,link      = wizard.page6.GetInput()
            
            image = StoreImage(image)
            fc_path = StoreFC(fc_path)
            
            myrow = [name,cID,mytype,mag,size,dist,mycon,RA,dec,fc_path,image,desc,other,link,comm]
            add_row(dname,'objects',myrow)
            wx.MessageBox("Wizard completed successfully", "That's all folks!")
            self.UpdateData()
        else:
            wx.MessageBox("Wizard was cancelled", "That's all folks!")
        wizard.Destroy()

    def ExportTxt(self,evt):
        wildcard = "Txt File (*.txt)|*.txt|"     \
                   "All files (*.*)|*.*"
        
        dlg = wx.FileDialog(
            self, message="Save file as ...", defaultDir=os.getcwd(), 
            defaultFile="list.txt", wildcard=wildcard, style=wx.SAVE | wx.OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            
            delim = '\t'
            
            text = "Name\tID\tType\tMag\tSize(arcmin)\tDist(kly)\tConstln\tComments\n"
            for i in range(0,len(self.data)):
                text += self.GetColumnText(i, 0)
                for j in range(1,8):
                    text += delim + self.GetColumnText(i, j)
                text += '\n'         

            fp = file(path, 'w') # Create file anew
            fp.write(text)
            fp.close()
            wx.MessageBox("File successfully exported to tab delimited format!\n\n Can be opened in Excel via: 'Import Text File'.") 
        dlg.Destroy()

        

#---------------------------------------------------------------------------

if __name__ == '__main__':
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
    frame = MainFrame(None, wx.ID_ANY, "List of Objects") # A Frame is a top-level window.
    frame.Show(True)     # Show the frame.
    app.MainLoop()
#---------------------------------------------------------------------------
