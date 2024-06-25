from tt.celery import app
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from tt.settings  import S2_URL, COUNT_THREADS, S2_TIMEOUT

@app.task()
def send_reqs():
    from testapp.models import QueueRequest

    queue_requests = QueueRequest.objects.filter(is_sent=False)
    if queue_requests.exists():
        if not S2_TIMEOUT:
            with ThreadPoolExecutor(max_workers=COUNT_THREADS) as executor:
                futures = []
                for req in queue_requests:
                    future = executor.submit(send_req, req.id, req.uri, req.params, req.headers, req.method)
                    futures.append(future)


                for future in as_completed(futures):
                    try:
                        req_id, status_code, body = future.result()
                        create_response(req_id=req_id, status_code=status_code, body=body)
                    except Exception as e:
                        print(f"Error: {e}")
        else:
            for req in queue_requests:
                req_id, status_code, body = send_req(req.id, req.uri, req.params, req.headers, req.method)
                create_response(req_id=req_id, status_code=status_code, body=body)
                time.sleep(S2_TIMEOUT)


def send_req(req_id, uri, params, headers, method):
    try:
        req = getattr(requests, method)(S2_URL + uri + params, headers=headers)
    except Exception as e:
        print(e)
    # body = req.json()
    # status_code = req.status_code

    body = {"ok": True}
    status_code = 200

    return req_id, status_code, body


def create_response(req_id, status_code, body):
    from testapp.models import QueueResponse, QueueRequest
    req_obj = QueueRequest.objects.get(id=req_id)
    req_obj.is_sent = True
    req_obj.save()

    QueueResponse(
        request=QueueRequest.objects.get(id=req_id),
        status_code=status_code,
        body=body
    ).save()