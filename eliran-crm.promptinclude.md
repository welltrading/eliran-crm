# ELIRAN CRM — Core Project Context (Auto-Injected)

## פרויקט
מערכת CRM לניהול לקוחות, הצעות מחיר, הזמנות, מלאי, מתקינים ותשלומים — לעסק מקלחונים.

### בעלי תפקידים
- בעלים: עלירן
- תפעול: מורן
- מתקינים: צוות שטח

## טכנולוגיה
- **Backend**: Python / Flask
- **Database / Source of Truth**: Airtable
- **Frontend**: HTML + Jinja2
- **שפת ממשק**: עברית, RTL תמיד
- **אינטגרציות**: Airtable API, Ezcount API (עתידי)
- **אירוח**: Hostinger

## עקרון יסוד
> **Airtable = Source of Truth**
>
> הדשבורד הוא שכבת שליטה על גבי Airtable — לא מחליף אותו.
> אין לאחסן נתונים עסקיים ראשיים מחוץ ל-Airtable.

## ישויות ליבה
- `Customers` — לקוחות
- `Orders` — הזמנות
- `OrderLineItems` — שורות הזמנה
- `Products` — מוצרים
- `InventoryByLocation` — מלאי לפי מיקום
- `InventoryMovements` — תנועות מלאי
- `Installers` — מתקינים
- `InstallationTasks` — משימות התקנה
- `ExecutionApprovals` — אישורי ביצוע
- `InstallerPayments` — תשלומים למתקינים

## זרימת עבודה עסקית
Lead → Measurement → Quote → Approval → Inventory → Installation → Approval → Payment

## כללי לוגיקה עסקית קריטיים
1. **מלאי**: `stock_out` רק לאחר אישור לקוח. ביטול לא משפיע אוטומטית על מלאי.
2. **תשלום למתקינים**: רק עבודות שמקיימות `approvedByEliran=true` + `status=approved` + לא בוטלו.
3. **Soft Delete**: ביטול שומר רשומה, לא מוחק. ברירת המחדל היא לסנן מבוטלים מ-queries.
4. **אישורים**: כל תשלום וביטול חייב אישור עלירן.
5. **אישור התקנה**: `Task(type=installation)` במצב `Completed` יוצר `Approval`.

## מבנה API
כל תגובה חייבת להיות בפורמט אחיד:

```json
{ "success": true, "data": {}, "meta": {} }
{ "success": false, "error": { "code": "", "message": "", "details": {} } }
```

## כללי פיתוח מחייבים
- **RTL תמיד** — כל תגובה, כל מסך, כל טקסט.
- **לא לבנות UI לפני אישור Phase 1** (Data + API).
- **לא להוסיף פיצ'רים שלא נדרשו**.
- **לא לנחש שמות שדות ב-Airtable** — לבדוק ולוודא לפני שימוש.
- **לשאול לפני שלב חדש**.
- **לא לשמור נתוני ליבה עסקיים מחוץ ל-Airtable**.

## העדפות תצוגה ושיח
- המשתמש מעדיף תצוגת תוכן בעברית ברורה וב-RTL בכל תשובה אפשרית.
- גם כאשר שכבת המערכת כופה פורמט טכני, יש לנסח את התוכן עצמו בעברית ובצורה קריאה ככל האפשר.

## מצב נוכחי
- Phase 1 בתהליך — חיבור Airtable פעיל ✅
- Base ID: `app77CdzKEqLlhZ8d`
- הושלם audit טכני ממוקד על `airtable_client.py` ו-`app.py` (2026-05-10)

- הוחלו 4 תיקונים מיידיים ב-`app.py`: שדה `שם לקוח`, Soft Delete להזמנות/הצעות, `SECRET_KEY` חובה, ו-`debug` דרך env בלבד (2026-05-10)
- הוחל תיקון ממוקד לחוזה ה-API: נוספו תגובות JSON אחידות ו-error handling אחיד לנתיבי `/api/*` בלבד, בלי שינוי פיצ׳רים (2026-05-10)
- הוחל audit טכני ממוקד נוסף על `logging`, `error visibility` ו-`update(typecast)` בלי שינוי פיצ׳רים: נוספו logs מובנים, `request_id` לתגובות API, והקשחת `update()` עם `typecast=True` וולידציה בסיסית (2026-05-10)
- הושלם איחוד טעינת `env / secrets loader` לכל נקודות ההפעלה בלי שינוי פיצ׳רים: גם `run_stable.py` וגם `debug_app.py` יושרו ל-loader המוקשח של `app.py`, עם `load_dotenv(stream=...)` ו-normalization לקבצי env (2026-05-10)
- בוצע audit ממוקד על `debug_app.py` ותוקנה שגיאת תשתית/typing בלבד: `AirttableClient()` הוחלף ל-`AirtableClient()` בלי שינוי פיצ׳רים (2026-05-10)
- בוצע audit ממוקד על `start.sh` ו-`verify_app.py`: נקודת ההפעלה יושרה ל-`run_stable.py`, תלויות עודכנו, ו-`verify_app.py` יושר ל-`localhost:5000` ולנתיבי מערכת קיימים בפועל (2026-05-10)

## מסמכי reference
- לוג שינויים: `docs/project_changelog.md`
- כללי מלאי: `docs/inventory_rules.md`
- מיפוי שדות לקוחות: `docs/customers_fields_mapping.md`
- מפרט PDF: `docs/pdf_templates_spec.md`

## Skills רלוונטיים
- בדיקת שדות Airtable: `skills/eliran_airtable_field_check/SKILL.md`
- תהליך מלאי: `skills/eliran_inventory_flow/SKILL.md`
- Phase guardrails: `skills/eliran_phase_guardrails/SKILL.md`

## הנחיית שימוש
- אם המשימה נוגעת לשדות Airtable, יש לבדוק קודם את מסמך השדות/הקשרים או להפעיל skill מתאים.
- אם המשימה נוגעת למלאי, יש לפעול לפי כללי `inventory_rules.md`.
- אם המשימה נוגעת ל-PDF, יש לפעול לפי `pdf_templates_spec.md`.
- אם המשימה נוגעת למסכי לקוחות, יש לפעול לפי `customers_fields_mapping.md`.

- הוחל תיקון ממוקד ל-Airtable formula escaping וקשיחות קלט: נוספו builders בטוחים ל-formula, הוחלף escaping בנוסחאות קיימות, ונוספה המרת מספרים קשיחה בקלטים רגישים בלי שינוי פיצ׳רים (2026-05-10)

- תוקן כשל טעינת סביבה ב-`run_stable.py`: טעינת `.a0proj/secrets.env` ו-`.a0proj/variables.env` מתבצעת לפני `from app import app`, כדי ש-`SECRET_KEY` יהיה זמין בזמן import (2026-05-10, import order fix)
- נוסף `SECRET_KEY` ל-`.a0proj/secrets.env` כדי לאפשר עליית Flask תקינה בסביבת הפרויקט; לאחר מכן השרת עלה בהצלחה ו-smoke test חודש (2026-05-10)
