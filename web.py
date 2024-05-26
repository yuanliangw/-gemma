import json
import requests
import streamlit as st
import ollama

from streamlit_chat import message


role = 'user'
st.set_page_config(
    page_title="ChatApp",
    page_icon=" ",
    layout="wide",
)
st.title(" Gemma Chat Program")

# 给对话增加history属性，将历史对话信息储存下来
if "history" not in st.session_state:
    st.session_state.history = []

# 显示历史信息
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Chat with Gemma: "):
    # 在页面上显示用户的输入
    with st.chat_message(role):
        st.markdown(user_input)
    content = user_input
    m = {'role': role, 'content': content}
    # get_response_material用来获取模型生成的回复，这个是需要根据自己的情况去实现
    # response为大模型生成的回复，material为RAG的检索的内容
    st.session_state.history.append(m)
    response = ollama.chat(model='gemma:2b', messages=st.session_state.history)
    # st.session_state.history.append(response['message'])

    # 将用户的输入加入历史
    # st.session_state.history.append({"role": role, "content": user_input})
    # 在页面上显示模型生成的回复
    with st.chat_message("assistant"):
        st.markdown(response['message']['content'])
    # 将模型的输出加入到历史信息中
    st.session_state.history.append({"role": 'assistant', "content": response['message']['content']})

    # 只保留十轮对话，这个可根据自己的情况设定，我这里主要是会把history给大模型，context有限，轮数不能太多
    if len(st.session_state.history) > 20:
        st.session_state.messages = st.session_state.messages[-20:]