# ELIRAN CRM — Project Context (Auto-Injected)

## פרויקט
מערכת CRM לניהול לקוחות, הזמנות, מלאי, מתקינים ותשלומים — עסק מקלחונים.
בעלים: עלירן | תפעול: מורן | מתקינים: צוות שטח

## טכנולוגיה
- **Backend**: Python / Flask
- **Database / Source of Truth**: Airtable (לא SQLite)
- **Frontend**: HTML + Jinja2 (RTL עברית)
- **אינטגרציות**: Airtable API, Ezcount API (עתידי)
- **אירוח**: Hostinger

## עיקרון יסוד
> **Airtable = Source of Truth**
> הדשבורד הוא שכבת שליטה על גבי Airtable — לא מחליף אותו.
> אין לאחסן נתונים עסקיים ראשיים מחוץ ל-Airtable.

## ישויות ליבה
- `Customers` — לקוחות
- `Orders` — הזמנות
- `OrderLineItems` — פריטים בהזמנה
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
1. **מלאי**: stock_out רק לאחר אישור לקוח. ביטול = לא משפיע אוטומטית.
2. **תשלום למתקינים**: רק עבודות שמקיימות `approvedByEliran=true` + `status=approved` + לא בוטלו.
3. **Soft Delete**: ביטול שומר רשומה, לא מוחק. מסונן מ-default queries.
4. **אישורים**: כל תשלום וביטול חייב אישור עלירן.
5. **אישור התקנה**: Task(type=installation) → Completed → יוצר Approval.

## מבנה API
כל תגובה חייבת להיות בפורמט אחיד:
```json
{ "success": true, "data": {}, "meta": {} }
{ "success": false, "error": { "code": "", "message": "", "details": {} } }
```

## כללי פיתוח
- **שפת ממשק**: עברית, RTL תמיד — כל תגובה, כל ממשק, כל טקסט
- **כל תשובה של הסוכן חייבת להיות מימין לשמאל (RTL)**
- **לא לבנות UI לפני אישור Phase 1** (Data + API)
- **לא להוסיף פיצ'רים שלא נדרשו**
- **לא לנחש שמות שדות ב-Airtable** — לשאול תמיד
- **לשאול לפני שלב חדש**

## מצב נוכחי
- Phase 1 בתהליך — חיבור Airtable פעיל ✅
- Base ID: `app77CdzKEqLlhZ8d` (ניהול לקוחות ופרויקטים - א.ש מקלחונים מעוצבים)

## טבלאות Airtable (שמות + IDs)
| שם טבלה | Table ID |
|---|---|
| לקוחות | `tbl3ZGvwQ5cLigpFM` |
| משימות | `tblsodUowDPPiOcCk` |
| הצעות מחיר | `tblJTBG0o9jhcs522` |
| הזמנות | `tblJYbxBXWUkAoI7m` |
| שורות הזמנה | `tbliWBlXR7HdaZms5` |
| תנועות מלאי | `tblS074Z1pDNpEVWO` |
| מלאי לפי מיקום | `tbl6HhpUq3cTba1RB` |
| מדידות | `tblOBD9ctlmESWA2x` |
| אישורי ביצוע | `tbl6z2mmkNpEFI6jx` |
| מתקינים | `tblNj2W8WJWbeG1sl` |
| ביטולים | `tblATBHZSrauLczV9` |
| צוות | `tblOVdS88j37ydSQm` |
| הזמנות למפעל | `tblgNNGPAk4sSADlq` |
| ספקים | `tblPVjHSRx6T6f8jj` |
| יומן / לוז יומי | `tblgBFxsESiqesTNY` |
| תעריפים | `tbl4guJMDoluPnHLD` |
| פרויקטים | `tblXRD8ZN1twkFbjh` |
| התקנות | `tblndyBo0AqfNm3l3` |
| מוצרים | `tbl9DI5ogG6HkbsOo`
| מוצרים-1 | `tblbf9GDDRUfDa9zW` |
| קיצורים לטפסים | `tblPCrhTfNmyQIFDL` |
| מוצרים | `tbl9DI5ogG6HkbsOo` |


## שדות הטבלאות (Field IDs)

