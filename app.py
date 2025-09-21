from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Date, Time, Text  # هذا إن لم تكن تستورد من db مباشرة
from sqlalchemy import Column, Enum
from flask_cors import CORS
import os
import time  # ✅ هذا صحيح
from datetime import datetime, date, time
from datetime import datetime, timezone, timedelta
from flask import send_from_directory
import uuid
import json
from zoneinfo import ZoneInfo
from werkzeug.utils import secure_filename
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from sqlalchemy import func, desc
from datetime import datetime, time
from calendar import monthrange
import threading
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from sqlalchemy import text
from sqlalchemy import or_, and_
from sqlalchemy.orm import relationship
from sqlalchemy import JSON
import requests
import pytz
from decimal import Decimal
import math
from flask import Flask, request, jsonify, send_file
import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta, date
import xlsxwriter
from urllib.parse import unquote
import traceback
from sqlalchemy import distinct
import base64
import cloudinary
import cloudinary.uploader
import cloudinary.api
app = Flask(__name__)
app.permanent_session_lifetime = timedelta(days=365*100) 

app.config['SECRET_KEY'] = 'f9c7d2b8a1e6f5b4c3d9a0e2b6d1c8f7e3a2b5d6c4f0a9e1b7d8c2f3a6b5e7d4'
cloudinary.config(
    cloud_name = 'dwnydnavt',         # ضع هنا Cloud Name
    api_key = '154189674494148',       # ضع هنا API Key
    api_secret = 'uCh0dqbPmwW0I2yw0q-DQNTckdI',  # ضع هنا API Secret
    secure = True
)
# تمكين CORS لدعم الطلبات من الـ frontend
CORS(app, 
     supports_credentials=True,  # مهم لدعم الكوكيز
     origins=["https://loginsystem-almohtarif.netlify.app"],
     allow_headers=["Content-Type", "Authorization"],
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     expose_headers=["Content-Disposition"],
     max_age=600)
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/almohtarif_company_db4'

#app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
#   'pool_size': 10,
#    'pool_recycle': 3600,
#    'pool_pre_ping': True,
#    'connect_args': {
#        'connect_timeout': 30
#    }
#}
# في بداية ملف الخادم (بعد import os)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://almohtarif_company_2:c9Q8hMMdmZSO@37.60.250.83:3306/almohtarif_company_db_3"
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,              # قلل العدد - أكثر ليس دائماً أفضل
    'max_overflow': 15,           # قلل هذا أيضاً
    'pool_timeout': 10,           # قلل الانتظار - فشل سريع أفضل
    'pool_recycle': 3600,         # زود المدة لتجنب إعادة الاتصال المتكررة
    'pool_pre_ping': True,        # ممتاز - احتفظ بهذا
    'connect_args': {
        'connect_timeout': 5,     # قلل أكثر للاتصال السريع
        'read_timeout': 10,       # إضافة timeout للقراءة
        'write_timeout': 10,      # إضافة timeout للكتابة
        'charset': 'utf8mb4',     # تحديد charset مباشرة
        'autocommit': True,       # تسريع العمليات البسيطة
        'sql_mode': 'TRADITIONAL' # تحسين أداء MySQL
    }
}
# basedir = os.path.abspath(os.path.dirname(__file__))
# UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/static/uploads/<path:filename>')
# def serve_uploads(filename):
#     return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
db = SQLAlchemy(app) 
# جدول الموظفين
class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    full_name_arabic = db.Column(db.String(150), nullable=False)
    full_name_english = db.Column(db.String(150), nullable=False)
    employee_number = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    profile_image = db.Column(db.String(255))
    telegram_chatid = db.Column(db.String(50))
    phone = db.Column(db.String(20), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.dep_id'), nullable=False)
    position = db.Column(db.Text, nullable=False)  # المنصب الوظيفي
    position_english = db.Column(db.Text, nullable=False)  # المنصب الوظيفي بالانكليزية
    status = db.Column(db.String(10), default='off')  # قيمته إما 'on' أو 'off'
    # ✅ يجب استخدام db.String وليس String فقط
    role = db.Column(db.String(20), nullable=False)
    end_of_service_date = db.Column(db.Date, nullable=True)
    bank_account = db.Column(db.String(100))
    address = db.Column(db.String(255))
    weekly_day_off = db.Column(db.String(10), nullable=False)

    # ✅ يجب استخدام db.Time و db.Date و db.Text
    work_start_time = db.Column(db.Time, nullable=False)
    work_end_time = db.Column(db.Time, nullable=False)
    date_of_joining = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    # ✅ الحقول الجديدة المطلوبة
    study_major = db.Column(db.Text, nullable=False)  # الدراسة والتخصص
    governorate = db.Column(db.Text, nullable=False)  # المحافظة
    relative_phone = db.Column(db.String(20))  # رقم شخص قريب (اختياري)
    relative_relation = db.Column(db.Text, nullable=True)  # صلة القرابة (اختياري)
    date_of_birth = db.Column(db.Date, nullable=False)  # المواليد
    national_id = db.Column(db.String(20), nullable=False)  # الرقم الوطني
    job_level = db.Column(db.String(20), nullable=False)  # الدرجة الوظيفية
    promotion = db.Column(db.Text,nullable=True)  # الترقية (اختياري)
    career_stages = db.Column(db.Text)  # المراحل الوظيفية (اختياري)
    employee_status = db.Column(db.String(20), nullable=False)  # وضع الموظف
    work_location = db.Column(db.String(20), nullable=False)  # مكان العمل
    work_nature = db.Column(db.String(20), nullable=False)  # طبيعة العمل
    marital_status = db.Column(db.String(15))  # الحالة الاجتماعية (اختياري)
    nationality = db.Column(db.String(50))  # الجنسية (اختياري)
    trainings = db.Column(db.Text)  # تدريبات (اختياري)
    external_privileges = db.Column(db.Text)  # امتيازات خارجية (اختياري)
    special_leave_record = db.Column(db.Text)  # سجل إجازات خاصة (اختياري)
    drive_folder_link = db.Column(db.Text, nullable=True)  # رابط مجلد الموظف درايف (اختياري)
    is_leave = db.Column(db.String(10), default='off')  # إجازة ساعية
    is_vacation = db.Column(db.String(10), default='off')  # إجازة رسمية أو سنوية
    is_weekly_day_off = db.Column(db.String(10), default='off')  # يوم عطلة أسبوعية
        # ✅ الإضافات الجديدة للإجازات
    regular_leave_hours = Column(db.Float, default=0.0)
    sick_leave_hours = Column(db.Float, default=0.0)
    emergency_leave_hours = Column(db.Float, default=0.0)
    regular_leave_total = db.Column(db.Float, default=0.0) 
    regular_leave_used = db.Column(db.Float, default=0.0)    # المستخدم
    regular_leave_remaining = db.Column(db.Float, default=0.0) # المتبقي

    sick_leave_total = db.Column(db.Float, default=0.0)
    sick_leave_used = db.Column(db.Float, default=0.0)
    sick_leave_remaining = db.Column(db.Float, default=0.0)

    emergency_leave_total = db.Column(db.Float, default=0.0)
    emergency_leave_used = db.Column(db.Float, default=0.0)
    emergency_leave_remaining = db.Column(db.Float, default=0.0)
    department = db.relationship("Department", back_populates="employees")
    leave_requests = db.relationship("LeaveRequest", back_populates="employee", cascade="all, delete-orphan")
    attendance_records = db.relationship("AttendanceRecord", back_populates="employee", cascade="all, delete-orphan")
    compensation_leaves = db.relationship("CompensationLeaveRequest", back_populates="employee", cascade="all, delete-orphan")
    work_delay_archives = db.relationship("WorkDelayArchive", back_populates="employee", cascade="all, delete-orphan")
    notifications = db.relationship("Notification", back_populates="recipient", cascade="all, delete-orphan")
    salary_components = db.relationship("SalaryComponent", back_populates="employee", cascade="all, delete-orphan")
    financial_entitlements = db.relationship("FinancialEntitlement", back_populates="employee", cascade="all, delete-orphan")    
    # ✅ يجب استخدام db.relationship
    additional_information = db.relationship('AdditionalInformation', back_populates='employee', cascade='all, delete-orphan')
    supervisor_profile = db.relationship('Supervisor', back_populates='employee',cascade="all, delete-orphan", uselist=False)
    additional_attendance_records = db.relationship("AdditionalAttendanceRecord",back_populates="employee",cascade="all, delete-orphan")
    custom_fields = db.relationship('EmployeeCustomField', back_populates='employee', cascade='all, delete-orphan')
class EmployeeCustomField(db.Model):
    __tablename__ = 'employee_custom_fields'  # ✅ يجب أن تبدأ بـ __tablename__

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    field_name = db.Column(db.String(100), nullable=False)
    field_value = db.Column(db.String(255), nullable=True)

    employee = db.relationship('Employee', back_populates='custom_fields')  # ✅ العلاقة هنا


class AdditionalAttendanceRecord(db.Model):
    __tablename__ = 'additional_attendance_records'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)

    name = db.Column(db.String(150), nullable=False)      # الاسم بالإنجليزية
    arname = db.Column(db.String(150), nullable=False)    # الاسم بالعربية
    role = db.Column(db.String(20), nullable=False)        # مثل 'ادمن' أو 'مشرف' أو 'موظف'
    is_holiday = db.Column(db.Boolean, default=False)
    start_time = db.Column(Time)  # ✅ وقت البداية
    end_time = db.Column(Time)    # ✅ وقت النهاية
    add_attendance_minutes = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)# pending/approved/rejected
    notes = db.Column(db.Text)

    employee = db.relationship("Employee", back_populates="additional_attendance_records")
#جدول المشرفين
class Supervisor(db.Model):
    __tablename__ = 'supervisors'

    supervisor_ID = db.Column(db.Integer, db.ForeignKey('employees.id'), primary_key=True)
    dep_id = db.Column(db.Integer, db.ForeignKey('departments.dep_id'), nullable=False)
    dep_name = db.Column(db.String(100), nullable=False)

    employee = db.relationship('Employee', back_populates='supervisor_profile')
    department = db.relationship('Department', back_populates='supervisors')
    leave_requests = db.relationship("LeaveRequest", back_populates="supervisor", cascade="all, delete-orphan")
    compensation_leaves = db.relationship("CompensationLeaveRequest", back_populates="supervisor", cascade="all, delete-orphan")
    work_delay_archives = db.relationship("WorkDelayArchive", back_populates="supervisor", cascade="all, delete-orphan")

# جدول الاقسام
class Department(db.Model):
    __tablename__ = 'departments'

    dep_id = db.Column(db.Integer, primary_key=True)
    dep_name = db.Column(db.String(100), nullable=False)
    dep_name_english = db.Column(db.String(100), nullable=False)
    visible = db.Column(db.Boolean, default=True, nullable=False)


    employees = db.relationship("Employee", back_populates="department", cascade="all, delete")
    supervisors = db.relationship("Supervisor", back_populates="department", cascade="all, delete")
    special_buttons = db.relationship("SpecialButton", back_populates="department", cascade="all, delete")
class AdditionalInformation(db.Model):
    __tablename__ = 'additional_information'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id', ondelete='CASCADE'), nullable=False)
    name1 = db.Column(db.String(100), nullable=False)

    employee = relationship('Employee', back_populates='additional_information')
def current_syria_time():
    tz = pytz.timezone('Asia/Damascus')
    return datetime.now(tz)
def get_syria_date():
    tz = pytz.timezone('Asia/Damascus')
    return datetime.now(tz).date()
def time_to_minutes(time_obj):
    if time_obj is None:
        return 0
    return time_obj.hour * 60 + time_obj.minute
class AttendanceRecord(db.Model):
    __tablename__ = 'attendance_records'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    check_in_time = db.Column(db.DateTime, default=current_syria_time)
    check_out_time = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    is_auto_checkout = db.Column(db.Boolean, default=False)
    office_work_hours = db.Column(db.Float, nullable=True)
    work_hours = db.Column(db.Float, nullable=True)
    work_date = db.Column(db.Date, nullable=True)

    employee = db.relationship('Employee', back_populates='attendance_records')

# جدول طلبات الإجازة
class LeaveRequest(db.Model):
    __tablename__ = 'leave_requests'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisors.supervisor_ID'), nullable=False)
    type = db.Column(db.String(50))  # hourly/daily/multi-day
    classification = db.Column(db.String(50))  # normal/emergency/sick
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    hours_requested = db.Column(db.Float)
    status = db.Column(db.String(50))  # pending/approved/rejected
    start_time = db.Column(db.Time)  # بداية الإجازة الساعية (مثل 11:00)
    end_time = db.Column(db.Time)    # نهاية الإجازة الساعية (مثل 13:00)
    note = db.Column(db.Text)
    
    employee = db.relationship("Employee", back_populates="leave_requests")
    supervisor = db.relationship("Supervisor", back_populates="leave_requests")
# جدول طلبات تعويض الإجازة
class CompensationLeaveRequest(db.Model):
    __tablename__ = 'compensation_leave_requests'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisors.supervisor_ID'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    hours_requested = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.Time)  # بداية الإجازة الساعية (مثل 11:00)
    end_time = db.Column(db.Time)  
    note = db.Column(db.Text)  # ✅ العمود الجديد 

    employee = db.relationship("Employee", back_populates="compensation_leaves")
    supervisor = db.relationship("Supervisor", back_populates="compensation_leaves")
# جدول تأخيرات العمل
class WorkDelayArchive(db.Model):
    __tablename__ = 'work_delay_archives'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=current_syria_time)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    supervisor_id = db.Column(db.Integer, db.ForeignKey('supervisors.supervisor_ID'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    minutes_delayed = db.Column(db.Integer, nullable=False)
    from_timestamp = db.Column(db.DateTime, nullable=False)
    to_timestamp = db.Column(db.DateTime, nullable=False)
    delay_note = db.Column(db.String(255))
    status = db.Column(db.String(50), nullable=False)  # Justified / Unjustified

    employee = db.relationship("Employee", back_populates="work_delay_archives")
    supervisor = db.relationship("Supervisor", back_populates="work_delay_archives")
# جدول الإشعارات
class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True)
    recipient_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=current_syria_time)
    is_read = db.Column(db.Boolean, default=False)

    recipient = db.relationship("Employee", back_populates="notifications")
# جدول مكونات الراتب

class SalaryComponent(db.Model):
    __tablename__ = 'salary_components'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    base_salary = db.Column(db.Integer,default=0, nullable=False)
    hour_salary = db.Column(db.Numeric(15, 10),default=0.0, nullable=False)  # DECIMAL(15,10) دقة أعلى مع 10 خانات عشرية
    overtime_rate = db.Column(db.Float)  # نسبة العمل الإضافي العادي
    holiday_overtime_rate = db.Column(db.Float)  # نسبة العمل الإضافي في العطلات
    internet_allowance = db.Column(db.Integer, default=0)  # بدل الإنترنت
    transport_allowance = db.Column(db.Integer, default=0)  # بدل النقل
    depreciation_allowance = db.Column(db.Integer, default=0)  # بدل الإهلاك
    administrative_allowance= db.Column(db.Integer, default=0)  # بدل إداري 
    administrative_deduction = db.Column(db.Integer, default=0) # خصم اداري

    employee = db.relationship("Employee", back_populates="salary_components")

# جدول الأزرار الخاصة
class SpecialButton(db.Model):
    __tablename__ = 'special_buttons'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.dep_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    
    department = db.relationship("Department", back_populates="special_buttons")
# جدول المستحقات المالية

class FinancialEntitlement(db.Model):
    __tablename__ = 'financial_entitlements'

    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    month_year = db.Column(db.String(7), nullable=False)  # e.g. "2024-05"
    total_amount = db.Column(db.Float, nullable=False)
    google_sheet_url = db.Column(db.String(255))

    employee = db.relationship("Employee", back_populates="financial_entitlements")
# جدول العطل الرسمية
class OfficialHoliday(db.Model):
    __tablename__ = 'official_holidays'

    id = db.Column(db.Integer, primary_key=True)
    holiday_date = db.Column(db.Date, nullable=False)
    description = db.Column(db.String(255), nullable=False)   
        # إضافة دالة to_dict المطلوبة
    def to_dict(self):
        return {
            'id': self.id,
            'holiday_date': self.holiday_date.isoformat(),  # تحويل التاريخ إلى سلسلة نصية
            'description': self.description
        } 
# جدول التعميمات
class Broadcast(db.Model):
    __tablename__ = 'broadcasts'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=current_syria_time)  

# إعداد التلغرام
TELEGRAM_BOT_TOKEN = "7873576432:AAFzoweD7-tfpvYoetIdgNJRjx_3LhV0lHQ"  # ضع هنا توكن البوت الخاص بك
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
# دالة الرد على أمر /start
@app.route('/telegram/webhook', methods=['POST'])
def telegram_webhook():
    data = request.json

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")
        first_name = data["message"]["from"].get("first_name", "مستخدم")

        if text == "/start":
            message = (
                f"مرحباً {first_name}!\n"
                f"أهلا بك في 𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡\n"
                f"🔹 رقم الدردشة الخاص بك: <code>{chat_id}</code>"
            )
            requests.post(TELEGRAM_API_URL, json={
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            })

    return "OK"
@app.route('/api/compensation-leave-requests', methods=['POST'])
def create_compensation_leave_request():
    if 'employee' not in session:
        return jsonify({"success": False, "message": "يرجى تسجيل الدخول"}), 401

    syria_tz = pytz.timezone("Asia/Damascus")
    employee_id = session['employee']['id']
    data = request.get_json()

    # التحقق من البيانات المطلوبة
    required_fields = ['date', 'start_time', 'end_time', 'note']
    if not all(field in data for field in required_fields):
        return jsonify({
            "success": False,
            "message": "بيانات ناقصة. يرجى تعبئة جميع الحقول المطلوبة"
        }), 400

    employee = db.session.get(Employee, employee_id)
    if not employee:
        return jsonify({
            "success": False,
            "message": "الموظف غير موجود"
        }), 404
       # 🔴 التحقق من أهلية الموظف للتعويض
    if employee.regular_leave_total == employee.regular_leave_remaining:
        return jsonify({
            "success": False,
            "message": "لا يمكنك تقديم طلب تعويض لأن رصيد إجازاتك لم يُستخدم بعد"
        }), 400
    # احصل على جميع المشرفين المسؤولين عن القسم
    department_supervisors = Supervisor.query.filter_by(dep_id=employee.department_id).all()
    if not department_supervisors:
        return jsonify({
            "success": False,
            "message": "لا يوجد مشرفين في القسم"
        }), 404

    # التحقق من كون الموظف مشرفًا
    is_supervisor = Supervisor.query.filter_by(supervisor_ID=employee_id).first() is not None
    status = 'approved' if is_supervisor else 'pending'

    # تحويل الأوقات إلى كائنات الوقت
    try:
        request_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        end_time = datetime.strptime(data['end_time'], '%H:%M').time()
    except ValueError:
        return jsonify({
            "success": False,
            "message": "تنسيق التاريخ أو الوقت غير صحيح"
        }), 400

    # حساب ساعات الطلب
    start_dt = datetime.combine(datetime.today(), start_time)
    end_dt = datetime.combine(datetime.today(), end_time)
    if end_dt < start_dt:
        end_dt += timedelta(days=1)

    diff = end_dt - start_dt
    hours_requested = diff.total_seconds() / 3600

    # التحقق من وجود طلب سابق لنفس التاريخ
    existing_request = CompensationLeaveRequest.query.filter_by(
        employee_id=employee_id,
        date=request_date
    ).first()
    
    if existing_request:
        return jsonify({
            "success": False,
            "message": "يوجد طلب تعويض إجازة لهذا التاريخ مسبقاً"
        }), 400

    # إنشاء سجل طلب تعويض الإجازة
    new_request = CompensationLeaveRequest(
        timestamp=datetime.now(syria_tz),
        employee_id=employee_id,
        supervisor_id=department_supervisors[0].supervisor_ID,
        date=request_date,
        hours_requested=hours_requested,
        status=status,
        start_time=start_time,
        end_time=end_time,
        note=data['note']
    )

    try:
        db.session.add(new_request)
        db.session.commit()
        
        # إذا كان المشرف قبل الطلب تلقائياً، أضف الساعات إلى رصيده
        if is_supervisor:
            employee.regular_leave_remaining += hours_requested
            employee.regular_leave_used = max(0, employee.regular_leave_used - hours_requested)
            
            # إرسال إشعار للموظف (المشرف نفسه)
            notification = Notification(
                recipient_id=employee_id,
                message="تم قبول طلب التعويض تلقائياً"
            )
            db.session.add(notification)
            
            # إرسال رسالة تلغرام للموظف (المشرف)
            if employee.telegram_chatid:
                date_str = request_date.strftime('%Y-%m-%d')
                start_time_str = start_time.strftime('%I:%M %p').replace('AM','ص').replace('PM','م')
                end_time_str = end_time.strftime('%I:%M %p').replace('AM','ص').replace('PM','م')
                
                employee_message = f"""
✅ <b>تم قبول طلب التعويض تلقائياً</b>
━━━━━━━━━━━━━━━━━━━━
👤 <b>الموظف:</b> {employee.full_name_arabic}
📅 <b>التاريخ:</b> {date_str}
⏰ <b>من وقت:</b> {start_time_str}
⏰ <b>إلى وقت:</b> {end_time_str}
⏱️ <b>المدة:</b> {hours_requested:.2f} ساعة
📝 <b>السبب:</b> {data['note']}
🕒 <b>وقت المعالجة:</b> {datetime.now(syria_tz).strftime("%Y-%m-%d %I:%M %p")}
━━━━━━━━━━━━━━━━━━━━
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
                """
                send_telegram_message(employee.telegram_chatid, employee_message)
            
            # إرسال الطلب المعتمد إلى مجموعة التلغرام كأرشيف
            try:
                archive_message = f"""
📋 <b>طلب معتمد - أرشيف</b>
━━━━━━━━━━━━━━━━━━━━
📄 <b>نوع الطلب:</b> تعويض
👤 <b>الموظف:</b> {employee.full_name_arabic}
🏢 <b>القسم:</b> {employee.department.dep_name}
👨‍💼 <b>المشرف:</b> {employee.full_name_arabic}
📅 <b>التاريخ:</b> {date_str}
⏰ <b>من وقت:</b> {start_time_str}
⏰ <b>إلى وقت:</b> {end_time_str}
⏱️ <b>المدة:</b> {hours_requested:.2f} ساعة
📝 <b>السبب:</b> {data['note']}
🕒 <b>وقت المعالجة:</b> {datetime.now(syria_tz).strftime("%Y-%m-%d %I:%M %p")}
━━━━━━━━━━━━━━━━━━━━
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
                """
                group_chat_id = "-4847322310"
                send_telegram_message(group_chat_id, archive_message)
            except Exception as e:
                print(f"فشل في إرسال الأرشيف إلى التلغرام: {str(e)}")
        
        # إرسال إشعارات للمشرفين إذا كان الموظف غير مشرف
        else:
            for supervisor in department_supervisors:
                notification = Notification(
                    recipient_id=supervisor.supervisor_ID,
                    message=f"طلب تعويض إجازة جديد من الموظف {employee.full_name_arabic}"
                )
                db.session.add(notification)
                
                # إرسال إشعار تلغرام
                supervisor_employee = db.session.get(Employee, supervisor.supervisor_ID)
                if supervisor_employee and supervisor_employee.telegram_chatid:
                    telegram_message = f"""
🔔 <b>طلب تعويض إجازة جديد</b>
━━━━━━━━━━━━━━━━━━━━
👤 الموظف: {employee.full_name_arabic}
📅 تاريخ التعويض: {request_date.strftime('%Y-%m-%d')}
⏰ الوقت: من {datetime.strptime(data['start_time'], '%H:%M').strftime('%I:%M %p').replace('AM','ص').replace('PM','م')} 
   ⬅️ إلى {datetime.strptime(data['end_time'], '%H:%M').strftime('%I:%M %p').replace('AM','ص').replace('PM','م')}
⏳ المدة: {hours_requested:.2f} ساعة
📝 الملاحظة: {data['note']}
━━━━━━━━━━━━━━━━━━━━
🕒 {datetime.now(syria_tz).strftime("%Y-%m-%d %I:%M %p")}
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
                    """
                    send_telegram_message(supervisor_employee.telegram_chatid, telegram_message)
        
        db.session.commit()
        
        return jsonify({
            "success": True,
            "message": "تم قبول طلب تعويض الإجازة تلقائياً" if is_supervisor else "تم إرسال طلب تعويض الإجازة للمشرف",
            "request_id": new_request.id,
            "is_auto_approved": is_supervisor,
            "hours_requested": hours_requested
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": f"حدث خطأ أثناء حفظ الطلب: {str(e)}"
        }), 500
@app.route('/api/broadcasts/latest', methods=['GET'])
def get_latest_broadcast():
    if 'employee' not in session:
        return jsonify({"success": False, "message": "يرجى تسجيل الدخول"}), 401
    
    try:
        employee_id = session['employee']['id']
        # جلب الموظف الحالي
        current_employee = Employee.query.get(employee_id)
        if not current_employee:
            return jsonify({"success": False, "message": "المستخدم غير موجود"}), 404
        
        # جلب آخر إشعار "تعميم" للموظف الحالي
        latest_notification = Notification.query.filter(
            Notification.recipient_id == employee_id,
            Notification.message.like('%تعميم%')
        ).order_by(Notification.timestamp.desc()).first()
        
        if not latest_notification:
            return jsonify({
                'success': True,
                'message': 'لا يوجد تعميمات',
                'data': None
            }), 200
        
        # استخراج الرسالة والتاريخ
        message = latest_notification.message
        timestamp = latest_notification.timestamp
        
        # تحديد النوع (عام/خاص) من الرسالة
        broadcast_type = "خاص" if "قسمك" in message else "عام"
        
        # إزالة البادئة إذا كانت موجودة
        if ':' in message:
            message = message.split(':', 1)[1].strip()
        
        return jsonify({
            'success': True,
            'data': {
                'id': latest_notification.id,
                'message': message,
                'timestamp': timestamp.isoformat(),
                'type': broadcast_type
            }
        }), 200
        
    except Exception as e:
        import traceback
        print(f"Error in get_latest_broadcast: {str(e)}")
        print(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'message': f'خطأ في جلب آخر تعميم: {str(e)}'
        }), 500

# جلب الإشعارات للمستخدم الحالي
@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    if 'employee' not in session:
        return jsonify({"message": "يرجى تسجيل الدخول"}), 401
    
    try:
        employee_id = session['employee']['id']
        
        # جلب جميع إشعارات المستخدم غير المقروءة، مرتبة من الأحدث إلى الأقدم
        notifications = Notification.query.filter_by(
            recipient_id=employee_id
        ).order_by(Notification.timestamp.desc()).all()
        
        # تحويل النتائج إلى تنسيق JSON
        notifications_data = []
        for notification in notifications:
            notifications_data.append({
                'id': notification.id,
                'message': notification.message,
                'timestamp': notification.timestamp.isoformat(),
                'is_read': notification.is_read
            })
        
        # حساب عدد الإشعارات غير المقروءة
        unread_count = Notification.query.filter_by(
            recipient_id=employee_id,
            is_read=False
        ).count()
        
        return jsonify({
            'success': True,
            'notifications': notifications_data,
            'unread_count': unread_count
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في جلب الإشعارات: {str(e)}'
        }), 500

# تحديث الإشعارات كمقروءة
@app.route('/api/notifications/mark-as-read', methods=['POST'])
def mark_notifications_as_read():
    if 'employee' not in session:
        return jsonify({"message": "يرجى تسجيل الدخول"}), 401
    
    try:
        employee_id = session['employee']['id']
        
        # تحديث جميع إشعارات المستخدم إلى مقروءة
        Notification.query.filter_by(
            recipient_id=employee_id,
            is_read=False
        ).update({'is_read': True})
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم تحديث الإشعارات كمقروءة'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'خطأ في تحديث الإشعارات: {str(e)}'
        }), 500
@app.route('/api/leave-requests/<int:request_id>', methods=['PUT'])
def update_leave_request(request_id):
    try:
        data = request.get_json()
        new_status = data.get('status')
        new_note = data.get('note')  # الحصول على الملاحظات الجديدة
        
        if not new_status:
            return jsonify({'error': 'حالة الطلب مطلوبة'}), 400
        
        leave_request = LeaveRequest.query.get(request_id)
        
        if not leave_request:
            return jsonify({'error': 'طلب الإجازة غير موجود'}), 404
        
        leave_request.status = new_status
        if new_note is not None:  # إذا تم إرسال ملاحظات، نقوم بتحديثها
            leave_request.note = new_note
        db.session.commit()
        
        return jsonify({
            'message': 'تم تحديث طلب الإجازة بنجاح',
            'new_status': new_status,
            'new_note': new_note
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'خطأ في تحديث الطلب: {str(e)}'}), 500
# جلب جميع طلبات العمل الإضافي
@app.route('/api/admin-overtime-requests', methods=['GET'])
def get_admin_overtime_requests():
    try:
        overtime_requests = AdditionalAttendanceRecord.query.all()
        
        requests_data = []
        for record in overtime_requests:
            department_name = record.employee.department.dep_name if (
                record.employee and 
                record.employee.department
            ) else 'غير محدد'
            requests_data.append({
                'id': record.id,
                'date': record.date.isoformat() if record.date else None,
                'employee_id': record.employee_id,
                'employee_name': record.name,
                'arname': record.arname,
                'role': record.role,
                'is_holiday': record.is_holiday,
                'start_time': record.start_time.strftime('%H:%M') if record.start_time else None,
                'end_time': record.end_time.strftime('%H:%M') if record.end_time else None,
                'add_attendance_minutes': record.add_attendance_minutes,
                'status': record.status,
                'notes': record.notes,
                'department': department_name
            })
        
        return jsonify(requests_data), 200
        
    except Exception as e:
        return jsonify({'error': f'خطأ في جلب طلبات العمل الإضافي: {str(e)}'}), 500

# تحديث حالة طلب العمل الإضافي
@app.route('/api/admin-overtime-requests/<int:request_id>', methods=['PUT'])
def update_admin_overtime_request(request_id):
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({'error': 'حالة الطلب مطلوبة'}), 400
        
        # التحقق من صحة الحالة
        valid_statuses = ['pending', 'approved', 'rejected']
        if new_status not in valid_statuses:
            return jsonify({'error': 'حالة الطلب غير صحيحة'}), 400
        
        overtime_request = AdditionalAttendanceRecord.query.get(request_id)
        
        if not overtime_request:
            return jsonify({'error': 'طلب العمل الإضافي غير موجود'}), 404
        
        overtime_request.status = new_status
        db.session.commit()
        
        return jsonify({
            'message': 'تم تحديث حالة طلب العمل الإضافي بنجاح',
            'new_status': new_status
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'خطأ في تحديث حالة الطلب: {str(e)}'}), 500

# حذف طلب العمل الإضافي
@app.route('/api/admin-overtime-requests/<int:request_id>', methods=['DELETE'])
def delete_admin_overtime_request(request_id):
    try:
        # البحث عن الطلب
        overtime_request = db.session.get(AdditionalAttendanceRecord, request_id)
        
        if not overtime_request:
            return jsonify({'error': 'طلب العمل الإضافي غير موجود'}), 404
        
        # حذف الطلب من قاعدة البيانات
        db.session.delete(overtime_request)
        db.session.commit()
        
        return jsonify({'message': 'تم حذف طلب العمل الإضافي بنجاح'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'خطأ في حذف طلب العمل الإضافي: {str(e)}'}), 500
# تحديث حالة طلب التعويض
@app.route('/api/compensation-requests/<int:request_id>', methods=['PUT'])
def update_compensation_request(request_id):
    try:
        data = request.get_json()
        new_status = data.get('status')
        
        if not new_status:
            return jsonify({'error': 'حالة الطلب مطلوبة'}), 400
        
        comp_request = CompensationLeaveRequest.query.get(request_id)
        
        if not comp_request:
            return jsonify({'error': 'طلب التعويض غير موجود'}), 404
        
        comp_request.status = new_status
        db.session.commit()
        
        return jsonify({
            'message': 'تم تحديث حالة طلب التعويض بنجاح',
            'new_status': new_status
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'خطأ في تحديث حالة الطلب: {str(e)}'}), 500
# دالة لإرسال رسالة تلغرام
def send_telegram_message(chat_id, message, max_retries=3, retry_delay=2, attempt=1):
    """
    إرسال رسالة Telegram مع إعادة المحاولة عند الفشل بدون استخدام time.sleep()
    """
    TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }

    try:
        response = requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
        response.raise_for_status()
        print("✅ تم إرسال الرسالة بنجاح")
        return True

    except requests.exceptions.ConnectionError:
        print(f"🌐 لا يوجد اتصال بالإنترنت أو الحظر مفعل - المحاولة {attempt}/{max_retries}")

    except requests.exceptions.Timeout:
        print(f"⏳ انتهت المهلة - المحاولة {attempt}/{max_retries}")

    except requests.exceptions.RequestException as e:
        print(f"❌ خطأ في Telegram API (المحاولة {attempt}/{max_retries}): {e}")
        if 'response' in locals() and response is not None:
            print(f"📩 تفاصيل الاستجابة: {response.text}")
        if 'response' in locals() and response is not None and response.status_code < 500:
            return False

    # جدولة إعادة المحاولة بدون sleep
    if attempt < max_retries:
        print(f"⏳ سيتم إعادة المحاولة بعد {retry_delay} ثانية...")
        threading.Timer(retry_delay, send_telegram_message,
                        args=(chat_id, message, max_retries, retry_delay, attempt + 1)).start()

# دالة لإرسال التعميم لجميع الموظفين
# def send_broadcast_to_employees(broadcast_message, broadcast_type, department_id=None):
#     """إرسال التعميم للموظفين حسب القسم"""
#     with app.app_context():
#         try:
#             # بناء الاستعلام حسب القسم
#             query = Employee.query.filter(
#                 Employee.telegram_chatid.isnot(None),
#                 Employee.telegram_chatid != ''
#             )
            
#             if department_id:
#                 query = query.filter(Employee.department_id == department_id)
            
#             employees = query.all()
            
#             if not employees:
#                 print(f"لا يوجد موظفين في القسم {department_id} لديهم telegram_chatid")
#                 return
            
#             current_time = current_syria_time().strftime("%Y-%m-%d %I:%M %p")
#             telegram_message = f"""🔔 <b>تعميم {broadcast_type}</b>
# {broadcast_message}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# {current_time}
# 𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡"""

#             success_count = 0
#             failed_count = 0
            
#             for employee in employees:
#                 try:
#                     if send_telegram_message(employee.telegram_chatid, telegram_message):
#                         success_count += 1
#                         print(f"تم إرسال التعميم بنجاح إلى {employee.full_name_arabic}")
#                     else:
#                         failed_count += 1
#                         print(f"فشل إرسال التعميم إلى {employee.full_name_arabic}")
#                 except Exception as e:
#                     failed_count += 1
#                     print(f"خطأ في إرسال التعميم إلى {employee.full_name_arabic}: {str(e)}")
            
#             print(f"✅ تم إرسال التعميم بنجاح إلى {success_count} موظف، وفشل في {failed_count} حالة.")
        
#         except Exception as e:
#             print(f"❌ خطأ في إرسال التعميم: {str(e)}")

# def send_notifications_async(broadcast_message, broadcast_type, department_id=None):
#     thread = threading.Thread(
#         target=send_broadcast_to_employees,
#         args=(broadcast_message, broadcast_type, department_id)
#     )
#     thread.daemon = True
#     thread.start()

# جلب كل الأزرار الخاصة
@app.route('/api/special-buttons', methods=['GET'])
def get_special_buttons():
    try:
        buttons = SpecialButton.query.all()
        result = []

        for button in buttons:
            result.append({
                'id': button.id,
                'employee_id': button.employee_id,
                'department_id': button.department_id,
                'name': button.name,
                'link': button.link
            })

        return jsonify({'success': True, 'data': result}), 200
    except Exception as e:
        return jsonify({'success': False, 'message': f'خطأ في جلب الأزرار الخاصة: {str(e)}'}), 500


