import random

import numpy as np
import wx
from wx.lib.floatcanvas import NavCanvas, FloatCanvas, Resources
import wx.lib.colourdb


class FLCFrame(wx.Frame):
    """
    A simple frame that contains just an owner-drawn area.
    """
    def __init__(self, parent, nodes, edges, title="Canvas"):
        super().__init__(parent, title=title)
        h = wx.BoxSizer(wx.HORIZONTAL)
        self.nc = NavCanvas.NavCanvas(self, Debug = 0, BackgroundColor = "WHITE")
        h.Add(self.nc, flag=wx.EXPAND, proportion=2)
        self.SetSizer(h)

        self.nodes = nodes
        self.edges = edges

        self.draw_map()

    def draw_map(self):
        self.nc.Canvas.InitAll()
        for (x, y) in self.nodes:
            self.nc.Canvas.AddCircle((x, y), Diameter=10, LineColor="RED", FillColor="BLACK")
        for (i, j, w) in self.edges:
            self.nc.Canvas.AddLine([self.nodes[i], self.nodes[j]], LineWidth=1, LineColor="BLACK")
            tx = self.nodes[i][0] + (self.nodes[j][0] - self.nodes[i][0]) / 2
            ty = self.nodes[i][1] + (self.nodes[j][1] - self.nodes[i][1]) / 2
            self.nc.Canvas.AddText(str(w), (tx, ty), Position="tc", Size=20, Color="BLACK")
        self.nc.Canvas.ZoomToBB()


if "__main__" == __name__:
    nodes = sorted(set([(random.randrange(0, 100)*10, random.randrange(0, 100)*10) for i in range(20)]))
    edges = []
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            if random.random() < 0.2:
                edges.append((i, j, random.randrange(10, 1000)))

    app = wx.App()
    frame = FLCFrame(None, nodes, edges, title="Bleee Bleee")
    frame.Show()
    frame.Maximize()
    app.MainLoop()