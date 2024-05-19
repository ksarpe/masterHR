import numpy as np
import tensorflow as tf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split

from config.constants import *

model_cp_save_path = TEST_MODEL_CP_SAVE_PATH
tflite_save_path = TEST_TFLITE_SAVE_PATH

X_dataset = np.loadtxt(DATASET_PATH, delimiter=',', dtype='float32', usecols=list(range(1, (21 * 2) + 3))) # we got coordinates of 21 points hands + 2 of nose TIP
y_dataset = np.loadtxt(DATASET_PATH, delimiter=',', dtype='int32', usecols=(0)) # we got the labels
X_train, X_test, y_train, y_test = train_test_split(X_dataset, y_dataset, train_size=0.75, random_state=RANDOM_SEED)

model = tf.keras.models.Sequential([
    tf.keras.layers.Input((21 * 2 + 2, )),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(20, activation='relu'),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(10, activation='relu'),
    tf.keras.layers.Dense(NUM_CLASSES, activation='softmax')
])

model.summary()

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'] #Accuracy for how often the model is right, Precision for how often the model is right when it says it is right
)

checkpoint = tf.keras.callbacks.ModelCheckpoint(model_cp_save_path, verbose=0, save_weights_only=False, save_best_only=True)
earlystop = tf.keras.callbacks.EarlyStopping(patience=30, verbose=0) # wait 20 epochs before stopping (val_loss check)

model.fit(
    X_train,
    y_train,
    epochs=FIT_EPOCHS,
    batch_size=FIT_BATCH_SIZE,
    validation_data=(X_test, y_test),
    callbacks=[checkpoint, earlystop]
)

val_loss, val_acc = model.evaluate(X_test, y_test, batch_size=EVAL_BATCH_SIZE)

model = tf.keras.models.load_model(model_cp_save_path)

predict_result = model.predict(np.array([X_test[0]]))
print(np.squeeze(predict_result))
print(np.argmax(np.squeeze(predict_result)))

def print_confusion_matrix(y_true, y_pred):
    labels = sorted(list(set(y_true)))
    cmx_data = confusion_matrix(y_true, y_pred, labels=labels)
    
    df_cmx = pd.DataFrame(cmx_data, index=labels, columns=labels)
 
    _, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(df_cmx, annot=True, fmt='g' ,square=False)
    ax.set_ylim(len(set(y_true)), 0)
    plt.show()
    
    print('Class Report')
    print(classification_report(y_test, y_pred))

Y_pred = model.predict(X_test)
y_pred = np.argmax(Y_pred, axis=1)

print_confusion_matrix(y_test, y_pred)

model.save(model_cp_save_path)

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

open(tflite_save_path, 'wb').write(tflite_model)
