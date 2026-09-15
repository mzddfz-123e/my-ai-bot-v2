import os
import streamlit as st
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI

st.set_page_config(
    page_title="المساعد الذكي الشامل",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
    <style>
    .main { direction: rtl; text-align: right; }
    stChatMessage { direction: rtl; text-align: right; }
    .designer-tag {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        color: #155724;
        background-color: #d4edda;
        padding: 12px;
        border-radius: 10px;
        margin-bottom: 25px;
        border: 1px solid #c3e6cb;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="designer-tag">✨ صانعي وبكل فخر محمد علاء بن زايد ✨</div>', unsafe_allow_html=True)

st.title("🤖 المساعد الذكي الشامل")
st.caption("ذكاء اصطناعي مخصص للإجابة عن أسئلتك والبحث في الإنترنت عند الحاجة")

with st.sidebar:
    st.header("⚙️ الخيارات")
    if st.button("مسح السجل / محادثة جديدة"):
        st.session_state.messages = []
        st.rerun()

raw_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY", "")
api_key = str(raw_key).strip().encode("ascii", "ignore").decode("ascii")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("اكتب سؤالك هنا...")

if user_input:
    if not api_key:
        st.error("لم يتم العثور على مفتاح API صحيح في إعدادات Secrets.")
    else:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        try:
            # تم تحديد اسم النموذج المسجل رسمياً لدى API
            llm = ChatGoogleGenerativeAI(
                model="models/gemini-1.5-flash", 
                google_api_key=api_key,
                temperature=0.3
            )
            
            with st.chat_message("assistant"):
                with st.spinner("جاري التفكير وتوليد الإجابة..."):
                    if "بحث" in user_input or "ابحث" in user_input:
                        search = DuckDuckGoSearchRun()
                        search_results = search.run(user_input)
                        prompt = f"بناءً على نتائج البحث التالية: {search_results}\n\nأجب عن السؤال التالي باللغة العربية: {user_input}"
                        response = llm.invoke(prompt)
                    else:
                        response = llm.invoke(user_input)
                    
                    answer = response.content
                    st.markdown(answer)

            st.session_state.messages.append({"role": "assistant", "content": answer})

        except Exception as e:
            st.error(f"حدث خطأ أثناء معالجة الطلب: {e}")
