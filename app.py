import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import re

st.set_page_config(page_title="餐饮差评运营分析看板", page_icon="📊", layout="wide")

OP_STYLE = """
<style>
    :root {
        --primary-red: #EF4444;
        --primary-orange: #F97316;
        --primary-yellow: #F59E0B;
        --primary-blue: #3B82F6;
        --primary-purple: #8B5CF6;
        --primary-green: #10B981;
        --primary-teal: #14B8A6;
        --bg-dark: #0F172A;
        --bg-card: #1E293B;
        --bg-card-hover: #334155;
        --text-primary: #F1F5F9;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        --border-color: #334155;
        --gradient-red: linear-gradient(135deg, #EF4444 0%, #F97316 100%);
        --gradient-blue: linear-gradient(135deg, #3B82F6 0%, #8B5CF6 100%);
        --gradient-green: linear-gradient(135deg, #10B981 0%, #14B8A6 100%);
        --gradient-orange: linear-gradient(135deg, #F97316 0%, #F59E0B 100%);
    }
    
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'PingFang SC', 'Microsoft YaHei', sans-serif;
        background-color: var(--bg-dark);
        color: var(--text-primary);
    }
    
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    
    .dashboard-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #334155 100%);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        border: 1px solid #334155;
    }
    
    .dashboard-title {
        font-size: 28px;
        font-weight: 700;
        background: linear-gradient(135deg, #EF4444 0%, #F97316 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
    }
    
    .dashboard-subtitle {
        font-size: 14px;
        color: var(--text-secondary);
    }
    
    .section-header {
        font-size: 20px;
        font-weight: 600;
        color: var(--text-primary);
        padding-bottom: 0.75rem;
        margin-bottom: 1.25rem;
        border-bottom: 2px solid var(--primary-red);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .section-header .section-icon {
        font-size: 24px;
    }
    
    .kpi-row {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 2rem;
    }
    
    .kpi-card {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1.25rem;
        border: 1px solid var(--border-color);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }
    
    .kpi-card.critical {
        border-left: 3px solid var(--primary-red);
    }
    
    .kpi-card.warning {
        border-left: 3px solid var(--primary-orange);
    }
    
    .kpi-card.info {
        border-left: 3px solid var(--primary-blue);
    }
    
    .kpi-card.success {
        border-left: 3px solid var(--primary-green);
    }
    
    .kpi-label {
        font-size: 13px;
        color: var(--text-secondary);
        margin-bottom: 0.5rem;
    }
    
    .kpi-value {
        font-size: 32px;
        font-weight: 700;
        color: var(--text-primary);
        line-height: 1;
    }
    
    .kpi-value.critical {
        color: var(--primary-red);
    }
    
    .kpi-value.warning {
        color: var(--primary-orange);
    }
    
    .kpi-value.success {
        color: var(--primary-green);
    }
    
    .kpi-value.info {
        color: var(--primary-blue);
    }
    
    .kpi-trend {
        font-size: 12px;
        color: var(--text-muted);
        margin-top: 0.5rem;
    }
    
    .chart-card {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1.25rem;
        border: 1px solid var(--border-color);
        margin-bottom: 1.25rem;
    }
    
    .chart-title {
        font-size: 16px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 1rem;
    }
    
    .upload-box {
        border: 2px dashed var(--border-color);
        border-radius: 12px;
        padding: 3rem;
        text-align: center;
        background: var(--bg-card);
        transition: all 0.2s ease;
    }
    
    .upload-box:hover {
        border-color: var(--primary-red);
    }
    
    .stFileUploader label {
        display: none;
    }
    
    .insight-box {
        background: var(--bg-card);
        border-radius: 12px;
        padding: 1.25rem;
        border: 1px solid var(--border-color);
        margin-bottom: 1.25rem;
    }
    
    .insight-item {
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        background: rgba(239, 68, 68, 0.05);
        border-radius: 8px;
        border-left: 3px solid var(--primary-red);
    }
    
    .insight-item:last-child {
        margin-bottom: 0;
    }
    
    .insight-title {
        font-size: 14px;
        font-weight: 600;
        color: var(--text-primary);
        margin-bottom: 0.25rem;
    }
    
    .insight-desc {
        font-size: 13px;
        color: var(--text-secondary);
    }
    
    .tag-cloud {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        padding: 1rem;
    }
    
    .tag {
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid rgba(239, 68, 68, 0.3);
        border-radius: 20px;
        padding: 0.5rem 1rem;
        font-size: 13px;
        color: var(--primary-red);
    }
    
    .tag.warning {
        background: rgba(249, 115, 22, 0.1);
        border-color: rgba(249, 115, 22, 0.3);
        color: var(--primary-orange);
    }
    
    .tag.blue {
        background: rgba(59, 130, 246, 0.1);
        border-color: rgba(59, 130, 246, 0.3);
        color: var(--primary-blue);
    }
    
    .table-container {
        background: var(--bg-card);
        border-radius: 12px;
        border: 1px solid var(--border-color);
        overflow: hidden;
        margin-bottom: 1.25rem;
    }
    
    .table-header {
        padding: 1rem 1.25rem;
        background: rgba(239, 68, 68, 0.1);
        border-bottom: 1px solid var(--border-color);
    }
    
    .table-title {
        font-size: 16px;
        font-weight: 600;
        color: var(--text-primary);
        margin: 0;
    }
    
    .alert-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background: var(--primary-red);
        color: white;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 600;
    }
    
    .stDataFrame {
        background: transparent !important;
        color: #F1F5F9 !important;
    }

    /* 确保 Streamlit 原生文本在暗色主题下清晰 */
    .stMarkdown, .stText, p, span, label {
        color: #F1F5F9 !important;
    }

    /* 滑块标签 */
    .stSlider label {
        color: #F1F5F9 !important;
        font-weight: 500;
    }

    /* expander 标题 */
    .streamlit-expanderHeader {
        color: #F1F5F9 !important;
    }

    /* dataframe 文字 */
    .stDataFrame {
        color: #F1F5F9 !important;
    }
</style>
"""

