```python
#项目思路
#1、先标准化导入函数库，一行代码，pd.read_csv('albums.csv')直接进行数据清洗
#2、再根据需求进行数据分类统计
#3、使用matplib进行画图

以下是参考资料
"""前两个任务是普通柱状图，我们按所给资料中的代码进行了调整

# 按销售额从大到小排序，让柱状图更容易读。
sorted_sales = category_sales.sort_values(ascending=False)
# 创建柱状图画布。
fig, ax = plt.subplots(figsize=(8, 4))
# ax.bar(x, height, ...) 画竖向柱状图。
# 第 1 个位置参数 x 是类别位置或类别名称。
# 第 2 个位置参数 height 是柱子的高度，也就是要比较的数值。
# color 常用颜色名、十六进制颜色或 'tab:blue' 这类内置色。
bars = ax.bar(sorted_sales.index, sorted_sales.values, color='tab:blue')
# 设置标题和坐标轴。
ax.set_title('柱状图：不同类别销售额')
ax.set_xlabel('类别')
ax.set_ylabel('销售额')
# bar_label 给每根柱子加数值标签。
# padding=3 表示标签离柱子顶部有 3 个点的距离。
ax.bar_label(bars, padding=3)
# 设置 y 轴上限，给顶部标签留空间。
ax.set_ylim(0, sorted_sales.max() * 1.18)
# 显示图形。
plt.tight_layout()
plt.show()



"""任务三
看到的时候想到了使用百分比柱状图，而且刚好跟材料展示结果不谋而和，但是经过考量，未找到合适参考代码，于是通过折线加柱状图的形式融合，但整体还是有一定难度
因为加上了双轴图
# 创建主坐标轴。
fig, ax1 = plt.subplots(figsize=(10, 4))
# ax1 画销售额。
line_sales = ax1.plot(df['date'], df['sales'], color='tab:blue', label='销售额', linewidth=1.8)
# 设置左侧 y 轴。
ax1.set_ylabel('销售额', color='tab:blue')
ax1.tick_params(axis='y', labelcolor='tab:blue')
# ax.twinx() 创建共享 x 轴的新 y 轴。
# twinx 没有常用位置参数。
# 适合两个指标共用时间轴、但 y 轴单位不同的情况。
ax2 = ax1.twinx()
# ax2 画温度。
# 温度和销售额单位不同，所以放到右侧 y 轴。
line_temp = ax2.plot(df['date'], df['temperature'], color='tab:orange', label='温度', linewidth=1.8)
# 设置右侧 y 轴。
ax2.set_ylabel('温度', color='tab:orange')
ax2.tick_params(axis='y', labelcolor='tab:orange')
# 设置标题和 x 轴。
ax1.set_title('双轴图：销售额与温度')
ax1.set_xlabel('日期')
ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
# 合并两个坐标轴的图例。
lines = line_sales + line_temp
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc='upper left')
# 主轴加网格。
ax1.grid(alpha=0.3)
fig.autofmt_xdate()
plt.tight_layout()
plt.show()
"""

"""任务四
是典型的多折线图
 创建 2 行 2 列网格。
# width_ratios 控制两列宽度比例。
# height_ratios 控制两行高度比例。
fig = plt.figure(figsize=(11, 7))
grid = fig.add_gridspec(2, 2, width_ratios=[2, 1], height_ratios=[1, 1])
# 左侧大图跨两行。
ax_main = fig.add_subplot(grid[:, 0])
# 左侧大图画销售趋势。
ax_main.plot(df['date'], df['sales'], color='tab:blue', label='销售额')
ax_main.plot(df['date'], df['sales_7d_mean'], color='tab:red', label='7 天均值')
ax_main.set_title('销售趋势')
ax_main.set_xlabel('日期')
ax_main.set_ylabel('销售额')
ax_main.legend()
ax_main.grid(alpha=0.3)
ax_main.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
# 自动调整布局。
fig.tight_layout()
plt.show()
"""
"""任务五
我们看数据之间的差距有点小，于是我们取了2.7到2.9的区间
是分组柱状图问题
# x 是月份位置，0、1、2、3。
x = np.arange(len(channel_df['月份']))
# width 是每根柱子的宽度。
# 三组柱子并排时，0.24 比较合适，不会互相重叠。
width = 0.24
# 创建画布。
fig, ax = plt.subplots(figsize=(9, 4.5))
# ax.bar(x, height, width=...) 中 x 是柱子中心位置，height 是柱子高度。
# width 是关键字参数，控制柱子宽度；分组柱状图常用 0.2 到 0.3。
# 线上柱子放在 x - width 的位置。
bars_online = ax.bar(x - width, channel_df['线上'], width=width, label='线上')
# 门店柱子放在 x 的位置。
bars_store = ax.bar(x, channel_df['门店'], width=width, label='门店')
# 团购柱子放在 x + width 的位置。
bars_group = ax.bar(x + width, channel_df['团购'], width=width, label='团购')
# 设置 x 轴刻度位置和文字。
ax.set_xticks(x)
ax.set_xticklabels(channel_df['月份'])
# 设置标题和坐标轴。
ax.set_title('分组柱状图：各渠道月销售额')
ax.set_xlabel('月份')
ax.set_ylabel('销售额')
# legend 显示渠道名称。
ax.legend()
# 给每组柱子加标签。
ax.bar_label(bars_online, padding=2)
ax.bar_label(bars_store, padding=2)
ax.bar_label(bars_group, padding=2)
# 设置 y 轴上限，给标签留空间。
ax.set_ylim(0, channel_df[['线上', '门店', '团购']].to_numpy().max() * 1.25)
# 显示图形。
plt.tight_layout()
plt.show()
"""
