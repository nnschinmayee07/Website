#!/usr/bin/env python3
"""Download Freshman faculty photos and create the department page."""
import urllib.request, os

base_img = 'c:/mlr/homepage/departments/images/freshman'
os.makedirs(base_img, exist_ok=True)

faculty = [
    ('achireddy.jpg', 'Dr. Ch Achi Reddy', 'HOD, Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/achireddy.jpg', 'Physics, Material Science'),
    ('radhika-devi.jpg', 'Dr. V. Radhika Devi', 'Director, Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/radhika.jpg', 'Mathematics, Statistics'),
    ('raghunath-rao.jpg', 'Dr. Y. Raghunath Rao', 'Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/raghu.jpg', 'Chemistry, Materials'),
    ('ramgopal.jpg', 'Dr. N Ch Ramgopal', 'Professor', 'https://mlrit.ac.in/wp-content/uploads/2023/05/1667466248428.jpg', 'Physics, Electronics'),
    ('ravindranath.jpg', 'Dr. G. Ravindranath Reddy', 'Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/Dr.RavindranathReddy-scaled.jpg', 'Mathematics'),
    ('krishna-prasad.jpg', 'Dr. JSVR. Krishna Prasad', 'Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/JSVR.jpg', 'English, Communication'),
    ('umamaheswara.jpg', 'Dr. Umamaheswara Rao Bontha', 'Professor', 'https://mlrit.ac.in/wp-content/uploads/2024/08/IMG-20240810-WA0002.jpg', 'Physics, Optics'),
    ('anantha-lakshmi.jpg', 'Dr. Y. Anantha Lakshmi', 'Professor', 'https://mlrit.ac.in/wp-content/uploads/2023/05/Dr.AnanthaLaxmi.jpg', 'Chemistry'),
    ('yuganand.jpg', 'Dr. N. Yuganand', 'Professor', 'https://mlrit.ac.in/wp-content/uploads/2023/07/ganesh1.jpg', 'Mathematics'),
    ('vijaya-bhaskar.jpg', 'Dr. Mopur Vijaya Bhaskar Reddy', 'Professor', 'https://mlrit.ac.in/wp-content/uploads/2026/04/Vijaybhaskar-reddy.jpeg', 'Physics'),
    ('sailaja.jpg', 'Dr. Sailaja Peesapati', 'Professor', 'https://mlrit.ac.in/wp-content/uploads/2026/04/Dr-Sailaja.jpeg', 'Chemistry'),
    ('harika.jpg', 'Dr. Harika Patnala', 'Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/07/IMG-20240419-WA0060.jpg', 'English, Soft Skills'),
    ('deepthi-sista.jpg', 'Dr. Deepthi Sista', 'Associate Professor', 'https://mlrit.ac.in/wp-content/uploads/2024/08/IMG-20240812-WA0003.jpg', 'Mathematics'),
    ('lakshmi-rajesh.jpg', 'Dr. CH. Lakshmi Rajesh', 'Associate Professor', 'https://mlrit.ac.in/wp-content/uploads/2024/05/Lakshmi-Rajesh.png', 'Physics'),
    ('brahmayya.jpg', 'Dr. Manuri Brahmayya', 'Associate Professor', 'https://mlrit.ac.in/wp-content/uploads/2024/05/IMG-20240419-WA0065.jpg', 'Chemistry'),
    ('nirmala-kumari.jpg', 'Dr. V Nirmala Kumari', 'Associate Professor', 'https://mlrit.ac.in/wp-content/uploads/2023/07/WhatsApp-Image-2023-07-08-at-13.04.27.jpeg', 'Mathematics'),
    ('aravind-mudhiraj.jpg', 'Dr. Kola Aravind Mudhiraj', 'Associate Professor', 'https://mlrit.ac.in/wp-content/uploads/2023/07/WhatsApp-Image-2024-04-20-at-12.50.46.jpeg', 'Physics'),
    ('haripriya.jpg', 'Dr. V. Haripriya', 'Associate Professor', 'https://mlrit.ac.in/wp-content/uploads/2023/05/1688659643144.jpg', 'English'),
    ('parsharamulu.jpg', 'Parsharamulu Medichelmi', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2026/04/Parshuram.jpeg', 'Mathematics'),
    ('divya.jpg', 'Madhuraveni Divya', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2026/04/M-Divya.jpeg', 'Chemistry'),
    ('sumalatha.jpg', 'Dr. Sumalatha Manne', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2026/04/WhatsApp-Image-2026-04-01-at-15.06.39.jpeg', 'Mathematics'),
    ('amalendu.jpg', 'Dr. Amalendu Rana', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2024/08/amalendu-photo.jpg', 'Physics'),
    ('harsha-vincent.jpg', 'Dr. Harsha Vincent', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2024/08/PASSPOT-SIZE-PHOTO-HARSHA.jpg', 'English'),
    ('abdullah.jpg', 'Mr. Abdullah Nouman', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2024/08/IMG-20240812-WA0001.jpg', 'Mathematics'),
    ('pratyusha.jpg', 'Dr. N. Pratyusha', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2024/05/prathyusha-photo.jpg', 'Chemistry'),
    ('ratna-priya.jpg', 'Mrs. L Ratna Priya', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2024/05/Ratna-priya.jpeg', 'Physics'),
    ('eranna.jpg', 'Mr. S Eranna', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2024/05/WhatsApp-Image-2024-04-19-at-11.32.39.jpeg', 'Mathematics'),
    ('momin-ali.jpg', 'Mr. Momin Ali', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2024/05/FB_IMG_1713508925387.jpg', 'Physics'),
    ('subhadeep.jpg', 'Dr. Subhadeep Kumar', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2024/05/Photo-rotated.jpeg', 'Chemistry'),
    ('inzamul.jpg', 'Dr. Inzamul Sarkar', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2023/07/Inzamul-Sarkar.jpg', 'Physics'),
    ('ekramul.jpg', 'Mr. Ekramul Haque', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2023/07/b254e802-b577-47ca-b201-9b9e76749f1c-compressed-e1688977428704.jpg', 'Mathematics'),
    ('shubhra.jpg', 'Dr. Shubhra Dash', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2023/07/Shubhra-Dash-.jpg', 'Chemistry'),
    ('atasi.jpg', 'Dr. Atasi Ray', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2023/05/IMG_20230707_122240-1-e1688964867263.jpg', 'Physics'),
    ('srimanta.jpg', 'Dr. Srimanta Pal', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2023/05/Srimantha-Pal.jpg', 'Mathematics'),
    ('monaj.jpg', 'Dr. Monaj Karar', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/07/MK_Photo.jpg.jpeg', 'Chemistry'),
    ('srinivas-indla.jpg', 'Dr. Srinivas Indla', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/07/Srinivas-Indla.jpg', 'English'),
    ('subhasish.jpg', 'Dr. Subhasish Saha', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2024/05/Subhasish-saha.jpeg', 'Physics'),
    ('shiva-kumar.jpg', 'Sri Ram Shiva Kumar', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/sivakumar.jpg', 'Mathematics'),
    ('arif.jpg', 'Mr. Arif Ahammed', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/arif-1.jpg', 'Physics'),
    ('sujatha.jpg', 'M. Sujatha', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/sujatha-1.jpg', 'Chemistry'),
    ('janga-anil.jpg', 'Janga Anil Reddy', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/janga.jpg', 'English'),
    ('shilpa.jpg', 'A. Shilpa', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/Shilpa-Madam.jpg', 'Mathematics'),
    ('amritha.jpg', 'Dr. Amritha Saha', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/Dr.-Amritha.jpg', 'Chemistry'),
    ('noel.jpg', 'Mr. Noel Nalli', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/noel.jpg', 'English'),
    ('lavanya.jpg', 'Dr. Y. Lavanya', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/lavanya.jpg', 'Mathematics'),
    ('vishal.jpg', 'Mr. Vishal Nakka', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/Vishal-1.jpg', 'Physics'),
    ('hymavathi.jpg', 'M. Hymavathi', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/Hymavathi-madam.jpg', 'Chemistry'),
    ('praveen-kumar.jpg', 'N. Praveen Kumar', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/praveen-kumar-sir.jpg', 'Mathematics'),
    ('veera-raghavulu.jpg', 'Mr. T Veera Raghavulu', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/vaararaghavulu.jpg', 'Physics'),
    ('sudheer.jpg', 'Dr. M. Sudheer Kumar', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/sudheer.jpg', 'English'),
    ('amar-nath.jpg', 'Neela Amar Nath', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/amr.jpg', 'Mathematics'),
    ('krishnudu.jpg', 'Mr. K. Krishnudu', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/kk.jpg', 'Physics'),
    ('laxman-rao.jpg', 'Mr. A Venkata Laxman Rao', 'Assistant Professor', 'https://mlrit.ac.in/wp-content/uploads/2022/02/Laxman-rao-photo.jpeg', 'Chemistry'),
]

# Download photos
ok = fail = 0
for fname, name, role, url, spec in faculty:
    path = f'{base_img}/{fname}'
    if os.path.exists(path) and os.path.getsize(path) > 1000:
        ok += 1
        continue
    try:
        urllib.request.urlretrieve(url, path)
        ok += 1
    except:
        fail += 1

print(f'Photos: {ok} ok, {fail} fail out of {len(faculty)}')

# Save faculty data for page generator
with open('c:/mlr/freshman_faculty.txt', 'w', encoding='utf-8') as f:
    for fname, name, role, url, spec in faculty:
        f.write(f'{fname}|{name}|{role}|{spec}\n')

print(f'Faculty data saved: {len(faculty)} entries')
