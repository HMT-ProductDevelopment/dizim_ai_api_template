import os
from pydub import AudioSegment
import numpy as np
import joblib
import pickle
import librosa
from configs.config import Config

def convert_to_wav(file_path):
    """
    This function is to convert an audio file to .wav file
    Args:
        file_path (str): paths of audio file needed to be convert to .wav file
    Returns:
        new path of .wav file
    """
    ext = file_path.split(".")[-1]
    assert ext in [
        "mp4", "mp3", "acc"], "The current API does not support handling {} files".format(ext)

    sound = AudioSegment.from_file(file_path, ext)
    wav_file_path = ".".join(file_path.split(".")[:-1]) + ".wav"
    sound.export(wav_file_path, format="wav")

    os.remove(file_path)
    return wav_file_path

def extract(file):
    source, sr = librosa.load(file, res_type="kaiser_fast")
    stft = np.abs(librosa.stft(source))

    mfcc = librosa.feature.mfcc(y=source, sr=sr, n_mfcc=13)
    chroma = librosa.feature.chroma_stft(S=stft, sr=sr)
    mel = librosa.feature.melspectrogram(y=source, sr=sr)
    zrc = librosa.feature.zero_crossing_rate(source)

    mfcc = np.mean(mfcc, axis=1)
    chroma = np.mean(chroma, axis=1)
    mel = np.mean(mel, axis=1)
    zcr = np.mean(zrc)

    return mfcc, chroma, mel, zcr


def scale(features, name):
    scaler = joblib.load(str(Config.SCALER_PATH / f"scaler_{name}.save"))

    return scaler.transform(features.reshape(1, -1))

def predict(df):
    """
    This function is to predict class/probability.

    Args:
        df (dataFrame): include audio path and metadata information.

    Returns:
        assessment (float): class/probability

    """
    filename = df.file_path.values[0]
    mfcc, chroma, mel, zcr = extract(filename)
    zcr = scale(zcr, "zcr").reshape(-1)
    mfcc = scale(mfcc, "mfcc").reshape(-1)
    chroma = scale(chroma, "chroma").reshape(-1)
    mel = scale(mel, "mel").reshape(-1)

    x = np.concatenate([zcr, mfcc, chroma, mel], axis=0).reshape(1, -1)

    res = 0
    model_path = str(Config.MODEL_PATH)
    model_list = os.listdir(model_path)

    for name in model_list:
        model = pickle.load(open(os.path.join(model_path, name), "rb"))

        res += model.predict(x)

    return (res /len(model_list))[0]
