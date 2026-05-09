import pandas as pd

df = pd.read_excel('副本评价下载2026.02.01-2026.05.01_1483444_1778225233256.xlsx')

df['评价时间'] = pd.to_datetime(df['评价时间'])
df['评价日期'] = df['评价时间'].dt.date
df['评价月份'] = df['评价时间'].dt.month

print("="*70)
print("🍽️ 餐饮用户评价分析报告")
print("="*70)

print("\n📊 一、核心指标概览")
print("-"*40)
print(f"总评价数: {len(df):,} 条")
print(f"数据时间范围: {df['评价时间'].min().strftime('%Y-%m-%d')} 至 {df['评价时间'].max().strftime('%Y-%m-%d')}")
print(f"平均星级分: {df['星级分'].mean().round(2)} 分")
print(f"平均口味分: {df['口味分'].mean().round(2)} 分")
print(f"平均环境分: {df['环境分'].mean().round(2)} 分")
print(f"平均服务分: {df['服务分'].mean().round(2)} 分")
vip_ratio = (df['是否vip'].value_counts().get('是', 0) / len(df) * 100).round(1)
print(f"VIP用户占比: {vip_ratio}%")
complaint_rate = (df['投诉状态'].notna().sum() / len(df) * 100).round(1)
print(f"投诉率: {complaint_rate}%")
reply_rate = (df['回复状态'].notna().sum() / len(df) * 100).round(1)
print(f"回复率: {reply_rate}%")

print("\n📈 二、评分分布分析")
print("-"*40)
print("星级分分布:")
star_dist = df['星级分'].value_counts().sort_index()
for star, count in star_dist.items():
    percentage = round(count / len(df) * 100, 1)
    print(f"  {star}星: {int(count)}条 ({percentage}%)")

print("\n🏆 各项评分TOP3省份:")
province_scores = df.groupby('省份')[['星级分', '口味分', '环境分', '服务分']].mean().round(2)
print("星级分TOP3:")
print(province_scores['星级分'].sort_values(ascending=False).head(3))
print("\n口味分TOP3:")
print(province_scores['口味分'].sort_values(ascending=False).head(3))

print("\n🌍 三、地域分布分析")
print("-"*40)
print("评价量TOP10省份:")
province_counts = df['省份'].value_counts().head(10)
for i, (province, count) in enumerate(province_counts.items(), 1):
    print(f"  {i}. {province}: {count}条")

print("\n评价量TOP10城市:")
city_counts = df['城市'].value_counts().head(10)
for i, (city, count) in enumerate(city_counts.items(), 1):
    print(f"  {i}. {city}: {count}条")

print("\n🕐 四、时间趋势分析")
print("-"*40)
print("月度评价量:")
monthly_counts = df.groupby('评价月份')['评价ID'].count()
month_names = {2:'二月', 3:'三月', 4:'四月', 5:'五月'}
for month, count in monthly_counts.items():
    print(f"  {month_names.get(month, month)}: {count}条")

print("\n各时段评价分布:")
hourly_counts = df['评价时间'].dt.hour.value_counts().sort_index()
peak_hour = hourly_counts.idxmax()
print(f"  高峰时段: {peak_hour}:00")
print(f"  评价量峰值: {hourly_counts.max()}条")

print("\n👥 五、用户分析")
print("-"*40)
print("VIP用户分布:")
vip_counts = df['是否vip'].value_counts()
for vip, count in vip_counts.items():
    percentage = round(count / len(df) * 100, 1)
    print(f"  {'VIP用户' if vip == '是' else '普通用户'}: {int(count)}人 ({percentage}%)")

print("\n用户等级分布:")
level_counts = df['用户等级'].value_counts()
for level, count in level_counts.items():
    print(f"  {level}: {count}人")

print("\nVIP与非VIP评分对比:")
vip_scores = df.groupby('是否vip')['星级分'].mean().round(2)
print(f"  VIP用户平均评分: {vip_scores.get('是', 0)}分")
print(f"  普通用户平均评分: {vip_scores.get('否', 0)}分")

print("\n⚠️ 六、投诉分析")
print("-"*40)
complaint_df = df[df['投诉状态'].notna()]
print(f"投诉总数: {len(complaint_df)}条")
if len(complaint_df) > 0:
    print("\n投诉类型分布:")
    complaint_types = complaint_df['投诉类型'].value_counts()
    for complaint_type, count in complaint_types.items():
        print(f"  {complaint_type}: {count}条")
    
    print("\n投诉量TOP5城市:")
    complaint_cities = complaint_df['城市'].value_counts().head(5)
    for city, count in complaint_cities.items():
        print(f"  {city}: {count}条")

print("\n🏷️ 七、标签分析")
print("-"*40)
print("菜品标签TOP10:")
dish_tags = df['菜品标签'].dropna().str.split(',').explode().value_counts().head(10)
for tag, count in dish_tags.items():
    print(f"  {tag}: {count}次")

print("\n服务标签TOP10:")
service_tags = df['服务标签'].dropna().str.split(',').explode().value_counts().head(10)
for tag, count in service_tags.items():
    print(f"  {tag}: {count}次")

print("\n环境标签TOP10:")
env_tags = df['环境标签'].dropna().str.split(',').explode().value_counts().head(10)
for tag, count in env_tags.items():
    print(f"  {tag}: {count}次")

print("\n📊 八、平台分析")
print("-"*40)
print("各平台评价量:")
platform_counts = df['平台'].value_counts()
for platform, count in platform_counts.items():
    percentage = round(count / len(df) * 100, 1)
    print(f"  {platform}: {int(count)}条 ({percentage}%)")

print("\n各平台平均评分:")
platform_scores = df.groupby('平台')[['星级分']].mean().round(2)
print(platform_scores)

print("\n" + "="*70)
print("✅ 分析报告生成完成")
print("="*70)