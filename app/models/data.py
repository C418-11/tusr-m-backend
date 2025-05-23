# -*- coding: utf-8 -*-


from ..model_utils import BaseModel
from ..model_utils import BelongsTo
from ..model_utils import BoolCol
from ..model_utils import DateCol
from ..model_utils import DynamicMany
from ..model_utils import ForeignKeyCol
from ..model_utils import IdCol
from ..model_utils import IntCol
from ..model_utils import NullableBelongsTo
from ..model_utils import NullableBoolCol
from ..model_utils import NullableDateCol
from ..model_utils import NullableFloatCol
from ..model_utils import NullableStr128Col
from ..model_utils import NullableStr256Col
from ..model_utils import NullableStr64Col
from ..model_utils import Str128Col
from ..model_utils import Str256Col
from ..model_utils import Str32Col
from ..model_utils import Str64Col
from ..model_utils import UniqueStr64Col


class SchoolClass(BaseModel):
    """
    班级
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "classes"
    __editable__ = True
    id = IdCol()
    # 班级名称
    name = UniqueStr64Col()
    # 班级学生
    students = DynamicMany("Student", "school_class")


class Gender(BaseModel):
    """
    性别
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "genders"
    __editable__ = False
    id = IdCol()
    # 性别
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "gender")


class CertificateType(BaseModel):
    """
    证件类型
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "certificate_types"
    __editable__ = False
    id = IdCol()
    # 证件类型
    name = UniqueStr64Col()


class EthnicGroup(BaseModel):
    """
    民族
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "ethnic_groups"
    __editable__ = False
    id = IdCol()
    # 民族
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "ethnic_group")


class PreviousEducationLevel(BaseModel):
    """
    以前学历
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "previous_education_levels"
    __editable__ = False
    id = IdCol()
    # 学历
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "previous_education_level")


class StudentOrigin(BaseModel):
    # noinspection GrazieInspection
    """
    生源地
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "student_origins"
    __editable__ = False
    id = IdCol()
    # 生源地
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "student_origin")


class StudentCategory(BaseModel):
    """
    学生类别
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "student_categories"
    __editable__ = False
    id = IdCol()
    # 学生类别
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "student_category")


class PoliticalStatus(BaseModel):
    """
    政治面貌
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "political_statuses"
    __editable__ = False
    id = IdCol()
    # 政治面貌
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "political_status")


class HouseholdType(BaseModel):
    """
    户口性质
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "household_types"
    __editable__ = False
    id = IdCol()
    # 户口性质
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "household_type")


class HouseholdArea(BaseModel):
    """
    户口区域
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "household_areas"
    __editable__ = False
    id = IdCol()
    # 户口区域
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "household_area")


class HouseholdProvince(BaseModel):
    """
    户籍所在地-省
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "household_provinces"
    __editable__ = True
    id = IdCol()
    # 户籍所在地-省
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "household_province")
    # 户籍所在地-市
    household_cities = DynamicMany("HouseholdCity", "household_province")


class HouseholdCity(BaseModel):
    """
    户籍所在地-市
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "household_cities"
    __editable__ = True
    id = IdCol()
    # 户籍所在地-市
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "household_city")
    # 户籍所在地-省
    household_province, household_province_id = BelongsTo(HouseholdProvince, "household_cities")
    # 户籍所在地-县
    household_counties = DynamicMany("HouseholdCounty", "household_city")


class HouseholdCounty(BaseModel):
    """
    户籍所在地-县
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "household_counties"
    __editable__ = True
    id = IdCol()
    # 户籍所在地-县
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "household_county")
    # 户籍所在地-市
    household_city, household_city_id = BelongsTo(HouseholdCity, "household_counties")


class EnrollmentQuarter(BaseModel):
    """
    招生季度
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "enrollment_quarters"
    __editable__ = False
    id = IdCol()
    # 招生季度
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "enrollment_quarter")


class TrainingLevel(BaseModel):
    """
    培养层次
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "training_levels"
    __editable__ = False
    id = IdCol()
    # 培养层次
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "training_level")


class EducationSystem(BaseModel):
    """
    学制
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "education_systems"
    __editable__ = False
    id = IdCol()
    # 学制
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "education_system")


