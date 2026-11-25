# AlansarPrices

برنامج سطح مكتب بسيط لعرض أسعار مطبوعات الأنصار، مبني باستخدام Python وTkinter.

## البناء التلقائي

يستخدم المستودع GitHub Actions لبناء نسختين مستقلتين من نفس المصدر:

- **Windows:** ملف `AlansarPrices.exe`.
- **Linux:** ملف تنفيذي باسم `AlansarPrices`.

يبدأ البناء تلقائيًا عند كل تحديث يُرفع إلى فرع `main`، ويمكن تشغيله يدويًا من تبويب **Actions** باختيار **Build AlansarPrices** ثم **Run workflow**.

بعد انتهاء البناء بنجاح، افتح تفاصيل التشغيل ونزّل أحد الملفين من قسم **Artifacts**:

- `AlansarPrices-Windows`
- `AlansarPrices-Linux`

## البناء محليًا على Windows

1. ثبّت Python 3.12 أو إصدارًا متوافقًا.
2. افتح مجلد المشروع.
3. شغّل `build.bat`.
4. ستجد الملف التنفيذي داخل مجلد `dist`.

## المتطلبات

البرنامج نفسه يعتمد على مكتبات Python القياسية وTkinter. أما `requirements-build.txt` فيحتوي على أدوات البناء فقط: PyInstaller وPillow.

## ملاحظات

- يجب بناء كل نظام على بيئة تشغيل من نفس نوعه؛ لذلك يستخدم GitHub Actions عامل Windows وعامل Linux منفصلين.
- ملف `icon.png` هو مصدر الأيقونة، وملف `icon.ico` يُستخدم لأيقونة تطبيق Windows.
- لا ترفع كلمات مرور أو مفاتيح API أو بيانات اعتماد إلى المستودع.
