import pandas as pd

df = pd.read_excel('副本评价下载2026.02.01-2026.05.01_1483444_1778225233256.xlsx')

print('=== 数据验证 ===')
print()
print('回复状态分布:')
print(df['回复状态'].value_counts(dropna=False))
print()

total_replied = df['回复状态'].eq('已回复').sum()
total_unreplied = df['回复状态'].eq('未回复').sum()
overall_reply_rate = round(total_replied / len(df) * 100, 1)

print(f'已回复: {total_replied} 条')
print(f'未回复: {total_unreplied} 条')
print(f'总评价数: {len(df)} 条')
print(f'整体回复率: {overall_reply_rate}%')
print()

print('=== 差评数据 ===')
bad_reviews = df[df['星级分'] <= 2]
print(f'差评数量: {len(bad_reviews)} 条')
print(f'差评率: {round(len(bad_reviews) / len(df) * 100, 1)}%')

bad_replied = bad_reviews['回复状态'].eq('已回复').sum()
bad_unreplied = bad_reviews['回复状态'].eq('未回复').sum()
bad_reply_rate = round(bad_replied / len(bad_reviews) * 100, 1)

print(f'差评已回复: {bad_replied} 条')
print(f'差评未回复: {bad_unreplied} 条')
print(f'差评回复率: {bad_reply_rate}%')