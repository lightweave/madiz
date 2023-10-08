import json
from PIL import Image, ImageEnhance
import numpy as np
import time
from skimage.filters import threshold_multiotsu

from datetime import datetime

start_time = time.time()
# import numpy as np

def Mean(mass, ddof=0):
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
    cov_00 = Mean([(point[0] - M_0) ** 2 for point in mass_points], ddof=1)
    cov_11 = Mean([(point[1] - M_1) ** 2 for point in mass_points], ddof=1)

    cov_01 = Mean([(point[0] - M_0) * (point[1] - M_1) for point in mass_points], ddof=1)

    return [[cov_00, cov_01], [cov_01, cov_11]]


def EigenValues(matrix):
    '''
    Evaluates eigenvalues of 2D matrix
    '''

    D_sqrt = ((matrix[0][0] - matrix[1][1]) ** 2 + 4 * matrix[0][1] * matrix[1][0]) ** 0.5
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


const1 = 20
const2 = -0.35
img_with_trecks = Image.open("test_HQ_shutt_sharp_simp.png").convert("L") #сюда вставляем изображение с треками
img_without_trecks = Image.open("test_HQ_shutt_sharp.png").convert("L") #сюда вставляем изображение без треками
width, height = img_with_trecks.size
all_brights = np.array(img_with_trecks , dtype='uint8')

threshold = threshold_multiotsu(image=all_brights,classes=3)
const_br1 = threshold.max()
const_br2 = threshold.min()
                            
all_brights2=np.array(img_without_trecks , dtype='uint8')

all_brights[all_brights < const_br2] = 0
all_brights2[all_brights < const_br2] = 0

all_brights[(all_brights < const_br1) & (all_brights >= const_br2)] = 2
all_brights2[(all_brights < const_br1) & (all_brights >= const_br2)] = 2

all_brights[all_brights >= const_br1] = 1
all_brights2[all_brights >= const_br1] = 1



all_brights-=np.min(np.array([all_brights,all_brights2]),axis=0)
print(np.sum(all_brights[all_brights==1]))

#all_brights10 = np.subtract(all_brights, all_brights2)
#print(all_brights[0], all_brights2[0], all_brights10[0])
print(const_br1, const_br2)

all_brights1 = all_brights.copy()  # В all_brights1 будут 0, 1, 2
visited=np.zeros(all_brights1.shape)
queue=[]

print(all_brights1)
#input()
#all_brights1[all_brights < const_br2] = 0
#all_brights1[all_brights > const_br1] = 1
#all_brights1[(all_brights < const_br1) & (all_brights > const_br2)] = 2

all_C = []
mas_all_C=[]
for i in range(height):
    if (i*100%height==0):
        print(i/height*100)
    for j in range(width):
        C = []
        if (all_brights1[i][j]==1 and visited[i][j]==0):
            queue.append((i,j))
            visited[i][j]=1
            while (len(queue)>0):
                it,jt=queue.pop()
                for di in range(-1,2):
                    for dj in range(-1,2):
                        if (height>it+di and it+di>-1 and width>jt+dj and jt+dj>-1):
                            if (visited[it+di][jt+dj]==0 and all_brights1[it+di][jt+dj]>0):
                                visited[it+di][jt+dj]=1
                                queue.append((it+di,jt+dj))
                if (all_brights1[it][jt]==1):
                    C.append([it,jt])
            mas_all_C.append(C)
            if len(C) >= 3:
                if PCA_analyse(C) > 0.3:
                    all_C.append("particle")
                else:
                    all_C.append("treck")
            else:
                all_C.append("particle")
print("--- %s seconds ---" % (time.time() - start_time))
d = {
    "date": f"{datetime.now()}",
    "const_1": f"{const_br1}",
    "const_2": f"{const_br2}",
    "treck": f"{all_C.count('treck')}",
    "particle": f"{all_C.count('particle')}",
    "masive_all_brights_pixels": f"{mas_all_C}"
}
with open(f"{datetime.now().date()}.json", "w") as f:
    f.write(json.dumps(d))
f.close()
d1 = {
    "masive_all_brights_pixels": f"{mas_all_C}",
    "const_1": f"{const_br1}",
    "const_2": f"{const_br2}"
}
with open(f"{datetime.now().date()}(masive_all_brights_pixels).json", "w") as f:
    f.write(json.dumps(d1))
f.close()
#"""
print(f"количество треков:{all_C.count('treck')}")
print(f"количество частиц:{all_C.count('particle')}")
#"""
