import ollama
import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="AI Text Formatter & Translator", page_icon="🤖", layout="wide"
)

st.title("🤖 Local AI Text Formatter & Translator")
st.markdown(
    "قم برفع ملفك النصي، وحدد نوع التعديل أو التنسيق الذي تريده، وسيقوم الذكاء"
    " الاصطناعي بمعالجته محلياً باستخدام Ollama."
)

# الشريط الجانبي لإعدادات المستخدم
st.sidebar.header("⚙️ إعدادات المستخدم")
model_name = st.sidebar.selectbox(
    "اختر نموذج الذكاء الاصطناعي (Model):",
    ["llama3.2", "llama3", "mistral", "gemma"],
)
separator = st.sidebar.text_input(
    "فاصل الفقرات (Separator):", value="-------"
)

# خيارات التعديل المخصصة للمستخدم
st.sidebar.subheader("✍️ تخصيص التوجيه (Prompt Customization)")
custom_instruction = st.sidebar.text_area(
    "ما هو التعديل أو التنسيق الذي تريده على النصوص؟",
    value=(
        "1. إعطاء رقم تسلسلي للفقرة.\n2. التأكد من توفر النص باللغتين العربية"
        " والإنجليزية مع وضع Arabic: و English: بوضوح."
    ),
    height=150,
)

# منطقة رفع الملف
uploaded_file = st.file_uploader(
    "اختر ملف النص (TXT)", type=["txt"], help="يجب أن تكون الفقرات مفصولة بالفاصل المحدد"
)

if uploaded_file is not None:
  # قراءة الملف المرفوع
  input_text = uploaded_file.read().decode("utf-8")

  st.subheader("📄 النص الأصلي المستخرج:")
  st.text_area(
      "محتوى الملف:", input_text, height=150, disabled=True
  )

  if st.button("🚀 بدء المعالجة والتنسيق", type="primary"):
    paragraphs = [
        p.strip() for p in input_text.split(separator) if p.strip()
    ]
    processed_paragraphs = []

    progress_bar = st.progress(0)
    status_text = st.empty()

    for index, para in enumerate(paragraphs, start=1):
      status_text.text(
          f"جاري معالجة الفقرة {index} من {len(paragraphs)}..."
      )

      # بناء الموجه بناءً على رغبة المستخدم
      prompt = f"""
            أنت مساعد ذكي لتهيئة وتنظيم النصوص. لديك هذه الفقرة:
            "{para}"
            
            التعليمات المطلوبة منك بدقة:
            {custom_instruction}
            
            أرجع النتيجة بالنسق المطلوب فقط دون أي مقدمات إضافية.
            رقم الفقرة الحالي هو: {index}
            -------
            """

      try:
        response = ollama.chat(
            model=model_name, messages=[{"role": "user", "content": prompt}]
        )
        result = response["message"]["content"]
        processed_paragraphs.append(result)
      except Exception as e:
        processed_paragraphs.append(
            f"Error processing paragraph {index}: {e}"
        )

      progress_bar.progress(index / len(paragraphs))

    status_text.text("تم الانتهاء من المعالجة بنجاح! 🎉")
    final_output = f"\n{separator}\n".join(processed_paragraphs)

    st.subheader("✨ النتيجة النهائية:")
    st.text_area("النتيجة:", final_output, height=250)

    # زر لتحميل الملف الناتج
    st.download_button(
        label="📥 تحميل الملف الناتج (Formatted Output)",
        data=final_output,
        file_name="formatted_output.txt",
        mime="text/plain",
    )
