# transaction_History/views.py

from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from . import transaction_History

@require_POST
def delete_item(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        ids_to_delete = data.get('ids', [])

        # 데이터베이스에서 해당 ID들을 삭제하는 로직
        transaction_History.objects.filter(id__in=ids_to_delete).delete()

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)