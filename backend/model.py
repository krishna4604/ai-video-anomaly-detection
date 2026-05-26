import tensorflow as tf
import os

MODEL_PATH = "models/autoencoder.h5"


def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(64, 64, 3)),

        tf.keras.layers.Conv2D(32, 3, activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D(),

        tf.keras.layers.Conv2D(64, 3, activation='relu', padding='same'),
        tf.keras.layers.MaxPooling2D(),

        tf.keras.layers.Conv2DTranspose(64, 3, strides=2, padding='same', activation='relu'),
        tf.keras.layers.Conv2DTranspose(32, 3, strides=2, padding='same', activation='relu'),

        tf.keras.layers.Conv2D(3, 3, activation='sigmoid', padding='same')
    ])

    model.compile(optimizer='adam', loss='mse')
    return model


def load_model():
    os.makedirs("models", exist_ok=True)

    if os.path.exists(MODEL_PATH):
        try:
            return tf.keras.models.load_model(MODEL_PATH)
        except:
            pass

    model = build_model()
    model.save(MODEL_PATH)
    return model


def get_score(model, frame):
    frame = tf.image.resize(frame, (64, 64)) / 255.0
    frame = tf.expand_dims(frame, axis=0)

    recon = model.predict(frame, verbose=0)
    error = tf.reduce_mean(tf.square(frame - recon))

    return float(error)