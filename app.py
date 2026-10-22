import streamlit as st
import pandas as pd
import requests

st.title("📊 أداة معالجة جداول البيانات بالذكاء الاصطناعي")

# إعدادات بسيطة في الواجهة
server_url = "http://127.0.0.1:8000/process-row"
model_name = st.sidebar.selectbox("اختر النموذج:", ["llama3.2", "mistral", "gemma"])
text_column = st.sidebar.text_input("اسم العمود المستهدف:", value="Text")
custom_instruction = st.text_area("التعليمات المخصصة للمُعالجة:", "قم بتلخيص النص واستخراج الكلمات المفتاحية.")

# رفع الملف
uploaded_file = st.file_uploader("قم برفع ملف CSV:", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.dataframe(df.head())

    if st.button("🚀 بدء معالجة بيانات الجدول", type="primary"):
        if text_column not in df.columns:
            st.error(f"العمود '{text_column}' غير موجود في الملف!")
        else:
            processed_column = []
            progress_bar = st.progress(0)
            status_text = st.empty()
            total_rows = len(df)

            for i, text_val in enumerate(df[text_column]):
                status_text.text(f"جاري معالجة الصف {i + 1} من {total_rows}...")
                
                # تجهيز البيانات للتواصل مع السيرفر
                payload = {
                    "text_value": str(text_val),
                    "custom_instruction": custom_instruction,
                    "model_name": model_name
                }
                
                try:
                    # إرسال طلب POST إلى السيرفر
                    res = requests.post(server_url, json=payload)
                    if res.status_code == 200:
                        processed_column.append(res.json()["result"])
                    else:
                        processed_column.append(f"Error: Server responded with status {res.status_code}")
                except Exception as e:
                    processed_column.append(f"Connection Error: {e}")
                
                # تحديث شريط التقدم
                progress_bar.progress((i + 1) / total_rows)

            status_text.text("اكتملت معالجة الجدول بنجاح! 🎉")

            # إضافة النتائج وجدول البيانات
            df["AI_Processed_Result"] = processed_column
            st.subheader("✨ جدول البيانات بعد المعالجة:")
            st.dataframe(df.head())

            # تحميل الملف المعدل
            csv_buffer = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 تحميل جدول البيانات المعدل (CSV)",
                csv_buffer,
                file_name="processed_dataset.csv",
                mime="text/csv",
            )
