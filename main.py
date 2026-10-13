import os
import ollama


def process_text_file(
    input_path="input_sample.txt",
    output_path="formatted_output.txt",
    model_name="llama3.2",
):
  if not os.path.exists(input_path):
    print(f"Error: The file {input_path} was not found.")
    return

  with open(input_path, "r", encoding="utf-8") as f:
    input_text = f.read()

  # تقسيم النص وتصفية الفراغات
  paragraphs = [p.strip() for p in input_text.split("-------") if p.strip()]
  processed_paragraphs = []

  print(f"Processing {len(paragraphs)} paragraphs using {model_name}...")

  for index, para in enumerate(paragraphs, start=1):
    prompt = f"""
        أنت مساعد ذكي لتهيئة وتنظيم النصوص. لديك هذه الفقرة:
        "{para}"
        
        المطلوب منك:
        1. إعطاء رقم تسلسلي لهذه الفقرة وهو: {index}
        2. إعطاء معرف فريد (ID) لهذه الفقرة.
        3. التأكد من توفر النص باللغتين العربية والإنجليزية مع وضع الكلمتين "Arabic:" و "English:" بوضوح أمام كل نسخة داخل الفقرة.
        
        أرجع النتيجة بالنسق التالي فقط دون أي مقدمات:
        ID: para_{index}
        Number: {index}
        Arabic: [النص بالعربية هنا]
        English: [النص بالإنجليزية هنا]
        -------
        """

    try:
      response = ollama.chat(
          model=model_name, messages=[{"role": "user", "content": prompt}]
      )
      result = response["message"]["content"]
      processed_paragraphs.append(result)
      print(f"[✓] Processed paragraph {index}")
    except Exception as e:
      print(f"[✗] Error processing paragraph {index}: {e}")

  final_output = "\n-------\n".join(processed_paragraphs)

  with open(output_path, "w", encoding="utf-8") as f:
    f.write(final_output)

  print(f"\nDone! Results saved to {output_path}")


if name == "main":
  process_text_file()
