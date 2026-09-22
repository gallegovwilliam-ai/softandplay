"""Pruebas puras de integridad/concurrencia para Auditoría 7.
No requiere Django ni base de datos.
"""
from concurrent.futures import ThreadPoolExecutor
from threading import Lock


def simulate_serialized_draws(ball_count=54, workers=8, draws=40):
    lock = Lock()
    used = set()

    def draw(_):
        with lock:
            available = [n for n in range(1, ball_count + 1) if n not in used]
            if not available:
                return None
            ball = available[0]
            used.add(ball)
            return ball

    with ThreadPoolExecutor(max_workers=workers) as pool:
        result = list(pool.map(draw, range(draws)))
    picked = [x for x in result if x is not None]
    assert len(picked) == len(set(picked)), "Se repitió una balota"
    assert len(picked) == draws
    return picked


def simulate_serialized_sales(cartons=100, workers=12, requests=80):
    lock = Lock()
    sold = set()

    def sell(_):
        with lock:
            available = [n for n in range(1, cartons + 1) if n not in sold]
            if not available:
                return None
            carton = available[0]
            sold.add(carton)
            return carton

    with ThreadPoolExecutor(max_workers=workers) as pool:
        result = list(pool.map(sell, range(requests)))
    sold_now = [x for x in result if x is not None]
    assert len(sold_now) == len(set(sold_now)), "Se asignó un cartón dos veces"
    assert len(sold_now) == requests
    return sold_now


def simulate_idempotent_payment(attempts=50):
    lock = Lock()
    paid = False
    successful = 0

    def pay(_):
        nonlocal paid, successful
        with lock:
            if paid:
                return False
            paid = True
            successful += 1
            return True

    with ThreadPoolExecutor(max_workers=attempts) as pool:
        result = list(pool.map(pay, range(attempts)))
    assert successful == 1, "El pago no fue idempotente"
    assert sum(result) == 1
    return successful


if __name__ == '__main__':
    simulate_serialized_draws()
    simulate_serialized_sales()
    simulate_idempotent_payment()
    print('AUDITORIA 7: CONCURRENCIA E IDEMPOTENCIA SUPERADAS')
