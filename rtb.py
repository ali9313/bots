from config import *
from collections import defaultdict
import os

roles = {
    'مواطن': 1,           # تم تغيير اسم الرتبة إلى مواطن
    'موظف حكومي': 2,     # تم تغيير اسم الرتبة إلى موظف حكومي
    'رئيس الجمهورية': 3  # تم تغيير اسم الرتبة إلى رئيس الجمهورية
}
MAHIIB_ID = 232499688

# اسم الملف الذي سيتم تخزين الرتب فيه
roles_file = "backend/user_roles.txt"

# قائمة الأعضاء مع رتبهم
members = defaultdict(lambda: 'مواطن')  # افتراضي: مواطن

# دالة لتحميل الرتب من الملف
def load_roles():
    pass

# دالة لحفظ الرتب إلى الملف
def save_roles():
    pass

# دالة لمنح رتبة لأحد الأعضاء من خلال الرد على رسالته
def promote_user(a):
    pass

# دالة لقراءة رتبة مستخدم من خلال الرد على رسالته
def read_role(a):
    pass

# تحميل الرتب عند بدء تشغيل البوت
load_roles()