from cProfile import label
import hashlib
from subprocess import run
import time
import key_Generate

def signing(size,data):
    p1 = run(['.\\ringsign.exe', str(size), '50051', '0', hashlib.md5(data).hexdigest()], capture_output=True,check=True)
    sign = str(p1.stdout)[7:-2].split(' ')
    sign = [int(i,16) for i in sign]
    return sign


def verifying(size,data, str_sign):
    arg = ['.\\ringsign.exe', str(size), '50051', '1', hashlib.md5(data).hexdigest()]
    for i in str_sign:
        arg.append(hex(int(i)))
    p2 = run(arg, capture_output=True,check=True)
    return bool(str(p2.stdout)[-2:-1])

timecount=[[0,0] for i in range(7)]

l = [10,100,200,300]
for j in range(10):
    for i in l:
        key_Generate.makejson(i)
        t1 = time.time()
        sign = signing(i,'hello'.encode())
        t2 = time.time()
        out = verifying(i,'hello'.encode(),sign)
        if out == False:
            raise Exception
        t3 = time.time()
        timecount[l.index(i)][0] += t2-t1
        timecount[l.index(i)][1] += t3-t2

import matplotlib.pyplot as plt
import matplotlib as mpl


# 设置绘图风格
plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False
x_data = l

# 设置图框的大小
fig = plt.figure(figsize=(10,10))

parameters = {'axes.labelsize': 25,
          'axes.titlesize': 25,
          'xtick.labelsize':25,
          'ytick.labelsize':25,
          'legend.fontsize':22}
plt.rcParams.update(parameters)

# 绘图
y_data = [timecount[i][0]/10 for i in range(4)]

plt.plot(x_data, # x轴数据
         y_data, # y轴数据
         linestyle = '-', # 折线类型
         linewidth = 3, # 折线宽度
         color = '#ff9999', # 折线颜色
         marker = 'o', # 点的形状
         markersize = 0, # 点的大小
         markeredgecolor='black', # 点的边框色
         markerfacecolor='#ff9999',# 点的填充色
         label='签名算法'
         )

y_data2 = [timecount[i][1]/10 for i in range(4)]
plt.plot(x_data, # x轴数据
         y_data2, # y轴数据
         linestyle = '-', # 折线类型
         linewidth = 3, # 折线宽度
         color = '#9999ff', # 折线颜色
         marker = 'o', # 点的形状
         markersize = 0, # 点的大小
         markeredgecolor='black', # 点的边框色
         markerfacecolor='#9999ff',# 点的填充色
         label='验证算法'
         ) #


# 添加标题和坐标轴标签
plt.title('时间开销',fontdict={'weight':'normal','size': 25},pad=25)
plt.xlabel('节点数量',fontdict={'weight':'normal','size': 25})
plt.ylabel('时间（秒）',fontdict={'weight':'normal','size': 25})

# 剔除图框上边界和右边界的刻度
plt.tick_params(top = 'off', right = 'off')
# 获取图的坐标信息
ax = plt.gca()
# 设置x轴显示多少个日期刻度
#xlocator = mpl.ticker.LinearLocator(10)
# 设置x轴每个刻度的间隔天数
xlocator = mpl.ticker.MultipleLocator(50)
ax.xaxis.set_major_locator(xlocator)
# 显示图例
plt.legend()
# 显示图形
plt.show()
plt.savefig("环签名开销.esp", dpi=600,format='eps')
