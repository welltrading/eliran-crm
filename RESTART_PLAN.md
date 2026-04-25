# תיקון מחדש של הפרויקט - גישה לפי התכנון החדש (OpenAI)

## 🎯 מטרות התחלה חדשה

1. **Data First**: הגדרת מבנה הנתונים לפני בניית כל קוד.
2. **Business Logic Clear**: הבטחת לוגיקה עסקית וברורה.
3. **Simple Stack**: Flask (Python) + SQLite. לא מתחיל מחדש ב-TypeScript רק כדי לא להסתבך.

---

## 📊 שלב 1: הגדרת מודל הנתונים (Phase 1 - Data Contracts)

### 1.1 טבלאות דרושות

| שם טבלה | שדות דרושים | הסבר |
| :--- | :--- | :--- |
| `customers` | `id, name, phone, email, address, created_at` | מידע על הלקוחות |
| `products` | `id, name, sku, category, unit, default_price, warehouse_location` | פרטי המוצרים במלאי |
| `inventory` | `id, product_id, location, quantity, min_stock_level, last_movement` | מלאי נוכחי לפי מיקום (מחסן/חנות) |
| `orders` | `id, customer_id, order_number, status, total_amount, created_at, approved_by, notes` | הזמנות כלליות |
| `order_lines` | `id, order_id, product_id, quantity, unit_price, total_price` | פריטים בהזמנה |
| `tasks` | `id, order_id, installer_id, task_type, status, scheduled_date, completed_date, approved_by` | משימות התקנה ולוגיסטיקה |
| `payments` | `id, order_id, installer_id, amount, status, approved_by_eliran, paid_date, notes` | תשלומים למתקינים וקבלות |
| `approvals` | `id, task_id, approval_type, approved_by, status, notes, timestamp` | אישורים של לקוחות/עובדים |
| `file_uploads` | `id, entity_type, entity_id, file_path, uploaded_by, timestamp` | קבצים תמונות אישור/חשבוניות |

### 1.2 סטטוסים קריטיים (Enums)

`order.status`:
`['draft', 'confirmed', 'cancelled', 'approved', 'in_production', 'ready_to_ship', 'shipped', 'delivered']`

`task.status`:
`['pending', 'scheduled', 'in_progress', 'completed', 'approved', 'failed']`

`payment.status`:
`['pending', 'approved', 'paid', 'cancelled']`

---

## 🔧 שלב 2: אפיון ה-API Layer

### 2.1 מבנה תגובות אחיד

```json
{
  "success": true,
  "data": { ... },
  "meta": { "total": 1, "page": 1 }
}
```

או במקרה של שגיאה:

```json
{
  "success": false,
  "error": {
"code": "ERR_001",
"message": "לא נמצאו הזמנות",
"details": {
"validation_errors": [
```

### 2.2 סדרת אפיונים (Phase 1)  

1. `GET /api/orders` - רשימה, סינון, דפיפיינה  
2. `POST /api/orders` - יצירת הזמנה  
3. `GET /api/orders/{id}` - הצגת פרטים  
4. `PATCH /api/orders/{id}` - עדכון הזמנה  
5. `POST /api/orders/{id}/cancel` - ביטול הזמנה  
6. `GET /api/inventory` - ממשקי מלאי  
7. `GET /api/tasks` - רשימת משימות  
8. `POST /api/payments/installers` - תשלומים 

---

## 📝 שלב 3: לוגיקה עסקית קריטית

1. **המרת הצעה להזמנה**:  
   `order.status = 'approved'` רק כאשר `approval` קיים.

2. **מניעת כפילויות**:  
   `order_lines.product_id` לא יכול להיות כפול באותה הזמנה (איסוף).

3. **ניהול מלאי**:  
   `stock_out` רק לאחר אישור הלקוח.  
   `stock_in` רק כאשר נקבע מחדש / בוטלה הזמנה.

4. **ביטול הזמנה**:  
   `order.status = 'cancelled'` - לא מחזיר מלאי, ממשק עם מלאי נפרד (soft delete).

5. **תשלום למתקינים**:  
   סכום תשלום = רק עבודות ש-`approved_by_eliran = true` ו-`status = 'completed'`.

---

## ⚠️ חוקי יסוד חדשים

1. **לא בונים UI עוד שום דבר עד Phase 1**.  
   רק נתונים + API.  
2. **לא מוסיפים פיצ'רים שלא נדרשים**.  
   מתמקדים בהזמנות, משימות ותשלומים.  
3. **אישורי Eliran בלבד**.  
   כל תשלום/ביטול חייב אישור אדמין.  
4. **לא מנחשים שדות ב-Airtable**.  
   אם יש אירטבל - נתייחס בשדה ממשק.  
   (אם יש אירטבל).

---

## 🚀 תוכנית עבודה

1. נבנה מודל הנתונים (SQLAlchemy models)
2. נבנה ממשק API בסיסי ב-Flask
3. נבנה לוגיקה עסקית מלאה ב-Backend
4. נבדיק (Unit Tests) את הלוגיקה
5. נחכה לאישור Phase 1 לפני בניית הממשק

---

## 🤔 שאלות פתוחות

1. האם עדיין נשמור על אירטבל? או נעבור לסלייקט ללא אירטבל?
2. מה המיקומים הפיזיים של המלאי? (מחסן/חנות)  
3. מהם המוצרים הראשוניים שמוצגים במערכת?
4. האם צריך גינה (WhatsApp/Templates) או לא?

---

**המשך?**
