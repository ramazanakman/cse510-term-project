// PredictForm.jsx
import React, { useState } from 'react';
import axios from 'axios';

export default function PredictForm() {
  const [form, setForm] = useState({
    Gender: '',
    Ever_Married: '',
    Age: '',
    Graduated: '',
    Profession: '',
    Work_Experience: '',
    Spending_Score: '',
    Family_Size: '',
  });
  const [prediction, setPrediction] = useState('');

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async e => {
    e.preventDefault();
    const res = await axios.post('http://127.0.0.1:5000/predict', form);
    setPrediction(res.data.predicted_segment);
  };

  //Gender,Ever_Married,Age,Graduated,Profession,Work_Experience,Spending_Score,Family_Size

  return (
    <form onSubmit={handleSubmit}>
      {/* Create form fields for each attribute */}
      Age:<input name="Age" onChange={handleChange} />
      Work_Experience:<input name="Work_Experience" onChange={handleChange} />
      Family_Size:<input name="Family_Size" onChange={handleChange} />
     
      <button type="submit">Predict</button>
      {prediction && <p>Predicted Car Segment: {prediction}</p>}
    </form>
  );
}
