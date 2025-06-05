class Point:
    __x = 0
    __y = 0
    epsilon = 0

    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y

    def getX(self):
        return self.__x
    
    def getY(self):
        return self.__y
    
    def equals(self, otherPoint):
        if (otherPoint == None):
            return False
        elif (abs(self.__x - otherPoint.getX()) <= Point.epsilon and abs(self.__y - otherPoint.getY()) <= Point.epsilon):
            return True
        else:
            return False
        
    def setEpsilon(newEpsilon):
        Point.epsilon = newEpsilon

    def copy(self):
        return Point(self.getX(), self.getY())