class StudentStatus(BaseModel):
    """
    学生状态
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "student_statuses"
    __editable__ = False
    id = IdCol()
    # 学生状态
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "student_status")


class StudyMode(BaseModel):
    """
    学习形式
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "study_modes"
    __editable__ = False
    id = IdCol()
    # 学习形式
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "study_mode")


class OriginalRank(BaseModel):
    """
    原军衔
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "original_ranks"
    __editable__ = False
    id = IdCol()
    # 原军衔
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "original_rank")


class RetireType(BaseModel):
    """
    退役方式
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "retire_types"
    __editable__ = False
    id = IdCol()
    # 退役方式
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "retire_type")


class HealthStatus(BaseModel):
    """
    健康状况
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "health_statuses"
    __editable__ = False
    id = IdCol()
    # 健康状况
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "health_status")


class FinancialAidType(BaseModel):
    """
    资助申请类型
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "financial_aid_types"
    __editable__ = False
    id = IdCol()
    # 资助申请类型
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "financial_aid_type")


class Nationality(BaseModel):
    """
    国籍
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "nationalities"
    __editable__ = False
    id = IdCol()
    # 国籍
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "nationality")


class FamilyDifficultyType(BaseModel):
    """
    家庭困难类型
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "family_difficulty_types"
    __editable__ = False
    id = IdCol()
    # 家庭困难类型
    name = UniqueStr64Col()
    # 学生
    students = DynamicMany("Student", "family_difficulty_type")


