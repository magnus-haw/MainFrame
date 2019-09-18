#Add/Edit wizard main class

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

import  wx
import  wx.wizard as wiz
from numpy import array
from WizardPages import NamePage,NumberPage,TitlePage
from WizardPages import ImagePage, LocationPage,CommentPage

testrow = array([u'Albireo', u'Beta Cyg', u'Bin', u'3.18', u'0.583', u'0.45',
        u'Cyg', u'19.5120277778', u'27.9596388889',
        u'/graphics/finding_charts/Albireo.html',
        u'graphics/images/Albireo.jpg',
        u'Albireo (Beta Cyg) is the fifth brightest star in the constellation Cygnus. Although it has the Bayer designation beta, it is fainter than Gamma Cygni, Delta Cygni, and Epsilon Cygni. Albireo appears to the naked eye to be a single star of magnitude 3 but through a telescope, even low magnification views resolve it into a double star. The brighter yellow star (actually itself a very close binary system) makes a striking colour contrast with its fainter blue companion star.',
        u"Hen's beak, Menchir", u'http://en.wikipedia.org/wiki/Albireo',
        u'Can split with low power. Nice dual color binary.'], 
      dtype='<U477')

class mylog:
    def __init__(self,flag=True):
        self.log = ""
        self.flag=flag
    def write(self,txt):
        if self.flag:
            print txt
        self.log += txt + '\n'
  
#----------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Run Simple Wizard", pos=(50, 50))
        self.Bind(wx.EVT_BUTTON, self.OnRunSimpleWizard, b)
        

    def OnRunSimpleWizard(self, evt):
        # Create the wizard and the pages
        wizard = AddEditWizard(self,self.log,itemData=None)
        if wizard.RunWizard(wizard.page1):
            name,cID,other      = wizard.page2.GetInput()
            RA, dec, mycon      = wizard.page3.GetInput()
            mytype,mag,size,dist= wizard.page4.GetInput()
            fc_path,image       = wizard.page5.GetInput()
            desc,comm,link      = wizard.page6.GetInput()

            myrow = [name,cID,mytype,mag,size,dist,mycon,RA,dec,fc_path,image,desc,other,link,comm]
            
            wx.MessageBox("Wizard completed successfully!", "That's all folks!")
        else:
            wx.MessageBox("Wizard was cancelled", "That's all folks!")
        wizard.Destroy()


#---------------------------------------------------------------------------

class AddEditWizard(wiz.Wizard):
    def __init__(self, parent,log,itemData=None):
        # Create the wizard and the pages
        self.log = log
        wizard = wiz.Wizard.__init__(self, parent, wx.ID_ANY, "Add/Edit Wizard")

        pageData =[]
        print(itemData)
        if itemData is None:
            for i in range(0,5):
                pageData.append(None)
        else:
            pageData.append([itemData[0],itemData[1],itemData[-3]])
            pageData.append([itemData[7],itemData[8],itemData[6]])
            pageData.append([itemData[2],itemData[3],itemData[4],itemData[5]])
            pageData.append([itemData[9],itemData[10]])
            pageData.append([itemData[-4],itemData[-1],itemData[13]])
            
        self.page1 = TitlePage(self, "Instructions")
        self.page2 = NamePage(self,self.log,data=pageData[0])
        self.page3 = LocationPage(self,self.log,data=pageData[1])
        self.page4 = NumberPage(self,self.log,data=pageData[2])
        self.page5 = ImagePage(self,self.log,data=pageData[3])
        self.page6 = CommentPage(self,self.log,data=pageData[4])
        
        self.page1.sizer.Add(wx.StaticText(self.page1, -1, """
This wizard is is designed to add an object to the
observing database. Before beginning, make sure you
know the following information:

Name, Catalog ID, Object type, Visual magnitude,
Size in arcminutes, distance (kly), constellation,
Right Ascension, Declination, a finding chart, an
image, a paragraph description, other popular names,
a web link, and a brief comment.

"""))
        self.FitToPage(self.page1)

        # Use the convenience Chain function to connect the pages
        wiz.WizardPageSimple_Chain(self.page1, self.page2)
        wiz.WizardPageSimple_Chain(self.page2, self.page3)
        wiz.WizardPageSimple_Chain(self.page3, self.page4)
        wiz.WizardPageSimple_Chain(self.page4, self.page5)
        wiz.WizardPageSimple_Chain(self.page5, self.page6)

        self.GetPageAreaSizer().Add(self.page1)

        self.Bind(wiz.EVT_WIZARD_PAGE_CHANGED, self.OnWizPageChanged)
        self.Bind(wiz.EVT_WIZARD_PAGE_CHANGING, self.OnWizPageChanging)
        self.Bind(wiz.EVT_WIZARD_CANCEL, self.OnWizCancel)


    def OnWizPageChanged(self, evt):
        if evt.GetDirection():
            dir = "forward"
        else:
            dir = "backward"

        page = evt.GetPage()
        self.log.write("OnWizPageChanged: %s, %s\n" % (dir, page.__class__))


    def OnWizPageChanging(self, evt):
        if evt.GetDirection():
            dir = "forward"
        else:
            dir = "backward"

        page = evt.GetPage()
        self.log.write("OnWizPageChanging: %s, %s\n" % (dir, page.__class__))


    def OnWizCancel(self, evt):
        page = evt.GetPage()
        self.log.write("OnWizCancel: %s\n" % page.__class__)


    def OnWizFinished(self, evt):
        self.log.write("OnWizFinished\n")


#---------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
    frame = wx.Frame(None)
    log = mylog()
    tp = TestPanel(frame,log)
    frame.Show(True)     # Show the frame.
    app.MainLoop()
#---------------------------------------------------------------------------
