from flask_login import current_user

from utils.common import get_blood_pressure_category
from models import db, PatientImport

def analysis(patient_data, data, export_id):
    analysis_data = {}
    base_info = {}
    for elem in patient_data:
        name = elem.patient_name
        base_info[name] = elem


    age_avg_info = {} # 年龄对应的平均血压数据
    patient_pressure_info = {} # 患者对应的血压平均数据
    heartrate_info = {} # 心率对应的血压平均数据

    for elem in data:
        name = elem.patient_name
        heartrate = elem.heartrate
        base = base_info[name]
        age = base.age
        _temp = [elem.systolic, elem.diastolic, elem.heartrate]
        if age not in age_avg_info:
            age_avg_info[age] = [_temp, 1]
        else:
            age_avg_info[age][0] = list(map(lambda x: x[0] + x[1], zip(age_avg_info[age][0], _temp)))
            age_avg_info[age][1] += 1

        if name not in patient_pressure_info:
            patient_pressure_info[name] = [_temp, 1]
        else:
            patient_pressure_info[name][0] = list(map(lambda x: x[0] + x[1], zip(patient_pressure_info[name][0], _temp)))
            patient_pressure_info[name][1] += 1

        if heartrate not in heartrate_info:
            heartrate_info[heartrate] = [_temp, 1]
        else:
            heartrate_info[heartrate][0] = list(map(lambda x: x[0] + x[1], zip(heartrate_info[heartrate][0], _temp)))
            heartrate_info[heartrate][1] += 1

    for k, v in age_avg_info.items():
        age_avg_info[k] = tuple([round(x / v[1]) for x in v[0]])

    for k, v in heartrate_info.items():
        heartrate_info[k] = tuple([round(x / v[1]) for x in v[0]])

    normal_count = 0
    high_count = 0
    cate_info = {}
    gender_info = {}
    for k, v in patient_pressure_info.items():
        systolic, diastolic, _ = tuple([round(x / v[1]) for x in v[0]])
        cate = get_blood_pressure_category(systolic, diastolic)
        if cate in set(['理想血压', '正常血压', '正常高值']):
            normal_count += 1
        else:
            high_count += 1

        cate_info[cate] = cate_info.get(cate, 0) + 1
        patient_rec = PatientImport.query.filter_by(export_id=export_id, username=current_user.username, patient_name=k).first()
        patient_rec.cate = cate
        db.session.add(patient_rec)
        db.session.commit()

    age_avg_info = sorted([(m, v) for m, v in age_avg_info.items()], key=lambda x: x[0])
    analysis_data['age_avg_info'] = {
        'labels': [x[0] for x in age_avg_info],
        'data': [
            [round(x[1][0], 2) for x in age_avg_info],
            [round(x[1][1], 2) for x in age_avg_info],
            [round(x[1][2], 2) for x in age_avg_info],
        ],
    }

    heartrate_info = sorted([(m, v) for m, v in heartrate_info.items()], key=lambda x: x[0])
    analysis_data['heartrate_info'] = {
        'labels': [x[0] for x in heartrate_info],
        'data': [
            [round(x[1][0], 2) for x in heartrate_info],
            [round(x[1][1], 2) for x in heartrate_info],
        ],
    }
    cate_keys = list(cate_info.keys())
    analysis_data['pressure_info'] = {
        'labels': ['正常', '高血压患者'],
        'data': [round(normal_count / len(patient_data) * 100), round(high_count / len(patient_data) * 100)]
    }
    analysis_data['cate_info'] = {
        'labels': cate_keys,
        'data': [round(cate_info.get(x, 0)) for x in cate_keys]
    }

    analysis_data['patient_count'] = len(patient_data) # 患者人数
    analysis_data['sample_count'] = len(data) # 总测量数
    analysis_data['normal_count'] = normal_count # 正常患者数
    analysis_data['high_rate'] = round(high_count / len(patient_data), 2) # 高血压患者占比
    return analysis_data
    