from copy import deepcopy
from datetime import datetime, timedelta

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from sqlalchemy import and_

from models import db, PatientData, PatientImport

# 假设你已经有了数据库连接和合适的模型定义

def _get_patient_data(export_id, username, patient_name):
    # 查询PatientImport表获取相应的记录
    patient_import = PatientImport.query.filter_by(export_id=export_id, username=username, patient_name=patient_name).first()

    if patient_import:
        # 查询PatientData表获取对应的数据
        patient_data = PatientData.query.filter(and_(PatientData.export_id==export_id, PatientData.patient_name==patient_import.patient_name)).all()

        return patient_data

    return None

def predict_trends(export_id, username, patient_name):
    # 获取数据
    patient_data = _get_patient_data(export_id, username, patient_name)

    if patient_data:
        data = pd.DataFrame([(record.ctime, record.systolic, record.diastolic, record.heartrate) for record in patient_data],
                    columns=['ctime', 'systolic', 'diastolic', 'heartrate'])
        data['ctime'] = pd.to_datetime(data['ctime'])

        # 按时间升序排序
        data.sort_values('ctime', inplace=True)
        old_data = deepcopy(data)
        old_data.set_index('ctime', inplace=True)

        # 计算时间间隔
        time_diff = data['ctime'].diff().iloc[1]

        # 调整时间间隔
        data['ctime'] = data['ctime'].shift(1) + time_diff

        # data.index = pd.to_datetime(data.index)
        # 设置时间索引并转换为具有规律频率的时间序列
        data.set_index('ctime', inplace=True)


        # 构建ARIMA模型并进行训练
        model_systolic = ARIMA(data['systolic'], order=(1, 1, 0))
        model_systolic_fit = model_systolic.fit()

        model_diastolic = ARIMA(data['diastolic'], order=(1, 1, 0))
        model_diastolic_fit = model_diastolic.fit()

        model_heart_rate = ARIMA(data['heartrate'], order=(1, 1, 0))
        model_heart_rate_fit = model_heart_rate.fit()

        # 获取当前时间
        current_time = data.index[-1]

        # 预测未来三小时的时间戳
        future_time_range = pd.date_range(start=current_time, periods=7, freq='30T')[1:]

        # 预测未来三小时的舒张压、收缩压和心率
        prediction_systolic = model_systolic_fit.predict(start=len(data), end=len(data)+5)
        prediction_diastolic = model_diastolic_fit.predict(start=len(data), end=len(data)+5)
        prediction_heart_rate = model_heart_rate_fit.predict(start=len(data), end=len(data)+5)

        # 构建预测结果的DataFrame，并设置新的时间索引
        prediction_data = pd.DataFrame({'Systolic': prediction_systolic,
                                        'Diastolic': prediction_diastolic,
                                        'HeartRate': prediction_heart_rate})
        prediction_data.index = future_time_range[:6]
        return patient_data, old_data, prediction_data

    return None

if __name__ == '__main__':
    # 调用函数获取预测结果
    export_id = 'your_export_id'
    username = 'your_username'
    predictions = predict_trends(export_id, username)

    if predictions:
        print("未来三小时的预测结果:")
        print(predictions)
    else:
        print("无法获取预测结果。")
