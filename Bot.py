import os
import sys

def main():
    print("=== فحص مفتاح المحفظة ===")
    
    secret_key = os.environ.get("BTC_PRIVATE_KEY")
    
    if not secret_key:
        print("[!] خطأ قاتل: المتغير BTC_PRIVATE_KEY فارغ أو غير موجود في GitHub Secrets!")
        sys.exit(1)
        
    # تنظيف الفراغات الزائدة
    cleaned_key = " ".join(secret_key.strip().split())
    words = cleaned_key.split()
    
    print(f"[+] عدد الكلمات المستخرجة: {len(words)}")
    
    if len(words) != 12:
        print(f"[!] تحذير: عدد الكلمات هو {len(words)}، المفتاح القياسي يجب أن يتكون من 12 كلمة!")
    else:
        print("[+] عدد الكلمات صحيح (12 كلمة). المفتاح مقروء بنجاح.")
        
    print("=== انتهى الفحص بنجاح ===")

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(f"[!] حدث خطأ غير متوقع: {e}")
        sys.exit(0)
