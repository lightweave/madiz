"""
This script uses Raspberry Pi camera to capture pictures and analyze the radiation background.
The script counts the number of exposed pixels, classifies them into groups
and then puts the corresponding data into a log file for further analysis.
"""

import sys
import datetime
from io import BytesIO
from PIL import Image, ImageEnhance
import numpy as np
import picamera

def is_overexposed(img):
    """
    Check if the image is overexposed.
    Parameters:
        img - input image
    Return:
        True if the image is overexposed, False otherwise
    """

    pixel_values = list(img.getdata())
    mean_intensity = sum(pixel_values) / len(pixel_values)
    threshold = 100
    return mean_intensity <= threshold

def Mean(mass, ddof = 0):
    '''
    Returns mean value of massive of values
    '''
    return sum(mass) / (len(mass) - ddof)


def Cov_matrix(mass_points):
    '''
    Counts covariant matrix of massive of 2D vectors (dots)
    '''

    # Count mean values

    M_0 = Mean([point[0] for point in mass_points])
    M_1 = Mean([point[1] for point in mass_points])
#    print(M_0, M_1)


    # Count covariations
    cov_00 = Mean([(point[0] - M_0)**2 for point in mass_points], ddof = 1)
    cov_11 = Mean([(point[1] - M_1)**2 for point in mass_points], ddof = 1)

    cov_01 = Mean([(point[0] - M_0)*(point[1] - M_1) for point in mass_points], ddof = 1)


    return [[cov_00, cov_01], [cov_01, cov_11]]


def EigenValues(matrix):
    '''
    Evaluates eigenvalues of 2D matrix
    '''

    D_sqrt = ((matrix[0][0]-matrix[1][1])**2 + 4*matrix[0][1]*matrix[1][0])**0.5
    lamb_1 = (matrix[0][0] + matrix[1][1] + D_sqrt) / 2
    lamb_2 = (matrix[0][0] + matrix[1][1] - D_sqrt) / 2


    return [lamb_1, lamb_2]


'''
def EigenVectors(matrix, v_lamb):

    Evaluates eigenvectors, using eigenvalues and 2D matrix
    
    if matrix[0][1] != 0:
        k_1 = (v_lamb[0] - matrix[0][0]) / matrix[0][1]
        k_2 = (v_lamb[1] - matrix[0][0]) / matrix[0][1]
    else:
        k_1 = (v_lamb[0] - matrix[0][0]) * 1e10
        k_2 = (v_lamb[1] - matrix[0][0]) * 1e10

    vec_1 = [1 / (k_12 + 1)0.5, k_1 / (k_12 + 1)0.5]
    vec_2 = [1 / (k_22 + 1)0.5, k_2 / (k_22 + 1)0.5]


    return [vec_1, vec_2]
'''


def PCA_analyse(mass_points):
    '''
    Summarise all process of PCA and returns ratio of eiginvalues
    ratio ~ 0 --> points form a LINE
    ratio ~ 0.3 - 0.5 --> points form a SPOT
    '''

    cov_matrix = Cov_matrix(mass_points)
    v_lamb = EigenValues(cov_matrix)


    return min(v_lamb) / max(v_lamb)

def N_S(i,j):
    all_brights1[i][j]=0
    
    if all_brights1[i+1][j] == 1:
        all_brights1[i+1][j]=0
        N.append((i+1,j))

    if all_brights1[i+1][j] == 2:
        all_brights1[i+1][j]=0
        S.append((i+1,j))
        
    if all_brights1[i+1][j+1] == 1:
        all_brights1[i+1][j+1]=0
        N.append((i+1,j+1))

    if all_brights1[i+1][j+1] == 2:
        all_brights1[i+1][j+1]=0
        S.append((i+1,j+1))
        
    if all_brights1[i+1][j-1] == 1:
        all_brights1[i+1][j-1]=0
        N.append((i+1,j-1))
    
    if all_brights1[i+1][j-1] == 2:
        all_brights1[i+1][j-1]=0
        S.append((i+1,j-1))
        
    if all_brights1[i][j+1] == 1:
        all_brights1[i][j+1]=0
        N.append((i,j+1))
    
    if all_brights1[i][j+1] == 2:
        all_brights1[i][j+1]=0
        S.append((i,j+1))
            
    if all_brights1[i][j-1] == 1:
        all_brights1[i][j-1]=0
        N.append((i,j-1))
        
    if all_brights1[i][j-1] == 2:
        all_brights1[i][j-1]=0
        S.append((i,j-1))
         
    if all_brights1[i-1][j+1] == 1:
        all_brights1[i-1][j+1]=0
        N.append((i-1,j+1))
        
    if all_brights1[i-1][j+1] == 2:
        all_brights1[i-1][j+1]=0
        S.append((i-1,j+1))
         
    if all_brights1[i-1][j] == 1:
        all_brights1[i-1][j]=0
        N.append((i-1,j))
        
    if all_brights1[i-1][j] == 2:
        all_brights1[i-1][j]=0
        S.append((i-1,j))
        
    if all_brights1[i-1][j-1] == 1:
        all_brights1[i-1][j-1]=0
        N.append((i-1,j-1))
        
    if all_brights1[i-1][j-1] == 2:
        all_brights1[i-1][j-1]=0
        S.append((i-1,j-1))
