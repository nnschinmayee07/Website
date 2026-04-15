import os, re

base = 'c:/mlr/homepage/departments'

# Faculty data: (filename, name, role)
faculty = {
    'cse': [
        ('ajmeera-kiran.jpg', 'Dr. Ajmeera Kiran', 'Associate Professor & HOD'),
        ('k-srinivas-rao.jpg', 'Dr. K. Srinivas Rao', 'Professor'),
        ('n-sirisha.jpg', 'Dr. N. Sirisha', 'Professor & Associate Dean'),
        ('a-balaram.jpg', 'Dr. A. Balaram', 'Professor'),
        ('v-thrimurthulu.jpg', 'Dr. V. Thrimurthulu', 'Professor'),
        ('k-venkata-subbaiah.jpg', 'Dr. K. Venkata Subbaiah', 'Professor'),
        ('kandrakunta-chinnaiah.jpg', 'Dr. Kandrakunta Chinnaiah', 'Associate Professor'),
        ('j-mahalakshmi.jpeg', 'Dr. J. Mahalakshmi', 'Associate Professor'),
        ('john-samuel-babu.jpg', 'Dr. G. John Samuel Babu', 'Associate Professor'),
        ('k-gagan-kumar.jpg', 'Dr. K. Gagan Kumar', 'Associate Professor'),
        ('sai-krishna.jpg', 'Mr. Sai Krishna', 'Associate Professor'),
        ('nagarjuna-tandra.jpg', 'Mr. Nagarjuna Tandra', 'Associate Professor'),
        ('b-sanjai-prasad.jpg', 'Dr. B. Sanjai Prasada Rao', 'Associate Professor'),
        ('michael-preetam.jpg', 'Dr. P. Michael Preetam Raj', 'Associate Professor'),
        ('t-venkata-nagaraju.jpeg', 'Dr. T. Venkata Nagaraju', 'Associate Professor'),
        ('m-kalpana-chowdary.jpg', 'Dr. M. Kalpana Chowdary', 'Associate Professor'),
        ('b-devananda-rao.jpg', 'Mr. B. Devananda Rao', 'Associate Professor'),
        ('k-pushpa-rani.jpg', 'Dr. K. Pushpa Rani', 'Associate Professor'),
        ('g-prabhakara-reddy.jpg', 'G. Prabhakara Reddy', 'Associate Professor'),
        ('m-srinivasa-rao.jpg', 'Mr. M. Srinivasa Rao', 'Associate Professor'),
        ('allam-sangeetha.jpg', 'Allam Sangeetha', 'Associate Professor'),
        ('guduru-durga-bhavani.jpeg', 'Miss Guduru Durga Bhavani', 'Assistant Professor'),
        ('shaik-mohammed-ilias.jpeg', 'Dr. Shaik Mohammed Ilias', 'Assistant Professor'),
        ('sasmita-pradhan.png', 'Mrs. Sasmita Kumari Pradhan', 'Assistant Professor'),
        ('b-muralikrishna.jpeg', 'Mr. Boligarla Muralikrishna', 'Assistant Professor'),
        ('b-ratnamala.jpeg', 'Mrs. B. Ratnamala', 'Assistant Professor'),
        ('j-chaitanya.jpeg', 'Jonnalagadda Chaitanya', 'Assistant Professor'),
        ('d-jeevitha.jpeg', 'Dubasi Jeevitha', 'Assistant Professor'),
        ('d-tejaswini.jpg', 'D. Tejaswini', 'Assistant Professor'),
        ('hareesh-pesala.jpg', 'Mr. Hareesh Pesala', 'Assistant Professor'),
        ('ramya-s-pure.jpg', 'Ramya S Pure', 'Assistant Professor'),
        ('p-santhosh-kumar.jpeg', 'P. Santhosh Kumar', 'Assistant Professor'),
        ('jetti-sri-lakshmi.jpg', 'Jetti Sri Lakshmi', 'Assistant Professor'),
        ('ms-sabitha.jpg', 'M. S. Sabitha', 'Assistant Professor'),
        ('a-laxmi-prasanna.jpg', 'Anishetty Laxmi Prasanna', 'Assistant Professor'),
        ('kshitiza-vasudeva.jpg', 'Mrs. Kshitiza Vasudeva', 'Assistant Professor'),
        ('boddu-srilatha.jpg', 'Mrs. Boddu Srilatha', 'Assistant Professor'),
        ('v-balakrishna-reddy.jpg', 'Mr. V. Balakrishna Reddy', 'Assistant Professor'),
        ('p-victor-emmanuel.jpg', 'Mr. P. Victor Emmanuel', 'Assistant Professor'),
        ('m-vineesha.jpg', 'Mrs. M. Vineesha', 'Assistant Professor'),
        ('b-manjusha.jpg', 'Mrs. B. Manjusha', 'Assistant Professor'),
        ('m-srinivasulu.jpg', 'Mr. M. Srinivasulu', 'Assistant Professor'),
        ('nagarjuna-rao-gudelli.jpg', 'Mr. Nagarjuna Rao Gudelli', 'Assistant Professor'),
        ('swathi.jpeg', 'Mrs. Swathi', 'Assistant Professor'),
        ('k-samatha.jpeg', 'Mrs. K. Samatha', 'Assistant Professor'),
        ('a-nagamani.jpg', 'Mrs. A. Nagamani', 'Assistant Professor'),
        ('kranthi-kumari.jpg', 'Ms. Kranthi Kumari', 'Assistant Professor'),
        ('ragini-patil.jpg', 'Ragini Patil', 'Assistant Professor'),
        ('lingaiah-suramsetti.png', 'Lingaiah Suramsetti', 'Assistant Professor'),
        ('i-sapthami.jpg', 'I. Sapthami', 'Assistant Professor'),
        ('p-deepak.jpg', 'Mr. P. Deepak', 'Assistant Professor'),
        ('jeethu-philip.jpg', 'Mrs. Jeethu Philip', 'Assistant Professor'),
        ('j-pradeep-kumar.jpg', 'J. Pradeep Kumar', 'Assistant Professor'),
        ('telise-vinod.jpg', 'Telise Vinod', 'Assistant Professor'),
        ('kukunoor-shekar.jpg', 'Mr. Kukunoor Shekar', 'Assistant Professor'),
        ('g-praveen.jpg', 'Mr. G. Praveen', 'Assistant Professor'),
        ('sk-lokesh-naik.jpg', 'S K Lokesh Naik', 'Assistant Professor'),
        ('oruganti-ramesh.jpg', 'Oruganti Ramesh', 'Assistant Professor'),
        ('divya-priya-degala.jpg', 'Mrs. Divya Priya Degala', 'Assistant Professor'),
        ('palelli-purushotham.jpeg', 'Palelli Purushotham', 'Assistant Professor'),
        ('bashetty-suman.jpg', 'Bashetty Suman', 'Assistant Professor'),
        ('b-veda-vidhya.jpg', 'B. Veda Vidhya', 'Assistant Professor'),
        ('k-swetha.jpg', 'K. Swetha', 'Assistant Professor'),
        ('en-vijaya-kumari.jpg', 'E. N. Vijaya Kumari', 'Assistant Professor'),
    ],
    'ece': [
        ('svs-prasad.jpg', 'Dr. S V S Prasad', 'Professor & HOD'),
        ('shrikant-upadhyay.jpg', 'Dr. Shrikant Upadhyay', 'Associate Professor'),
        ('kiran-chand.jpeg', 'Dr. Kiran Chand Ravi', 'Associate Professor'),
        ('karthik-reddy.jpg', 'Dr. G. Karthik Reddy', 'Associate Professor'),
        ('t-vijetha.jpg', 'Dr. T. Vijetha', 'Associate Professor'),
        ('p-yakaiah.jpg', 'Dr. P. Yakaiah', 'Associate Professor'),
        ('k-nishanth-rao.jpg', 'Dr. K. Nishanth Rao', 'Associate Professor'),
        ('rudraram-divya.jpg', 'Rudraram Divya', 'Assistant Professor'),
        ('pullela-sravani.jpg', 'Pullela Sravani', 'Assistant Professor'),
        ('nagendra-babu.jpg', 'M. Nagendra Babu', 'Assistant Professor'),
        ('gv-subba-reddy.jpg', 'G. Venkata Subba Reddy', 'Assistant Professor'),
        ('akhila-akula.jpg', 'Akhila Akula', 'Assistant Professor'),
        ('mary-kannidi.jpeg', 'Ms. Mary Kannidi', 'Assistant Professor'),
        ('s-naveen-kumar.jpg', 'Mr. S. Naveen Kumar', 'Assistant Professor'),
        ('khobragade-pithamber.jpg', 'Mr. Khobragade Pithamber', 'Assistant Professor'),
        ('k-purushotham.jpg', 'Mr. K. Purushotham', 'Assistant Professor'),
        ('y-sivaramakrishna.jpg', 'Dr. Y. Sivaramakrishna', 'Assistant Professor'),
        ('ganesh-miriyala.jpg', 'Dr. Ganesh Miriyala', 'Assistant Professor'),
        ('velpula-vijaya-kumar.jpg', 'Dr. Velpula Vijaya Kumar', 'Assistant Professor'),
        ('sahitya.jpg', 'Mrs. Pinnamaraju Sahitya', 'Assistant Professor'),
        ('sandip-kumar.jpg', 'Mr. Ladi Sandip Kumar Patra', 'Assistant Professor'),
        ('vadla-arun-kumar.jpg', 'Mr. Vadla Arun Kumar', 'Assistant Professor'),
        ('manoj-kumar.jpg', 'Dr. Manoj Kumar', 'Assistant Professor'),
        ('b-sireesha.jpg', 'Ms. Badepalli Sireesha', 'Assistant Professor'),
        ('n-poornima-deepthi.jpg', 'Mrs. N. Poornima Deepthi', 'Assistant Professor'),
        ('b-kiran-kumar.jpg', 'Mr. B. Kiran Kumar', 'Assistant Professor'),
        ('g-kaushik.jpg', 'Mr. G. Kaushik', 'Assistant Professor'),
        ('geetha-yerramsetti.jpg', 'Mrs. Geetha Yerramsetti', 'Assistant Professor'),
        ('m-raju-naik.jpg', 'Mr. M. Raju Naik', 'Assistant Professor'),
        ('k-maniraj.jpg', 'Mr. K. Maniraj', 'Assistant Professor'),
        ('sudhakar-ajmera.jpg', 'Mr. Sudhakar Ajmera', 'Assistant Professor'),
        ('b-anusha.jpg', 'Ms. Badepalli Anusha', 'Assistant Professor'),
        ('chinthakindi-babaiah.jpeg', 'Mr. Chinthakindi Babaiah', 'Assistant Professor'),
        ('rayala-sateesh.jpg', 'Mr. Rayala Sateesh', 'Assistant Professor'),
        ('s-monika.jpg', 'Mrs. S. Monika', 'Assistant Professor'),
        ('k-hari-babu.png', 'Mr. K. Hari Babu', 'Assistant Professor'),
    ],
    'eee': [
        ('ashok-kumar.jpg', 'Prof. Ashok Kumar Cheeli', 'Professor & HOD'),
        ('dileep-kumar.jpg', 'Dr. M. Dileep Kumar', 'Associate Professor'),
        ('placeholder.jpg', 'Ashok Reddy Kanna', 'Associate Professor'),
        ('placeholder.jpg', 'K. Usha Rani', 'Associate Professor'),
        ('sumana-das.jpeg', 'Dr. Sumana Das', 'Associate Professor'),
        ('bv-rajanna.jpg', 'Dr. B. V. Rajanna', 'Associate Professor'),
        ('t-bhargava-ramu.jpg', 'Dr. T. Bhargava Ramu', 'Associate Professor'),
        ('sonu-kumar.jpeg', 'Dr. Sonu Kumar', 'Assistant Professor'),
        ('y-lalitha-kameswari.jpeg', 'Dr. Y. Lalitha Kameswari', 'Assistant Professor'),
        ('t-mrudula.jpg', 'T. Mrudula', 'Assistant Professor'),
        ('n-karthik.jpg', 'N. Karthik', 'Assistant Professor'),
        ('p-jithendar.jpg', 'P. Jithendar', 'Assistant Professor'),
        ('a-yadagiri.jpg', 'A. Yadagiri', 'Assistant Professor'),
        ('k-rajasri.jpg', 'K. Rajasri', 'Assistant Professor'),
        ('a-shubhangi-rao.jpg', 'A. Shubhangi Rao', 'Assistant Professor'),
        ('ch-srivardhan-kumar.jpg', 'Dr. CH. Srivardhan Kumar', 'Assistant Professor'),
        ('m-sreenivasa-reddy.jpg', 'M. Sreenivasa Reddy', 'Associate Professor'),
    ],
    'mechanical': [
        ('krishnaraj.jpg', 'Dr. J. Krishnaraj', 'Professor & HOD'),
        ('prabhu-kishore.jpeg', 'Dr. N. Prabhu Kishore', 'Associate Professor'),
        ('ravi-kiran.jpg', 'Dr. Ch. Ravi Kiran', 'Associate Professor'),
        ('harikishor.jpg', 'Dr. Harikishor Kumar', 'Associate Professor'),
        ('k-limbadri.jpg', 'Dr. K. Limbadri', 'Associate Professor'),
        ('pramod-kumar.jpg', 'Dr. Pramod Kumar P', 'Associate Professor'),
        ('lokasani-bhanuprakash.jpg', 'Dr. Lokasani Bhanuprakash', 'Associate Professor'),
        ('alli-anil-kumar.jpg', 'Dr. Alli Anil Kumar', 'Assistant Professor'),
        ('laxmi.jpg', 'Mrs. Laxmi', 'Assistant Professor'),
        ('chintala-muralikrishna.jpg', 'Mr. Chintala Muralikrishna', 'Assistant Professor'),
        ('j-sunil-kumar.jpg', 'Mr. J. Sunil Kumar', 'Assistant Professor'),
        ('j-laxmi-prasad.jpg', 'J. Laxmi Prasad', 'Assistant Professor'),
        ('ne-chandra-prasad.jpg', 'Mr. N E Chandra Prasad', 'Assistant Professor'),
        ('mudhuganti-mahender.jpg', 'Mr. Mudhuganti Mahender', 'Assistant Professor'),
        ('g-chandramohana-reddy.jpg', 'Dr. G. Chandramohana Reddy', 'Assistant Professor'),
        ('m-sundeep.jpg', 'Mr. M. Sundeep', 'Assistant Professor'),
        ('s-nagaraju.jpg', 'Mr. S. Nagaraju', 'Assistant Professor'),
        ('g-anandarao.jpg', 'Mr. G. Anandarao', 'Assistant Professor'),
        ('g-venkata-rambabu.jpg', 'Mr. G. Venkata Rambabu', 'Assistant Professor'),
        ('m-venkateswar-reddy.jpg', 'Mr. M. Venkateswar Reddy', 'Assistant Professor'),
    ],
    'aeronautical': [
        ('satyanarayana.jpg', 'Dr. M. Satyanarayana Gupta', 'HOD & Professor'),
        ('vivek-anand.jpg', 'Dr. A. Vivek Anand', 'Professor & Dean'),
        ('veeranjaneyulu.jpg', 'K. Veeranjaneyulu', 'Professor'),
        ('arvind-singh.jpg', 'Dr. R. Arvind Singh', 'Professor of Eminence'),
        ('s-jayalakshmi.jpg', 'Dr. S. Jayalakshmi', 'Professor of Eminence'),
        ('thangavel-sanjeeviraja.jpeg', 'Dr. Thangavel Sanjeeviraja', 'Associate Professor'),
        ('nayani-uday-ranjan.jpg', 'Nayani Uday Ranjan Goud', 'Associate Professor'),
        ('swetha-bala.jpg', 'Swetha Bala MNVS', 'Associate Professor & Associate Dean'),
        ('saiprakash.jpg', 'Dr. Saiprakash', 'Associate Professor'),
        ('m-ganesh.jpg', 'M. Ganesh', 'Associate Professor'),
        ('yelamasetti-balram.jpg', 'Mr. Yelamasetti Balram', 'Assistant Professor'),
        ('sreekanth-sura.jpg', 'Sreekanth Sura', 'Assistant Professor'),
        ('g-sravanthi.jpeg', 'Ms. G. Sravanthi', 'Assistant Professor'),
        ('b-manideep.jpg', 'Mr. B. Manideep', 'Assistant Professor'),
        ('nirmith-kumar-mishra.jpg', 'Nirmith Kumar Mishra', 'Assistant Professor'),
        ('a-udaya-deepika.jpg', 'A. Udaya Deepika', 'Assistant Professor'),
        ('k-arun-kumar.jpg', 'K. Arun Kumar', 'Assistant Professor'),
        ('b-nagaraj-goud.jpg', 'B. Nagaraj Goud', 'Assistant Professor'),
        ('a-sai-kumar.jpg', 'A. Sai Kumar', 'Assistant Professor'),
    ],
    'mba': [
        ('ramanjaneyulu.jpeg', 'Dr. N. Ramanjaneyulu', 'Professor & HOD'),
        ('narasimha-rao.jpg', 'Dr. M. V. Narasimha Rao', 'Professor'),
        ('aruna.jpg', 'Dr. G. Aruna', 'Professor'),
        ('umrez.jpg', 'M. Umrez', 'Associate Professor'),
        ('m-tirupalaiah.jpg', 'Dr. M. Tirupalaiah', 'Associate Professor'),
        ('jostna-kumar.jpg', 'Dr. Jostna Kumar Gantepogu', 'Assistant Professor'),
        ('vasudha-kurikala.jpg', 'Dr. Vasudha Kurikala', 'Assistant Professor'),
        ('a-koti-reddy.jpg', 'Mr. A. Koti Reddy', 'Assistant Professor'),
        ('m-parsharamulu.jpg', 'Mr. M. Parsharamulu', 'Assistant Professor'),
        ('bs-venkat-narayana.jpg', 'Mr. B. S. Venkat Narayana', 'Assistant Professor'),
        ('b-vishnu-prasad.jpg', 'B. Vishnu Prasad', 'Assistant Professor'),
        ('k-rajya-lakshmi.jpg', 'Dr. K. Rajya Lakshmi', 'Assistant Professor'),
        ('sudha-rani.jpeg', 'Mrs. Sudha Rani N', 'Assistant Professor'),
        ('n-madhusudhanarao.jpg', 'N. Madhusudhanarao', 'Assistant Professor'),
        ('ram-narsa-goud.jpg', 'Mr. Ram Narsa Goud', 'Assistant Professor'),
    ],
}

