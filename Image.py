import numpy as np
import random
import cv2
from copy import deepcopy

class Image:
    
    def __init__(self, image, numberOfPolygons):
        self.image_base = image
        self.image_w_polygons = np.copy(self.image_base)
        self.polygons = []
        self.polygon_colors = []
        for i in range(numberOfPolygons):
            self.addPolygon()
    
    def show(self):
        cv2.imshow('Image', self.image_w_polygons)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def showBase(self):
        cv2.imshow('Image', self.image_base)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    def differenceFrom(self, otherImage):
        assert self.image_base.shape == otherImage.image_base.shape
        
        total_rmse = 0
        for row_idx, row in enumerate(self.image_w_polygons):
            for pixel_idx, thisImagePixel in enumerate(row):
                otherImagePixel = otherImage.image_w_polygons[row_idx][pixel_idx]
                
                total_rmse += np.sqrt(np.mean((thisImagePixel-otherImagePixel)**2))
                
        return total_rmse
    
    def addPolygon(self):
        points = []
        for i in range(3):
            points += [[random.randint(0, len(self.image_base)), random.randint(0, len(self.image_base[0]))]]
        color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        
        self.polygons.append(points)
        self.polygon_colors.append(color)
        cv2.fillPoly(self.image_w_polygons, np.asarray([points], dtype=np.int32),  color)
        
    def createChild(self, otherImage):
        childPolygon = self.meanOfTwoPolygonLists(self.polygons, otherImage.polygons)
        childColors = self.meanOfTwoColorLists(self.polygon_colors, otherImage.polygon_colors)
        assert len(childPolygon) == len(self.polygons)
        
        child = Image(self.image_base,0)
        child.polygons = childPolygon
        child.polygon_colors = childColors
        child.applyPolygons()
        
        return child
        
    def meanOfTwoPolygonLists(self, one, two):
        assert len(one) == len(two)
        meanList = []
        for idx, polygon in enumerate(one):
            newPolygon = []
            for point in range(len(polygon)):
                coords1 = one[idx][point]
                coords2 = two[idx][point]
                newCoords = [(coords1[0]+coords2[0])//2, (coords1[1]+coords2[1])//2]
                newPolygon.append(newCoords)
            meanList.append(newPolygon)
        return meanList
    
    def meanOfTwoColorLists(self, one, two):
        assert len(one) == len(two)
        meanList = []
        for idx, color in enumerate(one):
            newColor = ((one[idx][0]+two[idx][0])//2, (one[idx][1]+two[idx][1])//2, (one[idx][2]+two[idx][2])//2)
            meanList.append(newColor)
        return meanList
    
    def applyPolygons(self):
        for i, points in enumerate(self.polygons):
            color = self.polygon_colors[i]
            cv2.fillPoly(self.image_w_polygons, np.asarray([points], dtype=np.int32),  color)
            
    def mutateRandomPolygon(self):
        polygonIndex = random.randint(0,len(self.polygons)-1)
        for idx, coord in enumerate(self.polygons[polygonIndex]):
            newCoord = [coord[1],coord[0]]
            self.polygons[polygonIndex][idx] = newCoord
        
        self.polygon_colors[polygonIndex] = ((random.randint(0,255)),(random.randint(0,255)),(random.randint(0,255)))
        self.applyPolygons()
    
    def createMutatedChild(self):
        child = Image(self.image_base, 0)
        child.polygons = deepcopy(self.polygons)
        child.polygon_colors = deepcopy(self.polygon_colors)
        
        polygonIndex = random.randint(0,len(child.polygons)-1)
        for idx, coord in enumerate(child.polygons[polygonIndex]):
            newCoord = [coord[1],coord[0]]
            child.polygons[polygonIndex][idx] = newCoord 
            
        child.polygon_colors[polygonIndex] = ((random.randint(0,255)),(random.randint(0,255)),(random.randint(0,255)))
        child.applyPolygons()
        return child
    
    def mergeParents(self, otherImage):

        child = Image(self.image_base,0)
        child.polygons = self.polygons
        child.polygon_colors = self.polygon_colors
        
        random_idx = random.randint(0,len(self.polygons)-1)
        child.polygons[random_idx:] = otherImage.polygons[random_idx:]
        child.polygon_colors[random_idx:] = otherImage.polygon_colors[random_idx:]
        
        child.applyPolygons()
        
        return child