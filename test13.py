import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class MyFrame1
###########################################################################

class MyFrame ( wx.Frame ):
  
  def __init__( self, parent ):
    wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.Point( 0,0 ), size = wx.Size( 816,708 ), style = wx.DEFAULT_FRAME_STYLE, name = u"test" )
    
    self.SetSizeHintsSz( wx.Size( 0,0 ), wx.Size( 1024,768 ) )
    self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_INFOBK ) )
    self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
    
    fgSizer2 = wx.FlexGridSizer( 0, 2, 0, 0 )
    fgSizer2.SetFlexibleDirection( wx.BOTH )
    fgSizer2.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
    
    self.m_textCtrl2 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.Point( 0,22 ), wx.DefaultSize, 0 )
    fgSizer2.Add( self.m_textCtrl2, 0, wx.ALL, 5 )
    
    self.m_button1 = wx.Button( self, wx.ID_ANY, _(u"确认"), wx.DefaultPosition, wx.DefaultSize, 0 )
    fgSizer2.Add( self.m_button1, 0, wx.ALL, 5 )
    
    self.m_textCtrl3 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
    fgSizer2.Add( self.m_textCtrl3, 0, wx.ALL, 5 )
    
    self.m_button2 = wx.Button( self, wx.ID_ANY, _(u"MyButton"), wx.DefaultPosition, wx.DefaultSize, 0 )
    fgSizer2.Add( self.m_button2, 0, wx.ALL, 5 )
    
    self.m_textCtrl4 = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
    fgSizer2.Add( self.m_textCtrl4, 0, wx.ALL, 5 )
    
    self.m_button3 = wx.Button( self, wx.ID_ANY, _(u"MyButton"), wx.DefaultPosition, wx.DefaultSize, 0 )
    fgSizer2.Add( self.m_button3, 0, wx.ALL, 5 )
    
    
    self.SetSizer( fgSizer2 )
    self.Layout()
    
    self.Centre( wx.BOTH )
  
if __name__== "__main__":
    app = wx.App()
    frame = MyFrame(parent=None)
    frame.Show()
    app.MainLoop()