def gen_initials(name):
    parts = name.replace('Dr.','').replace('Mr.','').replace('Mrs.','').replace('Ms.','').replace('Miss','').replace('Prof.','').strip().split()
    if len(parts) >= 2:
        return parts[0][0].upper() + parts[-1][0].upper()
    return parts[0][:2].upper()

def gen_faculty_html(dept, fac_list):
    cards = []
    for img, name, role in fac_list:
        initials = gen_initials(name)
        safe_name = name.replace('&', '&amp;')
        safe_role = role.replace('&', '&amp;')
        cards.append(f'''          <div class="card faculty-card" data-faculty>
            <div class="faculty-card__photo">
              <img src="images/{dept}/{img}" alt="{safe_name}" onerror="this.style.display=&quot;none&quot;;this.parentElement.textContent=&quot;{initials}&quot;" />
            </div>
            <div class="faculty-card__info">
              <div class="faculty-card__name">{safe_name}</div>
              <div class="faculty-card__role">{safe_role}</div>
            </div>
            <div class="faculty-card__details">
              <p><strong>Designation:</strong> {safe_role}</p>
            </div>
          </div>''')
    return '\n'.join(cards)

for dept, fac_list in faculty.items():
    filepath = f'{base}/{dept}.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    html = gen_faculty_html(dept, fac_list)

    # Replace the faculty grid content
    pattern = r'(<div class="faculty-grid">)\s*(.*?)\s*(</div>\s*</section>)'
    # Find the faculty section
    match = re.search(r'<div class="faculty-grid">(.*?)</div>\s*</section>', content, re.DOTALL)
    if match:
        old_grid = match.group(0)
        new_grid = f'<div class="faculty-grid">\n{html}\n        </div>\n      </section>'
        content = content.replace(old_grid, new_grid)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'{dept}: Updated with {len(fac_list)} faculty')
    else:
        print(f'{dept}: PATTERN NOT FOUND')
