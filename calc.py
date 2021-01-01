import numpy as np
import copy
import matplotlib.pyplot as plt
import pandas as pd


#--------------------------------获取订单中的数据-------------------------#
data = pd.read_excel('./order.xlsx')
data = np.array(data)
data = data.tolist()

markets = np.zeros(shape=(len(data), 2))  # 商超位置
time_limit = np.zeros(shape=(len(data), 2), dtype=int)  # 时间窗
markets_huan = []  # 商超的环数
vk = []  # 货物的体积
mk = []  # 货物的质量

flag = 0
for i in range(len(data)):
    if np.isnan(data[i][1]) == False:
        markets[flag, 0] = data[i][1]
        markets[flag, 1] = data[i][2]
        markets_huan.append(data[i][3])
        time_limit[flag, 0] = int(str(data[i][7]).split(":")[0])
        time_limit[flag, 1] = int(str(data[i][8]).split(":")[0])
        flag += 1

    vk.append(data[i][5])
    mk.append(data[i][6])

for i in range(len(data)):
    if markets[i, 0] == 0:
        break

markets = markets[:i, :]
time_limit = time_limit[:i, :]

for i in range(time_limit.shape[0]):
    if time_limit[i, 0] == 0:
        time_limit[i, 1] = 24

del vk[0]
del mk[0]
vk = np.array(vk)
mk = np.array(mk)

#---------------------------计算两点之间的直线距离-----------------------------------#
D = np.zeros((markets.shape[0], markets.shape[0]))
for i in range(markets.shape[0]):
    for j in range(markets.shape[0]):
        D[i, j] = (markets[i, 0]-markets[j, 0])**2 + \
            (markets[i, 1]-markets[j, 1])**2


##-----------------------------定义初始值---------------------------------------##
Ve = [2, 3, 6, 10, 13, 15, 25]  # 车辆的额定体积
Me = [4, 6, 15, 17, 30, 40, 50]  # 车辆的额定载重
c1 = 30  # 单位投入成本
c2 = 1000  # 单位行驶成本
cv = 100  # 机会成本
cw = 100  # 机会成本
time_cost = 500  # 时间成本
av = np.zeros(vk.shape)
aw = np.zeros(vk.shape)
av[(mk/vk) > 3] = 1
aw = 1 - av  # 判断泡、重货
v = 0.2


##——————————————————————一个对应的关系————————————————————————————————————#
# 一1-2、二3、三4、四5-6、五7-10、六11、七12-14、八15-17、九18、十19-22、十一23-26、十二27-83、
# 十三84、十四85-87、十五88-89、十六90-91、十七92、十八93-150、十九151-153、二十154-155、二十一156-159
def map(list):
    path = []
    temp = 0
    for i in list:
        if i <= 1:
            k = 1
        elif i == 2:
            k = 2
        elif i == 3:
            k = 3
        elif i >= 4 and i <= 5:
            k = 4
        elif i >= 6 and i <= 9:
            k = 5
        elif i == 10:
            k = 6
        elif i >= 11 and i <= 13:
            k = 7
        elif i >= 14 and i <= 16:
            k = 8
        elif i == 17:
            k = 9
        elif i >= 18 and i <= 21:
            k = 10
        elif i >= 22 and i <= 25:
            k = 11
        elif i >= 26 and i <= 82:
            k = 12
        elif i == 83:
            k = 13
        elif i >= 84 and i <= 86:
            k = 14
        elif i >= 87 and i <= 88:
            k = 15
        elif i >= 89 and i <= 90:
            k = 16
        elif i == 91:
            k = 17
        elif i >= 92 and i <= 149:
            k = 18
        elif i >= 150 and i <= 152:
            k = 19
        elif i >= 153 and i <= 154:
            k = 20
        else:
            k = 21

        if temp == 0:
            path.append(k)
            temp += 1
        else:
            if path[temp-1] != k:
                path.append(k)
                temp += 1

    return path


