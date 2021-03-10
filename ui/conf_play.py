# 选择项目

# 是否进行完全匹配：
## -尝试匹配次数：？
## -每次匹配间隔：

# 热键配置
## 开始播放：F1
## 循环播放：F2
## 暂停播放：F3
## 继续播放：F4
## 重新播放：F5
## 退出：F8

# 'match': {
#     'times': 10, # 在执行click事件的时候，是否需要匹配有没有目标元素
#     'interval': 0.5, # 在执行click事件的时候，是否需要匹配有没有目标元素
# },
# 'project': {
#     'name': 'temp', # 录制的项目名，默认为temp
#     'path': '.\\business\\' # 录制项目的存储路径
# },
# 'hotkey': {
#     'play': {
#         u'开始': 'F1',
#         u'循环': 'F2',
#         u'暂停': 'F3',
#         u'继续': 'F4',
#         u'结束': 'F5',
#     },
#     'record': {
#         u'开始': 'F1',
#         u'暂停': 'F2',
#         u'继续': 'F3',
#         u'结束': 'F4',
#     }
# }
# 开始按钮
# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class MyFrame
###########################################################################
FN_KEY = [ u"F1", u"F2", u"F3", u"F4", u"F5", u"F6", u"F7", u"F8", u"F9", u"F10", u"F11", u"F12" ]
FN_TITLE = [ u"开始播放", u"循环播放", u"暂停播放", u"继续播放", u"停止播放", u"F6", u"F7", u"退出", u"F9", u"F10", u"F11", u"F12" ]
class MyFrame ( wx.Frame ):

  def __init__( self, parent ):
    wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 629,478 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
    
    self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
    self.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWFRAME ) )
    
    main_frame = wx.BoxSizer( wx.VERTICAL )
    # 文件选框
    self.__FilePickerModule__( main_frame )

    # 是否匹配背景
    self.__MatchConfirmModule__( main_frame )

    # 配置快捷键
    self.__HotKeyConfigModule__( main_frame )
    
    # 底部按钮
    self.__ConfirmButtonModule__( main_frame )
    
    self.SetSizer( main_frame )
    self.Layout()
    
    self.Centre( wx.BOTH )

  def __del__( self ):
    pass

  def __CreateSelect__ ( self, fgSizer, title ):
    m_staticText = wx.StaticText( self, wx.ID_ANY, title, wx.Point( -1,-1 ), wx.Size( -1,-1 ), wx.ALIGN_RIGHT )
    m_staticText.Wrap( -1 )
    m_staticText.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_SCROLLBAR ) )
    m_staticText.SetMinSize( wx.Size( 100,-1 ) )

    fgSizer.Add( m_staticText, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

    options = FN_KEY
    def_index = FN_TITLE.index(title)
    m_choice = wx.Choice( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, options, 0 )
    m_choice.SetSelection( def_index ) # 设置默认值
    fgSizer.Add( m_choice, 0, wx.ALL, 5 )
    return m_choice

  def __HotKeyConfigModule__ ( self, main_frame ):
    # 创建标题
    m_staticText = wx.StaticText( self, wx.ID_ANY, u"配置快捷键：", wx.DefaultPosition, wx.DefaultSize, 0 )
    m_staticText.Wrap( -1 )
    m_staticText.SetFont( wx.Font( 11, 70, 90, 90, False, "宋体" ) )
    m_staticText.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
    main_frame.Add( m_staticText, 0, wx.ALL, 5 )

    # 创建配置表
    fgSizer = wx.FlexGridSizer( 3, 4, 15, 15 )
    fgSizer.SetFlexibleDirection( wx.BOTH )
    fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

    # 创建下拉选框
    self.__CreateSelect__(fgSizer, u'开始播放')
    self.__CreateSelect__(fgSizer, u'继续播放')
    self.__CreateSelect__(fgSizer, u'循环播放')
    self.__CreateSelect__(fgSizer, u'停止播放')
    self.__CreateSelect__(fgSizer, u'暂停播放')
    self.__CreateSelect__(fgSizer, u'退出')
    main_frame.Add( fgSizer, 0, wx.EXPAND, 5 )
    return main_frame

  def __MatchConfirmModule__ (self, main_frame):
    
    fgSizer = wx.FlexGridSizer( 0, 3, 0, 0 )
    fgSizer.SetFlexibleDirection( wx.BOTH )
    fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )

    fgSizer.SetMinSize( wx.Size( -1,50 ) ) 
    self.m_staticText5 = wx.StaticText( self, wx.ID_ANY, u"是否进行背景匹配：", wx.DefaultPosition, wx.DefaultSize, 0 )
    self.m_staticText5.Wrap( -1 )
    self.m_staticText5.SetFont( wx.Font( 11, 70, 90, 90, False, "宋体" ) )
    self.m_staticText5.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )

    fgSizer.Add( self.m_staticText5, 0, wx.ALL, 5 )

    self.m_radioBtn1 = wx.RadioButton( self, wx.ID_ANY, u"是", wx.DefaultPosition, wx.DefaultSize, 0 )
    self.m_radioBtn1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_SCROLLBAR ) )

    fgSizer.Add( self.m_radioBtn1, 0, wx.ALL, 5 )

    self.m_radioBtn2 = wx.RadioButton( self, wx.ID_ANY, u"否", wx.DefaultPosition, wx.DefaultSize, 0 )
    self.m_radioBtn2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_SCROLLBAR ) )
    
    fgSizer.Add( self.m_radioBtn2, 0, wx.ALL, 5 )
    
    main_frame.Add( fgSizer, 0, wx.EXPAND, 5 )

  def __FilePickerModule__ (self, main_frame):
    fgSizer = wx.FlexGridSizer( 0, 2, 0, 0 )
    fgSizer.SetFlexibleDirection( wx.BOTH )
    fgSizer.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
    
    fgSizer.SetMinSize( wx.Size( -1,60 ) ) 
    m_staticText = wx.StaticText( self, wx.ID_ANY, u"选择项目：", wx.DefaultPosition, wx.DefaultSize, 0 )
    m_staticText.Wrap( -1 )
    m_staticText.SetFont( wx.Font( 11, 70, 90, 90, False, "宋体" ) )
    m_staticText.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
    
    fgSizer.Add( m_staticText, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )
    
    m_filePicker = wx.FilePickerCtrl( self, wx.ID_ANY, wx.EmptyString, u"选择要执行的项目", u"*.*", wx.DefaultPosition, wx.Size( 500,-1 ), wx.FLP_DEFAULT_STYLE )
    m_filePicker.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWFRAME ) )
    m_filePicker.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWFRAME ) )
    
    fgSizer.Add( m_filePicker, 0, wx.ALL, 5 )
    
    main_frame.Add( fgSizer, 0, wx.EXPAND, 5 )

  def __ConfirmButtonModule__ (self, main_frame):
    m_sdbSizer = wx.StdDialogButtonSizer()
    m_sdbSizerOK = wx.Button( self, wx.ID_OK )
    m_sdbSizerCancel = wx.Button( self, wx.ID_CANCEL )
    m_sdbSizer.AddButton( m_sdbSizerOK )
    m_sdbSizer.AddButton( m_sdbSizerCancel )
    m_sdbSizer.Realize()
    main_frame.Add( m_sdbSizer, 1, wx.ALIGN_CENTER, 5 )
    # Connect Events
    m_sdbSizerOK.Bind( wx.EVT_BUTTON, self.confirmEvent )
    m_sdbSizerCancel.Bind( wx.EVT_BUTTON, self.cancelEvent )

  # Virtual event handlers, overide them in your derived class
  def cancelEvent( self, event ):
    event.Skip()
    self.Hide()
  
  def confirmEvent( self, event ):
    event.Skip()
    self.Hide()

if __name__== "__main__":
    app = wx.App()
    frame = MyFrame(parent=None)
    frame.Show()
    app.MainLoop()