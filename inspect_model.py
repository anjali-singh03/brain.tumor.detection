import tensorflow as tf
model = tf.keras.models.load_model('model.keras')
model.summary()
for layer in model.layers:
    print(layer.name, layer.__class__.__name__)
