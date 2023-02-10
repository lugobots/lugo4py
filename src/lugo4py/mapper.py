from .protos import physics_pb2
from .protos import server_pb2

from . import specs

from math import floor

# ErrMinCols defines an error for invalid number of cols
ErrMinCols = AttributeError("number of cols lower the minimum")
# ErrMaxCols defines an error for invalid number of cols
ErrMaxCols = AttributeError("number of cols higher the maximum")
# ErrMinRows defines an error for invalid number of rows
ErrMinRows = AttributeError("number of rows lower the minimum")
# ErrMaxRows defines an error for invalid number of rows
ErrMaxRows = AttributeError("number of rows higher the maximum")


# MinCols Define the min number of cols allowed on the field division by the Mapper
MinCols = 4
# MinRows Define the min number of rows allowed on the field division by the Mapper
MinRows = 2
# MaxCols Define the max number of cols allowed on the field division by the Mapper
MaxCols = 200
# MaxRows Define the max number of rows allowed on the field division by the Mapper
MaxRows = 100


def mirrorCoordsToAway(center):
    mirrored = physics_pb2.Point
    mirrored.x = (specs.MAX_X_COORDINATE - center.x)
    mirrored.y = (specs.MAX_Y_COORDINATE - center.y)
    return mirrored

class Mapper:
    def __init__(self, cols: int, rows: int, side: server_pb2.Team.Side):
        if (cols < MinCols):
            raise ErrMinCols

        if (cols > MaxCols):
            raise ErrMaxCols

        if (rows < MinRows):
            raise ErrMinRows

        if (rows > MaxRows):
            raise ErrMaxRows

        self.cols = cols
        self.rows = rows
        self.side = side
        self.regionWidth = specs.MAX_X_COORDINATE / cols
        self.regionHeight = specs.MAX_Y_COORDINATE / rows

    def getRegion(self, col: int, row: int): 
        col = max(0, col)
        col = min(self.cols - 1, col)

        row = max(0, row)
        row = min(self.rows - 1, row)

        center = physics_pb2.Point()
        center.x = (round((col * self.regionWidth) + (self.regionWidth / 2)))
        center.y = (round((row * self.regionHeight) + (self.regionHeight / 2)))

        if (self.side == server_pb2.Team.Side.AWAY):
            center = mirrorCoordsToAway(center)

        return Region(
            col,
            row,
            self.side,
            center,
            self,
        )

    def getRegionFromPoint(self, point: physics_pb2.Point):
        if (self.side == server_pb2.Team.Side.AWAY):
            point = mirrorCoordsToAway(point)

        cx = floor(point.x / self.regionWidth)
        cy = floor(point.y / self.regionHeight)
        col = min(cx, self.cols - 1)
        row = min(cy, self.rows - 1)
        return self.getRegion(col, row)

class Region:
    def __init__(self, col:int , row:int, side:server_pb2.Team.Side, center:physics_pb2.Point, positioner:Mapper):
        self.col = col
        self.row = row
        self.side = side
        self.center = center
        self.positioner = positioner

    def eq(self, region): 
        return region.getCol() == self.col and region.side == self.side and region.getRow() == self.row

    def getCol(self):
        return self.col

    def getRow(self):
        return self.row

    def getCenter(self):
        return self.center

    def toString(self):
        return "{"+self.col+","+self.row+"}"

    def front(self):
        return self.positioner.getRegion(max(self.col + 1, 0), self.row)

    def back(self): 
        return self.positioner.getRegion(max(self.col - 1, 0), self.row)

    def left(self): 
        return self.positioner.getRegion(self.col, max(self.row + 1, 0))

    def sright(self): 
        return self.positioner.getRegion(self.col, max(self.row - 1, 0))