STOP_WORDS = {
    '的', '了', '是', '在', '我', '很', '也', '都', '就', '有', '不', '这', '那', '和', '你', '他', '她', '它',
    '着', '过', '被', '把', '给', '为', '让', '到', '从', '上', '下', '来', '去', '吃', '个', '又', '还', '要',
    '会', '能', '可以', '已经', '比较', '一个', '什么', '怎么', '没有', '因为', '所以', '但是', '而且', '或者',
    '如果', '虽然', '不过', '然后', '之后', '以后', '之前', '以前', '时候', '地方', '东西', '点了', '味道', '感觉',
    '觉得', '还是', '一般', '不错', '店里', '门店', '服务员', '这个', '那个', '一下', '真的'
}

POSITIVE_WORDS = {
    '味道好', '好吃', '美味', '香', '可口', '鲜美', '回味无穷', '赞', '满意',
    '态度好', '服务好', '热情', '周到', '贴心', '细心', '耐心', '专业', '快速',
    '出餐快', '上菜快', '响应快',
    '环境好', '干净', '整洁', '优雅', '舒适', '温馨', '宽敞', '明亮',
    '实惠', '划算', '性价比高', '便宜',
    '份量足', '量大', '足量',
    '新鲜', '卫生',
    '赠送菜', '送菜',
    '推荐', '值得', '再来'
}

def make_plotly_theme():
    return {
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'font': {'color': '#94A3B8', 'family': '-apple-system, BlinkMacSystemFont, sans-serif'},
        'xaxis': {'gridcolor': '#334155', 'zerolinecolor': '#334155'},
        'yaxis': {'gridcolor': '#334155', 'zerolinecolor': '#334155'},
        'margin': {'l': 10, 'r': 10, 't': 40, 'b': 10}
    }

st.markdown(OP_STYLE, unsafe_allow_html=True)

def calculate_reply_rate(df):
    replied_count = df['回复状态'].eq('已回复').sum()
    total_count = len(df)
    if total_count == 0:
        return 0
    return round(replied_count / total_count * 100, 1)

def filter_negative_tags(tags_series):
    filtered = tags_series[~tags_series.isin(POSITIVE_WORDS)]
    return filtered

