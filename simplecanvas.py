import random
import threading
import time

import numpy as np
import wx


class SimpleCanvasFrame(wx.Frame):
    COLORS = {
        0: (0, 0, 0),
        1: (255, 255, 255),
        2: (255, 0, 0),
        3: (0, 255, 0),
        4: (0, 0, 255),
        5: (255, 255, 0),
        6: (255, 0, 255),
        7: (0, 255, 255),
        8: (128, 0, 0),
        9: (0, 128, 0),
        10: (0, 0, 128),
        11: (128, 128, 0),
        12: (128, 0, 128),
        13: (0, 128, 128),
        14: (128, 128, 128),
        15: (192, 192, 192),
    }
    MAX_COLOR = 16
    def upd_colors_db(self):
        def c():
            return random.choice((64, 128, 192, 255))
        for i in range(16, 128):
            self.COLORS[i] = (c(), c(), c())
        self.MAX_COLOR = 128

    """
    A simple frame that contains just an owner-drawn area.
    """
    def __init__(self, parent, title="Canvas", func=None, width=600, height=300):
        super().__init__(parent, title=title)
        self.upd_colors_db()

        self.height = height
        self.width = width
        h = wx.BoxSizer(wx.HORIZONTAL)

        # Create the canvas
        self.canvas = wx.Panel(self)
        self.canvas.Bind(wx.EVT_PAINT, self.on_paint)
        self.log = wx.ListBox(self, style=wx.LB_SINGLE)
        h.Add(self.canvas, proportion=3, flag=wx.EXPAND)
        h.Add(self.log, proportion=1, flag=wx.EXPAND)
        self.SetSizer(h)

        self.data = np.zeros((height, width, 3), dtype=np.uint8)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_timer, self.timer)
        self.timer.Start(10)
        self.c_idx = 0
        self.x = 0
        self.y = 0

        if func:
            threading.Thread(target=func, args=(self, )).start()

    def on_paint(self, evt):
        """
        Draw the bitmap (self.data) on the panel.
        """
        evt.Skip()
        dc = wx.PaintDC(self.canvas)
        (w, h) = self.canvas.GetClientSize()
        sc_x = w // self.width
        sc_y = h // self.height
        sc = max((0, min((sc_x, sc_y))))
        dc.SetUserScale(sc, sc)
        dc.DrawBitmap(wx.Bitmap.FromBuffer(self.width, self.height, self.data), 0, 0)

    def on_timer(self, evt):
        evt.Skip()
        self.canvas.Refresh()

    def draw_point(self, x, y, color):
        """
        Draw a point on the bitmap.
        """
        self.do_log("[{} {}] => {}".format(x, y, color))
        self.data[y, x, :] = self.COLORS[color % self.MAX_COLOR]

    def do_log(self, t):
        wx.CallAfter(self.log.Insert, t, 0)
        wx.CallAfter(self.log.EnsureVisible, 0)

    def __setitem__(self, coords, color):
        self.draw_point(coords[0], coords[1], color)


def run_function(func, width=600, height=300):
    """
    Run the given function in a frame.
    """
    app = wx.App()
    frame = SimpleCanvasFrame(None, title="Bleee Bleee",
                              func=func, width=width, height=height)
    frame.Show()
    frame.Maximize()
    app.MainLoop()