#Location dialog box

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

class LocationDialog(wx.Dialog):
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
        label = wx.StaticText(self, -1, "Format: Degrees Minutes Seconds")
        label.SetFont(text_font)
        label.SetHelpText("Format: deg min sec")
        sizer.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        "Format: Degrees Minutes Seconds"

        box = wx.BoxSizer(wx.HORIZONTAL)

        ##Latitude section
        label = wx.StaticText(self, -1, "Latitude")
        label.SetHelpText("Enter d m s with spaces in between")
        box.Add(label, 1.3, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.latd = wx.TextCtrl(self, -1, "", size=(15,-1), validator=TxtDegreeValidator(90))
        self.latd.SetHelpText("Enter degrees [0,90]")
        box.Add(self.latd, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.latm = wx.TextCtrl(self, -1, "", size=(15,-1), validator=TxtDegreeValidator(60))
        self.latm.SetHelpText("Enter minutes [0,60]")
        box.Add(self.latm, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.lats = wx.TextCtrl(self, -1, "", size=(15,-1), validator=TxtDegreeValidator(60))
        self.lats.SetHelpText("Enter seconds [0,60]")
        box.Add(self.lats, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.latdirec = wx.ComboBox(self, -1, "N", choices=["N", "S"],size=(50,-1), style=wx.CB_DROPDOWN)
        self.latdirec.SetHelpText("Enter direction from equator")
        box.Add(self.latdirec, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 1, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        ##Longitude section
        label = wx.StaticText(self, -1, "Longitude")
        label.SetHelpText("Enter d m s with spaces in between")
        box.Add(label, 1.3, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.longd = wx.TextCtrl(self, -1, "", size=(15,-1), validator=TxtDegreeValidator(180))
        self.longd.SetHelpText("Enter degrees [0,180]")
        box.Add(self.longd, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.longm = wx.TextCtrl(self, -1, "", size=(15,-1), validator=TxtDegreeValidator(60))
        self.longm.SetHelpText("Enter minutes [0,60]")
        box.Add(self.longm, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.longs = wx.TextCtrl(self, -1, "", size=(15,-1), validator=TxtDegreeValidator(60))
        self.longs.SetHelpText("Enter seconds [0,60]")
        box.Add(self.longs, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        self.longdirec = wx.ComboBox(self, -1, "W", choices=["W", "E"],
                                     size=(50,-1), style=wx.CB_DROPDOWN)
        box.Add(self.longdirec, 1, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.longdirec.SetHelpText("Choose direction from Greenich England")

        sizer.Add(box, 1, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

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

    def GetLatLong(self):
        signs = dict(list(zip(['N','S','E','W'],[1,-1,1,-1])))
        lat  = float(self.latd.GetValue()) + float(self.latm.GetValue())/60. + float(self.lats.GetValue())/3600.
        longt= float(self.longd.GetValue()) + float(self.longm.GetValue())/60. + float(self.longs.GetValue())/3600.
        latsign = signs[self.latdirec.GetValue()]
        longsign= signs[self.longdirec.GetValue()]
        return lat*latsign,longt*longsign

#---------------------------------------------------------------------------

class TestPanel(wx.Panel):
    def __init__(self, parent, log):
        self.log = log
        wx.Panel.__init__(self, parent, -1)

        b = wx.Button(self, -1, "Create and Show a custom Dialog", (50,50))
        self.Bind(wx.EVT_BUTTON, self.OnButton, b)

    def OnButton(self, evt):    
        dlg = LocationDialog(self, -1, "Location: Lat, Long", size=(300, 200),
                         style=wx.DEFAULT_DIALOG_STYLE,
                         useMetal=False,
                         )
        dlg.CenterOnScreen()

        # this does not return until the dialog is closed.
        val = dlg.ShowModal()
        mylat=None
        mylong=None
        if val == wx.ID_OK:
            print("You pressed OK\n")
            mylat,mylong=dlg.GetLatLong()
            print(mylat,mylong)
        else:
            print("You pressed Cancel\n")
        dlg.Destroy()
        return mylat,mylong
        

#---------------------------------------------------------------------------

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

        if key < wx.WXK_SPACE or key == wx.WXK_DELETE or key > 255:
            event.Skip()
            return

        if chr(key) in string.digits or key == wx.WXK_SPACE or key ==wx.WXK_SUBTRACT or key==46:
            event.Skip()
            return

        if not wx.Validator_IsSilent():
            wx.Bell()

        # Returning without calling even.Skip eats the event before it
        # gets to the text control
        return

    def TransferToWindow(self):
        """ Transfer data from validator to window.

         The default implementation returns False, indicating that an error
         occurred.  We simply return True, as we don't do any data transfer.
        """
        return True # Prevent wxDialog from complaining.


    def TransferFromWindow(self):
        """ Transfer data from window to validator.

         The default implementation returns False, indicating that an error
         occurred.  We simply return True, as we don't do any data transfer.
        """
        return True # Prevent wxDialog from complaining.

#---------------------------------------------------------------------------


if __name__ == '__main__':
    import sys
    app = wx.App(False)  # Create a new app, don't redirect stdout/stderr to a window.
    frame = wx.Frame(None)
    tp = TestPanel(frame,sys.stdout)
    frame.Show(True)     # Show the frame.
    app.MainLoop()