def map2(markets_list):
    [row, col] = markets_list.shape
    pops = []
    for i in range(row):
        pop = []
        for markets_num in markets_list[i, :]:
            if markets_num == 1:
                v = range(0, 2)
            elif markets_num == 2:
                v = range(2, 3)
            elif markets_num == 3:
                v = range(3, 4)
            elif markets_num == 4:
                v = range(4, 6)
            elif markets_num == 5:
                v = range(6, 10)
            elif markets_num == 6:
                v = range(10, 11)
            elif markets_num == 7:
                v = range(11, 14)
            elif markets_num == 8:
                v = range(14, 17)
            elif markets_num == 9:
                v = range(17, 18)
            elif markets_num == 10:
                v = range(18, 22)
            elif markets_num == 11:
                v = range(22, 25)
            elif markets_num == 12:
                v = range(25, 83)
            elif markets_num == 13:
                v = range(83, 84)
            elif markets_num == 14:
                v = range(84, 87)
            elif markets_num == 15:
                v = range(87, 89)
            elif markets_num == 16:
                v = range(89, 91)
            elif markets_num == 17:
                v = range(91, 92)
            elif markets_num == 18:
                v = range(92, 150)
            elif markets_num == 19:
                v = range(150, 153)
            elif markets_num == 20:
                v = range(153, 155)
            else:
                v = range(155, 159)

            pop.extend(v)
        pops.append(pop)

    return np.array(pops)


def vehicle_limit(chexing, huan):
    flag = 1
    if chexing >= 4 and huan <= 4:
        flag = 0
    if chexing == 6 and huan <= 5:
        flag = 0
    return flag


#-----------------------------编码------------------------------------#
def encode(pop, vk, mk):

    [row, col] = pop.shape
    newpop = []

    for i in range(row):
        pop0 = []
        V_count = 0
        M_count = 0
        pop0.append(1000)
        m = np.random.randint(0, len(Ve))
        pop0.append(m)

        pop_flag = []  # 用来判断

        for it in pop[i, :]:
            pop0.append(it)
            pop_flag.append(it)
            V_count += vk[it]
            M_count += mk[it]
            Ve_lim = vehicle_limit(m, markets_huan[map(pop_flag)[-1]])
            if V_count > Ve[m] or M_count > Me[m] or (m <= 3 and len(map(pop_flag))) == 8 or Ve_lim == 0:
                # print(len(map(pop_flag)))
                pop_flag = []
                pop0.pop()  # 删掉最后一个元素然后插入起点和车型
                pop0.append(1000)
                m = np.random.randint(0, len(Ve))
                pop0.append(m)
                pop0.append(it)
                V_count = 0
                M_count = 0
        newpop.append(pop0)
    return newpop


#----------------------------解码------------------------------------------#
def decode(pop):
    # print(pop)
    Nind = len(pop)
    conss = []
    for j in range(Nind):
        con = []
        cons = []
        con.append(1000)
        for i in range(1, len(pop[j])):
            if pop[j][i] != 1000 and i != (len(pop[j])-1):
                con.append(pop[j][i])
            else:
                if (i == (len(pop[j])-1)):
                    con.append(pop[j][i])
                    con.append(1000)
                    if len(con) != 3:
                        cons.append(con)
                    con = []
                    # con.append(1000)
                else:
                    con.append(1000)
                    if len(con) != 3:
                        cons.append(con)
                    con = []
                    con.append(1000)
        conss.append(cons)

    return conss


#---------------------------初始种群--------------------------------------#
def IntPop(pop_L, Nind):
    pop = np.zeros(shape=(Nind, pop_L), dtype=int)
    for i in range(Nind):
        pop[i, :] = np.array([np.random.permutation(range(pop_L))])
    return pop


