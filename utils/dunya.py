import os
import requests
import requests.adapters
import os
import concurrent.futures
from clint.textui import progress
from pydub import AudioSegment
import pandas as pd
from tqdm import tqdm

session = requests.Session()
session.mount("http://", requests.adapters.HTTPAdapter(max_retries=5))
session.mount("https://", requests.adapters.HTTPAdapter(max_retries=5))

raagas = {
    "todi": "a9413dff-91d1-4e29-ad92-c04019dce5b8",
    "dhanyaasi": "5ce23030-f71d-4f5d-9d76-f91c2c182392",
    "saaveri": "a47e9d22-847a-46e8-b589-2a3537789f5f",
    "bhairavi": "123b09bd-9901-4e64-a65a-10b02c9e0597",
    "hindolam": "26553105-ee8c-4c90-aabf-18f16e37d603",
    "kharaharapriya": "f972db4d-5d16-4f9a-9841-f313e1601aaa",
    "aanandabhairavi": "e18fcaa7-1f9c-4f09-b627-0687481f4ec7",
    "kaanada": "9a071e54-3eed-48b2-83a3-1a3fd683b8e0",
    "kaapi": "09c179f3-8b19-4792-a852-e9fa0090e409",
    "madhyamaavati": "18b1acb9-dff6-47ec-873a-b2086c8d268d",
    "athaanaa": "6345e8fe-7061-4bdc-842c-dcfd4a379820",
    "shankaraabharanam": "a2f9f182-0ceb-4531-b286-b840b47a54b8",
    "neelaambari": "b4cd8c41-994c-4c03-af33-8a5b2c227c9c",
    "varaali": "e8a0bf54-13c6-4a09-922a-bfc744ddf38a",
    "pantuvaraali": "85ccf631-4cdf-4f6c-a841-0edfcf4255d1",
    "poorvikalyaani": "b6989a44-e85d-43cf-8b95-2eae5dcd28a2",
    "shanmukhapriya": "0277eae5-3411-4b22-9fa8-1b347e7528d1",
    "hamsanaadam": "d99b1d3c-36d0-41d2-8303-59ede6da7b78",
    "kalyaani": "bf4662d4-25c3-4cad-9249-4de2dc513c06",
    "mohanam": "39821826-3327-41d7-9cd5-e22fe7b08360",
}
TOKEN = "3fbbdb93b8dad5b33d356d01fb6e9325abf3bd19"
mapping_csv_path = "./data/raaga_mapping.csv"
input_dir = "./data/dunya"
output_dir = "./data/split_audio"
metadata_csv_path = "./data/split_audio_metadata.csv"


def get_recs_by_raaga(raagaid, token):
    url = "http://dunya.compmusic.upf.edu/api/carnatic/raaga/" + raagaid
    headers = {"Authorization": "Token %s" % token}
    json = session.get(url, headers=headers).json()
    return json["recordings"]


def download_dunya_mp3(recordingid, name, location, token):
    """Download the mp3 of a document and save it to the specificed directory.

    :param recordingid: The MBID of the recording
    :param location: Where to save the mp3 to

    """
    print("Downloading", name)
    if not os.path.exists(location):
        raise Exception("Location %s doesn't exist; can't save" % location)
    headers = {"Authorization": "Token %s" % token}
    url = "http://dunya.compmusic.upf.edu/document/by-id/" + recordingid + "/mp3"
    r = session.get(url, headers=headers, stream=True)
    path = os.path.join(location, name + ".mp3")
    with open(path, "wb") as f:
        total_length = int(r.headers.get("content-length"))
        for chunk in progress.bar(
            r.iter_content(chunk_size=1024), expected_size=(total_length / 1024) + 1
        ):
            if chunk:
                f.write(chunk)
                f.flush()
    print(name, "downloaded")
    return name


def download_all_recordings(raagas, token):
    output_dir = (
        "./data/dunya/"  # Specify the directory where you want to save the recordings
    )

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_raaga = {
            executor.submit(get_recs_by_raaga, raaga_id, token): raaga_name
            for raaga_name, raaga_id in raagas.items()
        }

        for future in concurrent.futures.as_completed(future_to_raaga):
            raaga_name = future_to_raaga[future]
            try:
                recordings = future.result()
                if not recordings:
                    print(f"No recordings found for {raaga_name}")

                    continue

                # Create a subdirectory for each raaga
                raaga_dir = os.path.join(output_dir, raaga_name)
                os.makedirs(raaga_dir, exist_ok=True)

                # Download the recordings in parallel
                download_futures = [
                    executor.submit(
                        download_recording, raaga_name, recording, output_dir, token
                    )
                    for recording in recordings
                ]

                # Wait for all download tasks to complete
                concurrent.futures.wait(download_futures)

            except Exception as e:
                print(f"An error occurred for {raaga_name}: {str(e)}")

    print("All recordings downloaded successfully!")


def download_recording(raaga_name, recording, output_dir, token):
    recording_id = recording["mbid"]
    recording_title = recording["title"]
    raaga_dir = os.path.join(output_dir, raaga_name)

    download_dunya_mp3(recording_id, recording_title, raaga_dir, token)


# Function to label raagas with numbers and save the mapping as CSV
def label_raagas(raagas, mapping_csv_path):
    raaga_labels = {raaga_name: i for i, raaga_name in enumerate(raagas.keys())}
    df = pd.DataFrame(list(raaga_labels.items()), columns=["RaagaName", "RaagaNumber"])
    df.to_csv(mapping_csv_path, index=False)
    return raaga_labels


def split_audio_files(raagas, input_dir, output_dir, raaga_labels, metadata_csv_path):
    data = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_raagas = [
            executor.submit(
                split_audio_directory,
                input_dir,
                output_dir,
                raaga_labels,
                raaga_name,
                metadata_csv_path,
            )
            for raaga_name in raagas.keys()
        ]

        concurrent.futures.wait(future_raagas)

    for d in future_raagas:
        data += d.result()

    df = pd.DataFrame(data, columns=["AudioPath", "RaagaNumber"])
    df.to_csv(metadata_csv_path, index=False)


def split_audio_directory(
    input_dir, output_dir, raaga_labels, raaga_name, metadata_csv_path
):
    data = []
    raaga_dir = os.path.join(input_dir, raaga_name)

    for root, dirs, files in os.walk(raaga_dir):
        for file in tqdm(files, f"Processing {raaga_name}"):
            if file.endswith(".mp3"):
                audio_path = os.path.join(root, file)

                try:
                    audio = AudioSegment.from_mp3(audio_path)
                except Exception as e:
                    print(f"Error reading {audio_path}: {str(e)}")
                    continue  # Skip this file if an error occurs

                chunk_length_ms = 30 * 1000  # 30 seconds in milliseconds

                for i, start_time in enumerate(range(0, len(audio), chunk_length_ms)):
                    chunk = audio[start_time : start_time + chunk_length_ms]
                    chunk_filename = f"{raaga_name}_{file}_{i}.mp3"
                    chunk_path = os.path.join(output_dir, chunk_filename)
                    chunk.export(chunk_path, format="mp3")
                    data.append(
                        [
                            os.path.relpath(chunk_path, metadata_csv_path),
                            raaga_labels[raaga_name],
                        ]
                    )
    return data
