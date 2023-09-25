import streamlit as st
from pandasai.llm.openai import OpenAI
import os
import pandas as pd
from pandasai import PandasAI, SmartDataframe

openai_api_key = os.getenv("OPENAI_API_KEY")

if __name__ == '__main__':

    st.set_page_config(layout='wide')
    st.title("数翼 Excel / CSV 分析")
    input_csv = st.file_uploader("上传 CSV 文件", type=['xlsx', 'csv'])

    if input_csv is not None:
        col1, col2 = st.columns([1, 1])

        with col1:
            st.info("CSV 上传成功")
            if input_csv.name.lower().endswith('.csv'):
                data = pd.read_csv(input_csv)
            else:
                data = pd.read_excel(input_csv)
            st.dataframe(data, use_container_width=True)

        with col2:
            st.info("开始聊天吧")
            input_text = st.text_area("输入您的问题", value='销量最好的三个产品是什么')

            if input_text is not None:
                if st.button("和 CSV 聊天"):
                    st.info(f"问题: {input_text}")
                    df = PandasAI(OpenAI(api_token=openai_api_key), verbose=True)
                    st.write(df.run(data, input_text))

