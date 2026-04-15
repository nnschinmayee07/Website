import os, re

base = 'c:/mlr/homepage/departments'

# Faculty data with research details for hover popups
# Format: (img, name, role, qual, areas, papers)
faculty = {
    'cse': [
        ('ajmeera-kiran.jpg', 'Dr. Ajmeera Kiran', 'Associate Professor & HOD', 'Ph.D (CSE), M.Tech (IT), B.E (CSE)', 'Deep Learning, ML, Image Processing, IoT, Cybersecurity', ['Deep Learning for Hyper-Multiclass Image Clustering — IEEE Trans. Consumer Electronics, 2024', 'Melanoma Diagnosis Integrating Imaging and Genomic Data — Skin Research & Technology, 2024', 'IoT Security Framework for Smart City Applications — Springer, 2023']),
        ('k-srinivas-rao.jpg', 'Dr. K. Srinivas Rao', 'Professor', 'Ph.D (CSE), M.Tech', 'IoT, Embedded Systems, Networks, Data Mining', ['IoT-based Smart Agriculture Monitoring System — IEEE Access, 2023', 'Intrusion Detection using Deep Learning for IoT Networks — Elsevier, 2024']),
        ('n-sirisha.jpg', 'Dr. N. Sirisha', 'Professor & Associate Dean', 'Ph.D (CSE), M.Tech', 'AI, Image Processing, WSN, Data Science', ['CNN-based Medical Image Classification — Journal of Biomedical Informatics, 2024', 'Energy-Efficient WSN Routing using Fuzzy Logic — Springer, 2022']),
        ('a-balaram.jpg', 'Dr. A. Balaram', 'Professor', 'Ph.D (CSE), M.Tech', 'Software Engineering, Cloud Computing', ['Cloud Resource Optimization using Metaheuristic Algorithms — Future Gen. Computer Systems, 2023']),
        ('v-thrimurthulu.jpg', 'Dr. V. Thrimurthulu', 'Professor', 'Ph.D (CSE), M.Tech', 'Data Mining, Machine Learning, Big Data', ['Sentiment Analysis using Transformer Models — ACM NLPTM Conference, 2023']),
        ('k-venkata-subbaiah.jpg', 'Dr. K. Venkata Subbaiah', 'Professor', 'Ph.D (CSE), M.Tech', 'Network Security, Cryptography', ['Blockchain-enabled Secure Data Sharing in Cloud — Cluster Computing, Springer, 2023']),
        ('kandrakunta-chinnaiah.jpg', 'Dr. Kandrakunta Chinnaiah', 'Associate Professor', 'Ph.D (CSE), M.Tech', 'Machine Learning, Computer Vision', []),
        ('j-mahalakshmi.jpeg', 'Dr. J. Mahalakshmi', 'Associate Professor', 'Ph.D (CSE), M.Tech', 'NLP, Text Mining, Deep Learning', []),
        ('john-samuel-babu.jpg', 'Dr. G. John Samuel Babu', 'Associate Professor', 'Ph.D (CSE), M.Tech', 'Cloud Computing, IoT', []),
        ('k-gagan-kumar.jpg', 'Dr. K. Gagan Kumar', 'Associate Professor', 'Ph.D (CSE), M.Tech', 'AI, Reinforcement Learning', []),
        ('sai-krishna.jpg', 'Mr. Sai Krishna', 'Associate Professor', 'M.Tech (CSE)', 'Web Technologies, Software Engineering', []),
        ('nagarjuna-tandra.jpg', 'Mr. Nagarjuna Tandra', 'Associate Professor', 'M.Tech (CSE)', 'Data Structures, Algorithms', []),
        ('b-sanjai-prasad.jpg', 'Dr. B. Sanjai Prasada Rao', 'Associate Professor', 'Ph.D (CSE), M.Tech', 'Data Science, Big Data Analytics', []),
        ('michael-preetam.jpg', 'Dr. P. Michael Preetam Raj', 'Associate Professor', 'Ph.D (CSE), M.Tech', 'Computer Networks, Security', []),
        ('t-venkata-nagaraju.jpeg', 'Dr. T. Venkata Nagaraju', 'Associate Professor', 'Ph.D (CSE), M.Tech', 'Image Processing, Pattern Recognition', []),
        ('m-kalpana-chowdary.jpg', 'Dr. M. Kalpana Chowdary', 'Associate Professor', 'Ph.D (CSE), M.Tech', 'Data Mining, Machine Learning', []),
        ('b-devananda-rao.jpg', 'Mr. B. Devananda Rao', 'Associate Professor', 'M.Tech (CSE)', 'Operating Systems, DBMS', []),
        ('k-pushpa-rani.jpg', 'Dr. K. Pushpa Rani', 'Associate Professor', 'Ph.D (CSE), M.Tech', 'Artificial Intelligence, Expert Systems', []),
        ('g-prabhakara-reddy.jpg', 'G. Prabhakara Reddy', 'Associate Professor', 'M.Tech (CSE)', 'Software Engineering, Testing', []),
        ('m-srinivasa-rao.jpg', 'Mr. M. Srinivasa Rao', 'Associate Professor', 'M.Tech (CSE)', 'Computer Networks, OS', []),
        ('allam-sangeetha.jpg', 'Allam Sangeetha', 'Associate Professor', 'M.Tech (CSE), (Ph.D)', 'Cloud Computing, Data Science', ['Hybrid ML for Crop Yield Prediction using Satellite Imagery — Computers & Electronics in Agriculture, Elsevier, 2021']),
        ('guduru-durga-bhavani.jpeg', 'Miss Guduru Durga Bhavani', 'Assistant Professor', 'M.Tech (CSE)', 'Web Technologies, Python', []),
        ('shaik-mohammed-ilias.jpeg', 'Dr. Shaik Mohammed Ilias', 'Assistant Professor', 'Ph.D (CSE)', 'Cybersecurity, Blockchain', []),
        ('sasmita-pradhan.png', 'Mrs. Sasmita Kumari Pradhan', 'Assistant Professor', 'M.Tech (CSE)', 'Machine Learning, NLP', []),
        ('b-muralikrishna.jpeg', 'Mr. Boligarla Muralikrishna', 'Assistant Professor', 'M.Tech (CSE)', 'Data Structures, Java', []),
        ('b-ratnamala.jpeg', 'Mrs. B. Ratnamala', 'Assistant Professor', 'M.Tech (CSE)', 'DBMS, Software Engineering', []),
        ('j-chaitanya.jpeg', 'Jonnalagadda Chaitanya', 'Assistant Professor', 'M.Tech (CSE)', 'Python, AI', []),
        ('d-jeevitha.jpeg', 'Dubasi Jeevitha', 'Assistant Professor', 'M.Tech (CSE)', 'Web Technologies, DBMS', []),
        ('d-tejaswini.jpg', 'D. Tejaswini', 'Assistant Professor', 'M.Tech (CSE)', 'Data Mining, ML', []),
        ('hareesh-pesala.jpg', 'Mr. Hareesh Pesala', 'Assistant Professor', 'M.Tech (CSE)', 'Cloud Computing, DevOps', []),
        ('ramya-s-pure.jpg', 'Ramya S Pure', 'Assistant Professor', 'M.Tech (CSE)', 'Software Engineering, Testing', []),
        ('p-santhosh-kumar.jpeg', 'P. Santhosh Kumar', 'Assistant Professor', 'M.Tech (CSE)', 'Computer Networks, IoT', []),
        ('jetti-sri-lakshmi.jpg', 'Jetti Sri Lakshmi', 'Assistant Professor', 'M.Tech (CSE)', 'AI, Deep Learning', []),
        ('ms-sabitha.jpg', 'M. S. Sabitha', 'Assistant Professor', 'M.Tech (CSE)', 'Machine Learning, Python', []),
        ('a-laxmi-prasanna.jpg', 'Anishetty Laxmi Prasanna', 'Assistant Professor', 'M.Tech (CSE)', 'DBMS, Web Technologies', []),
        ('kshitiza-vasudeva.jpg', 'Mrs. Kshitiza Vasudeva', 'Assistant Professor', 'M.Tech (CSE)', 'OS, Computer Networks', []),
        ('boddu-srilatha.jpg', 'Mrs. Boddu Srilatha', 'Assistant Professor', 'M.Tech (CSE)', 'Data Structures, Java', []),
        ('v-balakrishna-reddy.jpg', 'Mr. V. Balakrishna Reddy', 'Assistant Professor', 'M.Tech (CSE)', 'Cloud Computing, Big Data', []),
        ('p-victor-emmanuel.jpg', 'Mr. P. Victor Emmanuel', 'Assistant Professor', 'M.Tech (CSE)', 'Software Engineering, Agile', []),
        ('m-vineesha.jpg', 'Mrs. M. Vineesha', 'Assistant Professor', 'M.Tech (CSE)', 'Python, Data Science', []),
        ('b-manjusha.jpg', 'Mrs. B. Manjusha', 'Assistant Professor', 'M.Tech (CSE)', 'AI, Machine Learning', []),
        ('m-srinivasulu.jpg', 'Mr. M. Srinivasulu', 'Assistant Professor', 'M.Tech (CSE)', 'Computer Networks, Security', []),
        ('nagarjuna-rao-gudelli.jpg', 'Mr. Nagarjuna Rao Gudelli', 'Assistant Professor', 'M.Tech (CSE)', 'Data Structures, Algorithms', []),
        ('swathi.jpeg', 'Mrs. Swathi', 'Assistant Professor', 'M.Tech (CSE)', 'DBMS, Web Technologies', []),
        ('k-samatha.jpeg', 'Mrs. K. Samatha', 'Assistant Professor', 'M.Tech (CSE)', 'Software Engineering', []),
        ('a-nagamani.jpg', 'Mrs. A. Nagamani', 'Assistant Professor', 'M.Tech (CSE)', 'Operating Systems, C Programming', []),
        ('kranthi-kumari.jpg', 'Ms. Kranthi Kumari', 'Assistant Professor', 'M.Tech (CSE)', 'Python, Machine Learning', []),
        ('ragini-patil.jpg', 'Ragini Patil', 'Assistant Professor', 'M.Tech (CSE)', 'AI, NLP', []),
        ('lingaiah-suramsetti.png', 'Lingaiah Suramsetti', 'Assistant Professor', 'M.Tech (CSE)', 'Java, Data Structures', []),
        ('i-sapthami.jpg', 'I. Sapthami', 'Assistant Professor', 'M.Tech (CSE)', 'Web Technologies, DBMS', []),
        ('p-deepak.jpg', 'Mr. P. Deepak', 'Assistant Professor', 'M.Tech (CSE)', 'Computer Networks, IoT', []),
        ('jeethu-philip.jpg', 'Mrs. Jeethu Philip', 'Assistant Professor', 'M.Tech (CSE)', 'Software Engineering, Testing', []),
        ('j-pradeep-kumar.jpg', 'J. Pradeep Kumar', 'Assistant Professor', 'M.Tech (CSE)', 'OS, Linux Administration', []),
        ('telise-vinod.jpg', 'Telise Vinod', 'Assistant Professor', 'M.Tech (CSE)', 'Cloud Computing, DevOps', []),
        ('kukunoor-shekar.jpg', 'Mr. Kukunoor Shekar', 'Assistant Professor', 'M.Tech (CSE)', 'Data Mining, Big Data', []),
        ('g-praveen.jpg', 'Mr. G. Praveen', 'Assistant Professor', 'M.Tech (CSE)', 'Computer Networks, Security', []),
        ('sk-lokesh-naik.jpg', 'S K Lokesh Naik', 'Assistant Professor', 'M.Tech (CSE)', 'DBMS, SQL', []),
        ('oruganti-ramesh.jpg', 'Oruganti Ramesh', 'Assistant Professor', 'M.Tech (CSE)', 'Java, OOP', []),
        ('divya-priya-degala.jpg', 'Mrs. Divya Priya Degala', 'Assistant Professor', 'M.Tech (CSE)', 'Web Technologies, JavaScript', []),
        ('palelli-purushotham.jpeg', 'Palelli Purushotham', 'Assistant Professor', 'M.Tech (CSE)', 'Python, Data Analytics', []),
        ('bashetty-suman.jpg', 'Bashetty Suman', 'Assistant Professor', 'M.Tech (CSE)', 'Machine Learning, AI', []),
        ('b-veda-vidhya.jpg', 'B. Veda Vidhya', 'Assistant Professor', 'M.Tech (CSE)', 'Software Engineering', []),
        ('k-swetha.jpg', 'K. Swetha', 'Assistant Professor', 'M.Tech (CSE)', 'C Programming, Data Structures', []),
        ('en-vijaya-kumari.jpg', 'E. N. Vijaya Kumari', 'Assistant Professor', 'M.Tech (CSE)', 'Data Science, Python', []),
    ],
}

