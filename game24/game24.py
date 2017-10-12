#!/usr/bin/env python3
# coding=utf-8

list4 = [1, 2, 3, 4]


def getTwoInList(list):
    result = set()
    for i in range(len(list)):
        for j in range(len(list)):
            if (i != j):
                result.add(str(i) + "," + str(j))
                # print(str(i) + "," + str(j))
    return result


def math24(a, b, c, d):
    par = []
    par.append(a)
    par.append(b)
    par.append(c)
    par.append(d)
    go(par)


def go(par, vStr=""):
    if (len(par) == 1):
        # print(par)
        # print(vStr)
        if (par[0] == 24):
            print(par)
            print("bingo:" + "\n" + vStr)
        return
    # 取2个
    couple = getTwoInList(par)

    # 做加法 少一个
    for t in couple:
        a = int(t.split(",")[0])
        b = int(t.split(",")[1])
        temp = par[a] + par[b]
        result = par.copy()
        result.remove(par[a])
        result.remove(par[b])
        result.append(temp)
        tStr = vStr + str(par[a]) + "+" + str(par[b]) + "\n"
        # 递归调用
        go(result, tStr)

    # 做减法
    for t in couple:
        a = int(t.split(",")[0])
        b = int(t.split(",")[1])
        temp = par[a] - par[b]
        result = par.copy()
        result.remove(par[a])
        result.remove(par[b])
        result.append(temp)
        tStr = vStr + str(par[a]) + "-" + str(par[b]) + "\n"
        # 递归调用
        go(result, tStr)

    # 做乘法
    for t in couple:
        a = int(t.split(",")[0])
        b = int(t.split(",")[1])
        temp = par[a] * par[b]
        result = par.copy()
        result.remove(par[a])
        result.remove(par[b])
        result.append(temp)
        # 递归调用
        tStr = vStr + str(par[a]) + "*" + str(par[b]) + "\n"
        go(result, tStr)

    # 做除法
    for t in couple:
        a = int(t.split(",")[0])
        b = int(t.split(",")[1])
        try:
            temp = par[a] / par[b]
        except:
            return
        result = par.copy()
        result.remove(par[a])
        result.remove(par[b])
        result.append(temp)
        va = par[a]
        vb = par[b]
        tStr = vStr + str(par[a]) + "/" + str(par[b]) + "\n"
        # if (par[a]== 1 and par[b] == 5):
        #     print(tStr)
        #     print(temp)
        # 递归调用
        go(result, tStr)


if __name__ == '__main__':
    math24(10, 10, 4, 4)
