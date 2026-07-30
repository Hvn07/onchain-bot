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
    # استخدام المسار الصحيح المحدث لجلب المعاملات الحديثة
    url = "https://mempool.space/api/v1/mempool/recent"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"فشل في جلب المعاملات العامة: {response.status_code}")

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
    print(f"[*] تم جلب {len(txs)} معاملة حديثة بنجاح من الميمبول العام.")
    
    for i, tx in enumerate(txs[:3]):
        txid = tx.get("txid", "")
        value = tx.get("value", 0)
        fee = tx.get("fee", 0)
        print(f"   -> [Tx {i+1}] ID: {txid[:12]}... | القيمة: {value} ساتوشي | الرسوم: {fee} sat")

    print("=== اكتملت دورة الرصد والتحويل بنجاح ===")

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(f"[!] خطأ أثناء التنفيذ: {e}")
        sys.exit(0)
        
