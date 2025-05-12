# CSE-5010 Term Project
# K-Means kullanarak bir veri setini işleyip sonuçlarını görselleştireceğiz.
# Ramazan, Tunahan,Emre ve Batuhan

from flask import Flask,  request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder




app = Flask(__name__)
CORS(app)  # CORS için gerekli.Not:  localhost değil de 127.0.0.1 olarak çağrılmalı fronttan.

#Decision Tree
model, columns = joblib.load('decision_tree_model.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Receive JSON from React

    # Convert to DataFrame with same column structure
    df_input = pd.DataFrame([data])
    df_input = pd.get_dummies(df_input)
    
    # Add missing columns
    for col in columns:
        if col not in df_input.columns:
            df_input[col] = 0
    df_input = df_input[columns]

    prediction = model.predict(df_input)[0]

       
    return jsonify({'predicted_segment': prediction})


#K-Means
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
    features = ['Gender','Ever_Married','Age','Graduated','Work_Experience','Spending_Score','Family_Size','Var_1']
    X = df[features]

    # KMeans modelini oluşturalım
    kmeans = KMeans(n_clusters=5, random_state=42)
    df['Cluster'] = kmeans.fit_predict(X)

   # print(df['Var_1'].value_counts())

    # Sonuçları JSON formatında döndürelim
    result = [
        {
            "x": row['Age'],
            "y": row['Var_1'],
            "cluster": int(row['Cluster'])
        } for _, row in df.iterrows()
    ]
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
