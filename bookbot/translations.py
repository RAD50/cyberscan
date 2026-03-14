"""
Bilingual message translations for the Telegram Book Bot.
Supports English (en) and Arabic (ar).
"""

MESSAGES = {
    "en": {
        "welcome": "Welcome! Please choose your language:",
        "searching": "🔍 Searching across all bookstores...",
        "not_found": "❌ {store}: Book not found.",
        "available": "✅ Available",
        "unavailable": "❌ Not Available",
        "price": "💰 Price: {price}",
        "view_on_store": "🛒 View on {store}",
        "search_again": "🔍 Search Again",
        "help_text": "Send me any book name and I will search all Omani bookstores for you!",
        "summary": "📊 Search Summary:\n{summary}",
        "language_changed": "✅ Language changed to English.",
        "enter_book": "Please enter the book name you want to search for:",
        "no_results": "😔 No results found on any store for: {query}",
        "unauthorized": "⛔ You are not authorized to use this bot.",
        "admin_only": "⛔ This command is for admins only.",
        "whitelist_header": "📋 Whitelisted User IDs:",
        "whitelist_empty": "⚠️ Whitelist is empty — all users are allowed.",
        "user_added": "✅ User {user_id} added to whitelist.\n⚠️ Update .env for persistence after restart.",
        "user_removed": "✅ User {user_id} removed from whitelist.\n⚠️ Update .env for persistence after restart.",
        "user_not_found": "⚠️ User {user_id} is not in the whitelist.",
        "invalid_user_id": "⚠️ Invalid user ID. Please provide a numeric ID.",
        "status_header": "🤖 Bot Status:",
        "status_mode": "Mode: {mode}",
        "status_whitelist_count": "Whitelisted users: {count}",
        "status_admin_count": "Admin users: {count}",
        "mode_whitelist": "🔒 Whitelist Mode",
        "mode_open": "🔓 Open Mode",
        "store_unavailable": "⚠️ {store}: Store temporarily unavailable.",
        "all_stores_failed": "😔 All bookstores are currently unavailable. Please try again later.",
        "error_occurred": "❌ An error occurred. Please try again later.",
        "choose_language": "🌐 Choose your language:",
        "search_prompt": "📖 Enter a book name to search:",
    },
    "ar": {
        "welcome": "أهلاً! الرجاء اختيار لغتك:",
        "searching": "🔍 جاري البحث في جميع المكتبات...",
        "not_found": "❌ {store}: الكتاب غير موجود.",
        "available": "✅ متوفر",
        "unavailable": "❌ غير متوفر",
        "price": "💰 السعر: {price}",
        "view_on_store": "🛒 عرض في {store}",
        "search_again": "🔍 بحث مجدداً",
        "help_text": "أرسل لي اسم أي كتاب وسأبحث عنه في جميع المكتبات العُمانية!",
        "summary": "📊 ملخص البحث:\n{summary}",
        "language_changed": "✅ تم تغيير اللغة إلى العربية.",
        "enter_book": "الرجاء إدخال اسم الكتاب الذي تريد البحث عنه:",
        "no_results": "😔 لم يتم العثور على نتائج في أي متجر لـ: {query}",
        "unauthorized": "⛔ غير مصرح لك باستخدام هذا البوت.",
        "admin_only": "⛔ هذا الأمر مخصص للمشرفين فقط.",
        "whitelist_header": "📋 قائمة المستخدمين المسموح لهم:",
        "whitelist_empty": "⚠️ القائمة فارغة — جميع المستخدمين مسموح لهم.",
        "user_added": "✅ تم إضافة المستخدم {user_id} إلى القائمة.\n⚠️ قم بتحديث ملف .env للحفاظ على التغييرات بعد إعادة التشغيل.",
        "user_removed": "✅ تم إزالة المستخدم {user_id} من القائمة.\n⚠️ قم بتحديث ملف .env للحفاظ على التغييرات بعد إعادة التشغيل.",
        "user_not_found": "⚠️ المستخدم {user_id} غير موجود في القائمة.",
        "invalid_user_id": "⚠️ معرف مستخدم غير صالح. يرجى تقديم معرف رقمي.",
        "status_header": "🤖 حالة البوت:",
        "status_mode": "الوضع: {mode}",
        "status_whitelist_count": "المستخدمون المسموح لهم: {count}",
        "status_admin_count": "المشرفون: {count}",
        "mode_whitelist": "🔒 وضع القائمة البيضاء",
        "mode_open": "🔓 وضع مفتوح",
        "store_unavailable": "⚠️ {store}: المتجر غير متاح مؤقتاً.",
        "all_stores_failed": "😔 جميع المكتبات غير متاحة حالياً. يرجى المحاولة لاحقاً.",
        "error_occurred": "❌ حدث خطأ. يرجى المحاولة لاحقاً.",
        "choose_language": "🌐 اختر لغتك:",
        "search_prompt": "📖 أدخل اسم الكتاب للبحث:",
    },
}


def get_message(key: str, lang: str = "en", **kwargs) -> str:
    """Get a translated message by key and language, with optional formatting."""
    msg = MESSAGES.get(lang, MESSAGES["en"]).get(key, "")
    if kwargs:
        msg = msg.format(**kwargs)
    return msg
