"""
Phase E - download faculty photos for the 5 CSE-family pages and verify
that the fcard <img src> paths line up with what's saved on disk.

Photo URLs were scraped from
  https://mlrit.ac.in/faculty_categories/cs-it/
  https://mlrit.ac.in/faculty_categories/it/
  https://mlrit.ac.in/faculty_categories/cse-aiml/
  https://mlrit.ac.in/faculty_categories/cse-cyber-security/
  https://mlrit.ac.in/faculty_categories/cse-ds/

Strategy: each photo is saved as images/<dept>/<roster-slug>.jpg, matching
exactly what the fcard generator wrote into the HTML. We rely on the
existing onerror="show initials" handler for any download that fails.
"""
from pathlib import Path
import re
import urllib.request
import ssl

HERE = Path(__file__).resolve().parent
IMG_ROOT = HERE / "images"

# ---- archive name → photo URL --------------------------------------------------
# Each list mirrors what was scraped, name as-given by the archive page.
# We match these against the roster (in _phase_c_*.py) by re-slugging both sides.

ARCHIVES = {
    "csit": [
        ("Dr. D.B.K. Kamesh", "https://mlrit.ac.in/wp-content/uploads/2024/06/Prof.-Kamesh-Sir.jpg"),
        ("Ms .P.Nishitha", "https://mlrit.ac.in/wp-content/uploads/2024/07/20240727_102447-e1767091692299.jpeg"),
        ("D.Rajeshwari", "https://mlrit.ac.in/wp-content/uploads/2024/07/20240727_102408.jpeg"),
        ("A.Nirisha", "https://mlrit.ac.in/wp-content/uploads/2024/07/20240727_102321-e1767160788160.jpeg"),
        ("P. Poojasree", "https://mlrit.ac.in/wp-content/uploads/2024/07/IMG-20240727-WA0001.jpg"),
        ("Rajkumar Bhookya", "https://mlrit.ac.in/wp-content/uploads/2024/07/20240727_102345.jpeg"),
        ("Devolla Manogna", "https://mlrit.ac.in/wp-content/uploads/2024/07/20240727_102224.jpeg"),
        ("S. Anudeep", "https://mlrit.ac.in/wp-content/uploads/2024/07/20240727_102154.jpeg"),
        ("Banothu Seva", "https://mlrit.ac.in/wp-content/uploads/2024/07/20240727_102524.jpeg"),
        ("Ms.Madhavi Banala", "https://mlrit.ac.in/wp-content/uploads/2024/07/20240727_102119.jpeg"),
        ("N. Thulasi Chithra", "https://mlrit.ac.in/wp-content/uploads/2022/03/Thulasichitra-Photo.jpg"),
        ("V. Srikanth", "https://mlrit.ac.in/wp-content/uploads/2023/07/Srikanth-Sir.jpeg"),
        ("T. Gandhi", "https://mlrit.ac.in/wp-content/uploads/2023/07/Gandhi.jpeg"),
        ("Mrs T. Mounika", "https://mlrit.ac.in/wp-content/uploads/2023/07/Mounika-mam.jpeg"),
        ("Mrs S.Parvathi", "https://mlrit.ac.in/wp-content/uploads/2023/07/Pravathi-mam.jpeg"),
        ("N. Sandhya", "https://mlrit.ac.in/wp-content/uploads/2023/07/Sandhya-mam.jpeg"),
        ("Mrs M.Srividya", "https://mlrit.ac.in/wp-content/uploads/2023/07/Srividya-mam.jpg"),
        ("Ms D.Neelima Priyadarshini", "https://mlrit.ac.in/wp-content/uploads/2023/07/Neelima-mam.jpg"),
        ("Ms N.Vijayasri", "https://mlrit.ac.in/wp-content/uploads/2023/07/vijayasri.jpg"),
        ("S. Navya", "https://mlrit.ac.in/wp-content/uploads/2022/03/navya.jpg"),
    ],
    "it": [
        ("Dr.N V Raja Sekhar Reddy", "https://mlrit.ac.in/wp-content/uploads/2022/02/it-fac-1.jpg"),
        ("Dr. Dhilli Rao Gorja", "https://mlrit.ac.in/wp-content/uploads/2024/05/download_200x200_50-1.jpg"),
        ("Vemuri Nitin", "https://mlrit.ac.in/wp-content/uploads/2022/03/nitin.jpg"),
        ("Mrs Shruthi Patel", "https://mlrit.ac.in/wp-content/uploads/2022/03/sruthi.jpg"),
        ("Mr D. Sandeep", "https://mlrit.ac.in/wp-content/uploads/2022/03/sandeep.jpg"),
        ("J Adilakshmi", "https://mlrit.ac.in/wp-content/uploads/2022/03/aadhilaxmi.jpg"),
        ("Bhasker Boddu", "https://mlrit.ac.in/wp-content/uploads/2022/03/bhasker.jpg"),
        ("P laxmaiah", "https://mlrit.ac.in/wp-content/uploads/2022/03/laxmiah.jpg"),
        ("B Varija", "https://mlrit.ac.in/wp-content/uploads/2022/07/varija.png"),
        ("Ms B. Sushma", "https://mlrit.ac.in/wp-content/uploads/2022/07/Shushma.jpeg"),
        ("G Sathyanarayan", "https://mlrit.ac.in/wp-content/uploads/2022/02/place-person.jpg"),
        ("Mr.Mohd Anwar Ali", "https://mlrit.ac.in/wp-content/uploads/2022/07/Anwar-Passport-photo.jpg"),
        ("M Harshini", "https://mlrit.ac.in/wp-content/uploads/2024/01/IMG_20220308_141626-scaled.jpg"),
        ("Dr. Mopur Vijaya Bhaskar Reddy", "https://mlrit.ac.in/wp-content/uploads/2024/08/VIJAY.jpeg"),
    ],
    "aiml": [
        ("Dr. Kashi Sai Prasad", "https://mlrit.ac.in/wp-content/uploads/2022/03/Sai-Prasad-e1688727445691.jpeg"),
        ("Dr. K. Varada Rajkumar", "https://mlrit.ac.in/wp-content/uploads/2023/03/Photo-dr-Varada.jpg"),
        ("Dr. Penubaka Kiran Kumar Reddy", "https://mlrit.ac.in/wp-content/uploads/2023/03/WhatsApp-Image-2025-02-22-at-2.56.26-PM.jpeg"),
        ("VS Pavan kumar", "https://mlrit.ac.in/wp-content/uploads/2025/02/WhatsApp-Image-2025-02-22-at-3.25.51-PM.jpeg"),
        ("Bidinamcherla Ammanni", "https://mlrit.ac.in/wp-content/uploads/2024/08/Ammanni.jpeg"),
        ("Dr. Sivakrishna Kondaveeti", "https://mlrit.ac.in/wp-content/uploads/2024/02/SIVAKRISHNAPHOTO-Dr-K-Shiva-Krishna-e1708756480699.jpg"),
        ("G. Sowmya", "https://mlrit.ac.in/wp-content/uploads/2022/03/Sowmya.jpeg"),
        ("Singanamala Priyanka", "https://mlrit.ac.in/wp-content/uploads/2025/03/WhatsApp-Image-2025-03-19-at-12.48.36-PM-scaled-e1743237744317.jpeg"),
        ("Pasupuleti Pavani", "https://mlrit.ac.in/wp-content/uploads/2025/02/WhatsApp-Image-2025-02-27-at-10.12.56-AM.jpeg"),
        ("Remedi Sravani", "https://mlrit.ac.in/wp-content/uploads/2025/02/WhatsApp-Image-2025-02-27-at-10.34.30-AM.jpeg"),
        ("Lakshmi Saritha", "https://mlrit.ac.in/wp-content/uploads/2025/02/WhatsApp-Image-2025-02-27-at-10.41.24-AM.jpeg"),
        ("Komari BiksheswaraRao", "https://mlrit.ac.in/wp-content/uploads/2025/02/Bishu-scaled-e1755756057635.jpeg"),
        ("E Raghavender", "https://mlrit.ac.in/wp-content/uploads/2025/02/WhatsApp-Image-2025-02-27-at-1.44.31-PM.jpeg"),
        ("Seedarla Sandhya Rani", "https://mlrit.ac.in/wp-content/uploads/2025/02/WhatsApp-Image-2025-02-22-at-3.10.07-PM.jpeg"),
        ("Shaik Gouse Pasha", "https://mlrit.ac.in/wp-content/uploads/2025/02/WhatsApp-Image-2025-02-22-at-3.18.26-PM.jpeg"),
        ("M Lakshmi Saranya", "https://mlrit.ac.in/wp-content/uploads/2025/02/WhatsApp-Image-2025-02-22-at-2.48.04-PM-scaled.jpeg"),
        ("Pottapinjara Babu", "https://mlrit.ac.in/wp-content/uploads/2024/12/Babu.jpeg"),
        ("B.Mamatha", "https://mlrit.ac.in/wp-content/uploads/2024/08/Mamatha-Passport.jpg"),
        ("T Aswani", "https://mlrit.ac.in/wp-content/uploads/2024/06/Aswani-1.jpg"),
        ("Ravi Gangadharolla", "https://mlrit.ac.in/wp-content/uploads/2024/04/RAVI-G-e1713852968237.jpg"),
        ("Pacha Swathi", "https://mlrit.ac.in/wp-content/uploads/2024/04/Pacha-Swathi-e1713852474142.jpg"),
        ("T Nagini", "https://mlrit.ac.in/wp-content/uploads/2024/04/Nagini-e1713851709952.jpeg"),
        ("H Ramanjineyulu", "https://mlrit.ac.in/wp-content/uploads/2024/02/20240224_120918.jpg"),
        ("Talari Meena", "https://mlrit.ac.in/wp-content/uploads/2023/07/1688720149402-e1688720452294.jpg"),
        ("Nemala Jayasri", "https://mlrit.ac.in/wp-content/uploads/2023/07/Jayasri-e1688720643326.jpg"),
        ("Gunda Aishwarya", "https://mlrit.ac.in/wp-content/uploads/2023/07/1688720149419-e1688720728661.jpg"),
        ("P Lokesh Kumar", "https://mlrit.ac.in/wp-content/uploads/2023/07/1688720149435-e1688720304405.jpg"),
        ("J. Teja", "https://mlrit.ac.in/wp-content/uploads/2023/04/teja-jakka-sir-e1682320247206.jpg"),
        ("Mrs. K. Anusha", "https://mlrit.ac.in/wp-content/uploads/2023/04/Anusha-Mam-e1688724153110.jpg"),
        ("Mr.R Akhilesh Reddy", "https://mlrit.ac.in/wp-content/uploads/2023/04/IMG20240224124637-scaled-e1708759493323.jpg"),
        ("P Sai Kumar", "https://mlrit.ac.in/wp-content/uploads/2023/03/16-2-2023-Sai-Kumar-e1678525314727.jpeg"),
        ("Damala Obulesu", "https://mlrit.ac.in/wp-content/uploads/2023/03/WhatsApp-Image-2023-02-16-at-2.15.50-PM-1-Obulesh-Damala-e1678524653905.jpeg"),
        ("Bhaskar Mekala", "https://mlrit.ac.in/wp-content/uploads/2023/03/Bhaskar-Mekala-Photo-M-BHASKAR.jpg"),
        ("Masigari Nagalakshmi", "https://mlrit.ac.in/wp-content/uploads/2023/03/NAGALAKSHMI-N-LAKSHMI.png"),
        ("Y. Naveen", "https://mlrit.ac.in/wp-content/uploads/2023/03/NAVEEN-PHOTO-NEW1-Y-NAVEEN.jpg"),
        ("Kallam Hemanthi", "https://mlrit.ac.in/wp-content/uploads/2023/03/IMG_20230209_165826-Hemanthi-Kallam.jpg"),
        ("Vijay Keerthika", "https://mlrit.ac.in/wp-content/uploads/2022/03/keerthi-e1688722606936.jpg"),
        ("G. Umamaheswari", "https://mlrit.ac.in/wp-content/uploads/2022/03/uma.jpg"),
        ("K. Jyothsna Reddy", "https://mlrit.ac.in/wp-content/uploads/2022/03/jyotshna.jpg"),
    ],
    "cse-cs": [
        ("Dr. P. Subhashini", "https://mlrit.ac.in/wp-content/uploads/0202/03/subhashini-mam-e1767165355989.jpeg"),
        ("Mr. Atluri Srujan", "https://mlrit.ac.in/wp-content/uploads/2022/03/srujan.jpg"),
        ("Manisha Kandukuri", "https://mlrit.ac.in/wp-content/uploads/2025/12/manisha-e1767164594362.jpeg"),
        ("Juttu Suresh", "https://mlrit.ac.in/wp-content/uploads/2025/12/SURESH.jpeg"),
        ("K.Shiva Krishna", "https://mlrit.ac.in/wp-content/uploads/2025/03/shiva-e1767163081713.jpeg"),
        ("Bochu Sandhya", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.17.59-AM-1-e1717230120786.jpeg"),
        ("Mrs. Swathi Dendi", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.17.59-AM-2-e1717230252499.jpeg"),
        ("Mrs. Y Anjali Satyavati", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.03-AM-e1717230441350.jpeg"),
        ("Irfan Bagawan", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.03-AM-1-e1717230519763.jpeg"),
        ("Kiran Kumar Reddy.A", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.06-AM-e1717230722708.jpeg"),
        ("Ms. Mukku Bhavana", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.09-AM-e1717230797993.jpeg"),
        ("Bolagani Balaji", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-9.26.21-AM.jpeg"),
        ("Ms. D. Tejaswini", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.06-AM-1-e1717230870732.jpeg"),
        ("Mrs. Ch. Sharonu Pushpa", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.08-AM-e1717231106129.jpeg"),
        ("G. Umamaheswari", "https://mlrit.ac.in/wp-content/uploads/2023/03/IMG-20230216-WA0008-G-UMA-MAHESHWARI-e1678524077749.jpg"),
    ],
    "cse-ds": [
        ("Dr. D.B.K. Kamesh", "https://mlrit.ac.in/wp-content/uploads/2024/06/Prof.-Kamesh-Sir.jpg"),
        ("Dr. P. Subhashini", "https://mlrit.ac.in/wp-content/uploads/0202/03/subhashini-mam-e1767165355989.jpeg"),
        ("Dr. Damalla Jyothi", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.11-AM-1-e1717231709688.jpeg"),
        ("Dr. Veerasekhar reddy", "https://mlrit.ac.in/wp-content/uploads/2022/03/veera.jpg"),
        ("Tahneyath Ahmed", "https://mlrit.ac.in/wp-content/uploads/2025/03/WhatsApp-Image-2025-03-18-at-11.05.33-AM.jpeg"),
        ("K. Rani", "https://mlrit.ac.in/wp-content/uploads/2025/03/WhatsApp-Image-2025-03-18-at-10.39.42-AM-e1767087219391.jpeg"),
        ("Manasaraj", "https://mlrit.ac.in/wp-content/uploads/2025/03/WhatsApp-Image-2025-03-18-at-10.46.14-AM-e1767160277107.jpeg"),
        ("S. Shakina", "https://mlrit.ac.in/wp-content/uploads/2025/03/shakina.jpeg"),
        ("Sravanthi Anumasula", "https://mlrit.ac.in/wp-content/uploads/2025/03/SRAVANTHI.jpeg"),
        ("D.SRIVALLI", "https://mlrit.ac.in/wp-content/uploads/2025/03/SRIVALLI.jpeg"),
        ("D.GAYATHRI", "https://mlrit.ac.in/wp-content/uploads/2025/03/GAYATRI-e1742367605108.jpeg"),
        ("N.BABY RANI", "https://mlrit.ac.in/wp-content/uploads/2025/03/babyrani-e1742367135438.jpeg"),
        ("Dasari Amulya", "https://mlrit.ac.in/wp-content/uploads/2025/03/AMULYA.jpeg"),
        ("V. DIVYA", "https://mlrit.ac.in/wp-content/uploads/2024/08/Divya-Vinjamuri.jpg"),
        ("Ms .P.Nishitha", "https://mlrit.ac.in/wp-content/uploads/2024/07/20240727_102447-e1767091692299.jpeg"),
        ("A.Nirisha", "https://mlrit.ac.in/wp-content/uploads/2024/07/20240727_102321-e1767160788160.jpeg"),
        ("S. Anudeep", "https://mlrit.ac.in/wp-content/uploads/2024/07/20240727_102154.jpeg"),
        ("Ms.Madhavi Banala", "https://mlrit.ac.in/wp-content/uploads/2024/07/20240727_102119.jpeg"),
        ("Mrs. Pallavi Mechineni", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-24-at-2.05.20-PM.jpeg"),
        ("Bochu Sandhya", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.17.59-AM-1-e1717230120786.jpeg"),
        ("Mrs. Swathi Dendi", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.17.59-AM-2-e1717230252499.jpeg"),
        ("Mrs. Banoth Rajeshwari", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.02-AM-e1717231032849.jpeg"),
        ("Irfan Bagawan", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.03-AM-1-e1717230519763.jpeg"),
        ("Kiran Kumar Reddy.A", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.06-AM-e1717230722708.jpeg"),
        ("Bolagani Balaji", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-9.26.21-AM.jpeg"),
        ("Malothu Sindhuja", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.07-AM-e1715157114915.jpeg"),
        ("Hasina Nasrin", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.08-AM-1-e1714024454302.jpeg"),
        ("Ms. K.Alankruthi", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.08-AM-2-e1715157305225.jpeg"),
        ("Mrs. B.Ravali Reddy", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.09-AM-1-e1717231290334.jpeg"),
        ("Mathipogu Ashok Babu", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.09-AM-2-e1717231362360.jpeg"),
        ("Mrs. K.Srinija", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.10-AM-e1717231420387.jpeg"),
        ("Bhukya Balakrishna", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.10-AM-1-e1717231497753.jpeg"),
        ("Jangam Nagaraju", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.10-AM-2-e1717231567808.jpeg"),
        ("Mary Navyatha Govindu", "https://mlrit.ac.in/wp-content/uploads/2024/04/WhatsApp-Image-2024-04-25-at-11.18.11-AM-e1717231637621.jpeg"),
        ("N. Thulasi Chithra", "https://mlrit.ac.in/wp-content/uploads/2022/03/Thulasichitra-Photo.jpg"),
        ("Mrs S.Parvathi", "https://mlrit.ac.in/wp-content/uploads/2023/07/Pravathi-mam.jpeg"),
        ("N. Sandhya", "https://mlrit.ac.in/wp-content/uploads/2023/07/Sandhya-mam.jpeg"),
        ("Mrs M.Srividya", "https://mlrit.ac.in/wp-content/uploads/2023/07/Srividya-mam.jpg"),
        ("Ms D.Neelima Priyadarshini", "https://mlrit.ac.in/wp-content/uploads/2023/07/Neelima-mam.jpg"),
        ("Ms N.Vijayasri", "https://mlrit.ac.in/wp-content/uploads/2023/07/vijayasri.jpg"),
        ("Rowsonara Begum", "https://mlrit.ac.in/wp-content/uploads/2023/07/IMG20190818205251-Rowsonara-Begum-e1688632978390.jpg"),
        ("Mr.Mohd Anwar Ali", "https://mlrit.ac.in/wp-content/uploads/2022/07/Anwar-Passport-photo.jpg"),
        ("Ms B. Sushma", "https://mlrit.ac.in/wp-content/uploads/2022/07/Shushma.jpeg"),
        ("Mr D. Sandeep", "https://mlrit.ac.in/wp-content/uploads/2022/03/sandeep.jpg"),
        ("S. Navya", "https://mlrit.ac.in/wp-content/uploads/2022/03/navya.jpg"),
    ],
}


def slug(name: str) -> str:
    s = name.lower()
    s = re.sub(r"\b(dr|mr|mrs|ms|hm)\b\.?", "", s)
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


# Some browsers ship with strict TLS; we relax for the wp-content uploads
ssl_ctx = ssl.create_default_context()


def download(url: str, dst: Path) -> str:
    if dst.exists() and dst.stat().st_size > 0:
        return "exists"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=30, context=ssl_ctx) as resp:
            data = resp.read()
        if not data:
            return "empty"
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(data)
        return f"ok ({len(data):,} B)"
    except Exception as e:
        return f"FAIL: {type(e).__name__}: {e}"


def run():
    summary = {}
    for dept, items in ARCHIVES.items():
        dept_dir = IMG_ROOT / dept
        ok = fail = exists = 0
        for archive_name, url in items:
            sl = slug(archive_name)
            dst = dept_dir / f"{sl}.jpg"
            res = download(url, dst)
            if res.startswith("ok"):
                ok += 1
            elif res == "exists":
                exists += 1
            else:
                fail += 1
                print(f"  [{dept}] {archive_name!r} -> {dst.name}: {res}")
        summary[dept] = (ok, exists, fail, len(items))
    print()
    print(f"{'dept':<10} {'ok':>5} {'exists':>7} {'fail':>5} {'total':>6}")
    for dept, (o, e, f, t) in summary.items():
        print(f"{dept:<10} {o:>5} {e:>7} {f:>5} {t:>6}")


if __name__ == "__main__":
    run()