### הזמנות (tblJYbxBXWUkAoI7m)
| שם שדה | סוג | Field ID |
|---|---|---|
| מספר הזמנה | autoNumber | fldDrP4MqsxV6EtJd |
| תאריך יצירה | createdTime | flde2no9Qoof141vN |
| שם לקוח | singleLineText | fldZEobEKEQtMtoGV |
| כתובת | singleLineText | fldzNnG3a9uojQPyO |
| סטטוס | singleSelect | fldwvbnGd8e3PAU7d |
| שם מוצר | multipleRecordLinks | fldZBzef2fD5yiVad |
| כמות | number | flddmlzT9ZHk5spa1 |
| מחיר בשקלים | currency | fldcsD7TEjjYB6kz3 |
| תשלום מלא/מקדמה | singleSelect | fldPN0eZPJuSJSh8o |
| יתרת תשלום | number | fldOAbx5iIaFAihvt |
| אמצעי תשלום | singleSelect | fldUealfvxq803w4h |
| אישור תשלום התקבל | checkbox | fldBvprcQWNtsC6jt |
| סטטוס תשלום | singleSelect | fldWzlNdgHiiIzYrl |
| הזמנה בוטלה | checkbox | fldnNtwioUCbTRiUw |
| תאריך ביטול | dateTime | fldqcjeSVvJT33Oqx |
| שורות הזמנה | multipleRecordLinks | fldIJzxGrwPaDNACs |
| מלאי לפי מיקום | multipleRecordLinks | fldQgXcY4Rxa5RXfB |
| משימות | multipleRecordLinks | fldEZ175gAwbH7vge |
| הערות | multilineText | fldFRK1Kz26jE99xR |
| אופי ההזמנה | singleSelect | flduurO6CcPQx6oya |
| RecordId | formula | fldpb2vKvhrcpOxGR |

### שורות הזמנה (tbliWBlXR7HdaZms5)
| שם שדה | סוג | Field ID |
|---|---|---|
| שורת הזמנה | autoNumber | fldnk3IiyNeTTGqsa |
| הזמנה | multipleRecordLinks | fldPxGffqlrfcYZIM |
| מוצר | multipleRecordLinks | fldYnSRIPH7j9rpSn |
| כמות | number | fldhrAvwCw1grQHNI |
| מהיכן יוצא המוצר | singleSelect | fldRcottFIlIX0r4F |
| נוצרה תנועת מלאי? | checkbox | fldVQqGmjwHTXiRo2 |
| תנועת מלאי | multipleRecordLinks | fldcqQlOTPJydjKMu |
| סוג תנועה | singleSelect | fldr1hhLfgIDGxhHS |
| סטטוס | singleSelect | fldPzANseMCMWf7kJ |
| מלאי לפי מיקום | multipleRecordLinks | fldXFRuHc3seJreuX |

### מוצרים (tbl9DI5ogG6HkbsOo)
| שם שדה | סוג | Field ID |
|---|---|---|
| דגם | multilineText | fld7oDVwD2TD3960b |
| שם מוצר מלא | formula | flddMBY4tu0y0TR1t |
| תיאור המוצר | richText | fldQNEmSl0FlCONu5 |
| דגם בסיס | singleSelect | fldldbeNRfgk6jrYA |
| מידה | singleSelect | fldygZqbnX3OknW9b |
| סוג זכוכית | singleSelect | fldsl5TQHXUfg3EEH |
| גוון פרזול | singleSelect | fldZQxtBcT4c324xc |
| גובה | singleSelect | fldUdDB11R6kXBSPn |
| מקט | formula | flddQjyBs57UJhijs |
| מחיר בשקלים | number | fldrwR6l60DWTwQhF |
| כמות | number | flduVqvO1HzeVmGPU |
| מלאי לפי מיקום | multipleRecordLinks | fld2OAgpd1gDAXnD4 |
| שורות הזמנה | multipleRecordLinks | fld6G3fYNigasmvj5 |
| תנועות מלאי 2 | multipleRecordLinks | fldtfSk4hW33XX8Ou |

