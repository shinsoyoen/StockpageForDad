from .forms import TransactionForm
from .models import TransactionHistory
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)  # 로거 설정 (콘솔 출력용)

def index(request):
    today = datetime.now().date()
    logger.info("💬 [VIEW] index() 호출됨")

    if request.method == 'POST':
        logger.info("📩 POST 요청 감지됨")
        logger.info(f"📄 받은 데이터: {request.POST}")

        form = TransactionForm(request.POST)

        if form.is_valid():
            logger.info("✅ 폼 유효성 검사 통과")
            transaction = form.save(commit=False)
            transaction.date = today
            transaction.save()

            messages.success(request, '✅ 등록이 성공적으로 완료되었습니다!')
            logger.info("🎉 DB 저장 완료")
            return redirect('index')
        else:
            logger.warning("⚠️ 폼 유효성 검사 실패")
            logger.warning(f"📌 오류 내용: {form.errors}")
            messages.error(request, '⚠️ 모든 항목을 작성해주세요.')
    else:
        logger.info("🟢 GET 요청 처리 중")
        form = TransactionForm(initial={'trans_date': today})

    data = TransactionHistory.objects.all().order_by('-trans_date')

    context = {
        'form': form,
        'today': today,
        'data': data
    }

    return render(request, 'users/trade_list.html', context)