def gen_initials(name):
    parts = name.replace('Dr.','').replace('Mr.','').replace('Mrs.','').replace('Ms.','').replace('Miss','').replace('Prof.','').strip().split()
    if len(parts) >= 2:
        return parts[0][0].upper() + parts[-1][0].upper()
    return parts[0][:2].upper()

def gen_memory_lane(dept, fac_list):
    items = []
    for img, name, role, qual, areas, papers in fac_list:
        initials = gen_initials(name)
        sn = name.replace('&', '&amp;').replace('"', '&quot;')
        sr = role.replace('&', '&amp;')

        # Build area tags
        area_tags = ''
        for a in areas.split(', ')[:4]:
            area_tags += f'<span class="faculty-popup__tag">{a}</span>'

        # Build papers
        papers_html = ''
        if papers:
            papers_html = '<div class="faculty-popup__papers"><div class="faculty-popup__papers-title">Key Publications</div>'
            for p in papers[:3]:
                papers_html += f'<div class="faculty-popup__paper">{p}</div>'
            papers_html += '</div>'

        items.append(f'''            <div class="faculty-item">
              <div class="faculty-item__photo">
                <img src="images/{dept}/{img}" alt="{sn}" onerror="this.style.display='none';this.parentElement.textContent='{initials}'" />
              </div>
              <div class="faculty-item__name">{sn}</div>
              <div class="faculty-item__role">{sr}</div>
              <div class="faculty-popup">
                <div class="faculty-popup__name">{sn}</div>
                <div class="faculty-popup__role">{sr}</div>
                <p class="faculty-popup__detail"><strong>Qualification:</strong> {qual}</p>
                <p class="faculty-popup__detail"><strong>Areas:</strong></p>
                <div>{area_tags}</div>
                {papers_html}
              </div>
            </div>''')

    return '\n'.join(items)

# Only do CSE for now
for dept in ['cse']:
    filepath = f'{base}/{dept}.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    html = gen_memory_lane(dept, faculty[dept])

    # Find and replace the faculty section content
    # Pattern: from <div class="faculty-grid"> to the next </section>
    match = re.search(r'(<section class="dept-section" id="faculty">.*?<h2 class="dept-section__heading">Faculty Profiles</h2>\s*)<div class="faculty-grid">.*?</div>\s*</section>', content, re.DOTALL)
    if match:
        prefix = match.group(1)
        new_section = f'''{prefix}<div class="faculty-lane">
{html}
          </div>
      </section>'''
        content = content[:match.start()] + new_section + content[match.end():]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'{dept}: Updated to memory lane with {len(faculty[dept])} faculty')
    else:
        print(f'{dept}: PATTERN NOT FOUND')
