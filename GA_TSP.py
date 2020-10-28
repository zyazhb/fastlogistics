import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


##### 计算距离

def Distanse(Cities):
    num = Cities.shape[0]  # 城市个数
    Dis = np.zeros(shape=(num, num))
    for i in range(num):
        for j in range(num):
            Dis[i, j] = ((Cities[i, 0] - Cities[j, 0]) ** 2 + (Cities[i, 1] - Cities[j, 1]) ** 2) ** 0.5
    return Dis


# ##### 种群初始化

def Initpop(Nind, num):
    Chrom = np.zeros(shape=(Nind, num))
    for i in range(Nind):
        ChromSort = np.array(range(num))
        Chrom[i, :] = np.random.permutation(ChromSort)

    return Chrom


# ##### 适应度函数

def PathLengh(Dis, Chrom):
    [row, col] = Chrom.shape
    # Objv = np.zeros(shape=(row,1))
    Objv = np.zeros(row)
    for i in range(row):
        for j in range(col - 1):
            Objv[i] += Dis[int(Chrom[i, j]), int(Chrom[i, j + 1])]
        Objv[i] += Dis[int(Chrom[i, col - 1]), int(Chrom[i, 0])]
    return 1 / Objv


##### 选择操作

def Select(Chrom, Objv, GGap):
    num1 = int(np.rint(Chrom.shape[0] * GGap))
    Objv_index = np.argsort(Objv, 0)
    newpop = np.zeros(shape=(num1, Chrom.shape[1]))
    for i in range(num1):
        newpop[i, :] = Chrom[Objv_index[-(i + 1)], :]
    return newpop


##### 交叉

def Recombin(SelCh, Pc):
    SelCh = SelCh.astype(np.int16)
    [row, col] = SelCh.shape
    Sel = np.array(range(row))
    Sel = np.random.permutation(Sel)
    Sel_index = Sel[:int(row * Pc)]
    flag = 0

    for t in Sel_index:
        Place = np.random.permutation(np.array(range(col)))
        Place1 = min(Place[0:2])
        Place2 = max(Place[0:2])

        a1 = SelCh[t, 0:Place1]
        a2 = SelCh[t, Place2:col]
        a0 = []
        for i in SelCh[t, Place1:Place2]:
            a0.append(i)

        b = []
        for i in SelCh[flag, :]:  ### 0->T
            b.append(i)

        re = []
        for i in b:
            if i not in a0:
                re.append(i)
        re1 = re[0:len(a1)]
        re2 = re[len(a1):len(re)]

        for i in range(len(a1)):
            a1[i] = re1[i]
        for j in range(len(a2)):
            a2[j] = re2[j]
        flag += 1
        if flag == 51:
            flag = 0
    return SelCh


# ##### 变异

def Mutate(SelCh, Pm):
    [row, col] = SelCh.shape
    for i in range(row):
        if np.random.rand(1, 1) < Pm:
            P = np.random.randint(col, size=(2, 1))
            SelCh[i, P[0]], SelCh[i, P[1]] = SelCh[i, P[1]], SelCh[i, P[0]]
    return SelCh


# ##### 插入新个体

def Insert(SelCh, GGap, Nind):
    Newpop = np.zeros(shape=(int(Nind * (1 - GGap)) + 1, SelCh.shape[1]))
    for i in range(int(Nind * (1 - GGap)) + 1):
        Newpop0 = np.array(range(SelCh.shape[1]))
        Newpop[i, :] = np.random.permutation(Newpop0)
    return np.concatenate([SelCh, Newpop], 0)


## mian

Cities = np.array(
    [[126.31227, 45.38355], [126.61686, 45.75567], [126.56279, 45.80825], [126.58796, 45.88899], [127.4035, 46.08536],
     [128.04392, 45.95038], [128.74607, 45.9901],
     [129.56859, 46.32489], [128.82707, 45.85253], [127.96027, 45.21102], [127.16746, 44.93191], [128.33162, 45.4519],
     [127.48586, 45.75864], [126.95717, 45.54774],
     [126.64932, 45.79201], [126.66837, 45.76021], [126.66287, 45.70847], [126.63768, 45.59799]])  # 城市坐标
Nind = 1000  # 种群大小
MaxGen = 100  # 最大迭代次数
Pc = 0.9  # 交叉概率
Pm = 0.1  # 变异概率
GGap = 0.9  # 选择概率
num = Cities.shape[0]  # 城市个数
Dis = Distanse(Cities)  # 计算距离

Objv_Best = np.zeros(MaxGen)
Gen_Best = np.zeros(shape=(MaxGen, num))

##初始化种群
Chrom = Initpop(Nind, num)

##迭代
for gen in range(MaxGen):
    ##计算适应度
    Objv = PathLengh(Dis, Chrom)
    Objv_Best[gen] = (max(Objv))
    Gen_Bests = Chrom[Objv == max(Objv), :]
    Gen_Best[gen, :] = Gen_Bests[0, :]

    ##选择
    SelCh = Select(Chrom, Objv, GGap)

    ##交叉
    SelCh = Recombin(SelCh, Pc)

    ##变异
    SelCh = Mutate(SelCh, Pm)

    ##插入新个体
    Chrom = Insert(SelCh, GGap, Nind)

#### 画图


plt.figure(1)
x = np.array(range(MaxGen))
BEST = Gen_Best[Objv_Best == max(Objv_Best), :]
for i in range(MaxGen - 1):
    Objv_Best[i + 1] = max(Objv_Best[i], Objv_Best[i + 1])
plt.plot(x, 1 / Objv_Best, 'b-.')

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.title(f' 最短路径为:{1/Objv_Best[-1]}')
plt.legend
# plt.show()
# plt.savefig('diedaigcheng.png',dpi = 500 ,bbox_inches = 'tight' ) #保存图片

print(f"最短路径为:{1 / Objv_Best[-1]}")

plt.figure(2)
X = []
Y = []
for i in range(num):
    X.append(Cities[int(BEST[0, i]), 0])
    Y.append(Cities[int(BEST[0, i]), 1])
X.append(Cities[int(BEST[0, 0]), 0])
Y.append(Cities[int(BEST[0, 0]), 1])
plt.plot(X, Y)
plt.scatter(Cities[:, 0], Cities[:, 1], color='m', marker='D', alpha=1)
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.title(f' 最短路径为:{1/Objv_Best[-1]}')
plt.legend

plt.show()