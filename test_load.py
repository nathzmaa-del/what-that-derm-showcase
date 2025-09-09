import tensorflow as tf
try:
    model = tf.keras.models.load_model('best_resnet_model.keras')
    print("Model loaded successfully locally!")
except Exception as e:
    print(f"Failed to load model locally: {e}")