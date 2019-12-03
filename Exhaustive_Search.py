from PIL import Image, ImageFont, ImageDraw, ImageEnhance
import sys




TESTFILENAME = 'TestVegetable.jpg'
TEMPLATEFILENAME = 'TemplateVegetable.jpg'
imTest = Image.open(TESTFILENAME).convert('RGB')
imTemp = Image.open(TEMPLATEFILENAME).convert('RGB')



pixTest = imTest.load()
pixTemp = imTemp.load()
widthTest, heightTest = imTest.size
widthTemp, heightTemp = imTemp.size
colDiff = widthTest - widthTemp
rowDiff = heightTest - heightTemp




minSADred = sys.maxint
minSADgreen = sys.maxint
minSADblue = sys.maxint
bestRow = -1
bestCol = -1

for x in range(colDiff + 1):
    for y in range(rowDiff + 1):
        SADred = 0
        SADgreen = 0
        SADblue = 0
        for j in range(widthTemp):
            for i in range(heightTemp):
                SADred += abs(pixTest[x+j, y+i][0] - pixTemp[j, i][0])
                SADgreen += abs(pixTest[x+j, y+i][1] - pixTemp[j, i][1])
                SADblue += abs(pixTest[x+j, y+i][2] - pixTemp[j, i][2])

        if minSADred > SADred :
            if minSADgreen > SADgreen :
                if minSADblue > SADblue :
                    bestRow = x
                    bestCol = y
                    minSADred = SADred
                    minSADgreen = SADgreen
                    minSADblue = SADblue


draw = ImageDraw.Draw(imTest)
draw.rectangle(((bestRow, bestCol), (bestRow + heightTemp, bestCol + widthTemp)), outline="black")
imTest.save("OutputExhaustive.jpg","JPEG")

print(bestRow, bestCol)