# إضافة زر خاص
@app.route('/api/special-buttons', methods=['POST'])
def create_special_button():
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        link = data.get('link', '').strip()
        department_id = data.get('department_id')

        if not all([name, link, department_id]):
            return jsonify({'success': False, 'message': 'جميع الحقول مطلوبة'}), 400

        new_button = SpecialButton(
            name=name,
            link=link,
            department_id=int(department_id),
            employee_id=1  # استخدم ID الموظف المناسب من الجلسة أو الطلب
        )

        db.session.add(new_button)
        db.session.commit()

        return jsonify({'success': True, 'message': 'تم إضافة الزر بنجاح'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'خطأ أثناء الإضافة: {str(e)}'}), 500


# تعديل زر خاص
@app.route('/api/special-buttons/<int:button_id>', methods=['PUT'])
def update_special_button(button_id):
    try:
        button = SpecialButton.query.get(button_id)
        if not button:
            return jsonify({'success': False, 'message': 'الزر غير موجود'}), 404

        data = request.get_json()
        button.name = data.get('name', button.name)
        button.link = data.get('link', button.link)
        button.department_id = int(data.get('department_id', button.department_id))

        db.session.commit()
        return jsonify({'success': True, 'message': 'تم تحديث الزر بنجاح'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'خطأ أثناء التحديث: {str(e)}'}), 500


# حذف زر خاص
@app.route('/api/special-buttons/<int:button_id>', methods=['DELETE'])
def delete_special_button(button_id):
    try:
        button = SpecialButton.query.get(button_id)
        if not button:
            return jsonify({'success': False, 'message': 'الزر غير موجود'}), 404

        db.session.delete(button)
        db.session.commit()
        return jsonify({'success': True, 'message': 'تم حذف الزر بنجاح'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'خطأ أثناء الحذف: {str(e)}'}), 500
@app.route('/api/broadcasts', methods=['GET'])
def get_broadcasts():
    try:
        broadcasts = Broadcast.query.order_by(Broadcast.timestamp.desc()).all()
        
        broadcasts_data = []
        for broadcast in broadcasts:
            broadcasts_data.append({
                'id': broadcast.id,
                'message': broadcast.message,
                'timestamp': broadcast.timestamp.isoformat() if broadcast.timestamp else None
            })
        
        return jsonify({
            'success': True,
            'data': broadcasts_data,
            'message': 'تم جلب التعميمات بنجاح'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في جلب التعميمات: {str(e)}'
        }), 500

# 2. إضافة تعميم جديد
@app.route('/api/broadcasts', methods=['POST'])
def create_broadcast():
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'success': False,
                'message': 'محتوى التعميم مطلوب'
            }), 400
        
        message = data['message'].strip()
        department_id = data.get('department_id')
        
        if not message:
            return jsonify({
                'success': False,
                'message': 'محتوى التعميم لا يمكن أن يكون فارغاً'
            }), 400
        
        # إنشاء التعميم الجديد
        new_broadcast = Broadcast(
            message=message,
            timestamp=current_syria_time()
        )
        
        db.session.add(new_broadcast)
        db.session.commit()
        
        # تحديد المستلمين
        all_recipients = []
        
        if department_id:
            # 1. موظفي القسم المحدد
            department_employees = Employee.query.filter_by(department_id=department_id).all()
            
            # 2. مشرفي القسم المحدد فقط
            department_supervisors = Supervisor.query.filter_by(dep_id=department_id).all()
            supervisor_employees = [db.session.get(Employee, s.supervisor_ID) for s in department_supervisors]
            
            # 3. دمج القائمتين مع إزالة التكرار
            all_recipients = list(set(department_employees + supervisor_employees))
            message_prefix = "تعميم جديد في قسمك"
        else:
            # 1. جميع الموظفين
            all_employees = Employee.query.all()
            
            # 2. جميع المشرفين
            all_supervisors = Supervisor.query.all()
            supervisor_employees = [db.session.get(Employee, s.supervisor_ID) for s in all_supervisors]
            
            # 3. دمج القائمتين مع إزالة التكرار
            all_recipients = list(set(all_employees + supervisor_employees))
            message_prefix = "تعميم عام"
        
        # إضافة إشعار لكل مستلم
        for employee in all_recipients:
            if employee:  # التأكد من وجود الموظف
                notification = Notification(
                    recipient_id=employee.id,
                    message=f"{message_prefix}: {message}",
                    timestamp=datetime.now(pytz.timezone("Asia/Damascus")),
                    is_read=False
                )
                db.session.add(notification)
        
        db.session.commit()
        
        # إرسال التلغرام فقط للموظفين في القسم المحدد
        send_telegram_broadcast_async(message, department_id, message_prefix)
        
        return jsonify({
            'success': True,
            'message': 'تم إضافة التعميم بنجاح وإرسال الإشعارات للمستلمين',
            'data': {
                'id': new_broadcast.id,
                'message': new_broadcast.message,
                'timestamp': new_broadcast.timestamp.isoformat(),
                'notifications_sent': len(all_recipients)
            }
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'خطأ في إضافة التعميم: {str(e)}'
        }), 500

def send_telegram_broadcast_async(broadcast_message, department_id, message_prefix):
    """إرسال التعميم للموظفين عبر التلغرام بشكل غير متزامن"""
    def task():
        with app.app_context():
            try:
                # تحديد المستلمين
                telegram_recipients = []
                
                if department_id:
                    # 1. موظفو القسم المحدد
                    department_employees = Employee.query.filter(
                        Employee.department_id == department_id,
                        Employee.telegram_chatid.isnot(None),
                        Employee.telegram_chatid != ''
                    ).all()
                    
                    # 2. مشرفو القسم المحدد فقط
                    department_supervisors = Supervisor.query.filter_by(dep_id=department_id).all()
                    supervisor_employees = [
                        db.session.get(Employee, s.supervisor_ID) 
                        for s in department_supervisors
                        if db.session.get(Employee, s.supervisor_ID) and
                        db.session.get(Employee, s.supervisor_ID).telegram_chatid
                    ]
                    
                    # 3. الدمج
                    telegram_recipients = list(set(department_employees + supervisor_employees))
                    
                else:
                    # 1. جميع الموظفين
                    all_employees = Employee.query.filter(
                        Employee.telegram_chatid.isnot(None),
                        Employee.telegram_chatid != ''
                    ).all()
                    
                    # 2. جميع المشرفين
                    all_supervisors = Supervisor.query.all()
                    supervisor_employees = [
                        db.session.get(Employee, s.supervisor_ID) 
                        for s in all_supervisors
                        if db.session.get(Employee, s.supervisor_ID) and
                        db.session.get(Employee, s.supervisor_ID).telegram_chatid
                    ]
                    
                    # 3. الدمج
                    telegram_recipients = list(set(all_employees + supervisor_employees))
                
                if not telegram_recipients:
                    print(f"لا يوجد مستلمين لديهم telegram_chatid")
                    return
                
                current_time = current_syria_time().strftime("%Y-%m-%d %I:%M %p")
                telegram_message = f"""🔔 <b>{message_prefix}</b>
{broadcast_message}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{current_time}
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡"""

                success_count = 0
                failed_count = 0
                
                for employee in telegram_recipients:
                    try:
                        if send_telegram_message(employee.telegram_chatid, telegram_message):
                            success_count += 1
                        else:
                            failed_count += 1
                    except Exception as e:
                        failed_count += 1
                        print(f"خطأ في إرسال التلغرام: {str(e)}")
                
                print(f"✅ تم إرسال التعميم عبر التلغرام بنجاح إلى {success_count} موظف، وفشل في {failed_count} حالة.")
            
            except Exception as e:
                print(f"❌ خطأ في إرسال التعميم عبر التلغرام: {str(e)}")
    
    # تشغيل المهمة في خيط منفصل
    thread = threading.Thread(target=task)
    thread.daemon = True
    thread.start()
# 3. حذف تعميم
@app.route('/api/broadcasts/<int:broadcast_id>', methods=['DELETE'])
def delete_broadcast(broadcast_id):
    try:
        # البحث عن التعميم المطلوب
        broadcast = Broadcast.query.get(broadcast_id)
        
        if not broadcast:
            return jsonify({
                'success': False,
                'message': 'التعميم غير موجود'
            }), 404
        
        # حذف التعميم
        db.session.delete(broadcast)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم حذف التعميم بنجاح'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'خطأ في حذف التعميم: {str(e)}'
        }), 500
# 5. جلب تعميم محدد
@app.route('/api/broadcasts/<int:broadcast_id>', methods=['GET'])
def get_broadcast(broadcast_id):
    try:
        broadcast = Broadcast.query.get(broadcast_id)
        if not broadcast:
            return jsonify({
                'success': False,
                'message': 'التعميم غير موجود'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'id': broadcast.id,
                'message': broadcast.message,
                'timestamp': broadcast.timestamp.isoformat() if broadcast.timestamp else None
            }
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في جلب التعميم: {str(e)}'
        }), 500

# 6. إرسال تعميم موجود مرة أخرى
@app.route('/api/broadcasts/<int:broadcast_id>/resend', methods=['POST'])
def resend_broadcast(broadcast_id):
    try:
        broadcast = Broadcast.query.get(broadcast_id)
        if not broadcast:
            return jsonify({
                'success': False,
                'message': 'التعميم غير موجود'
            }), 404
        
        # إرسال التعميم مرة أخرى
        resend_message = f"إعادة إرسال التعميم:\n\n{broadcast.message}"
        send_notifications_async(resend_message, "معاد الإرسال")
        
        return jsonify({
            'success': True,
            'message': 'تم إعادة إرسال التعميم بنجاح'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في إعادة إرسال التعميم: {str(e)}'
        }), 500

# 7. اختبار اتصال التلغرام
@app.route('/api/broadcasts/test-telegram', methods=['POST'])
def test_telegram_connection():
    try:
        data = request.get_json()
        test_chat_id = data.get('chat_id')
        
        if not test_chat_id:
            return jsonify({
                'success': False,
                'message': 'chat_id مطلوب للاختبار'
            }), 400
        
        test_message = "🔔 رسالة اختبار من نظام إدارة الموظفين"
        
        if send_telegram_message(test_chat_id, test_message):
            return jsonify({
                'success': True,
                'message': 'تم إرسال رسالة الاختبار بنجاح'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'فشل في إرسال رسالة الاختبار'
            }), 500
    
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في اختبار التلغرام: {str(e)}'
        }), 500
# جلب جميع الإجازات الرسمية
@app.route('/api/official-holidays', methods=['GET'])
def get_official_holidays():
    try:
        holidays = OfficialHoliday.query.order_by(OfficialHoliday.holiday_date).all()
        return jsonify({
            'success': True,
            'data': [holiday.to_dict() for holiday in holidays]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في جلب البيانات: {str(e)}'
        }), 500

# إضافة إجازة رسمية جديدة
@app.route('/api/official-holidays', methods=['POST'])
def add_official_holiday():
    try:
        data = request.get_json()

        if not data.get('holiday_date') or not data.get('description'):
            return jsonify({
                'success': False,
                'message': 'الرجاء ملء جميع الحقول المطلوبة'
            }), 400

        holiday_date = datetime.strptime(data['holiday_date'], '%Y-%m-%d').date()

        existing_holiday = OfficialHoliday.query.filter_by(holiday_date=holiday_date).first()
        if existing_holiday:
            return jsonify({
                'success': False,
                'message': 'يوجد عطلة رسمية مسجلة بنفس التاريخ'
            }), 400

        new_holiday = OfficialHoliday(
            holiday_date=holiday_date,
            description=data['description'].strip()
        )

        db.session.add(new_holiday)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'تم إضافة يوم العطلة الرسمي بنجاح',
            'data': new_holiday.to_dict()
        }), 201

    except ValueError:
        return jsonify({
            'success': False,
            'message': 'تنسيق التاريخ غير صحيح'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'خطأ في إضافة العطلة: {str(e)}'
        }), 500

# تحديث إجازة رسمية
@app.route('/api/official-holidays/<int:holiday_id>', methods=['PUT'])
def update_official_holiday(holiday_id):
    try:
        holiday = OfficialHoliday.query.get_or_404(holiday_id)
        data = request.get_json()

        if not data.get('holiday_date') or not data.get('description'):
            return jsonify({
                'success': False,
                'message': 'الرجاء ملء جميع الحقول المطلوبة'
            }), 400

        holiday_date = datetime.strptime(data['holiday_date'], '%Y-%m-%d').date()

        existing_holiday = OfficialHoliday.query.filter(
            OfficialHoliday.holiday_date == holiday_date,
            OfficialHoliday.id != holiday_id
        ).first()
        if existing_holiday:
            return jsonify({
                'success': False,
                'message': 'يوجد عطلة رسمية مسجلة بنفس التاريخ'
            }), 400

        holiday.holiday_date = holiday_date
        holiday.description = data['description'].strip()

        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'تم تحديث يوم العطلة الرسمي بنجاح',
            'data': holiday.to_dict()
        })

    except ValueError:
        return jsonify({
            'success': False,
            'message': 'تنسيق التاريخ غير صحيح'
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'خطأ في تحديث العطلة: {str(e)}'
        }), 500

# حذف إجازة رسمية
@app.route('/api/official-holidays/<int:holiday_id>', methods=['DELETE'])
def delete_official_holiday(holiday_id):
    try:
        holiday = OfficialHoliday.query.get_or_404(holiday_id)

        db.session.delete(holiday)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'تم حذف يوم العطلة الرسمي بنجاح'
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'خطأ في حذف العطلة: {str(e)}'
        }), 500
