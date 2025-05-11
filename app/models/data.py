# -*- coding: utf-8 -*-


from ..extensions import db
from ..model_utils import BelongsTo
from ..model_utils import DateCol
from ..model_utils import DynamicMany
from ..model_utils import IdCol
from ..model_utils import NullableBoolCol
from ..model_utils import NullableStr64Col
from ..model_utils import Str64Col
from ..model_utils import UniqueStr64Col
from ..model_utils import IntCol


class SchoolClass(db.Model):  # type: ignore[misc, name-defined]
    """
    班级
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "classes"
    id = IdCol()
    # 班级名称
    name = UniqueStr64Col()
    # 班级学生
    students = DynamicMany("Student", "school_class")


class Gender(db.Model):  # type: ignore[misc, name-defined]
    """
    性别
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "genders"
    id = IdCol()
    # 性别
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "gender")


class CertificateType(db.Model):  # type: ignore[misc, name-defined]
    """
    证件类型
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "certificate_types"
    id = IdCol()
    # 证件类型
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "certificate_type")


class EthnicGroup(db.Model):  # type: ignore[misc, name-defined]
    """
    民族
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "ethnic_groups"
    id = IdCol()
    # 民族
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "ethnic_group")


class EducationLevel(db.Model):  # type: ignore[misc, name-defined]
    """
    以前学历
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "education_levels"
    id = IdCol()
    # 学历
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "education_level")


class StudentOrigin(db.Model):  # type: ignore[misc, name-defined]
    # noinspection GrazieInspection
    """
    生源地
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "student_origins"
    id = IdCol()
    # 生源地
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "student_origin")


class StudentCategory(db.Model):  # type: ignore[misc, name-defined]
    """
    学生类别
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "student_categories"
    id = IdCol()
    # 学生类别
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "student_category")


class PoliticalStatus(db.Model):  # type: ignore[misc, name-defined]
    """
    政治面貌
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "political_statuses"
    id = IdCol()
    # 政治面貌
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "political_status")


# 户口性质
# 11.农村 12.县镇 21.城市 30.港澳台 40.外国籍
class HouseholdType(db.Model):  # type: ignore[misc, name-defined]
    """
    户口性质
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "household_types"
    id = IdCol()
    # 户口性质
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "household_type")


# 户口区域
# 11.本市 12.非本市 21.省外 22.港澳台 30.国外
class HouseholdArea(db.Model):  # type: ignore[misc, name-defined]
    """
    户口区域
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "household_areas"
    id = IdCol()
    # 户口区域
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "household_area")


class HouseholdProvince(db.Model):  # type: ignore[misc, name-defined]
    """
    户籍所在地-省
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "household_provinces"
    id = IdCol()
    # 户籍所在地-省
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "household_province")
    # 户籍所在地-市
    household_cities = DynamicMany("HouseholdCity", "household_province")


class HouseholdCity(db.Model):  # type: ignore[misc, name-defined]
    """
    户籍所在地-市
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "household_cities"
    id = IdCol()
    # 户籍所在地-市
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "household_city")
    # 户籍所在地-省
    household_province, household_province_id = BelongsTo(HouseholdProvince, "household_cities", foreign_key=".id")
    # 户籍所在地-县
    household_counties = DynamicMany("HouseholdCounty", "household_city")


class HouseholdCounty(db.Model):  # type: ignore[misc, name-defined]
    """
    户籍所在地-县
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "household_counties"
    id = IdCol()
    # 户籍所在地-县
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "household_county")
    # 户籍所在地-市
    household_city, household_city_id = BelongsTo(HouseholdCity, "household_counties", foreign_key=".id")


class EnrollmentQuarter(db.Model):  # type: ignore[misc, name-defined]
    """
    招生季度
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "enrollment_quarters"
    id = IdCol()
    # 招生季度
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "enrollment_quarter")


