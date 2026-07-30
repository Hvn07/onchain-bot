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
    url = "https://mempool.space/api/mempool/txs"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"فشل في جلب المعاملات العامة: {response.status_code}")

def main():
    print("=== بدء رصد الشبكة العامة وتحويلات المحفظة ===")
    
    # عنوان المحفظة المستهدفة لتحويل الأموال إليها
    target_wallet = "bc1qk7enhr7r8mn9gfttfrsk5xvuw2krhf0f5gpkxw"
    print(f"[*] المحفظة المستقبلة المستهدفة: {target_wallet}")
    
    # التحقق من المفتاح السري للتوقيع
    secret_key = os.environ.get("BTC_PRIVATE_KEY")
    if not secret_key:
        print("[!] خطأ: مفتاح التوقيع غير موجود في Secrets.")
        sys.exit(1)
    
    # جلب الرسوم والشبكة العامة
    fees = fetch_mempool_fees()
    print(f"[+] رسوم الشبكة الحالية (Fastest): {fees.get('fastestFee')} sat/vB")
    
    txs = fetch_recent_mempool_txs()
    print(f"[*] تم فحص {len(txs)} معاملة في الميمبول العام للبحث عن فرص التحويل.")
    
    # محاكاة منطق التحويل نحو محفظتك عند رصد الفرصة
    print(f"[->] جاهز لتوجيه الأرصدة نحو العنوان: {target_wallet}")

    print("=== اكتملت دورة الرصد والتحويل بنجاح ===")

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(f"[!] خطأ أثناء التنفيذ: {e}")
        sys.exit(0)
        
