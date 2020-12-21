#!/usr/bin/python3
#
# My solution for Day 20 Part 1
#
# PROBLEM
#    Given a set of "Input Images" consisting of 8-by-8 binary maps, each
#    tagged with a specific "Image ID", construct a mosaic by matching the
#    edges. Tiles may need rotating and/or flipping to align along the borders.
#
# QUESTION:
#      What is the product of the IDs of the 4 corner tiles?
import sys


datfile="../data/day20_input.txt"
#datfile="../data/day20_test.txt"

###############################################################################
# Every day starts with a....
def read_images(fromfile) :
    images={}
    with open(fromfile,"r") as imagefile:
        inImage=False
        imageID=0
        imageMatrix=[]
        for l in imagefile:
            #Have we found an image? Take advantage of the well-formatted input
            if l[0:4] == "Tile" :
                imageID = int(l[5:9])
                inImage=True
                images[imageID] = {}
                continue
            if inImage and (l[0] == "." or l[0] == "#" ) :
                imageMatrix.append(l.strip())
                continue
            elif len(l.strip())==0 :
                #End of image. Write.
                images[imageID]['image']=imageMatrix
                imageID=0
                imageMatrix=[]
                inImage=False
            else :
                print(f"Input invalid or unexpected? - |{l}|")
        if len(imageMatrix)>0 and imageID>0 :
            images[imageID]['image'] = imageMatrix
    return images

###############################################################################
# Convert a string of #/. into a number (expecting 10-bit so 0-1024)
def calcBinNumber(str) :
    bStr = str.replace(".","0").replace("#","1")
    strInt = int(bStr,2)
    #print(f"{str}->{bStr}->{strInt}")
    return strInt

###############################################################################
# Matching borders is going to be easier if we do it by calculating an ID
# number matching the #/. pattern "down" that edge...
def calc_border_ints(image) :
    bIDS={}
    #Top & bottom are easy
    bIDS['top'] = calcBinNumber(image[0])
    bIDS['bottom'] = calcBinNumber(image[len(image)-1]) #Ought to be 7....

    #Left and Right aren't *too* much harder....
    lStr=''
    rStr=''
    for i in image :
        lStr += i[0]
        rStr += i[len(i)-1]
    bIDS['left'] = calcBinNumber(lStr)
    bIDS['right'] = calcBinNumber(rStr)

    #To support "flipping" (horiz/vert) we need to calculate the numbers
    #under that translation (essentially going big-endian <-> little-endian)

    #Top & Bottom change under a horizontal flip
    bIDS['top_mirror'] = calcBinNumber(image[0][::-1])
    bIDS['bottom_mirror'] = calcBinNumber(image[len(image)-1][::-1])

    #Left & Right change under a vertical flip
    bIDS['left_mirror'] = calcBinNumber(lStr[::-1])
    bIDS['right_mirror'] = calcBinNumber(rStr[::-1])


    return bIDS

###############################################################################
###############################################################################
###############################################################################
if __name__ == '__main__' :
    images = read_images(datfile)
    print(f"Got {len(images.keys())} images from {datfile}")

    #Augment each image with ID numbers for the borders, both normal and
    #reversed. Also build up a reversed version linking borderIDs back to
    #images....
    borderRefs={}
    for id in images.keys() :
        bIDS=calc_border_ints(images[id]['image'])
        images[id]['borders'] = bIDS
        for k in bIDS.keys() :
            if bIDS[k] not in borderRefs :
                borderRefs[bIDS[k]] = {id : k}
            else :
                borderRefs[bIDS[k]][id]=k

    #Now each borderRefs ID should have 1 or 2 Image IDs associated with it.
    #If it's got 2, it's a linked vertex
    #If it's got 1, it's a border.
    #There should be 16 one-ID links - 2 per image in the corner with reflections
    edgeImages={}
    for i in borderRefs.keys() :
        if len(borderRefs[i].keys()) == 1 :
            for k,v in borderRefs[i].items() :
                if k not in edgeImages :
                    edgeImages[k] = [v]
                else :
                    edgeImages[k].append(v)

    #Border images are those with 4 edges (2 normal, 2 mirrored) in the edgeImages
    #list.
    cImages=[]
    for i in edgeImages.keys() :
        if len(edgeImages[i])==4 :
            cImages.append(i)

    if len(cImages) == 4 :
        p=1
        for c in cImages :
            p *= c
        print(f"Product of corner images {cImages} is : {p}")
    else :
        print(f"ERROR. Mis-calculation of corner images, expected 4 got {cImages}")