# POST - إضافة حقل مخصص جديد لجميع الموظفين
@app.route('/api/custom-fields', methods=['POST'])
def add_custom_field():
    try:
        data = request.get_json()
        field_name = data.get('field_name')
        
        if not field_name:
            return jsonify({'error': 'اسم الحقل مطلوب'}), 400
            
        # التحقق من عدم وجود حقل بنفس الاسم
        existing_field = EmployeeCustomField.query.filter_by(field_name=field_name).first()
        if existing_field:
            return jsonify({'error': 'يوجد حقل بهذا الاسم بالفعل'}), 409
            
        # إضافة الحقل لجميع الموظفين الموجودين
        employees = Employee.query.all()
        
        for employee in employees:
            new_field = EmployeeCustomField(
                employee_id=employee.id,
                field_name=field_name,
                field_value=''  # قيمة فارغة في البداية
            )
            db.session.add(new_field)
            
        db.session.commit()
        
        return jsonify({
            'field_name': field_name,
            'message': f'تم إضافة الحقل لـ {len(employees)} موظف'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# PUT - تحديث اسم حقل مخصص لجميع الموظفين
# GET - جلب جميع الحقول المخصصة المتاحة
@app.route('/api/custom-fields', methods=['GET'])
def get_all_custom_fields():
    try:
        # جلب جميع أسماء الحقول المخصصة (بدون تكرار)
        distinct_fields = db.session.query(EmployeeCustomField.field_name).distinct().all()
        
        result = []
        for i, field in enumerate(distinct_fields, 1):
            # عدد الموظفين الذين لديهم هذا الحقل
            employee_count = EmployeeCustomField.query.filter_by(field_name=field[0]).count()
            result.append({
                'id': i,  # معرف فريد لكل حقل
                'field_name': field[0],
                'employee_count': employee_count
            })
            
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


from urllib.parse import unquote

# GET - جلب قيم الحقول المخصصة لموظف معين
@app.route('/api/employees/<int:employee_id>/custom-fields', methods=['GET'])
def get_employee_custom_fields(employee_id):
    try:
        # استخدام الطريقة الحديثة بدلاً من query.get()
        custom_fields = EmployeeCustomField.query.filter_by(employee_id=employee_id).all()
        
        result = []
        for field in custom_fields:
            result.append({
                'id': field.id,
                'field_name': field.field_name,
                'field_value': field.field_value
            })
            
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/employees/<int:employee_id>/custom-fields', methods=['PUT'])
def update_employee_custom_fields(employee_id):
    try:
        print(f"Updating custom fields for employee {employee_id}")
        
        # التحقق من وجود الموظف
        employee = db.session.get(Employee, employee_id)
        if not employee:
            return jsonify({'error': 'Employee not found'}), 404
        
        # جلب بيانات الطلب
        update_data = request.get_json()
        print(f"Received data: {update_data}")
        
        # التحقق من صحة البيانات
        if not isinstance(update_data, dict):
            return jsonify({'error': 'Invalid data format. Expected a JSON object.'}), 400
        
        if not update_data:
            return jsonify({'error': 'No data provided'}), 400
        
        # جلب الحقول الحالية للموظف
        current_fields = EmployeeCustomField.query.filter_by(employee_id=employee_id).all()
        print(f"Current fields count: {len(current_fields)}")
        
        # إنشاء قاموس لتسهيل الوصول
        current_field_map = {field.field_name: field for field in current_fields}
        
        updated_count = 0
        added_count = 0
        
        # معالجة التحديثات
        for field_name, new_value in update_data.items():
            print(f"Processing field: {field_name} = {new_value}")
            
            # إذا كان الحقل موجودًا - تحديث القيمة
            if field_name in current_field_map:
                old_value = current_field_map[field_name].field_value
                if old_value != new_value:
                    current_field_map[field_name].field_value = new_value
                    updated_count += 1
                    print(f"Updated field '{field_name}': '{old_value}' -> '{new_value}'")
            # إذا كان جديدًا - إضافة حقل
            else:
                new_field = EmployeeCustomField(
                    employee_id=employee_id,
                    field_name=field_name,
                    field_value=new_value
                )
                db.session.add(new_field)
                added_count += 1
                print(f"Added new field '{field_name}': '{new_value}'")
        
        # حذف الحقول غير المرسلة في الطلب (اختياري - قد تريد تعطيل هذا)
        deleted_count = 0
        for field_name in list(current_field_map.keys()):
            if field_name not in update_data:
                db.session.delete(current_field_map[field_name])
                deleted_count += 1
                print(f"Deleted field '{field_name}'")
        
        # حفظ التغييرات
        db.session.commit()
        
        print(f"Changes committed: {updated_count} updated, {added_count} added, {deleted_count} deleted")
        
        return jsonify({
            'message': 'Custom fields updated successfully',
            'employee_id': employee_id,
            'changes': {
                'updated': updated_count,
                'added': added_count,
                'deleted': deleted_count
            }
        }), 200
        
    except Exception as e:
        print(f"Error updating custom fields: {str(e)}")
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
# PUT - تحديث قيم الحقول المخصصة لموظف معين
@app.route('/api/custom-fields/<field_name>', methods=['PUT'])
def update_custom_field(field_name):
    try:
        # فك تشفير اسم الحقل من URL
        old_field_name = unquote(field_name)
        
        data = request.get_json()
        new_field_name = data.get('field_name')
       
        if not new_field_name:
            return jsonify({'error': 'اسم الحقل الجديد مطلوب'}), 400
       
        # التحقق من وجود الحقل الحالي
        existing_fields = EmployeeCustomField.query.filter_by(field_name=old_field_name).all()
        if not existing_fields:
            return jsonify({'error': 'لم يتم العثور على الحقل'}), 404
       
        # التحقق من عدم وجود حقل آخر بنفس الاسم الجديد
        if old_field_name != new_field_name:
            duplicate_field = EmployeeCustomField.query.filter_by(field_name=new_field_name).first()
            if duplicate_field:
                return jsonify({'error': 'يوجد حقل بهذا الاسم بالفعل'}), 409
           
        # تحديث اسم الحقل لجميع الموظفين
        updated_count = EmployeeCustomField.query.filter_by(field_name=old_field_name).update(
            {'field_name': new_field_name}
        )
       
        db.session.commit()
       
        return jsonify({
            'old_field_name': old_field_name,
            'new_field_name': new_field_name,
            'message': f'تم تحديث الحقل لـ {updated_count} موظف'
        }), 200
       
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
# إضافة endpoint جديد للحذف
# إضافة endpoint جديد للحذف
@app.route('/api/custom-fields/<field_name>', methods=['DELETE'])
def delete_custom_field_by_name(field_name):
    try:
        # فك تشفير اسم الحقل من URL
        field_name = unquote(field_name)
        
        # التحقق من وجود الحقل
        existing_fields = EmployeeCustomField.query.filter_by(field_name=field_name).all()
        if not existing_fields:
            return jsonify({'error': 'لم يتم العثور على الحقل'}), 404
       
        # حذف الحقل من جميع الموظفين
        deleted_count = EmployeeCustomField.query.filter_by(field_name=field_name).delete()
       
        db.session.commit()
       
        return jsonify({
            'message': f'تم حذف الحقل من {deleted_count} موظف'
        }), 200
       
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
# إضافة حقل مخصص لموظف جديد عند إنشائه
def add_existing_custom_fields_to_new_employee(employee_id):
    try:
        # جلب جميع أسماء الحقول المخصصة الموجودة
        existing_field_names = db.session.query(EmployeeCustomField.field_name).distinct().all()
        
        for field_name_tuple in existing_field_names:
            field_name = field_name_tuple[0]
            
            # التحقق من عدم وجود الحقل للموظف الجديد
            existing_field = EmployeeCustomField.query.filter_by(
                employee_id=employee_id,
                field_name=field_name
            ).first()
            
            if not existing_field:
                new_field = EmployeeCustomField(
                    employee_id=employee_id,
                    field_name=field_name,
                    field_value=''  # قيمة فارغة في البداية
                )
                db.session.add(new_field)
        
        db.session.commit()
        return True
        
    except Exception as e:
        db.session.rollback()
        print(f"خطأ في إضافة الحقول المخصصة للموظف الجديد: {e}")
        return False


@app.route('/api/leave-requests', methods=['GET'])
def get_leave_requests():
    # ترتيب النتائج حسب تاريخ البداية من الأحدث إلى الأقدم
    requests = LeaveRequest.query.join(Employee).join(Department).order_by(LeaveRequest.start_date.desc()).all()
    results = []
    for req in requests:
        leave_data = {
            "id": req.id,
            "employee_name": req.employee.full_name_arabic,
            "department": req.employee.department.dep_name if req.employee.department else None,
            "classification": req.classification,
            "status": req.status,
            "start_date": req.start_date.strftime('%Y-%m-%d'),
            "type": req.type,
            "note": req.note
        }
        # إرسال end_date بنفس قيمة start_date إذا كانت الإجازة يومية أو ساعية
        if req.type in ['daily', 'hourly']:
            leave_data["end_date"] = req.start_date.strftime('%Y-%m-%d')
        else:
            leave_data["end_date"] = req.end_date.strftime('%Y-%m-%d') if req.end_date else None
        results.append(leave_data)
    return jsonify(results)
@app.route('/api/employees-list', methods=['GET'])
def get_employees_list():
    try:
        # استرجاع جميع الموظفين بدون فلترة على status
        employees = Employee.query.filter(Employee.role != 'ادمن').all()
        # تحويل البيانات إلى JSON مع الحقول المطلوبة فقط
        employees_data = [
            {
                'id': emp.id,
                'name': emp.full_name_arabic,
                'employee_number': emp.employee_number
            }
            for emp in employees
        ]

        return jsonify(employees_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/test-db-connection')
def test_db_connection():
    try:
        # تنفيذ استعلام بسيط: عد الموظفين
        count = db.session.query(Employee).count()
        return jsonify({
            'status': 'success',
            'message': 'Database connection successful.',
            'employee_count': count
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Database connection failed.',
            'error': str(e)
        }), 500
# Flask Route لحذف الموظف
@app.route('/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        # العثور على الموظف
        employee = db.session.get(Employee, employee_id)

        
        if not employee:
            return jsonify({
                'success': False,
                'message': 'الموظف غير موجود'
            }), 404
        
        # حفظ اسم الموظف للرسالة
        employee_name = employee.full_name_arabic
        
        # حذف الموظف - SQLAlchemy سيحذف جميع العلاقات تلقائياً بسبب cascade="all, delete-orphan"
        db.session.delete(employee)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'تم حذف الموظف "{employee_name}" وجميع بياناته المرتبطة بنجاح'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'حدث خطأ أثناء حذف الموظف: {str(e)}'
        }), 500
@app.route('/api/my-leave-requests', methods=['GET'])
def get_my_leave_requests():
    # التحقق من وجود جلسة للموظف
    if 'employee' not in session:
        return jsonify({"message": "غير مسجل دخول"}), 401

    employee_id = session['employee']['id']
    
    # استعلام عن طلبات الإجازة الخاصة بالموظف الحالي فقط
    requests = LeaveRequest.query.filter_by(employee_id=employee_id).order_by(LeaveRequest.start_date.desc()).all()
    
    results = []
    for req in requests:
        leave_data = {
            "id": req.id,
            "classification": req.classification,
            "type": req.type,
            "start_date": req.start_date.strftime('%Y-%m-%d'),
            "end_date": req.end_date.strftime('%Y-%m-%d') if req.end_date else None,
            "start_time": req.start_time.strftime('%H:%M') if req.start_time else None,
            "end_time": req.end_time.strftime('%H:%M') if req.end_time else None,
            "hours_requested": req.hours_requested,
            "note": req.note,  # <-- استبدل reason بـ note
            "status": req.status,
            "created_at": req.timestamp.strftime('%Y-%m-%d %H:%M:%S') if req.timestamp else None

        }
        
        # إذا كانت الإجازة يومية أو ساعية، نعرض تاريخ البداية فقط في end_date
        if req.type in ['daily', 'hourly']:
            leave_data["end_date"] = req.start_date.strftime('%Y-%m-%d')
        
        results.append(leave_data)
    
    return jsonify(results)

@app.route('/api/employees', methods=['POST'])
def add_employee():
    try:
        data = request.form
        print("📦 البيانات المستلمة:", data.to_dict())
        profile_image = request.files.get('profile_image')
        
        # التحقق من الحقول المطلوبة
        required_fields = [
            'full_name_arabic', 'full_name_english', 'employee_number', 'email', 'password',
            'phone', 'department_id', 'position', 'position_english', 'role', 'weekly_day_off',
            'work_start_time', 'work_end_time', 'date_of_joining', 'study_major', 'governorate',
            'date_of_birth', 'national_id', 'job_level', 'employee_status', 'work_location', 'work_nature'
        ]
        
        errors = {}
        for field in required_fields:
            if not data.get(field):
                errors[field] = f"الحقل {field} مطلوب."
        
        if errors:
            return jsonify({'errors': errors}), 400
        
        # التحقق من تكرار البريد الإلكتروني
        if Employee.query.filter_by(email=data.get('email')).first():
            return jsonify({'errors': {'email': 'هذا البريد الإلكتروني مستخدم بالفعل.'}}), 400
        
        # التحقق من تكرار الرقم الوظيفي
        if Employee.query.filter_by(employee_number=data.get('employee_number')).first():
            return jsonify({'errors': {'employee_number': 'هذا الرقم الوظيفي مستخدم بالفعل، يرجى استخدام رقم آخر.'}}), 400
        
        # التحقق من تكرار الرقم الوطني
        if Employee.query.filter_by(national_id=data.get('national_id')).first():
            return jsonify({'errors': {'national_id': 'هذا الرقم الوطني مستخدم بالفعل.'}}), 400
        
        # التحقق من وجود مشرف آخر في القسم
        if data.get('role') == 'مشرف' and data.get('department_id'):
            if Employee.query.filter(Employee.department_id == data.get('department_id'),
                                     Employee.role == 'مشرف').first():
                return jsonify({'errors': {'role': 'تم رفض العملية: لا يمكن وجود أكثر من مشرف في نفس القسم.'}}), 400
        
        # رفع الصورة إن وجدت
        image_url = None
        if profile_image:
            result = cloudinary.uploader.upload(profile_image)
            image_url = result["secure_url"]
        
        # دوال مساعدة
        def parse_int(value):
            try:
                return int(value)
            except (ValueError, TypeError):
                return 0
        
        def parse_float(value):
            try:
                return float(value)
            except (ValueError, TypeError):
                return 0.0
        
        def parse_date(value):
            try:
                return datetime.strptime(value, '%Y-%m-%d').date() if value else None
            except ValueError:
                return None
        
        def parse_time(value):
            try:
                return datetime.strptime(value, '%H:%M').time() if value else None
            except ValueError:
                return None
        
        # تعيين قيم الإجازات الافتراضية
        regular_hours = parse_float(data.get('regular_leave_hours'))
        sick_hours = parse_float(data.get('sick_leave_hours'))
        emergency_hours = parse_float(data.get('emergency_leave_hours'))
        
        # إنشاء سجل الموظف
        new_employee = Employee(
            full_name_arabic=data.get('full_name_arabic'),
            full_name_english=data.get('full_name_english'),
            employee_number=data.get('employee_number'),
            email=data.get('email'),
            password=data.get('password'),
            profile_image=image_url,
            telegram_chatid=data.get('telegram_chatid'),
            phone=data.get('phone'),
            department_id=parse_int(data.get('department_id')),
            position=data.get('position'),
            position_english=data.get('position_english'),
            role=data.get('role'),
            bank_account=data.get('bank_account'),
            address=data.get('address'),
            weekly_day_off=data.get('weekly_day_off'),
            work_start_time=parse_time(data.get('work_start_time')),
            work_end_time=parse_time(data.get('work_end_time')),
            date_of_joining=parse_date(data.get('date_of_joining')),
            notes=data.get('notes'),
            study_major=data.get('study_major'),
            governorate=data.get('governorate'),
            relative_phone=data.get('relative_phone'),
            relative_relation=data.get('relative_relation'),
            date_of_birth=parse_date(data.get('date_of_birth')),
            national_id=data.get('national_id'),
            job_level=data.get('job_level'),
            promotion=data.get('promotion'),
            career_stages=data.get('career_stages'),
            employee_status=data.get('employee_status'),
            work_location=data.get('work_location'),
            work_nature=data.get('work_nature'),
            marital_status=data.get('marital_status'),
            nationality=data.get('nationality'),
            trainings=data.get('trainings'),
            external_privileges=data.get('external_privileges'),
            special_leave_record=data.get('special_leave_record'),
            drive_folder_link=data.get('drive_folder_link'),
            status=data.get('status', 'off'),
            is_leave=data.get('is_leave', 'off'),
            is_vacation=data.get('is_vacation', 'off'),
            is_weekly_day_off=data.get('is_weekly_day_off', 'off'),
            regular_leave_hours=regular_hours,
            sick_leave_hours=sick_hours,
            emergency_leave_hours=emergency_hours,
            regular_leave_total=regular_hours,
            regular_leave_used=0.0,
            regular_leave_remaining=regular_hours,
            sick_leave_total=sick_hours,
            sick_leave_used=0.0,
            sick_leave_remaining=sick_hours,
            emergency_leave_total=emergency_hours,
            emergency_leave_used=0.0,
            emergency_leave_remaining=emergency_hours
        )
        
        db.session.add(new_employee)
        db.session.commit()
        
        # إضافة الحقول المخصصة
        field_names = db.session.query(distinct(EmployeeCustomField.field_name)).all()
        for (field_name,) in field_names:
            db.session.add(EmployeeCustomField(
                employee_id=new_employee.id,
                field_name=field_name,
                field_value=''
            ))
        db.session.commit()
        
        # إضافة مكونات الراتب
        salary_components = data.get('salary_components')
        if salary_components:
            try:
                salary_data = json.loads(salary_components)
                db.session.add(SalaryComponent(
                    employee_id=new_employee.id,
                    base_salary=parse_int(salary_data.get('base_salary')),
                    hour_salary=parse_float(salary_data.get('hour_salary')),
                    overtime_rate=parse_float(salary_data.get('overtime_rate')),
                    holiday_overtime_rate=parse_float(salary_data.get('holiday_overtime_rate')),
                    internet_allowance=parse_float(salary_data.get('internet_allowance')),
                    transport_allowance=parse_float(salary_data.get('transport_allowance')),
                    depreciation_allowance=parse_int(salary_data.get('depreciation_allowance')),
                    administrative_allowance=parse_int(salary_data.get('administrative_allowance')),
                    administrative_deduction=parse_int(salary_data.get('administrative_deduction'))
                ))
                db.session.commit()
            except Exception as e:
                print(f"❌ خطأ في إضافة مكونات الراتب: {str(e)}")
        
        return jsonify({'message': 'تمت إضافة الموظف بنجاح'}), 201
    
    except Exception as e:
        print("🚨 خطأ أثناء إضافة الموظف:")
        traceback.print_exc()
        return jsonify({'message': 'حدث خطأ أثناء إضافة الموظف', 'error': str(e)}), 500
# 1. جلب جميع الموظفين
# 1. جلب جميع الموظفين
@app.route('/api/employees', methods=['GET'])
def get_employees():
    try:
        employees = Employee.query.filter(Employee.role != 'ادمن').all()
        employees_list = []
        
        for emp in employees:
            # جلب الحقول المخصصة لكل موظف
            custom_fields = EmployeeCustomField.query.filter_by(employee_id=emp.id).all()
            custom_fields_data = [
                {'id': f.id, 'field_name': f.field_name, 'field_value': f.field_value}
                for f in custom_fields
            ]
            
            employee_data = {
                # الحقول الأساسية
                'id': emp.id,
                'name': emp.full_name_arabic,
                'full_name_english': emp.full_name_english,  # تم التعديل هنا
                'employee_id': emp.employee_number,
                'department': emp.department.dep_name if emp.department else 'غير محدد',
                'position': emp.position,
                'position_english': emp.position_english,
                'email': emp.email,
                'phone': emp.phone,
                'status': emp.status,
                'role': emp.role,
                'work_start_time': emp.work_start_time.strftime('%H:%M') if emp.work_start_time else None,
                'work_end_time': emp.work_end_time.strftime('%H:%M') if emp.work_end_time else None,
                'date_of_joining': emp.date_of_joining.strftime('%Y-%m-%d') if emp.date_of_joining else None,
                'end_of_service_date': emp.end_of_service_date.strftime('%Y-%m-%d') if emp.end_of_service_date else None,
                'weekly_day_off': emp.weekly_day_off,
                'profile_image': emp.profile_image,
                'telegram_chatid': emp.telegram_chatid,
                'bank_account': emp.bank_account,
                'address': emp.address,
                'notes': emp.notes,

                # الحالات والإجازات
                'is_leave': emp.is_leave,
                'is_vacation': emp.is_vacation,
                'is_weekly_day_off': emp.is_weekly_day_off,
                'regular_leave_hours': emp.regular_leave_hours,
                'sick_leave_hours': emp.sick_leave_hours,
                'emergency_leave_hours': emp.emergency_leave_hours,

                # الحقول الجديدة
                'study_major': emp.study_major,
                'governorate': emp.governorate,
                'relative_phone': emp.relative_phone,
                'relative_relation': emp.relative_relation,
                'date_of_birth': emp.date_of_birth.strftime('%Y-%m-%d') if emp.date_of_birth else None,
                'national_id': emp.national_id,
                'job_level': emp.job_level,
                'promotion': emp.promotion,
                'career_stages': emp.career_stages,
                'employee_status': emp.employee_status,
                'work_location': emp.work_location,
                'work_nature': emp.work_nature,
                'marital_status': emp.marital_status,
                'nationality': emp.nationality,
                'trainings': emp.trainings,
                'external_privileges': emp.external_privileges,
                'special_leave_record': emp.special_leave_record,
                'drive_folder_link': emp.drive_folder_link,
                
                # الحقول المخصصة
                'custom_fields': custom_fields_data
            }
            employees_list.append(employee_data)
        
        return jsonify(employees_list), 200
    
    except Exception as e:
        return jsonify({'error': f'فشل في جلب بيانات الموظفين: {str(e)}'}), 500
@app.route('/api/employee/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    try:
        # جلب بيانات الموظف الأساسية
        employee = db.session.get(Employee, employee_id)
        if not employee:
            return jsonify({'message': 'Employee not found'}), 404

        # جلب الحقول المخصصة للموظف
        custom_fields = EmployeeCustomField.query.filter_by(employee_id=employee_id).all()
        custom_fields_data = [{
            'id': field.id,
            'field_name': field.field_name,
            'field_value': field.field_value
        } for field in custom_fields]

        # جلب بيانات الراتب
        salary_component = SalaryComponent.query.filter_by(employee_id=employee_id).first()

        # ✅ بناء رابط الصورة بشكل صحيح
        if employee.profile_image and not employee.profile_image.startswith('http'):
            image_url = f"{request.host_url.rstrip('/')}/static/uploads/{employee.profile_image}"
        else:
            image_url = employee.profile_image

        department = db.session.get(Department, employee.department_id)

        # تجهيز بيانات الإرجاع (محدث مع الحقول الجديدة)
        employee_data = {
            'id': employee.id,
            'full_name_arabic': employee.full_name_arabic,
            'full_name_english': employee.full_name_english,
            'employee_number': employee.employee_number,
            'email': employee.email,
            'password': employee.password,
            'profile_image': image_url,
            'telegram_chatid': employee.telegram_chatid,
            'phone': employee.phone,
            'department': department.dep_name if department else None,
            'department_id': employee.department_id,
            'position': employee.position,
            'position_english': employee.position_english,
            'role': employee.role,
            'bank_account': employee.bank_account,
            'address': employee.address,
            'notes': employee.notes,
            'weekly_day_off': employee.weekly_day_off,
            'work_start_time': str(employee.work_start_time) if employee.work_start_time else None,
            'work_end_time': str(employee.work_end_time) if employee.work_end_time else None,
            'date_of_joining': str(employee.date_of_joining) if employee.date_of_joining else None,
            'is_leave': employee.is_leave,
            'is_vacation': employee.is_vacation,
            'is_weekly_day_off': employee.is_weekly_day_off,
            'regular_leave_hours': employee.regular_leave_hours,
            'sick_leave_hours': employee.sick_leave_hours,
            'emergency_leave_hours': employee.emergency_leave_hours,

            # ✅ الحقول الجديدة
            'study_major': employee.study_major,
            'governorate': employee.governorate,
            'relative_phone': employee.relative_phone,
            'relative_relation': employee.relative_relation,
            'date_of_birth': str(employee.date_of_birth) if employee.date_of_birth else None,
            'national_id': employee.national_id,
            'job_level': employee.job_level,
            'promotion': employee.promotion,
            'career_stages': employee.career_stages,
            'employee_status': employee.employee_status,
            'work_location': employee.work_location,
            'work_nature': employee.work_nature,
            'marital_status': employee.marital_status,
            'nationality': employee.nationality,
            'trainings': employee.trainings,
            'external_privileges': employee.external_privileges,
            'special_leave_record': employee.special_leave_record,
            'drive_folder_link': employee.drive_folder_link,

            # الحقول المخصصة والراتب
            'custom_fields': custom_fields_data,
            'salary_components': None,
            'allowances': {},
            'deductions': {}
        }

        # إضافة بيانات الراتب إذا وجدت
        if salary_component:
            employee_data['salary_components'] = {
                'base_salary': salary_component.base_salary,
                'hour_salary': float(salary_component.hour_salary) if salary_component.hour_salary else None,
                'overtime_rate': salary_component.overtime_rate,
                'holiday_overtime_rate': salary_component.holiday_overtime_rate,
                'internet_allowance': salary_component.internet_allowance,
                'transport_allowance': salary_component.transport_allowance,
                'depreciation_allowance': salary_component.depreciation_allowance,
                'administrative_allowance': salary_component.administrative_allowance,
                'administrative_deduction': salary_component.administrative_deduction
            }

            # بدلات وخصومات
            employee_data['allowances'] = {
                'بدل انترنت': salary_component.internet_allowance or 0,
                'بدل نقل': salary_component.transport_allowance or 0,
            }
            employee_data['deductions'] = {
                'خصم إداري': salary_component.administrative_deduction or 0,
            }

        return jsonify(employee_data), 200

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({'message': str(e)}), 500
@app.route('/api/employee/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    try:
        data = request.get_json()
        employee = db.session.get(Employee, employee_id)
        
        if not employee:
            return jsonify({'message': 'Employee not found'}), 404
        
        # -------------------------
        # تحديث الحقول الأساسية
        # -------------------------
        employee.full_name_arabic = data.get('full_name_arabic', employee.full_name_arabic)
        employee.full_name_english = data.get('full_name_english', employee.full_name_english)
        employee.employee_number = data.get('employee_number', employee.employee_number)
        employee.email = data.get('email', employee.email)
        employee.password = data.get('password', employee.password)

        # -------------------------
        # الحقول الجديدة
        # -------------------------
        employee.study_major = data.get('study_major', employee.study_major)
        employee.governorate = data.get('governorate', employee.governorate)
        employee.relative_phone = data.get('relative_phone', employee.relative_phone)
        employee.date_of_birth = data.get('date_of_birth', employee.date_of_birth)
        employee.national_id = data.get('national_id', employee.national_id)
        employee.nationality = data.get('nationality', employee.nationality)
        employee.marital_status = data.get('marital_status', employee.marital_status)
        employee.relative_relation = data.get('relative_relation', employee.relative_relation)
        employee.position_english = data.get('position_english', employee.position_english)
        employee.job_level = data.get('job_level', employee.job_level)
        employee.employee_status = data.get('employee_status', employee.employee_status)
        employee.work_location = data.get('work_location', employee.work_location)
        employee.work_nature = data.get('work_nature', employee.work_nature)
        employee.promotion = data.get('promotion', employee.promotion)
        employee.career_stages = data.get('career_stages', employee.career_stages)
        employee.trainings = data.get('trainings', employee.trainings)
        employee.external_privileges = data.get('external_privileges', employee.external_privileges)
        employee.special_leave_record = data.get('special_leave_record', employee.special_leave_record)
        employee.drive_folder_link = data.get('drive_folder_link', employee.drive_folder_link)

        # -------------------------
        # تحديث أو رفع صورة الموظف
        # -------------------------
        if 'profile_image' in data and data['profile_image']:
            new_image = data['profile_image']
            if new_image.startswith('data:image'):
                try:
                    img_data = new_image.split(',')[1] if ',' in new_image else new_image
                    result = cloudinary.uploader.upload(
                        base64.b64decode(img_data),
                        public_id=f"profile_{employee_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
                    )
                    employee.profile_image = result['secure_url']
                except Exception as e:
                    print(f"Error processing image: {e}")
            elif new_image.startswith('http'):
                employee.profile_image = new_image

        # -------------------------
        # الحقول الأخرى
        # -------------------------
        employee.telegram_chatid = data.get('telegram_chatid', employee.telegram_chatid)
        employee.phone = data.get('phone', employee.phone)
        employee.position = data.get('position', employee.position)
        employee.role = data.get('role', employee.role)

        # التحقق من وجود مشرف آخر في نفس القسم
        new_role = data.get('role', employee.role)
        new_department_id = data.get('department_id', employee.department_id)
        employee.department_id = new_department_id

        if new_role == 'مشرف' or (employee.role == 'مشرف' and new_role != 'مشرف'):
            existing_supervisor = Employee.query.filter(
                Employee.department_id == new_department_id,
                Employee.role == 'مشرف',
                Employee.id != employee_id
            ).first()
            if existing_supervisor:
                return jsonify({
                    'message': 'تم رفض العملية: لا يمكن وجود أكثر من مشرف في نفس القسم'
                }), 400

        employee.bank_account = data.get('bank_account', employee.bank_account)
        employee.address = data.get('address', employee.address)
        employee.notes = data.get('notes', employee.notes)
        employee.weekly_day_off = data.get('weekly_day_off', employee.weekly_day_off)

        # -------------------------
        # تحديث الحقول الثابتة أولاً
        # -------------------------
        if 'regular_leave_hours' in data:
            employee.regular_leave_hours = float(data['regular_leave_hours'])
        
        if 'sick_leave_hours' in data:
            employee.sick_leave_hours = float(data['sick_leave_hours'])
        
        if 'emergency_leave_hours' in data:
            employee.emergency_leave_hours = float(data['emergency_leave_hours'])

        # -------------------------
        # نسخ القيم من الحقول الثابتة إلى الحقول الإجمالية
        # -------------------------
        employee.regular_leave_total = employee.regular_leave_hours
        employee.sick_leave_total = employee.sick_leave_hours
        employee.emergency_leave_total = employee.emergency_leave_hours

        # -------------------------
        # إعادة حساب الساعات المتبقية بناءً على القيم الجديدة
        # -------------------------
        employee.regular_leave_remaining = max(0, employee.regular_leave_total - employee.regular_leave_used)
        employee.sick_leave_remaining = max(0, employee.sick_leave_total - employee.sick_leave_used)
        employee.emergency_leave_remaining = max(0, employee.emergency_leave_total - employee.emergency_leave_used)

        # -------------------------
        # تحويل وتحديث التواريخ والأوقات
        # -------------------------
        if 'work_start_time' in data:
            employee.work_start_time = time.fromisoformat(data['work_start_time'])
        if 'work_end_time' in data:
            employee.work_end_time = time.fromisoformat(data['work_end_time'])
        if 'date_of_joining' in data:
            employee.date_of_joining = date.fromisoformat(data['date_of_joining'])
        if 'end_of_service_date' in data:
            employee.end_of_service_date = date.fromisoformat(data['end_of_service_date'])
        if 'date_of_birth' in data and data['date_of_birth']:
            employee.date_of_birth = date.fromisoformat(data['date_of_birth'])

        # -------------------------
        # تحديث أو إنشاء بيانات الراتب
        # -------------------------
        salary_data = data.get('salary_components')
        if salary_data:
            salary_component = SalaryComponent.query.filter_by(employee_id=employee_id).first()
            if not salary_component:
                salary_component = SalaryComponent(employee_id=employee_id)
                db.session.add(salary_component)

            base_salary = salary_data.get('base_salary', salary_component.base_salary or 0.0)
            salary_component.base_salary = float(base_salary)

            hour_salary = salary_data.get('hour_salary')
            if hour_salary is None:
                try:
                    salary_component.hour_salary = float(base_salary) / (8 * 26)
                except ZeroDivisionError:
                    salary_component.hour_salary = 0.0
            else:
                salary_component.hour_salary = float(hour_salary)

            salary_component.overtime_rate = salary_data.get('overtime_rate', salary_component.overtime_rate or 0.0)
            salary_component.holiday_overtime_rate = salary_data.get('holiday_overtime_rate', salary_component.holiday_overtime_rate or 0.0)
            salary_component.internet_allowance = salary_data.get('internet_allowance', salary_component.internet_allowance or 0.0)
            salary_component.transport_allowance = salary_data.get('transport_allowance', salary_component.transport_allowance or 0.0)
            salary_component.depreciation_allowance = salary_data.get('depreciation_allowance', salary_component.depreciation_allowance or 0.0)
            salary_component.administrative_allowance = salary_data.get('administrative_allowance', salary_component.administrative_allowance or 0.0)
            salary_component.administrative_deduction = salary_data.get('administrative_deduction', salary_component.administrative_deduction or 0.0)

        # -------------------------
        # حفظ التعديلات
        # -------------------------
        db.session.commit()
        db.session.refresh(employee, ['department'])

        # -------------------------
        # تحديث الجلسة إذا كان المستخدم الحالي هو نفسه
        # -------------------------
        if 'employee' in session and session['employee']['id'] == employee_id:
            session['employee'].update({
                "full_name_arabic": employee.full_name_arabic,
                "full_name_english": employee.full_name_english,
                "employee_number": employee.employee_number,
                "email": employee.email,
                "password": employee.password,
                "telegram_chatid": employee.telegram_chatid,
                "phone": employee.phone,
                "department_id": employee.department_id,
                "department_name": employee.department.dep_name if employee.department else None,
                "position": employee.position,
                "role": employee.role,
                "bank_account": employee.bank_account,
                "address": employee.address,
                "weekly_day_off": employee.weekly_day_off,
                "work_start_time": employee.work_start_time.strftime('%H:%M:%S') if employee.work_start_time else None,
                "work_end_time": employee.work_end_time.strftime('%H:%M:%S') if employee.work_end_time else None,
                "date_of_joining": employee.date_of_joining.strftime('%Y-%m-%d') if employee.date_of_joining else None,
                "end_of_service_date": employee.end_of_service_date.strftime('%Y-%m-%d') if employee.end_of_service_date else None,
                "notes": employee.notes,
                "profile_image": employee.profile_image,
                "status": employee.status,
                "is_leave": employee.is_leave,
                "is_vacation": employee.is_vacation,
                "is_weekly_day_off": employee.is_weekly_day_off,
                "regular_leave_hours": employee.regular_leave_hours,
                "sick_leave_hours": employee.sick_leave_hours,
                "emergency_leave_hours": employee.emergency_leave_hours,
                "regular_leave_total": employee.regular_leave_total,
                "sick_leave_total": employee.sick_leave_total,
                "emergency_leave_total": employee.emergency_leave_total,
                "regular_leave_used": employee.regular_leave_used,
                "sick_leave_used": employee.sick_leave_used,
                "emergency_leave_used": employee.emergency_leave_used,
                "regular_leave_remaining": employee.regular_leave_remaining,
                "sick_leave_remaining": employee.sick_leave_remaining,
                "emergency_leave_remaining": employee.emergency_leave_remaining,
                # الحقول الجديدة
                "study_major": employee.study_major,
                "governorate": employee.governorate,
                "relative_phone": employee.relative_phone,
                "date_of_birth": employee.date_of_birth.strftime('%Y-%m-%d') if employee.date_of_birth else None,
                "national_id": employee.national_id,
                "nationality": employee.nationality,
                "marital_status": employee.marital_status,
                "relative_relation": employee.relative_relation,
                "position_english": employee.position_english,
                "job_level": employee.job_level,
                "employee_status": employee.employee_status,
                "work_location": employee.work_location,
                "work_nature": employee.work_nature,
                "promotion": employee.promotion,
                "career_stages": employee.career_stages,
                "trainings": employee.trainings,
                "external_privileges": employee.external_privileges,
                "special_leave_record": employee.special_leave_record,
                "drive_folder_link": employee.drive_folder_link
            })
            session.modified = True

        return jsonify({'message': 'Employee updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500
# إضافة قسم جديد
@app.route('/api/departments', methods=['POST'])
def add_department():
    try:
        data = request.get_json()

        # التحقق من وجود البيانات المطلوبة
        if not data or 'dep_name' not in data or 'dep_name_english' not in data:
            return jsonify({
                'success': False,
                'message': 'يرجى إدخال جميع البيانات المطلوبة'
            }), 400

        dep_name = data['dep_name'].strip()
        dep_name_english = data['dep_name_english'].strip()

        # التحقق من عدم ترك الحقول فارغة
        if not dep_name or not dep_name_english:
            return jsonify({
                'success': False,
                'message': 'يرجى إدخال اسم القسم بالعربية والإنجليزية'
            }), 400

        # التحقق من وجود قسم مخفي بنفس الاسم العربي
        existing_hidden_ar = Department.query.filter_by(dep_name=dep_name, visible=0).first()
        if existing_hidden_ar:
            existing_hidden_ar.visible = 1
            existing_hidden_ar.dep_name_english = dep_name_english  # يمكنك تحديث الإنجليزية أيضًا
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'تم إعادة تفعيل القسم المخفي (عربي)',
                'department': {
                    'id': existing_hidden_ar.dep_id,
                    'name': existing_hidden_ar.dep_name,
                    'name_english': existing_hidden_ar.dep_name_english,
                    'visible': existing_hidden_ar.visible
                }
            }), 200

        # التحقق من وجود قسم مخفي بنفس الاسم الإنجليزي
        existing_hidden_en = Department.query.filter_by(dep_name_english=dep_name_english, visible=0).first()
        if existing_hidden_en:
            existing_hidden_en.visible = 1
            existing_hidden_en.dep_name = dep_name  # يمكنك تحديث العربي أيضًا
            db.session.commit()
            return jsonify({
                'success': True,
                'message': 'تم إعادة تفعيل القسم المخفي (إنجليزي)',
                'department': {
                    'id': existing_hidden_en.dep_id,
                    'name': existing_hidden_en.dep_name,
                    'name_english': existing_hidden_en.dep_name_english,
                    'visible': existing_hidden_en.visible
                }
            }), 200

        # التحقق من عدم وجود قسم ظاهر بنفس الاسم
        existing_dept_ar = Department.query.filter_by(dep_name=dep_name, visible=1).first()
        existing_dept_en = Department.query.filter_by(dep_name_english=dep_name_english, visible=1).first()

        if existing_dept_ar:
            return jsonify({
                'success': False,
                'message': 'يوجد قسم بنفس الاسم العربي بالفعل'
            }), 400

        if existing_dept_en:
            return jsonify({
                'success': False,
                'message': 'يوجد قسم بنفس الاسم الإنجليزي بالفعل'
            }), 400

        # إنشاء قسم جديد
        new_department = Department(
            dep_name=dep_name,
            dep_name_english=dep_name_english,
            visible=1
        )

        db.session.add(new_department)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'تم إضافة القسم بنجاح',
            'department': {
                'id': new_department.dep_id,
                'name': new_department.dep_name,
                'name_english': new_department.dep_name_english,
                'visible': new_department.visible
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'حدث خطأ أثناء إضافة القسم: {str(e)}'
        }), 500
@app.route('/api/departments/<int:department_id>', methods=['DELETE'])
def delete_department(department_id):
    try:
        # البحث عن القسم
        department = Department.query.filter_by(dep_id=department_id, visible=1).first()
        if not department:
            return jsonify({
                'success': False,
                'message': 'القسم غير موجود'
            }), 404

        # عدد المشرفين في القسم
        supervisors_count = Supervisor.query.filter_by(dep_id=department_id).count()

        # عدد الموظفين (باستثناء من لديهم الدور "مشرف")
        employees_count = Employee.query.filter(
            Employee.department_id == department_id,
            Employee.role != 'مشرف'
        ).count()

        # التحقق من وجود مشرفين أو موظفين
        if supervisors_count > 0 or employees_count > 0:
            message_parts = []
            if employees_count > 0:
                message_parts.append(f"{employees_count} موظف")
            if supervisors_count > 0:
                message_parts.append(f"{supervisors_count} مشرف")

            message = (
                "لا يمكن حذف القسم لأنه يحتوي على: " +
                " و ".join(message_parts) +
                ". يرجى نقلهم إلى قسم آخر أو حذفهم أولًا."
            )

            return jsonify({
                'success': False,
                'message': message
            }), 400

        # حذف القسم (تغيير visible إلى 0)
        department.visible = 0
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'تم حذف القسم بنجاح'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'حدث خطأ أثناء حذف القسم: {str(e)}'
        }), 500

@app.route('/api/departments', methods=['GET'])
def get_departments():
    try:
        departments = Department.query.filter(
            Department.visible == 1,
            Department.dep_name != 'الإدارة العامة'  # ✅ استثناء قسم الادمن
        ).all()

        departments_list = []
        
        for dept in departments:
            employee_count = Employee.query.filter_by(department_id=dept.dep_id).count()
            department_data = {
                'id': dept.dep_id,
                'name': dept.dep_name,
                'name_english': dept.dep_name_english,
                'visible': dept.visible,
                'employees_count': len(dept.employees) if dept.employees else 0
            }
            departments_list.append(department_data)
        
        return jsonify(departments_list), 200
    
    except Exception as e:
        return jsonify({'error': f'فشل في جلب بيانات الأقسام: {str(e)}'}), 500


@app.route('/api/employee-statistics', methods=['GET'])
def employee_statistics():
    try:
        employee_id = request.args.get('employee_id')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        # طباعة القيم المستلمة للتشخيص
        print(f"🔍 Parameters received:")
        print(f"   employee_id: {employee_id}")
        print(f"   start_date: {start_date}")
        print(f"   end_date: {end_date}")
        
        if not all([employee_id, start_date, end_date]):
            return jsonify({"error": "Missing required query parameters."}), 400
        
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        print(f"📅 Parsed dates:")
        print(f"   start_date: {start_date}")
        print(f"   end_date: {end_date}")
        
        employee = db.session.get(Employee, employee_id)
        if not employee:
            return jsonify({"error": "Employee not found."}), 404
        
        print(f"👤 Employee found:")
        print(f"   ID: {employee.id}")
        print(f"   Name: {employee.full_name_arabic}")
        print(f"   Weekly off: {employee.weekly_day_off}")
        
        # ============== حساب أيام الحضور ==============
        
        # 1. الحصول على جميع أيام الحضور الفعلية
        attendance_records = db.session.query(AttendanceRecord).filter(
            AttendanceRecord.employee_id == employee_id,
            AttendanceRecord.work_date >= start_date,
            AttendanceRecord.work_date <= end_date,
            AttendanceRecord.check_in_time.isnot(None)
        ).all()
        
        print(f"📊 Attendance records found: {len(attendance_records)}")
        for record in attendance_records:
            print(f"   Date: {record.work_date}, Check-in: {record.check_in_time}")
        
        # 2. الحصول على العطل الرسمية
        official_holidays = db.session.query(OfficialHoliday.holiday_date).filter(
            OfficialHoliday.holiday_date >= start_date,
            OfficialHoliday.holiday_date <= end_date
        ).all()
        holiday_dates = [holiday.holiday_date for holiday in official_holidays]
        
        print(f"🏖️ Official holidays: {len(holiday_dates)}")
        for holiday in holiday_dates:
            print(f"   Holiday: {holiday}")
        
        # 3. تحديد يوم العطلة الأسبوعية
        weekly_day_off = employee.weekly_day_off.lower()
        day_mapping = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 
            'friday': 4, 'saturday': 5, 'sunday': 6,
            'الاثنين': 0, 'الثلاثاء': 1, 'الأربعاء': 2, 'الخميس': 3, 
            'الجمعة': 4, 'السبت': 5, 'الأحد': 6
        }
        weekly_off_day_num = day_mapping.get(weekly_day_off, 4)
        
        print(f"📅 Weekly day off: {weekly_day_off} (day number: {weekly_off_day_num})")
                # حساب عدد ساعات العمل اليومية للموظف
        def get_work_hours(start_time, end_time):
            # تحويل Time إلى datetime اليومي
            dt_start = datetime.combine(date.today(), start_time)
            dt_end   = datetime.combine(date.today(), end_time)
            return (dt_end - dt_start).total_seconds() / 3600  # بالساعة
        daily_hours = get_work_hours(employee.work_start_time, employee.work_end_time)

        # 3. جلب الإجازات الموافق عليها ضمن الفترة
        leaves = db.session.query(
            LeaveRequest.id,
            LeaveRequest.type,
            LeaveRequest.classification,
            LeaveRequest.start_date,
            LeaveRequest.end_date,
            LeaveRequest.hours_requested
        ).filter(
            LeaveRequest.employee_id == employee_id,
            LeaveRequest.status == 'approved',
            or_(
                # إجازة ساعية تقع بدايتها ضمن المدى
                and_(
                    LeaveRequest.type == 'hourly',
                    LeaveRequest.start_date >= start_date,
                    LeaveRequest.start_date <= end_date
                ),
                # إجازة يومية أو متعددة الأيام تتداخل مع المدى
                and_(
                    LeaveRequest.type != 'hourly',
                    LeaveRequest.start_date <= end_date,
                    LeaveRequest.end_date   >= start_date,
                    LeaveRequest.end_date.isnot(None)
                )
            )
        ).all()

        # 4. حساب الساعات الفعلية المأخوذة بحسب النوع
        total_leave_hours = 0.0
        for lv in leaves:
            if lv.type == 'hourly':
                total_leave_hours += (lv.hours_requested or 0)
            else:
                # تحديد التداخل بين فترة الإجازة والفترة المطلوبة
                overlap_start = max(lv.start_date, start_date)
                overlap_end   = min(lv.end_date,   end_date)
                if overlap_start <= overlap_end:
                    days = (overlap_end - overlap_start).days + 1
                    total_leave_hours += days * daily_hours

        # 5. تفصيل الساعات إلى ساعات + دقائق للعرض
        hourss = int(round(total_leave_hours * 60))  # 480
        print("leave totola hours",hourss)
        # 4. حساب أيام العمل المتوقعة
        total_expected_work_days = 0
        expected_work_dates = []
        current_date = start_date
        
        while current_date <= end_date:
            day_name = current_date.strftime('%A').lower()
            is_weekend = current_date.weekday() == weekly_off_day_num
            is_holiday = current_date in holiday_dates
            
            print(f"   {current_date} ({day_name}): weekend={is_weekend}, holiday={is_holiday}")
            
            if not is_weekend and not is_holiday:
                total_expected_work_days += 1
                expected_work_dates.append(current_date)
            
            current_date += timedelta(days=1)
        
        print(f"📈 Total expected work days: {total_expected_work_days}")
        print(f"   Expected work dates: {expected_work_dates}")
        
        # 5. حساب أيام الحضور الفعلية
        actual_attendance_dates = set()
        total_work_hours = 0
        total_delay_minutes = 0
        delay_count = 0
        total_overtime_minutes = 0
        
        for record in attendance_records:
            if record.work_date:
                actual_attendance_dates.add(record.work_date)
                
                # حساب ساعات العمل
                if record.work_hours:
                    total_work_hours += record.work_hours
                
                # حساب التأخير
                if record.check_in_time and employee.work_start_time:
                    expected_start = datetime.combine(record.work_date, employee.work_start_time)
                    actual_start = record.check_in_time
                    
                    if actual_start > expected_start:
                        delay_minutes = int((actual_start - expected_start).total_seconds() / 60)
                        if delay_minutes > 15:
                            total_delay_minutes += delay_minutes
                            delay_count += 1
                            print(f"   ⏰ Delay on {record.work_date}: {delay_minutes} minutes")
                
                # حساب الوقت الإضافي
                if (record.check_out_time and record.check_in_time and 
                    employee.work_end_time and employee.work_start_time):
                    
                    expected_end = datetime.combine(record.work_date, employee.work_end_time)
                    actual_end = record.check_out_time
                    
                    if actual_end > expected_end:
                        overtime_minutes = int((actual_end - expected_end).total_seconds() / 60)
                        if overtime_minutes > 10:
                            total_overtime_minutes += overtime_minutes
                            print(f"   ⏱️ Overtime on {record.work_date}: {overtime_minutes} minutes")
        
        present_days = len(actual_attendance_dates)
        print(f"✅ Present days calculated: {present_days}")
        print(f"   Actual attendance dates: {sorted(actual_attendance_dates)}")
        
        # ============== حساب ساعات العمل اليومية للموظف ==============
        
        # الحصول على معلومات الموظف ووقت العمل
        employee = db.session.query(Employee).filter(Employee.id == employee_id).first()
        if not employee:
            raise ValueError(f"Employee with ID {employee_id} not found")
        
        # حساب ساعات العمل اليومية للموظف
        work_start_time = employee.work_start_time  # مثال: datetime.time(8, 0)
        work_end_time = employee.work_end_time      # مثال: datetime.time(17, 0)
        
        # تحويل الأوقات إلى ساعات وحساب الفرق
        if work_start_time and work_end_time:
            start_hours = work_start_time.hour + work_start_time.minute / 60
            end_hours = work_end_time.hour + work_end_time.minute / 60
            hours_per_day = end_hours - start_hours
            
            # التعامل مع الحالات الخاصة (العمل لليوم التالي)
            if hours_per_day < 0:
                hours_per_day += 24
        else:
            # قيمة افتراضية في حالة عدم وجود أوقات عمل محددة
            hours_per_day = 8.0
        
        print(f"👤 Employee work hours: {hours_per_day} hours per day")
        print(f"   Work time: {work_start_time} - {work_end_time}")
        
        # ============== حساب الإجازات بالساعات الفعلية (التعديل الجديد) ==============
        
        # استرجاع جميع طلبات الإجازات المعتمدة للموظف
        leaves = db.session.query(
            LeaveRequest.id,
            LeaveRequest.type,
            LeaveRequest.classification,
            LeaveRequest.start_date,
            LeaveRequest.end_date,
            LeaveRequest.hours_requested
        ).filter(
            LeaveRequest.employee_id == employee_id,
            LeaveRequest.status == 'approved',
            or_(
                and_(
                    LeaveRequest.type == 'hourly',
                    LeaveRequest.start_date >= start_date,
                    LeaveRequest.start_date <= end_date
                ),
                and_(
                    LeaveRequest.type != 'hourly',
                    LeaveRequest.start_date <= end_date,
                    LeaveRequest.end_date >= start_date,
                    LeaveRequest.end_date.isnot(None)
                )
            )
        ).all()

        print(f"📋 Approved leaves found: {len(leaves)}")
        for i, leave in enumerate(leaves, 1):
            print(f"   {i}. ID: {leave.id}, Type: {leave.type}, Classification: {leave.classification}")
            print(f"      Start: {leave.start_date}, End: {leave.end_date}, Hours: {leave.hours_requested}")

        # حساب الإجازات المأخوذة لكل تصنيف
        leave_hours_taken = {"normal": 0, "emergency": 0, "sick": 0}
        leave_types_breakdown = {}

        for leave in leaves:
            classification = leave.classification or "normal"
            if classification not in leave_hours_taken:
                classification = "normal"

            if leave.type == 'hourly':
                # الإجازات الساعية: نأخذ الساعات مباشرة
                hours = leave.hours_requested or 0
                leave_hours_taken[classification] += hours
                
                # تحديث تفاصيل الأنواع
                if leave.type in leave_types_breakdown:
                    leave_types_breakdown[leave.type] += hours
                else:
                    leave_types_breakdown[leave.type] = hours
            else:
                # الإجازات اليومية والمتعددة الأيام: نحسب الأيام الفعلية
                # تحديد فترة التداخل مع الفترة المطلوبة
                overlap_start = max(leave.start_date, start_date)
                overlap_end = min(leave.end_date, end_date)
                
                # حساب الأيام الفعلية في الفترة
                if overlap_start <= overlap_end:
                    days_in_period = (overlap_end - overlap_start).days + 1
                    hours_in_period = days_in_period * hours_per_day  # استخدام ساعات العمل الخاصة بالموظف
                    leave_hours_taken[classification] += hours_in_period
                    
                    # تحديث تفاصيل الأنواع
                    if leave.type in leave_types_breakdown:
                        leave_types_breakdown[leave.type] += hours_in_period
                    else:
                        leave_types_breakdown[leave.type] = hours_in_period
                    
                    print(f"   📅 Multi-day leave: {days_in_period} days ({hours_in_period} hours) added")
        regular_leave_hours = employee.regular_leave_hours or 0
        normal_leave_taken = leave_hours_taken.get("normal", 0)
        emergency_hours = employee.emergency_leave_hours or 0
        emergency_taken = leave_hours_taken.get("emergency", 0)

        sick_hours = employee.sick_leave_hours or 0
        sick_taken = leave_hours_taken.get("sick", 0)
        # تحويل إجمالي الساعات لكل نوع إلى أيام
        leave_types_result = {}
        for leave_type, total_hours in leave_types_breakdown.items():
            leave_types_result[leave_type] = {
                "hours": total_hours,
                "days": round(total_hours / hours_per_day, 2)  # استخدام ساعات العمل الخاصة بالموظف
            }

        # حساب الإجازات المأخوذة بالأيام لكل تصنيف
        leave_days_taken = {
            "normal": round(leave_hours_taken["normal"] / hours_per_day, 2),     # استخدام ساعات العمل الخاصة بالموظف
            "emergency": round(leave_hours_taken["emergency"] / hours_per_day, 2), # استخدام ساعات العمل الخاصة بالموظف
            "sick": round(leave_hours_taken["sick"] / hours_per_day, 2)          # استخدام ساعات العمل الخاصة بالموظف
        }
        # رصيد الإجازات بالساعات والأيام
        leave_balance_hours = {
            "normal": employee.regular_leave_hours,
            "emergency": employee.emergency_leave_hours,
            "sick": employee.sick_leave_hours
        }
        
        leave_balance_days = {
            "normal": round((employee.regular_leave_hours or 0) / hours_per_day, 2),
            "emergency": round((employee.emergency_leave_hours or 0) / hours_per_day, 2),
            "sick": round((employee.sick_leave_hours or 0) / hours_per_day, 2)
        }
        # الرصيد المتبقي
        remaining_leave_hours = {
            "normal": max(0, regular_leave_hours - normal_leave_taken),
            "emergency": max(0, emergency_hours - emergency_taken),
            "sick": max(0, sick_hours - sick_taken)
        }
        
        remaining_leave_days = {
            "normal": round(remaining_leave_hours["normal"] / hours_per_day, 2),
            "emergency": round(remaining_leave_hours["emergency"] / hours_per_day, 2),
            "sick": round(remaining_leave_hours["sick"] / hours_per_day, 2)
        }

        print(f"📊 Leave calculation results:")
        print(f"   Hours taken: normal={leave_hours_taken['normal']}, emergency={leave_hours_taken['emergency']}, sick={leave_hours_taken['sick']}")
        print(f"   Days taken: normal={leave_days_taken['normal']}, emergency={leave_days_taken['emergency']}, sick={leave_days_taken['sick']}")
        print(f"   Remaining hours: normal={remaining_leave_hours['normal']}, emergency={remaining_leave_hours['emergency']}, sick={remaining_leave_hours['sick']}")
        print(f"   Remaining days: normal={remaining_leave_days['normal']}, emergency={remaining_leave_days['emergency']}, sick={remaining_leave_days['sick']}")
        
        # ============== حساب التعويضات والحضور الإضافي ==============
        
        # حساب دقائق التعويض
        compensation_requests = db.session.query(
            func.sum(CompensationLeaveRequest.hours_requested)
        ).filter(
            CompensationLeaveRequest.employee_id == employee_id,
            CompensationLeaveRequest.status == 'approved',
            CompensationLeaveRequest.date >= start_date,
            CompensationLeaveRequest.date <= end_date
        ).scalar()
        
        compensation_minutes = int((compensation_requests or 0) * 60)
        
        # ============== حساب الحضور الإضافي (محدث) ==============
        
        # حساب الحضور الإضافي - منفصل للأيام العادية والعطل
        regular_days_additional = db.session.query(
            func.sum(AdditionalAttendanceRecord.add_attendance_minutes)
        ).filter(
            AdditionalAttendanceRecord.employee_id == employee_id,
            AdditionalAttendanceRecord.status == "approved",
            AdditionalAttendanceRecord.date >= start_date,
            AdditionalAttendanceRecord.date <= end_date,
            AdditionalAttendanceRecord.is_holiday == False  # الأيام العادية
        ).scalar() or 0

        holidays_additional = db.session.query(
            func.sum(AdditionalAttendanceRecord.add_attendance_minutes)
        ).filter(
            AdditionalAttendanceRecord.employee_id == employee_id,
            AdditionalAttendanceRecord.status == "approved",
            AdditionalAttendanceRecord.date >= start_date,
            AdditionalAttendanceRecord.date <= end_date,
            AdditionalAttendanceRecord.is_holiday == True  # العطل (الأسبوعية والرسمية)
        ).scalar() or 0

        # إجمالي الحضور الإضافي
        total_additional_attendance_minutes = regular_days_additional + holidays_additional
        
        print(f"📈 Additional attendance breakdown:")
        print(f"   Regular days: {regular_days_additional} minutes ({round(regular_days_additional/60, 2)} hours)")
        print(f"   Holidays: {holidays_additional} minutes ({round(holidays_additional/60, 2)} hours)")
        print(f"   Total: {total_additional_attendance_minutes} minutes ({round(total_additional_attendance_minutes/60, 2)} hours)")
        
        # جلب تفاصيل طلبات التعويض
        comp_requests = db.session.query(
            CompensationLeaveRequest.date,
            CompensationLeaveRequest.hours_requested,
            CompensationLeaveRequest.start_time,
            CompensationLeaveRequest.end_time,
            CompensationLeaveRequest.note,
            CompensationLeaveRequest.status
        ).filter(
            CompensationLeaveRequest.employee_id == employee_id,
            CompensationLeaveRequest.status == 'approved',
            CompensationLeaveRequest.date >= start_date,
            CompensationLeaveRequest.date <= end_date
        ).all()

        compensation_records = []
        for rec in comp_requests:
            duration_minutes = int(rec.hours_requested * 60)
            compensation_records.append({
                "date": rec.date.strftime("%Y-%m-%d"),
                "hours_requested": rec.hours_requested,
                "duration_minutes": duration_minutes,
                "start_time": rec.start_time.strftime("%H:%M") if rec.start_time else None,
                "end_time": rec.end_time.strftime("%H:%M") if rec.end_time else None,
                "note": rec.note,
                "status": rec.status
            })
        
        # سجلات الدوام الإضافي خلال الفترة (محدث)
        add_att_recs = db.session.query(
            AdditionalAttendanceRecord.date,
            AdditionalAttendanceRecord.add_attendance_minutes,
            AdditionalAttendanceRecord.notes,
            AdditionalAttendanceRecord.role,
            AdditionalAttendanceRecord.is_holiday,
            AdditionalAttendanceRecord.start_time,  # ✅ أضف هذا
            AdditionalAttendanceRecord.end_time     # ✅ وأيضًا هذا
        ).filter(
            AdditionalAttendanceRecord.employee_id == employee_id,
            AdditionalAttendanceRecord.status == "approved",
            AdditionalAttendanceRecord.date >= start_date,
            AdditionalAttendanceRecord.date <= end_date
        ).all()

        additional_records = []
        for rec in add_att_recs:
            if rec.is_holiday:
                type_description = "إضافي - عطلة"
            else:
                type_description = "إضافي - يوم عادي"

            additional_records.append({
                "date": rec.date.strftime("%Y-%m-%d"),
                "duration_minutes": rec.add_attendance_minutes,
                "duration_hours": round(rec.add_attendance_minutes / 60, 2),
                "start_time": "-",
                "end_time": "-",
                "notes": rec.notes or "-",
                "type": type_description  # ✅ نرسل النص النهائي هنا مباشرة
            })
        # دمج السجلات في جدول واحد (محدث)
        merged_records = []

        for rec in comp_requests:
            merged_records.append({
                "date": rec.date.strftime("%Y-%m-%d"),
                "duration_minutes": int(rec.hours_requested * 60),
                "duration_hours": round(rec.hours_requested, 2),
                "start_time": rec.start_time.strftime("%H:%M") if rec.start_time else "-",
                "end_time": rec.end_time.strftime("%H:%M") if rec.end_time else "-",
                "notes": rec.note or "-",
                "type": "تعويض",
                "day_type": "-"
            })
        for rec in add_att_recs:
            if rec.is_holiday:
                type_description = "إضافي - عطلة"
            else:
                type_description = "إضافي - يوم عادي"
            merged_records.append({
                "date": rec.date.strftime("%Y-%m-%d"),
                "duration_minutes": rec.add_attendance_minutes,
                "duration_hours": round(rec.add_attendance_minutes / 60, 2),
                "start_time": rec.start_time.strftime("%H:%M") if rec.start_time else "-",  # ✅ وقت البداية بصيغة 08:30 مثلاً
                "end_time": rec.end_time.strftime("%H:%M") if rec.end_time else "-",        # ✅ وقت النهاية
                "notes": rec.notes or "-",
                "type": type_description
            })
        # ترتيب حسب التاريخ تصاعدياً
        merged_records.sort(key=lambda x: x["date"])
        
        # ============== إعداد النتيجة النهائية ==============
        
        absent_days = max(0, total_expected_work_days - present_days)
        # ============== حساب الراتب ==============
        
        # جلب مكونات الراتب للموظف
        salary_component = db.session.query(SalaryComponent).filter(
            SalaryComponent.employee_id == employee_id
        ).first()
        
        salary_info = {}
        
        if salary_component:
            # 1. قراءة القيم الأساسية من salary_component
            base_salary = salary_component.base_salary or 0
            hour_salary = salary_component.hour_salary or 0
            overtime_rate = salary_component.overtime_rate or 1
            holiday_overtime_rate = salary_component.holiday_overtime_rate or 1

            print(f"1) Base Salary: {base_salary}")
            print(f"2) Hourly Wage: {hour_salary}")
            print(f"3) Overtime Rate: {overtime_rate}")
            print(f"4) Holiday Overtime Rate: {holiday_overtime_rate}")

            # 2. قراءة البدلات
            daily_internet_allowance = salary_component.internet_allowance or 0
            daily_transport_allowance = salary_component.transport_allowance or 0
            daily_depreciation_allowance = salary_component.depreciation_allowance or 0
            daily_administrative_allowance = salary_component.administrative_allowance or 0
                        # 3. حساب مجموع البدلات بالدقة
            internet_allowance = daily_internet_allowance * present_days
            transport_allowance = daily_transport_allowance * present_days
            depreciation_allowance = daily_depreciation_allowance * present_days
            administrative_allowance = daily_administrative_allowance * present_days

            print(f"5) Internet Allowance: {internet_allowance}")
            print(f"6) Transport Allowance: {transport_allowance}")
            print(f"7) Depreciation Allowance: {depreciation_allowance}")
            print(f"7) administrative_allowance: {administrative_allowance}")
            # 3. قراءة الاستقطاعات
            daily_administrative_deduction = salary_component.administrative_deduction or 0
            administrative_deduction = daily_administrative_deduction * present_days
            print(f"8) administrative Deduction: {administrative_deduction}")
            holiday_overtime_rate_dec = Decimal(str(holiday_overtime_rate))
            overtime_rate_dec = Decimal(str(overtime_rate))
            internet_allowance_dec = Decimal(str(internet_allowance))
            transport_allowance_dec = Decimal(str(transport_allowance))
            depreciation_allowance_dec = Decimal(str(depreciation_allowance))
            administrative_allowance_dec = Decimal(str(administrative_allowance))
            administrative_deduction_dec = Decimal(str(administrative_deduction))
            regular_overtime_hours = Decimal(str(regular_days_additional / 60))
            holiday_overtime_hours = Decimal(str(holidays_additional / 60))
            total_work_hours_dec = Decimal(str(total_work_hours))

            print(f"10) Actual Work Hours: {total_work_hours_dec} hours")
            print(f"11) Regular Overtime Hours: {regular_overtime_hours} hours")
            print(f"12) holiday Attendance Hours: {holiday_overtime_hours} hours")

            # 6. حساب الراتب الأساسي المكتسب
            actual_salary_earned = total_work_hours_dec * hour_salary
            print(f"13) Actual Salary Earned = Work Hours × Hourly Wage = {total_work_hours_dec} × {hour_salary} = {actual_salary_earned}")

            # 7. حساب أجر الوقت الإضافي العادي
            regular_overtime_pay = regular_overtime_hours * hour_salary * overtime_rate_dec
            print(f"14) Regular Overtime Pay = Overtime Hours × Hourly Wage × Overtime Rate = {regular_overtime_hours} × {hour_salary} × {overtime_rate_dec} = {regular_overtime_pay}")

            # 8. حساب أجر الحضور الإضافي في ايام العطل
            holiday_overtime_pay = holiday_overtime_hours * hour_salary * holiday_overtime_rate_dec
            print(f"15) holiday Overtime Pay = Approved Extra Hours × Hourly Wage × Overtime Rate = {holiday_overtime_hours} × {hour_salary} × {holiday_overtime_rate_dec} = {holiday_overtime_pay}")

            # 9. حساب إجمالي البدلات
            total_allowances = internet_allowance_dec + transport_allowance_dec + depreciation_allowance_dec + administrative_allowance_dec
            print(f"16) Total Allowances = Internet + Transport + Depreciation + Others = {internet_allowance_dec} + {transport_allowance_dec} + {depreciation_allowance_dec}+ {administrative_allowance_dec}= {total_allowances}")

            # 10. حساب إجمالي الاستقطاعات
            total_deductions = administrative_deduction_dec
            print(f"17) Total Deductions = {total_deductions}")

            # 11. حساب الراتب الإجمالي
            gross_salary = actual_salary_earned + regular_overtime_pay + holiday_overtime_pay + total_allowances
            print(f"18) Gross Salary = Actual Salary + Regular Overtime Pay + Additional Overtime Pay + Total Allowances = {actual_salary_earned} + {regular_overtime_pay} + {holiday_overtime_pay} + {total_allowances} = {gross_salary}")

            # 12. حساب صافي الراتب بعد الاستقطاعات
            net_salary = gross_salary - total_deductions
            print(f"19) Net Salary = Gross Salary - Total Deductions = {gross_salary} - {total_deductions} = {net_salary}")


            
            salary_info = {
                "base_salary": base_salary,
                "hour_salary": hour_salary,
                "overtime_rate": overtime_rate,
                "holiday_overtime_rate": holiday_overtime_rate,
                "actual_work_hours": total_work_hours,
                "actual_salary_earned": round(actual_salary_earned, 2),
                "regular_overtime_hours": round(regular_overtime_hours, 2),
                "regular_overtime_pay": round(regular_overtime_pay, 2),
                "holiday_overtime_pay": round(holiday_overtime_pay, 2),
                "total_overtime_pay": round(regular_overtime_pay + holiday_overtime_pay, 2),
                "allowances": {
                    "internet_allowance": internet_allowance,
                    "transport_allowance": transport_allowance,
                    "depreciation_allowance": depreciation_allowance,
                    "administrative_allowance": administrative_allowance,
                    "total_allowances": total_allowances
                },
                "deductions": {
                    "administrative_deduction": administrative_deduction,
                    "total_deductions": total_deductions
                },
                "gross_salary": round(gross_salary, 2),
                "net_salary": round(net_salary, 2)
            }
            
            print(f"💰 Salary calculation:")
            print(f"   Actual work hours: {total_work_hours}")
            print(f"   Hour salary: {hour_salary}")
            print(f"   Actual salary earned: {actual_salary_earned}")
            print(f"   Regular overtime hours: {regular_overtime_hours}")
            print(f"   holiday overtime hours: {holiday_overtime_hours}")
            print(f"   Total allowances: {total_allowances}")
            print(f"   Total deductions: {total_deductions}")
            print(f"   Gross salary: {gross_salary}")
            print(f"   Net salary: {net_salary}")
        else:
            print("⚠️ No salary component found for this employee")
            salary_info = {
                "error": "No salary component found for this employee"
            }
        # استعلام جمع دقائق التأخير غير المبرر حسب الفترة والموظف
        total_unjustified_delay = db.session.query(
            func.coalesce(func.sum(WorkDelayArchive.minutes_delayed), 0)
        ).filter(
            WorkDelayArchive.status == 'Unjustified',
            WorkDelayArchive.employee_id == employee_id,
            WorkDelayArchive.date >= start_date,
            WorkDelayArchive.date <= end_date
        ).scalar()
        # النتيجة النهائية
        result = {
            "employee_info": {
                "name_arabic": employee.full_name_arabic,
                "name_english": employee.full_name_english,
                "employee_number": employee.employee_number,
                "weekly_day_off": employee.weekly_day_off
            },
            "period_info": {
                "start_date": start_date.strftime("%Y-%m-%d"),
                "end_date": end_date.strftime("%Y-%m-%d"),
                "total_expected_work_days": total_expected_work_days,
                "official_holidays_count": len(holiday_dates)
            },
            "attendance_stats": {
                "present_days": present_days,
                "absent_days": max(0, total_expected_work_days - present_days),
                "attendance_percentage": round((present_days / total_expected_work_days * 100) if total_expected_work_days > 0 else 0, 2)
            },
            "time_stats": {
                "hourss": str(round(hourss / 60, 2)),  # "2"
                "minutess": str(hourss), 
                "total_unjustified_delay_minutes": total_unjustified_delay,
                "total_unjustified_delay_hours": round(total_unjustified_delay / 60, 2),
                "total_work_hours": round(total_work_hours, 2),
                "delays_count": delay_count,
                "total_delay_minutes": total_delay_minutes,
                "overtime_minutes": total_overtime_minutes,
                "compensation_minutes": compensation_minutes,
                "regular_days_additional_minutes": regular_days_additional,
                "regular_days_additional_hours": round(regular_days_additional / 60, 2),
                "holidays_additional_minutes": holidays_additional,
                "holidays_additional_hours": round(holidays_additional / 60, 2),
                "total_additional_minutes": total_additional_attendance_minutes,
                "total_additional_hours": round(total_additional_attendance_minutes / 60, 2),
            },
            "leaves_info": {
                "leaves_taken_hours": {
                    "normal": leave_hours_taken["normal"],
                    "emergency": leave_hours_taken["emergency"],
                    "sick": leave_hours_taken["sick"]
                },
                "leaves_taken_days": {
                    "normal": leave_days_taken["normal"],
                    "emergency": leave_days_taken["emergency"],
                    "sick": leave_days_taken["sick"]
                },
                "leave_types_breakdown": leave_types_result,
                "leave_balance_hours": leave_balance_hours,
                "leave_balance_days": leave_balance_days,
                "remaining_leave_hours": remaining_leave_hours,
                "remaining_leave_days": remaining_leave_days
            },
            "salary_info": salary_info,
            "compensation_records": compensation_records,
            "additional_attendance_records": additional_records,
            "merged_records": merged_records
        }
        print(f"📤 Final result:")
        print(f"   Present days: {result['attendance_stats']['present_days']}")
        print(f"   Total work hours: {result['time_stats']['total_work_hours']}")
        print(f"   Leave hours taken: {result['leaves_info']['leaves_taken_hours']}")
        print(f"   Leave days taken: {result['leaves_info']['leaves_taken_days']}")
        print(f"   Net salary: {result['salary_info'].get('net_salary', 'N/A')}")
        
        return jsonify(result)
    except ValueError as ve:
        print(f"❌ ValueError: {str(ve)}")
        return jsonify({"error": f"Invalid date format: {str(ve)}"}), 400
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500
@app.route('/api/compensation-requests', methods=['GET'])
def get_compensation_requests():
    # ترتيب النتائج حسب التاريخ من الأحدث إلى الأقدم
    requests = CompensationLeaveRequest.query.join(Employee).join(Department).order_by(CompensationLeaveRequest.date.desc()).all()
    results = []
    for req in requests:
        results.append({
            "id": req.id,
            "employee_name": req.employee.full_name_arabic,
            "department": req.employee.department.dep_name if req.employee.department else None,
            "hours_requested": req.hours_requested,
            "status": req.status,
            "date": req.date.strftime('%Y-%m-%d'),
            "start_time": req.start_time.strftime('%H:%M') if req.start_time else None,
            "end_time": req.end_time.strftime('%H:%M') if req.end_time else None
        })
    return jsonify(results)
