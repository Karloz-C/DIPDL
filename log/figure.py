# 导入模块
import matplotlib.pyplot as plt
import matplotlib as mpl

def get_data(datafrom):
    # 读取需要绘图的数据
    port = [50051, 50053, 50055, 50057]
    test_error = []
    filename = "C:/Users/Silence/Documents/Github/SPDL/log/4/"+datafrom+"/error/"+"Test_error_"
    with open(filename + "50051.txt", "r") as f:
        l = f.readlines()
        for j in l:
            test_error.append(float(j.strip("\n").split(" ")[1]))

    for i in port[1:]:
        filenametemp = filename + str(i) + ".txt"
        f = open(filenametemp, "r")
        l = f.readlines()
        count = 0
        for j in l:
            test_error[count] += float(j.strip("\n").split(" ")[1])
            count += 1
    for i in range(100):
        test_error[i] = test_error[i] / 5
    return test_error

# 设置绘图风格
plt.style.use('ggplot')
plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False
t004=get_data("10")
t04=get_data("04")
x_data = [i for i in range(1,101)]
# 设置图框的大小
fig = plt.figure(figsize=(10,6))
# 绘图
"""
plt.plot(x_data, # x轴数据
         t04, # y轴数据
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = '#ff9999', # 折线颜色
         marker = 'o', # 点的形状
         markersize = 1, # 点的大小
         markeredgecolor='black', # 点的边框色
         markerfacecolor='#ff9999',
         label='BS=100') # 点的填充色

plt.plot(x_data, # x轴数据
         t004, # y轴数据
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = '#99ff99', # 折线颜色
         marker = 'o', # 点的形状
         markersize = 2, # 点的大小
         markeredgecolor='black', # 点的边框色
         markerfacecolor='#99ff99',
         label='BS=10') # 点的填充色
"""
krum = get_data("krum")
DP = get_data("DP")
pure = get_data("pure")

x_data = [i for i in range(1,101)]
# 设置图框的大小
fig = plt.figure(figsize=(10,6))
# 绘图
plt.plot(x_data, # x轴数据
         pure, # y轴数据
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = '#ff9999', # 折线颜色
         marker = 'o', # 点的形状
         markersize = 1, # 点的大小
         markeredgecolor='black', # 点的边框色
         markerfacecolor='#ff9999',
         label='pure') # 点的填充色

plt.plot(x_data, # x轴数据
         DP, # y轴数据
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = '#99ff99', # 折线颜色
         marker = 'o', # 点的形状
         markersize = 2, # 点的大小
         markeredgecolor='black', # 点的边框色
         markerfacecolor='#99ff99',
         label='DP') # 点的填充色

plt.plot(x_data, # x轴数据
         krum, # y轴数据
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = 'steelblue', # 折线颜色
         marker = 'o', # 点的形状
         markersize = 2, # 点的大小
         markeredgecolor='black', # 点的边框色
         markerfacecolor='steelblue',
         label='krum') # 点的填充色

# 添加标题和坐标轴标签
plt.title('N=5')
plt.xlabel('round')
plt.ylabel('Test Error')

# 剔除图框上边界和右边界的刻度
plt.tick_params(top = 'off', right = 'off')

# 获取图的坐标信息
ax = plt.gca()

# 设置x轴显示多少个日期刻度
#xlocator = mpl.ticker.LinearLocator(10)
# 设置x轴每个刻度的间隔天数
xlocator = mpl.ticker.MultipleLocator(10)
ax.xaxis.set_major_locator(xlocator)

# 为了避免x轴日期刻度标签的重叠，设置x轴刻度自动展现，并且45度倾斜
fig.autofmt_xdate(rotation = 45)

# 显示图例
plt.legend()

# 显示图形
plt.show()