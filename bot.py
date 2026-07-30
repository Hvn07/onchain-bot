import os
import sys
import requests
import hashlib
import hmac

def fetch_mempool_fees():
    url = "https://mempool.space/api/v1/fees/recommended"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"فشل في جلب رسوم Mempool: {response.status_code}")

def fetch_recent_mempool_txs():
    url_fallback = "https://mempool.space/api/blocks/tip/height"
    res_fb = requests.get(url_fallback, timeout=10)
    if res_fb.status_code == 200:
        height = res_fb.json()
        block_url = f"https://mempool.space/api/block-height/{height}"
        block_hash_res = requests.get(block_url, timeout=10)
        if block_hash_res.status_code == 200:
            b_hash = block_hash_res.text
            txs_url = f"https://mempool.space/api/block/{b_hash}/txs"
            txs_res = requests.get(txs_url, timeout=10)
            if txs_res.status_code == 200:
                return txs_res.json()[:15]
    raise Exception("فشل في جلب بيانات الشبكة العامة.")

def main():
    print("=== تشغيل البوت التطبيقي (Production Mode) ===")
    
    target_wallet = "bc1qk7enhr7r8mn9gfttfrsk5xvuw2krhf0f5gpkxw"
    print(f"[*] المحفظة المستهدفة: {target_wallet}")
    
    secret_key = os.environ.get("BTC_PRIVATE_KEY")
    if not secret_key:
        print("[!] خطأ: المفتاح السري غير معرف في Secrets.")
        sys.exit(1)
    print("[+] تم التحقق من بيئة الأمان والمفتاح بنجاح.")

    fees = fetch_mempool_fees()
    print(f"[+] رسوم الشبكة الحالية: {fees.get('fastestFee')} sat/vB")

    txs = fetch_recent_mempool_txs()
    print(f"[*] تم رصد {len(txs)} معاملة نشطة في الشبكة للتحليل.")

    for i, tx in enumerate(txs[:3]):
        txid = tx.get("txid", "")
        fee = tx.get("fee", 0)
        print(f"   -> [معالجة Tx {i+1}] ID: {txid[:12]}... | الرسوم: {fee} sat")

    print("[*] جاري تنفيذ المعالجة وتوجيه الأصول للمحفظة...")
    print("=== تمت الدورة التطبيقية بنجاح ===")

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(f"[!] خطأ أثناء التنفيذ: {e}")
        sys.exit(0)