@app.route('/api/all-employees-salary-statistics/export-excel', methods=['GET'])
def export_all_employees_to_excel():
    try:
        # الحصول على المعاملات
        start_date = request.args.get('filterstartDate')
        end_date = request.args.get('filterendDate')
        
        if not all([start_date, end_date]):
            return jsonify({"error": "Missing required query parameters."}), 400
        
        start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        
        # استدعاء نفس منطق الحصول على البيانات من الدالة الأصلية
        employees = db.session.query(Employee).filter(Employee.role != 'ادمن').all()
        print("🧾 قائمة الموظفين:")
        for emp in employees:
            print(f" - {emp.full_name_arabic}")
        
        if not employees:
            return jsonify({"error": "No employees found."}), 404
        
        # الحصول على العطل الرسمية
        official_holidays = db.session.query(OfficialHoliday.holiday_date).filter(
            OfficialHoliday.holiday_date >= start_date,
            OfficialHoliday.holiday_date <= end_date
        ).all()
        holiday_dates = [holiday.holiday_date for holiday in official_holidays]
        
        all_employees_data = []
        
        # معالجة كل موظف (نفس المنطق من الدالة الأصلية)
        for employee in employees:
            try:
                # حساب أيام العمل المتوقعة
                weekly_day_off = employee.weekly_day_off.lower()
                day_mapping = {
                    'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 
                    'friday': 4, 'saturday': 5, 'sunday': 6,
                    'الاثنين': 0, 'الثلاثاء': 1, 'الأربعاء': 2, 'الخميس': 3, 
                    'الجمعة': 4, 'السبت': 5, 'الأحد': 6
                }
                weekly_off_day_num = day_mapping.get(weekly_day_off, 4)
                
                total_expected_work_days = 0
                current_date = start_date
                
                while current_date <= end_date:
                    is_weekend = current_date.weekday() == weekly_off_day_num
                    is_holiday = current_date in holiday_dates
                    
                    if not is_weekend and not is_holiday:
                        total_expected_work_days += 1
                    
                    current_date += timedelta(days=1)
                
                # جلب سجلات الحضور
                attendance_records = db.session.query(AttendanceRecord).filter(
                    AttendanceRecord.employee_id == employee.id,
                    AttendanceRecord.work_date >= start_date,
                    AttendanceRecord.work_date <= end_date,
                    AttendanceRecord.check_in_time.isnot(None)
                ).all()
                
                # حساب الحضور الفعلي
                actual_attendance_dates = set()
                total_work_hours = 0
                total_delay_minutes = 0
                delay_count = 0
                total_overtime_minutes = 0
                
                for record in attendance_records:
                    if record.work_date:
                        actual_attendance_dates.add(record.work_date)
                        
                        if record.work_hours:
                            total_work_hours += record.work_hours
                        
                        # حساب التأخير
                        if record.check_in_time and employee.work_start_time:
                            expected_start = datetime.combine(record.work_date, employee.work_start_time)
                            actual_start = record.check_in_time
                            
                            if actual_start > expected_start:
                                delay_minutes = int((actual_start - expected_start).total_seconds() / 60)
                                if delay_minutes > 15:
                                    total_delay_minutes += delay_minutes
                                    delay_count += 1
                        
                        # حساب الوقت الإضافي
                        if (record.check_out_time and record.check_in_time and 
                            employee.work_end_time and employee.work_start_time):
                            
                            expected_end = datetime.combine(record.work_date, employee.work_end_time)
                            actual_end = record.check_out_time
                            
                            if actual_end > expected_end:
                                overtime_minutes = int((actual_end - expected_end).total_seconds() / 60)
                                if overtime_minutes > 10:
                                    total_overtime_minutes += overtime_minutes
                
                present_days = len(actual_attendance_dates)
                absent_days = max(0, total_expected_work_days - present_days)
                
                # حساب ساعات العمل اليومية
                work_start_time = employee.work_start_time
                work_end_time = employee.work_end_time
                
                if work_start_time and work_end_time:
                    start_hours = work_start_time.hour + work_start_time.minute / 60
                    end_hours = work_end_time.hour + work_end_time.minute / 60
                    hours_per_day = end_hours - start_hours
                    
                    if hours_per_day < 0:
                        hours_per_day += 24
                else:
                    hours_per_day = 8.0
                
                # حساب الإجازات
                leaves = db.session.query(
                    LeaveRequest.id,
                    LeaveRequest.type,
                    LeaveRequest.classification,
                    LeaveRequest.start_date,
                    LeaveRequest.end_date,
                    LeaveRequest.hours_requested
                ).filter(
                    LeaveRequest.employee_id == employee.id,
                    LeaveRequest.status == 'approved',
                    or_(
                        and_(
                            LeaveRequest.type == 'hourly',
                            LeaveRequest.start_date >= start_date,
                            LeaveRequest.start_date <= end_date
                        ),
                        and_(
                            LeaveRequest.type != 'hourly',
                            LeaveRequest.start_date <= end_date,
                            LeaveRequest.end_date >= start_date,
                            LeaveRequest.end_date.isnot(None)
                        )
                    )
                ).all()

                leave_hours_taken = {"normal": 0, "emergency": 0, "sick": 0}

                for leave in leaves:
                    classification = leave.classification or "normal"
                    if classification not in leave_hours_taken:
                        classification = "normal"

                    if leave.type == 'hourly':
                        hours = leave.hours_requested or 0
                        leave_hours_taken[classification] += hours
                    else:
                        overlap_start = max(leave.start_date, start_date)
                        overlap_end = min(leave.end_date, end_date)
                        
                        if overlap_start <= overlap_end:
                            days_in_period = (overlap_end - overlap_start).days + 1
                            hours_in_period = days_in_period * hours_per_day
                            leave_hours_taken[classification] += hours_in_period

                # حساب الحضور الإضافي
                regular_days_additional = db.session.query(
                    func.sum(AdditionalAttendanceRecord.add_attendance_minutes)
                ).filter(
                    AdditionalAttendanceRecord.employee_id == employee.id,
                    AdditionalAttendanceRecord.status == "approved",
                    AdditionalAttendanceRecord.date >= start_date,
                    AdditionalAttendanceRecord.date <= end_date,
                    AdditionalAttendanceRecord.is_holiday == False
                ).scalar() or 0

                holidays_additional = db.session.query(
                    func.sum(AdditionalAttendanceRecord.add_attendance_minutes)
                ).filter(
                    AdditionalAttendanceRecord.employee_id == employee.id,
                    AdditionalAttendanceRecord.status == "approved",
                    AdditionalAttendanceRecord.date >= start_date,
                    AdditionalAttendanceRecord.date <= end_date,
                    AdditionalAttendanceRecord.is_holiday == True
                ).scalar() or 0

                # حساب التعويضات
                compensation_requests = db.session.query(
                    func.sum(CompensationLeaveRequest.hours_requested)
                ).filter(
                    CompensationLeaveRequest.employee_id == employee.id,
                    CompensationLeaveRequest.status == 'approved',
                    CompensationLeaveRequest.date >= start_date,
                    CompensationLeaveRequest.date <= end_date
                ).scalar()
                
                compensation_minutes = int((compensation_requests or 0) * 60)
                
                # حساب التأخير غير المبرر
                total_unjustified_delay = db.session.query(
                    func.coalesce(func.sum(WorkDelayArchive.minutes_delayed), 0)
                ).filter(
                    WorkDelayArchive.status == 'Unjustified',
                    WorkDelayArchive.employee_id == employee.id,
                    WorkDelayArchive.date >= start_date,
                    WorkDelayArchive.date <= end_date
                ).scalar()
                
                # حساب الراتب
                salary_component = db.session.query(SalaryComponent).filter(
                    SalaryComponent.employee_id == employee.id
                ).first()
                
                if salary_component:
                    from decimal import Decimal
                    
                    # قراءة القيم الأساسية
                    base_salary = salary_component.base_salary or 0
                    hour_salary = salary_component.hour_salary or 0
                    overtime_rate = salary_component.overtime_rate or 1
                    holiday_overtime_rate = salary_component.holiday_overtime_rate or 1

                    # حساب البدلات
                    daily_internet_allowance = salary_component.internet_allowance or 0
                    daily_transport_allowance = salary_component.transport_allowance or 0
                    daily_depreciation_allowance = salary_component.depreciation_allowance or 0
                    daily_administrative_allowance = salary_component.administrative_allowance or 0

                    internet_allowance = daily_internet_allowance * present_days
                    transport_allowance = daily_transport_allowance * present_days
                    depreciation_allowance = daily_depreciation_allowance * present_days
                    administrative_allowance = daily_administrative_allowance * present_days

                    # حساب الاستقطاعات
                    daily_administrative_deduction = salary_component.administrative_deduction or 0
                    administrative_deduction = daily_administrative_deduction * present_days

                    # تحويل إلى Decimal
                    holiday_overtime_rate_dec = Decimal(str(holiday_overtime_rate))
                    overtime_rate_dec = Decimal(str(overtime_rate))
                    internet_allowance_dec = Decimal(str(internet_allowance))
                    transport_allowance_dec = Decimal(str(transport_allowance))
                    depreciation_allowance_dec = Decimal(str(depreciation_allowance))
                    administrative_allowance_dec = Decimal(str(administrative_allowance))
                    administrative_deduction_dec = Decimal(str(administrative_deduction))
                    regular_overtime_hours = Decimal(str(regular_days_additional / 60))
                    holiday_overtime_hours = Decimal(str(holidays_additional / 60))
                    total_work_hours_dec = Decimal(str(total_work_hours))

                    # حساب الراتب
                    actual_salary_earned = total_work_hours_dec * hour_salary
                    regular_overtime_pay = regular_overtime_hours * hour_salary * overtime_rate_dec
                    holiday_overtime_pay = holiday_overtime_hours * hour_salary * holiday_overtime_rate_dec
                    total_allowances = internet_allowance_dec + transport_allowance_dec + depreciation_allowance_dec + administrative_allowance_dec
                    total_deductions = administrative_deduction_dec
                    gross_salary = actual_salary_earned + regular_overtime_pay + holiday_overtime_pay + total_allowances
                    net_salary = gross_salary - total_deductions
                    
                    # إضافة البيانات للقائمة
                    employee_row = {
                        'رقم الموظف': employee.employee_number,
                        'الاسم العربي': employee.full_name_arabic,
                        'الاسم الإنجليزي': employee.full_name_english,
                        'الايميل': employee.email,
                        'يوم العطلة الأسبوعية': employee.weekly_day_off,
                        'وقت بداية العمل': employee.work_start_time.strftime("%H:%M") if employee.work_start_time else '',
                        'وقت نهاية العمل': employee.work_end_time.strftime("%H:%M") if employee.work_end_time else '',
                        'أيام الحضور': present_days,
                        'أيام الغياب': absent_days,
                        'إجمالي أيام العمل المتوقعة': total_expected_work_days,
                        'نسبة الحضور %': round((present_days / total_expected_work_days * 100) if total_expected_work_days > 0 else 0, 2),
                        'إجمالي ساعات العمل': round(total_work_hours, 2),
                        'عدد مرات التأخير': delay_count,
                        'إجمالي دقائق التأخير': total_delay_minutes,
                        'التأخير غير المبرر (دقيقة)': total_unjustified_delay,
                        'الوقت الإضافي (دقيقة)': total_overtime_minutes,
                        'ساعات إضافية أيام عادية': round(regular_days_additional / 60, 2),
                        'ساعات إضافية أيام عطل': round(holidays_additional / 60, 2),
                        'إجازات عادية (ساعة)': leave_hours_taken["normal"],
                        'إجازات خاصة (ساعة)': leave_hours_taken["emergency"],
                        'إجازات مرضية (ساعة)': leave_hours_taken["sick"],
                        'الراتب الأساسي': base_salary,
                        'أجر الساعة': hour_salary,
                        'الراتب المكتسب': actual_salary_earned,
                        'أجر الوقت الإضافي العادي': round(float(regular_overtime_pay), 2),
                        'أجر الوقت الإضافي العطل': round(float(holiday_overtime_pay), 2),
                        'بدل إنترنت': float(internet_allowance),
                        'بدل مواصلات': float(transport_allowance),
                        'بدل إهلاك': float(depreciation_allowance),
                        'بدل إداري': float(administrative_allowance),
                        'إجمالي البدلات': float(total_allowances),
                        'الاستقطاع الإداري': float(administrative_deduction),
                        'إجمالي الاستقطاعات': float(total_deductions),
                        'الراتب الإجمالي': round(float(gross_salary), 2),
                        'صافي الراتب': f"{net_salary:,.0f}",
                        'مكافآت': '',
                        'تعويضات': '',
                        'منح': '',
                        'مشاركة أرباح': '',
                        'إضافات أخرى': '',
                        'خصم قرض': '',
                        'عقوبات': '',
                        'خصومات أخرى': '',
                        'ملاحظات': '',
                        'الراتب النهائي': '',
                        'رابط الملف': '',
                        'الارسال': ''
                    }
                    
                    all_employees_data.append(employee_row)
                    
            except Exception as emp_error:
                print(f"❌ Error processing employee {employee.full_name_arabic}: {str(emp_error)}")
                continue
        
        # التحقق من وجود بيانات قبل إنشاء Excel
        if not all_employees_data:
            return jsonify({"error": "No employee data found to export."}), 404
        
        # إنشاء DataFrame بعد انتهاء حلقة المعالجة
        df = pd.DataFrame(all_employees_data)
        print(f"✅ Successfully processed {len(all_employees_data)} employees")

        # إنشاء ملف Excel في الذاكرة
        output = BytesIO()

        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # كتابة البيانات بدون رؤوس الأعمدة الافتراضية (سنضيفها يدوياً)
            df.to_excel(writer, sheet_name='Payroll', index=False, header=False, startrow=0)
        
            # الحصول على workbook و worksheet
            workbook = writer.book
            worksheet = writer.sheets['Payroll']
        
            # تنسيق رؤوس الأعمدة
            header_format = workbook.add_format({
                'bold': True,
                'font_size': 11,
                'align': 'center',
                'valign': 'vcenter',
                'font_color': 'black',
                'border': 1,
                'text_wrap': True
            })
        
            # تنسيق البيانات
            data_format = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'border': 1
            })
        
            # تنسيق البيانات الرقمية
            number_format = workbook.add_format({
                'align': 'center',
                'valign': 'vcenter',
                'border': 1,
                'num_format': '#,##0.00'
            })
        
            # كتابة رؤوس الأعمدة في الصف الأول (index 0)
            for col_num, value in enumerate(df.columns.values):
                worksheet.write(0, col_num, value, header_format)
        
            # كتابة البيانات بدءاً من الصف الثاني (index 1)
            for row_num in range(len(df)):
                for col_num in range(len(df.columns)):
                    cell_value = df.iloc[row_num, col_num]
                
                    # استخدام تنسيق مختلف للأرقام
                    if isinstance(cell_value, (int, float)) and col_num > 7:  # الأعمدة الرقمية تبدأ من العمود 8
                        worksheet.write(row_num + 1, col_num, cell_value, number_format)
                    else:
                        worksheet.write(row_num + 1, col_num, cell_value, data_format)
        
            # ضبط عرض الأعمدة بالتفصيل لحل مشكلة #####
            column_widths = [
                ('A', 15),  # رقم الموظف
                ('B', 25),  # الاسم العربي
                ('C', 25),  # الاسم الإنجليزي
                ('D', 30),  # الايميل
                ('E', 20),  # يوم العطلة الأسبوعية
                ('F', 18),  # وقت بداية العمل
                ('G', 18),  # وقت نهاية العمل
                ('H', 15),  # أيام الحضور
                ('I', 15),  # أيام الغياب
                ('J', 25),  # إجمالي أيام العمل المتوقعة
                ('K', 18),  # نسبة الحضور %
                ('L', 20),  # إجمالي ساعات العمل
                ('M', 18),  # عدد مرات التأخير
                ('N', 22),  # إجمالي دقائق التأخير
                ('O', 25),  # التأخير غير المبرر (دقيقة)
                ('P', 22),  # الوقت الإضافي (دقيقة)
                ('Q', 25),  # ساعات إضافية أيام عادية
                ('R', 25),  # ساعات إضافية أيام عطل
                ('S', 20),  # إجازات عادية (ساعة)
                ('T', 20),  # إجازات خاصة (ساعة)
                ('U', 20),  # إجازات مرضية (ساعة)
                ('V', 18),  # الراتب الأساسي
                ('W', 15),  # أجر الساعة
                ('X', 18),  # الراتب المكتسب
                ('Y', 25),  # أجر الوقت الإضافي العادي
                ('Z', 25),  # أجر الوقت الإضافي العطل
                ('AA', 15), # بدل إنترنت
                ('AB', 15), # بدل مواصلات
                ('AC', 15), # بدل إهلاك
                ('AD', 15), # بدل إداري
                ('AE', 18), # إجمالي البدلات
                ('AF', 20), # الاستقطاع الإداري
                ('AG', 20), # إجمالي الاستقطاعات
                ('AH', 18), # الراتب الإجمالي
                ('AI', 15), # صافي الراتب
                ('AJ', 15), # مكافآت
                ('AK', 15), # تعويضات
                ('AL', 15), # منح
                ('AM', 18), # مشاركة أرباح
                ('AN', 15), # إضافات أخرى
                ('AO', 15), # خصم قرض
                ('AP', 15), # عقوبات
                ('AQ', 15), # خصومات أخرى
                ('AR', 20), # ملاحظات
                ('AS', 18), # الراتب النهائي
                ('AT', 15), # رابط الملف
                ('AU', 15), # الارسال
            ]
            
            # تطبيق عرض الأعمدة
            for col_letter, width in column_widths:
                worksheet.set_column(f'{col_letter}:{col_letter}', width)
            
            # ضبط ارتفاع الصف الأول (رؤوس الأعمدة)
            worksheet.set_row(0, 40)  # زيادة الارتفاع لاستيعاب النص المطوي

        output.seek(0)

        # إرسال الملف
        filename = f'Payroll_{start_date}_{end_date}.xlsx'

        return send_file(
            output,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        
    except Exception as e:
        print(f"❌ Error in Excel export: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"خطأ في تصدير البيانات: {str(e)}"}), 500
@app.route('/api/leave-requests/<int:request_id>', methods=['DELETE'])
def delete_leave_request(request_id):
    try:
        # البحث عن الطلب
        leave_request = db.session.get(LeaveRequest, request_id)
        
        if not leave_request:
            return jsonify({'error': 'طلب الإجازة غير موجود'}), 404
        
        # حذف الطلب من قاعدة البيانات
        db.session.delete(leave_request)
        db.session.commit()
        
        return jsonify({'message': 'تم حذف طلب الإجازة بنجاح'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'خطأ في حذف طلب الإجازة: {str(e)}'}), 500

@app.route('/api/compensation-requests/<int:request_id>', methods=['DELETE'])
def delete_compensation_request(request_id):
    try:
        # البحث عن الطلب
        compensation_request = db.session.get(CompensationLeaveRequest, request_id)
        
        if not compensation_request:
            return jsonify({'error': 'طلب تعويض الإجازة غير موجود'}), 404
        
        # حذف الطلب من قاعدة البيانات
        db.session.delete(compensation_request)
        db.session.commit()
        
        return jsonify({'message': 'تم حذف طلب تعويض الإجازة بنجاح'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'خطأ في حذف طلب تعويض الإجازة: {str(e)}'}), 500

# إذا كنت تريد إضافة التحقق من الصلاحيات (اختياري)
@app.route('/api/leave-requests/<int:request_id>', methods=['DELETE'])
def delete_leave_request_with_auth(request_id):
    try:
        leave_request = db.session.get(LeaveRequest, request_id)
        
        if not leave_request:
            return jsonify({'error': 'طلب الإجازة غير موجود'}), 404
        
        # التحقق من أن المستخدم له صلاحية حذف هذا الطلب
        # (يمكنك إضافة منطق التحقق هنا حسب نظامك)
        # مثال: التحقق من أن الطلب خاص بالموظف أو أن المستخدم مشرف
        
        db.session.delete(leave_request)
        db.session.commit()
        
        return jsonify({'message': 'تم حذف طلب الإجازة بنجاح'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'خطأ في حذف طلب الإجازة: {str(e)}'}), 500

@app.route('/api/admin/dashboard-data', methods=['GET'])
def get_dashboard_data():
    try:
        if 'employee' not in session or session['employee'].get('role') != 'ادمن':
            return jsonify({"error": "غير مصرح لك بالوصول"}), 403
        current_datetime = datetime.now(ZoneInfo("Asia/Damascus"))
        today = current_datetime.date()
        # للاختبار: استخدام وقت ثابت (الساعة 6 مساءً)
        current_time = current_datetime.time()
        print(f"التاريخ: {today}, الوقت الحالي: {current_time}")

        total_all_employees = db.session.query(Employee).filter(Employee.role != 'ادمن').count()

        all_employees = db.session.query(Employee, Department)\
            .join(Department, Employee.department_id == Department.dep_id)\
            .filter(Employee.role != 'ادمن')\
            .all()

        # جلب جميع سجلات الحضور لليوم مرتبة حسب الوقت
        today_attendance = db.session.query(AttendanceRecord)\
            .filter(AttendanceRecord.work_date == today)\
            .order_by(AttendanceRecord.check_in_time.desc())\
            .all()

        # بناء قاموس لآخر سجل لكل موظف (أحدث سجل)
        attendance_dict = {}
        for record in today_attendance:
            emp_id = int(record.employee_id)
            if emp_id not in attendance_dict:
                attendance_dict[emp_id] = record  # أول سجل يكون الأحدث لأنه مرتب desc

        attendances = []
        delays = []
        absences = []

        for employee, department in all_employees:
            employee_data = {
                'name': employee.full_name_arabic,
                'department': department.dep_name,
                'employee_number': employee.employee_number,
                'expected_time': employee.work_start_time.strftime('%H:%M')
            }

            # التحقق من الإجازة المبررة
            is_excused = (
                employee.is_leave == 'on' or
                employee.is_vacation == 'on' or
                employee.is_weekly_day_off == 'on'
            )

            is_leave_excused = (employee.is_leave == 'on')
            print(f"\n=== الموظف: {employee.full_name_arabic} ===")
            print(f"وقت العمل: {employee.work_start_time} - {employee.work_end_time}")
            print(f"في إجازة مبررة: {is_excused}")

            # معالجة آخر سجل للموظف
            if employee.id in attendance_dict:
                last_record = attendance_dict[employee.id]
                print(f"آخر سجل - دخول: {last_record.check_in_time}, خروج: {last_record.check_out_time}")
                
                # التحقق من وجود تسجيل دخول في آخر سجل
                if last_record.check_in_time:
                    last_check_in_time = last_record.check_in_time.time()
                    last_check_out_time = last_record.check_out_time.time() if last_record.check_out_time else None
                    
                    employee_data['check_in_time'] = last_check_in_time.strftime('%I:%M %p')
                    
                    # حساب التأخير بناءً على آخر دخول
                    work_start_minutes = time_to_minutes(employee.work_start_time)
                    work_end_minutes = time_to_minutes(employee.work_end_time)
                    checkin_minutes = time_to_minutes(last_check_in_time)
                    current_minutes = time_to_minutes(current_time)
                    
                    # حساب التأخير
                    delay_minutes = checkin_minutes - work_start_minutes
                    
                    # إذا كان وقت الحضور بعد نهاية الدوام (work_end_minutes)
                    if checkin_minutes > work_end_minutes:
                        is_delayed = False  # حضور عادي، ليس متأخر
                    else:
                        # إذا كان الحضور ضمن الدوام وتأخر 15 دقيقة أو أكثر
                        is_delayed = delay_minutes > 15
                    
                    # هل آخر دخول ضمن أوقات الدوام؟
                    is_checkin_during_work = work_start_minutes <= checkin_minutes <= work_end_minutes
                    
                    print(f"تأخير: {delay_minutes} دقيقة - متأخر 15+ دقيقة: {is_delayed}")
                    print(f"دخول ضمن أوقات الدوام: {is_checkin_during_work}")
                    
                    # معالجة الحالات
                    if last_check_out_time:
                        # يوجد تسجيل خروج
                        employee_data['check_out_time'] = last_check_out_time.strftime('%I:%M %p')
                        
                        checkout_minutes = time_to_minutes(last_check_out_time)
                        
                        # منطقة المسامحة (5 دقائق قبل انتهاء الدوام)
                        grace_period_start = work_end_minutes - 5
                        
                        # هل خرج ضمن أوقات الدوام؟
                        is_checkout_during_work = checkout_minutes < grace_period_start
                        is_checkout_in_grace_or_after = checkout_minutes >= grace_period_start
                        
                        print(f"وقت الخروج: {last_check_out_time}")
                        print(f"خروج ضمن الدوام (قبل المسامحة): {is_checkout_during_work}")
                        print(f"خروج في المسامحة أو بعدها: {is_checkout_in_grace_or_after}")
                        
                        if is_checkout_during_work:
                            if is_leave_excused:
                                employee_data['absence_type'] = 'مبرر'
                                print("النتيجة: غياب مبرر (لديه إذن + خروج مبكر)")
                            else:
                                employee_data['absence_type'] = 'غير مبرر'
                                print("النتيجة: غياب غير مبرر (خروج مبكر)")
                            
                            if is_delayed:
                                employee_data['delay_minutes'] = delay_minutes
                            
                            # حساب الخروج المبكر
                            early_departure = work_end_minutes - checkout_minutes
                            employee_data['early_departure_minutes'] = early_departure
                            absences.append(employee_data)
                            
                        elif is_checkout_in_grace_or_after:
                            # خرج في منطقة المسامحة أو بعدها
                            if is_checkout_in_grace_or_after and checkout_minutes <= work_end_minutes + 60:
                                # خرج في المسامحة أو خلال ساعة بعد الدوام = غياب مبرر
                                employee_data['absence_type'] = 'مبرر'
                                if is_delayed:
                                    employee_data['delay_minutes'] = delay_minutes
                                absences.append(employee_data)
                                print("النتيجة: غياب مبرر (خروج في المسامحة أو قريب من نهاية الدوام)")
                            else:
                                # خرج بعد الدوام بوقت طويل
                                if is_delayed:
                                    # متأخر لكن أكمل الدوام = تأخير
                                    employee_data['delay_minutes'] = delay_minutes
                                    delays.append(employee_data)
                                    print("النتيجة: تأخير (أكمل الدوام)")
                                else:
                                    # حضور طبيعي
                                    attendances.append(employee_data)
                                    print("النتيجة: حضور")
                    else:
                        # لا يوجد تسجيل خروج
                        print("لا يوجد تسجيل خروج")
                        
                        if current_minutes > work_end_minutes:
                            # انتهى الدوام ولم يسجل خروج
                            if is_delayed:
                                # متأخر + لم يسجل خروج = تأخير
                                employee_data['delay_minutes'] = delay_minutes
                                delays.append(employee_data)
                                print("النتيجة: تأخير (لم يسجل خروج بعد انتهاء الدوام)")
                            else:
                                # حضور طبيعي ولم يسجل خروج
                                attendances.append(employee_data)
                                print("النتيجة: حضور (لم يسجل خروج بعد انتهاء الدوام)")
                        else:
                            # ما زال في الدوام
                            if is_checkin_during_work:
                                if is_delayed:
                                    # متأخر وما زال في الدوام = تأخير
                                    employee_data['delay_minutes'] = delay_minutes
                                    delays.append(employee_data)
                                    print("النتيجة: تأخير (ما زال في الدوام)")
                                else:
                                    # حضور طبيعي وما زال في الدوام = حضور
                                    attendances.append(employee_data)
                                    print("النتيجة: حضور (ما زال في الدوام)")
                            else:
                                # دخول خارج أوقات الدوام
                                attendances.append(employee_data)
                                print("النتيجة: حضور (دخول خارج أوقات الدوام)")
                else:
                    # لا يوجد تسجيل دخول في آخر سجل
                    employee_data['absence_type'] = 'مبرر' if is_excused else 'غير مبرر'
                    absences.append(employee_data)
                    print("النتيجة: غياب (لا يوجد تسجيل دخول في آخر سجل)")
            else:
                # لا يوجد أي سجل حضور اليوم
                current_minutes = time_to_minutes(current_time)
                work_start_minutes = time_to_minutes(employee.work_start_time)
                
                print("لا يوجد سجل حضور اليوم")
                
                # التحقق من التوقيت
                if current_minutes > work_start_minutes + 30:
                    # تجاوز وقت العمل بأكثر من 30 دقيقة = غياب
                    employee_data['absence_type'] = 'مبرر' if is_excused else 'غير مبرر'
                    absences.append(employee_data)
                    print("النتيجة: غياب (تجاوز وقت العمل)")
                else:
                    # ما زال في الوقت المسموح
                    if is_excused:
                        employee_data['absence_type'] = 'مبرر'
                        absences.append(employee_data)
                        print("النتيجة: غياب مبرر")
                    else:
                        print("النتيجة: في الانتظار (لم يتجاوز الوقت المسموح)")

        attendance_count = len(attendances)
        delay_count = len(delays)
        absence_count = len(absences)

        print(f"\n=== الملخص النهائي ===")
        print(f"حضور: {attendance_count}")
        print(f"تأخير: {delay_count}")
        print(f"غياب: {absence_count}")
        print(f"المجموع: {total_all_employees}")

        return jsonify({
            'attendances': {
                'data': attendances,
                'stats': f'{attendance_count} out of {total_all_employees}',
                'title': 'الحضور اليوم'
            },
            'delays': {
                'data': delays,
                'stats': f'{delay_count} out of {total_all_employees}',
                'title': 'التأخيرات اليوم'
            },
            'absences': {
                'data': absences,
                'stats': f'{absence_count} out of {total_all_employees}',
                'title': 'الغيابات اليوم'
            },
            'summary': {
                'total': total_all_employees,
                'present': attendance_count + delay_count,
                'on_time': attendance_count,
                'delayed': delay_count,
                'absent': absence_count,
                'date': today.strftime('%Y-%m-%d')
            }
        }), 200

    except Exception as e:
        print("خطأ في get_dashboard_data:", e)
        traceback.print_exc()  # 👈 يطبع كامل الخطأ بما فيه السطر المسبب
        return jsonify({"error": "حدث خطأ في استرجاع البيانات"}), 500
@app.route('/test-db')
def test_db():
    try:
        result = db.session.execute(text("SELECT 1"))
        return "تم الاتصال بقاعدة البيانات بنجاح!"
    except Exception as e:
        return f"فشل الاتصال بقاعدة البيانات: {e}"
@app.route('/')
def index():
    if 'employee' in session:
        employee = session['employee']
        return jsonify({"message": f"مرحبًا {employee['full_name_arabic']}، أنت مسجل دخول"})
    else:
        return jsonify({"message": "يرجى تسجيل الدخول"}), 401   
#Employees Section
from datetime import datetime, time, timedelta
import pytz  # إضافة مكتبة pytz للمناطق الزمنية
# في بداية الملف، أضف الاستيرادات المطلوبة
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from threading import Lock

# إنشاء scheduler عام
scheduler = BackgroundScheduler(timezone=pytz.timezone('Asia/Damascus'))
scheduler.start()

# قاموس لتتبع المهام المجدولة لكل موظف
scheduled_checkouts = {}
checkout_lock = Lock()

def schedule_auto_checkout(employee_id, work_end_time):
    """
    جدولة الخروج التلقائي للموظف
    """
    try:
        with checkout_lock:
            # إلغاء المهمة السابقة إن وجدت
            if employee_id in scheduled_checkouts:
                try:
                    scheduler.remove_job(scheduled_checkouts[employee_id])
                except:
                    pass
                del scheduled_checkouts[employee_id]
            
            # حساب وقت الخروج التلقائي (وقت انتهاء العمل + 30 دقيقة)
            damascus_tz = pytz.timezone('Asia/Damascus')
            today = datetime.now(damascus_tz).date()
            
            # تحويل وقت انتهاء العمل إلى datetime
            if isinstance(work_end_time, str):
                hours, minutes = work_end_time.split(':')
                work_end_dt = datetime.combine(today, datetime.min.time().replace(hour=int(hours), minute=int(minutes)))
            else:
                work_end_dt = datetime.combine(today, work_end_time)
            
            work_end_dt = damascus_tz.localize(work_end_dt)
            auto_checkout_time = work_end_dt + timedelta(minutes=30)
            
            # التحقق من أن الوقت لم يمر بعد
            current_time = datetime.now(damascus_tz)
            if auto_checkout_time <= current_time:
                # إذا فات الوقت، قم بالخروج فوراً
                perform_auto_checkout(employee_id)
                return
            
            # إنشاء job_id فريد
            job_id = f"auto_checkout_{employee_id}_{today.strftime('%Y%m%d')}"
            
            # جدولة المهمة
            scheduler.add_job(
                func=perform_auto_checkout,
                trigger=DateTrigger(run_date=auto_checkout_time),
                args=[employee_id],
                id=job_id,
                replace_existing=True
            )
            
            # حفظ معرف المهمة
            scheduled_checkouts[employee_id] = job_id
            
            print(f"تم جدولة الخروج التلقائي للموظف {employee_id} في {auto_checkout_time}")
            
    except Exception as e:
        print(f"خطأ في جدولة الخروج التلقائي: {str(e)}")

def perform_auto_checkout(employee_id):
    with app.app_context():  # نقل السياق ليشمل الكل
        try:
            employee = db.session.get(Employee, employee_id)
            
            if not employee:
                print(f"الموظف {employee_id} غير موجود")
                return
            
            if employee.status != 'on':
                print(f"الموظف {employee_id} ليس في حالة عمل")
                return
            
            damascus_tz = pytz.timezone('Asia/Damascus')
            current_time = datetime.now(damascus_tz)
            today = current_time.date()
            
            record = AttendanceRecord.query.filter_by(
                employee_id=employee.id,
                work_date=today,
                check_out_time=None
            ).first()
            
            if not record:
                print(f"لا يوجد سجل حضور نشط للموظف {employee_id}")
                return
            
            record.check_out_time = current_time
            record.is_auto_checkout = True
            employee.status = 'off'
            
            if record.check_in_time:
                check_in = record.check_in_time.astimezone(damascus_tz)
                check_out = current_time
                
                work_seconds = (check_out - check_in).total_seconds()
                office_work_hours = round(work_seconds / 3600, 2)
                record.office_work_hours = office_work_hours
            
                work_start_dt = datetime.combine(today, employee.work_start_time)
                work_end_dt = datetime.combine(today, employee.work_end_time)
                
                work_start_dt = damascus_tz.localize(work_start_dt)
                work_end_dt = damascus_tz.localize(work_end_dt)
                
                start_work = max(check_in, work_start_dt)
                end_work = min(check_out, work_end_dt)
                
                if start_work < end_work:
                    work_seconds_within = (end_work - start_work).total_seconds()
                    work_hours_within = round(work_seconds_within / 3600, 2)
                else:
                    work_hours_within = 0
                
                record.work_hours = work_hours_within
            db.session.commit()
            print(f"تم حفظ التغييرات في قاعدة البيانات للموظف {employee_id}")    
            if employee.telegram_chatid:
                telegram_message = f"""🔔 <b>خروج تلقائي</b>
تم تسجيل خروجك تلقائياً الساعة {current_time.strftime('%H:%M')} (بتوقيت دمشق) بعد نصف ساعة من انتهاء دوامك الرسمي، نظراً لعدم تسجيل الخروج في الوقت المحدد.

إذا رغبت في تعويض وقت الدوام أو تسجيل دوام إضافي، يرجى:
1. الانتقال إلى التطبيق الآن
2. استخدام الأزرار المخصصة:
   • زر <b>طلب تعويض</b> لطلب من المشرف تعويض ساعات الاجازة
   • زر <b>طلب إضافي</b> لطلب من المشرف ساعات إضافية

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{current_time.strftime('%Y-%m-%d %I:%M %p')}
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡"""
                # استدعاء الدالة بعد تعريفها
                send_telegram_message(employee.telegram_chatid, telegram_message)
            with checkout_lock:
                if employee_id in scheduled_checkouts:
                    del scheduled_checkouts[employee_id]
            
            print(f"تم تسجيل الخروج التلقائي للموظف {employee_id} بنجاح")
            
        except Exception as e:
            if db.session.is_active:
                db.session.rollback()
            print(f"خطأ في الخروج التلقائي للموظف {employee_id}: {str(e)}")
            traceback.print_exc()  # طباعة تفاصيل الخطأ
def cancel_auto_checkout(employee_id):
    """
    إلغاء الخروج التلقائي المجدول للموظف
    """
    try:
        with checkout_lock:
            if employee_id in scheduled_checkouts:
                job_id = scheduled_checkouts[employee_id]
                try:
                    scheduler.remove_job(job_id)
                    print(f"تم إلغاء الخروج التلقائي للموظف {employee_id}")
                except:
                    pass
                del scheduled_checkouts[employee_id]
    except Exception as e:
        print(f"خطأ في إلغاء الخروج التلقائي: {str(e)}")

# جلب الأزرار الخاصة بقسم الموظف الحالي
@app.route('/api/special-buttons/employee', methods=['GET'])
def get_employee_special_buttons():
    if 'employee' not in session:
        return jsonify({"message": "يرجى تسجيل الدخول"}), 401
    
    try:
        employee_id = session['employee']['id']
        employee = db.session.get(Employee, employee_id)
        
        if not employee:
            return jsonify({'success': False, 'message': 'الموظف غير موجود'}), 404
        
        # جلب الأزرار الخاصة بقسم الموظف
        buttons = SpecialButton.query.filter_by(department_id=employee.department_id).all()
        result = []
        
        for button in buttons:
            result.append({
                'id': button.id,
                'name': button.name,
                'link': button.link,
                'department_id': button.department_id
            })
        
        return jsonify({'success': True, 'data': result}), 200
        
    except Exception as e:
        return jsonify({
            'success': False, 
            'message': f'خطأ في جلب الأزرار الخاصة: {str(e)}'
        }), 500
# تحديث route تسجيل الدخول/الخروج
@app.route('/api/attendance', methods=['POST'])
def handle_attendance():
    try:
        if 'employee' not in session:
            return jsonify({
                'success': False,
                'message': 'يجب تسجيل الدخول أولاً'
            }), 401

        employee_id = session['employee']['id']
        employee = db.session.get(Employee, employee_id)
        
        damascus_tz = pytz.timezone('Asia/Damascus')
        current_time = datetime.now(damascus_tz)
        today = current_time.date()

        if not employee:
            return jsonify({
                'success': False,
                'message': 'الموظف غير موجود'
            }), 404

        # 1. الحصول على المشرف المسؤول عن قسم الموظف
        department = employee.department
        supervisor = None
        
        if department and department.supervisors:
            # بما أن كل قسم له مشرف واحد فقط، نأخذ أول مشرف
            supervisor = department.supervisors[0]
        
        # 2. إذا لم يوجد مشرف، نبحث عن مشرف بديل
        if not supervisor:
            # نبحث عن أي مشرف في النظام
            fallback_supervisor = Supervisor.query.first()
            
            if fallback_supervisor:
                supervisor = fallback_supervisor
                # تسجيل خطأ في السجلات
                print(f"لم يتم العثور على مشرف للقسم {employee.department_id}، تم استخدام مشرف بديل: {supervisor.supervisor_ID}")
            else:
                # في حالة عدم وجود أي مشرف في النظام
                print("لا يوجد أي مشرفين في النظام!")
                return jsonify({
                    'success': False,
                    'message': 'حدث خطأ في النظام'
                }), 500

        existing_record = AttendanceRecord.query.filter(
            AttendanceRecord.employee_id == employee_id,
            AttendanceRecord.work_date == today,
            AttendanceRecord.check_out_time.is_(None)
        ).first()

        if not existing_record:  # Check-in
            employee.status = 'on'
            db.session.commit()

            new_record = AttendanceRecord(
                employee_id=employee_id,
                check_in_time=current_time,
                work_date=today
            )
            db.session.add(new_record)
            db.session.commit()

            # جدولة الخروج التلقائي
            schedule_auto_checkout(employee.id, employee.work_end_time)

            start_time = employee.work_start_time
            actual_start = damascus_tz.localize(datetime.combine(today, start_time))
            delay_start_time = actual_start + timedelta(minutes=16)
            
            if current_time > delay_start_time:
                delay_seconds = (current_time - delay_start_time).total_seconds()
                delay_minutes = int(delay_seconds // 60)
                
                delay_record = WorkDelayArchive(
                    employee_id=employee_id,
                    supervisor_id=supervisor.supervisor_ID,
                    date=today,
                    minutes_delayed=delay_minutes,
                    from_timestamp=delay_start_time,
                    to_timestamp=current_time,
                    status='Unjustified',
                    delay_note=f'تأخير غير مبرر: {delay_minutes} دقيقة'
                )
                db.session.add(delay_record)
                db.session.commit()
                
                # إرسال إشعار للمشرف
                supervisor_employee = supervisor.employee
                if supervisor_employee and supervisor_employee.telegram_chatid:
                    allowed_start_time = actual_start + timedelta(minutes=16)
                    message = (
                        f"🔔 <b>إشعار تأخير موظف</b>\n\n"
                        f"• الموظف: <b>{employee.full_name_arabic}</b>\n"
                        f"• القسم: <b>{department.dep_name if department else 'غير معروف'}</b>\n"
                        f"• مدة التأخير: <b>{delay_minutes} دقيقة</b>\n"
                        f"• وقت الدخول الفعلي: <b>{current_time.strftime('%Y-%m-%d %I:%M %p')}</b>\n"
                        f"• فترة التأخير: من <b>{allowed_start_time.strftime('%I:%M %p')}</b> "
                        f"إلى <b>{current_time.strftime('%I:%M %p')}</b>"
                    )
                    send_telegram_message(supervisor_employee.telegram_chatid, message)
            
            return jsonify({
                'success': True,
                'message': 'تم تسجيل الحضور بنجاح',
                'operation_type': 'check_in'
            })
            
        else:  # Check-out
            employee.status = 'off'
            db.session.commit()

            # إلغاء الخروج التلقائي المجدول
            cancel_auto_checkout(employee.id)

            existing_record.check_out_time = current_time
            
            if existing_record.check_in_time:
                check_in = existing_record.check_in_time.astimezone(damascus_tz)
                check_out = current_time
                
                # حساب ساعات العمل الفعلية
                work_seconds = (check_out - check_in).total_seconds()
                office_work_hours = round(work_seconds / 3600, 2)
                existing_record.office_work_hours = office_work_hours
            
                # حساب ساعات العمل ضمن الدوام
                work_start = employee.work_start_time
                work_end = employee.work_end_time
                
                work_start_dt = damascus_tz.localize(datetime.combine(today, work_start))
                work_end_dt = damascus_tz.localize(datetime.combine(today, work_end))
                
                start_work = max(check_in, work_start_dt)
                end_work = min(check_out, work_end_dt)
                
                if start_work < end_work:
                    work_seconds_within = (end_work - start_work).total_seconds()
                    work_hours_within = round(work_seconds_within / 3600, 2)
                else:
                    work_hours_within = 0
                    
                existing_record.work_hours = work_hours_within
            
            db.session.commit()

            return jsonify({
                'success': True,
                'message': 'تم تسجيل الانصراف بنجاح',
                'operation_type': 'check_out'
            })
            
    except Exception as e:
        db.session.rollback()
        print(f"حدث خطأ في تسجيل الحضور: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'حدث خطأ: {str(e)}'
        }), 500

# إبقاء route منفصل للخروج التلقائي للمرونة
@app.route('/api/attendance/auto-checkout', methods=['POST'])
def auto_checkout():
    # التحقق من وجود جلسة الموظف
    if 'employee' not in session:
        return jsonify({
            'success': False,
            'message': 'يجب تسجيل الدخول أولاً'
        }), 401
    try:
        employee_id = session['employee']['id']
        employee = db.session.get(Employee, employee_id)
       
        damascus_tz = pytz.timezone('Asia/Damascus')
        current_time = datetime.now(damascus_tz)
        today = current_time.date()
        
        if not employee:
            return jsonify({
                'success': False,
                'message': 'الموظف غير موجود'
            }), 404
        
        # التحقق من أن الموظف مسجل دخول
        if employee.status != 'on':
            return jsonify({
                'success': False,
                'message': 'الموظف ليس في حالة عمل'
            }), 400
        
        # البحث عن سجل الحضور النشط
        record = AttendanceRecord.query.filter_by(
            employee_id=employee.id,
            work_date=today,
            check_out_time=None
        ).first()
        
        if not record:
            return jsonify({
                'success': False,
                'message': 'لا يوجد سجل حضور نشط'
            }), 400
        
        # تسجيل الخروج التلقائي
        record.check_out_time = current_time
        record.is_auto_checkout = True  # تمييز أنه خروج تلقائي
        employee.status = 'off'
        
        # حساب ساعات العمل (كما في الخروج العادي)
        if record.check_in_time:
            check_in = record.check_in_time.astimezone(damascus_tz)
            check_out = current_time
           
            # حساب ساعات العمل الفعلية
            work_seconds = (check_out - check_in).total_seconds()
            office_work_hours = round(work_seconds / 3600, 2)
            record.office_work_hours = office_work_hours
       
            # حساب ساعات العمل ضمن الدوام
            work_start_dt = datetime.combine(today, employee.work_start_time)
            work_end_dt = datetime.combine(today, employee.work_end_time)
           
            work_start_dt = damascus_tz.localize(work_start_dt)
            work_end_dt = damascus_tz.localize(work_end_dt)
           
            start_work = max(check_in, work_start_dt)
            end_work = min(check_out, work_end_dt)
           
            if start_work < end_work:
                work_seconds_within = (end_work - start_work).total_seconds()
                work_hours_within = round(work_seconds_within / 3600, 2)
            else:
                work_hours_within = 0
               
            record.work_hours = work_hours_within
        
        db.session.commit()
        
        # إرسال إشعار للموظف
        notification = Notification(
            recipient_id=employee.id,
            message=f"تم تسجيل خروجك تلقائياً في {current_time.strftime('%H:%M')}",
            read=False,
            type='auto_checkout'
        )
        db.session.add(notification)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'تم تسجيل الخروج تلقائياً بنجاح',
            'operation_type': 'auto_checkout'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'حدث خطأ: {str(e)}'
        }), 500

