#Filter Settings dialog box

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
import string
#---------------------------------------------------------------------------
# Create and set a help provider.  Normally you would do this in
# the app's OnInit as it must be done before any SetHelpText calls.
provider = wx.SimpleHelpProvider()
wx.HelpProvider.Set(provider)

#---------------------------------------------------------------------------

class FilterDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, size=wx.DefaultSize, pos=wx.DefaultPosition, 
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False,
            ):

        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)

        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)


        # Now continue with the normal construction of the dialog
        # contents
        sizer = wx.BoxSizer(wx.VERTICAL)
        text_font = wx.Font(15, wx.SWISS, wx.NORMAL, wx.NORMAL)

        box = wx.BoxSizer(wx.HORIZONTAL)

        ##Altitude control section
        label = wx.StaticText(self, -1, "Min Altitude")
        label.SetHelpText("Minimum altitude cutoff [0-30]")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.altCtrl = wx.SpinCtrl(self, -1, "", (30, 50))
        self.altCtrl.SetRange(0,35)
        self.altCtrl.SetValue(25)
        box.Add(self.altCtrl, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        ##Limit control
        label = wx.StaticText(self, -1, "Max # Objects")
        label.SetHelpText("Limits number objects displayed in list")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.limCtrl = wx.SpinCtrl(self, -1, "", (30, 50))
        self.limCtrl.SetRange(10,250)
        self.limCtrl.SetValue(50)
        box.Add(self.limCtrl, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        self.limCtrl.SetHelpText("Max number objects listed [1,250]")
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        ##Late hour control section
        label = wx.StaticText(self, -1, "Time Cutoff")
        label.SetHelpText("Latest hour of observation")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.lateCtrl = wx.SpinCtrl(self, -1, "", (30, 50))
        self.lateCtrl.SetRange(1,24)
        self.lateCtrl.SetValue(23)
        box.Add(self.lateCtrl, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        btn.SetHelpText("The OK button completes the dialog")
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        btn.SetHelpText("The Cancel button cancels the dialog.")
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        self.SetSizer(sizer)
        sizer.Fit(self)

    def GetAltLimLate(self):
        signs = dict(zip(['N','S','E','W'],[1,-1,1,-1]))
        alt  = int(self.altCtrl.GetValue())
        late = int(self.lateCtrl.GetValue())
        lim  = int(self.limCtrl.GetValue())
        return alt,lim,late

#---------------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Filter Settings Dialog", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

    def OnButton(self, evt):    
        dlg = FilterDialog(self, -1, "Filter Settings", size=(300, 200),
                         style=wx.DEFAULT_DIALOG_STYLE,
                         useMetal=False,
                         )
        dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
        mylat=None
        mylong=None
        if val == wx.ID_OK:
            print "You pressed OK\n"
            alt,limit,late=dlg.GetAltLimLate()
            print alt,limit,late
        else:
            print "You pressed Cancel\n"
        dlg.Destroy()
        return alt,limit,late
        



#---------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
    frame = wx.Frame(None)
    tp = TestPanel(frame,sys.stdout)
    frame.Show(True)     # Show the frame.
    app.MainLoop()
#---------------------------------------------------------------------------
