# -*- coding: utf-8 -*-
from collections.abc import Callable
from dataclasses import dataclass

from flask import Flask
from mypy_extensions import NamedArg

from .bp import bp


def initialize_hooks(_app: Flask) -> None:
    ...


def initialize_setup() -> None:
    from flask_sqlalchemy.model import Model

    from ...extensions import db
    from ...models.data import CertificateType
    from ...models.data import EducationLevel
    from ...models.data import EthnicGroup
    from ...models.data import Gender
    from ...models.data import StudentOrigin
    from ...models.data import StudentCategory
    from ...models.data import PoliticalStatus
    from ...models.data import HouseholdType
    from ...models.data import HouseholdArea
    from ...models.data import EnrollmentQuarter
    from ...models.data import TrainingLevel
    from ...models.data import EducationSystem
    from ...models.data import StudentStatus

    type ModelType = Callable[[NamedArg(str, "name")], Model]  # noqa: F821

    # noinspection PyPep8Naming
    ENUM_DATA = (
        ("证件类型", CertificateType, [
            "01.身份证",
            "05.军官证",
            "10.护照",
            "15.港澳台身份证",
            "20.其他",
            "25.港澳台居民居住证",
            "30.香港居民身份证",
            "35.澳门居民身份证",
            "40.台湾居民身份证",
        ]),
        ("性别", Gender, ["1.男", "2.女"]),
        ("民族", EthnicGroup, [
            "01.汉族",
            "02.蒙古族",
            "03.回族",
            "04.藏族",
            "05.维吾尔族",
            "06.苗族",
            "07.彝族",
            "08.壮族",
            "09.布依族",
            "10.朝鲜族",
            "11.满族",
            "12.侗族",
            "13.瑶族",
            "14.白族",
            "15.土家族",
            "16.哈尼族",
            "17.哈萨克族",
            "18.傣族",
            "19.黎族",
            "20.傈傈族",
            "21.佤族",
            "22.畲族",
            "23.高山族",
            "24.拉祜族",
            "25.水族",
            "26.东乡族",
            "27.纳西族",
            "28.景颇族",
            "29.柯尔克孜族",
            "30.土族",
            "31.达翰尔族",
            "32.仫佬族",
            "33.羌族",
            "34.布朗族",
            "35.撒拉族",
            "36.毛南族",
            "37.仡佬族",
            "38.锡伯族",
            "39.阿昌族",
            "40.普米族",
            "41.塔吉克族",
            "42.怒族",
            "43.乌孜别克族",
            "44.俄罗斯族",
            "45.鄂温克族",
            "46.德昂族",
            "47.保安族",
            "48.裕固族",
            "49.京族",
            "50.塔塔尔族",
            "51.独龙族",
            "52.鄂伦春族",
            "53.赫哲族",
            "54.门巴族",
            "55.珞巴族",
            "56.基诺族",
            "57.穿青人",
            "90.外籍人士"
        ]),
        ("以前学历", EducationLevel, [
            "11.博士",
            "12.硕士",
            "21.本科",
            "31.专科",
            "40.中专",
            "50.技校",
            "61.高中",
            "62.高技",
            "70.初中",
            "80.小学",
            "90.文盲或半文盲"
        ]),
        ("生源地", StudentOrigin, [
            "深圳市", "广东省内(深圳市外)", "广东省外"
        ]),
        ("学生类别", StudentCategory, [
            "01.应届毕业", "05.在职人员", "10.非在职人员", "15.退役士兵"
        ]),
        ("政治面貌", PoliticalStatus, [
            "01.中国共产党党员",
            "02.中国共产党预备党员",
            "03.中国共产主义青年团团员",
            "04.中国国民党革命委员会会员",
            "05.中国民主同盟盟员",
            "06.中国民主建国会会员",
            "07.中国民主促进会会员",
            "08.中国农工党党员",
            "09.中国致公党党员",
            "10.九三学社社员",
            "11.台湾民主自治同盟盟员",
            "12.无党派民主人士",
            "13.群众"
        ]),
        ("户口类型", HouseholdType, [
            "11.农村", "12.县镇", "21.城市", "30.港澳台", "40.外国籍"
        ]),
        ("户口所在地", HouseholdArea, [
            "11.本市", "12.非本市", "21.省外", "22.港澳台", "30.国外"
        ]),
        ("招生季度", EnrollmentQuarter, [
            "1.春季", "2.秋季"
        ]),
        ("培养层次", TrainingLevel, [
            "初级", "中级", "高级", "预备技师", "技师"
        ]),
        ("学制", EducationSystem, [
            "二年",  "三年", "四年", "五年", "六年",
        ]),
        ("学生状态", StudentStatus, [
            "01.在校", "05.休学", "10.转入", "15.转出", "20.退学", "25.复学", "30.留级", "35.开除", "40.肄业", "45.毕业", "50.结业"
        ]),
    )

    @dataclass
    class EnumData:
        name: str
        model: ModelType
        types: list[str]

    def add_enum(data: EnumData) -> None:
        for t in data.types:
            print(f"添加{data.name}： {t}")
            # noinspection PyArgumentList
            db.session.add(data.model(name=t))
            db.session.commit()

    print("正在初始化基础数据")
    for (name, model, types) in ENUM_DATA:
        print()
        add_enum(EnumData(name=name, model=model, types=types))
    print()
    print("初始化基础数据成功")


__all__ = ("bp", "initialize_hooks",)