#-----------------------------适应度函数-------------------------------#
def Objv(pop0, c1, c2, cv, cw, D, Ve, Me, av, aw, vk, mk, v, time_limit, time_cost):
    pop = copy.deepcopy(pop0)
    Nind = len(pop)
    fit_value = []
    for i in range(Nind):
        che_num = len(pop[i])
        che_xing = []
        Z1 = c1*che_num  # 折旧成本

        Z4 = 0
        # 计算行驶成本&时间成本
        path_D = 0
        for j in range(che_num):
            che_xing.append(pop[i][j][1])
            del pop[i][j][1]
            del pop[i][j][0]
            del pop[i][j][-1]
            path = map(pop[i][j])
            path_num = len(path)
            D_count = 0
            if path_num != 0:
                D_count = D[0, path[0]-1]
                for k in range(path_num-1):
                    D_count += D[path[k]-1, path[k+1]-1]
                D_count += D[path[-1]-1, 0]
            path_D = D_count

            # 时间成本
            path.insert(0, 0)
            path.append(0)
            path_num = len(path)
            market_time = 8
            for k in range(path_num-1):
                if k != 0:
                    market_time += (D[k, k+1]/v + 1.5)
                    if market_time < time_limit[path[k]][0] or market_time > time_limit[path[k]][1]:
                        Z4 += time_cost

        Z2 = c2*path_D

        # print(che_xing)
        # 计算机会成本
        Ve_count = 0
        Me_count = 0
        for che in che_xing:
            Ve_count += Ve[che]
            Me_count += Me[che]
        vk_count = 0
        mk_count = 0
        v_num = av.shape[0]
        for k in range(v_num):
            if av[k] == 1:
                vk_count += vk[k]
            else:
                mk_count += mk[k]
        # print(vk_count)
        # print(mk_count)
        Z31 = cv*(1-vk_count/Ve_count)
        Z32 = cw*(1-mk_count/Me_count)

        # print(Z1+Z2+Z31+Z32)
        fit_value.append(Z1+Z2+Z31+Z32+Z4)

    return fit_value


#-----------------------------------选择操作---------------------------#
def Select(Chrom, Objv, GGap):
    num1 = int(np.rint(Chrom.shape[0] * GGap))
    Objv_index = np.argsort(Objv, 0)
    newpop = np.zeros(shape=(num1, Chrom.shape[1]))
    for i in range(num1):
        newpop[i, :] = Chrom[Objv_index[-(i + 1)], :]
    return newpop


#--------------------------------交叉-----------------------------------#
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
        for i in SelCh[flag, :]:  # 0->T
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


#-----------------------------------变异---------------------------#
def Mutate(SelCh, Pm):
    [row, col] = SelCh.shape
    for i in range(row):
        if np.random.rand(1, 1) < Pm:
            P = np.random.randint(col, size=(2, 1))
            SelCh[i, P[0]], SelCh[i, P[1]] = SelCh[i, P[1]], SelCh[i, P[0]]
    return SelCh


#---------------------------插入新个体-----------------------------#
def Insert(SelCh, GGap, Nind):
    Newpop = np.zeros(shape=(int(Nind * (1 - GGap)) + 1, SelCh.shape[1]))
    for i in range(int(Nind * (1 - GGap)) + 1):
        Newpop0 = np.array(range(SelCh.shape[1]))+1
        Newpop[i, :] = np.random.permutation(Newpop0)
    return np.concatenate([SelCh, Newpop], 0)


######--------------------迭代的参数-------------------------------#####
pop_L = vk.shape[0]
markets_num = markets.shape[0]
Nind = 50  # 种群大小
MaxGen = 500  # 最大迭代次数
Pc = 0.9  # 交叉概率
Pm = 0.1  # 变异概率
GGap = 0.9  # 选择概率
pop0 = IntPop(markets_num-1, Nind)+1
Min_fit = []
Mean_fit = []
path = []


# 第13和19个商场的货物进行交叉
pop13 = np.zeros(shape=(Nind, 56), dtype=int)
for i in range(Nind):
    pop13[i, :] = np.array([np.random.permutation(range(26, 82))])


pop19 = np.zeros(shape=(Nind, 57), dtype=int)
for i in range(Nind):
    pop19[i, :] = np.array([np.random.permutation(range(92, 149))])


