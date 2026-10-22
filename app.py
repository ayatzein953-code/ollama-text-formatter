import streamlit as st
import pandas as pd
import requests

st.title("🤖 نظام الوكيل الذكي (AI Agent) لتنظيف وتحليل البيانات")

server_url = "http://127.0.0.1:8000/agent-process"

# رفع الملف
uploaded_file = st.file_uploader("قم برفع ملف الـ CSV الخاص بك:", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("📋 معاينة البيانات الأصلية:")
    st.dataframe(df.head())

    st.sidebar.header("🛠️ إعدادات الوكيل الذكي (Agent Config)")
    
    # تفاعل الوكيل الذكي مع المستخدم
    use_rag = st.sidebar.checkbox("🤖 هل تريد استخدام قواعد التنظيف المخزنة في نظام الـ RAG؟")
    
    rag_topic = "customer_support"
    custom_instruction = ""
    
    if use_rag:
        rag_topic = st.sidebar.selectbox("اختر نوع القواعد من الـ RAG:", ["customer_support", "financial"])
        st.sidebar.info(f"سيتم سحب القواعد تلقائياً من نظام الـ RAG الخاص بـ: {rag_topic}")
    else:
        custom_instruction = st.sidebar.text_area("أدخل تعليمات التنظيف الخاصة بك:", "قم بتصحيح الأخطاء وإزالة الفراغات الزائدة.")

    text_column = st.sidebar.selectbox("اختر العمود النصي للمعالجة الذكية:", df.columns)

    # --- خيارات أداة Pandas المتقدمة ---
    st.sidebar.subheader("⚙️ خوات أداة Pandas الهيكلية")
    handle_nulls = st.sidebar.checkbox("معالجة القيم الفارغة (Missing Values)")
    null_strategy = "fill"
    if handle_nulls:
        null_strategy = st.sidebar.selectbox("طريقة المعالجة:", ["ملء بقيمة محددة (Unknown)", "حذف الصفوف الفارغة (Drop)"])

    if st.button("🚀 تشغيل الوكيل الذكي لتنفيذ المعالجة", type="primary"):
        with st.spinner("الوكيل الذكي يقوم بتنسيق الأدوات وتطبيق التنظيف..."):
            
            # 1. تطبيق أدوات Pandas أولاً (بايثون الصرفة)
            if handle_nulls:
                if null_strategy == "حذف الصفوف الفارغة (Drop)":
                    df = df.dropna(subset=[text_column])
                else:
                    df[text_column] = df[text_column].fillna("Unknown")

            # 2. إرسال النصوص للسيرفر لاستخدام نموذج الذكاء الاصطناعي و الـ RAG
            payload = {
                "use_rag": use_rag,
                "rag_topic": rag_topic,
                "custom_instruction": custom_instruction,
                "text_values: df[text_column].astype(str).tolist()
            }

            try:
                response = requests.post(server_url, json=payload)
                if response.status_code == 200:
                    res_data = response.json()
                    df["AI_Agent_Cleaned"] = res_data["ai_processed_texts"]
                    
                    st.success("تمت المعالجة بنجاح عبر تكامل الأدوات (Pandas + RAG + Ollama)! 🎉")
                    st.info(using القواعد التالية: {res_data['rag_instructions_used']})")
                    
                    st.subheader("✨ الجدول بعد التعديل:")
                    st.dataframe(df.head())

                    # زر التحميل
                    csv_data = df.to_csv(index=False).encode("utf-8")
                    st.download_button("📥 تحميل الجدول المحدث نهائياً", csv_data, "agent_processed_data.csv", "mime/csv")
                else:
                    st.error("حدث خطأ في الاتصال بالسيرفر.")
            except Exception as e:
                st.error(f"خطأ تقني: {e}")