# إضافة route للحصول على حالة الخروج التلقائي
@app.route('/api/attendance/auto-checkout-status/<int:employee_id>', methods=['GET'])
def get_auto_checkout_status(employee_id):
    try:
        with checkout_lock:
            is_scheduled = employee_id in scheduled_checkouts
            
        if is_scheduled:
            job_id = scheduled_checkouts[employee_id]
            job = scheduler.get_job(job_id)
            if job:
                return jsonify({
                    'success': True,
                    'scheduled': True,
                    'next_run_time': job.next_run_time.isoformat()
                })
        
        return jsonify({
            'success': True,
            'scheduled': False
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ: {str(e)}'
        }), 500

# تنظيف الـ scheduler عند إغلاق التطبيق
import atexit
atexit.register(lambda: scheduler.shutdown())
# أضف هذا Route في الباك إند إذا لم تضعه
@app.route('/api/user/status', methods=['GET'])
def get_user_status():
    if 'employee' not in session:
        return jsonify({
            'success': False,
            'message': 'يجب تسجيل الدخول أولاً'
        }), 401
    
    try:
        employee_id = session['employee']['id']
        employee = db.session.get(Employee, employee_id)
        
        if not employee:
            return jsonify({
                'success': False,
                'message': 'الموظف غير موجود'
            }), 404
        
        return jsonify({
            'success': True,
            'status': employee.status,  # 'on' أو 'off'
            'employee_id': employee.id
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ: {str(e)}'
        }), 500
@app.route('/api/delay-archive', methods=['GET'])
def get_delay_archive():
    """
    جلب أرشيف التأخيرات للمستخدم المتصل فقط (تأخيراته الشخصية فقط)
    """
    if 'employee' not in session:
        return jsonify({
            'success': False,
            'message': 'غير مسموح - يجب تسجيل الدخول أولاً'
        }), 401
   
    try:
        employee_id = session['employee']['id']
       
        # إعداد الاستعلام الأساسي
        query = db.session.query(
            WorkDelayArchive,
            Employee.full_name_arabic.label('employee_name')
        ).join(Employee, WorkDelayArchive.employee_id == Employee.id)
       
        # جلب السجلات التي يكون المستخدم موظفًا فيها فقط (تأخيراته الشخصية)
        query = query.filter(WorkDelayArchive.employee_id == employee_id)
       
        # ترتيب النتائج (الأحدث أولاً - بناءً على ID أو timestamp)
        delays_data = query.order_by(
            WorkDelayArchive.id.desc()  # أو WorkDelayArchive.timestamp.desc() إذا كان متاحاً
        ).all()
       
        # تحويل النتائج لقوائم
        delays_list = [
            {
                'id': delay.id,
                'timestamp': delay.timestamp.isoformat() if delay.timestamp else None,
                'employee_id': delay.employee_id,
                'employee_name': employee_name,
                'supervisor_id': delay.supervisor_id,
                'date': delay.date.isoformat() if delay.date else None,
                'minutes_delayed': delay.minutes_delayed,
                'from_timestamp': delay.from_timestamp.isoformat() if delay.from_timestamp else None,
                'to_timestamp': delay.to_timestamp.isoformat() if delay.to_timestamp else None,
                'delay_note': delay.delay_note,
                'status': delay.status
            }
            for delay, employee_name in delays_data
        ]
       
        return jsonify({
            'success': True,
            'delays': delays_list,
            'total_count': len(delays_list)
        })
       
    except Exception as e:
        print("حدث استثناء في /api/delay-archive:")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'message': f'حدث خطأ أثناء جلب البيانات: {str(e)}'
        }), 500
@app.route('/api/compensation-leave-requests', methods=['GET'])
def get_compensation_leave_requests():
    # التحقق من وجود session
    if 'employee' not in session:
        return jsonify({"message": "غير مسموح - يجب تسجيل الدخول أولاً"}), 401
    
    try:
        employee_id = session['employee']['id']
        
        # جلب جميع طلبات تعويض الإجازات للموظف المتصل
        requests = CompensationLeaveRequest.query.filter_by(
            employee_id=employee_id
        ).order_by(
            CompensationLeaveRequest.timestamp.desc()
        ).all()
        
        # تحويل البيانات إلى قاموس
        requests_data = []
        for req in requests:
            requests_data.append({
                'id': req.id,
                'timestamp': req.timestamp.strftime('%Y-%m-%d %H:%M:%S') if req.timestamp else None,
                'date': req.date.strftime('%Y-%m-%d') if req.date else None,
                'hours_requested': req.hours_requested,
                'status': req.status,
                'start_time': req.start_time.strftime('%H:%M:%S') if req.start_time else None,
                'end_time': req.end_time.strftime('%H:%M:%S') if req.end_time else None,
                'note': req.note,
                'employee_id': req.employee_id,
                'supervisor_id': req.supervisor_id
            })
        
        return jsonify({
            "message": "تم جلب البيانات بنجاح",
            "requests": requests_data,
            "total": len(requests_data)
        }), 200
        
    except Exception as e:
        print(f"Error fetching compensation leave requests: {str(e)}")
        return jsonify({
            "message": "حدث خطأ أثناء جلب البيانات",
            "error": str(e)
        }), 500
