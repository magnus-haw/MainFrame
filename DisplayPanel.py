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

import wx,os
import wx.lib.agw.hyperlink as hl
from string import lower

class MyDisplayPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1, style=wx.WANTS_CHARS)

        tID = wx.NewId()
        
        #Create Sizers
        vsizer = wx.BoxSizer(wx.VERTICAL)
        
        #Initialize image
        self.Image = wx.StaticBitmap(self, bitmap=wx.EmptyBitmap(100, 100))
        vsizer.Add(self.Image,4, wx.ALIGN_CENTRE|wx.ALL, 5)

        #Object web link
        self.hyper = hl.HyperLinkCtrl(self, wx.ID_ANY, "",URL="",style=wx.HL_ALIGN_CENTRE)
        self.hyper.SetColours(link=wx.Colour(0, 0, 255), visited=wx.Colour(0,0,255), rollover=wx.Colour(0, 0, 255))
        self.hyper.SetFont(wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD))
        vsizer.Add(self.hyper,0, wx.ALIGN_CENTRE|wx.ALL|wx.EXPAND, 5)

        #Description text 
        self.txt = wx.TextCtrl(self, -1, "", (20,10), style=wx.TE_MULTILINE|wx.BORDER_NONE|wx.TE_NO_VSCROLL)
        self.txt.SetEditable(False)
        self.txt.SetForegroundColour("white")
        self.txt.SetBackgroundColour("black")
        vsizer.Add(self.txt,3, wx.EXPAND|wx.ALL, 5)

        
        #Finding chart link
        self.FChart = hl.HyperLinkCtrl(self, wx.ID_ANY, "Open Finding Chart",URL="",style=wx.HL_ALIGN_CENTRE)
        self.FChart.SetColours(link=wx.Colour(0, 0, 255), visited=wx.Colour(0,0,255), rollover=wx.Colour(0, 0, 255))
        self.FChart.SetFont(wx.Font(18, wx.SWISS, wx.NORMAL, wx.BOLD))
        vsizer.Add(self.FChart,1, wx.ALIGN_CENTRE|wx.ALL, 5)
        #Define layout constraints
##        lc = wx.LayoutConstraints()
##        lc.top.SameAs(self, wx.Top, 10)
##        lc.left.SameAs(self, wx.Left, 10)
##        lc.bottom.PercentOf(self, wx.Bottom, 50)
##        lc.right.SameAs(self, wx.Right, 10)
##        lc.centreX.SameAs(self, wx.CentreX)
##        
##        self.Image.SetConstraints(lc)
##
##        lc = wx.LayoutConstraints()
##        lc.top.PercentOf(self, wx.Bottom, 53)
##        lc.right.SameAs(self, wx.Right, 10)
##        lc.bottom.PercentOf(self, wx.Bottom, 57)
##        lc.left.SameAs(self,wx.Left, 10)
##        self.hyper.SetConstraints(lc)
##
##        txtc = wx.LayoutConstraints()
##        txtc.top.Below(self.hyper, 1)
##        txtc.right.SameAs(self, wx.Right, 10)
##        txtc.bottom.SameAs(self, wx.Bottom, 90)
##        txtc.left.SameAs(self,wx.Left, 10)
##        self.txt.SetConstraints(txtc)
##
##        fcc = wx.LayoutConstraints()
##        fcc.top.Below(self.txt, 1)
##        fcc.right.SameAs(self, wx.Right, 10)
##        fcc.left.SameAs(self,wx.Left, 10)
##        fcc.bottom.SameAs(self, wx.Bottom, 10)
##        self.FChart.SetConstraints(fcc)

        self.SetSizer(vsizer)
        self.sizer = vsizer
        self.SetAutoLayout(True)

    def setText(self,text):
        if text == None:
            text = ""
        #print text
        text = "Description:\n\n" + text
        self.txt.SetValue(text)
            
    def setLink(self,label,url):
        if label == None or url == None:
            label=''
            url=''
        self.hyper.SetLabel(label)
        self.hyper.SetURL(url)

    def setFChart(self,url):
        if url == None:
            url=''
        cwd = os.getcwd()
        URL ='file://' + cwd+ '/' + url
        self.FChart.SetURL(URL)
        print("URL",self.FChart.GetURL())
        
    def setImage(self,fname):
        if lower(fname[-4:]) == '.jpg' or lower(fname[-4:]) == '.jpeg':
            ftype = wx.BITMAP_TYPE_JPEG
        elif lower(fname[-4:]) == '.png':
            ftype = wx.BITMAP_TYPE_PNG
        elif lower(fname[-4:]) == '.bmp':
            ftype = wx.BITMAP_TYPE_BMP
        elif lower(fname[-4:]) == '.gif':
            ftype = wx.BITMAP_TYPE_GIF
        else:
            img = wx.EmptyBitmap(300, 300)
            self.Image.SetBitmap(wx.BitmapFromImage(img))
            return
        img = wx.Image(fname,ftype)
        size = img.GetSize()
        img = img.Rescale(300.*size[0]/size[1], 300)

        self.Image.SetBitmap(wx.BitmapFromImage(img))
        self.SendSizeEvent()