class Student(BaseModel):
    """
    学生信息
    """
    # noinspection SpellCheckingInspection
    __tablename__ = "students"
    __editable__ = True
    id = IdCol()
    # 办学点名称
    campus_name = Str64Col()
    # 班级
    # 第一个参数为模型时类，外键应为'.'开头的相对外键，省略表名
    school_class, school_class_id = BelongsTo(SchoolClass, "students")
    # 学号
    student_id = UniqueStr64Col()
    # 证件类型
    certificate_type_id = ForeignKeyCol(CertificateType)
    # 证件号码 之所以不用Unique是因为我不确定证件类型不同的情况下证件号码会不会是全局唯一的
    certificate_number = Str64Col()
    # 姓名
    name = Str128Col()
    # 性别
    gender, gender_id = BelongsTo(Gender, "students")
    # 出生日期 YYYY-MM-DD
    birthday = DateCol()
    # 民族
    ethnic_group, ethnic_group_id = BelongsTo(EthnicGroup, "students")
    # 联系电话
    phone = Str64Col()
    # 开户银行名称
    bank_name = NullableStr64Col()
    # 银行卡号
    bank_account = NullableStr64Col()
    # 以前学历
    previous_education_level, previous_education_level_id = BelongsTo(PreviousEducationLevel, "students")
    # 生源地
    student_origin, student_origin_id = BelongsTo(StudentOrigin, "students")
    # 学生类别
    student_category, student_category_id = BelongsTo(StudentCategory, "students")
    # 政治面貌
    political_status, political_status_id = BelongsTo(PoliticalStatus, "students")
    # 户口性质
    household_type, household_type_id = BelongsTo(HouseholdType, "students")
    # 户口区域
    household_area, household_area_id = BelongsTo(HouseholdArea, "students")
    # 户籍所在地 保留，精确到户的完整地址
    household_address = Str256Col()
    # 户籍所在地-省
    household_province, household_province_id = BelongsTo(HouseholdProvince, "students")
    # 户籍所在地-市
    household_city, household_city_id = BelongsTo(HouseholdCity, "students")
    # 户籍所在地-县
    household_county, household_county_id = BelongsTo(HouseholdCounty, "students")
    # 是否三侨生
    is_overseas_chinese = NullableBoolCol()
    # 招生年份
    admission_year = IntCol()
    # 招生季度
    enrollment_quarter, enrollment_quarter_id = BelongsTo(EnrollmentQuarter, "students")
    # (所学)专业(的)代码
    major_code = Str64Col()
    # 培养层次
    training_level, training_level_id = BelongsTo(TrainingLevel, "students")
    # 学制
    education_system, education_system_id = BelongsTo(EducationSystem, "students")
    # 入学时间 YYYY-MM-DD
    admission_time = DateCol()
    # 学生状态
    student_status, student_status_id = BelongsTo(StudentStatus, "students")
    # 学习形式
    study_mode, study_mode_id = BelongsTo(StudyMode, "students")
    # 家庭联系人姓名
    family_contact_name = Str64Col()
    # 家庭联系人电话
    family_contact_phone = Str64Col()
    # 家庭地址
    family_address = Str256Col()
    # 邮编
    postal_code = Str32Col()
    # 兴趣爱好
    hobby = NullableStr256Col()
    # 获奖情况
    award_situation = NullableStr256Col()
    # 原部队
    old_army = NullableStr64Col()
    # 原军衔
    original_rank, original_rank_id = NullableBelongsTo(OriginalRank, "students")
    # 入伍地
    military_base = NullableStr256Col()
    # 入伍时间
    enlistment_time = NullableDateCol()
    # 退伍时间
    retirement_time = NullableDateCol()
    # 退役方式
    retire_type, retire_type_id = NullableBelongsTo(RetireType, "students")
    # 健康状况
    health_status, health_status_id = NullableBelongsTo(HealthStatus, "students")
    # 全国学籍号
    national_student_id = NullableStr128Col()
    # 是否广东技校毕业
    is_guangdong_technical_school_graduation = BoolCol()
    # 毕业学校
    graduation_school = Str64Col()
    # 入学前毕业证号
    graduation_certificate_number = Str64Col()
    # 入学前毕业专业
    graduation_major = NullableStr64Col()
    # 入学前技能水平
    graduation_skill_level = NullableStr64Col()
    # 文科综合分
    comprehensive_score = NullableFloatCol()
    # 理科综合分
    science_score = NullableFloatCol()
    # 家庭年总收入（元） 源文档没详细说明，权且当成是整数罢
    family_annual_income = IntCol()
    # 家庭人均收入（元）
    family_per_capita_income = IntCol()
    # 家庭经济来源
    family_income_source = Str64Col()
    # 是否10万以下民族
    is_ethnic_minority_below_100k = BoolCol()
    # 是否低保
    is_low_income = BoolCol()
    # 资助申请类型
    financial_aid_type, financial_aid_type_id = BelongsTo(FinancialAidType, "students")
    # 是否建档立卡
    is_poor_households = BoolCol()
    # 父亲姓名
    father_name = Str128Col()
    # 父亲身份证件类别
    father_certificate_type_id = ForeignKeyCol(CertificateType)
    # 父亲身份证号
    father_certificate_number = Str64Col()
    # 母亲姓名
    mother_name = Str128Col()
    # 母亲身份证件类别
    mother_certificate_type_id = ForeignKeyCol(CertificateType)
    # 母亲身份证号
    mother_certificate_number = Str64Col()
    # 其他监护人证件类型
    guardian_certificate_type_id = ForeignKeyCol(CertificateType)
    # 其他监护人身份证号
    guardian_certificate_number = Str64Col()
    # 其他监护人姓名
    guardian_name = Str128Col()
    # 其他监护人联系方式
    guardian_contact = Str64Col()
    # 备注1-5
    remark1 = NullableStr128Col()
    remark2 = NullableStr128Col()
    remark3 = NullableStr128Col()
    remark4 = NullableStr128Col()
    remark5 = NullableStr128Col()
    # todo repeated field
    # 国系统学籍号
    # national_student_id = Str64Col()
    # 国籍
    nationality, nationality_id = BelongsTo(Nationality, "students")
    # 是否家庭困难
    is_family_difficulty = BoolCol()
    # 家庭困难类型
    family_difficulty_type, family_difficulty_type_id = BelongsTo(FamilyDifficultyType, "students")
    # 社保卡号
    social_security_card_number = NullableStr64Col()
    # 缴费金额
    payment_amount = NullableFloatCol()
    # 缴费收款收据单号
    payment_receipt_number = NullableStr64Col()


TABLES = [
    SchoolClass,
    Gender,
    CertificateType,
    EthnicGroup,
    PreviousEducationLevel,
    StudentOrigin,
    StudentCategory,
    PoliticalStatus,
    HouseholdType,
    HouseholdArea,
    HouseholdProvince,
    HouseholdCity,
    HouseholdCounty,
    EnrollmentQuarter,
    TrainingLevel,
    EducationSystem,
    StudentStatus,
    StudyMode,
    OriginalRank,
    RetireType,
    HealthStatus,
    FinancialAidType,
    Nationality,
    FamilyDifficultyType,
    Student,
]
EDITABLE_TABLE_NAMES = [table.__tablename__ for table in TABLES if table.__editable__]