class TrainingLevel(db.Model):  # type: ignore[misc, name-defined]
    """
    培养层次
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "training_levels"
    id = IdCol()
    # 培养层次
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "training_level")


class EducationSystem(db.Model):  # type: ignore[misc, name-defined]
    """
    学制
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "education_systems"
    id = IdCol()
    # 学制
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "education_system")


class StudentStatus(db.Model):  # type: ignore[misc, name-defined]
    """
    学生状态
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "student_statuses"
    id = IdCol()
    # 学生状态
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "student_status")


class StudyType(db.Model):  # type: ignore[misc, name-defined]
    """
    学习形式
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "study_types"
    id = IdCol()
    # 学习形式
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "study_type")


class Student(db.Model):  # type: ignore[misc, name-defined]
    """
    学生信息
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "students"
    id = IdCol()
    # 办学点名称
    campus_name = Str64Col()
    # 班级
    # 第一个参数为模型时类，外键应为'.'开头的相对外键，省略表名
    school_class, school_class_id = BelongsTo(SchoolClass, "students", foreign_key=".id")
    # 学号
    student_id = UniqueStr64Col()
    # 证件类型
    certificate_type, certificate_type_id = BelongsTo(CertificateType, "students", foreign_key=".id")
    # 证件号码 之所以不用Unique是因为我不确定证件类型不同的情况下证件号码会不会是全局唯一的
    certificate_number = Str64Col()
    # 姓名
    name = Str64Col()
    # 性别
    gender, gender_id = BelongsTo(Gender, "students", foreign_key=".id")
    # 出生日期 YYYY-MM-DD
    birthday = DateCol()
    # 民族
    ethnic_group, ethnic_group_id = BelongsTo(EthnicGroup, "students", foreign_key=".id")
    # 联系电话
    phone = Str64Col()
    # 开户银行名称
    bank_name = NullableStr64Col()
    # 银行卡号
    bank_account = NullableStr64Col()
    # 以前学历
    education_level, education_level_id = BelongsTo(EducationLevel, "students", foreign_key=".id")
    # 生源地
    student_origin, student_origin_id = BelongsTo(StudentOrigin, "students", foreign_key=".id")
    # 学生类别
    student_category, student_category_id = BelongsTo(StudentCategory, "students", foreign_key=".id")
    # 政治面貌
    political_status, political_status_id = BelongsTo(PoliticalStatus, "students", foreign_key=".id")
    # 户口性质
    household_type, household_type_id = BelongsTo(HouseholdType, "students", foreign_key=".id")
    # 户口区域
    household_area, household_area_id = BelongsTo(HouseholdArea, "students", foreign_key=".id")
    # 户籍所在地 保留，精确到户的完整地址
    household_address = Str64Col()
    # 户籍所在地-省
    household_province, household_province_id = BelongsTo(HouseholdProvince, "students", foreign_key=".id")
    # 户籍所在地-市
    household_city, household_city_id = BelongsTo(HouseholdCity, "students", foreign_key=".id")
    # 户籍所在地-县
    household_county, household_county_id = BelongsTo(HouseholdCounty, "students", foreign_key=".id")
    # 是否三侨生
    is_overseas_chinese = NullableBoolCol()
    # 招生年份
    admission_year = IntCol()
    # 招生季度
    enrollment_quarter, enrollment_quarter_id = BelongsTo(EnrollmentQuarter, "students", foreign_key=".id")
    # (所学)专业(的)代码
    major_code = Str64Col()
    # 培养层次
    training_level, training_level_id = BelongsTo(TrainingLevel, "students", foreign_key=".id")
    # 学制
    education_system, education_system_id = BelongsTo(EducationSystem, "students", foreign_key=".id")
    # 入学时间 YYYY-MM-DD
    admission_time = DateCol()
    # 学生状态
    student_status, student_status_id = BelongsTo(StudentStatus, "students", foreign_key=".id")
    # 学习形式
    study_type, study_type_id = BelongsTo(StudyType, "students", foreign_key=".id")
