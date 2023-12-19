import streamlit as st
import requests
from bs4 import BeautifulSoup
import jieba
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import Pie, Bar, Line
from pyecharts.globals import ThemeType
import streamlit.components.v1 as components


def generate_word_frequency(url):
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    filter_words = ['\n', ' ', '，', '。', '！', '？', '的', '是', '在', '了', '和', '同', '为', '也', '这', '有',
                    '就', '又', '或', '但', '如果', '由于', '因此', '所以', '之', '与',
                    '及', '或者', '一些', '一样', '例如', '这些', '那些', '不', '也不',
                    '之一', '之二', '之三', '之四', '之五', '之六', '之七', '之八', '之九', '之十',
                    '……', '。', '，', '、', '：', '；', '！', '？', '“', '”',
                    '（', '）', '【', '】', '《', '》', '［', '］', '｛', '｝'
                    ,'我', '他', '她', '你']
    for word in filter_words:
        text = text.replace(word, '')

    words = jieba.cut(text)

    word_count = Counter(words)

    top_10_words = dict(word_count.most_common(10))

    x = list(top_10_words.keys())
    y = list(top_10_words.values())

    pie = (
        Pie(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add("", [list(z) for z in zip(x, y)])
        .set_global_opts(title_opts=opts.TitleOpts(title="饼状图"),
                         legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )

    bar = (
        Bar(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(x)
        .add_yaxis("word Count", y)
       .set_global_opts(title_opts=opts.TitleOpts(title="柱状图 "),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
                         legend_opts=opts.LegendOpts(is_show=False))
    )

    line = (
        Line(init_opts=opts.InitOpts(theme=ThemeType.LIGHT))
        .add_xaxis(x)
        .add_yaxis("word Count", y)
        .set_global_opts(title_opts=opts.TitleOpts(title=" 折线图"),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=45)),
                         legend_opts=opts.LegendOpts(is_show=False))
    )

    return pie.render_embed(), bar.render_embed(), line.render_embed()


def main():
    st.title("Word Frequency")
    url = st.text_input("请输入要爬取的网址")
    chart_type = st.selectbox("请选择要显示的图表类型", ["饼状图", "柱状图", "折线图"])

    if st.button("生成图") or url:
        if url:
            pie_html, bar_html, line_html = generate_word_frequency(url)
            if chart_type == "饼状图":
                chart_html = pie_html
            elif chart_type == "柱状图":
                chart_html = bar_html
            else:
                chart_html = line_html

            chart_component = components.html(chart_html, height=500, width=1000)


if __name__ == "__main__":
    main()