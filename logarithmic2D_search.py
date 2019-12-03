from PIL import Image, ImageDraw
import math




TESTFILENAME = 'TestVegetable.jpg'
TEMPLATEFILENAME = 'TemplateVegetable.jpg'
imTest = Image.open(TESTFILENAME).convert('L')
imTemp = Image.open(TEMPLATEFILENAME).convert('L')



pixTest = imTest.load()
pixTemp = imTemp.load()
widthTest, heightTest = imTest.size
widthTemp, heightTemp = imTemp.size

"""
def normalized_cost(center_x, center_y):
    total_cost = 0
    test_cost = 0
    ref_cost = 0
    for j in range(widthTemp):
        for i in range(heightTemp):
            total_cost += pixTemp[j, i] * pixTest[center_x + j, center_y + i]
            test_cost += pixTest[center_x + j, center_y + i] * pixTest[center_x + j, center_y + i]
            ref_cost += pixTemp[j, i] * pixTemp[j, i]
    return total_cost / math.sqrt( test_cost * ref_cost )
"""
def normalized_cost(center_x, center_y):
    total_cost = 0
    test_cost = 0
    ref_cost = 0
    for i in range(heightTemp):
        for j in range(widthTemp):
            total_cost += pixTemp[j, i] * pixTest[center_x + j, center_y + i]
            test_cost += pixTest[center_x + j, center_y + i] * pixTest[center_x + j, center_y + i]
            ref_cost += pixTemp[j, i] * pixTemp[j, i]
    #print total_cost / math.sqrt( test_cost * ref_cost )
    return total_cost / math.sqrt( test_cost * ref_cost )


#starting the algorithm
#initial center
search_center_x = widthTest / 2
search_center_y = heightTest / 2
#initial step size
step_size = 4.0
breaking = 0
if search_center_x + step_size + widthTemp > widthTest and search_center_x - step_size < 0 and search_center_y + step_size + heightTemp > heightTest and search_center_y - step_size < 0 :
    breaking = 1

while step_size >= 1 and breaking == 0 :
    #cost of center and 4 positions around the center along axis X-Y
    cost_center = normalized_cost(search_center_x, search_center_y)
    cost_left = normalized_cost(search_center_x - step_size, search_center_y)
    cost_right = normalized_cost(search_center_x + step_size, search_center_y)
    cost_up = normalized_cost(search_center_x, search_center_y + step_size)
    cost_down = normalized_cost(search_center_x, search_center_y - step_size)


    #finding maximum cost function
    cost_list = [0.0, 0.0, 0.0, 0.0, 0.0]
    cost_list[0] = cost_center
    cost_list[1] = cost_left
    cost_list[2] = cost_right
    cost_list[3] = cost_up
    cost_list[4] = cost_down
    cost_list.sort()
    maximum_cost = cost_list[4]


    if maximum_cost==cost_center:
        step_size /= 2
        #print step_size
    else:
        if maximum_cost == cost_left:
            search_center_x = search_center_x - step_size
        elif maximum_cost == cost_right:
            search_center_x = search_center_x + step_size
        elif maximum_cost == cost_up:
            search_center_y = search_center_y + step_size
        else:
            search_center_y = search_center_y - step_size

        step_size = 4

    if search_center_x + step_size + widthTemp > widthTest and search_center_x - step_size < 0 and search_center_y + step_size + heightTemp > heightTest and search_center_y - step_size < 0:
        breaking = 1


#showing pictorially
imTesting = Image.open(TESTFILENAME).convert('RGB')
draw = ImageDraw.Draw(imTesting)
draw.rectangle(((search_center_x, search_center_y), (search_center_x + widthTemp, search_center_y + heightTemp)), outline="black")
imTesting.save("Output2DLogarithmic.jpg","JPEG")

#print(maximum_cost, search_center_x, search_center_y, breaking, step_size)
print(search_center_x, search_center_y)