#!/usr/bin/python3
#
# My solution for Day 20 Part 2. 36 hours in the making.
#
# PROBLEM
#    Given a set of "Input Images" consisting of 8-by-8 binary maps, each
#    tagged with a specific "Image ID", construct a mosaic by matching the
#    edges. Tiles may need rotating and/or flipping to align along the borders.
#    Once the image is assembled and oriented, search it for "monster" patterns.
#
# QUESTION:
#    After excluding "monsters", how many "waves" (unassigned '#' chars)
#    remain?
import sys
import math

datfile="../data/day20_input.txt"
#datfile="../data/day20_test.txt"


# Nessie looks like:
#             1         2
#   012345678901234567890
# 0|                  #
# 1|#    ##    ##    ###
# 2| #  #  #  #  #  #
nessie=[
    [18,0],
    [0,1],[5,1],[6,1],[11,1],[12,1],[17,1],[18,1],[19,1],
    [1,2],[4,2],[7,2],[10,2],[13,2],[16,2]
    ]

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
    image[0] = image[0].replace(".","0").replace("#","1")
    bIDS['top'] = int(image[0],2)
    image[len(image)-1] = image[len(image)-1].replace(".","0").replace("#","1")
    bIDS['bottom'] = int(image[len(image)-1],2)

    #Left and Right aren't *too* much harder....
    lStr=''
    rStr=''
    for i in range(len(image)) :
        line=list(image[i])
        line[0] = line[0].replace(".","0").replace("#","1")
        line[len(line)-1] = line[len(line)-1].replace(".","0").replace("#","1")

        lStr += line[0]
        rStr += line[len(line)-1]
        image[i] = "".join(line)
    bIDS['left'] = int(lStr,2) #calcBinNumber(lStr)
    bIDS['right'] = int(rStr,2) #calcBinNumber(rStr)

    #To support "flipping" (horiz/vert) we need to calculate the numbers
#    for r in image:
#        print(f"\t{r}")
    #Top & Bottom change under a horizontal flip
#    print(f"top: {image[0]} ({bIDS['top']}) bottom: {image[len(image)-1]} ({bIDS['bottom']})")
    bIDS['top_mirror'] = calcBinNumber(image[0][::-1])
    bIDS['bottom_mirror'] = calcBinNumber(image[len(image)-1][::-1])
#    print(f"top_mirror: {image[0][::-1]} ({bIDS['top_mirror']}) bottom_mirror: {image[len(image)-1][::-1]} ({bIDS['bottom_mirror']})")

    #Left & Right change under a vertical flip
#    print(f" left: {lStr} ({bIDS['left']})  right: {rStr} ({bIDS['right']})")
    bIDS['left_mirror'] = calcBinNumber(lStr[::-1])
    bIDS['right_mirror'] = calcBinNumber(rStr[::-1])
    #print(f" left_mirror: {lStr[::-1]} ({bIDS['left_mirror']})  right_mirror: {rStr[::-1]} ({bIDS['right_mirror']})")

    return bIDS

###############################################################################
def flipHorizontal(toFlip) :
    flipped=[]
    for row in toFlip :
        fRow = row[::-1]
        flipped.append(fRow)
    return flipped
###############################################################################
def flipVertical(toFlip) :
    flipped=[]
    for row in toFlip[::-1] :
        flipped.append(row)
    return flipped
###############################################################################
def rotateRight(srcImage) :
    matrix=[]
    #Initialise a blank.
    for i in range(len(srcImage)) :
        matrix.append([])
        for j in range(len(srcImage)) :
            matrix[i].append('.')
    #Rotate 90 right is the transformation (x,y)->(y,-x)
    #(we translate y by +len to keep above the join)
    offset=len(srcImage)-1
    for x in range(len(srcImage)) :
        for y in range(len(srcImage)) :
            toX=y
            toY=(-1*x) + offset
            #print(f"({x},{y})->({toX},{toY})")
            matrix[y][x] = srcImage[toY][toX]
    #And just join the rows back
    rotated=[]
    for r in range(len(srcImage)) :
        rotated.append(''.join(matrix[r]))
    return rotated
###############################################################################
def rotateLeft(srcImage) :
    matrix=[]
    for i in range(len(srcImage)) :
        matrix.append([])
        for j in range(len(srcImage)) :
            matrix[i].append('.')
    #Rotate 90 left is the transformation (x,y)->(-y,x)
    #(we translate y by +len to keep above the join)
    offset=len(srcImage)-1
    for x in range(len(srcImage)) :
        for y in range(len(srcImage)) :
            toX=(-1*y)+offset
            toY=x
            matrix[y][x] = srcImage[toY][toX]
    rotated=[]
    for r in range(len(srcImage)) :
        rotated.append(''.join(matrix[r]))
    return rotated

