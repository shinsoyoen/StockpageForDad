from .forms import TransactionForm
from .models import TransactionHistory
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from django.http import JsonResponse
import logging

logger = logging.getLogger(__name__)

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

    data = TransactionHistory.objects.all().order_by('-trans_date', '-trade_id')  # 최신순 정렬


    context = {
        'form': form,
        'today': today,
        'data': data
    }

    return render(request, 'users/trade_list.html', context)

def delete_transaction(request, trade_id):
    if request.method == 'POST':
        TransactionHistory.objects.filter(trade_id=trade_id).delete()
        return JsonResponse({'success': True})
