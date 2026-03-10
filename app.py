import streamlit as st
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage

from chatbot_with_memory import graph,config
st.subheader('chatbot',divider='rainbow')
if 'messages' not in st.session_state:
    st.session_state['messages']=[]



for msg in st.session_state['messages']:
    if isinstance(msg,SystemMessage):
        continue
    elif isinstance(msg,HumanMessage):
        with st.chat_message('user'):
            st.markdown(msg.content)
    elif isinstance(msg,AIMessage):
        with st.chat_message('ai'):
            st.markdown(msg['messages'][-1].content)

if prompt:=st.chat_input():
    with st.chat_message('user'):
        st.markdown(prompt)
    response=graph.invoke({'messages':HumanMessage(content=prompt)},config=config)
    ai_msg = response["messages"][-1].content
    with st.chat_message('ai'):
        st.markdown(ai_msg)



