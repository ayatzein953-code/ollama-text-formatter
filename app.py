 import io
import ollama
import pandas as pd
import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="Local AI Data & Text Processor", page_icon="📊", layout="wide"
)

st.title("📊 Local AI Data & Text Pipeline Processor")
st.markdown(
    "أداة محلية متقدمة لمعالجة وتحليل النصوص والبيانات باستخدام نماذج الذكاء"
    " الاصطناعي عبر Ollama لضمان الخصوصية وسرعة الأداء."
)

# الشريط الجانبي للإعدادات
st.sidebar.header("⚙️ إعدادات النموذج")
model_name = st.sidebar.selectbox(
    "اختر نموذج الذكاء الاصطناعي:", ["llama3.2", "llama3", "mistral", "gemma"]
)

st.sidebar.subheader("✍️ تخصيص التعليمات (Prompt)")
custom_instruction = st.sidebar.text_area(
    "ما هو التعديل أو التحليل المطلوب على النصوص؟",
    value=(
        "1. تلخيص أو تنظيف النص المدخل.\n2. ترجمته إلى اللغتين العربية"
        " والإنجليزية.\n3. تصحيح أي أخطاء لغوية."
    ),
    height=140,
)

# اختيار نوع الملف
file_type = st.radio(
    "اختر نوع الملف المراد معالجته:", ("ملف نصي (TXT)", "ملف بيانات (CSV)")
)

if file_type == "ملف نصي (TXT)":
  # خيارات تقسيم النص الذكية
  split_method = st.selectbox(
      "طريقة تقسيم النص في الملف:",
      (
          "حسب الأسطر الفارغة تلقائياً (Paragraphs / \\n\\n)",
          "باستخدام فاصل مخصص (Custom Separator)",
      ),
  )

  if split_method == "باستخدام فاصل مخصص (Custom Separator)":
    separator = st.text_input("أدخل الفاصل المستخدم:", value="-------")
  else:
    separator = "\n\n"

  uploaded_file = st.file_uploader("اختر ملف TXT", type=["txt"])

  if uploaded_file is not None:
    input_text = uploaded_file.read().decode("utf-8")
    st.subheader("📄 معاينة النص الأصلي:")
    st.text_area("المحتوى:", input_text, height=120, disabled=True)

    if st.button("🚀 بدء المعالجة", type="primary"):
      if split_method == "باستخدام فاصل مخصص (Custom Separator)":
        paragraphs = [p.strip() for p in input_text.split(separator) if p.strip()]
      else:
        paragraphs = [p.strip() for p in input_text.split("\n\n") if p.strip()]

      processed_results = []
      progress_bar = st.progress(0)
      status_text = st.empty()

      for i, para in enumerate(paragraphs, start=1):
        status_text.text(f"جاري معالجة العنصر {i} من {len(paragraphs)}...")
        prompt = f"""
                أنت مساعد ذكي لتحليل النصوص. لديك هذا النص:
                "{para}"
                
                التعليمات المطلوبة:
                {custom_instruction}
                
                أرجع النتيجة بصيغة واضحة ومرتبة فقط.
                """
        try:
          response = ollama.chat(
              model=model_name, messages=[{"role": "user", "content": prompt}]
          )
          processed_results.append(response["message"]["content"])
        except Exception as e:
          processed_results.append(f"Error: {e}")
        progress_bar.progress(i / len(paragraphs))

      status_text.text("اكتملت المعالجة بنجاح! 🎉")

      if split_method == "باستخدام فاصل مخصص (Custom Separator)":
        final_output = f"\n{separator}\n".join(processed_results)
      else:
        final_output = "\n\n".join(processed_results)

      st.subheader("✨ النتائج المعالجة:")
      st.text_area("النتيجة النهائية:", final_output, height=200)

      st.download_button(
          "📥 تحميل الملف الناتج",
          final_output,
          file_name="processed_output.txt",
          mime="text/plain",
      )

else:  # ملف CSV
  uploaded_csv = st.file_uploader("اختر ملف CSV", type=["csv"])

  if uploaded_csv is not None:
    df = pd.read_csv(uploaded_csv)
    st.subheader("📊 معاينة جدول البيانات الأصلي:")
    st.dataframe(df.head())

    text_column = st.selectbox(
        "اختر عمود النصوص المراد معالجته بالذكاء الاصطناعي:", df.columns
    )

    if st.button("🚀 بدء معالجة بيانات الجدول", type="primary"):
      processed_column = []
      progress_bar = st.progress(0)
      status_text = st.empty()
      for i, text_val in enumerate(df[text_column]):
        status_text.text(f"جاري معالجة الصف {i+1} من {len(df)}...")
        prompt = f"""
                أنت مساعد ذكي لتحليل وتنظيف البيانات. لديك هذا النص من عمود جدول:
                "{str(text_val)}"
                
                التعليمات المطلوبة:
                {custom_instruction}
                
                أرجع النتيجة المختصرة والمناسبة لتوضع مباشرة في جدول بيانات دون إضافات زائدة.
                """
        try:
          response = ollama.chat(
              model=model_name, messages=[{"role": "user", "content": prompt}]
          )
          processed_column.append(response["message"]["content"])
        except Exception as e:
          processed_column.append(f"Error: {e}")
        progress_bar.progress((i + 1) / len(df))

      status_text.text("اكتملت معالجة الجدول بنجاح! 🎉")

      df["AI_Processed_Result"] = processed_column

      st.subheader("✨ جدول البيانات بعد المعالجة:")
      st.dataframe(df.head())

      csv_buffer = df.to_csv(index=False).encode("utf-8")
      st.download_button(
          "📥 تحميل جدول البيانات المعدل (CSV)",
          csv_buffer,
          file_name="processed_dataset.csv",
          mime="text/csv",
      )
