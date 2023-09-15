import streamlit as st
from pandasai.llm.openai import OpenAI
import os
import pandas as pd
from pandasai import PandasAI, SmartDataframe
from pandasai.middlewares.base import Middleware

openai_api_key = os.getenv("OPENAI_API_KEY")


class StreamlitMiddleware(Middleware):
    def run(self, code: str) -> str:
        wrapper = st.session_state.wrapper if 'wrapper' in st.session_state else 'st'
        code = code.replace("plt.show()", f"{wrapper}.pyplot(plt.gcf())")
        code = code.replace("plt.close(fig)", f"{wrapper}.pyplot(plt.gcf())")
        code = code.replace("plt.close()", f"{wrapper}.pyplot(plt.gcf())")
        code = "import streamlit as st\n" + code
        return code


class ChatBot:
    def __init__(self):
        self.llm = OpenAI(api_token=openai_api_key)

    def set_data(self, data):
        self.data = data
        # self.df = SmartDataframe(data, config={"llm": self.llm, 'verbose': True, 'middlewares':[StreamlitMiddleware()]})
        self.df = PandasAI(
            llm=self.llm,
            verbose=True,
            middlewares=[StreamlitMiddleware()],
            save_charts=True,
            save_charts_path='/tmp/pandasai'
        )

    def chat(self, prompt):
        result = self.df.run(self.data, prompt)
        return result


if __name__ == '__main__':
    bot = ChatBot()

    st.set_page_config(layout='wide')
    st.title("数翼 Excel / CSV 分析")
    input_csv = st.file_uploader("上传 CSV 文件", type=['xlsx', 'csv'])

    if input_csv is not None:
        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            st.info("CSV 上传成功")
            if input_csv.name.lower().endswith('.csv'):
                data = pd.read_csv(input_csv)
            else:
                data = pd.read_excel(input_csv)
            st.dataframe(data, use_container_width=True)
            bot.set_data(data)

        with col2:
            st.info("开始聊天吧")
            input_text = st.text_area("输入您的问题", value='销量最好的三个产品饼图')

            if input_text is not None:
                if st.button("和 CSV 聊天"):
                    with col3:
                        st.success("问题: " + input_text)
                        result = bot.chat(input_text)
                        st.write(result)
