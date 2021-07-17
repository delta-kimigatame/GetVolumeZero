import os.path
from scipy.io.wavfile import read
import numpy as np
import array
import wave

WAV_FILE_PATH=os.path.join("data","sample.wav")
START_TIME=1600
END_TIME=1800
N=512
STEP=32
WINDOW="hanning"
VOLUME_THRESHOLD=50
DIF_THRESHOLD=3

class GVZ:
    def __init__(self,wavfile,start_time,end_time,n=512,step=32,window="hanning",volume_threshold=VOLUME_THRESHOLD,dif_threshold=DIF_THRESHOLD):
        self.rate,data=read(wavfile)
        self.start_frame=int(self.rate*start_time/1000)
        self.end_frame=int(self.rate*end_time/1000)
        self.data=data[self.start_frame:self.end_frame]
        self.n=n
        self.step=step
        self.volume_threshold=volume_threshold
        self.dif_threshold=dif_threshold
        if(window=="hamming"):
            self.window=np.hamming(n)
        elif(window=="hanning"):
            self.window=np.hanning(n)
        else:
            self.window=np.hanning(n)

    def __GetSumOfSquare(self,data):
        sum_of_square=0
        for i in range(N):
            sum_of_square+=((data[i]*self.window[i])**2)**0.5
        return sum_of_square/N

    def __GetSumOfSquares(self):
        self.sum_of_squares=[]
        self.dif_sum_of_squares=[]
        length=int((len(self.data)-self.n)/self.step)
        for i in range(length):
            offset=i*self.step
            self.sum_of_squares.append(self.__GetSumOfSquare(self.data[offset:self.n+offset]))
            if(len(self.sum_of_squares)>=2):
                self.dif_sum_of_squares.append(self.sum_of_squares[-1]-self.sum_of_squares[-2])
            else:
                self.dif_sum_of_squares.append(0)

    def Get(self):
        self.__GetSumOfSquares()
        value=-1
        for i in range(len(self.sum_of_squares)):
            if(self.sum_of_squares[i]<self.volume_threshold and abs(self.dif_sum_of_squares[i])<self.dif_threshold):
                value=i
                break
        value=value*self.step+self.start_frame
        value=value*1000/self.rate
        return(value)

if __name__=="__main__":
    gvz=GVZ(WAV_FILE_PATH,START_TIME,END_TIME)
    print(gvz.Get())