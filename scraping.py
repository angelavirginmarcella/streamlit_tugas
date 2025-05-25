import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

# --- Koneksi ke MongoDB ---
try:
    client = MongoClient("mongodb://localhost:27017/")
    db = client["scraping_db"]
    collection = db["sektarbandung_articles"]
    print("[✓] Koneksi ke MongoDB berhasil.")
except Exception as e:
    print("[✗] Gagal konek ke MongoDB:", e)
    exit()

# --- URL target ---
url = "https://ayosehat.kemkes.go.id/kenali-gejala-stroke-dengan-segera-ke-rs"
""
response = requests.get(url)

# --- Cek jika request sukses ---
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # DEBUG: Lihat struktur HTML awal
    print("\n[DEBUG] Potongan HTML halaman:\n")
    print(soup.prettify()[:1000])  # tampilkan 1000 karakter pertama

    # --- Ambil data artikel ---
    try:
        title_tag = soup.find('h1')
        title = title_tag.text.strip() if title_tag else 'No title found'
    except:
        title = 'No title found'

    try:
        author_tag = soup.find('span', class_='author-name')
        author = author_tag.text.strip() if author_tag else 'No author found'
    except:
        author = 'No author found'

    try:
        date_tag = soup.find('time')
        date = date_tag.text.strip() if date_tag else 'No date found'
    except:
        date = 'No date found'

    try:
        article_body = soup.find('div', class_='entry-content')
        paragraphs = article_body.find_all('p') if article_body else []
        content = '\n'.join([p.text.strip() for p in paragraphs])
    except:
        content = 'No content found'

    # --- Print hasil scraping ---
    print("\n[✓] Data berhasil diambil:")
    print("Judul :", title)
    print("Penulis :", author)
    print("Tanggal :", date)
    print("Jumlah paragraf:", len(content.split('\n')))

    # --- Simpan ke MongoDB ---
    document = {
        "url": url,
        "title": title,
        "author": author,
        "date": date,
        "content": content
    }

    result = collection.insert_one(document)
    print(f"[✓] Artikel berhasil disimpan ke MongoDB! ID: {result.inserted_id}")

else:
    print("[✗] Gagal mengakses halaman:", response.status_code)