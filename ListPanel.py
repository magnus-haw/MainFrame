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

import wx
import  wx.lib.mixins.listctrl  as  listmix
import sys

class MyListCtrl(wx.ListCtrl,
                   listmix.ListCtrlAutoWidthMixin,
                   listmix.ColumnSorterMixin):
    def __init__(self, parent, ID, objdata, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        self.itemDataMap = objdata

        #populate intial list
        self.Populate()

        #define sorter
        listmix.ColumnSorterMixin.__init__(self, 8)
        self.SortListItems(3, True)

    def Populate(self):
        self.InsertColumn(0, "Name")
        self.InsertColumn(1, "ID", wx.LIST_FORMAT_RIGHT)
        self.InsertColumn(2, "Type")
        self.InsertColumn(3, "Mag")
        self.InsertColumn(4, "Size (arcmin)")
        self.InsertColumn(5, "Dist (kly)")
        self.InsertColumn(6, "Constellation")
        self.InsertColumn(7, "Comments")

        items = self.itemDataMap.items()
        for key, data in items:
            #print key,data
            index = self.InsertStringItem(sys.maxint, data[0])
            for i in range(1,7):
                self.SetStringItem(index, i, str(data[i]))
            self.SetStringItem(index, 7, str(data[-2]))
            mykey = int(data[-1])
            #print index,mykey
            self.SetItemData(index, mykey)

        for i in range(0,8):
            self.SetColumnWidth(i, wx.LIST_AUTOSIZE)
        

    def Repopulate(self):
        self.DeleteAllItems()
        self.DeleteAllColumns()
        self.Populate()

    # Used by the ColumnSorterMixin, see wx/lib/mixins/listctrl.py
    def GetListCtrl(self):
        return self
    
class MyListCtrlPanel(wx.Panel):
    def __init__(self, parent, log, objdata):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)

        self.log = log
        tID = wx.NewId()
        
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.list = MyListCtrl(self, tID, objdata,
                                 style=wx.LC_REPORT 
                                 #| wx.BORDER_SUNKEN
                                 | wx.BORDER_NONE
                                 | wx.LC_EDIT_LABELS
                                 | wx.LC_SORT_ASCENDING
                                 #| wx.LC_NO_HEADER
                                 #| wx.LC_VRULES
                                 #| wx.LC_HRULES
                                 #| wx.LC_SINGLE_SEL
                                 )
        
        sizer.Add(self.list, 1, wx.EXPAND)

        self.SetSizer(sizer)
        self.SetAutoLayout(True)
