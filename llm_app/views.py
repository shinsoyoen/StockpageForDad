from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import google.generativeai as genai
from django.shortcuts import render

def chatbot_page(request):
    return render(request, "llm_app/llm_app.html")

#디버깅 꼭 하기

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

@csrf_exempt
def chat_with_llm(request):
    print("👉 chat_with_llm 뷰 함수 실행됨!")

    if request.method == "POST":
        user_message = request.POST.get("message", "")
        print(f"📩 클라이언트 입력: {user_message}")

        if not user_message:
            print("⚠️ message 값이 비어있음")
            return JsonResponse({"error": "message is required"}, status=400)

        try:
            model = genai.GenerativeModel("gemini-2.0-flash")
            print("✅ Gemini 모델 로드 성공")

            response = model.generate_content(user_message)
            print(f"🤖 모델 응답 원본: {response}")   # 객체 전체 확인
            print(f"💬 모델 응답 텍스트: {response.text}")  # 텍스트만 확인

            return JsonResponse({"reply": response.text})

        except Exception as e:
            print(f"❌ Gemini 호출 중 에러 발생: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    print("⚠️ 잘못된 요청 메서드:", request.method)
    return JsonResponse({"reply": response.text}, json_dumps_params={'ensure_ascii': False})