### מלאי לפי מיקום (tbl6HhpUq3cTba1RB)
| שם שדה | סוג | Field ID |
|---|---|---|
| מלאי לפי מיקום | formula | fldYboj1U8ZHJK6aq |
| מוצר | multipleRecordLinks | fldHUiTkn1TFdW9n4 |
| כמות מחושבת | rollup | fldr4VIQAnulf5eIv |
| תנועות מלאי | multipleRecordLinks | flddno6IQLP121x7f |
| נמצא במלאי | formula | fld5uQzsRkmiQOthD |
| מיקום | singleSelect | fldmKrx7PBJjv0zUH |
| שם המוצר | multipleLookupValues | fldJllZEkwhXL6SIH |
| מקט (from מוצר) | multipleLookupValues | fldgrSdEuxPne8fUH |
| הערות | multilineText | fldTVVWgOLmKesSlK |
| RECORD_ID | formula | fldbWwt0xs5Qtd7aG |

### מתקינים (tblNj2W8WJWbeG1sl)
| שם שדה | סוג | Field ID |
|---|---|---|
| Name | formula | fldOSaSnJIAr43Btv |
| שם פרטי | singleLineText | fld0sR1uUVVUdSSKV |
| שם משפחה | multilineText | fld5Qhfq26o0cRHoo |
| נייד | phoneNumber | fldEKq3y8mVAqnQZu |
| אימייל | email | fld1pT9vTum0JNiFa |
| סוג התקנה שיכול לבצע | multipleSelects | fldGiu9i3KciTcMSO |
| משימות | multipleRecordLinks | fldBJNnxG0XgYQRbV |
| אישורי ביצוע | multipleRecordLinks | fldUki6GepMFoSKGs |
| סכום לתשלום Rollup | rollup | fldpaHuYIWVkk9z17 |
| התקנות | multipleRecordLinks | fldGXoA62KAUMriEY |
| תעריפי התקנה | multipleRecordLinks | fldPq2BTsJ9fYHQyq |

### התקנות (tblndyBo0AqfNm3l3)
| שם שדה | סוג | Field ID |
|---|---|---|
| מספר התקנה | autoNumber | fldrPFpfTEZu0udKy |
| מספר הזמנה | multipleRecordLinks | fldfunGJjY7cKZJ5J |
| תאריך התקנה | date | fldsyiqzHdwCb1ISK |
| חלון זמן | singleSelect | fld9Sj4UJFlUetVNa |
| מתקין | multipleRecordLinks | fldjuWa7s8ge2mKES |
| סטטוס התקנה | singleSelect | fldI0B8nua9XMGThv |
| תמונות לאחר התקנה | multipleAttachments | fldHXLCn1sjKIwxbm |
| תעריף התקנה | multipleRecordLinks | fldMcGL2OR6UTZlxH |
| סכום לתשלום | formula | flduALBfS6xK1nxxt |
| אושר לתשלום | formula | fldWIH7qtLeQ0RriG |
| הערות מהשטח | multilineText | fldS9QIMmbCR9XYVe |
| RecordID | formula | fld96i478LEr6Ru0k |
| ביטולים | multipleRecordLinks | fldFtbQqqhXUxlgV2 |

### תעריפים (tbl4guJMDoluPnHLD)
| שם שדה | סוג | Field ID |
|---|---|---|
| סוג המשימה | singleLineText | fldpoNfga22gQZsau |
| מחיר בשקלים | currency | fldB8SlJKO4BbLRbE |
| סוג התקנה | singleSelect | fldm6wOCYWYCNsQLa |
| פעיל | checkbox | fldm3OVYRryVl6bvx |
| הערות | multilineText | fldACR1SUAZAD7ycD |

### אישורי ביצוע (tbl6z2mmkNpEFI6jx)
| שם שדה | סוג | Field ID |
|---|---|---|
| אישור ביצוע | autoNumber | fld4qJrGGMWtr09dp |
| משימות | multipleRecordLinks | fldpAZh1st8qRqA7n |
| תאריך התקנה | dateTime | fld82nUwa5hZGSDlF |
| מתקינים | multipleRecordLinks | fldTjEOiF0qd1FgEd |
| תמונה לאחר התקנה | multipleAttachments | fldl3KooMqphzRR3I |
| אושר ע"י אלירן | checkbox | fldOCqFBKS8KuXSSV |
| סטטוס אישור | singleSelect | fldmg9acRqIp0zim0 |
| בטל אישור | checkbox | fldxJM4QXKh7kitBM |
| סכום לתשלום (מאושר בלבד) | formula | fldsMGqafeCRlN7zo |
| אישור תקף לתשלום | formula | fldeYPqA4yfUEee12 |
| תאריך אישור | dateTime | fldDLbU0YVyUJN3WV |