@app.route('/api/compensation-leave-requests/<int:request_id>', methods=['DELETE'])
def delete_compensation_leave_request(request_id):
    # التحقق من وجود جلسة للموظف
    if 'employee' not in session:
        return jsonify({"message": "غير مسموح - يجب تسجيل الدخول أولاً"}), 401
    
    try:
        employee_id = session['employee']['id']
        
        # البحث عن الطلب المرتبط بالموظف
        comp_request = CompensationLeaveRequest.query.filter_by(
            id=request_id,
            employee_id=employee_id
        ).first()
        
        if not comp_request:
            return jsonify({"message": "طلب التعويض غير موجود أو لا يتعلق بهذا الموظف"}), 404
        
        # حذف الطلب من قاعدة البيانات
        db.session.delete(comp_request)
        db.session.commit()
        
        return jsonify({
            "message": "تم حذف طلب التعويض بنجاح"
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"خطأ في حذف طلب التعويض: {str(e)}")
        return jsonify({
            "message": "حدث خطأ أثناء حذف الطلب",
            "error": str(e)
        }), 500
@app.route('/api/leave-requests', methods=['POST'])
def create_leave_request():
    try:
        print("=== بدء إنشاء طلب إجازة ===")
        
        if 'employee' not in session:
            print("❌ لم يتم تسجيل الدخول")
            return jsonify({"message": "يرجى تسجيل الدخول"}), 401

        syria_tz = pytz.timezone("Asia/Damascus")
        leave_type_arabic = {
            'hourly': 'ساعية',
            'daily': 'يومية',
            'multi-day': 'متعددة الأيام'
        }

            # تعريف قاموس تحويل تصنيفات الإجازات إلى العربية
        classification_arabic = {
                'regular': 'عادية',
                'sick': 'مرضية',
                'emergency': 'خاصة'
        }
        employee_id = session['employee']['id']
        print(f"Employee ID: {employee_id}")

        data = request.get_json()
        print(f"البيانات المستلمة: {data}")

        # التحقق من البيانات المطلوبة
        required_fields = ['classification', 'type', 'start_date', 'note']
        print(f"الحقول المطلوبة: {required_fields}")
        
        if not all(field in data for field in required_fields):
            print("❌ بيانات ناقصة")
            return jsonify({"message": "بيانات ناقصة"}), 400

        # تحويل التصنيف من 'normal' إلى 'regular'
        if data['classification'] == 'normal':
            data['classification'] = 'regular'
            print("تم تحويل التصنيف من 'normal' إلى 'regular'")

        # تحقق من الحقول الإضافية
        if data['type'] == 'hourly':
            print("التحقق من الحقول الساعية...")
            if 'start_time' not in data or 'end_time' not in data:
                print("❌ نقص في بيانات الوقت")
                return jsonify({"message": "يجب تحديد وقت البداية والنهاية للإجازة الساعية"}), 400
                
        elif data['type'] == 'multi-day' and 'end_date' not in data:
            print("❌ نقص في تاريخ النهاية")
            return jsonify({"message": "يجب تحديد تاريخ النهاية للإجازة المتعددة الأيام"}), 400

        employee = db.session.get(Employee, employee_id)
        print(f"بيانات الموظف: {employee}")
        
        if not employee:
            print("❌ الموظف غير موجود")
            return jsonify({"message": "الموظف غير موجود"}), 404

        # طباعة أرصدة الإجازات الحالية
        print("=== أرصدة الإجازات الحالية ===")
        print(f"رصيد الإجازة العادية: {employee.regular_leave_remaining} ساعة")
        print(f"رصيد الإجازة المرضية: {employee.sick_leave_remaining} ساعة")
        print(f"رصيد الإجازة الخاصة: {employee.emergency_leave_remaining} ساعة")
        print(f"الإجازة العادية المستخدمة: {employee.regular_leave_used} ساعة")
        print(f"الإجازة المرضية المستخدمة: {employee.sick_leave_used} ساعة")
        print(f"الإجازة الخاصة المستخدمة: {employee.emergency_leave_used} ساعة")
        print("=============================")

        department_supervisors = Supervisor.query.filter_by(dep_id=employee.department_id).all()
        print(f"المشرفون: {department_supervisors}")
        
        if not department_supervisors:
            print("❌ لا يوجد مشرفين")
            return jsonify({"message": "المشرف غير موجود"}), 404

        # حساب مدة الإجازة
        hours_requested = 0.0
        start_dt = end_dt = None
        print(f"نوع الإجازة: {data['type']}")

        if data['type'] == 'hourly':
            print("معالجة الإجازة الساعية...")
            start_time = datetime.strptime(data['start_time'], '%H:%M').time()
            end_time = datetime.strptime(data['end_time'], '%H:%M').time()
            start_dt = datetime.combine(datetime.today(), start_time)
            end_dt = datetime.combine(datetime.today(), end_time)
            if end_dt < start_dt:
                end_dt += timedelta(days=1)
            hours_requested = (end_dt - start_dt).total_seconds() / 3600
            start_date = end_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            print(f"الساعات المطلوبة: {hours_requested}")

        elif data['type'] == 'daily':
            print("معالجة الإجازة اليومية...")
            start_dt = datetime.combine(datetime.today(), employee.work_start_time if employee.work_start_time else datetime.strptime('09:00', '%H:%M').time())
            end_dt = datetime.combine(datetime.today(), employee.work_end_time if employee.work_end_time else datetime.strptime('17:00', '%H:%M').time())
            if end_dt < start_dt:
                end_dt += timedelta(days=1)
            hours_requested = (end_dt - start_dt).total_seconds() / 3600
            start_date = end_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            print(f"الساعات المطلوبة: {hours_requested}")

        elif data['type'] == 'multi-day':
            print("معالجة الإجازة المتعددة الأيام...")
            start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
            if end_date < start_date:
                print("❌ تاريخ النهاية قبل البداية")
                return jsonify({"message": "تاريخ النهاية يجب أن يكون بعد تاريخ البداية"}), 400
            num_days = (end_date - start_date).days + 1
            start_dt = datetime.combine(datetime.today(), employee.work_start_time if employee.work_start_time else datetime.strptime('09:00', '%H:%M').time())
            end_dt = datetime.combine(datetime.today(), employee.work_end_time if employee.work_end_time else datetime.strptime('17:00', '%H:%M').time())
            if end_dt < start_dt:
                end_dt += timedelta(days=1)
            daily_hours = (end_dt - start_dt).total_seconds() / 3600
            hours_requested = num_days * daily_hours
            print(f"عدد الأيام: {num_days}, الساعات اليومية: {daily_hours}, المجموع: {hours_requested}")

        # التحقق من كونه مشرفاً
        is_supervisor = Supervisor.query.filter_by(supervisor_ID=employee_id).first() is not None
        print(f"هل هو مشرف: {is_supervisor}")
        status = 'approved' if is_supervisor else 'pending'
        print(f"الحالة: {status}")

        # التحقق من الرصيد
        classification = data['classification']
        print(f"تصنيف الإجازة: {classification}")

        if classification == 'regular':
            current_balance = employee.regular_leave_remaining
            print(f"الرصيد المتاح للإجازة العادية: {current_balance} ساعة")
        elif classification == 'sick':
            current_balance = employee.sick_leave_remaining
            print(f"الرصيد المتاح للإجازة المرضية: {current_balance} ساعة")
        elif classification == 'emergency':
            current_balance = employee.emergency_leave_remaining
            print(f"الرصيد المتاح للإجازة الخاصة: {current_balance} ساعة")
        else:
            current_balance = 0
            print(f"❌ تصنيف غير معروف: {classification}")

        # حساب مجموع ساعات الطلبات المعلقة لنفس التصنيف
        pending_requests = LeaveRequest.query.filter_by(
            employee_id=employee_id,
            classification=classification,
            status='pending'
        ).all()
        total_pending_hours = sum(req.hours_requested for req in pending_requests)

        available_balance = current_balance - total_pending_hours

        print(f"الرصيد المتاح (بعد خصم الطلبات المعلقة): {available_balance} ساعة, الساعات المطلوبة: {hours_requested} ساعة")

        if hours_requested > available_balance:
            print("❌ رصيد غير كافي (بعد احتساب الطلبات المعلقة)")
            return jsonify({
                "message": "رصيد الإجازة غير كافي عند احتساب الطلبات المعلقة",
                "requested": hours_requested,
                "available": available_balance,
                "pending_requests": total_pending_hours
            }), 400
            
        # إنشاء سجل الإجازة
        new_request = LeaveRequest(
            timestamp=datetime.now(syria_tz),
            employee_id=employee_id,
            supervisor_id=department_supervisors[0].supervisor_ID,
            type=data['type'],
            classification=classification,
            start_date=start_date,
            end_date=end_date if data['type'] == 'multi-day' else None,
            hours_requested=hours_requested,
            status=status,
            note=data['note'],
            start_time=start_dt.time() if data['type'] == 'hourly' else None,
            end_time=end_dt.time() if data['type'] == 'hourly' else None
        )
        print(f"طلب الإجازة الجديد: {new_request.__dict__}")

        db.session.add(new_request)
        db.session.flush()
        print(f"تم إنشاء الطلب برقم: {new_request.id}")

        # إذا كان الطلب معتمداً تلقائياً (مشرف) نخصم الرصيد
        if is_supervisor:
            print("خصم الرصيد للمشرف...")
            if classification == 'regular':
                employee.regular_leave_used += hours_requested
                employee.regular_leave_remaining -= hours_requested
                print(f"تم تحديث رصيد الإجازة العادية - المستخدم: {employee.regular_leave_used}, المتبقي: {employee.regular_leave_remaining}")
            elif classification == 'sick':
                employee.sick_leave_used += hours_requested
                employee.sick_leave_remaining -= hours_requested
                print(f"تم تحديث رصيد الإجازة المرضية - المستخدم: {employee.sick_leave_used}, المتبقي: {employee.sick_leave_remaining}")
            elif classification == 'emergency':
                employee.emergency_leave_used += hours_requested
                employee.emergency_leave_remaining -= hours_requested
                print(f"تم تحديث رصيد الإجازة الخاصة - المستخدم: {employee.emergency_leave_used}, المتبقي: {employee.emergency_leave_remaining}")
            print("تم خصم الرصيد")

        medical_message = ""
        if classification == 'sick':
            medical_message = "يرجى أيضاً التواصل مع مسؤول قسم الموارد البشرية لعرض التقارير الطبية لحالتك، مع تمنياتنا لك بالسلامة.🩹"
            print("تم إضافة رسالة طبية")

        # إعداد رسائل التلغرام مع تواريخ مناسبة
        date_info = ""
        if data['type'] == 'multi-day':
            date_info = f"📅 من {data['start_date']} إلى {data['end_date']}"
        elif data['type'] == 'daily':
            date_info = f"📅 تاريخ {data['start_date']}"
        elif data['type'] == 'hourly':
            date_info = f"📅 تاريخ {data['start_date']} ⏰ من {data['start_time']} إلى {data['end_time']}"
        archive_message = None  # تعريف مسبق
        # إرسال الإشعارات
        if not is_supervisor:
            print("إرسال إشعارات للمشرفين...")
            for supervisor in department_supervisors:
                notification = Notification(
                    recipient_id=supervisor.supervisor_ID,
                    message=f"طلب إجازة جديد من الموظف {employee.full_name_arabic}. {medical_message}"
                )
                db.session.add(notification)
                print(f"تم إنشاء إشعار للمشرف: {supervisor.supervisor_ID}")

                # إرسال رسالة التلغرام للمشرف
                supervisor_employee = db.session.get(Employee, supervisor.supervisor_ID)
                if supervisor_employee and supervisor_employee.telegram_chatid:
                    telegram_message = f"""
👤 <b>طلب إجازة جديد</b>

📋 <b>الموظف:</b> {employee.full_name_arabic}
🏷️ <b>التصنيف:</b> {classification}
📊 <b>النوع:</b> {data['type']}
{date_info}
⏱️ <b>المدة:</b> {hours_requested} ساعة
📝 <b>ملاحظة:</b> {data['note']}

{"يرجى أيضاً اخبار الموظف بالتواصل مع مسؤول قسم الموارد البشرية لعرض التقارير الطبية لحالة الموظف، مع تمنياتنا له بالسلامة🩹." if classification == 'sick' else ""}
                    """
                    send_telegram_message(supervisor_employee.telegram_chatid, telegram_message)
                if classification == 'sick' and employee.telegram_chatid:
                    sick_message = f"تم إرسال الإجازة المرضية إلى المشرف. {medical_message}"
                    send_telegram_message(employee.telegram_chatid, sick_message)
        else:
            print("إرسال إشعار للموظف (مشرف)")
            notification = Notification(
                recipient_id=employee_id,
                message=f"تم قبول طلب إجازتك تلقائياً. {medical_message}"
            )
            db.session.add(notification)
            
            # إرسال رسالة التلغرام للموظف (المشرف)
            if employee.telegram_chatid:
                telegram_message = f"""
✅ <b>تم قبول طلب إجازتك تلقائياً</b>

🏷️ <b>التصنيف:</b> {classification}
{date_info}
⏱️ <b>المدة:</b> {hours_requested} ساعة
📝 <b>ملاحظة:</b> {data['note']}

{medical_message if medical_message else ''}
                """
                send_telegram_message(employee.telegram_chatid, telegram_message)
            archive_message = f"""
📋 طلب معتمد - أرشيف
━━━━━━━━━━━━━━━━━━━━
📄 نوع الطلب: إجازة
👤 الموظف: {employee.full_name_arabic}
🏢 القسم: {employee.department.dep_name if employee.department else "غير محدد"}
👨‍💼 المشرف: {Supervisor.query.get(new_request.supervisor_id).employee.full_name_arabic if new_request.supervisor_id else "غير محدد"}

📋 نوع الإجازة: {data['type']}
🏷️ التصنيف: {classification}
📅 التاريخ: {start_date}{f' إلى {end_date}' if data['type'] == 'multi-day' else ""}
{f"⏰ الوقت: من {new_request.start_time.strftime('%I:%M %p')} إلى {new_request.end_time.strftime('%I:%M %p')}" if data['type'] == 'hourly' else ""}
⏱️ المدة: {hours_requested:.2f} ساعة
📝 السبب: {data['note']}

🕒 وقت المعالجة: {datetime.now(pytz.timezone("Asia/Damascus")).strftime('%Y-%m-%d %I:%M %p')}
━━━━━━━━━━━━━━━━━━━━
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
    """
        group_chat_id = "-4847322310"
        send_telegram_message(group_chat_id, archive_message)
        db.session.commit()
        print("تم حفظ التغييرات في قاعدة البيانات")

        try:
            # تحويل النوع والتصنيف إلى العربية
            arabic_type = leave_type_arabic.get(new_request.type, new_request.type)
            arabic_classification = classification_arabic.get(new_request.classification, new_request.classification)

            # إعداد تفاصيل الإجازة حسب النوع
            if new_request.type == 'hourly':
                start_time_str = new_request.start_time.strftime('%I:%M %p') if new_request.start_time else "غير محدد"
                end_time_str = new_request.end_time.strftime('%I:%M %p') if new_request.end_time else "غير محدد"
                leave_details = f"""
📋 <b>نوع الإجازة:</b> {arabic_type}
🏷️ <b>التصنيف:</b> {arabic_classification}
📅 <b>التاريخ:</b> {new_request.start_date}
⏰ <b>وقت البدء:</b> {start_time_str}
⏰ <b>وقت الانتهاء:</b> {end_time_str}
⏱️ <b>المدة:</b> {new_request.hours_requested:.2f} ساعة
                """
            elif new_request.type == 'daily':
                leave_details = f"""
📋 <b>نوع الإجازة:</b> {arabic_type}
🏷️ <b>التصنيف:</b> {arabic_classification}
📅 <b>التاريخ:</b> {new_request.start_date}
⏱️ <b>المدة:</b> {new_request.hours_requested:.2f} ساعة
                """
            elif new_request.type == 'multi-day':
                leave_details = f"""
📋 <b>نوع الإجازة:</b> {arabic_type}
🏷️ <b>التصنيف:</b> {arabic_classification}
📅 <b>تاريخ البدء:</b> {new_request.start_date}
📅 <b>تاريخ الانتهاء:</b> {new_request.end_date}
⏱️ <b>المدة:</b> {new_request.hours_requested:.2f} ساعة
                """
            else:
                leave_details = f"""
📋 <b>نوع الإجازة:</b> {arabic_type}
🏷️ <b>التصنيف:</b> {arabic_classification}
📅 <b>التاريخ:</b> {new_request.start_date}
⏱️ <b>المدة:</b> {new_request.hours_requested:.2f} ساعة
                """

            # نص الإعلان (يتم تنفيذه لجميع أنواع الإجازات)
            announcement_message = f"""
📢 <b>إشعار إجازة موظف</b>
━━━━━━━━━━━━━━━━━━━━
👤 <b>الموظف:</b> {employee.full_name_arabic}
{leave_details}
🕒 <b>وقت الإعلان:</b> {datetime.now(pytz.timezone("Asia/Damascus")).strftime("%Y-%m-%d %I:%M %p")}
━━━━━━━━━━━━━━━━━━━━
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
            """

            # جلب موظفين القسم مع استثناء مقدم الطلب
            department_employees = Employee.query.filter_by(
                department_id=employee.department_id
            ).filter(
                Employee.telegram_chatid.isnot(None),  # تصحيح: استخدام None بدلاً من Null
                Employee.id != employee.id
            ).all()

            # إضافة المشرف للقائمة (لو عنده chatid)
            supervisor = Supervisor.query.get(new_request.supervisor_id)
            if supervisor:
                supervisor_employee = db.session.get(Employee, supervisor.supervisor_ID)
                if supervisor_employee and supervisor_employee.telegram_chatid and supervisor_employee.id != employee.id:
                    department_employees.append(supervisor_employee)

            # إرسال الإشعار لكل موظف
            for dept_employee in department_employees:
                try:
                    send_telegram_message(dept_employee.telegram_chatid, announcement_message)
                    print(f"تم إرسال إشعار إلى {dept_employee.full_name_arabic}")
                except Exception as e:
                    print(f"فشل إرسال الإشعار إلى {dept_employee.full_name_arabic}: {str(e)}")

        except Exception as e:
            print(f"❌ فشل إعلام الموظفين: {str(e)}")

        # طباعة أرصدة الإجازات بعد التحديث
        print("=== أرصدة الإجازات بعد التحديث ===")
        print(f"رصيد الإجازة العادية: {employee.regular_leave_remaining} ساعة")
        print(f"رصيد الإجازة المرضية: {employee.sick_leave_remaining} ساعة")
        print(f"رصيد الإجازة الخاصة: {employee.emergency_leave_remaining} ساعة")
        print(f"الإجازة العادية المستخدمة: {employee.regular_leave_used} ساعة")
        print(f"الإجازة المرضية المستخدمة: {employee.sick_leave_used} ساعة")
        print(f"الإجازة الخاصة المستخدمة: {employee.emergency_leave_used} ساعة")
        print("================================")

        print("=== انتهاء العملية بنجاح ===")
        
        # رسالة الرد النهائية
        if is_supervisor:
            message = "تم قبول طلب إجازتك تلقائيًا. " + (medical_message if classification == 'sick' else "")
        else:
            message = "تم إرسال طلب الإجازة بنجاح. " + (medical_message if classification == 'sick' else "")

        return jsonify({
            "success": True,
            "message": message,
            "request_id": new_request.id,
            "is_auto_approved": is_supervisor,
            "hours_requested": hours_requested
        }), 201

    except Exception as e:
        print(f"❌ حدث خطأ: {str(e)}")
        db.session.rollback()
        return jsonify({
            "success": False,
            "message": "حدث خطأ أثناء حفظ الطلب",
            "error": str(e)
        }), 500
@app.route('/api/compensation-leave-requests/<int:request_id>', methods=['PUT'])
def update_compensation_leave_request(request_id):
    # التحقق من وجود session
    if 'employee' not in session:
        return jsonify({"message": "غير مسموح - يجب تسجيل الدخول أولاً"}), 401
    
    try:
        employee_id = session['employee']['id']
        data = request.get_json()
        
        # البحث عن الطلب
        comp_request = CompensationLeaveRequest.query.filter_by(
            id=request_id,
            employee_id=employee_id
        ).first()
        
        if not comp_request:
            return jsonify({"message": "طلب التعويض غير موجود أو لا يتعلق بهذا الموظف"}), 404
        
        # التحقق من حالة الطلب (يجب أن يكون قيد الانتظار)
        if comp_request.status != 'pending':
            return jsonify({
                "message": "لا يمكن تعديل الطلب بعد الموافقة أو الرفض"
            }), 403
        
        # تحديث البيانات
        if 'date' in data:
            comp_request.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        
        # تحديث الأوقات وحساب الساعات
        if 'start_time' in data and 'end_time' in data:
            try:
                start_time = datetime.strptime(data['start_time'], '%H:%M').time()
                end_time = datetime.strptime(data['end_time'], '%H:%M').time()
                
                # حساب الفرق بين الأوقات
                start_datetime = datetime.combine(datetime.today(), start_time)
                end_datetime = datetime.combine(datetime.today(), end_time)
                
                # التحقق من الحالات المختلفة
                if start_time == end_time:
                    # إذا كان نفس الوقت، اعتبره 24 ساعة كاملة
                    end_datetime += timedelta(days=1)
                elif end_datetime <= start_datetime:
                    # وقت النهاية في اليوم التالي
                    end_datetime += timedelta(days=1)
                
                time_diff = end_datetime - start_datetime
                hours_requested = time_diff.total_seconds() / 3600
                
                if hours_requested <= 0:
                    return jsonify({"message": "وقت النهاية يجب أن يكون بعد وقت البداية"}), 400
                
                # التحقق من عدم تجاوز 24 ساعة
                if hours_requested > 24:
                    return jsonify({"message": "لا يمكن أن تتجاوز ساعات العمل 24 ساعة"}), 400
                
                comp_request.start_time = start_time
                comp_request.end_time = end_time
                comp_request.hours_requested = float(hours_requested)
                
            except ValueError:
                return jsonify({"message": "صيغة الوقت غير صحيحة"}), 400
        
        if 'note' in data:
            comp_request.note = data['note']
        
        # تحديث طابع الزمن للتعديل
        comp_request.timestamp = datetime.now(ZoneInfo("Asia/Damascus"))
        
        db.session.commit()
        
        return jsonify({
            "message": "تم تحديث طلب التعويض بنجاح",
            "request": {
                'id': comp_request.id,
                'date': comp_request.date.strftime('%Y-%m-%d'),
                'hours_requested': comp_request.hours_requested,
                'note': comp_request.note,
                'status': comp_request.status,
                'timestamp': comp_request.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'start_time': comp_request.start_time.strftime('%H:%M') if comp_request.start_time else None,
                'end_time': comp_request.end_time.strftime('%H:%M') if comp_request.end_time else None
            }
        }), 200
        
    except ValueError as e:
        return jsonify({
            "message": "بيانات غير صالحة",
            "error": str(e)
        }), 400
    except Exception as e:
        db.session.rollback()
        print(f"Error updating compensation leave request: {str(e)}")
        return jsonify({
            "message": "حدث خطأ أثناء تحديث الطلب",
            "error": str(e)
        }), 500
@app.route('/api/employees-list-self', methods=['GET'])
def get_employees_list_self():
    # التحقق من وجود جلسة نشطة
    if 'employee' not in session:
        return jsonify({
            'success': False,
            'message': 'غير مسموح - يجب تسجيل الدخول أولاً'
        }), 401
    
    try:
        employee_id = session['employee']['id']
        
        # جلب الموظف الحالي فقط
        current_employee = Employee.query.filter_by(id=employee_id).first()
        
        if not current_employee:
            return jsonify([]), 200
        
        # إرجاع بيانات الموظف الحالي في صورة قائمة
        employees_data = [
            {
                'id': current_employee.id,
                'name': current_employee.full_name_arabic,
                'employee_number': current_employee.employee_number
            }
        ]
        
        return jsonify(employees_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/api/current-employee', methods=['GET'])
def get_current_employee():
    if 'employee' not in session:
        return jsonify({'message': 'يرجى تسجيل الدخول'}), 401

    employee_id = session['employee']['id']
    employee = db.session.get(Employee, employee_id)
    if not employee:
        return jsonify({'message': 'الموظف غير موجود'}), 404

    # جلب الحقول المخصصة
    custom_fields = EmployeeCustomField.query.filter_by(employee_id=employee_id).all()
    custom_fields_data = [
        {'id': f.id, 'field_name': f.field_name, 'field_value': f.field_value}
        for f in custom_fields
    ]

    salary_component = SalaryComponent.query.filter_by(employee_id=employee_id).first()

    # بناء رابط الصورة
    if employee.profile_image and not employee.profile_image.startswith('http'):
        image_url = f"{request.host_url.rstrip('/')}/static/uploads/{employee.profile_image}"
    else:
        image_url = employee.profile_image

    department = db.session.get(Department, employee.department_id)

    employee_data = {
        'id': employee.id,
        'full_name_arabic': employee.full_name_arabic,
        'full_name_english': employee.full_name_english,
        'employee_number': employee.employee_number,
        'email': employee.email,
        'password': employee.password,
        'profile_image': image_url,
        'telegram_chatid': employee.telegram_chatid,
        'phone': employee.phone,
        'department_name': department.dep_name if department else None,
        'department_id': employee.department_id,
        'position': employee.position,
        'role': employee.role,
        'bank_account': employee.bank_account,
        'address': employee.address,
        'notes': employee.notes,
        'weekly_day_off': employee.weekly_day_off,
        'work_start_time': str(employee.work_start_time) if employee.work_start_time else None,
        'work_end_time': str(employee.work_end_time) if employee.work_end_time else None,
        'date_of_joining': str(employee.date_of_joining) if employee.date_of_joining else None,
        'is_leave': employee.is_leave,
        'is_vacation': employee.is_vacation,
        'is_weekly_day_off': employee.is_weekly_day_off,
        'regular_leave_hours': employee.regular_leave_hours,
        'sick_leave_hours': employee.sick_leave_hours,
        'emergency_leave_hours': employee.emergency_leave_hours,
        'custom_fields': custom_fields_data,
        'salary_components': None,
        'allowances': {},
        'deductions': {},
        # الحقول الجديدة المضافة
        'study_major': employee.study_major,
        'governorate': employee.governorate,
        'relative_phone': employee.relative_phone,
        'relative_relation': employee.relative_relation,
        'date_of_birth': str(employee.date_of_birth) if employee.date_of_birth else None,
        'national_id': employee.national_id,
        'job_level': employee.job_level,
        'promotion': employee.promotion,
        'career_stages': employee.career_stages,
        'employee_status': employee.employee_status,
        'work_location': employee.work_location,
        'work_nature': employee.work_nature,
        'marital_status': employee.marital_status,
        'nationality': employee.nationality,
        'trainings': employee.trainings,
        'external_privileges': employee.external_privileges,
        'special_leave_record': employee.special_leave_record,
        'drive_folder_link': employee.drive_folder_link
    }

    if salary_component:
        employee_data['salary_components'] = {
            'base_salary': salary_component.base_salary,
            'hour_salary': float(salary_component.hour_salary) if salary_component.hour_salary else None,
            'overtime_rate': salary_component.overtime_rate,
            'holiday_overtime_rate': salary_component.holiday_overtime_rate,
            'internet_allowance': salary_component.internet_allowance,
            'transport_allowance': salary_component.transport_allowance,
            'depreciation_allowance': salary_component.depreciation_allowance,
            'administrative_allowance': salary_component.administrative_allowance,
            'administrative_deduction': salary_component.administrative_deduction
        }

        employee_data['allowances'] = {
            'بدل انترنت': salary_component.internet_allowance,
            'بدل نقل': salary_component.transport_allowance,
        }
        employee_data['deductions'] = {
            'خصم إداري': salary_component.administrative_deduction
        }

    return jsonify(employee_data), 200

# Routes for Additional Attendance Records (Overtime Requests)
# Routes for Additional Attendance Records (Overtime Requests)
@app.route('/api/overtime-requests', methods=['GET'])
def get_all_overtime_requests():
    if 'employee' not in session:
        return jsonify({'success': False, 'message': 'يجب تسجيل الدخول أولاً'}), 401

    employee_id = session['employee']['id']
    overtime_requests = AdditionalAttendanceRecord.query.filter_by(employee_id=employee_id).all()

    requests_data = []
    for req in overtime_requests:
        requests_data.append({
            'id': req.id,
            'date': req.date.strftime('%Y-%m-%d'),
            'start_time': req.start_time.strftime('%H:%M') if req.start_time else None,
            'end_time': req.end_time.strftime('%H:%M') if req.end_time else None,
            'hours_requested': round(req.add_attendance_minutes / 60, 2),
            'note': req.notes,
            'status': req.status,
            'timestamp': req.date.strftime('%Y-%m-%d')
        })

    return jsonify({'success': True, 'requests': requests_data}), 200
@app.route('/api/overtime-requests', methods=['POST'])
def create_overtime_request():
    """إنشاء طلب دوام إضافي جديد"""
    try:
        # التحقق من وجود session للموظف
        if 'employee' not in session:
            return jsonify({
                'success': False,
                'message': 'يجب تسجيل الدخول أولاً'
            }), 401
            
        # جلب معرف الموظف من الـ session
        employee_id = session['employee']['id']
        employee = db.session.get(Employee, employee_id)
       
        if not employee:
            return jsonify({
                'success': False,
                'message': 'الموظف غير موجود'
            }), 404
            
        # التحقق من كون المستخدم مشرف من خلال جدول المشرفين
        supervisor_record = Supervisor.query.filter_by(supervisor_ID=employee_id).first()
        is_supervisor = supervisor_record is not None
        
        # جلب البيانات من الطلب
        data = request.get_json()
       
        # التحقق من وجود البيانات المطلوبة
        required_fields = ['date', 'start_time', 'end_time', 'note']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'message': f'الحقل {field} مطلوب'
                }), 400
                
        # تحويل التاريخ والوقت
        from datetime import datetime
        syria_tz = pytz.timezone("Asia/Damascus")
        request_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        end_time = datetime.strptime(data['end_time'], '%H:%M').time()
       
        # التحقق مما إذا كان التاريخ يوم عطلة
        is_holiday = False
        holiday_reason = ""

        # 1. التحقق من العطل الرسمية
        official_holiday = OfficialHoliday.query.filter_by(holiday_date=request_date).first()
        if official_holiday:
            is_holiday = True
            holiday_reason = f"عطلة رسمية: {official_holiday.description}"
        
        # 2. التحقق من العطلة الأسبوعية للموظف
        if not is_holiday:
            # الحصول على يوم الأسبوع للتاريخ المطلوب (باللغة الإنجليزية)
            weekday_name = request_date.strftime('%A')  # Monday, Tuesday, etc.
            
            # التحقق إذا كان هذا اليوم هو يوم العطلة الأسبوعية للموظف
            if employee.weekly_day_off and employee.weekly_day_off.lower() == weekday_name.lower():
                is_holiday = True
                holiday_reason = f"عطلة أسبوعية: {employee.weekly_day_off}"
       
        # حساب الفرق بالدقائق
        start_datetime = datetime.combine(request_date, start_time)
        end_datetime = datetime.combine(request_date, end_time)
       
        # إذا كان وقت الانتهاء قبل وقت البداية، فهذا يعني أن العمل امتد لليوم التالي
        if end_datetime <= start_datetime:
            end_datetime = end_datetime.replace(day=end_datetime.day + 1)
       
        time_diff = end_datetime - start_datetime
        total_minutes = int(time_diff.total_seconds() / 60)

        # حساب الساعات المطلوبة
        hours_requested = total_minutes / 60.0
        
        # التحقق من عدم وجود طلب آخر لنفس التاريخ
        existing_request = AdditionalAttendanceRecord.query.filter_by(
            employee_id=employee_id,
            date=request_date
        ).first()
       
        if existing_request:
            return jsonify({
                'success': False,
                'message': 'يوجد طلب دوام إضافي لهذا التاريخ مسبقاً'
            }), 400
            
        # تحديد حالة الطلب بناءً على نوع المستخدم
        if is_supervisor:
            # إذا كان المرسل مشرف، يتم قبول الطلب تلقائياً
            status = 'approved'
        else:
            # إذا كان موظف عادي، يبقى الطلب قيد الانتظار
            status = 'pending'
            
        # إنشاء طلب الدوام الإضافي الجديد
        new_request = AdditionalAttendanceRecord(
            date=request_date,
            employee_id=employee_id,
            name=employee.full_name_english,
            arname=employee.full_name_arabic,
            role=employee.role,
            is_holiday=is_holiday,
            start_time=start_time,
            end_time=end_time,
            add_attendance_minutes=total_minutes,
            status=status,
            notes=data['note']
        )
        
        # حفظ الطلب في قاعدة البيانات
        db.session.add(new_request)
        db.session.commit()

        # إرسال إشعارات للمشرفين إذا كان الموظف غير مشرف
        if not is_supervisor:
            department_supervisors = Supervisor.query.filter_by(dep_id=employee.department_id).all()
            if department_supervisors:
                for supervisor in department_supervisors:
                    notification = Notification(
                        recipient_id=supervisor.supervisor_ID,
                        message=f"طلب دوام إضافي جديد من الموظف {employee.full_name_arabic}"
                    )
                    db.session.add(notification)

                    # إرسال إشعار تلغرام
                    supervisor_employee = db.session.get(Employee, supervisor.supervisor_ID)
                    if supervisor_employee and supervisor_employee.telegram_chatid:
                        # إضافة معلومات العطلة إذا كانت موجودة
                        holiday_info = f"\n🏖️ نوع اليوم: {holiday_reason}" if is_holiday else ""
                        
                        telegram_message = f"""
🔔 <b>طلب دوام إضافي جديد</b>
━━━━━━━━━━━━━━━━━━━━
👤 الموظف: {employee.full_name_arabic}
📅 التاريخ: {request_date.strftime('%Y-%m-%d')}
⏰ الوقت: من {datetime.strptime(data['start_time'], '%H:%M').strftime('%I:%M %p').replace('AM','ص').replace('PM','م')} 
     ⬅️ إلى {datetime.strptime(data['end_time'], '%H:%M').strftime('%I:%M %p').replace('AM','ص').replace('PM','م')}
⏳ المدة: {hours_requested:.2f} ساعة
📝 الملاحظة: {data['note']}
{holiday_info}
━━━━━━━━━━━━━━━━━━━━
🕒 وقت الطلب: {datetime.now(syria_tz).strftime("%Y-%m-%d %I:%M %p")}
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
                        """
                        send_telegram_message(supervisor_employee.telegram_chatid, telegram_message)
                db.session.commit()
        
        # إرسال رسالة الأرشيف للموافقة التلقائية (إذا كان مشرفاً)
        if is_supervisor:
            # حساب المدة بالساعات والدقائق
            hours = int(total_minutes // 60)
            minutes = int(total_minutes % 60)
            duration_str = f"{hours} ساعة و {minutes} دقيقة" if minutes > 0 else f"{hours} ساعة"
            
            # إضافة معلومات العطلة إذا كانت موجودة
            holiday_info = f"\n🏖️ نوع اليوم: {holiday_reason}" if is_holiday else ""
            
            # إعداد رسالة الأرشيف
            archive_message = f"""
📋 طلب معتمد - أرشيف
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📄 نوع الطلب: عمل إضافي
👤 الموظف: {employee.full_name_arabic}
🏢 القسم: {employee.department.dep_name if employee.department else "غير محدد"}

📅 التاريخ: {request_date}
⏰ الوقت: من {start_time.strftime('%I:%M %p').replace('AM', 'ص').replace('PM', 'م')} إلى {end_time.strftime('%I:%M %p').replace('AM', 'ص').replace('PM', 'م')}
⏱️ المدة: {duration_str}
📝 السبب: {data['note']}
{holiday_info}
                
🕒 وقت المعالجة: {datetime.now(syria_tz).strftime('%Y-%m-%d %I:%M %p')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
            """
            group_chat_id = "-4847322310"  # تأكد من أن هذا هو معرف المجموعة الصحيح
            send_telegram_message(group_chat_id, archive_message)
            
            # إرسال رسالة تأكيد للموظف (المشرف) عبر التلغرام
            if employee.telegram_chatid:
                # إضافة معلومات العطلة إذا كانت موجودة
                holiday_info = f"\n🏖️ نوع اليوم: {holiday_reason}" if is_holiday else ""
                
                confirmation_message = f"""
✅ <b>تم قبول طلب دوامك الإضافي تلقائياً</b>

📅 التاريخ: {request_date}
⏰ الوقت: من {start_time.strftime('%I:%M %p').replace('AM', 'ص').replace('PM', 'م')} إلى {end_time.strftime('%I:%M %p').replace('AM', 'ص').replace('PM', 'م')}
⏱️ المدة: {duration_str}
📝 الملاحظة: {data['note']}
{holiday_info}

🕒 وقت المعالجة: {datetime.now(syria_tz).strftime('%Y-%m-%d %I:%M %p')}
━━━━━━━━━━━━━━━━━━━━
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
                """
                send_telegram_message(employee.telegram_chatid, confirmation_message)
        
        # رسالة مختلفة حسب نوع المستخدم
        if is_supervisor:
            message = "تم إنشاء وقبول طلب الدوام الإضافي تلقائياً"
        else:
            message = "تم إرسال طلب الدوام الإضافي بنجاح"
            
        # إضافة معلومات حول نوع اليوم إذا كان عطلة
        if is_holiday:
            message += f" (يوم {holiday_reason})"
        
        return jsonify({
            'success': True,
            'message': message,
            'request_id': new_request.id,
            'hours_requested': round(hours_requested, 2),
            'is_auto_approved': is_supervisor,
            'is_holiday': is_holiday,
            'holiday_reason': holiday_reason if is_holiday else ""
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'حدث خطأ أثناء إنشاء الطلب: {str(e)}'
        }), 500
@app.route('/api/overtime-requests/<int:request_id>', methods=['PUT'])
def update_overtime_request(request_id):
    """تعديل طلب دوام إضافي موجود"""
    try:
        # التحقق من وجود session للموظف
        if 'employee' not in session:
            return jsonify({
                'success': False,
                'message': 'يجب تسجيل الدخول أولاً'
            }), 401

        # جلب معرف الموظف من الـ session
        employee_id = session['employee']['id']
        employee = db.session.get(Employee, employee_id)
        
        if not employee:
            return jsonify({
                'success': False,
                'message': 'الموظف غير موجود'
            }), 404
        
        # البحث عن الطلب
        overtime_request = AdditionalAttendanceRecord.query.filter_by(
            id=request_id,
            employee_id=employee_id
        ).first()
        
        if not overtime_request:
            return jsonify({
                'success': False,
                'message': 'الطلب غير موجود'
            }), 404

        # التحقق من أن الطلب قيد الانتظار (يمكن تعديله فقط إذا كان pending)
        if overtime_request.status != 'pending':
            return jsonify({
                'success': False,
                'message': 'لا يمكن تعديل طلب تم الرد عليه'
            }), 400

        # جلب البيانات من الطلب
        data = request.get_json()
        
        # التحقق من وجود البيانات المطلوبة
        required_fields = ['date', 'start_time', 'end_time', 'note']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({
                    'success': False,
                    'message': f'الحقل {field} مطلوب'
                }), 400

        # تحويل التاريخ والوقت
        from datetime import datetime
        
        request_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        
        # التحقق مما إذا كان التاريخ يوم عطلة
        is_holiday = False
        holiday_reason = ""

        # 1. التحقق من العطل الرسمية
        official_holiday = OfficialHoliday.query.filter_by(holiday_date=request_date).first()
        if official_holiday:
            is_holiday = True
            holiday_reason = f"عطلة رسمية: {official_holiday.description}"
        
        # 2. التحقق من العطلة الأسبوعية للموظف
        if not is_holiday:
            # الحصول على يوم الأسبوع للتاريخ المطلوب (باللغة الإنجليزية)
            weekday_name = request_date.strftime('%A')  # Monday, Tuesday, etc.
            
            # التحقق إذا كان هذا اليوم هو يوم العطلة الأسبوعية للموظف
            if employee.weekly_day_off and employee.weekly_day_off.lower() == weekday_name.lower():
                is_holiday = True
                holiday_reason = f"عطلة أسبوعية: {employee.weekly_day_off}"
        
        # حساب الدقائق
        start_datetime = datetime.combine(request_date, start_time)
        end_datetime = datetime.combine(request_date, end_time)
        
        # إذا كان وقت الانتهاء قبل وقت البداية، فهذا يعني أن العمل امتد لليوم التالي
        if end_datetime <= start_datetime:
            end_datetime = end_datetime.replace(day=end_datetime.day + 1)
        
        time_diff = end_datetime - start_datetime
        total_minutes = int(time_diff.total_seconds() / 60)

        # حساب الساعات المطلوبة
        hours_requested = total_minutes / 60.0

        # التحقق من عدم وجود طلب آخر لنفس التاريخ (ما عدا الطلب الحالي)
        existing_request = AdditionalAttendanceRecord.query.filter(
            AdditionalAttendanceRecord.employee_id == employee_id,
            AdditionalAttendanceRecord.date == request_date,
            AdditionalAttendanceRecord.id != request_id
        ).first()
        
        if existing_request:
            return jsonify({
                'success': False,
                'message': 'يوجد طلب دوام إضافي آخر لهذا التاريخ'
            }), 400

        # تحديث بيانات الطلب
        overtime_request.date = request_date
        overtime_request.start_time = start_time
        overtime_request.end_time = end_time
        overtime_request.add_attendance_minutes = total_minutes
        overtime_request.notes = data['note']
        overtime_request.is_holiday = is_holiday  # تحديث حالة العطلة

        # حفظ التغييرات
        db.session.commit()

        # إرسال رسالة تأكيد للموظف عبر التلغرام إذا كان لديه معرف تلغرام
        if employee.telegram_chatid:
            # حساب المدة بالساعات والدقائق
            hours = int(total_minutes // 60)
            minutes = int(total_minutes % 60)
            duration_str = f"{hours} ساعة و {minutes} دقيقة" if minutes > 0 else f"{hours} ساعة"
            
            # إضافة معلومات العطلة إذا كانت موجودة
            holiday_info = f"\n🏖️ نوع اليوم: {holiday_reason}" if is_holiday else ""
            
            confirmation_message = f"""
✏️ <b>تم تعديل طلب الدوام الإضافي بنجاح</b>

📅 التاريخ: {request_date}
⏰ الوقت: من {start_time.strftime('%I:%M %p').replace('AM', 'ص').replace('PM', 'م')} إلى {end_time.strftime('%I:%M %p').replace('AM', 'ص').replace('PM', 'م')}
⏱️ المدة: {duration_str}
📝 الملاحظة: {data['note']}
{holiday_info}

🕒 وقت التعديل: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}
━━━━━━━━━━━━━━━━━━━━
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
            """
            send_telegram_message(employee.telegram_chatid, confirmation_message)

        return jsonify({
            'success': True,
            'message': 'تم تحديث طلب الدوام الإضافي بنجاح',
            'is_holiday': is_holiday,
            'holiday_reason': holiday_reason if is_holiday else "",
            'hours_requested': round(hours_requested, 2)
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'حدث خطأ أثناء تحديث الطلب: {str(e)}'
        }), 500

@app.route('/api/overtime-requests/<int:request_id>', methods=['DELETE'])
def delete_overtime_request(request_id):
    """حذف طلب دوام إضافي"""
    try:
        # التحقق من وجود session للموظف
        if 'employee' not in session:
            return jsonify({
                'success': False,
                'message': 'يجب تسجيل الدخول أولاً'
            }), 401

        # جلب معرف الموظف من الـ session
        employee_id = session['employee']['id']
        
        # البحث عن الطلب
        overtime_request = AdditionalAttendanceRecord.query.filter_by(
            id=request_id,
            employee_id=employee_id
        ).first()
        
        if not overtime_request:
            return jsonify({
                'success': False,
                'message': 'الطلب غير موجود'
            }), 404

        # التحقق من أن الطلب قيد الانتظار (يمكن حذفه فقط إذا كان pending)
        if overtime_request.status != 'pending':
            return jsonify({
                'success': False,
                'message': 'لا يمكن حذف طلب تم الرد عليه'
            }), 400

        # حذف الطلب
        db.session.delete(overtime_request)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'تم حذف طلب الدوام الإضافي بنجاح'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'حدث خطأ أثناء حذف الطلب: {str(e)}'
        }), 500


