import browser_cookie3
import requests
import shutil
import os
from tqdm.auto import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup

cj = browser_cookie3.edge()


def extract_rows(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as file:
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(file, "html.parser")

        # Find the table with id "searchresults_table"
        table = soup.find("table", {"id": "searchresults_table"})

        if table:
            # Find the tbody inside the table
            tbody = table.find("tbody")

            if tbody:
                # Extract all tr elements in the tbody
                tr_elements = tbody.find_all("tr")

                return tr_elements
            else:
                print(f"No tbody found in {html_file_path}")
        else:
            print(f"No table with id 'searchresults_table' found in {html_file_path}")

    return []


def process_html_files(folder_path, output_file_path):
    with open(output_file_path, "w", encoding="utf-8") as output_file:
        # Write the HTML header and the opening tag for the tbody
        output_file.write("<html><body><table><tbody>")

        # Iterate through all HTML files in the folder
        for filename in os.listdir(folder_path):
            if filename.endswith(".html"):
                html_file_path = os.path.join(folder_path, filename)

                # Extract rows from the current HTML file
                rows = extract_rows(html_file_path)

                # Write each tr element to the output file
                for row in rows:
                    output_file.write(str(row))

        # Write the closing tags for tbody and html
        output_file.write("</tbody></table></body></html>")


def convert_html_to_link(html_element):
    # Parse the HTML element with BeautifulSoup
    soup = BeautifulSoup(html_element, "html.parser")

    # Extract relevant information from the HTML
    concert_id = soup.find("td", {"class": "sorting_1"}).text.strip()
    track_number = soup.find_all("td")[1].text.strip()
    title = soup.find_all("td")[2].text.strip()
    ragam = soup.find_all("td")[3].text.strip()
    composer = soup.find_all("td")[4].text.strip()
    artist = soup.find_all("td")[5].text.strip()

    # Extract the href attribute from the <a> tag
    href = soup.find("a")["href"]

    # Extract the file name from the href attribute
    if "tvg" in href:
        file_name = href[href.find("tvg") :]

        # Construct the final link
        final_link = f"https://www.sangeethamshare.org/fstream.php?file=/home/data/www.sangeethamshare.org/public_html/{file_name}/{int(track_number):02d}-{title.replace(' ', '_')}-{ragam}.mp3"

        return final_link
    else:
        return None


def download_file(url, root_des_path="./"):
    fn = url.split("/")[-2] + "_" + url.split("/")[-1]
    local_filename = os.path.join(root_des_path, fn)
    downloaded = os.listdir(root_des_path)
    with requests.get(url, cookies=cj, stream=True) as r:
        total_length = int(r.headers.get("content-length"))
        if fn in downloaded:
            return "done"
        if total_length < 1000:
            return "error" + r.text
        with open(local_filename, "wb") as f:
            for chunk in tqdm(
                r.iter_content(chunk_size=1024),
                total=(total_length / 1024) + 1,
                desc=local_filename,
            ):
                if chunk:
                    f.write(chunk)
                    f.flush()
    return local_filename


def extract_links_from_html(html_content):
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the table with id "searchresults_table"
    table = soup.find("table")

    # Check if the table is found
    if table:
        # Iterate through each row in the table
        rows = table.find("tbody").find_all("tr")
        links = []
        for row in rows:
            link = convert_html_to_link(str(row))
            if link:
                links.append(link)
        return links
    else:
        print("Table with not found.")
        return []


def process_html_file(file_path, output_folder):
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    links = extract_links_from_html(html_content)

    done = 0
    error = 0
    success = 0

    with ThreadPoolExecutor() as executor:
        for out in tqdm(
            as_completed(
                [executor.submit(download_file, link, output_folder) for link in links]
            ),
            total=len(links),
        ):
            if out.result() == "done":
                done += 1
            elif out.result().startswith("error"):
                error += 1
            else:
                success += 1

    print(f"Done: {done}, Error: {error}, Success: {success}")
