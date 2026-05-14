# Skill — ELIRAN Airtable Field Check

## מטרה
למנוע טעויות שנובעות מניחוש שמות שדות, טבלאות, וערכי select ב-Airtable.

## מתי להשתמש
- לפני שינוי ב-`airtable_client.py`
- לפני חיבור שדה חדש ל-template
- לפני הוספת route או query חדש
- לפני שינוי במסכי לקוחות, מלאי, הצעות מחיר, הזמנות או PDF

## עקרונות חובה
- לא מנחשים שמות שדות.
- לא מנחשים שם טבלה.
- לא מנחשים ערכי select.
- לא בונים UI על בסיס שדה שלא אומת.
- Airtable הוא מקור האמת.

## צ'ק ליסט
1. לזהות את הישות העסקית הרלוונטית.
2. לזהות את הטבלה המתאימה ב-Airtable.
3. לאמת את שם השדה המדויק.
4. לבדוק אם מדובר ב:
   - text
   - select
   - linked record
   - lookup
   - formula
   - rollup
5. לבדוק אם הערך מוחזר כ-string, list, או מבנה אחר.
6. לוודא שה-backend וה-template משתמשים באותו שם.
7. לוודא שאין החלפה שקטה בין `שם`, `Name`, ו-`שם לקוח`.

## דוגמאות רגישות בפרויקט
- `שם לקוח` אינו בהכרח `שם`.
- `מקט (from מוצר)` הוא lookup ולא שדה טקסט רגיל.
- `כמות מחושבת` היא rollup.
- `מפתח מוצר-מיקום חדש` הוא formula.

## פלט צפוי לפני שינוי
לפני שינוי יש לדעת:
- שם טבלה מאומת
- שם שדה מאומת
- סוג שדה
- איפה משתמשים בו בקוד

## מה לא לעשות
- לא לכתוב קוד לפי השערה.
- לא לעדכן template לפני אימות הנתון ב-backend.
- לא להניח שמבנה הערך זהה בין lookup לבין text.

## מסמכים משלימים
- `/a0/usr/projects/eliran/eliran-crm.promptinclude.md`
- `/a0/usr/projects/eliran/docs/customers_fields_mapping.md`
- `/a0/usr/projects/eliran/docs/inventory_rules.md`
