import pandas as pd
from tqdm import tqdm
import yt_dlp

def download_yt_audio(url, filename="", output_dir="."):
    """
    Downloads audio from a YouTube video using yt_dlp library.

    Parameters:
        url (str): The URL of the YouTube video to download audio from.
        filename (str, optional): The desired filename for the downloaded audio. If not provided, the video's title will be used as the filename. Default is an empty string.
        output_dir (str, optional): The directory where the downloaded audio will be saved. Default is the current directory.

    Note:
        - The yt_dlp library should be installed to use this function.
        - The 'extract_audio' and 'format' options are set to True and 'bestaudio' respectively, for downloading the best audio format available.
        - The 'outtmpl' option is used to specify the output file name template.

    Returns:
        None: The downloaded audio file will be saved to the specified output directory with the specified filename or video title.
    """
    with yt_dlp.YoutubeDL({'extract_audio': True, 'format': 'bestaudio', 'outtmpl': f'{output_dir}/%(title)s.mp3' if filename == "" else f'{output_dir}/{filename}.mp3'}) as video:
        info_dict = video.extract_info(url, download = True)

def download_audio_from_csv(csv_file, output_dir=".", link_column="link", fn_column="id"):
    """
    Downloads audio from YouTube videos listed in a CSV file using yt_dlp library.

    Parameters:
        csv_file (str): The path to the CSV file containing YouTube video links and desired filenames.
        output_dir (str, optional): The directory where the downloaded audio files will be saved. Default is the current directory.
        link_column (str, optional): The name of the column in the CSV file that contains YouTube video links. Default is "link".
        fn_column (str, optional): The name of the column in the CSV file that contains the desired filenames for the downloaded audio. Default is "id".

    Note:
        - The yt_dlp library should be installed to use this function.
        - The CSV file should contain at least the link_column and fn_column headers.

    Returns:
        None: The downloaded audio files will be saved to the specified output directory using the specified filenames or video titles from the CSV file.
    """
    df = pd.read_csv(csv_file)
    for index, row in tqdm(df.iterrows()):
        download_yt_audio(row[link_column], row[fn_column], output_dir)

