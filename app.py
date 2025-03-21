import streamlit as st
from utils import search_ebay_items, check_google_presence
import pandas as pd
import time

st.title("唯一在售商品检测器")
keyword = st.text_input("请输入关键词", "bicycle playing cards rare")
max_results = st.slider("检索数量", 1, 20, 5)

if st.button("开始检测"):
    with st.spinner("正在搜索 eBay..."):
        items = search_ebay_items(keyword, max_results=max_results)

    results = []
    for item in items:
        st.write(f"检查：**{item['title']}**")
        non_ebay_links = check_google_presence(item['title'])
        time.sleep(2)

        is_unique = len(non_ebay_links) == 0
        results.append({
            "标题": item['title'],
            "eBay链接": item['link'],
            "是否唯一": "是" if is_unique else "否",
            "其他链接": "\n".join(non_ebay_links) if non_ebay_links else "-"
        })

    df = pd.DataFrame(results)
    st.dataframe(df)

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("下载结果为CSV", data=csv, file_name="unique_items.csv")
