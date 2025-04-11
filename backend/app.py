# CSE-5010 Term Project
# K-Means kullanarak bir veri setini işleyip sonuçlarını görselleştireceğiz.
# Ramazan, Tunahan,Emre ve Batuhan

from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
CORS(app)  # CORS için gerekli.Not:  localhost değil de 127.0.0.1 olarak çağrılmalı fronttan.

@app.route('/kmeans', methods=['GET'])
def kmeans_cluster():
    # CSV dosyasını oku
    # ID,Gender,Ever_Married,Age,Graduated,Profession,Work_Experience,Spending_Score,Family_Size,Var_1
    df = pd.read_csv('dataset.csv')  # CSV dosyanızın yolunu buraya yazın
    
    # CSV de bozuk datalar varsa (Nan) onları temizleyelim.
    df = df.dropna()

    # Veri temizliği ve encoding yapalım gerekli alanlar için.
    df['Spending_Score'] = LabelEncoder().fit_transform(df['Spending_Score'])

    # Özelliklerinizi belirleyin (örneğin: 'Age', 'Work_Experience', 'Spending_Score')
    features = ['Age', 'Work_Experience', 'Spending_Score']
    X = df[features]

    # KMeans modelini oluşturalım
    kmeans = KMeans(n_clusters=2, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X)

    # Sonuçları JSON formatında döndürelim
    result = [
        {
            "x": row['Age'],
            "y": row['Work_Experience'],
            "cluster": int(row['Cluster'])
        } for _, row in df.iterrows()
    ]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
