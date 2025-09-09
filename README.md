---
title: What's That Derm?
emoji: 🔬
colorFrom: indigo
colorTo: blue
sdk: streamlit
app_file: app.py
pinned: false
---
🔬 What's That Derm? - AI Skin Lesion Classifier
[![Hugging Face Spaces](https://img.shields.io/badge/🤗%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/Meeew/what-that-derm-showcase)

โปรแกรมช่วยจำแนกประเภทของรอยโรคบนผิวหนังเบื้องต้นด้วย AI สำหรับการศึกษา สร้างขึ้นเพื่อเป็นส่วนหนึ่งของ Portfolio สำหรับยื่นสมัครเข้าศึกษาต่อในคณะแพทยศาสตร์

✨ Features
AI-Powered Classification: ใช้โมเดล Deep Learning (ResNet50V2) ในการจำแนกรอยโรคผิวหนัง 7 ประเภท

Interactive Web App: สร้างด้วย Streamlit และ Deploy บน Hugging Face Spaces ทำให้ทุกคนสามารถทดลองใช้งานได้

Focus on Medical Application: โปรเจกต์นี้แสดงให้เห็นถึงความเข้าใจในการนำเทคโนโลยี AI มาประยุกต์ใช้ในทางการแพทย์ พร้อมทั้งตระหนักถึงข้อจำกัดและความสำคัญของการวินิจฉัยโดยแพทย์ผู้เชี่ยวชาญ

🚀 Technologies Used
Backend & Model: Python, TensorFlow, Keras

Data Science Stack: Pandas, NumPy, Scikit-learn, Matplotlib

Web Framework: Streamlit

Deployment: GitHub, Git LFS, Hugging Face Spaces

🛠️ Installation & Usage
1. Clone repository นี้:

git clone [https://github.com/nathzmaa-del/what-that-derm-app.git](https://github.com/nathzmaa-del/what-that-derm-app.git)

2. ติดตั้ง Dependencies:

cd what-that-derm-app
pip install -r requirements.txt

3. รันแอปพลิเคชัน:

streamlit run app.py

📈 Model Performance
โมเดลสุดท้ายให้ผลลัพธ์ที่น่าพอใจบน Test Set โดยมีความแม่นยำโดยรวม 78.38% และค่า AUC สูงถึง 0.96 ซึ่งบ่งชี้ถึงความสามารถในการจำแนกที่ดีเยี่ยม

⚠️ Disclaimer
โปรแกรมนี้เป็นเพียงเครื่องมือช่วยคัดกรองเบื้องต้นเพื่อการศึกษาเท่านั้น ผลลัพธ์จาก AI ไม่สามารถใช้แทนการวินิจฉัยจากแพทย์ผู้เชี่ยวชาญได้ กรุณาปรึกษาแพทย์เพื่อรับการตรวจและการวินิจฉัยที่ถูกต้อง
