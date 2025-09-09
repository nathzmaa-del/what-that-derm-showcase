import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os
from huggingface_hub import hf_hub_download

# --- การตั้งค่าหน้าเว็บ ---
st.set_page_config(
    page_title="What's That Derm? - AI Skin Lesion Classifier",
    page_icon="🔬",
    layout="centered",
    initial_sidebar_state="auto",
)

# --- พจนานุกรมสำหรับคลาส (เพื่อให้แสดงผลสวยงาม) ---
CLASS_NAMES = {
    'akiec': 'Actinic Keratoses (โรคผิวหนังอักเสบจากแสงแดด)',
    'bcc': 'Basal Cell Carcinoma (มะเร็งผิวหนังชนิดเบซัลเซลล์)',
    'bkl': 'Benign Keratosis-like Lesions (รอยโรคคล้ายหูดที่ไม่ใช่มะเร็ง)',
    'df': 'Dermatofibroma (เนื้องอกผิวหนังชนิดเดอร์มาโตไฟโบรมา)',
    'mel': 'Melanoma (มะเร็งผิวหนังชนิดเมลาโนมา)',
    'nv': 'Melanocytic Nevi (ไฝ)',
    'vasc': 'Vascular Lesions (รอยโรคของหลอดเลือด)'
}

# --- ฟังก์ชันหลัก ---

@st.cache_resource
def load_model():
    try:
        model_path = hf_hub_download(
            repo_id="Meeew/what-that-derm-showcase",   # 🔹 แก้เป็น model repo ของคุณ
            filename="best_resnet_model.keras"
        )
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการโหลดโมเดล: {e}")
        return None

def preprocess_image(image):
    """
    เตรียมรูปภาพสำหรับป้อนเข้าโมเดล
    """
    # ปรับขนาดให้ตรงกับ Input size ของโมเดล
    img = image.resize((160, 160))
    # แปลงเป็น Numpy array
    img_array = np.array(img)
    # เพิ่ม dimension สำหรับ batch
    img_array = np.expand_dims(img_array, axis=0)
    # ทำ Normalization
    img_array = img_array / 255.0
    return img_array

# --- ส่วนของ UI ---

st.title("🔬 What's That Derm?")
st.markdown("โปรแกรมช่วยจำแนกประเภทของรอยโรคบนผิวหนังเบื้องต้นด้วย AI")
st.markdown("---")

# โหลดโมเดล
model = load_model()

if model is not None:
    # สร้างปุ่มสำหรับอัปโหลดไฟล์
    uploaded_file = st.file_uploader(
        "อัปโหลดรูปภาพรอยโรคบนผิวหนังของคุณที่นี่",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        # แสดงรูปภาพ
        image = Image.open(uploaded_file)
        st.image(image, caption='รูปภาพที่อัปโหลด', use_column_width=True)

        with st.spinner('AI กำลังวิเคราะห์รูปภาพ...'):
            # เตรียมรูปภาพ
            processed_image = preprocess_image(image)

            # ทำนายผล
            predictions = model.predict(processed_image)
            score = tf.nn.softmax(predictions[0])
            
            # หาคลาสที่มีความน่าจะเป็นสูงสุด
            class_index = np.argmax(score)
            class_key = list(CLASS_NAMES.keys())[class_index]
            predicted_class_name = CLASS_NAMES[class_key]
            confidence = 100 * np.max(score)

        st.subheader("ผลการวิเคราะห์เบื้องต้น:")
        st.success(f"**ประเภท:** {predicted_class_name}")
        st.info(f"**ความเชื่อมั่น:** {confidence:.2f}%")

        # (Creative Tip) เพิ่มคำอธิบายที่เป็นประโยชน์
        if predicted_class_name == 'Melanoma':
             st.warning("รอยโรคนี้มีลักษณะที่อาจเข้าได้กับเมลาโนมา ซึ่งเป็นมะเร็งผิวหนังชนิดร้ายแรง **ควรปรึกษาแพทย์ผู้เชี่ยวชาญโดยเร็วที่สุด**")
        elif predicted_class_name == 'Basal Cell Carcinoma':
            st.warning("รอยโรคนี้มีลักษณะที่อาจเข้าได้กับมะเร็งผิวหนังชนิดเบซัลเซลล์ **ควรปรึกษาแพทย์เพื่อรับการวินิจฉัยที่ถูกต้อง**")

# (Error Prevention & Empathy) เพิ่มคำเตือนที่สำคัญ
st.markdown("---")
st.error(
    "**คำเตือน:** โปรแกรมนี้เป็นเพียงเครื่องมือช่วยคัดกรองเบื้องต้นเพื่อการศึกษาเท่านั้น "
    "ผลลัพธ์จาก AI **ไม่สามารถ**ใช้แทนการวินิจฉัยจากแพทย์ผู้เชี่ยวชาญได้ "
    "กรุณาปรึกษาแพทย์เพื่อรับการตรวจและการวินิจฉัยที่ถูกต้อง"
)