def count_cloudsPCA(img):        
    const1 = 117
    const2 = 20
    groups_bright=[]
    sum_group_bright=[]
    all_brights = np.asarray(img, dtype='uint8')
    const_br1 = np.sum(all_brights ) / (img.size[0] * img.size[1]) + const1
    const_br2 = np.sum(all_brights ) / (img.size[0] * img.size[1]) + const2

    all_brights1 = all_brights.copy() # В all_brights1 будут 0, 1, 2

    all_brights1[all_brights<const_br2] = 0
    all_brights1[all_brights>const_br1] = 1 
    all_brights1[(all_brights<const_br1) & (all_brights>const_br2)] = 2
    all_C = []
    N=[]
    S=[]
    while 1 in all_brights1:
        C = []
        group_bright=[]
        i=np.where(all_brights1 == 1)[0][0]
        j=np.where(all_brights1[i] == 1)[0][0]
        group_bright.append(all_brights[i][j])
        C.append((i,j))
        N_S(i,j)
        while len(N)+len(S)>0:
            while len(N)==0:
                if len(S)>0:
                    N_S(S[0][0],S[0][1])
                    del S[0]
                if len(S)==0:
                    break
            if len(N)==0:
                break
            C.append(N[0])
            group_bright.append(all_brights[N[0][0]][N[0][1]])
            N_S(N[0][0],N[0][1])
            del N[0]
        groups_bright.append(sum(group_bright)/len(group_bright))
        sum_group_bright.append(sum(group_bright))
        if len(C)>=3:
            if PCA_analyse(C)>0.3:
                all_C.append("particle")
            else:
                all_C.append("treck")
        else:
            all_C.append("particle")
    return all_C.count('treck'), all_C.count('particle'),groups_bright,sum_group_bright

def get_groups(num_ar, pos, visited = [], coord_list = [], group_list = []):
    """
    Classify exposed pixels into groups using recursion.
    Parameters:
        num_ar - np.array of the coordinates of the exposed pixels
        pos - coordinates of the entry point
        visited - list of the visited pixels
        coord_list - list of the exposed pixels in one group
        group_list - list of the groups of the exposed pixels
    Return:
        group_list - list of the groups of the exposed pixels
    """

    if pos in visited:
        return group_list
    visited.append(pos)

    if pos not in coord_list:
        coord_list.append(pos)

    num_ar = np.delete(num_ar, num_ar.tolist().index(pos), 0)

    neighbors = [[pos[0] + 1, pos[1]],
                 [pos[0], pos[1] + 1],
                 [pos[0] - 1, pos[1]],
                 [pos[0], pos[1] - 1],
                 [pos[0] - 1, pos[1] + 1],
                 [pos[0] + 1, pos[1] - 1],
                 [pos[0] + 1, pos[1] + 1],
                 [pos[0] - 1, pos[1] - 1]]

    for neighbor in neighbors:
        if neighbor in num_ar.tolist():
            coord_list.append(neighbor)
            return get_groups(num_ar, neighbor, visited, coord_list, group_list)

    if num_ar.tolist() == []:
        return group_list

    group_list.append(coord_list)
    coord_list = []

    return get_groups(num_ar, num_ar[0].tolist(), visited, coord_list, group_list)

def count_groups(img, average):
    """
    Prepare the image for the get_groups function.
    Parameters:
        img - input image
        average - threshold for the binarization
    Return:
        number of the groups of the exposed pixels
    """

    width, height = img.size
    const_br = average
    br_list = np.asarray(img, dtype='uint8').T

    x = np.arange(0, width)
    y = np.arange(0, height)
    num_ar = np.array(np.meshgrid(x, y)).T
    num_ar = num_ar[br_list > const_br]
    if len(num_ar) == 0:
        group_list = []
    else:
        group_list = get_groups(num_ar, num_ar[0].tolist())

    return len(group_list)

save_image = bool(sys.argv[1])

while True:

    stream = BytesIO()
    with picamera.PiCamera() as camera:
        camera.start_preview()
        camera.resolution = (3280, 2464)
        camera.shutter_speed = 3000000
        camera.ISO = 800
        camera.capture(stream, format="jpeg")
        stream.seek(0)
        image = Image.open(stream).convert("L")
        if save_image:
            a = f"{str(datetime.datetime.now())}.png"
            image.save(a)
    const=17
    pixel_brightness = np.asarray(image, dtype='uint8')
    average = np.sum(pixel_brightness) / (image.size[0] * image.size[1]) + const
    count_clouds_trecks,count_clouds_partickle,groups_bright_PCA,sum_group_bright_PCA=count_cloudsPCA(image)
    if is_overexposed(image):
    	with open("20230719.csv", "a") as file:
        	file.write(str(datetime.datetime.now()) + ";" +
        	           str(count_clouds_trecks)+';'+
        	           str(count_clouds_partickle)+';'+
                           str(groups_bright_PCA)+';'+
                           str(sum_group_bright_PCA)+';'+
                   	   str(count_groups(image,average))+ "\n")
