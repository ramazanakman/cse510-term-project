import React, { useEffect, useState } from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts';
import axios from 'axios';
import PredictForm from './PredictForm';

function App() {
  const [data, setData] = useState([]);
  const [decisions, setDecisions] = useState([]);

  useEffect(() => {
    
    // Flask Api ile hazırladığımız backend i çağırıyoruz. 
    // K-means algoritması orada çalıştırılıyor. 
    axios.get('http://127.0.0.1:5000/kmeans')
    .then(response => {
      // Okunan dataları state e alalım.
      setData(response.data);
      // Sonuçlardan bir karar listesi oluşturalım.
      generateDecisions(response.data);
    })
    .catch(error => {
      console.error('Data çekilirken bir hata oldu!', error);
    });
  }, []);


  const generateDecisions = (data) => {
    const decisionResults = data.map((item) => {
      switch (item.cluster) {
        case 0:
          return {
            cluster: item.cluster,
            decision: 'Target with premium products and high-value marketing campaigns.'
          };
        case 1:
          return {
            cluster: item.cluster,
            decision: 'Offer loyalty programs or discounts to improve retention.'
          };
        case 2:
          return {
            cluster: item.cluster,
            decision: 'Focus on providing affordable options and improving customer service.'
          };
        default:
          return { cluster: item.cluster, decision: 'No specific decision.' };
      }
    });
    setDecisions(decisionResults);
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Müşteri Segmentasyonu (K-Means)</h2>
      <ScatterChart width={600} height={400}>
        <CartesianGrid />
        <XAxis type="number" dataKey="x" name="Age" />
        <YAxis type="number" dataKey="y" name="Var_1" />
        <Tooltip cursor={{ strokeDasharray: '3 3' }} />
        {[...new Set(data.map(d => d.cluster))].map(cluster => (
          <Scatter
            key={cluster}
            name={`Cluster ${cluster}`}
            data={data.filter(d => d.cluster === cluster)}
            fill={['#8884d8', '#82ca9d', '#ffc658'][cluster % 3]}
          />
        ))}
      </ScatterChart>

      <PredictForm />


      <h2>Decisions Based on Clusters</h2>
      <table>
        <thead>
          <tr>
            <th>Cluster</th>
            <th>Suggested Decision</th>
          </tr>
        </thead>
        <tbody>
          {decisions.map((decision, index) => (
            <tr key={index}>
              <td>{decision.cluster}</td>
              <td>{decision.decision}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;
