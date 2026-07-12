import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('albums.csv')

print("=== 数据集基本信息 ===")
print(df.info())

print("\n=== 数据集描述性统计 ===")
print(df.describe())

print("\n=== 各列缺失值统计 ===")
print(df.isnull().sum())

print("\n=== genre类型分布 ===")
print(df['genre'].value_counts())

print("\n=== 年份范围 ===")
print(f"最早年份: {df['year_of_pub'].min()}")
print(f"最晚年份: {df['year_of_pub'].max()}")

# 1. 使用 df['genre'].value_counts() 统计数量
# 2. 使用 sns.barplot() 绘制柱状图
# 3. 保存为 task1_genre_counts.png

#Task1
print('\n===任务一：统计各类专辑数量===')
genre_counts = df['genre'].value_counts()
print('\n各类专辑数量：')
print(genre_counts)

#创建画布
plt.figure(figsize=(15,8))
#柱状图
sns.barplot(x=genre_counts.index,y=genre_counts.values)
plt.title('各类型专辑数量分布')
plt.xlabel('专辑类型')
plt.ylabel('专辑数量')
plt.xticks(rotation=90)
plt.tight_layout()
#自动调整布局，防止标签被裁切

#保存-关闭
plt.savefig('task1_genre_counts.png',dpi = 100)
plt.close()
print('图表已保存为：task1_genre_counts.png')

#Task2
print('\n===任务二：统计各类型专辑的销量总数===')
genre_sales = df.groupby('genre')['num_of_sales'].sum()
genre_sales = genre_sales.sort_values(ascending=False)
print('\n各类型专辑销量总数：')
print(genre_sales)

#柱状图
plt.figure(figsize=(15,8))
sns.barplot(x=genre_sales.index,y=genre_sales.values)
plt.title('各类型专辑销量总数')
plt.xlabel('专辑类型')
plt.ylabel('销量总数')
plt.xticks(rotation=90)
plt.tight_layout()

#保存-关闭
plt.savefig('task2_genre_sales.png',dpi = 100)
plt.close()
print('图表已保存为：task2_genre_sales.png')

#Task3
print('\n===任务三：统计近20年每年发行的专辑数量和单曲数量===')
year_stats = df.groupby('year_of_pub').agg(album_count=('id','count'),total_tracks=('num_of_tracks','sum')).sort_index()
print(year_stats)

#双轴图表
fig,ax1 = plt.subplots(figsize=(15,8))
color1 = 'tab:blue'
ax1.set_xlabel('年份')
ax1.set_ylabel('专辑数量',color=color1)
ax1.bar(year_stats.index,year_stats['album_count'],color=color1,alpha=0.6)
ax1.tick_params(axis='y',labelcolor=color1)

ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel('单曲数量',color=color2)
ax2.plot(year_stats.index,year_stats['total_tracks'],color=color2,marker='o')
ax2.tick_params(axis='y',labelcolor=color2)

#添加标题例
plt.title('近20年每年发行的专辑数量和单曲数量')
plt.tight_layout()
plt.savefig('task3_year_stats.png',dpi=100)
plt.close()
print('图表已保存为：task3_year_stats.png')

#Task4
print('\n===任务四：分析总销量前五的专辑类型的各年份销量===')
top5_genres = df.groupby('genre')['num_of_sales'].sum().sort_values(ascending=False).head(5)
print('\n总销量前五的专辑类型：')
print(top5_genres)

#提取前五类型名称列表
top5_genres_names = top5_genres.index.tolist()
#筛选前五类型专辑
filtered_df = df[df['genre'].isin(top5_genres_names)]
yearly_sales = filtered_df.groupby(['genre','year_of_pub'])["num_of_sales"].sum().unstack()#unstack()将多索引转换为列，方便绘图
print('\n前五专辑类型的各年份销量：')
print(yearly_sales)

#绘制折线图
plt.figure(figsize=(15,8))
for genre in top5_genres_names:
    plt.plot(yearly_sales.columns,yearly_sales.loc[genre],marker='o',label=genre)
plt.title('总销量前五的专辑类型各年份销量趋势')
plt.xlabel('年份')
plt.ylabel('销量')
plt.legend(title='专辑类型')
#添加图例
plt.grid(True,alpha=0.3)
plt.tight_layout()

#保存-关闭
plt.savefig('task4_yearly_sales.png',dpi = 100)
plt.close()
print('图表已保存为：task4_yearly_sales.png')

#Task5
print('\n===任务五：分析总销量前五的专辑类型，在不同评分体系中的平均评分===')
filtered_df = df[df['genre'].isin(top5_genres_names)]
avg_ratings = filtered_df.groupby('genre')[['rolling_stone_critic','mtv_critic','music_maniac_critic']].mean()
print('\n前五类型在不同评分体系中的平均评分：')
print(avg_ratings)

#分组柱状图
plt.figure(figsize=(12,8))
bar_width = 0.25
index = np.arange(len(top5_genres_names))
plt.bar(index,avg_ratings['rolling_stone_critic'],width=bar_width,label='滚石评分')
plt.bar(index + bar_width,avg_ratings['mtv_critic'],width=bar_width,label='MTV评分')
plt.bar(index + 2 * bar_width,avg_ratings['music_maniac_critic'],width=bar_width,label='音乐达人评分')
#图标属性
plt.title('总销量前五的专辑类型在不同评分体系中的平均评分')
plt.xlabel('专辑类型')
plt.ylabel('平均评分')
plt.xticks(index + bar_width,top5_genres_names,rotation=45)
plt.legend(title='评分体系')
plt.ylim(0,5.5)#设置y轴范围
plt.tight_layout()

#保存-关闭
plt.savefig('task5_avg_ratings.png',dpi = 100)
plt.close()
print('图表已保存为：task5_avg_ratings.png')
