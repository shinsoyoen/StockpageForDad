from .forms import TransactionForm
from .models import TransactionHistory
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib import messages
from django.http import JsonResponse
import logging
from django.shortcuts import get_object_or_404
from django.shortcuts import render

logger = logging.getLogger(__name__)

def index(request):
    user_email = request.session.get("user_email")
    today = datetime.now().date()
    logger.info("💬 [VIEW] index() 호출됨")

    if request.method == 'POST':
        logger.info("📩 POST 요청 감지됨")
        logger.info(f"📄 받은 데이터: {request.POST}")

        mode = request.POST.get('mode')
        trade_id = request.POST.get('trade_id')

        if mode == 'update':
            logger.info(f"🔄 업데이트 모드 감지됨 - trade_id: {trade_id}")
            try:
                transaction = TransactionHistory.objects.get(trade_id=trade_id)
                transaction.category = request.POST.get('category')
                transaction.price = request.POST.get('price')
                transaction.quantity = request.POST.get('quantity')
                transaction.memo = request.POST.get('memo')
                transaction.date = today
                transaction.save()
                messages.success(request, '✅ 거래 정보가 성공적으로 수정되었습니다!')
                logger.info(f"🎉 trade_id {trade_id} 업데이트 완료")
                return redirect('index')
            except TransactionHistory.DoesNotExist:
                messages.error(request, '⚠️ 수정하려는 거래 정보를 찾을 수 없습니다.')
                logger.warning(f"⚠️ trade_id {trade_id}에 해당하는 거래 정보 없음")

        else:
            logger.info("➕ 등록 모드 감지됨")
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

    data = TransactionHistory.objects.all().order_by('-trans_date', '-trade_id')

    context = {
        "user_email": user_email,
        'form': form,
        'today': today,
        'data': data
    }

    return render(request, 'board/board.html', context)

def delete_transaction(request, trade_id):
    if request.method == 'POST':
        TransactionHistory.objects.filter(trade_id=trade_id).delete()
        return JsonResponse({'success': True})

def delete_trade(request, trade_id):
    if request.method == 'POST':
        trade = get_object_or_404(TransactionHistory, pk=trade_id)
        trade.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

class Meta:
    db_table = 'transaction_History'
    managed = False