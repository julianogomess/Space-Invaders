import pygame

class Retangulo(object):
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

class Circulo(object):
    def __init__(self,x,y,raio):
        self.x = x
        self.y = y
        self.r = raio

def intersectRC(retangulo,circulo):
    cx = abs(circulo.x - retangulo.x - retangulo.w/2)
    xDist = retangulo.w/2 + circulo.r
    if cx >xDist:
        return False
    cy = abs(circulo.y - retangulo.y - retangulo.h/2)
    yDist = retangulo.h / 2 + circulo.r
    if cy > yDist:
        return False
    if cx <= retangulo.w/2 or cy <= retangulo.h/2:
        return True
    xCornerDist = cx - retangulo.w/2
    yCornerDist = cy - retangulo.h/2
    xCornerDistSq = xCornerDist * xCornerDist
    yCornerDistSq = yCornerDist * yCornerDist
    maxCornerDistSq = circulo.r * circulo.r
    return xCornerDistSq+yCornerDistSq<=maxCornerDistSq

def intersectRR(retangulo1,retangulo2):
    if retangulo1.x < retangulo2.x+retangulo2.w and retangulo1.x + retangulo1.w>retangulo2.x and retangulo1.y <retangulo2.y +retangulo2.h and retangulo1.y + retangulo1.h > retangulo2.y:
        return True
    return False


