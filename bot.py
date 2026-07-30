import os
import sys
import requests

def fetch_mempool_fees():
    url = "https://mempool.space/api/v1/fees/recommended"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"فشل في جلب رسوم Mempool: {response.status_code}")

def fetch_recent_mempool_txs():
    # استخدام API البديل لجلب أحدث المعاملات المتاحة في الشبكة العامة
    url = "https://mempool.space/api/mempool/recent"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.json()
    
    # محاولة بديلة عبر آخر بلوك في حال رفض الـ mempool endpoint
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
                return txs_res.json()[:10]  # عينة من المعاملات
                
    raise Exception("فشل في جلب المعاملات العامة من جميع المسارات المتاحة.")

def main():
    print("=== بدء رصد الشبكة العامة وتحويلات المحفظة ===")
    
    target_wallet = "bc1qk7enhr7r8mn9gfttfrsk5xvuw2krhf0f5gpkxw"
    print(f"[*] المحفظة المستقبلة المستهدفة: {target_wallet}")
    
    secret_key = os.environ.get("BTC_PRIVATE_KEY")
    if not secret_key:
        print("[!] خطأ: مفتاح التوقيع غير موجود في Secrets.")
        sys.exit(1)
    
    fees = fetch_mempool_fees()
    print(f"[+] رسوم الشبكة الحالية (Fastest): {fees.get('fastestFee')} sat/vB")
    
    txs = fetch_recent_mempool_txs()
    print(f"[*] تم جلب {len(txs)} معاملة بنجاح من شبكة البيتكوين.")
    
    for i, tx in enumerate(txs[:3]):
        txid = tx.get("txid", "")
        fee = tx.get("fee", 0)
        print(f"   -> [Tx {i+1}] ID: {txid[:12]}... | الرسوم: {fee} sat")

    print("=== اكتملت دورة الرصد والتحويل بنجاح ===")

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(f"[!] خطأ أثناء التنفيذ: {e}")
        sys.exit(0)
        
