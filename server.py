from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import ollama

app = FastAPI(title="AI Dataset Processing API")

# تحديد هيكل البيانات المستقبلة في الطلب (Request Body)
class ProcessRequest(BaseModel):
    text_value: str
    custom_instruction: str
    model_name: str = "llama3.2"

@app.post("/process-row")
async def process_row(request: ProcessRequest):
    """
    مقبس (Endpoint) لمعالجة صف واحد من البيانات عبر نموذج Ollama
    """
    prompt = f"""
    أنت مساعد ذكي لتحليل وتنظيف البيانات. لديك هذا النص من عمود جدول:
    "{request.text_value}"
    
    التعليمات المطلوبة:
    {request.custom_instruction}
    
    أرجع النتيجة المختصرة والمناسبة لتوضع مباشرة في جدول بيانات دون إضافات زائدة.
    """
    try:
        response = ollama.chat(
            model=request.model_name,
            messages=[{"role": "user", "content": prompt}]
        )
        return {"result": response["message"]["content"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # تشغيل السيرفر المحلي على المنفذ 8000
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
