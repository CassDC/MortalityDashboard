import uuid

class Graph:
    def __init__(self, title, xtitle, ytitle, type, x, y, tick_angle=None):
        self.id = str(uuid.uuid4())
        self.title = title
        self.xtitle = xtitle
        self.ytitle = ytitle
        self.type = type
        self.x = x  # Contains X values for the graph
        self.y = y  # Contains DataRow values for the graph (ie. y values + label)
        self.tick_angle = tick_angle


class FoliumMap:
    def __init__(self, name, title):
        self.id = str(uuid.uuid4())
        self.name = name
        self.title = title


class LabeledTimeSeries:
    def __init__(self, values, name):
        self.values = values
        self.name = name


class Table:
    def __init__(self, values, title, col1, col2):
        self.values = values
        self.title = title
        self.col1 = col1
        self.col2 = col2


class InfoBox:
    def __init__(self, title, value):
        self.title = title
        self.value = value
