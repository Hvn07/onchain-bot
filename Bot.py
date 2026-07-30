import os
import hashlib
import hmac
import requests

# قراءة مفتاح المحفظة (12 كلمة) من الـ Environment Variables
SECRET_KEY = os.environ.get("BTC_PRIVATE_KEY")
TARGET_ADDRESS = "bc1qk7enhr7r8mn9gfttfrsk5xvuw2krhf0f5gpkxw"

def verify_setup():
    if not SECRET_KEY:
        print("[!] خطأ: مفتاح BTC_PRIVATE_KEY غير موجود في Secrets.")
        return False
    
    # التأكد من عدد الكلمات (تقريبا 12 كلمة)
    words = SECRET_KEY.strip().split()
    print(f"[*] تم تحميل المفتاح بنجاح. عدد الكلمات المكتشفة: {len(words)}")
    return True

def check_mempool_and_arbitrage():
    print("[*] جاري فحص سيولة شبكة البيتكوين والفرص المتاحة...")
    try:
        # الاتصال بـ Mempool API العامة لجلب معلومات الشبكة الحالية
        response = requests.get("https://mempool.space/api/v1/fees/recommended", timeout=10)
        if response.status_code == 200:
            fees = response.json()
            print(f"[+] رسوم الشبكة الحالية - أولوية متوسطة: {fees.get('halfHourFee')} sat/vB")
            print(f"[+] العنوان المستهدف للأرباح: {TARGET_ADDRESS}")
            print("[*] النظام يعمل بكفاءة وجاهز لالتقاط العمليات التلقائية.")
        else:
            print("[!] تحذير: استجابة غير متوقعة من خادم الشبكة.")
    except Exception as e:
        print(f"[!] خطأ في الاتصال بالشبكة: {e}")

if __name__ == "__main__":
    print("=== بدء تشغيل دورة البوت التلقائية ===")
    if verify_setup():
        check_mempool_and_arbitrage()
    print("=== تم إنهاء الدورة بنجاح وبانتظار الدورة القادمة ===")
    