### הצעות מחיר (tblJTBG0o9jhcs522)
| שם שדה | סוג | Field ID |
|---|---|---|
| Name | autoNumber | fldFfYboIrcFejtHN |
| שם לקוח | singleLineText | fld07wwSMqvzYk0s4 |
| טלפון | phoneNumber | fldPYvrQHENHZC8pJ |
| כתובת | singleLineText | fldhF5IRofdRLTkhN |
| סטטוס | singleSelect | fldrtuHdHK8SEKLfM |
| מוצרים | multipleRecordLinks | fldPt89KYMnfPHc1X |
| כמות | number | fldcS4I85kjhbKZbJ |
| מחיר בשקלים | currency | fldHnLVvPoqT0VHvA |
| מחיר כולל | formula | flduCk9ASG6faQhPs |
| סטנדרטי/ייצור אישי | singleSelect | fldN4EILKJZND3FOf |
| הערות | multilineText | fldGnHde4OSCi00ue |
| מידות לקוח רוחב | number | fldtxUhlZi7FeSJX3 |
| מידות לקוח עומק | number | fld8TK2mavUQZ39Q2 |
| גובה מקלחון (מטר) | number | fldtuIXm9M6hJThCV |
| לקוחות | multipleRecordLinks | fldrmgK4J1zPrBY3T |

### משימות (tblsodUowDPPiOcCk)
| שם שדה | סוג | Field ID |
|---|---|---|
| תיאור משימה | formula | fld9pZpcEyipF5teB |
| בקשת ביטול | checkbox | fldzH9z9C3yOUlyYJ |
| סטטוס | singleSelect | fldAP5bP6n8okIqec |
| הזמנות | multipleRecordLinks | fldJQBgJQDdtQFvML |
| מתקין | multipleRecordLinks | fldtSaIGqknI4t1IM |
| סוג משימה | multipleRecordLinks | fld8xgcv4HEeW2NYF |
| תאריך ביצוע | date | fld7wFWvaROfYEQ8B |
| חלון זמן | singleSelect | fldGurfCRnIZNu8Dl |
| הערות | multilineText | fldIcfmWGysvQYv8c |
| אישורי ביצוע | multipleRecordLinks | fldqdMr1fzW7rT3PR |
| סוג משימה כותרת לדאשבורד | singleSelect | fld8IAHnls7oZUMOC |
| בוצע בפועל | checkbox | fld00gbAzyZVvDWOt |
| התקנות | multipleRecordLinks | fldgwOLbZLhd8jIiM |
| אחראי | singleSelect | fldMehHwe8j62Zmd3 |
| דחיפות | singleSelect | fldOvaY4pXw0s0mr5 |
| ביטולים | multipleRecordLinks | fldaVuPt8MiNJIfwu |
| RECORD ID | formula | fldMblO2S5pD6t4iO |

### תנועות מלאי (tblS074Z1pDNpEVWO)
| שם שדה | סוג | Field ID |
|---|---|---|
| מספר תנועה | autoNumber | fldKRpqK9M9M0oODe |
| מוצר | multipleRecordLinks | fldG4ahYiyKWCGvoJ |
| מיקום | singleSelect | fldXNpU6Ga5KX9vic |
| סוג תנועה | singleSelect | fldseUfuzw9ktKuRy |
| כמות | number | fldRVE4yaMKwT5e1S |
| כמות מחושבת | formula | fld733WyctwcweOC6 |
| סטטוס תנועה | singleSelect | fldFqsW6nY2Q5Guvd |
| מלאי לפי מיקום | multipleRecordLinks | fldtsmbAgTKPc7kUj |
| שורות הזמנה | multipleRecordLinks | fldModhBcaJqCP6na |
| תאריך | dateTime | fldoQUdwvZUId6wmd |
| הערות | multilineText | fldQ8umCODTY80hBU |

## כלל עדכון הקשר — חובה
- **בסוף כל שלב** — הסוכן חייב לעדכן את סעיף "מצב נוכחי" בקובץ זה
- **כל החלטה חשובה** (טכנולוגיה, שדות Airtable, לוגיקה) — נשמרת כאן מיד
- **לפני שיחה חדשה** — הסוכן קורא קובץ זה ומסתמך עליו כ-Single Source of Truth של ההקשר
- קבצים ישנים ב-/a0/usr/projects/eliran (app.py, templates) — ימוחקו/יוחלפו