###############################################################################
# helper for later visualisation, also used for calculating vertices
def turnBorderToBinary(image) :
    image[0] = image[0].replace(".","0").replace("#","1")
    image[len(image)-1] = image[len(image)-1].replace(".","0").replace("#","1")
    for i in range(len(image)) :
        l=list(image[i])
        l[0] = l[0].replace(".","0").replace("#","1")
        l[len(l)-1] = l[len(l)-1].replace(".","0").replace("#","1")
        image[i]="".join(l)
    return image

###############################################################################
def simple_vertex_calc(image) :
    vert={}
    vert["t"] = int(image[0],2)
    vert["b"] = int(image[len(image)-1],2)
    lStr=''
    rStr=''
    for i in image :
        lStr += i[0]
        rStr += i[len(i)-1]
    vert["l"] = int(lStr,2)
    vert["r"] = int(rStr,2)
    return vert

###############################################################################
def permute_image(img) :
    permute =  {
        'normal'     : img,
        'right'      : rotateRight(img),
        'diagonal'   : rotateRight(rotateRight(img)),
        'left'       : rotateLeft(img),
        'horizontal' : flipHorizontal(img),
        'vertical'   : flipVertical(img),
        'right_horizontal' : rotateRight(flipHorizontal(img)),
        'right_vertical'  : rotateRight(flipVertical(img))
    }
    return permute

###############################################################################
def calc_permute_vertices(permImg) :
    borders = {
        'normal' : simple_vertex_calc(permImg['normal']),
        'right' : simple_vertex_calc(permImg['right']),
        'diagonal' : simple_vertex_calc(permImg['diagonal']),
        'left' : simple_vertex_calc(permImg['left']),
        'horizontal' : simple_vertex_calc(permImg['horizontal']),
        'vertical' : simple_vertex_calc(permImg['vertical']),
        'right_horizontal' : simple_vertex_calc(permImg['right_horizontal']),
        'right_vertical' : simple_vertex_calc(permImg['right_vertical'])
    }
    return borders

###############################################################################
def add_overlay_to_bitmap(bitmap,overlay,offset) :
    for p in overlay :
        bitmap[p[1]+offset[1]][p[0]+offset[0]] = "O"
    return bitmap

###############################################################################
# It's a match if all the points in nessie map to '#' chars
def match_nessie(bitmap,x,y) :
    global nessie
    mP=[]
    for p in nessie :
        if bitmap[p[1]+y][p[0]+x] != '#' :
            return False
        else :
            mP.append([p[0]+x,p[1]+y])
    return True

###############################################################################
# We probably could do a RegEx search but that's multi-line and I don't wanna.
# So we'll define as a sparse array and search from offsets. As a convenience,
# return an altered bitmap with all found Nessies overlaid on the original
# (which actually makes *answering the question asked* easier as well as looking
#  good....)
def search_for_nessie(img) :
    #Strictly speaking we don't need to do this but it'll make life easier to
    #treat the whole image as a point-addressable "bitmap"
    srchImg=[]
    for r in img :
        srchImg.append(list(r))
    #We can search the image by permuting across from a start-point that's
    #3-down-from-top and along as far as 19-left-of-end looking for nessie matches
    nessieMatches=[]
    print(f"imgDim x={len(srchImg[0])}, y={len(srchImg)}")
    for y in range(0,len(srchImg)-2) :
        for x in range(0,len(srchImg[0])-19) :
            if match_nessie(srchImg,x,y) :
                nessieMatches.append([x,y])
    for m in nessieMatches :
        srchImg = add_overlay_to_bitmap(srchImg,nessie,m)
    return len(nessieMatches), srchImg

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
        exit(1)

