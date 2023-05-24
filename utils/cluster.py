import os

import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def cluster_patient(filepath):
    # 读取数据集并进行预处理
    df = pd.read_excel(filepath)
    # 通过姓名对其他字段进行平均
    df = df.groupby('姓名').mean().reset_index()

    # 选择要用于聚类的特征
    X = df[['收缩压', '舒张压', '心率']]

    # 对数据进行标准化处理
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 创建聚类模型并进行拟合
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(X_scaled)

    # 输出每个样本所属的簇标签
    df['cluster'] = kmeans.labels_

    # 查看聚类结果
    result = df.groupby('cluster').agg({
        '年龄': 'mean',
        '身高': 'mean',
        '体重': 'mean',
        '脉压差': 'mean',
        '心率': 'mean',
        '舒张压': 'mean',
        '收缩压': 'mean',
        '姓名': 'count'
    }).reset_index()

    return df, result

