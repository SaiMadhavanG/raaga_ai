import pandas as pd
from tqdm import tqdm
import yt_dlp
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from os import devnull, listdir


@contextmanager
def suppress_stdout_stderr():
    with open(devnull, "w") as fnull:
        with redirect_stderr(fnull) as err, redirect_stdout(fnull) as out:
            yield (err, out)


def download_yt_audio(url, filename="", output_dir="."):
    with yt_dlp.YoutubeDL(
        {
            "extract_audio": True,
            "format": "bestaudio",
            "outtmpl": f"{output_dir}/%(title)s.mp3"
            if filename == ""
            else f"{output_dir}/{filename}.mp3",
        }
    ) as video:
        info_dict = video.extract_info(url, download=True)


def download_audio_from_csv(
    csv_file, output_dir=".", link_column="link", fn_column="id"
):
    df = pd.read_csv(csv_file)
    for index, row in tqdm(df.iterrows(), total=df.shape[0]):
        if str(row[fn_column]) + ".mp3" in listdir(output_dir):
            continue
        with suppress_stdout_stderr():
            download_yt_audio(row[link_column], row[fn_column], output_dir)