#-----------------------------迭代训练-----------------------------------#
plt.ion()
for iter in range(MaxGen):

    pop_markets = pop0

    pop = map2(pop_markets)

    # 将交叉完的13，19顺序插入
    for i in range(Nind):
        In13 = np.argwhere(pop[i, :] == 26)[0][0]
        In19 = np.argwhere(pop[i, :] == 92)[0][0]
        # print(In19)
        pop[i, In13:In13+56] = np.array(pop13[i, :])
        pop[i, In19:In19+57] = np.array(pop19[i, :])
    ####################################

    en = encode(pop, vk, mk)
    de = decode(en)
    fit_value = Objv(de, c1, c2, cv, cw, D, Ve, Me, av,
                     aw, vk, mk, v, time_limit, time_cost)

    fit_value_min = np.min(fit_value)
    Mean_fit.append(np.min(fit_value))

    if (iter != 0) and (fit_value_min > Min_fit[iter-1]):
        Min_fit.append(Min_fit[iter-1])
    else:
        Min_fit.append(fit_value_min)
        for i in range(len(fit_value)):
            if fit_value[i] == fit_value_min:
                path.append(de[i])
                break

    pop_markets = Select(pop_markets, fit_value, GGap)
    pop_markets = Recombin(pop_markets, Pc)

    # 对13和19号商超的商品进行交叉
    pop13 = Recombin(pop13, Pc)
    pop19 = Recombin(pop19, Pc)
    ###########################
    pop_markets = Mutate(pop_markets, Pm)
    pop_markets = Insert(pop_markets, GGap, Nind)
    pop0 = np.array(pop_markets, dtype=int)

    plt.clf()
    plt.figure(1)
    plt.title('cost')
    plt.plot(Min_fit, color='red', linestyle='-', linewidth=1)
    plt.pause(0.1)
    plt.xlabel("gen")
    plt.ylabel('cost')


#---------------输出结果------------------------#
def main():
    Best_path = path[-1]
    lines = []
    print(f"一共需要{len(Best_path)}辆车")
    for i in range(len(Best_path)):
        print(
            f"第{Best_path[i][1]}种类型的车,路径为0->{map(Best_path[i][2:-1])}->0,运输的商品为{Best_path[i][2:-1]}")
        lines.append(map(Best_path[i][2:-1]))
    print(f"最低成本为{Min_fit[-1]}")
    print(Best_path, "\n\n\n", lines)
    return Best_path, lines

    #--------------------------------画图------------------------------#
    colors = ['lightcoral', 'black', 'gray', 'lime', 'pink', 'gold',
              'red', 'cadetblue', 'navy', 'brown', 'deeppink', 'green']
    linestyles = ['-', '--', '-.', ':', '-', '--', '-.',
                  ':', '-', '--', '-.', ':', '-', '--', '-.', ':']

    for i in range(len(Best_path)):
        plt.figure(i+2)
        plt.scatter(markets[:, 0], markets[:, 1], s=30, marker='o', c='b')
        plt.scatter(markets[0, 0], markets[0, 1], s=60, marker='o', c='r')
        plt.figure(i+2)
        Best_path_che = map(Best_path[i][2:-1])
        for j in range(len(Best_path_che)-1):
            plt.plot([markets[Best_path_che[j], 0], markets[Best_path_che[j+1], 0]], [markets[Best_path_che[j],
                                                                                              1], markets[Best_path_che[j+1], 1]], color='k', linestyle='-.', linewidth='1')
        plt.plot([markets[0, 0], markets[Best_path_che[0], 0]], [
                 markets[0, 1], markets[Best_path_che[0], 1]], color='k', linestyle='-.', linewidth='1')
        plt.plot([markets[0, 0], markets[Best_path_che[-1], 0]], [markets[0, 1],
                                                                  markets[Best_path_che[-1], 1]], color='k', linestyle='-.', linewidth='1')

    plt.figure(len(Best_path)+3)

    plt.plot(Mean_fit, color='red', linestyle='-', linewidth=1)

    plt.show()
    plt.pause(0)


print(main())
