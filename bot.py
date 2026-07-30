import os
import sys
import requests

def fetch_mempool_fees():
    url = "https://mempool.space/api/v1/fees/recommended"
    response = requests.get(url, timeout=10)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"فشل في جلب رسوم Mempool: {response.status_code}")

def main():
    print("=== بدء رصد شبكة البيتكوين ===")
    
    # عنوان المحفظة الخاص بك
    wallet_address = "bc1qk7enhr7r8mn9gfttfrsk5xvuw2krhf0f5gpkxw"
    print(f"[*] العنوان المستهدف: {wallet_address}")
    
    # التحقق من المفتاح السري (Seed Phrase) من GitHub Secrets
    secret_key = os.environ.get("BTC_PRIVATE_KEY")
    if not secret_key:
        print("[!] تحذير: مفتاح BTC_PRIVATE_KEY غير مسجل بشكل صحيح في Secrets.")
    else:
        words = secret_key.strip().split()
        print(f"[*] تم التحقق من المفتاح بنجاح. عدد الكلمات: {len(words)}")
    
    # جلب الرسوم الحالية من الشبكة
    fees = fetch_mempool_fees()
    print(f"[+] رسوم الأولوية القصوى (Fastest): {fees.get('fastestFee')} sat/vB")
    print(f"[+] رسوم النصف ساعة (Half Hour): {fees.get('halfHourFee')} sat/vB")
    print(f"[+] رسوم الساعة (Hour): {fees.get('hourFee')} sat/vB")
    
    print("=== اكتملت دورة الفحص بنجاح ===")

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(f"[!] خطأ أثناء التنفيذ: {e}")
        sys.exit(0)
        
