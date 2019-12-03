from PIL import Image, ImageDraw, ImageFilter
import math




TESTFILENAME = 'TestVegetable.jpg'
TEMPLATEFILENAME = 'TemplateVegetable.jpg'
imTest = Image.open(TESTFILENAME).convert('L')
imTemp = Image.open(TEMPLATEFILENAME).convert('L')

TestWidth, TestHeight = imTest.size
TempWidth, TempHeight = imTemp.size
image_center_x = TestWidth / 2
image_center_y = TestHeight / 2

def logarithmic_search(pixTest, pixTemp, widthTest, heightTest, widthTemp, heightTemp, search_center_x, search_center_y):
    def normalized_cost(center_x, center_y):
        total_cost = 0
        test_cost = 0
        ref_cost = 0
        #print center_x, center_y
        for i in range(heightTemp):
            for j in range(widthTemp):
                total_cost += pixTemp[j, i] * pixTest[center_x + j, center_y + i]
                test_cost += pixTest[center_x + j, center_y + i] * pixTest[center_x + j, center_y + i]
                ref_cost += pixTemp[j, i] * pixTemp[j, i]
        # print total_cost / math.sqrt( test_cost * ref_cost )
        return total_cost / math.sqrt(test_cost * ref_cost)

    # starting the algorithm
    # initial center
    #search_center_x = widthTest / 2
    #search_center_y = heightTest / 2
    # initial step size
    step_size = 4.0
    breaking = 0
    #count = 1
    if search_center_x + step_size + widthTemp > widthTest or search_center_x - step_size < 0 or search_center_y + step_size + heightTemp > heightTest or search_center_y - step_size < 0:
        #print search_center_y + step_size + heightTemp, heightTest
        breaking = 1

    while step_size >= 1 and breaking == 0:
        # cost of center and 4 positions around the center along axis X-Y
        #print widthTest, heightTest, widthTemp, heightTemp,step_size
        #print count+1
        cost_center = normalized_cost(search_center_x, search_center_y)
        cost_left = normalized_cost(search_center_x - step_size, search_center_y)
        cost_right = normalized_cost(search_center_x + step_size, search_center_y)
        cost_up = normalized_cost(search_center_x, search_center_y + step_size)
        cost_down = normalized_cost(search_center_x, search_center_y - step_size)
        cost_upperRight = normalized_cost(search_center_x + step_size, search_center_y + step_size)
        cost_upperLeft = normalized_cost(search_center_x - step_size, search_center_y + step_size)
        cost_lowerRight = normalized_cost(search_center_x + step_size, search_center_y - step_size)
        cost_lowerLeft = normalized_cost(search_center_x - step_size, search_center_y - step_size)

        # finding maximum cost function
        cost_list = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        cost_list[0] = cost_center
        cost_list[1] = cost_left
        cost_list[2] = cost_right
        cost_list[3] = cost_up
        cost_list[4] = cost_down
        cost_list[5] = cost_upperRight
        cost_list[6] = cost_upperLeft
        cost_list[7] = cost_lowerRight
        cost_list[8] = cost_lowerLeft
        cost_list.sort()
        #print  cost_list
        maximum_cost = cost_list[8]

        if maximum_cost == cost_center:
            step_size /= 2.0
            #print 'center'
            #print search_center_x, search_center_y, step_size
        # print step_size
        else:
            #step_size = 8
            if maximum_cost == cost_left:
                search_center_x = search_center_x - step_size
            elif maximum_cost == cost_right:
                search_center_x = search_center_x + step_size
            elif maximum_cost == cost_up:
                search_center_y = search_center_y + step_size
                #print 'up'
                #print search_center_x, search_center_y, step_size
            elif maximum_cost == cost_down:
                search_center_y = search_center_y - step_size
                #print 'down'
                #print search_center_x, search_center_y, step_size
            elif maximum_cost == cost_upperRight:
                search_center_x = search_center_x + step_size
                search_center_y = search_center_y + step_size
            elif maximum_cost == cost_upperLeft:
                search_center_x = search_center_x - step_size
                search_center_y = search_center_y + step_size
            elif maximum_cost == cost_lowerLeft:
                search_center_x = search_center_x - step_size
                search_center_y = search_center_y - step_size
            else:
                #print 'else'
                search_center_x = search_center_x + step_size
                search_center_y = search_center_y - step_size
            step_size = 4
        #print 'bal'
        #print search_center_x, search_center_y, step_size
        if search_center_x + step_size + widthTemp > widthTest or search_center_x - step_size < 0 or search_center_y + step_size + heightTemp > heightTest or search_center_y - step_size < 0:
            breaking = 1
    return search_center_x, search_center_y



#starting algorithm
def hierarchical( imTesting , imTemping, leveling):
    if leveling == level+1:
        return 0, 0

    #low-filtering an image
    blurred_test = imTesting.filter(ImageFilter.BLUR)
    blurred_temp = imTemping.filter(ImageFilter.BLUR)

    #subsampled by 2
    blurred_test = blurred_test.resize((imTesting.size[0] / 2, imTesting.size[1] / 2), Image.BILINEAR)
    blurred_temp = blurred_temp.resize((imTemping.size[0] / 2, imTemping.size[1] / 2), Image.BILINEAR)
    pixTest = blurred_test.load()
    pixTemp = blurred_temp.load()
    widthTest, heightTest = blurred_test.size
    widthTemp, heightTemp = blurred_temp.size

    search_center_x, search_center_y = hierarchical(blurred_test, blurred_temp, leveling+1)
    #print search_center_x, search_center_y, leveling
    search_center_x = search_center_x * 2 + widthTest / 2
    search_center_y = search_center_y * 2 + heightTest / 2
    #print widthTest, heightTest, search_center_x, search_center_y, leveling

    best_x, best_y = logarithmic_search(pixTest, pixTemp, widthTest, heightTest, widthTemp, heightTemp, search_center_x, search_center_y)
    #print best_x, best_y, leveling
    if leveling == 0:
        blurred_test = imTesting.filter(ImageFilter.BLUR)
        blurred_temp = imTemping.filter(ImageFilter.BLUR)
        pixTest = blurred_test.load()
        pixTemp = blurred_temp.load()
        best_x -= search_center_x
        best_y -= search_center_y
        search_center_x = best_x * 2 + TestWidth / 2
        search_center_y = best_y * 2 + TestHeight / 2
        #return search_center_x, search_center_y
        #print TestWidth, TestHeight, TempWidth, TempHeight, search_center_x, search_center_y
        return logarithmic_search(pixTest, pixTemp, TestWidth, TestHeight, TempWidth, TempHeight, search_center_x, search_center_y)
        #return best_x, best_y
    else:
        return best_x - search_center_x, best_y - search_center_y



#define number of level
level = 2
bestPosition = hierarchical(imTest, imTemp, 0)









#showing pictorially
imTesting = Image.open(TESTFILENAME).convert('RGB')
draw = ImageDraw.Draw(imTesting)
draw.rectangle(((bestPosition[0], bestPosition[1]), (bestPosition[0] + TempWidth, bestPosition[1] + TempHeight)), outline="black")
imTesting.save("OutputHierarchical.jpg","JPEG")

#print(maximum_cost, search_center_x, search_center_y, breaking, step_size)
print(bestPosition[0], bestPosition[1])