@app.route('/api/overtime-requests/<int:request_id>/details', methods=['GET'])
def get_overtime_request_details(request_id):
    """جلب تفاصيل طلب دوام إضافي محدد"""
    try:
        # التحقق من وجود session للموظف
        if 'employee' not in session:
            return jsonify({
                'success': False,
                'message': 'يجب تسجيل الدخول أولاً'
            }), 401

        # جلب معرف الموظف من الـ session
        employee_id = session['employee']['id']
        
        # البحث عن الطلب
        overtime_request = AdditionalAttendanceRecord.query.filter_by(
            id=request_id,
            employee_id=employee_id
        ).first()
        
        if not overtime_request:
            return jsonify({
                'success': False,
                'message': 'الطلب غير موجود'
            }), 404

        # إرجاع تفاصيل الطلب
        request_data = {
            'id': overtime_request.id,
            'date': overtime_request.date.strftime('%Y-%m-%d'),
            'start_time': overtime_request.start_time.strftime('%H:%M') if overtime_request.start_time else None,
            'end_time': overtime_request.end_time.strftime('%H:%M') if overtime_request.end_time else None,
            'hours_requested': round(overtime_request.add_attendance_minutes / 60, 2),
            'note': overtime_request.notes,
            'status': overtime_request.status,
            'employee_name': overtime_request.arname,
            'employee_role': overtime_request.role,
            'is_holiday': overtime_request.is_holiday,
            'timestamp': overtime_request.date.strftime('%Y-%m-%d')
        }

        return jsonify({
            'success': True,
            'request': request_data
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'حدث خطأ أثناء جلب تفاصيل الطلب: {str(e)}'
        }), 500


# Route إضافي لجلب إحصائيات الدوام الإضافي
@app.route('/api/overtime-requests/statistics', methods=['GET'])
def get_overtime_statistics():
    """جلب إحصائيات طلبات الدوام الإضافي للموظف"""
    try:
        # التحقق من وجود session للموظف
        if 'employee' not in session:
            return jsonify({
                'success': False,
                'message': 'يجب تسجيل الدخول أولاً'
            }), 401

        # جلب معرف الموظف من الـ session
        employee_id = session['employee']['id']
        
        # حساب الإحصائيات
        total_requests = AdditionalAttendanceRecord.query.filter_by(employee_id=employee_id).count()
        approved_requests = AdditionalAttendanceRecord.query.filter_by(employee_id=employee_id, status='approved').count()
        pending_requests = AdditionalAttendanceRecord.query.filter_by(employee_id=employee_id, status='pending').count()
        rejected_requests = AdditionalAttendanceRecord.query.filter_by(employee_id=employee_id, status='rejected').count()
        
        # حساب إجمالي الساعات المعتمدة
        approved_records = AdditionalAttendanceRecord.query.filter_by(
            employee_id=employee_id, 
            status='approved'
        ).all()
        
        total_approved_hours = sum(record.add_attendance_minutes / 60 for record in approved_records)

        return jsonify({
            'success': True,
            'statistics': {
                'total_requests': total_requests,
                'approved_requests': approved_requests,
                'pending_requests': pending_requests,
                'rejected_requests': rejected_requests,
                'total_approved_hours': round(total_approved_hours, 2)
            }
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'حدث خطأ أثناء جلب الإحصائيات: {str(e)}'
        }), 500
@app.route('/api/employee-leave-summary', methods=['GET'])
def get_employee_leave_summary():
    try:
        # التحقق من وجود session للموظف
        if 'employee' not in session:
            return jsonify({
                'success': False,
                'message': 'يجب تسجيل الدخول أولاً'
            }), 401

        # جلب معرف الموظف من الـ session
        employee_id = session['employee']['id']
        
        # جلب بيانات الموظف
        employee = db.session.get(Employee, employee_id)
        if not employee:
            return jsonify({
                'success': False,
                'message': 'الموظف غير موجود'
            }), 404

        # استخدام الأعمدة الجديدة مباشرة
        return jsonify({
            'success': True,
            'remaining': {
                'normal': employee.regular_leave_remaining,
                'sick': employee.sick_leave_remaining,
                'emergency': employee.emergency_leave_remaining
            },
            'used': {
                'normal': employee.regular_leave_used,
                'sick': employee.sick_leave_used,
                'emergency': employee.emergency_leave_used
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في الخادم: {str(e)}'
        }), 500
@app.route('/api/leave-balance', methods=['GET'])
def get_employee_leave_balance():
    try:
        # التحقق من وجود session للموظف
        if 'employee' not in session:
            return jsonify({
                'success': False,
                'message': 'يجب تسجيل الدخول أولاً'
            }), 401

        # جلب معرف الموظف من الـ session
        employee_id = session['employee']['id']
        
        # جلب بيانات الموظف
        employee = db.session.get(Employee, employee_id)
        if not employee:
            return jsonify({
                'success': False,
                'message': 'الموظف غير موجود'
            }), 404

        # حساب عدد ساعات العمل اليومية للموظف
        work_start = employee.work_start_time
        work_end = employee.work_end_time
        
        # تحويل الوقت إلى دقائق لحساب الفرق
        start_minutes = work_start.hour * 60 + work_start.minute
        end_minutes = work_end.hour * 60 + work_end.minute
        
        # حساب عدد ساعات العمل اليومية
        daily_work_hours = (end_minutes - start_minutes) / 60

        # استخدام الأعمدة الجديدة مباشرة بدلاً من الحساب اليدوي
        return jsonify({
            'success': True,
            'employee_id': employee_id,
            'employee_name': employee.full_name_arabic,
            'daily_work_hours': daily_work_hours,
            'balance': {
                'regular': {
                    'total': employee.regular_leave_total,
                    'used': employee.regular_leave_used,
                    'remaining': employee.regular_leave_remaining
                },
                'sick': {
                    'total': employee.sick_leave_total,
                    'used': employee.sick_leave_used,
                    'remaining': employee.sick_leave_remaining
                },
                'emergency': {
                    'total': employee.emergency_leave_total,
                    'used': employee.emergency_leave_used,
                    'remaining': employee.emergency_leave_remaining
                }
            }
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في الخادم: {str(e)}'
        }), 500
#SuperVisor
@app.route('/api/supervisor/dashboard-data', methods=['GET'])
def get_supervisor_dashboard_data():
    try:
        # التحقق من صلاحيات المشرف
        if 'employee' not in session or session['employee'].get('role') != 'مشرف':
            return jsonify({"error": "غير مصرح لك بالوصول"}), 403

        # الحصول على بيانات المشرف الحالي
        supervisor_id = session['employee']['id']
        supervisor = db.session.get(Employee, supervisor_id)
        
        if not supervisor or not supervisor.department_id:
            return jsonify({"error": "بيانات المشرف غير صحيحة"}), 404
        
        # استخدام قسم المشرف كفلتر
        supervisor_department_id = supervisor.department_id
        department_name = supervisor.department.dep_name

        # تاريخ ووقت ثابت للاختبار (يمكن تغييره للاستخدام الحقيقي)
        today = date.today()
        test_time = datetime.now().time()
        current_time = test_time
        print(f"التاريخ: {today}, الوقت الحالي: {current_time}")

        # جلب جميع الموظفين في قسم المشرف فقط
        all_employees = db.session.query(Employee, Department)\
            .join(Department, Employee.department_id == Department.dep_id)\
            .filter(
                Employee.department_id == supervisor_department_id,
                Employee.role != 'ادمن',
                Employee.id != supervisor_id
            )\
            .all()
        
        total_all_employees = len(all_employees)
        
        # جلب سجلات الحضور لموظفي القسم فقط
        department_employee_ids = [emp.id for emp, _ in all_employees]
        today_attendance = db.session.query(AttendanceRecord)\
            .filter(
                AttendanceRecord.work_date == today,
                AttendanceRecord.employee_id.in_(department_employee_ids)
            )\
            .order_by(AttendanceRecord.check_in_time.desc())\
            .all()

        # بناء قاموس لآخر سجل لكل موظف
        attendance_dict = {}
        for record in today_attendance:
            emp_id = int(record.employee_id)
            if emp_id not in attendance_dict:
                attendance_dict[emp_id] = record

        # تصنيف الموظفين
        attendances = []
        delays = []
        absences = []

        for employee, department in all_employees:
            employee_data = {
                'name': employee.full_name_arabic,
                'department': department.dep_name,
                'employee_number': employee.employee_number,
                'expected_time': employee.work_start_time.strftime('%H:%M')
            }

            # التحقق من الإجازة المبررة
            is_excused = (
                employee.is_leave == 'on' or
                employee.is_vacation == 'on' or
                employee.is_weekly_day_off == 'on'
            )

            is_leave_excused = (employee.is_leave == 'on')

            # معالجة آخر سجل للموظف
            if employee.id in attendance_dict:
                last_record = attendance_dict[employee.id]
                
                if last_record.check_in_time:
                    last_check_in_time = last_record.check_in_time.time()
                    last_check_out_time = last_record.check_out_time.time() if last_record.check_out_time else None
                    
                    employee_data['check_in_time'] = last_check_in_time.strftime('%I:%M %p')
                    
                    # حساب التأخير
                    work_start_minutes = time_to_minutes(employee.work_start_time)
                    work_end_minutes = time_to_minutes(employee.work_end_time)
                    checkin_minutes = time_to_minutes(last_check_in_time)
                    current_minutes = time_to_minutes(current_time)
                    
                    delay_minutes = checkin_minutes - work_start_minutes
                    is_delayed = delay_minutes > 15 and checkin_minutes <= work_end_minutes
                    
                    # هل آخر دخول ضمن أوقات الدوام؟
                    is_checkin_during_work = work_start_minutes <= checkin_minutes <= work_end_minutes
                    
                    # معالجة الحالات
                    if last_check_out_time:
                        employee_data['check_out_time'] = last_check_out_time.strftime('%I:%M %p')
                        checkout_minutes = time_to_minutes(last_check_out_time)
                        
                        # منطقة المسامحة (5 دقائق قبل انتهاء الدوام)
                        grace_period_start = work_end_minutes - 5
                        is_checkout_in_grace_or_after = checkout_minutes >= grace_period_start
                        
                        if checkout_minutes < grace_period_start:
                            # خروج مبكر
                            if is_leave_excused:
                                employee_data['absence_type'] = 'مبرر'
                            else:
                                employee_data['absence_type'] = 'غير مبرر'
                            
                            if is_delayed:
                                employee_data['delay_minutes'] = delay_minutes
                            
                            early_departure = work_end_minutes - checkout_minutes
                            employee_data['early_departure_minutes'] = early_departure
                            absences.append(employee_data)
                        elif is_checkout_in_grace_or_after:
                            if checkout_minutes <= work_end_minutes + 60:
                                employee_data['absence_type'] = 'مبرر'
                                if is_delayed:
                                    employee_data['delay_minutes'] = delay_minutes
                                absences.append(employee_data)
                            else:
                                if is_delayed:
                                    employee_data['delay_minutes'] = delay_minutes
                                    delays.append(employee_data)
                                else:
                                    attendances.append(employee_data)
                    else:
                        # لا يوجد تسجيل خروج
                        if current_minutes > work_end_minutes:
                            if is_delayed:
                                employee_data['delay_minutes'] = delay_minutes
                                delays.append(employee_data)
                            else:
                                attendances.append(employee_data)
                        else:
                            if is_checkin_during_work:
                                if is_delayed:
                                    employee_data['delay_minutes'] = delay_minutes
                                    delays.append(employee_data)
                                else:
                                    attendances.append(employee_data)
                            else:
                                attendances.append(employee_data)
                else:
                    # لا يوجد تسجيل دخول في آخر سجل
                    employee_data['absence_type'] = 'مبرر' if is_excused else 'غير مبرر'
                    absences.append(employee_data)
            else:
                # لا يوجد أي سجل حضور اليوم
                current_minutes = time_to_minutes(current_time)
                work_start_minutes = time_to_minutes(employee.work_start_time)
                
                if current_minutes > work_start_minutes + 30:
                    employee_data['absence_type'] = 'مبرر' if is_excused else 'غير مبرر'
                    absences.append(employee_data)
                else:
                    if is_excused:
                        employee_data['absence_type'] = 'مبرر'
                        absences.append(employee_data)

        # الإحصائيات النهائية
        attendance_count = len(attendances)
        delay_count = len(delays)
        absence_count = len(absences)

        return jsonify({
            'attendances': {
                'data': attendances,
                'stats': f'{attendance_count} out of {total_all_employees}',
                'title': 'الحضور اليوم'
            },
            'delays': {
                'data': delays,
                'stats': f'{delay_count} out of {total_all_employees}',
                'title': 'التأخيرات اليوم'
            },
            'absences': {
                'data': absences,
                'stats': f'{absence_count} out of {total_all_employees}',
                'title': 'الغيابات اليوم'
            },
            'summary': {
                'department': department_name,
                'total': total_all_employees,
                'present': attendance_count + delay_count,
                'on_time': attendance_count,
                'delayed': delay_count,
                'absent': absence_count,
                'date': today.strftime('%Y-%m-%d')
            }
        }), 200

    except Exception as e:
        print("خطأ في get_supervisor_dashboard_data:", e)
        traceback.print_exc()
        return jsonify({"error": "حدث خطأ في استرجاع البيانات"}), 500
@app.route('/api/sp-leave-requests', methods=['GET'])
def get_supervisor_leave_requests():
    if 'employee' not in session:
        return jsonify({"message": "يرجى تسجيل الدخول"}), 401
   
    supervisor_id = session['employee']['id']
    supervisor = db.session.get(Employee, supervisor_id)
   
    if not supervisor or supervisor.role != 'مشرف':
        return jsonify({"message": "غير مصرح بالوصول"}), 403
   
    # جلب طلبات الإجازة للقسم التابع للمشرف مع أرصدة الموظفين
    leave_requests = db.session.query(
        LeaveRequest.id,
        Employee.full_name_arabic.label('employee_name'),
        Employee.regular_leave_remaining,
        Employee.sick_leave_remaining,
        Employee.emergency_leave_remaining,
        LeaveRequest.start_date,
        LeaveRequest.end_date,
        LeaveRequest.hours_requested,
        LeaveRequest.status,
        LeaveRequest.timestamp,
        LeaveRequest.type,
        LeaveRequest.classification,
        LeaveRequest.start_time,
        LeaveRequest.end_time,
        LeaveRequest.note
    ).join(Employee, Employee.id == LeaveRequest.employee_id)\
     .filter(
        LeaveRequest.supervisor_id == supervisor_id,
        LeaveRequest.status == 'pending'
     ).all()
   
    result = []
    for r in leave_requests:
        request_data = {
            'id': r.id,
            'employee_name': r.employee_name,
            'start_date': r.start_date.strftime('%Y-%m-%d'),
            'hours_requested': r.hours_requested,
            'status': r.status,
            'timestamp': r.timestamp.strftime('%Y-%m-%d %H:%M'),
            'leave_type': r.type,
            'category': r.classification,
            'note': r.note or 'لا يوجد سبب محدد',
            'remaining_balance': {
                'regular': r.regular_leave_remaining,
                'sick': r.sick_leave_remaining,
                'emergency': r.emergency_leave_remaining
            }
        }
        
        # إضافة end_date وأوقات البداية والنهاية حسب نوع الإجازة
        if r.type == 'hourly':
            request_data['start_time'] = r.start_time.strftime('%H:%M') if r.start_time else None
            request_data['end_time'] = r.end_time.strftime('%H:%M') if r.end_time else None
        elif r.type == 'daily':
            request_data['end_date'] = r.end_date.strftime('%Y-%m-%d') if r.end_date else r.start_date.strftime('%Y-%m-%d')
        elif r.type == 'multi-day':
            request_data['end_date'] = r.end_date.strftime('%Y-%m-%d') if r.end_date else None
        
        result.append(request_data)
   
    return jsonify({"requests": result}), 200
@app.route('/api/sp-overtime-requests', methods=['GET'])
def get_supervisor_overtime_requests():
    if 'employee' not in session:
        return jsonify({"message": "يرجى تسجيل الدخول"}), 401
    
    supervisor_id = session['employee']['id']
    supervisor = db.session.get(Employee, supervisor_id)
    
    if not supervisor or supervisor.role != 'مشرف':
        return jsonify({"message": "غير مصرح بالوصول"}), 403
    
    # جلب طلبات العمل الإضافي للقسم مع حقول الوقت
    overtime_requests = db.session.query(
        AdditionalAttendanceRecord.id,
        Employee.full_name_arabic.label('employee_name'),
        AdditionalAttendanceRecord.date,
        AdditionalAttendanceRecord.add_attendance_minutes,
        AdditionalAttendanceRecord.status,
        AdditionalAttendanceRecord.start_time,  # أضفنا
        AdditionalAttendanceRecord.end_time,    # أضفنا
        AdditionalAttendanceRecord.notes
    ).join(Employee, Employee.id == AdditionalAttendanceRecord.employee_id)\
     .filter(
        Employee.department_id == supervisor.department_id,
        AdditionalAttendanceRecord.status == 'pending'
     ).all()
    
    # تحويل الدقائق إلى ساعات وإضافة الوقت
    result = [{
        'id': r.id,
        'employee_name': r.employee_name,
        'date': r.date.strftime('%Y-%m-%d'),
        'hours': round(r.add_attendance_minutes / 60, 2),
        'status': r.status,
        'start_time': r.start_time.strftime('%H:%M') if r.start_time else None,  # تحويل الوقت إلى سلسلة
        'end_time': r.end_time.strftime('%H:%M') if r.end_time else None,
        'notes': r.notes
    } for r in overtime_requests]
    
    return jsonify({"requests": result}), 200
@app.route('/api/sp-compensation-leave-requests', methods=['GET'])
def get_supervisor_compensation_requests():
    if 'employee' not in session:
        return jsonify({"message": "يرجى تسجيل الدخول"}), 401
    
    supervisor_id = session['employee']['id']
    supervisor = db.session.get(Employee, supervisor_id)
    
    if not supervisor or supervisor.role != 'مشرف':
        return jsonify({"message": "غير مصرح بالوصول"}), 403
    
    # جلب طلبات التعويض للقسم
    comp_requests = db.session.query(
        CompensationLeaveRequest.id,
        Employee.full_name_arabic.label('employee_name'),
        CompensationLeaveRequest.date,
        CompensationLeaveRequest.hours_requested,
        CompensationLeaveRequest.status,
        CompensationLeaveRequest.timestamp,
        CompensationLeaveRequest.start_time,
        CompensationLeaveRequest.end_time,
        CompensationLeaveRequest.note
    ).join(Employee, Employee.id == CompensationLeaveRequest.employee_id)\
     .filter(
        CompensationLeaveRequest.supervisor_id == supervisor_id,
        CompensationLeaveRequest.status == 'pending'
     ).all()
    
    result = [{
        'id': r.id,
        'employee_name': r.employee_name,
        'date': r.date.strftime('%Y-%m-%d'),
        'hours': r.hours_requested,
        'status': r.status,
        'timestamp': r.timestamp.strftime('%Y-%m-%d %H:%M'),
        'start_time': r.start_time.strftime('%H:%M') if r.start_time else None,
        'end_time': r.end_time.strftime('%H:%M') if r.end_time else None,
        'note': r.note
    } for r in comp_requests]
    
    return jsonify({"requests": result}), 200
@app.route('/api/sp-delay-requests', methods=['GET'])
def get_supervisor_delay_requests():
    if 'employee' not in session:
        return jsonify({"message": "يرجى تسجيل الدخول"}), 401
    
    supervisor_id = session['employee']['id']
    supervisor = db.session.get(Employee, supervisor_id)
    
    if not supervisor or supervisor.role != 'مشرف':
        return jsonify({"message": "غير مصرح بالوصول"}), 403
    
    # جلب طلبات التأخير المخصصة لهذا المشرف
    delay_requests = db.session.query(
        WorkDelayArchive.id,
        Employee.full_name_arabic.label('employee_name'),
        WorkDelayArchive.date,
        WorkDelayArchive.minutes_delayed,
        WorkDelayArchive.status,
        WorkDelayArchive.timestamp,
        WorkDelayArchive.delay_note
    ).join(Employee, Employee.id == WorkDelayArchive.employee_id) \
     .join(Supervisor, Supervisor.supervisor_ID == WorkDelayArchive.supervisor_id) \
     .filter(
        WorkDelayArchive.supervisor_id == supervisor_id,
        WorkDelayArchive.status == 'pending'
     ).all()
    
    # Debug output
    print(f"Found {len(delay_requests)} delay requests for supervisor {supervisor_id}")
    
    result = [{
        'id': r.id,
        'employee_name': r.employee_name,
        'date': r.date.strftime('%Y-%m-%d'),
        'minutes_delayed': r.minutes_delayed,
        'status': r.status,
        'timestamp': r.timestamp.strftime('%Y-%m-%d %H:%M') if r.timestamp else None,
        'justification_note': r.delay_note
    } for r in delay_requests]
    
    return jsonify({"requests": result}), 200
@app.route('/api/sp-2-leave-requests', methods=['GET'])
def get_supervisor_2_leave_requests():
    if 'employee' not in session:
        return jsonify({"message": "يرجى تسجيل الدخول"}), 401
   
    supervisor_id = session['employee']['id']
    supervisor = db.session.get(Employee, supervisor_id)
   
    if not supervisor or supervisor.role != 'مشرف':
        return jsonify({"message": "غير مصرح بالوصول"}), 403
   
    # جلب طلبات الإجازة للقسم التابع للمشرف
    leave_requests = db.session.query(
        LeaveRequest.id,
        Employee.full_name_arabic.label('employee_name'),
        LeaveRequest.start_date,
        LeaveRequest.end_date,
        LeaveRequest.hours_requested,
        LeaveRequest.status,
        LeaveRequest.timestamp,
        LeaveRequest.type,
        LeaveRequest.classification,
        LeaveRequest.start_time,
        LeaveRequest.end_time,
        LeaveRequest.note,
        LeaveRequest.regular_leave_hours,
        LeaveRequest.sick_leave_hours,
        LeaveRequest.emergency_leave_hours
    ).join(Employee, Employee.id == LeaveRequest.employee_id)\
     .filter(
        LeaveRequest.supervisor_id == supervisor_id,
        LeaveRequest.employee_id != supervisor_id
     ).all()
   
    result = []
    for r in leave_requests:
        request_data = {
            'id': r.id,
            'employee_name': r.employee_name,
            'start_date': r.start_date.strftime('%Y-%m-%d'),
            'hours_requested': r.hours_requested,
            'status': r.status,
            'timestamp': r.timestamp.strftime('%Y-%m-%d %H:%M'),
            'leave_type': r.type,
            'category': r.classification,
            'note': r.note or 'لا يوجد سبب محدد',
            'remaining_balance': {
                'regular': r.regular_leave_hours,
                'sick': r.sick_leave_hours,
                'emergency': r.emergency_leave_hours
            }
        }
        
        # إضافة end_date وأوقات البداية والنهاية حسب نوع الإجازة
        if r.type == 'hourly':
            # للإجازة الساعية: لا نرسل end_date
            request_data['start_time'] = r.start_time.strftime('%H:%M') if r.start_time else None
            request_data['end_time'] = r.end_time.strftime('%H:%M') if r.end_time else None
        elif r.type == 'daily':
            # للإجازة اليومية: end_date يساوي start_date
            request_data['end_date'] = r.end_date.strftime('%Y-%m-%d') if r.end_date else r.start_date.strftime('%Y-%m-%d')
        elif r.type == 'multi-day':
            # للإجازة متعددة الأيام: end_date مختلف
            request_data['end_date'] = r.end_date.strftime('%Y-%m-%d') if r.end_date else None
        
        result.append(request_data)
   
    return jsonify({"requests": result}), 200
@app.route('/api/sp-2-overtime-requests', methods=['GET'])
def get_supervisor_2_overtime_requests():
    if 'employee' not in session:
        return jsonify({"message": "يرجى تسجيل الدخول"}), 401
    
    supervisor_id = session['employee']['id']
    supervisor = db.session.get(Employee, supervisor_id)
    
    if not supervisor or supervisor.role != 'مشرف':
        return jsonify({"message": "غير مصرح بالوصول"}), 403
    
    # جلب طلبات العمل الإضافي للقسم مع حقول الوقت
    overtime_requests = db.session.query(
        AdditionalAttendanceRecord.id,
        Employee.full_name_arabic.label('employee_name'),
        AdditionalAttendanceRecord.date,
        AdditionalAttendanceRecord.add_attendance_minutes,
        AdditionalAttendanceRecord.status,
        AdditionalAttendanceRecord.start_time,  # أضفنا
        AdditionalAttendanceRecord.end_time     # أضفنا
    ).join(Employee, Employee.id == AdditionalAttendanceRecord.employee_id)\
     .filter(
        Employee.department_id == supervisor.department_id,
        AdditionalAttendanceRecord.employee_id != supervisor_id
     ).all()
    
    # تحويل الدقائق إلى ساعات وإضافة الوقت
    result = [{
        'id': r.id,
        'employee_name': r.employee_name,
        'date': r.date.strftime('%Y-%m-%d'),
        'hours': round(r.add_attendance_minutes / 60, 2),
        'status': r.status,
        'start_time': r.start_time.strftime('%H:%M') if r.start_time else None,  # تحويل الوقت إلى سلسلة
        'end_time': r.end_time.strftime('%H:%M') if r.end_time else None
    } for r in overtime_requests]
    
    return jsonify({"requests": result}), 200
@app.route('/api/sp-2-compensation-leave-requests', methods=['GET'])
def get_supervisor_2_compensation_requests():
    if 'employee' not in session:
        return jsonify({"message": "يرجى تسجيل الدخول"}), 401
    
    supervisor_id = session['employee']['id']
    supervisor = db.session.get(Employee, supervisor_id)
    
    if not supervisor or supervisor.role != 'مشرف':
        return jsonify({"message": "غير مصرح بالوصول"}), 403
    
    # جلب طلبات التعويض للقسم
    comp_requests = db.session.query(
        CompensationLeaveRequest.id,
        Employee.full_name_arabic.label('employee_name'),
        CompensationLeaveRequest.date,
        CompensationLeaveRequest.hours_requested,
        CompensationLeaveRequest.status,
        CompensationLeaveRequest.timestamp,
        CompensationLeaveRequest.start_time,
        CompensationLeaveRequest.end_time,
        CompensationLeaveRequest.note
    ).join(Employee, Employee.id == CompensationLeaveRequest.employee_id)\
     .filter(
        CompensationLeaveRequest.supervisor_id == supervisor_id,
        CompensationLeaveRequest.employee_id != supervisor_id  # استبعاد المشرف نفسه
     ).all()
    
    result = [{
        'id': r.id,
        'employee_name': r.employee_name,
        'date': r.date.strftime('%Y-%m-%d'),
        'hours': r.hours_requested,
        'status': r.status,
        'timestamp': r.timestamp.strftime('%Y-%m-%d %H:%M'),
        'start_time': r.start_time.strftime('%H:%M') if r.start_time else None,
        'end_time': r.end_time.strftime('%H:%M') if r.end_time else None,
        'note': r.note
    } for r in comp_requests]
    
    return jsonify({"requests": result}), 200
@app.route('/api/sp-2-delay-requests', methods=['GET'])
def get_supervisor_2_delay_requests():
    if 'employee' not in session:
        return jsonify({"message": "يرجى تسجيل الدخول"}), 401
    
    supervisor_id = session['employee']['id']
    supervisor = db.session.get(Employee, supervisor_id)
    
    if not supervisor or supervisor.role != 'مشرف':
        return jsonify({"message": "غير مصرح بالوصول"}), 403
    
    # جلب طلبات التأخير المخصصة لهذا المشرف
    delay_requests = db.session.query(
        WorkDelayArchive.id,
        Employee.full_name_arabic.label('employee_name'),
        WorkDelayArchive.date,
        WorkDelayArchive.minutes_delayed,
        WorkDelayArchive.status,
        WorkDelayArchive.timestamp,
        WorkDelayArchive.delay_note
    ).join(Employee, Employee.id == WorkDelayArchive.employee_id) \
     .join(Supervisor, Supervisor.supervisor_ID == WorkDelayArchive.supervisor_id) \
     .filter(
        WorkDelayArchive.supervisor_id == supervisor_id,
        WorkDelayArchive.employee_id != supervisor_id  # استبعاد المشرف نفسه
     ).all()
    
    # Debug output
    print(f"Found {len(delay_requests)} delay requests for supervisor {supervisor_id}")
    
    result = [{
        'id': r.id,
        'employee_name': r.employee_name,
        'date': r.date.strftime('%Y-%m-%d'),
        'minutes_delayed': r.minutes_delayed,
        'status': r.status,
        'timestamp': r.timestamp.strftime('%Y-%m-%d %H:%M') if r.timestamp else None,
        'justification_note': r.delay_note
    } for r in delay_requests]
    
    return jsonify({"requests": result}), 200
@app.route('/api/handle-request/<string:request_type>/<int:request_id>/<string:action>', methods=['PUT'])
def handle_supervisor_request(request_type, request_id, action):
    if 'employee' not in session:
        return jsonify({"message": "يرجى تسجيل الدخول"}), 401

    supervisor_id = session['employee']['id']
    supervisor = db.session.get(Employee, supervisor_id)

    if not supervisor or supervisor.role != 'مشرف':
        return jsonify({"message": "غير مصرح بالوصول"}), 403

    model_map = {
        'leave': LeaveRequest,
        'overtime': AdditionalAttendanceRecord,
        'compensation': CompensationLeaveRequest,
        'delay': WorkDelayArchive
    }

    # قاموس لتحويل أنواع الطلبات إلى العربية
    request_type_arabic = {
        'leave': 'إجازة',
        'overtime': 'عمل إضافي',
        'compensation': 'تعويض',
        'delay': 'تأخير'
    }
    
    # قاموس لتحويل أنواع الإجازات إلى العربية
    leave_type_arabic = {
        'hourly': 'ساعية',
        'daily': 'يومية',
        'multi-day': 'متعددة الأيام'
    }
    
    # قاموس لتحويل تصنيفات الإجازات إلى العربية
    classification_arabic = {
        'normal': 'عادية',
        'sick': 'مرضية',
        'emergency': 'خاصة'
    }

    model = model_map.get(request_type)
    if not model:
        return jsonify({"message": "نوع الطلب غير صحيح"}), 400

    request_record = db.session.get(model, request_id)
    if not request_record:
        return jsonify({"message": "الطلب غير موجود"}), 404

    employee = db.session.get(Employee, request_record.employee_id)
    if not employee:
        return jsonify({"message": "الموظف صاحب الطلب غير موجود"}), 404

    if employee.department_id != supervisor.department_id:
        return jsonify({"message": "غير مصرح بتعديل هذا الطلب"}), 403

    # حفظ الحالة القديمة للطلب (للتأكد من التغيير)
    old_status = request_record.status

    # تحديث حالة الطلب
# تحديث حالة الطلب
    if request_type == 'delay':
        if action == 'approve':
            request_record.status = 'Justified'
        elif action == 'reject':
            request_record.status = 'Unjustified'

        # تعديل أرصدة التأخير مباشرة بعد تحديث الحالة
        delay_hours = request_record.minutes_delayed / 60  # تحويل دقائق التأخير لساعات

        if action == 'approve' and old_status != 'Justified':
            if delay_hours > employee.regular_leave_remaining:
                return jsonify({
                    "message": "الرصيد غير كافي لتبرير هذا التأخير",
                    "requested": delay_hours,
                    "available": employee.regular_leave_remaining
                }), 400

            employee.regular_leave_used += delay_hours
            employee.regular_leave_remaining -= delay_hours

        elif action == 'reject' and old_status == 'Justified':
            employee.regular_leave_used -= delay_hours
            employee.regular_leave_remaining += delay_hours

    else:
        request_record.status = 'approved' if action == 'approve' else 'rejected'

    # معالجة أرصدة الإجازات في حالة طلبات الإجازة
    if request_type == 'leave':
        classification = request_record.classification
        hours_requested = request_record.hours_requested
        
        # تحديد الأعمدة المناسبة بناءً على نوع الإجازة
        used_attr = f"{classification}_leave_used"
        remaining_attr = f"{classification}_leave_remaining"
        total_attr = f"{classification}_leave_total"
        
        if action == 'approve' and old_status != 'approved':
            # الموافقة على طلب إجازة - نخصم من الرصيد
            # التحقق أولاً من أن الرصيد كافي
            current_balance = getattr(employee, remaining_attr, 0)
            if hours_requested > current_balance:
                return jsonify({
                    "message": "رصيد الإجازة غير كافي للموافقة على هذا الطلب",
                    "requested": hours_requested,
                    "available": current_balance
                }), 400
            
            # زيادة الساعات المستخدمة
            setattr(employee, used_attr, getattr(employee, used_attr, 0) + hours_requested)
            # تقليل الرصيد المتبقي
            setattr(employee, remaining_attr, getattr(employee, remaining_attr, 0) - hours_requested)
            
        elif action == 'reject' and old_status == 'approved':
            # رفض طلب إجازة كان معتمداً سابقاً - نرجع الرصيد
            setattr(employee, used_attr, getattr(employee, used_attr, 0) - hours_requested)
            setattr(employee, remaining_attr, getattr(employee, remaining_attr, 0) + hours_requested)
    if request_type == 'compensation':
        if action == 'approve' and old_status != 'approved':
            hours_requested = request_record.hours_requested if request_record.hours_requested else 0
            
            # زيادة فقط الرصيد المتبقي
            employee.regular_leave_remaining += hours_requested
            employee.regular_leave_used = max(0, employee.regular_leave_used - hours_requested)
        elif action == 'reject' and old_status == 'approved':
            hours_requested = request_record.hours_requested if request_record.hours_requested else 0
            # إلغاء الزيادة في حالة رفض طلب معتمد سابقاً
            employee.regular_leave_remaining -= hours_requested
            employee.regular_leave_used += hours_requested
    if request_type == 'overtime' and action == 'approve':
        overtime_hours = request_record.add_attendance_minutes / 60
        # employee.overtime_balance += overtime_hours

    db.session.commit()

    # إرسال إشعار للموظف
    notification = Notification(
        recipient_id=request_record.employee_id,
        message=f"تم {'الموافقة على' if action=='approve' else 'رفض'} طلبك ({request_type_arabic.get(request_type, request_type)})"
    )
    db.session.add(notification)
    db.session.commit()

    # إرسال رسالة تيليغرام إلى الموظف
    try:
        if employee.telegram_chatid:
            # تنسيق الرسالة حسب نوع الطلب
            if request_type == 'leave':
                # تحويل النوع والتصنيف إلى العربية
                arabic_type = leave_type_arabic.get(request_record.type, request_record.type)
                arabic_classification = classification_arabic.get(request_record.classification, request_record.classification)
                
                # تحديد تفاصيل العرض حسب نوع الإجازة
                if request_record.type == 'hourly':
                    # تحويل الوقت إلى تنسيق مناسب
                    start_time_str = request_record.start_time.strftime('%I:%M %p') if request_record.start_time else "غير محدد"
                    end_time_str = request_record.end_time.strftime('%I:%M %p') if request_record.end_time else "غير محدد"
                    
                    details = f"""
📅 <b>التاريخ:</b> {request_record.start_date}
⏰ <b>الوقت:</b> من {start_time_str} إلى {end_time_str}
⏱️ <b>المدة:</b> {request_record.hours_requested:.2f} ساعة
📝 <b>السبب:</b> {request_record.note}
                    """
                elif request_record.type == 'daily':
                    details = f"""
📅 <b>التاريخ:</b> {request_record.start_date}
⏱️ <b>المدة:</b> {request_record.hours_requested:.2f} ساعة
📝 <b>السبب:</b> {request_record.note}
                    """
                else:
                    details = f"""
📅 <b>من تاريخ:</b> {request_record.start_date}
📅 <b>إلى تاريخ:</b> {request_record.end_date}
⏱️ <b>المدة:</b> {request_record.hours_requested:.2f} ساعة
📝 <b>السبب:</b> {request_record.note}
                    """
                    
                employee_message = f"""
{'✅' if action == 'approve' else '❌'} <b>تم {'الموافقة على' if action == 'approve' else 'رفض'} طلب الإجازة</b>
━━━━━━━━━━━━━━━━━━━━
👤 <b>الموظف:</b> {employee.full_name_arabic}
📋 <b>نوع الإجازة:</b> {arabic_type}
🏷️ <b>التصنيف:</b> {arabic_classification}
{details}
🕒 <b>وقت المعالجة:</b> {datetime.now(pytz.timezone("Asia/Damascus")).strftime("%Y-%m-%d %I:%M %p")}
━━━━━━━━━━━━━━━━━━━━
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
                """
                
            elif request_type == 'overtime':
                # تحويل الدقائق إلى ساعات ودقائق
                hours = request_record.add_attendance_minutes // 60
                minutes = request_record.add_attendance_minutes % 60
                time_display = f"{hours} ساعة و {minutes} دقيقة" if hours > 0 else f"{minutes} دقيقة"
                start_time_str = request_record.start_time.strftime('%I:%M %p') if request_record.start_time else "غير محدد"
                end_time_str = request_record.end_time.strftime('%I:%M %p') if request_record.end_time else "غير محدد"
                
                employee_message = f"""
{'✅' if action == 'approve' else '❌'} <b>تم {'الموافقة على' if action == 'approve' else 'رفض'} طلب العمل الإضافي</b>
━━━━━━━━━━━━━━━━━━━━
👤 <b>الموظف:</b> {employee.full_name_arabic}
📅 <b>التاريخ:</b> {request_record.date}
⏰ <b>الوقت:</b> от {start_time_str} إلى {end_time_str}
⏱️ <b>المدة:</b> {time_display}
📝 <b>السبب:</b> {request_record.notes}
🕒 <b>وقت المعالجة:</b> {datetime.now(pytz.timezone("Asia/Damascus")).strftime("%Y-%m-%d %I:%M %p")}
━━━━━━━━━━━━━━━━━━━━
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
                """
                
            elif request_type == 'compensation':
                # التحقق من وجود البيانات قبل استخدامها
                date_str = request_record.date.strftime('%Y-%m-%d') if request_record.date else "غير محدد"
                
                start_time_str = "غير محدد"
                if request_record.start_time:
                    if hasattr(request_record.start_time, 'strftime'):
                        start_time_str = request_record.start_time.strftime('%I:%M %p')
                    else:
                        start_time_str = str(request_record.start_time)
                
                end_time_str = "غير محدد"
                if request_record.end_time:
                    if hasattr(request_record.end_time, 'strftime'):
                        end_time_str = request_record.end_time.strftime('%I:%M %p')
                    else:
                        end_time_str = str(request_record.end_time)
                
                hours = request_record.hours_requested if request_record.hours_requested else 0
                note = request_record.note if request_record.note else "لا يوجد"
                
                employee_message = f"""
{'✅' if action == 'approve' else '❌'} <b>تم {'الموافقة على' if action == 'approve' else 'رفض'} طلب التعويض</b>
━━━━━━━━━━━━━━━━━━━━
👤 <b>الموظف:</b> {employee.full_name_arabic}
📅 <b>التاريخ:</b> {date_str}
⏰ <b>من وقت:</b> {start_time_str}
⏰ <b>إلى وقت:</b> {end_time_str}
⏱️ <b>المدة:</b> {hours:.2f} ساعة
📝 <b>السبب:</b> {note}
🕒 <b>وقت المعالجة:</b> {datetime.now(pytz.timezone("Asia/Damascus")).strftime("%Y-%m-%d %I:%M %p")}
━━━━━━━━━━━━━━━━━━━━
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
                """
                
            elif request_type == 'delay':
                # تحويل دقائق التأخير إلى تنسيق أفضل
                delay_hours = request_record.minutes_delayed // 60
                delay_minutes = request_record.minutes_delayed % 60
                delay_display = f"{delay_hours} ساعة و {delay_minutes} دقيقة" if delay_hours > 0 else f"{delay_minutes} دقيقة"
                from_time_str = request_record.from_timestamp.strftime('%I:%M %p') if request_record.from_timestamp else "غير محدد"
                to_time_str = request_record.to_timestamp.strftime('%I:%M %p') if request_record.to_timestamp else "غير محدد"

                employee_message = f"""
{'✅' if action == 'approve' else '❌'} <b>تم {'تبرير' if action == 'approve' else 'رفض تبرير'} التأخير</b>
━━━━━━━━━━━━━━━━━━━━
👤 <b>الموظف:</b> {employee.full_name_arabic}
📅 <b>التاريخ:</b> {request_record.date}
⏰ <b>وقت التأخير:</b> من {from_time_str} إلى {to_time_str}
⏱️ <b>مدة التأخير:</b> {delay_display}
📝 <b>السبب/التبرير:</b> {request_record.delay_note if request_record.delay_note else "لا يوجد"}
🕒 <b>وقت المعالجة:</b> {datetime.now(pytz.timezone("Asia/Damascus")).strftime("%Y-%m-%d %I:%M %p")}
━━━━━━━━━━━━━━━━━━━━
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
                """
            
            # إرسال الرسالة إلى الموظف عبر التلغرام
            send_telegram_message(employee.telegram_chatid, employee_message)
            
    except Exception as e:
        print(f"فشل في إرسال الرسالة إلى الموظف عبر التلغرام: {str(e)}")
        # يمكنك إضافة تسجيل الخطأ في قاعدة البيانات هنا إذا أردت

    # إرسال الطلب المعتمد إلى مجموعة التلغرام كأرشيف
    if action == 'approve':
        try:
            # تنسيق الرسالة حسب نوع الطلب
            if request_type == 'leave':
                # تحويل النوع والتصنيف إلى العربية
                arabic_type = leave_type_arabic.get(request_record.type, request_record.type)
                arabic_classification = classification_arabic.get(request_record.classification, request_record.classification)
                
                # تحديد تفاصيل العرض حسب نوع الإجازة
                if request_record.type == 'hourly':
                    # تحويل الوقت إلى تنسيق مناسب
                    start_time_str = request_record.start_time.strftime('%I:%M %p') if request_record.start_time else "غير محدد"
                    end_time_str = request_record.end_time.strftime('%I:%M %p') if request_record.end_time else "غير محدد"
                    
                    details = f"""
📋 <b>نوع الإجازة:</b> {arabic_type}
🏷️ <b>التصنيف:</b> {arabic_classification}
📅 <b>التاريخ:</b> {request_record.start_date}
⏰ <b>الوقت:</b> من {start_time_str} إلى {end_time_str}
⏱️ <b>المدة:</b> {request_record.hours_requested:.2f} ساعة
📝 <b>السبب:</b> {request_record.note}
                    """
                elif request_record.type == 'daily':
                    details = f"""
📋 <b>نوع الإجازة:</b> {arabic_type}
🏷️ <b>التصنيف:</b> {arabic_classification}
📅 <b>التاريخ:</b> {request_record.start_date}
⏱️ <b>المدة:</b> {request_record.hours_requested:.2f} ساعة
📝 <b>السبب:</b> {request_record.note}
                    """
                elif request_record.type == 'multi-day':
                    details = f"""
📋 <b>نوع الإجازة:</b> {arabic_type}
🏷️ <b>التصنيف:</b> {arabic_classification}
📅 <b>من تاريخ:</b> {request_record.start_date}
📅 <b>إلى تاريخ:</b> {request_record.end_date}
⏱️ <b>المدة:</b> {request_record.hours_requested:.2f} ساعة
📝 <b>السبب:</b> {request_record.note}
                    """
                else:
                    details = f"""
📋 <b>نوع الإجازة:</b> {arabic_type}
🏷️ <b>التصنيف:</b> {arabic_classification}
📅 <b>من تاريخ:</b> {request_record.start_date}
📅 <b>إلى تاريخ:</b> {request_record.end_date}
⏱️ <b>المدة:</b> {request_record.hours_requested:.2f} ساعة
📝 <b>السبب:</b> {request_record.note}
                    """
            elif request_type == 'overtime':
                # تحويل الدقائق إلى ساعات ودقائق
                hours = request_record.add_attendance_minutes // 60
                minutes = request_record.add_attendance_minutes % 60
                time_display = f"{hours} ساعة و {minutes} دقيقة" if hours > 0 else f"{minutes} دقيقة"
                start_time_str = request_record.start_time.strftime('%I:%M %p') if request_record.start_time else "غير محدد"
                end_time_str = request_record.end_time.strftime('%I:%M %p') if request_record.end_time else "غير محدد"
                details = f"""
📅 <b>التاريخ:</b> {request_record.date}
⏰ <b>الوقت:</b> من {start_time_str} إلى {end_time_str}
⏱️ <b>المدة:</b> {time_display}
📝 <b>السبب:</b> {request_record.notes}
                """
            elif request_type == 'compensation':
                # التحقق من وجود البيانات قبل استخدامها
                date_str = request_record.date.strftime('%Y-%m-%d') if request_record.date else "غير محدد"
                
                start_time_str = "غير محدد"
                if request_record.start_time:
                    if hasattr(request_record.start_time, 'strftime'):
                        start_time_str = request_record.start_time.strftime('%I:%M %p')
                    else:
                        start_time_str = str(request_record.start_time)
                
                end_time_str = "غير محدد"
                if request_record.end_time:
                    if hasattr(request_record.end_time, 'strftime'):
                        end_time_str = request_record.end_time.strftime('%I:%M %p')
                    else:
                        end_time_str = str(request_record.end_time)
                
                hours = request_record.hours_requested if request_record.hours_requested else 0
                note = request_record.note if request_record.note else "لا يوجد"
                
                details = f"""
📅 <b>التاريخ:</b> {date_str}
⏰ <b>من وقت:</b> {start_time_str}
⏰ <b>إلى وقت:</b> {end_time_str}
⏱️ <b>المدة:</b> {hours:.2f} ساعة
📝 <b>السبب:</b> {note}
                """
            elif request_type == 'delay':
                # تحويل دقائق التأخير إلى تنسيق أفضل
                delay_hours = request_record.minutes_delayed // 60
                delay_minutes = request_record.minutes_delayed % 60
                delay_display = f"{delay_hours} ساعة و {delay_minutes} دقيقة" if delay_hours > 0 else f"{delay_minutes} دقيقة"
                from_time_str = request_record.from_timestamp.strftime('%I:%M %p') if request_record.from_timestamp else "غير محدد"
                to_time_str = request_record.to_timestamp.strftime('%I:%M %p') if request_record.to_timestamp else "غير محدد"

                details = f"""
📅 <b>التاريخ:</b> {request_record.date}
⏰ <b>وقت التأخير:</b> من {from_time_str} إلى {to_time_str}
⏱️ <b>مدة التأخير:</b> {delay_display}
📝 <b>السبب/تبرير التأخير:</b> {request_record.delay_note if request_record.delay_note else "لا يوجد"}
                """
            else:
                details = "📋 لا توجد تفاصيل إضافية"

            archive_message = f"""
📋 <b>طلب معتمد - أرشيف</b>
━━━━━━━━━━━━━━━━━━━━
📄 <b>نوع الطلب:</b> {"تبرير التأخير" if request_type == "delay" else request_type_arabic.get(request_type, request_type)}
👤 <b>الموظف:</b> {employee.full_name_arabic}
🏢 <b>القسم:</b> {employee.department.dep_name}
👨‍💼 <b>المشرف:</b> {supervisor.full_name_arabic}
{details}
🕒 <b>وقت المعالجة:</b> {datetime.now(pytz.timezone("Asia/Damascus")).strftime("%Y-%m-%d %I:%M %p")}
━━━━━━━━━━━━━━━━━━━━
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
            """
            
            group_chat_id = "-4847322310"
            send_telegram_message(group_chat_id, archive_message)
            
            # إرسال رسالة منفصلة للإجازات لإعلام الموظفين في القسم فقط
            if request_type == 'leave':
                # تحويل النوع والتصنيف إلى العربية
                arabic_type = leave_type_arabic.get(request_record.type, request_record.type)
                arabic_classification = classification_arabic.get(request_record.classification, request_record.classification)
                
                # رسالة مختصرة للموظفين مع تفاصيل التاريخ والوقت ولكن بدون السبب
                if request_record.type == 'hourly':
                    start_time_str = request_record.start_time.strftime('%I:%M %p') if request_record.start_time else "غير محدد"
                    end_time_str = request_record.end_time.strftime('%I:%M %p') if request_record.end_time else "غير محدد"
                    leave_details = f"""
📋 <b>نوع الإجازة:</b> {arabic_type}
🏷️ <b>التصنيف:</b> {arabic_classification}
📅 <b>التاريخ:</b> {request_record.start_date}
⏰ <b>وقت البدء:</b> {start_time_str}
⏰ <b>وقت الانتهاء:</b> {end_time_str}
⏱️ <b>المدة:</b> {request_record.hours_requested:.2f} ساعة
                    """
                elif request_record.type == 'daily':
                    leave_details = f"""
📋 <b>نوع الإجازة:</b> {arabic_type}
🏷️ <b>التصنيف:</b> {arabic_classification}
📅 <b>التاريخ:</b> {request_record.start_date}
⏱️ <b>المدة:</b> {request_record.hours_requested:.2f} ساعة
                    """
                elif request_record.type == 'multi-day':
                    leave_details = f"""
📋 <b>نوع الإجازة:</b> {arabic_type}
🏷️ <b>التصنيف:</b> {arabic_classification}
📅 <b>تاريخ البدء:</b> {request_record.start_date}
📅 <b>تاريخ الانتهاء:</b> {request_record.end_date}
⏱️ <b>المدة:</b> {request_record.hours_requested:.2f} ساعة
                    """
                else:
                    leave_details = f"""
📋 <b>نوع الإجازة:</b> {arabic_type}
🏷️ <b>التصنيف:</b> {arabic_classification}
📅 <b>تاريخ البدء:</b> {request_record.start_date}
📅 <b>تاريخ الانتهاء:</b> {request_record.end_date}
⏱️ <b>المدة:</b> {request_record.hours_requested:.2f} ساعة
                    """
                
                # رسالة إعلام للموظفين
                announcement_message = f"""
📢 <b>إشعار إجازة موظف</b>
━━━━━━━━━━━━━━━━━━━━
👤 <b>الموظف:</b> {employee.full_name_arabic}
{leave_details}
🕒 <b>وقت الإعلان:</b> {datetime.now(pytz.timezone("Asia/Damascus")).strftime("%Y-%m-%d %I:%M %p")}
━━━━━━━━━━━━━━━━━━━━
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
                """
                
                # جمع جميع telegram_chatid للموظفين في القسم نفسه
                department_employees = Employee.query.filter_by(
                    department_id=employee.department_id
                ).filter(
                    Employee.telegram_chatid.isnot(None),
                    Employee.id != employee.id  # استبعاد الموظف صاحب الإجازة
                ).all()
                
                # إضافة المشرف إلى قائمة المستلمين إذا كان لديه telegram_chatid ولم يكن هو صاحب الإجازة
                if supervisor.telegram_chatid and supervisor.id != employee.id:
                    department_employees.append(supervisor)
                
                # إرسال الرسالة لكل موظف في القسم بشكل منفرد
                for dept_employee in department_employees:
                    if dept_employee.telegram_chatid:
                        try:
                            send_telegram_message(dept_employee.telegram_chatid, announcement_message)
                        except Exception as e:
                            print(f"فشل في إرسال الرسالة إلى {dept_employee.full_name_arabic}: {str(e)}")
                
        except Exception as e:
            print(f"فشل في إرسال الأرشيف إلى التلغرام: {str(e)}")
            # يمكنك إضافة تسجيل الخطأ في قاعدة البيانات هنا إذا أردت

    return jsonify({
        "success": True,
        "message": f"تم {'الموافقة على' if action=='approve' else 'رفض'} الطلب بنجاح"
    }), 200
@app.route('/api/sp-overtime-requests/<int:request_id>/time', methods=['PUT'])
def update_overtime_time(request_id):
    if 'employee' not in session:
        return jsonify({"message": "يرجى تسجيل الدخول"}), 401
    
    data = request.get_json()
    time_type = data.get('time_type')  # 'start_time' أو 'end_time'
    time_value = data.get('time_value')  # القيمة الجديدة للوقت
    
    if not time_type or time_type not in ['start_time', 'end_time']:
        return jsonify({"message": "نوع الوقت غير صالح"}), 400
    
    if not time_value:
        return jsonify({"message": "قيمة الوقت غير صالحة"}), 400
    
    # جلب طلب العمل الإضافي
    overtime_request = db.session.get(AdditionalAttendanceRecord, request_id)
    if not overtime_request:
        return jsonify({"message": "طلب العمل الإضافي غير موجود"}), 404
    
    # تحديث الوقت المطلوب
    if time_type == 'start_time':
        overtime_request.start_time = datetime.strptime(time_value, '%H:%M').time()
    else:
        overtime_request.end_time = datetime.strptime(time_value, '%H:%M').time()
    
    # إذا كان كلا الوقتين موجودين، احسب الفرق
    if overtime_request.start_time and overtime_request.end_time:
        start_dt = datetime.combine(datetime.today(), overtime_request.start_time)
        end_dt = datetime.combine(datetime.today(), overtime_request.end_time)
        
        # إذا كان وقت النهاية قبل البداية، نعتبر أن النهاية في اليوم التالي
        if end_dt < start_dt:
            end_dt += timedelta(days=1)
        
        diff = end_dt - start_dt
        total_minutes = int(diff.total_seconds() / 60)
        overtime_request.add_attendance_minutes = total_minutes
    
    db.session.commit()
    
    # إعادة الساعات المحسوبة (بالساعات)
    updated_hours = overtime_request.add_attendance_minutes / 60.0
    
    return jsonify({
        "success": True,
        "message": "تم تحديث الوقت بنجاح",
        "updated_minutes": overtime_request.add_attendance_minutes,
        "updated_hours": round(updated_hours, 2)
    }), 200
@app.route('/api/sp-compensation-leave-requests/<int:request_id>/time', methods=['PUT'])
def update_compensation_time(request_id):
    if 'employee' not in session:
        return jsonify({"message": "يرجى تسجيل الدخول"}), 401
    
    data = request.get_json()
    time_type = data.get('time_type')
    time_value = data.get('time_value')
    
    if not time_type or time_type not in ['start_time', 'end_time']:
        return jsonify({"message": "نوع الوقت غير صالح"}), 400
    
    if not time_value:
        return jsonify({"message": "قيمة الوقت غير صالحة"}), 400
    
    # جلب طلب التعويض
    comp_request = db.session.get(CompensationLeaveRequest, request_id)
    if not comp_request:
        return jsonify({"message": "طلب التعويض غير موجود"}), 404
    
    # تحديث الوقت المطلوب
    if time_type == 'start_time':
        comp_request.start_time = datetime.strptime(time_value, '%H:%M').time()
    else:
        comp_request.end_time = datetime.strptime(time_value, '%H:%M').time()
    
    # إذا كان كلا الوقتين موجودين، احسب الساعات
    if comp_request.start_time and comp_request.end_time:
        start_dt = datetime.combine(datetime.today(), comp_request.start_time)
        end_dt = datetime.combine(datetime.today(), comp_request.end_time)
        
        # إذا كان وقت النهاية قبل البداية، نعتبر أن النهاية في اليوم التالي
        if end_dt < start_dt:
            end_dt += timedelta(days=1)
        
        diff = end_dt - start_dt
        total_hours = round(diff.total_seconds() / 3600, 2)
        comp_request.hours_requested = total_hours
    
    db.session.commit()
    
    return jsonify({
        "success": True,
        "message": "تم تحديث الوقت بنجاح",
        "updated_hours": comp_request.hours_requested
    }), 200
@app.route('/api/justify-delay', methods=['POST'])
def justify_delay():
    if 'employee' not in session:
        return jsonify({"success": False, "message": "يرجى تسجيل الدخول"}), 401
        
    data = request.get_json()
    delay_id = data.get('delay_id')
    justification_note = data.get('justification_note')
    
    if not delay_id or not justification_note:
        return jsonify({"success": False, "message": "معرّف التأخير وسبب التبرير مطلوبان"}), 400
    
    employee_id = session['employee']['id']
    employee = db.session.get(Employee, employee_id)
    
    if not employee:
        return jsonify({"success": False, "message": "الموظف غير موجود"}), 404
        
    delay_record = db.session.get(WorkDelayArchive, delay_id)
    if not delay_record:
        return jsonify({"success": False, "message": "سجل التأخير غير موجود"}), 404
        
    if delay_record.employee_id != employee.id:
        return jsonify({"success": False, "message": "ليس لديك صلاحية لتبرير هذا التأخير"}), 403
    
    # حساب عدد ساعات التأخير
    delay_hours = getattr(delay_record, 'minutes_delayed', 0) / 60
    
    # التحقق من الرصيد المتبقي - هذا ينطبق على جميع الموظفين بما فيهم المشرفين
    if delay_hours > employee.regular_leave_remaining:
        return jsonify({
            "success": False,
            "message": f"الرصيد غير كافٍ لتبرير التأخير. الساعات المطلوبة: {delay_hours:.2f}, المتبقي: {employee.regular_leave_remaining:.2f}"
        }), 400
    
    department_supervisors = Supervisor.query.filter_by(dep_id=employee.department_id).all()
    if department_supervisors:
        delay_record.supervisor_id = department_supervisors[0].supervisor_ID
    
    syria_tz = pytz.timezone("Asia/Damascus")
    
    # التحقق من كون الموظف مشرفًا
    is_supervisor = Supervisor.query.filter_by(supervisor_ID=employee_id).first() is not None
    
    if is_supervisor:
        # للمشرف - التبرير التلقائي بعد التحقق من الرصيد
        delay_record.status = 'Justified'
        delay_record.delay_note = justification_note
        
        # خصم الرصيد مباشرة
        employee.regular_leave_used += delay_hours
        employee.regular_leave_remaining -= delay_hours
        
        try:
            db.session.commit()
            
            # إرسال إشعار للموظف (المشرف نفسه)
            notification = Notification(
                recipient_id=employee_id,
                message="تم تبرير التأخير تلقائياً"
            )
            db.session.add(notification)
            
            # إرسال رسالة تلغرام للموظف (المشرف)
            if employee.telegram_chatid:
                delay_minutes = getattr(delay_record, 'minutes_delayed', 0)
                delay_display = f"{delay_hours:.0f} ساعة و {delay_minutes % 60} دقيقة" if delay_hours >= 1 else f"{delay_minutes} دقيقة"
                from_time_str = delay_record.from_timestamp.strftime('%I:%M %p') if delay_record.from_timestamp else "غير محدد"
                to_time_str = delay_record.to_timestamp.strftime('%I:%M %p') if delay_record.to_timestamp else "غير محدد"
                
                employee_message = f"""
✅ <b>تم تبرير التأخير تلقائياً</b>
━━━━━━━━━━━━━━━━━━━━
👤 <b>الموظف:</b> {employee.full_name_arabic}
📅 <b>التاريخ:</b> {delay_record.date.strftime('%Y-%m-%d') if delay_record.date else 'غير محدد'}
⏰ <b>وقت التأخير:</b> من {from_time_str} إلى {to_time_str}
⏱️ <b>مدة التأخير:</b> {delay_display}
📝 <b>سبب/التبرير:</b> {justification_note}
🕒 <b>وقت المعالجة:</b> {datetime.now(syria_tz).strftime("%Y-%m-%d %I:%M %p")}
━━━━━━━━━━━━━━━━━━━━
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
                """
                send_telegram_message(employee.telegram_chatid, employee_message)
            
            # إرسال الطلب المعتمد إلى مجموعة التلغرام كأرشيف
            try:
                delay_minutes = getattr(delay_record, 'minutes_delayed', 0)
                delay_display = f"{delay_hours:.0f} ساعة و {delay_minutes % 60} دقيقة" if delay_hours >= 1 else f"{delay_minutes} دقيقة"
                from_time_str = delay_record.from_timestamp.strftime('%I:%M %p') if delay_record.from_timestamp else "غير محدد"
                to_time_str = delay_record.to_timestamp.strftime('%I:%M %p') if delay_record.to_timestamp else "غير محدد"
                
                archive_message = f"""
📋 <b>طلب معتمد - أرشيف</b>
━━━━━━━━━━━━━━━━━━━━
📄 <b>نوع الطلب:</b> تبرير التأخير
👤 <b>الموظف:</b> {employee.full_name_arabic}
🏢 <b>القسم:</b> {employee.department.dep_name}
👨‍💼 <b>المشرف:</b> {employee.full_name_arabic}
📅 <b>التاريخ:</b> {delay_record.date.strftime('%Y-%m-%d') if delay_record.date else 'غير محدد'}
⏰ <b>وقت التأخير:</b> من {from_time_str} إلى {to_time_str}
⏱️ <b>مدة التأخير:</b> {delay_display}
📝 <b>سبب/تبرير التأخير:</b> {justification_note}
🕒 <b>وقت المعالجة:</b> {datetime.now(syria_tz).strftime("%Y-%m-%d %I:%M %p")}
━━━━━━━━━━━━━━━━━━━━
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
                """
                group_chat_id = "-4847322310"
                send_telegram_message(group_chat_id, archive_message)
            except Exception as e:
                print(f"فشل في إرسال الأرشيف إلى التلغرام: {str(e)}")
            
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": "تم تبرير التأخير تلقائياً",
                "immediately_justified": True,
                "hours_deducted": delay_hours
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f"حدث خطأ أثناء معالجة الطلب: {str(e)}"
            }), 500
    
    else:
        # للموظف العادي - إرسال للمشرف
        if not department_supervisors:
            return jsonify({"success": False, "message": "لا يوجد مشرفين في القسم"}), 400
        
        delay_record.status = 'pending'
        delay_record.delay_note = justification_note
        
        try:
            db.session.commit()
            
            # إرسال إشعارات للمشرفين
            for supervisor in department_supervisors:
                notification = Notification(
                    recipient_id=supervisor.supervisor_ID,
                    message=f"طلب تبرير تأخير جديد من الموظف {employee.full_name_arabic}",
                )
                db.session.add(notification)
                
                # إرسال إشعار تلغرام للمشرف
                supervisor_employee = db.session.get(Employee, supervisor.supervisor_ID)
                if supervisor_employee and supervisor_employee.telegram_chatid:
                    delay_minutes = getattr(delay_record, 'minutes_delayed', 0)
                    delay_display = f"{delay_hours:.0f} ساعة و {delay_minutes % 60} دقيقة" if delay_hours >= 1 else f"{delay_minutes} دقيقة"
                    from_time_str = delay_record.from_timestamp.strftime('%I:%M %p') if delay_record.from_timestamp else "غير محدد"
                    to_time_str = delay_record.to_timestamp.strftime('%I:%M %p') if delay_record.to_timestamp else "غير محدد"
                    
                    telegram_message = f"""
🔔 <b>طلب تبرير تأخير جديد</b>
━━━━━━━━━━━━━━━━━━━━
👤 الموظف: {employee.full_name_arabic}
📅 التاريخ: {delay_record.date.strftime('%Y-%m-%d') if delay_record.date else 'غير محدد'}
⏰ وقت التأخير: من {from_time_str} إلى {to_time_str}
⏱️ مدة التأخير: {delay_display}
📝 سبب التبرير: {justification_note}
━━━━━━━━━━━━━━━━━━━━
🕒 وقت الإرسال: {datetime.now(syria_tz).strftime("%Y-%m-%d %I:%M %p").replace('AM','ص').replace('PM','م')}
𝑨𝒍𝒎𝒐𝒉𝒕𝒂𝒓𝒊𝒇 🅗🅡
                    """
                    send_telegram_message(supervisor_employee.telegram_chatid, telegram_message)
            
            db.session.commit()
            
            return jsonify({
                "success": True,
                "message": "تم إرسال طلب التبرير إلى المشرف",
                "immediately_justified": False,
                "hours_to_deduct": delay_hours
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "success": False,
                "message": f"حدث خطأ أثناء إرسال الطلب: {str(e)}"
            }), 500
