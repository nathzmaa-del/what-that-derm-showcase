import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os

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
}import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import os

# --- การตั้งค่าหน้าเว็บ ---
st.set_page_config(
    page_title="What's That Derm? - AI Skin Lesion Classifier",
    page_icon="🔬",
    layout="centered"
)

# --- พจนานุกรมสำหรับคลาส (เพื่อให้แสดงผลเป็นภาษาไทยสวยงาม) ---
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
    """
    โหลดโมเดล Keras จากไฟล์ที่อยู่ใน Repository เดียวกัน
    นี่คือวิธีที่เสถียรที่สุดสำหรับ Hugging Face Spaces
    """
    model_path = 'best_resnet_model.keras'
    try:
        # ตรวจสอบว่าไฟล์มีอยู่จริงในตำแหน่งที่คาดหวัง
        if not os.path.exists(model_path):
            st.error(f"ไม่พบไฟล์โมเดลที่ '{model_path}'. โปรดตรวจสอบว่าคุณได้อัปโหลดไฟล์ขึ้น GitHub และใช้ Git LFS อย่างถูกต้อง")
            return None
        
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as e:
        st.error(f"เกิดข้อผิดพลาดในการโหลดโมเดล: {e}")
        return None

def preprocess_image(image):
    """เตรียมรูปภาพสำหรับป้อนเข้าโมเดล"""
    img = image.resize((160, 160)) # ต้องตรงกับ IMG_SIZE ตอนเทรน
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0) # สร้าง Batch dimension
    img_array = img_array / 255.0 # Normalization
    return img_array

# --- ส่วนของ UI (User Interface) ---
st.title("🔬 What's That Derm?")
st.markdown("โปรแกรมช่วยจำแนกประเภทของรอยโรคบนผิวหนังเบื้องต้นด้วย AI")
st.markdown("---")

model = load_model()

# ถ้าโหลดโมเดลสำเร็จ ถึงจะแสดงปุ่มอัปโหลด
if model is not None:
    uploaded_file = st.file_uploader(
        "อัปโหลดรูปภาพรอยโรคบนผิวหนังของคุณที่นี่",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # แสดงรูปที่อัปโหลด
        st.image(image, caption='รูปภาพที่อัปโหลด', use_column_width=True)
        
        # ทำนายผลเมื่อกดปุ่ม
        if st.button('ทำการวิเคราะห์', use_container_width=True):
            with st.spinner('AI กำลังวิเคราะห์รูปภาพ...'):
                processed_image = preprocess_image(image)
                predictions = model.predict(processed_image)
                score = tf.nn.softmax(predictions[0])
                
                # หาคลาสที่ได้คะแนนสูงสุด
                class_index = np.argmax(score)
                class_key = list(CLASS_NAMES.keys())[class_index]
                predicted_class_name = CLASS_NAMES[class_key]
                confidence = 100 * np.max(score)

            # แสดงผลลัพธ์
            st.subheader("ผลการวิเคราะห์เบื้องต้น:")
            st.success(f"**ประเภท:** {predicted_class_name}")
            st.info(f"**ความเชื่อมั่น:** {confidence:.2f}%")

            # ให้คำแนะนำเพิ่มเติมสำหรับเคสที่น่ากังวล
            if 'mel' in class_key or 'bcc' in class_key:
                 st.warning("รอยโรคนี้มีลักษณะที่อาจเข้าได้กับมะเร็งผิวหนัง **ควรปรึกษาแพทย์ผู้เชี่ยวชาญโดยเร็วที่สุด**")

st.markdown("---")
st.error(
    "**คำเตือน:** โปรแกรมนี้เป็นเพียงเครื่องมือช่วยคัดกรองเบื้องต้นเพื่อการศึกษาเท่านั้น "
    "ผลลัพธ์จาก AI **ไม่สามารถ**ใช้แทนการวินิจฉัยจากแพทย์ผู้เชี่ยวชาญได้"
)

