import cv2
import matplotlib.pyplot as plt
import numpy as np
from math import log10, sqrt

"""def cv2_main():
  foto=cv2.imread("./1.jpg",0)
  hist_es_foto=cv2.equalizeHist(foto)
  yanyana=np.hstack((foto,hist_es_foto))

  plt.imshow(yanyana,cmap="gray")
  plt.show()


def main():
   pass
if __name__=="__main__":
    cv2_main()"""

def fotografin_histogramini_olustur(foto,L): #L 8 bitlik fotoğraf için 256
    #numpy histpgram fonksiyonu fotonun histogramını döndürür
    histogram,bind=np.histogram(foto,bins=L,range=(0,L))#0 ile 256 arasındaki her bir pikselin kaç tane oldupunu döndürür
    #print(histogram)
    return histogram



def normallestirilmis_histogram_olustur(foto,L):
    histogram=fotografin_histogramini_olustur(foto,L)
    return histogram/foto.size



def kumulatif_dagilim_olustur(p_r_r):
    return np.cumsum(p_r_r)#her bir k değeri için prr yi verir toplaya toplaya gider
   

def histogram_esitleme(foto,L):
    p_r_r=normallestirilmis_histogram_olustur(foto,L)
    kumulatif_dagilim=kumulatif_dagilim_olustur(p_r_r)
    donusum_fonksiyonu=(L-1)*kumulatif_dagilim
    shape=foto.shape
    ravel=foto.ravel()#mesela bu foto 800x600 dü fotoyu tek boyut yapar 480.000 gibi
    hist_es_foto=np.zeros_like(ravel)#orjinal fotoyu değiştirmeyelim kopyasını oluşturduk,sıfırlardan oluşturduk ki içini dolduralım rahat bir şekilde
    

    for i,pixel in enumerate(ravel):#fotonun içindeki piksel değelrrini dönüşüm fonksiyonundaki değerler ile değiştirmek
        hist_es_foto[i]=donusum_fonksiyonu[pixel]
    return hist_es_foto.reshape(shape).astype(np.uint8)
    
    #ravelin içindeki 0 piksel değelerini dönüşüm fonk içindeki değerlerle doldurduk,
    # dönüşüm fomksiyonu içindeki her bir eleman k nın değerini veriyor,k piksel değeridir
    #mesela ravel arrayinin içindeki ilk pikselin değeri 50 
    #yani mesela bu ravel footonun içindeki  ilk piksel değeri 50 ise eğer dönüşüm fonksiyonundaki 50.indeksteki değeri döndürelim ki 
    # k nın 50 olan değerine eşit olsun ve burda bu piksel değerini bu değerle değiştireyim
    #döngüde ravelin içindeki piksel değerlerine ve  indekslerine (i)teker teker eriştik


#psnr=20log10(L-1/RMSE) rmse kök ortalama kare hatası
  
def PSNR(original, enchanment2):#bozuk foto ile kaliteli foto arasındaki oran kaliteyi ölçer ,ne kadar büyükse o kadar iyi
    mse = np.mean((original - enchanment2) ** 2)#mse girdi ile çıktı arasındaki hatanın karesinin ortalaması
    if(mse == 0): 
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr
  


def main():
    L=256
    foto=cv2.imread("./6.tif",0)
    
    hist_es_foto=histogram_esitleme(foto,L)
    yanyana=np.hstack((foto,hist_es_foto))
    #cv2.imwrite("6ench.jpg",hist_es_foto)
    original = cv2.imread("6.tif")
    enchanment2= cv2.imread("6ench.jpg", 1)
    value = PSNR(original, enchanment2)
    print(f"PSNR value is {value} dB")

    histr = cv2.calcHist([foto],[0],None,[256],[0,256])
    plt.plot(histr)
    plt.show()
    
    histr2 = cv2.calcHist([hist_es_foto],[0],None,[256],[0,256])
    plt.plot(histr2)
    plt.show()

    plt.imshow(yanyana,cmap="gray")
    plt.show()
 
       

if __name__=="__main__":
    main()