st.markdown("""
<div class="dashboard-header">
    <div class="dashboard-title">📊 餐饮差评运营分析看板</div>
    <div class="dashboard-subtitle">聚焦差评问题 · 定位整改方向 · 提升门店服务质量</div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader("上传评价数据", type=["xlsx", "xls"], label_visibility="collapsed")

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        
        required_columns = ['评价时间', '评价ID', '省份', '城市', '评价门店', '星级分', '口味分', '环境分', '服务分', '回复状态']
        missing_cols = [col for col in required_columns if col not in df.columns]
        
        if missing_cols:
            st.error(f"上传的文件缺少必要列: {', '.join(missing_cols)}")
            st.stop()
        
        df['评价时间'] = pd.to_datetime(df['评价时间'], errors='coerce')
        df = df.dropna(subset=['评价时间'])
        
        df['评价日期'] = df['评价时间'].dt.date
        df['评价小时'] = df['评价时间'].dt.hour
        df['评价月份'] = df['评价时间'].dt.month
        
        # 星级范围筛选
        st.markdown('<div class="chart-card" style="margin-bottom: 1.5rem;">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">筛选条件</div>', unsafe_allow_html=True)
        col_filter1, col_filter2 = st.columns([3, 1])
        with col_filter1:
            star_range = st.slider("星级范围", min_value=0, max_value=5, value=(0, 5), step=1)
        with col_filter2:
            st.markdown(f'<div style="padding-top: 0.5rem; font-size: 13px; color: #94A3B8;">筛选前数据: {len(df):,} 条</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 应用星级筛选
        df = df[(df['星级分'] >= star_range[0]) & (df['星级分'] <= star_range[1])]
        
        if len(df) == 0:
            st.warning("当前筛选条件下无数据，请调整星级范围。")
            st.stop()
        
        st.markdown(f'<div style="font-size: 13px; color: #94A3B8; margin-bottom: 1rem;">当前筛选结果: {len(df):,} 条评价（星级 {star_range[0]}-{star_range[1]} 星）</div>', unsafe_allow_html=True)
        
        bad_reviews = df[df['星级分'] <= 2]
        neutral_reviews = df[(df['星级分'] > 2) & (df['星级分'] < 4)]
        good_reviews = df[df['星级分'] >= 4]
        
        bad_replied = bad_reviews['回复状态'].eq('已回复').sum()
        bad_unreplied = bad_reviews['回复状态'].eq('未回复').sum()
        bad_reply_rate = calculate_reply_rate(bad_reviews)
        
        neutral_replied = neutral_reviews['回复状态'].eq('已回复').sum()
        neutral_unreplied = neutral_reviews['回复状态'].eq('未回复').sum()
        neutral_reply_rate = calculate_reply_rate(neutral_reviews)
        
        total_replied = df['回复状态'].eq('已回复').sum()
        total_unreplied = df['回复状态'].eq('未回复').sum()
        overall_reply_rate = calculate_reply_rate(df)
        
        bad_rate = round(len(bad_reviews) / len(df) * 100, 1)
        neutral_rate = round(len(neutral_reviews) / len(df) * 100, 1)
        good_rate = round(len(good_reviews) / len(df) * 100, 1)
        
        platform_total = df['平台'].value_counts()
        platform_bad = bad_reviews['平台'].value_counts()
        platform_bad_rate = (platform_bad / platform_total * 100).round(1).fillna(0)
        
        if len(bad_reviews) == 0:
            bad_avg_scores = pd.Series({'口味分': 0, '环境分': 0, '服务分': 0})
            bad_mean_star = 0
        else:
            bad_avg_scores = bad_reviews[['口味分', '环境分', '服务分']].mean().round(2)
            bad_mean_star = bad_reviews['星级分'].mean().round(2)
        neutral_avg_scores = neutral_reviews[['口味分', '环境分', '服务分']].mean().round(2)
        
        # 差评环比变化计算
        monthly_stats = df.groupby('评价月份').agg(
            总评价=('评价ID', 'count'),
            差评数=('星级分', lambda x: (x <= 2).sum())
        ).reset_index()
        monthly_stats['差评率'] = (monthly_stats['差评数'] / monthly_stats['总评价'] * 100).round(1)
        monthly_stats = monthly_stats.sort_values('评价月份')
        
        if len(monthly_stats) >= 2:
            current_rate = monthly_stats.iloc[-1]['差评率']
            prev_rate = monthly_stats.iloc[-2]['差评率']
            change = round(current_rate - prev_rate, 1)
            if change > 0:
                mom_trend_html = f'<span style="color:#EF4444;">↑{change}%</span>'
                mom_trend_desc = f'较上月上升 {change}%，需重点关注'
                mom_class = 'critical'
            elif change < 0:
                mom_trend_html = f'<span style="color:#10B981;">↓{abs(change)}%</span>'
                mom_trend_desc = f'较上月下降 {abs(change)}%，趋势向好'
                mom_class = 'success'
            else:
                mom_trend_html = f'<span style="color:#94A3B8;">→0%</span>'
                mom_trend_desc = '与上月持平'
                mom_class = 'info'
        else:
            mom_trend_html = '<span style="color:#94A3B8;">数据不足</span>'
            mom_trend_desc = '需至少两个月数据'
            mom_class = 'info'
        
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">📌</span>
            核心KPI指标
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="kpi-row">
            <div class="kpi-card critical">
                <div class="kpi-label">差评率</div>
                <div class="kpi-value critical">{bad_rate}%</div>
                <div class="kpi-trend">差评 {len(bad_reviews):,} 条 / 总计 {len(df):,} 条</div>
            </div>
            <div class="kpi-card warning">
                <div class="kpi-label">差评回复率</div>
                <div class="kpi-value warning">{bad_reply_rate}%</div>
                <div class="kpi-trend">已回复 {bad_replied:,} 条 / 未回复 {bad_unreplied:,} 条</div>
            </div>
            <div class="kpi-card info">
                <div class="kpi-label">差评环比变化</div>
                <div class="kpi-value {mom_class}">{mom_trend_html}</div>
                <div class="kpi-trend">{mom_trend_desc}</div>
            </div>
            <div class="kpi-card success">
                <div class="kpi-label">未回复差评数</div>
                <div class="kpi-value critical">{bad_unreplied:,}</div>
                <div class="kpi-trend">紧急待处理 / 共 {len(bad_reviews):,} 条差评</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">📊</span>
            评价结构总览
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">评价等级分布</div>', unsafe_allow_html=True)
            eval_dist = pd.Series({'差评': len(bad_reviews), '中性': len(neutral_reviews), '好评': len(good_reviews)})
            fig = px.pie(
                values=eval_dist.values, 
                names=eval_dist.index,
                color=eval_dist.index,
                color_discrete_map={'差评': '#EF4444', '中性': '#F59E0B', '好评': '#10B981'},
                hole=0.6
            )
            fig.update_layout(**make_plotly_theme(), height=280, showlegend=True)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">各平台差评率对比</div>', unsafe_allow_html=True)
            fig = px.bar(
                x=platform_bad_rate.index, 
                y=platform_bad_rate.values,
                color=platform_bad_rate.values,
                color_continuous_scale=['#10B981', '#F59E0B', '#EF4444'],
                title=''
            )
            fig.update_layout(
                **make_plotly_theme(), 
                height=280,
                xaxis_title='平台',
                yaxis_title='差评率(%)',
                coloraxis_showscale=False,
                showlegend=False
            )
            for i, v in enumerate(platform_bad_rate.values):
                fig.add_annotation(
                    x=i, y=v,
                    text=f'{v}%',
                    showarrow=False,
                    font=dict(color='#F1F5F9', size=14, weight='bold'),
                    yshift=10
                )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">🎯</span>
            差评问题诊断
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">差评星级分布</div>', unsafe_allow_html=True)
            star_dist = bad_reviews['星级分'].value_counts().sort_index()
            fig = px.bar(
                x=star_dist.index.astype(str), 
                y=star_dist.values,
                color=star_dist.values,
                color_continuous_scale=['#F59E0B', '#EF4444'],
                title=''
            )
            fig.update_layout(
                **make_plotly_theme(),
                height=280,
                xaxis_title='星级',
                yaxis_title='差评数量',
                coloraxis_showscale=False,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">差评各项评分均值</div>', unsafe_allow_html=True)
            fig = px.bar(
                x=bad_avg_scores.index, 
                y=bad_avg_scores.values,
                color=['#EF4444', '#F97316', '#F59E0B'],
                title=''
            )
            fig.update_layout(
                **make_plotly_theme(),
                height=280,
                xaxis_title='评分维度',
                yaxis_title='平均分',
                yaxis_range=[0, 3],
                showlegend=False
            )
            for i, (dim, val) in enumerate(bad_avg_scores.items()):
                fig.add_annotation(
                    x=i, y=val,
                    text=str(val),
                    showarrow=False,
                    font=dict(color='#F1F5F9', size=14, weight='bold'),
                    yshift=10
                )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">🏷️</span>
            差评标签分析（已过滤好评词汇）
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="insight-box">
            <div style="font-size: 13px; color: var(--text-secondary);">
                💡 已自动过滤以下好评词汇：味道好、好吃、美味、态度好、服务好、出餐快、环境好、干净、整洁、实惠、性价比高、份量足、新鲜、推荐...
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">菜品负面标签TOP10</div>', unsafe_allow_html=True)
            if '菜品标签' in df.columns:
                bad_dish_tags = bad_reviews['菜品标签'].dropna().str.split(',').explode()
                bad_dish_tags = filter_negative_tags(bad_dish_tags)
                bad_dish_tags = bad_dish_tags.value_counts().head(10)
                if len(bad_dish_tags) > 0:
                    fig = px.bar(
                        x=bad_dish_tags.values, 
                        y=bad_dish_tags.index, 
                        orientation='h',
                        color=bad_dish_tags.values,
                        color_continuous_scale=['#EF4444', '#F97316']
                    )
                    fig.update_layout(
                        **make_plotly_theme(),
                        height=320,
                        xaxis_title='出现次数',
                        coloraxis_showscale=False,
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.markdown('<div style="text-align:center; color: var(--text-muted); padding: 2rem;">暂无数据</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center; color: var(--text-muted); padding: 2rem;">缺少菜品标签列</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">服务负面标签TOP10</div>', unsafe_allow_html=True)
            if '服务标签' in df.columns:
                bad_service_tags = bad_reviews['服务标签'].dropna().str.split(',').explode()
                bad_service_tags = filter_negative_tags(bad_service_tags)
                bad_service_tags = bad_service_tags.value_counts().head(10)
                if len(bad_service_tags) > 0:
                    fig = px.bar(
                        x=bad_service_tags.values, 
                        y=bad_service_tags.index, 
                        orientation='h',
                        color=bad_service_tags.values,
                        color_continuous_scale=['#F97316', '#F59E0B']
                    )
                    fig.update_layout(
                        **make_plotly_theme(),
                        height=320,
                        xaxis_title='出现次数',
                        coloraxis_showscale=False,
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.markdown('<div style="text-align:center; color: var(--text-muted); padding: 2rem;">暂无数据</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center; color: var(--text-muted); padding: 2rem;">缺少服务标签列</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">环境负面标签TOP10</div>', unsafe_allow_html=True)
            if '环境标签' in df.columns:
                bad_env_tags = bad_reviews['环境标签'].dropna().str.split(',').explode()
                bad_env_tags = filter_negative_tags(bad_env_tags)
                bad_env_tags = bad_env_tags.value_counts().head(10)
                if len(bad_env_tags) > 0:
                    fig = px.bar(
                        x=bad_env_tags.values, 
                        y=bad_env_tags.index, 
                        orientation='h',
                        color=bad_env_tags.values,
                        color_continuous_scale=['#F59E0B', '#EF4444']
                    )
                    fig.update_layout(
                        **make_plotly_theme(),
                        height=320,
                        xaxis_title='出现次数',
                        coloraxis_showscale=False,
                        showlegend=False
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.markdown('<div style="text-align:center; color: var(--text-muted); padding: 2rem;">暂无数据</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center; color: var(--text-muted); padding: 2rem;">缺少环境标签列</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">🔍</span>
            差评关键词分析
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if '评价详情' in df.columns:
            bad_comments = ' '.join(bad_reviews['评价详情'].dropna().astype(str))
            words = re.findall(r'[\u4e00-\u9fa5]{2,}', bad_comments)
            words = [w for w in words if w not in POSITIVE_WORDS and w not in STOP_WORDS]
            # 保留3字以上的关键短语，或2字有实际业务含义的词（已过滤停用词）
            words = [w for w in words if len(w) >= 3 or len(w) == 2]
            if words:
                word_counts = pd.Series(words).value_counts().head(20)
                fig = px.bar(
                    x=word_counts.values, 
                    y=word_counts.index, 
                    orientation='h',
                    color=word_counts.values,
                    color_continuous_scale=['#EF4444', '#F59E0B']
                )
                fig.update_layout(
                    **make_plotly_theme(),
                    height=400,
                    xaxis_title='出现次数',
                    yaxis_autorange='reversed',
                    coloraxis_showscale=False,
                    showlegend=False
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.markdown('<div style="text-align:center; color: var(--text-muted); padding: 2rem;">暂无有效负面关键词数据</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="text-align:center; color: var(--text-muted); padding: 2rem;">缺少评价详情列</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">📍</span>
            差评地域分布
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">差评量TOP10省份</div>', unsafe_allow_html=True)
            province_bad = bad_reviews['省份'].value_counts().head(10)
            fig = px.bar(
                x=province_bad.index, 
                y=province_bad.values,
                color=province_bad.values,
                color_continuous_scale=['#EF4444', '#F97316']
            )
            fig.update_layout(
                **make_plotly_theme(),
                height=300,
                xaxis_title='省份',
                yaxis_title='差评数量',
                coloraxis_showscale=False,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">差评量TOP10城市</div>', unsafe_allow_html=True)
            city_bad = bad_reviews['城市'].value_counts().head(10)
            fig = px.bar(
                x=city_bad.values, 
                y=city_bad.index, 
                orientation='h',
                color=city_bad.values,
                color_continuous_scale=['#F97316', '#F59E0B']
            )
            fig.update_layout(
                **make_plotly_theme(),
                height=300,
                xaxis_title='差评数量',
                coloraxis_showscale=False,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">各省份差评率TOP10</div>', unsafe_allow_html=True)
        province_bad_rate = (bad_reviews['省份'].value_counts() / df['省份'].value_counts() * 100).round(1).dropna().sort_values(ascending=False).head(10)
        fig = px.bar(
            x=province_bad_rate.index, 
            y=province_bad_rate.values,
            color=province_bad_rate.values,
            color_continuous_scale=['#10B981', '#F59E0B', '#EF4444']
        )
        fig.update_layout(
            **make_plotly_theme(),
            height=280,
            xaxis_title='省份',
            yaxis_title='差评率(%)',
            coloraxis_showscale=False,
            showlegend=False
        )
        for i, v in enumerate(province_bad_rate.values):
            fig.add_annotation(
                x=i, y=v,
                text=f'{v}%',
                showarrow=False,
                font=dict(color='#F1F5F9', size=12, weight='bold'),
                yshift=10
            )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">📈</span>
            差评时间趋势
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">每日差评数量趋势</div>', unsafe_allow_html=True)
            daily_bad = bad_reviews.groupby('评价日期')['评价ID'].count()
            fig = px.line(
                daily_bad,
                color_discrete_sequence=['#EF4444']
            )
            fig.update_traces(fill='tozeroy', fillcolor='rgba(239, 68, 68, 0.1)')
            fig.update_layout(
                **make_plotly_theme(),
                height=280,
                xaxis_title='日期',
                yaxis_title='差评数量'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">各时段差评分布</div>', unsafe_allow_html=True)
            hourly_bad = bad_reviews.groupby('评价小时')['评价ID'].count()
            fig = px.line(
                hourly_bad,
                color_discrete_sequence=['#F97316'],
                markers=True
            )
            fig.update_layout(
                **make_plotly_theme(),
                height=280,
                xaxis_title='小时',
                yaxis_title='差评数量'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        month_names = ['', '1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        monthly_bad = bad_reviews.groupby('评价月份')['评价ID'].count()
        monthly_total = df.groupby('评价月份')['评价ID'].count()
        monthly_bad_rate = (monthly_bad / monthly_total * 100).round(1).fillna(0)
        monthly_bad_rate.index = monthly_bad_rate.index.map(lambda x: month_names[x])
        
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">月度差评率趋势</div>', unsafe_allow_html=True)
        fig = px.line(
            monthly_bad_rate,
            markers=True,
            color_discrete_sequence=['#F59E0B']
        )
        fig.update_traces(fill='tozeroy', fillcolor='rgba(245, 158, 11, 0.1)')
        fig.update_layout(
            **make_plotly_theme(),
            height=280,
            xaxis_title='月份',
            yaxis_title='差评率(%)'
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">👥</span>
            差评用户画像
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">差评用户VIP分布</div>', unsafe_allow_html=True)
            vip_bad = bad_reviews['是否vip'].value_counts()
            fig = px.pie(
                values=vip_bad.values, 
                names=vip_bad.index,
                color_discrete_sequence=['#EF4444', '#3B82F6']
            )
            fig.update_layout(
                **make_plotly_theme(),
                height=280
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="chart-card">', unsafe_allow_html=True)
            st.markdown('<div class="chart-title">差评用户等级分布</div>', unsafe_allow_html=True)
            level_bad = bad_reviews['用户等级'].value_counts().sort_index()
            fig = px.bar(
                x=level_bad.index.astype(str), 
                y=level_bad.values,
                color=level_bad.values,
                color_continuous_scale=['#3B82F6', '#EF4444']
            )
            fig.update_layout(
                **make_plotly_theme(),
                height=280,
                xaxis_title='用户等级',
                yaxis_title='差评数量',
                coloraxis_showscale=False,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">VIP与普通用户差评率对比</div>', unsafe_allow_html=True)
        vip_bad_rate = (bad_reviews['是否vip'].value_counts() / df['是否vip'].value_counts() * 100).round(1).fillna(0)
        fig = px.bar(
            x=vip_bad_rate.index.astype(str), 
            y=vip_bad_rate.values,
            color=['#EF4444', '#3B82F6'][:len(vip_bad_rate)]
        )
        fig.update_layout(
            **make_plotly_theme(),
            height=280,
            xaxis_title='用户类型',
            yaxis_title='差评率(%)',
            showlegend=False
        )
        for i, v in enumerate(vip_bad_rate.values):
            fig.add_annotation(
                x=i, y=v,
                text=f'{v}%',
                showarrow=False,
                font=dict(color='#F1F5F9', size=14, weight='bold'),
                yshift=10
            )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">⚠️</span>
            未回复差评预警
        </div>
        """, unsafe_allow_html=True)
        
        unreplied_bad = bad_reviews[bad_reviews['回复状态'] == '未回复']
        
        st.markdown(f"""
        <div class="kpi-row">
            <div class="kpi-card critical">
                <div class="kpi-label">未回复差评</div>
                <div class="kpi-value critical">{len(unreplied_bad):,}</div>
                <div class="kpi-trend">需优先处理</div>
            </div>
            <div class="kpi-card warning">
                <div class="kpi-label">未回复中性评价</div>
                <div class="kpi-value warning">{neutral_unreplied:,}</div>
                <div class="kpi-trend">建议跟进回复</div>
            </div>
            <div class="kpi-card info">
                <div class="kpi-label">整体未回复数</div>
                <div class="kpi-value info">{total_unreplied:,}</div>
                <div class="kpi-trend">整体回复率 {overall_reply_rate}%</div>
            </div>
            <div class="kpi-card success">
                <div class="kpi-label">差评回复率</div>
                <div class="kpi-value success">{bad_reply_rate}%</div>
                <div class="kpi-trend">已回复 {bad_replied:,} 条</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">未回复差评城市分布TOP10</div>', unsafe_allow_html=True)
        if len(unreplied_bad) > 0:
            unreplied_city = unreplied_bad['城市'].value_counts().head(10)
            fig = px.bar(
                x=unreplied_city.values, 
                y=unreplied_city.index, 
                orientation='h',
                color=unreplied_city.values,
                color_continuous_scale=['#F59E0B', '#EF4444']
            )
            fig.update_layout(
                **make_plotly_theme(),
                height=320,
                xaxis_title='未回复差评数',
                coloraxis_showscale=False,
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown('<div style="text-align:center; color: var(--text-muted); padding: 2rem;">暂无未回复差评</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 门店差评排行榜
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">🏪</span>
            门店差评排行（与门店共识重点）
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.markdown('<div class="chart-title">TOP15 门店差评率排行</div>', unsafe_allow_html=True)
        
        store_total = df.groupby('评价门店').size().reset_index(name='总评价数')
        store_bad_count = bad_reviews.groupby('评价门店').size().reset_index(name='差评数')
        store_unreplied_count = bad_reviews[bad_reviews['回复状态'] == '未回复'].groupby('评价门店').size().reset_index(name='未回复数')
        
        store_rank = store_total.merge(store_bad_count, on='评价门店', how='left').fillna(0)
        store_rank = store_rank.merge(store_unreplied_count, on='评价门店', how='left').fillna(0)
        store_rank['差评率'] = (store_rank['差评数'] / store_rank['总评价数'] * 100).round(1)
        store_rank = store_rank.sort_values('差评率', ascending=False).head(15)
        
        def get_store_top_tags(store_name):
            store_bad = bad_reviews[bad_reviews['评价门店'] == store_name]
            tags = []
            for col in ['菜品标签', '服务标签', '环境标签']:
                if col in df.columns:
                    t = store_bad[col].dropna().str.split(',').explode().str.strip()
                    t = filter_negative_tags(t)
                    tags.extend(t.tolist())
            tag_counts = pd.Series(tags).value_counts().head(2)
            return '、'.join(tag_counts.index) if len(tag_counts) > 0 else '-'
        
        store_rank['主要问题'] = store_rank['评价门店'].apply(get_store_top_tags)
        store_rank = store_rank[['评价门店', '差评数', '差评率', '未回复数', '主要问题']]
        store_rank.columns = ['门店名称', '差评数', '差评率(%)', '未回复数', '主要问题标签']
        
        def highlight_high_bad_rate(row):
            if row['差评率(%)'] > 20:
                return ['background-color: rgba(239, 68, 68, 0.15); color: #F1F5F9;'] * len(row)
            return [''] * len(row)
        
        styled_store = store_rank.style.apply(highlight_high_bad_rate, axis=1).format({'差评率(%)': '{:.1f}'})
        st.dataframe(styled_store, use_container_width=True)
        
        if (store_rank['差评率(%)'] > 20).any():
            high_risk_count = (store_rank['差评率(%)'] > 20).sum()
            st.markdown(f'<div style="margin-top: 0.5rem; font-size: 13px; color: #EF4444;">⚠️ 有 {high_risk_count} 家门店差评率超过20%，建议优先重点共识整改</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">📋</span>
            运营整改建议
        </div>
        """, unsafe_allow_html=True)
        
        issue_list = []
        
        def collect_issues(tag_col, category_name, suggestions_map):
            if tag_col not in df.columns:
                return
            tags = bad_reviews[tag_col].dropna().str.split(',').explode().str.strip()
            tags = filter_negative_tags(tags)
            tags = tags[tags != '']
            for tag, count in tags.value_counts().head(5).items():
                mask = bad_reviews[tag_col].fillna('').str.contains(tag, regex=False)
                affected = bad_reviews[mask]['评价门店'].nunique() if mask.sum() > 0 else 0
                avg_star = bad_reviews[mask]['星级分'].mean() if mask.sum() > 0 else 2
                severity = round(count * (3 - avg_star), 1)
                suggestion = suggestions_map.get(tag, f'针对"{tag}"问题，建议加强{category_name}方面的管理和培训')
                issue_list.append({
                    '问题': tag,
                    '分类': category_name,
                    '频次': int(count),
                    '影响门店': int(affected),
                    '均星': round(avg_star, 1),
                    '严重程度': severity,
                    '建议': suggestion
                })
        
        collect_issues('菜品标签', '菜品', {
            '难吃': '优化菜品配方，加强厨师培训，建立出品试吃机制',
            '太咸': '调整菜品盐度标准，统一调味配方',
            '太辣': '调整辣度标准，提供辣度选择',
            '太甜': '调整糖度标准，统一甜品配方',
            '油腻': '优化烹饪方式，减少用油量',
            '不新鲜': '加强食材验收标准，优化库存周转',
            '有异物': '加强后厨卫生管理，建立异物防控SOP',
            '量少': '调整份量标准，确保出品稳定',
            '凉了': '优化出餐流程，确保热菜热送',
            '慢': '优化出餐流程，提升后厨效率'
        })
        
        collect_issues('服务标签', '服务', {
            '慢': '优化服务流程，提升响应速度，增加高峰期人手',
            '态度差': '加强服务培训，建立服务态度考核机制',
            '不理人': '明确服务标准，要求主动迎客和响应',
            '上菜慢': '优化点餐出餐流程，加强前后台配合',
            '不热情': '加强服务意识培训，建立奖惩机制'
        })
        
        collect_issues('环境标签', '环境', {
            '脏': '加强清洁频次，建立卫生检查表',
            '吵': '优化座位布局，增加隔音措施',
            '挤': '优化座位间距，提升用餐舒适度',
            '热': '检查空调设备，确保温度适宜',
            '冷': '检查空调/暖气设备，确保温度适宜'
        })
        
        issue_list.sort(key=lambda x: x['严重程度'], reverse=True)
        
        insights_html = '<div class="insight-box">'
        
        category_icons = {'菜品': '🍽️', '服务': '👩‍💼', '环境': '🏠'}
        category_colors = {'菜品': '#EF4444', '服务': '#F97316', '环境': '#F59E0B'}
        
        if len(issue_list) > 0:
            for issue in issue_list[:8]:
                icon = category_icons.get(issue['分类'], '🔴')
                color = category_colors.get(issue['分类'], '#EF4444')
                insights_html += f'''<div class="insight-item" style="border-left-color: {color};">
                    <div class="insight-title">{icon} 【{issue['分类']}】{issue['问题']} — 严重程度: {issue['严重程度']}</div>
                    <div class="insight-desc">
                        出现 {issue['频次']} 次，影响 {issue['影响门店']} 家门店，平均星级 {issue['均星']}<br>
                        💡 建议：{issue['建议']}
                    </div>
                </div>'''
        
        if bad_rate > 20:
            insights_html += f'<div class="insight-item"><div class="insight-title">🔴 整体差评率偏高 ({bad_rate}%)</div><div class="insight-desc">建议组织门店店长召开专项整改会议，制定改善计划</div></div>'
        
        if bad_reply_rate < 80:
            insights_html += f'<div class="insight-item"><div class="insight-title">🟠 差评回复率不足 ({bad_reply_rate}%)</div><div class="insight-desc">建议制定差评回复SLA标准，要求24小时内100%回复</div></div>'
        
        if len(issue_list) == 0 and bad_rate <= 20 and bad_reply_rate >= 80:
            insights_html += '<div class="insight-item"><div class="insight-title">🟢 整体表现良好</div><div class="insight-desc">当前差评率与回复率均在合理范围内，建议继续保持并关注细节优化</div></div>'
        
        insights_html += '</div>'
        st.markdown(insights_html, unsafe_allow_html=True)
        
        with st.expander("📊 差评详情数据"):
            display_columns = ['评价时间', '省份', '城市', '评价门店', '星级分', '口味分', '环境分', '服务分', '评价详情', '回复状态']
            available_cols = [col for col in display_columns if col in df.columns]
            st.dataframe(bad_reviews[available_cols].sort_values('评价时间', ascending=False), use_container_width=True)
        
        with st.expander("⚠️ 未回复差评明细"):
            if len(unreplied_bad) > 0:
                st.dataframe(unreplied_bad[available_cols].sort_values('评价时间', ascending=False), use_container_width=True)
            else:
                st.success("所有差评均已回复！")
        
        with st.expander("📋 数据验证"):
            st.markdown(f"""
            **回复状态数据验证:**
            - 已回复: {total_replied} 条
            - 未回复: {total_unreplied} 条
            - 合计: {len(df)} 条
            
            **差评数据验证:**
            - 差评数量: {len(bad_reviews)} 条
            - 差评率: {bad_rate}%
            - 差评已回复: {bad_replied} 条
            - 差评未回复: {bad_unreplied} 条
            - 差评回复率: {bad_reply_rate}%
            
            **中性评价数据验证:**
            - 中性评价数量: {len(neutral_reviews)} 条
            - 中性评价率: {neutral_rate}%
            - 中性评价已回复: {neutral_replied} 条
            - 中性评价未回复: {neutral_unreplied} 条
            - 中性评价回复率: {neutral_reply_rate}%
            """)
    
    except Exception as e:
        st.error(f"处理文件时发生错误: {str(e)}")
        st.info("请确保上传的Excel文件包含必要的列：评价时间、评价ID、省份、城市、评价门店、星级分、口味分、环境分、服务分、回复状态")

