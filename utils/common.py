def get_blood_pressure_category(systolic, diastolic):
    """ 根据收缩压和舒张压的范围来确定血压类别
    """
    if systolic < 120 and diastolic < 80:
        return "理想血压"
    elif 120 <= systolic < 130 and diastolic < 85:
        return "正常血压"
    elif 130 <= systolic < 140 or 85 <= diastolic < 90:
        return "正常高值"
    elif 140 <= systolic < 160 or 90 <= diastolic < 100:
        return "1级高血压(轻度)"
    elif 160 <= systolic < 180 or 100 <= diastolic < 110:
        return "2级高血压(中度)"
    elif systolic >= 180 or diastolic >= 110:
        return "3级高血压(重度)"
    elif 140 <= systolic < 150 and 90 <= diastolic < 100:
        return "单纯收缩性高血压"
    else:
        if systolic < 140:
            return '正常血压'
        elif systolic < 160:
            return "1级高血压(轻度)"
        elif systolic < 180:
            return "2级高血压(中度)"
        else:
            return "3级高血压(重度)"

if __name__ == '__main__':
    print(get_blood_pressure_category(110, 70))  # 理想血压
    print(get_blood_pressure_category(125, 80))  # 正常血压
    print(get_blood_pressure_category(135, 88))  # 正常高值
    print(get_blood_pressure_category(145, 92))  # 1级高血压(轻度)
    print(get_blood_pressure_category(170, 105))  # 2级高血压(中度)
    print(get_blood_pressure_category(190, 115))  # 3级高血压(重度)
    print(get_blood_pressure_category(145, 95))  # 单纯收缩性高血压
    print(get_blood_pressure_category(120, 60))  # 其他
