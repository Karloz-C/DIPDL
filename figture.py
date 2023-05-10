import matplotlib.pyplot as plt
import matplotlib as mpl

def get_data(datafrom):
    # 读取需要绘图的数据
    data = []
    filename = "G:/Program/SPDL/"+datafrom+".txt"
    with open(filename, "r") as f:
        l = f.readlines()
        for j in l:
            data.append(float(j.strip("\n").split(" ")[1]))
    return data

# 设置绘图风格
plt.style.use('ggplot')
plt.rcParams['font.sans-serif'] = 'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False

time_coat = get_data("t_sig")

x_data = [10,20,40,60,100,200]
# 设置图框的大小
fig = plt.figure(figsize=(10,6))
# 绘图
plt.plot(x_data, # x轴数据
         time_coat, # y轴数据
         linestyle = '-', # 折线类型
         linewidth = 2, # 折线宽度
         color = '#ff9999', # 折线颜色
         marker = 'o', # 点的形状
         markersize = 1, # 点的大小
         markeredgecolor='black', # 点的边框色
         markerfacecolor='#ff9999',
         label='krum') # 点的填充色
        
plt.tick_params(labelsize=13)
# 添加标题和坐标轴标签
plt.title('签名生成',fontdict={'weight':'bold','size': 20})
plt.xlabel('节点数目',fontdict={'weight': 'bold', 'size': 15})
plt.ylabel('时间：毫秒',fontdict={'weight': 'bold', 'size': 15})

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