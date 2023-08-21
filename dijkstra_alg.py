import random

import wx
import wx.lib.colourdb


class PictureFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Picture Frame")
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.bmp = None

    def prepare_image(self, nodes, edges):
        bmp = wx.Bitmap(1100, 1100)
        
        memdc = wx.MemoryDC(bmp)
        memdc.Clear()
        memdc.SetPen(wx.RED_PEN)
        memdc.SetBrush(wx.Brush("BLUE"))
        memdc.SetTextForeground(wx.GREEN)

        for (x, y) in nodes:
            memdc.DrawCircle(x+50, y+50, 10)
        for (i, j, w) in edges:
            memdc.DrawLine(nodes[i][0]+50, nodes[i][1]+50, nodes[j][0]+50, nodes[j][1]+50)
            tx = nodes[i][0] + (nodes[j][0] - nodes[i][0]) / 2
            ty = nodes[i][1] + (nodes[j][1] - nodes[i][1]) / 2
            memdc.DrawText(str(w), tx+50, ty+50)

        self.bmp = bmp
        self.Refresh()


    def on_paint(self, evt):
        evt.Skip()
        dc = wx.PaintDC(self)

        if self.bmp:
            dc.DrawBitmap(self.bmp, wx.Point(0, 0))



if "__main__" == __name__:
    nodes = sorted(set([(random.randrange(0, 100)*10, random.randrange(0, 100)*10) for i in range(15)]))
    edges = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if random.random() < 0.2:
                edges.append((i, j, random.randrange(10, 1000)))

    app = wx.App()
    frame = PictureFrame(None)
    frame.prepare_image(nodes, edges)
    frame.Maximize()
    frame.Show()
    app.MainLoop()