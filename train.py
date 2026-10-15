import os
import argparse
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.utils import class_weight
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


# 1. Fix random seeds for reproducibility
def set_seeds(seed=42):
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    tf.random.set_seed(seed)


# Constants
IMG_SIZE = (160, 160)
CLASSES = ["glioma", "meningioma", "notumor", "pituitary"]


def load_data(data_dir, img_size=IMG_SIZE):
    """Load images and labels from a directory structured with class subfolders."""
    dataset = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        labels='inferred',
        label_mode='int',
        class_names=CLASSES,
        color_mode='rgb',
        batch_size=None,
        image_size=img_size,
        shuffle=True,
        seed=42,
    )

    images = []
    labels = []
    for img, label in dataset:
        images.append(img.numpy())
        labels.append(label.numpy())

    return np.array(images, dtype=np.float32), np.array(labels, dtype=np.int32)


def build_model(input_shape=IMG_SIZE + (3,), num_classes=len(CLASSES)):
    """Build MobileNetV2 transfer learning model."""
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=input_shape,
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False  # Freeze base model initially

    inputs = tf.keras.Input(shape=input_shape)
    # Rescaling [0, 255] -> [-1, 1] as required by MobileNetV2
    x = tf.keras.layers.Rescaling(scale=1./127.5, offset=-1.0, name="rescaling")(inputs)
    x = base_model(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D(name="global_average_pooling2d")(x)
    x = tf.keras.layers.Dropout(0.5, name="dropout")(x)
    outputs = tf.keras.layers.Dense(num_classes, activation='softmax', name="dense")(x)

    model = tf.keras.Model(inputs, outputs, name="mobilenetv2_brain_tumor")
    return model, base_model


def main():
    parser = argparse.ArgumentParser(description="Train Brain Tumor Detection Model")
    parser.add_argument("--data_dir", type=str, default=None, help="Path to training dataset directory")
    parser.add_argument("--batch_size", type=int, default=32, help="Batch size for training")
    parser.add_argument("--epochs_phase1", type=int, default=10, help="Epochs for top layer training")
    parser.add_argument("--epochs_phase2", type=int, default=10, help="Epochs for fine-tuning")
    parser.add_argument("--output_model", type=str, default="improved_model.keras", help="Path to save trained model")
    args = parser.parse_args()

    set_seeds()

    if args.data_dir and os.path.isdir(args.data_dir):
        print(f"Loading real dataset from: {args.data_dir}")
        images, labels = load_data(args.data_dir, IMG_SIZE)
        print(f"Loaded {len(images)} images.")
    else:
        print("DATA_DIR not provided or not found. Using synthetic dummy data for script validation.")
        images = np.random.rand(100, IMG_SIZE[0], IMG_SIZE[1], 3).astype(np.float32) * 255.0
        labels = np.random.randint(0, len(CLASSES), 100).astype(np.int32)

    # 2. Stratified validation split
    X_train, X_val, y_train, y_val = train_test_split(
        images, labels, test_size=0.2, stratify=labels, random_state=42
    )

    # 3. Data augmentation — applied only in the training pipeline, NOT inside the model
    data_augmentation = tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.1),
        tf.keras.layers.RandomZoom(0.1),
        tf.keras.layers.RandomContrast(0.1)
    ])

    # 4. Class weights
    class_weights = class_weight.compute_class_weight(
        class_weight='balanced',
        classes=np.unique(y_train),
        y=y_train
    )
    class_weight_dict = dict(enumerate(class_weights))
    print("Class weights:", class_weight_dict)

    train_ds = (
        tf.data.Dataset.from_tensor_slices((X_train, y_train))
        .batch(args.batch_size)
        .map(lambda x, y: (data_augmentation(x, training=True), y),
             num_parallel_calls=tf.data.AUTOTUNE)
        .prefetch(tf.data.AUTOTUNE)
    )
    val_ds = (
        tf.data.Dataset.from_tensor_slices((X_val, y_val))
        .batch(args.batch_size)
        .prefetch(tf.data.AUTOTUNE)
    )

    # Build model architecture
    model, base_model = build_model(IMG_SIZE + (3,), len(CLASSES))

    # Phase 1: Train only the top layers
    print("--- Phase 1: Training top layers ---")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    model.fit(
        train_ds,
        epochs=args.epochs_phase1,
        validation_data=val_ds,
        class_weight=class_weight_dict
    )

    # Phase 2: Fine-tuning
    print("--- Phase 2: Fine-tuning base model ---")
    base_model.trainable = True
    # Freeze bottom layers, fine-tune the top 20 layers
    for layer in base_model.layers[:-20]:
        layer.trainable = False
    for layer in base_model.layers[-20:]:
        # Keep BatchNormalization in inference mode for stability
        if isinstance(layer, tf.keras.layers.BatchNormalization):
            layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    model.fit(
        train_ds,
        epochs=args.epochs_phase2,
        validation_data=val_ds,
        class_weight=class_weight_dict
    )

    # Save trained model
    model.save(args.output_model)
    print(f"Model successfully saved to {args.output_model}")

    # Evaluation
    val_preds = model.predict(X_val, batch_size=args.batch_size)
    val_pred_classes = np.argmax(val_preds, axis=1)

    # 5. Per-class report and confusion matrix
    report = classification_report(
        y_val, val_pred_classes, target_names=CLASSES, labels=list(range(len(CLASSES))), zero_division=0
    )
    with open("classification_report.txt", "w") as f:
        f.write(report)
    print("Classification report saved to classification_report.txt")

    cm = confusion_matrix(y_val, val_pred_classes, labels=list(range(len(CLASSES))))
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=CLASSES, yticklabels=CLASSES)
    plt.xlabel('Predicted')
    plt.ylabel('True')
    plt.title('Confusion Matrix')
    plt.tight_layout()
    plt.savefig('confusion_matrix.png')
    plt.close()
    print("Confusion matrix saved to confusion_matrix.png")


if __name__ == "__main__":
    main()
