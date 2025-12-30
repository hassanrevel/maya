import streamlit as st
from langchain_core.messages import HumanMessage
from maya_agent import Maya, config

st.set_page_config(page_title="Maya - Hospital Receptionist", page_icon="🏥")

st.title("🏥 Maya - Your Hospital Receptionist")
st.write("Ask me about hospital services, departments, doctors, or book an appointment!")

# Initialize chat history in Streamlit session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# User input box
if user_input := st.chat_input("Type your message here..."):
    # Save user input
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Run Maya
    result = Maya.invoke(
        {"messages": [HumanMessage(content=user_input)]},
        config=config
    )

    ai_response = result["messages"][-1].content

    # Save AI response
    st.session_state.messages.append({"role": "assistant", "content": ai_response})
    st.chat_message("assistant").write(ai_response)
