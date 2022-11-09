from math import exp, sqrt, pi
import matplotlib.pyplot as plt
import numpy as np
import tkinter, os, glob, csv, sys
from tkinter import messagebox
import tkinter.filedialog


def export_DB(dataPath=None, Freqency=None, Amplitude=None, header=None, savePath=None):
  DB = []
  for i in range(int(len(Freqency)/2)):
    DB.append([Freqency[i], Amplitude[i]])
  df = pandas.DataFrame(DB)
  df.to_excel(savePath + os.sep + dataPath + '.xlsx', index=False, header=header)

def FFT_body(np_FrictionCoefficient=None, dt=None, savePath=None, data_Path=None):
  N = len(np_FrictionCoefficient)
  F = np.fft.fft(np_FrictionCoefficient) # 変換結果
  freq = np.fft.fftfreq(N, d=dt) # 周波数
  Amp = np.abs(F/(N/2)) # 振幅
  fig, ax = plt.subplots()
  ax.plot(freq[1:int(N/2)], Amp[1:int(N/2)])
  ax.set_xlabel("Freqency [Hz]")
  ax.set_ylabel("Amplitude")
  ax.grid()
  fileName = savePath + os.sep + os.path.splitext(os.path.basename(data_Path))[0] + ".png"
  fig.savefig(fileName, bbox_inches="tight", pad_inches=0.05)  # Save the photo
  header = ['Freqency', 'Amplitude']
  if not os.path.exists(savePath + os.sep + 'data'):
    os.makedirs(savePath + os.sep + 'data')    #Make fold
  export_DB(dataPath=os.path.splitext(os.path.basename(data_Path))[0], Freqency=freq, Amplitude=Amp, header=header, savePath= savePath + os.sep + 'data')
  print("saved[" + fileName + "]")



target_Path = tkinter.filedialog.askdirectory(title="データの参照をフォルダを指定してください。", mustexist=True)
target_Path_csv = target_Path + os.sep + "*.csv"
target_Path_xlsx = target_Path + os.sep + "*.xlsx"
fileList_csv = glob.glob(target_Path_csv)
fileList_xlsx = glob.glob(target_Path_xlsx)
if (len(fileList_csv) != 0) and (len(fileList_xlsx) != 0):
  messagebox.showerror("error01", "選択したフォルダにデータがありません。システムを終了します。")
  sys.exit()
savePath = tkinter.filedialog.askdirectory(title="データの保存先を指定してください。", mustexist=True)
dt = float(input('サンプル間隔を入力してください。\n>>'))
type_macine = int(input('旧型なら0、新型なら1を入力してください。\n>>'))
if type_macine == 0:
  step = 20
else:
  step = 1

if len(fileList_csv) != 0:
    import csv
    for count_fL in range(len(fileList_csv)):     #count_fL = count_fileList
        print(str(count_fL+1) + "/" + str(len(fileList_csv)))

        DB_Outcome = []
        #DB取得
        data_Path = fileList_csv[count_fL]
        with open(data_Path, encoding="shift-jis") as f:
        #DB→計算用一次元配列に置き換え
            csvreader = csv.reader(f)
            DB = [row for row in csvreader] 
        SlidingTime = []
        FrictionCoefficient = []
        for i in range(len(DB)-step):
            SlidingTime.append(float(DB[i+step][0]))
            FrictionCoefficient.append(float(DB[i+step][2]))
        np_FrictionCoefficient = np.array(FrictionCoefficient)
        FFT_body(np_FrictionCoefficient=np_FrictionCoefficient, dt=dt, savePath=savePath, data_Path=data_Path)


if len(fileList_xlsx) != 0:
  import pandas
  for count_fL in range(len(fileList_xlsx)):     #count_fL = count_fileList
        print(str(count_fL+1) + "/" + str(len(fileList_xlsx)))

        #DB取得
        data_Path = fileList_xlsx[count_fL]
        DB = pandas.read_excel(data_Path, sheet_name = "Sheet1")

        #DB→計算用一次元配列に置き換え
        SlidingTime = []
        FrictionCoefficient = []
        for i in range(len(DB)-step):
            SlidingTime.append(DB.values[i+step][0])
            FrictionCoefficient.append(DB.values[i+step][2])
        np_FrictionCoefficient = np.array(FrictionCoefficient)
        FFT_body(np_FrictionCoefficient=np_FrictionCoefficient, dt=dt, savePath=savePath, data_Path=data_Path)