else:
    st.markdown("""
    <div class="upload-box">
        <div style="font-size: 48px; margin-bottom: 1rem;">📤</div>
        <div style="font-size: 18px; font-weight: 600; color: var(--text-primary); margin-bottom: 0.5rem;">上传Excel评价数据</div>
        <div style="font-size: 14px; color: var(--text-secondary);">支持 .xlsx 和 .xls 格式，上传后将自动生成差评分析看板</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: var(--bg-card); border-radius: 12px; padding: 2rem; margin-top: 1rem; border: 1px solid var(--border-color);">
        <h3 style="font-size: 18px; font-weight: 600; color: var(--text-primary); margin-bottom: 1.5rem;">📊 差评运营分析看板</h3>
        
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.5rem;">
            <div>
                <h4 style="font-size: 14px; font-weight: 500; color: #EF4444; margin-bottom: 0.5rem;">核心KPI</h4>
                <ul style="font-size: 13px; color: var(--text-secondary); list-style: none; padding: 0;">
                    <li style="margin-bottom: 0.25rem;">• 差评率</li>
                    <li style="margin-bottom: 0.25rem;">• 差评回复率</li>
                    <li style="margin-bottom: 0.25rem;">• 差评环比变化</li>
                    <li>• 未回复差评数</li>
                </ul>
            </div>
            
            <div>
                <h4 style="font-size: 14px; font-weight: 500; color: #F97316; margin-bottom: 0.5rem;">问题诊断</h4>
                <ul style="font-size: 13px; color: var(--text-secondary); list-style: none; padding: 0;">
                    <li style="margin-bottom: 0.25rem;">• 差评星级分布</li>
                    <li style="margin-bottom: 0.25rem;">• 差评各项评分</li>
                    <li style="margin-bottom: 0.25rem;">• 差评标签分析（过滤好评）</li>
                    <li>• 差评关键词分析</li>
                </ul>
            </div>
            
            <div>
                <h4 style="font-size: 14px; font-weight: 500; color: #F59E0B; margin-bottom: 0.5rem;">运营整改</h4>
                <ul style="font-size: 13px; color: var(--text-secondary); list-style: none; padding: 0;">
                    <li style="margin-bottom: 0.25rem;">• 差评地域分布</li>
                    <li style="margin-bottom: 0.25rem;">• 未回复差评预警</li>
                    <li style="margin-bottom: 0.25rem;">• 时间趋势分析</li>
                    <li>• 智能整改建议</li>
                </ul>
            </div>
        </div>
        
        <div style="margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid var(--border-color);">
            <h4 style="font-size: 14px; font-weight: 500; color: var(--text-primary); margin-bottom: 0.5rem;">📌 核心目的</h4>
            <p style="font-size: 13px; color: var(--text-secondary); line-height: 1.6;">
                通过数据化分析，精准定位差评原因，与门店共识整改方向，建立持续改进闭环，最终降低差评率、提升用户满意度。
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)