###################################################################################
    print("-"*80)
    #
    #PART TWO BEGINS HERE......
    #

    #ITS BRUTE FORCE TIME.
    #Each Tile can have 8 orientations -
    #  original,
    #  flippedVertical,
    #  flippedHorizontal,
    #  flippedHorizontal & flippedVertical ("flippedDiagonal", also a double-rotation)
    #  rotatedRight
    #  rotatedLeft
    #  flippedVertical + rotatedRight (or flippedHorizontal + rotatedLeft)
    #  flippedHorizontal + rotatedright ( or flippedVertical + rotatedLeft)

    #PERMUTE THE TILES and calc no-mirror IDs for all.
    imgPermute={}
    borders={}
    for i in images :
        imgPermute[i] = permute_image(turnBorderToBinary(images[i]['image']))
        borders[i] = calc_permute_vertices(imgPermute[i])

    #RIGHT, we have a FULLY PERMUTATED LIST.
    #build the rows as before.
    usedImages = [ cImages[0] ]
    dimSize = int(math.sqrt(len(images)))
    imgRef = []
    for y in range(dimSize) :
        imgRef.append([])
        for x in range(dimSize) :
            imgRef[y].append([])

    #FIRST ONE'S A BIT TRICKY - we don't know the orientation of the original
    #tile. Work it out.
    iFrom=usedImages[len(usedImages)-1]
    for k in borders[iFrom].keys() :
        fVert = borders[iFrom][k]['b']
        for iTo in images :
            if iTo in usedImages or iTo == iFrom :
                continue
            for tVert in borders[iTo].keys() :
                if fVert == borders[iTo][tVert]['t'] :
                    #Try the first match. Update both the FROM and TO orientations.
                    imgRef[0][0] = [iFrom,k]
                    imgRef[1][0] = [iTo,tVert]
                    usedImages.append(iTo)
                    break
            if len(imgRef[0][0]) != 0 :
                break #we found an answer.

    #DO THE REST OF THE FIRST COLUMN:
    y=2
    while y < dimSize :
        iFrom = usedImages[len(usedImages)-1]
        iOrient = imgRef[y-1][0][1]
        #Get the "down" link to match the vertex
        dVert = borders[iFrom][iOrient]['b']
        #Our "From" is now fixed in orientation which makes the sub-search easier
        for iTo in images:
            if iTo in usedImages or iTo == iFrom :
                continue
            for tOrient in borders[iTo].keys() :
                if dVert == borders[iTo][tOrient]['t'] :
                    imgRef[y][0] = [iTo,tOrient]
                    usedImages.append(iTo)
                    y+=1
                    break

    #NOW FILL IN THE ROWS:
    for y in range(dimSize) :
        for x in range(dimSize) :
            iFrom = imgRef[y][x][0]
            iOrient = imgRef[y][x][1]
            #We're looking RIGHT now.
            rVert = borders[iFrom][iOrient]['r']
            #print(f"{imgRef[y][x]} -> {rVert}")
            for iTo in images:
                if iTo in usedImages or iTo == iFrom :
                    continue
                for tOrient in borders[iTo].keys() :
                    #print(f"{iTo}->{tOrient}->{borders[iTo][tOrient]['l']}")
                    if rVert == borders[iTo][tOrient]['l'] :
                        x+=1
                        imgRef[y][x] = [iTo,tOrient]
                        usedImages.append(iTo)
                        break
        #Move on to the next line....
        y+=1

    #ASSEMBLE THIS MOTHER-LOVING IMAGE:
    bigImage=[]
    #Image height needs "stitch rows" removing.
    imgHeight = len(imgPermute[imgRef[0][0][0]]['normal'])-2
    maxY=len(imgRef)*imgHeight
    print("Image is ", maxY, " rows high")
    for i in range(maxY) :
        bigImage.append('')
    bigY=0
    for row in imgRef :
        for col in row :
            i,o=col
            img=imgPermute[i][o]
            for littleY in range(1,len(img)-1) :
                offset = bigY*imgHeight + littleY-1
                bigImage[offset] += img[littleY][1:len(img[littleY])-1]
        bigY+=1

    #OH DEAR GOD WE MADE IT (or something like it)
    #AN ASSEMBLED IMAGE:
    #for r in bigImage :
    #    print(r)

    #AND NOW WE'RE READY TO START ON PART TWO OF THE MOTHER-LOVING PROBLEM.
    permutedBigImages = permute_image(bigImage)
    for t in permutedBigImages.keys() :
        img=permutedBigImages[t]
        numMatches,matchImage = search_for_nessie(img)
        if numMatches>0 :
            for r in matchImage:
                print("".join(r))
            print(f"{t} image permutation has {numMatches} Nessie matches")
            #AND THE ANSWER TO THE QUESTION IS.....
            waveCount=0
            for y in range(len(matchImage)) :
                for x in range(len(matchImage[0])) :
                    if matchImage[y][x] == '#' :
                        waveCount += 1
            print(f"This leaves {waveCount} Wave Matches Remaining")
        else :
            print(f"{t} image permutation has no Nessie matches")