@app.route('/api/employees-list-super', methods=['GET'])
def get_employees_list_super():
    try:
        # التأكد من وجود الموظف في الجلسة
        if 'employee' not in session:
            return jsonify({"message": "يرجى تسجيل الدخول"}), 401
        
        # جلب بيانات الموظف من الجلسة
        supervisor_id = session['employee']['id']
        supervisor = db.session.get(Employee, supervisor_id)
        
        if not supervisor:
            return jsonify({"message": "الموظف غير موجود"}), 404
        
        # تحديد القسم الخاص بالمشرف
        department_id = supervisor.department_id
        
        # جلب الموظفين من نفس القسم بشرط ألا يكونوا ادمن
        employees = Employee.query.filter(
            Employee.department_id == department_id,
            Employee.role != 'ادمن'
        ).all()
        
        # تحويل النتائج إلى قائمة JSON
        employees_data = [
            {
                'id': emp.id,
                'name': emp.full_name_arabic,
                'employee_number': emp.employee_number
            }
            for emp in employees
        ]
        
        # إرجاع البيانات مع معرف المشرف
        return jsonify({
            "employees": employees_data,
            "supervisor_id": supervisor_id  # ✅ إضافة معرف المشرف
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@app.route('/home')
def home():
    if 'employee' not in session:
        return jsonify({"message": "يرجى تسجيل الدخول"}), 401

    employee_id = session['employee']['id']
    employee = db.session.get(Employee, employee_id)  # ✅ الطريقة الحديثة

    if not employee:
        return jsonify({"message": "الموظف غير موجود"}), 404

    return jsonify({
        "message": f"مرحبًا {employee.full_name_arabic}",
        "user": {
            "id": employee.id,
            "full_name_arabic": employee.full_name_arabic,
            "full_name_english": employee.full_name_english,
            "employee_number": employee.employee_number,
            "email": employee.email,
            "telegram_chatid": employee.telegram_chatid,
            "phone": employee.phone,
            "department_id": employee.department_id,
            "department_name": employee.department.dep_name_english if employee.department else None,
            "position": employee.position,
            "position_english": employee.position_english,
            "role": employee.role,
            "status": employee.status,
            "bank_account": employee.bank_account,
            "address": employee.address,
            "weekly_day_off": employee.weekly_day_off,
            "work_start_time": employee.work_start_time.strftime('%H:%M:%S') if employee.work_start_time else None,
            "work_end_time": employee.work_end_time.strftime('%H:%M:%S') if employee.work_end_time else None,
            "date_of_joining": employee.date_of_joining.strftime('%Y-%m-%d') if employee.date_of_joining else None,
            "end_of_service_date": employee.end_of_service_date.strftime('%Y-%m-%d') if employee.end_of_service_date else None,
            "notes": employee.notes,
            "profile_image": employee.profile_image,

            # ✅ الحقول الجديدة
            "study_major": employee.study_major,
            "governorate": employee.governorate,
            "relative_phone": employee.relative_phone,
            "relative_relation": employee.relative_relation,
            "date_of_birth": employee.date_of_birth.strftime('%Y-%m-%d') if employee.date_of_birth else None,
            "national_id": employee.national_id,
            "job_level": employee.job_level,
            "promotion": employee.promotion,
            "career_stages": employee.career_stages,
            "employee_status": employee.employee_status,
            "work_location": employee.work_location,
            "work_nature": employee.work_nature,
            "marital_status": employee.marital_status,
            "nationality": employee.nationality,
            "trainings": employee.trainings,
            "external_privileges": employee.external_privileges,
            "special_leave_record": employee.special_leave_record,
            "drive_folder_link": employee.drive_folder_link,

            # ✅ الإجازات
            "is_leave": employee.is_leave,
            "is_vacation": employee.is_vacation,
            "is_weekly_day_off": employee.is_weekly_day_off,
            "regular_leave_hours": employee.regular_leave_hours,
            "sick_leave_hours": employee.sick_leave_hours,
            "emergency_leave_hours": employee.emergency_leave_hours
        }
    })

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    employee = Employee.query.filter_by(email=email).first()
    if employee and employee.password == password:  # ⚠️ لاحقاً يفضل استخدام hashing مع werkzeug.security
        session['employee'] = {
            "id": employee.id,
            "full_name_arabic": employee.full_name_arabic,
            "full_name_english": employee.full_name_english,
            "employee_number": employee.employee_number,
            "email": employee.email,
            "password": employee.password,  # ⚠️ يفضل ما ترجعها بالـ session لأمان أكثر
            "telegram_chatid": employee.telegram_chatid,
            "phone": employee.phone,
            "department_id": employee.department_id,
            "department_name": employee.department.dep_name if employee.department else None,
            "position": employee.position,
            "position_english": employee.position_english,
            "role": employee.role,
            "bank_account": employee.bank_account,
            "address": employee.address,
            "weekly_day_off": employee.weekly_day_off,
            "work_start_time": employee.work_start_time.strftime('%H:%M:%S') if employee.work_start_time else None,
            "work_end_time": employee.work_end_time.strftime('%H:%M:%S') if employee.work_end_time else None,
            "date_of_joining": employee.date_of_joining.strftime('%Y-%m-%d') if employee.date_of_joining else None,
            "end_of_service_date": employee.end_of_service_date.strftime('%Y-%m-%d') if employee.end_of_service_date else None,
            "notes": employee.notes,
            "profile_image": employee.profile_image,
            "status": employee.status,

            # ✅ الحقول الجديدة
            "study_major": employee.study_major,
            "governorate": employee.governorate,
            "relative_phone": employee.relative_phone,
            "relative_relation": employee.relative_relation,
            "date_of_birth": employee.date_of_birth.strftime('%Y-%m-%d') if employee.date_of_birth else None,
            "national_id": employee.national_id,
            "job_level": employee.job_level,
            "promotion": employee.promotion,
            "career_stages": employee.career_stages,
            "employee_status": employee.employee_status,
            "work_location": employee.work_location,
            "work_nature": employee.work_nature,
            "marital_status": employee.marital_status,
            "nationality": employee.nationality,
            "trainings": employee.trainings,
            "external_privileges": employee.external_privileges,
            "special_leave_record": employee.special_leave_record,
            "drive_folder_link": employee.drive_folder_link,

            # ✅ الإجازات
            "is_leave": employee.is_leave,
            "is_vacation": employee.is_vacation,
            "is_weekly_day_off": employee.is_weekly_day_off,
            "regular_leave_hours": employee.regular_leave_hours,
            "sick_leave_hours": employee.sick_leave_hours,
            "emergency_leave_hours": employee.emergency_leave_hours
        }
        session.permanent = True
        return jsonify({
            "message": "تم تسجيل الدخول بنجاح",
            "user": session['employee']
        }), 200
    else:
        return jsonify({"message": "البريد الإلكتروني أو كلمة المرور غير صحيحة"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('employee', None)  # إزالة بيانات الجلسة الخاصة بالمستخدم
    return jsonify({"message": "تم تسجيل الخروج بنجاح"}), 200


if __name__ == '__main__':
    app.run(debug=True)