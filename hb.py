import numpy as np
import cv2 as cv

import sys 
import getopt 

argv = sys.argv[1:] 

try: 
    opts, args = getopt.getopt(argv, "i:p:") 
    
except: 
    print("Error") 

for opt, arg in opts: 
    if opt in ['-i']: 
        img = arg 
    elif opt in ['-p']:
        peso = int(arg)

def openImg(filename):
    imagem = cv.imread(filename, 0)
    if imagem is None:
        print('Imagem inválida')
        sys.exit()
        return None
    else:
        print('Imagem carregada')
        return imagem


def espacial(imagem):
    
    borrada=cv.blur(imagem, (10,10))
    gmascara=cv.subtract(imagem, borrada)
    
    return gmascara, borrada
    

def frequencia(imagem):

    #Compute the 2-dimensional discrete Fourier Transform
    fo = np.fft.fft2(imagem)
    i, j = imagem.shape
    ci, cj = int(i/2), int(j/2)
    gmascara = np.zeros((i, j), np.uint8)
    x,y = np.ogrid[:i, :j] #return ndarrays with only one dimension not equal to 1
    R=300
    meio=[ci, cj]
    aream = (x - meio[0]) ** 2 + (y - meio[1]) ** 2 <= R*R
    gmascara[aream] =  1
    gmascara = np.fft.fft2(gmascara)
    imagem2=np.multiply(fo, gmascara)
    imagem3=np.fft.ifft2(imagem2)
    imagem4=np.abs(imagem3)
    res=np.array(imagem4, dtype=np.uint8)
    mask = cv.subtract(imagem, res)

    return mask



imagem = openImg(img)
#se k > 1 teremos um high-boost
k = peso
masc, borrada = espacial(imagem)
resEspacial=cv.add(imagem, k*masc)

mask = frequencia(imagem)
resFrequencia = cv.add(imagem, k*mask)

cv.imwrite('resultadoEspacial.jpg', resEspacial)
cv.imwrite('borrada.jpg', borrada)
cv.imwrite('resultadoFrequencia.jpg', resFrequencia)
