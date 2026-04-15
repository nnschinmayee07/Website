import os, re

base = 'c:/mlr/homepage/departments'

# Compact faculty data: (img, name, role, qual, areas, papers_list)
departments = {
    'ece': [
        ('svs-prasad.jpg', 'Dr. S V S Prasad', 'Professor & HOD', 'Ph.D (Image Processing), M.Tech, B.Tech', 'Image Processing, VLSI, Signal Processing', ['Quantum CNN for Medical Image Segmentation — IEEE Trans. Medical Imaging, 2024', 'GPS Software Receiver Design — Springer, 2023', 'Cryptographic Framework for IoT — Elsevier, 2022']),
        ('shrikant-upadhyay.jpg', 'Dr. Shrikant Upadhyay', 'Associate Professor', 'Ph.D (ECE), M.Tech', 'Embedded Systems, IoT, VLSI', ['Energy Harvesting for IoT Sensor Networks — Elsevier Sustainable Energy, 2024']),
        ('kiran-chand.jpeg', 'Dr. Kiran Chand Ravi', 'Associate Professor', 'Ph.D (ECE), M.Tech', 'Wireless Communications, Signal Processing', ['Deep Learning for Speech Enhancement — IEEE Signal Processing Letters, 2023']),
        ('karthik-reddy.jpg', 'Dr. G. Karthik Reddy', 'Associate Professor', 'Ph.D (ECE), M.Tech', 'Digital Image Processing, Antenna Design', ['mm-Wave Antenna Design for 5G — Microwave & Optical Technology Letters, 2023']),
        ('t-vijetha.jpg', 'Dr. T. Vijetha', 'Associate Professor', 'Ph.D (ECE), M.Tech', 'VLSI Design, Digital Systems', []),
        ('p-yakaiah.jpg', 'Dr. P. Yakaiah', 'Associate Professor', 'Ph.D (ECE), M.Tech', 'Control Systems, Signal Processing', []),
        ('k-nishanth-rao.jpg', 'Dr. K. Nishanth Rao', 'Associate Professor', 'Ph.D (ECE), M.Tech', 'Communication Systems, DSP', []),
        ('rudraram-divya.jpg', 'Rudraram Divya', 'Assistant Professor', 'M.Tech (ECE)', 'VLSI, Embedded Systems', []),
        ('pullela-sravani.jpg', 'Pullela Sravani', 'Assistant Professor', 'M.Tech (ECE)', 'Signal Processing, Communications', []),
        ('nagendra-babu.jpg', 'M. Nagendra Babu', 'Assistant Professor', 'M.Tech (ECE)', 'Microprocessors, Embedded Systems', []),
        ('gv-subba-reddy.jpg', 'G. Venkata Subba Reddy', 'Assistant Professor', 'M.Tech (ECE)', 'Digital Electronics, VLSI', []),
        ('akhila-akula.jpg', 'Akhila Akula', 'Assistant Professor', 'M.Tech (ECE)', 'Communications, Signal Processing', []),
        ('mary-kannidi.jpeg', 'Ms. Mary Kannidi', 'Assistant Professor', 'M.Tech (ECE)', 'Embedded Systems, IoT', []),
        ('s-naveen-kumar.jpg', 'Mr. S. Naveen Kumar', 'Assistant Professor', 'M.Tech (ECE)', 'VLSI, Digital Design', []),
        ('khobragade-pithamber.jpg', 'Mr. Khobragade Pithamber', 'Assistant Professor', 'M.Tech (ECE)', 'Signal Processing, Communications', []),
        ('k-purushotham.jpg', 'Mr. K. Purushotham', 'Assistant Professor', 'M.Tech (ECE)', 'Microprocessors, Embedded C', []),
        ('y-sivaramakrishna.jpg', 'Dr. Y. Sivaramakrishna', 'Assistant Professor', 'Ph.D (ECE)', 'Antenna Design, EM Theory', []),
        ('ganesh-miriyala.jpg', 'Dr. Ganesh Miriyala', 'Assistant Professor', 'Ph.D (ECE)', 'Image Processing, ML', []),
        ('velpula-vijaya-kumar.jpg', 'Dr. Velpula Vijaya Kumar', 'Assistant Professor', 'Ph.D (ECE)', 'VLSI, Low Power Design', []),
        ('sahitya.jpg', 'Mrs. Pinnamaraju Sahitya', 'Assistant Professor', 'M.Tech (ECE)', 'Communications, DSP', []),
        ('sandip-kumar.jpg', 'Mr. Ladi Sandip Kumar Patra', 'Assistant Professor', 'M.Tech (ECE)', 'Embedded Systems, RTOS', []),
        ('vadla-arun-kumar.jpg', 'Mr. Vadla Arun Kumar', 'Assistant Professor', 'M.Tech (ECE)', 'VLSI Design, Verilog', []),
        ('manoj-kumar.jpg', 'Dr. Manoj Kumar', 'Assistant Professor', 'Ph.D (ECE)', 'Wireless Networks, IoT', []),
        ('b-sireesha.jpg', 'Ms. Badepalli Sireesha', 'Assistant Professor', 'M.Tech (ECE)', 'Signal Processing, MATLAB', []),
        ('n-poornima-deepthi.jpg', 'Mrs. N. Poornima Deepthi', 'Assistant Professor', 'M.Tech (ECE)', 'Digital Electronics, Microcontrollers', []),
        ('b-kiran-kumar.jpg', 'Mr. B. Kiran Kumar', 'Assistant Professor', 'M.Tech (ECE)', 'Communication Systems', []),
        ('g-kaushik.jpg', 'Mr. G. Kaushik', 'Assistant Professor', 'M.Tech (ECE)', 'Embedded Systems, ARM', []),
        ('geetha-yerramsetti.jpg', 'Mrs. Geetha Yerramsetti', 'Assistant Professor', 'M.Tech (ECE)', 'VLSI, Digital Design', []),
        ('m-raju-naik.jpg', 'Mr. M. Raju Naik', 'Assistant Professor', 'M.Tech (ECE)', 'Signal Processing', []),
        ('k-maniraj.jpg', 'Mr. K. Maniraj', 'Assistant Professor', 'M.Tech (ECE)', 'Control Systems, Instrumentation', []),
        ('sudhakar-ajmera.jpg', 'Mr. Sudhakar Ajmera', 'Assistant Professor', 'M.Tech (ECE)', 'Microprocessors, Embedded C', []),
        ('b-anusha.jpg', 'Ms. Badepalli Anusha', 'Assistant Professor', 'M.Tech (ECE)', 'Communications, Networks', []),
        ('chinthakindi-babaiah.jpeg', 'Mr. Chinthakindi Babaiah', 'Assistant Professor', 'M.Tech (ECE)', 'Digital Systems, FPGA', []),
        ('rayala-sateesh.jpg', 'Mr. Rayala Sateesh', 'Assistant Professor', 'M.Tech (ECE)', 'DSP, Communications', []),
        ('s-monika.jpg', 'Mrs. S. Monika', 'Assistant Professor', 'M.Tech (ECE)', 'VLSI, Analog Design', []),
        ('k-hari-babu.png', 'Mr. K. Hari Babu', 'Assistant Professor', 'M.Tech (ECE)', 'Embedded Systems, IoT', []),
    ],
    'eee': [
        ('ashok-kumar.jpg', 'Prof. Ashok Kumar Cheeli', 'Professor & HOD', 'M.Tech (Power Systems)', 'Power Systems, Smart Grids, Energy Management', ['Optimal Power Flow in Smart Grids using Meta-heuristic Algorithms — IEEE Power Systems, 2024', 'Fault Detection in Distribution Networks using ML — Elsevier, 2023']),
        ('dileep-kumar.jpg', 'Dr. M. Dileep Kumar', 'Associate Professor', 'Ph.D (EEE), M.Tech', 'Power Electronics, Electric Drives', ['SiC Multilevel Inverter for Solar PV — Power Electronics, Elsevier, 2024', 'Battery Management for EVs — Journal of Energy Storage, 2021']),
        ('placeholder.jpg', 'Ashok Reddy Kanna', 'Associate Professor', 'M.Tech (Power Electronics)', 'Renewable Energy, Power Electronics', ['IoT-enabled Smart Energy Metering — Sustainable Cities & Society, 2023']),
        ('placeholder.jpg', 'K. Usha Rani', 'Associate Professor', 'M.Tech (Control Systems)', 'Control Systems, Instrumentation', ['MPPT Controller for Wind Energy — Renewable Energy, Elsevier, 2022']),
        ('sumana-das.jpeg', 'Dr. Sumana Das', 'Associate Professor', 'Ph.D (EEE), M.Tech', 'Power Quality, Smart Grids', []),
        ('bv-rajanna.jpg', 'Dr. B. V. Rajanna', 'Associate Professor', 'Ph.D (EEE), M.Tech', 'Power Systems, Renewable Energy', []),
        ('t-bhargava-ramu.jpg', 'Dr. T. Bhargava Ramu', 'Associate Professor', 'Ph.D (EEE), M.Tech', 'Electrical Machines, Drives', []),
        ('sonu-kumar.jpeg', 'Dr. Sonu Kumar', 'Assistant Professor', 'Ph.D (EEE)', 'Power Electronics, Converters', []),
        ('y-lalitha-kameswari.jpeg', 'Dr. Y. Lalitha Kameswari', 'Assistant Professor', 'Ph.D (EEE)', 'Control Systems, Robotics', []),
        ('t-mrudula.jpg', 'T. Mrudula', 'Assistant Professor', 'M.Tech (EEE)', 'Power Systems, Protection', []),
        ('n-karthik.jpg', 'N. Karthik', 'Assistant Professor', 'M.Tech (EEE)', 'Electrical Machines', []),
        ('p-jithendar.jpg', 'P. Jithendar', 'Assistant Professor', 'M.Tech (EEE)', 'Power Electronics', []),
        ('a-yadagiri.jpg', 'A. Yadagiri', 'Assistant Professor', 'M.Tech (EEE)', 'Control Systems', []),
        ('k-rajasri.jpg', 'K. Rajasri', 'Assistant Professor', 'M.Tech (EEE)', 'Electrical Measurements', []),
        ('a-shubhangi-rao.jpg', 'A. Shubhangi Rao', 'Assistant Professor', 'M.Tech (EEE)', 'Power Systems', []),
        ('ch-srivardhan-kumar.jpg', 'Dr. CH. Srivardhan Kumar', 'Assistant Professor', 'Ph.D (EEE)', 'Renewable Energy, Solar PV', []),
        ('m-sreenivasa-reddy.jpg', 'M. Sreenivasa Reddy', 'Associate Professor', 'M.Tech (EEE)', 'Electrical Machines, Drives', []),
    ],
    'mechanical': [
        ('krishnaraj.jpg', 'Dr. J. Krishnaraj', 'Professor & HOD', 'Ph.D (Mech), M.Tech', 'Composite Materials, NDT, Welding', ['Friction Stir Welding Parameter Optimization — Journal of Manufacturing Processes, 2024', 'Fatigue Life of Composite Laminates — Composite Structures, 2023']),
        ('prabhu-kishore.jpeg', 'Dr. N. Prabhu Kishore', 'Associate Professor', 'Ph.D (Thermal), M.Tech', 'Heat Transfer, IC Engines, Thermal', ['Thermal Analysis of PCM for Solar Storage — Applied Thermal Engineering, 2024', 'Biodiesel Blends in CI Engines — Fuel, Elsevier, 2021']),
        ('ravi-kiran.jpg', 'Dr. Ch. Ravi Kiran', 'Associate Professor', 'Ph.D (Mech), M.Tech', 'Manufacturing, CAD/CAM', ['CNC Machining Optimization using GRA — Materials Today, 2023']),
        ('harikishor.jpg', 'Dr. Harikishor Kumar', 'Associate Professor', 'Ph.D (Design), M.Tech', 'Machine Design, FEM', ['Topology Optimization of Automotive Bracket — Finite Elements in Analysis & Design, 2022']),
        ('k-limbadri.jpg', 'Dr. K. Limbadri', 'Associate Professor', 'Ph.D (Mech), M.Tech', 'Manufacturing, Industrial Engg', []),
        ('pramod-kumar.jpg', 'Dr. Pramod Kumar P', 'Associate Professor', 'Ph.D (Mech), M.Tech', 'Thermal Engineering, CFD', []),
        ('lokasani-bhanuprakash.jpg', 'Dr. Lokasani Bhanuprakash', 'Associate Professor', 'Ph.D (Mech), M.Tech', 'Material Science, Composites', []),
        ('alli-anil-kumar.jpg', 'Dr. Alli Anil Kumar', 'Assistant Professor', 'Ph.D (Mech)', 'Manufacturing, Additive Mfg', []),
        ('laxmi.jpg', 'Mrs. Laxmi', 'Assistant Professor', 'M.Tech (Mech)', 'Thermal Engineering', []),
        ('chintala-muralikrishna.jpg', 'Mr. Chintala Muralikrishna', 'Assistant Professor', 'M.Tech (Mech)', 'CAD/CAM, Machine Design', []),
        ('j-sunil-kumar.jpg', 'Mr. J. Sunil Kumar', 'Assistant Professor', 'M.Tech (Mech)', 'Automobile Engineering', []),
        ('j-laxmi-prasad.jpg', 'J. Laxmi Prasad', 'Assistant Professor', 'M.Tech (Mech)', 'Fluid Mechanics, Hydraulics', []),
        ('ne-chandra-prasad.jpg', 'Mr. N E Chandra Prasad', 'Assistant Professor', 'M.Tech (Mech)', 'Manufacturing Processes', []),
        ('mudhuganti-mahender.jpg', 'Mr. Mudhuganti Mahender', 'Assistant Professor', 'M.Tech (Mech)', 'IC Engines, Automobile', []),
        ('g-chandramohana-reddy.jpg', 'Dr. G. Chandramohana Reddy', 'Assistant Professor', 'Ph.D (Mech)', 'FEM, Structural Analysis', []),
        ('m-sundeep.jpg', 'Mr. M. Sundeep', 'Assistant Professor', 'M.Tech (Mech)', 'Thermal Engineering', []),
        ('s-nagaraju.jpg', 'Mr. S. Nagaraju', 'Assistant Professor', 'M.Tech (Mech)', 'Production Engineering', []),
        ('g-anandarao.jpg', 'Mr. G. Anandarao', 'Assistant Professor', 'M.Tech (Mech)', 'Machine Design', []),
        ('g-venkata-rambabu.jpg', 'Mr. G. Venkata Rambabu', 'Assistant Professor', 'M.Tech (Mech)', 'Manufacturing, CNC', []),
        ('m-venkateswar-reddy.jpg', 'Mr. M. Venkateswar Reddy', 'Assistant Professor', 'M.Tech (Mech)', 'Robotics, Automation', []),
    ],
    'aeronautical': [
        ('satyanarayana.jpg', 'Dr. M. Satyanarayana Gupta', 'HOD & Professor', 'Ph.D (Aerospace), M.Tech', 'CFD, Aerodynamics, Turbulence', ['CFD Analysis of Morphing Wing for UAV — Aerospace Science & Technology, 2024', 'Autonomous Navigation for Quadcopter — Drones MDPI, 2021']),
        ('vivek-anand.jpg', 'Dr. A. Vivek Anand', 'Professor & Dean', 'Ph.D (Aerospace), M.Tech', 'Propulsion, Gas Turbines, Composites', ['Additive Manufacturing of Lattice Structures — Materials & Design, 2024', 'Turbine Blade Cooling Optimization — Applied Thermal Engg, 2023']),
        ('veeranjaneyulu.jpg', 'K. Veeranjaneyulu', 'Professor', 'M.Tech (Aerospace)', 'Aircraft Structures, FEM', ['SHM of Composite Aircraft Panels — Smart Materials & Structures, 2023']),
        ('arvind-singh.jpg', 'Dr. R. Arvind Singh', 'Professor of Eminence', 'Ph.D (Aeronautical)', 'Flight Dynamics, Control Systems', ['Flutter Analysis of High-Aspect-Ratio Wings — J. Fluids & Structures, 2022']),
        ('s-jayalakshmi.jpg', 'Dr. S. Jayalakshmi', 'Professor of Eminence', 'Ph.D', 'Aerospace Materials, NDT', []),
        ('thangavel-sanjeeviraja.jpeg', 'Dr. Thangavel Sanjeeviraja', 'Associate Professor', 'Ph.D', 'CFD, Heat Transfer', []),
        ('nayani-uday-ranjan.jpg', 'Nayani Uday Ranjan Goud', 'Associate Professor', 'M.Tech (Aerospace)', 'Aircraft Design, Aerodynamics', []),
        ('swetha-bala.jpg', 'Swetha Bala MNVS', 'Associate Professor & Associate Dean', 'M.Tech (Aerospace)', 'Structures, Composites', []),
        ('saiprakash.jpg', 'Dr. Saiprakash', 'Associate Professor', 'Ph.D', 'Propulsion, Combustion', []),
        ('m-ganesh.jpg', 'M. Ganesh', 'Associate Professor', 'M.Tech (Aerospace)', 'Flight Mechanics, Avionics', []),
        ('yelamasetti-balram.jpg', 'Mr. Yelamasetti Balram', 'Assistant Professor', 'M.Tech (Aerospace)', 'CFD, Aerodynamics', []),
        ('sreekanth-sura.jpg', 'Sreekanth Sura', 'Assistant Professor', 'M.Tech (Aerospace)', 'Aircraft Structures', []),
        ('g-sravanthi.jpeg', 'Ms. G. Sravanthi', 'Assistant Professor', 'M.Tech (Aerospace)', 'Avionics, Control Systems', []),
        ('b-manideep.jpg', 'Mr. B. Manideep', 'Assistant Professor', 'M.Tech (Aerospace)', 'Propulsion, Gas Turbines', []),
        ('nirmith-kumar-mishra.jpg', 'Nirmith Kumar Mishra', 'Assistant Professor', 'M.Tech (Aerospace)', 'UAV Systems, Drones', []),
        ('a-udaya-deepika.jpg', 'A. Udaya Deepika', 'Assistant Professor', 'M.Tech (Aerospace)', 'Aircraft Design', []),
        ('k-arun-kumar.jpg', 'K. Arun Kumar', 'Assistant Professor', 'M.Tech (Aerospace)', 'Space Mechanics, Orbital', []),
        ('b-nagaraj-goud.jpg', 'B. Nagaraj Goud', 'Assistant Professor', 'M.Tech (Aerospace)', 'Structures, Composites', []),
        ('a-sai-kumar.jpg', 'A. Sai Kumar', 'Assistant Professor', 'M.Tech (Aerospace)', 'CFD, Fluid Mechanics', []),
    ],
    'mba': [
        ('ramanjaneyulu.jpeg', 'Dr. N. Ramanjaneyulu', 'Professor & HOD', 'Ph.D (Management), MBA', 'Strategic Management, Leadership, OB', ['Impact of Digital Transformation on SME Performance — Intl. Journal of Management Studies, 2024', 'Sustainable Supply Chain in Indian Manufacturing — J. Cleaner Production, 2021']),
        ('narasimha-rao.jpg', 'Dr. M. V. Narasimha Rao', 'Professor', 'Ph.D (Finance), MBA', 'Financial Management, Banking, Fintech', ['Behavioral Finance and Investment Decisions — J. Financial Economics, 2024', 'Fintech Adoption among Urban Consumers — Electronic Commerce Research, 2022']),
        ('aruna.jpg', 'Dr. G. Aruna', 'Professor', 'Ph.D (Marketing), MBA', 'Marketing, Consumer Behaviour, Digital', ['Social Media Marketing for D2C Brands — J. Marketing Communications, 2023']),
        ('umrez.jpg', 'M. Umrez', 'Associate Professor', 'MBA, (Ph.D)', 'HR Management, OB, Training', ['Employee Engagement Post-Pandemic in IT — HR Management Review, 2023']),
        ('m-tirupalaiah.jpg', 'Dr. M. Tirupalaiah', 'Associate Professor', 'Ph.D (Management), MBA', 'Operations, Quality Management', []),
        ('jostna-kumar.jpg', 'Dr. Jostna Kumar Gantepogu', 'Assistant Professor', 'Ph.D (Management)', 'Entrepreneurship, Innovation', []),
        ('vasudha-kurikala.jpg', 'Dr. Vasudha Kurikala', 'Assistant Professor', 'Ph.D (Management)', 'Finance, Investment Analysis', []),
        ('a-koti-reddy.jpg', 'Mr. A. Koti Reddy', 'Assistant Professor', 'MBA', 'Marketing, Sales Management', []),
        ('m-parsharamulu.jpg', 'Mr. M. Parsharamulu', 'Assistant Professor', 'MBA', 'HR, Organizational Development', []),
        ('bs-venkat-narayana.jpg', 'Mr. B. S. Venkat Narayana', 'Assistant Professor', 'MBA', 'Finance, Accounting', []),
        ('b-vishnu-prasad.jpg', 'B. Vishnu Prasad', 'Assistant Professor', 'MBA', 'Operations, Supply Chain', []),
        ('k-rajya-lakshmi.jpg', 'Dr. K. Rajya Lakshmi', 'Assistant Professor', 'Ph.D (Management)', 'HR, Training & Development', []),
        ('sudha-rani.jpeg', 'Mrs. Sudha Rani N', 'Assistant Professor', 'MBA', 'Marketing, Digital Marketing', []),
        ('n-madhusudhanarao.jpg', 'N. Madhusudhanarao', 'Assistant Professor', 'MBA', 'Finance, Taxation', []),
        ('ram-narsa-goud.jpg', 'Mr. Ram Narsa Goud', 'Assistant Professor', 'MBA', 'Business Analytics, IT', []),
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
        sn = name.replace('&', '&amp;').replace('"', '&quot;').replace("'", '&#39;')
        sr = role.replace('&', '&amp;')
        area_tags = ''.join(f'<span class="faculty-popup__tag">{a.strip()}</span>' for a in areas.split(',')[:4])
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

# New CSS to inject
new_css = '''    /* ── Faculty Memory Lane ── */
    .faculty-lane {
      display: flex;
      gap: 28px;
      overflow-x: auto;
      padding: 20px 0 32px;
      scroll-behavior: smooth;
      -webkit-overflow-scrolling: touch;
    }
    .faculty-lane::-webkit-scrollbar { height: 6px; }
    .faculty-lane::-webkit-scrollbar-track { background: rgba(0,0,0,0.04); border-radius: 3px; }
    .faculty-lane::-webkit-scrollbar-thumb { background: rgba(24,69,59,0.2); border-radius: 3px; }
    .faculty-item { flex-shrink: 0; width: 120px; text-align: center; position: relative; cursor: pointer; }
    .faculty-item__photo {
      width: 90px; height: 90px; border-radius: 50%; margin: 0 auto 10px;
      background: linear-gradient(135deg, #2A2F40, #3A4050); overflow: hidden;
      border: 3px solid transparent; transition: border-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
      display: flex; align-items: center; justify-content: center;
      color: rgba(255,255,255,0.3); font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 1.1rem;
    }
    .faculty-item__photo img { width: 100%; height: 100%; object-fit: cover; }
    .faculty-item:hover .faculty-item__photo {
      border-color: #E85D1F; transform: scale(1.08); box-shadow: 0 4px 20px rgba(232,93,31,0.25);
    }
    .faculty-item__name { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.72rem; color: #0B0F1A; line-height: 1.3; margin-bottom: 2px; }
    .faculty-item__role { font-family: 'Raleway', sans-serif; font-size: 0.62rem; color: #888; font-weight: 600; letter-spacing: 0.04em; }
    .faculty-popup {
      display: none; position: absolute; bottom: calc(100% + 12px); left: 50%; transform: translateX(-50%);
      width: 300px; background: #fff; border-radius: 12px; box-shadow: 0 8px 32px rgba(0,0,0,0.15);
      padding: 20px; z-index: 50; text-align: left; border-top: 3px solid #18453B;
    }
    .faculty-popup::after {
      content: ''; position: absolute; bottom: -8px; left: 50%; transform: translateX(-50%);
      width: 16px; height: 8px; background: #fff; clip-path: polygon(0 0, 100% 0, 50% 100%);
    }
    .faculty-item:hover .faculty-popup { display: block; animation: popIn 0.25s ease; }
    @keyframes popIn { from { opacity: 0; transform: translateX(-50%) translateY(6px); } to { opacity: 1; transform: translateX(-50%) translateY(0); } }
    .faculty-popup__name { font-family: 'Playfair Display', serif; font-weight: 700; font-size: 1rem; color: #0B0F1A; margin-bottom: 4px; }
    .faculty-popup__role { font-size: 0.72rem; color: #E85D1F; font-weight: 600; margin-bottom: 10px; }
    .faculty-popup__detail { font-size: 0.78rem; color: #555; margin-bottom: 4px; line-height: 1.4; }
    .faculty-popup__detail strong { color: #18453B; font-weight: 700; }
    .faculty-popup__tag { display: inline-block; font-family: 'Raleway', sans-serif; font-size: 0.62rem; font-weight: 700; color: #18453B; background: rgba(24,69,59,0.08); padding: 2px 8px; border-radius: 4px; margin: 2px 2px 0 0; letter-spacing: 0.04em; }
    .faculty-popup__papers { margin-top: 10px; padding-top: 10px; border-top: 1px solid rgba(0,0,0,0.06); }
    .faculty-popup__papers-title { font-family: 'Raleway', sans-serif; font-weight: 700; font-size: 0.68rem; color: #18453B; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 6px; }
    .faculty-popup__paper { font-size: 0.72rem; color: #555; line-height: 1.4; margin-bottom: 4px; padding-left: 10px; border-left: 2px solid rgba(232,93,31,0.3); }'''

for dept, fac_list in departments.items():
    filepath = f'{base}/{dept}.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    html = gen_memory_lane(dept, fac_list)

    # 1. Replace old faculty CSS with new memory lane CSS
    old_css_pattern = r'/\* ── Faculty ── \*/.*?\.faculty-card__role \{[^}]+\}'
    if re.search(old_css_pattern, content, re.DOTALL):
        content = re.sub(old_css_pattern, new_css, content, flags=re.DOTALL)

    # 2. Remove old expandable faculty CSS if present
    content = re.sub(r'/\* ── Faculty expandable ── \*/.*?\.faculty-card__details p \{[^}]+\}', '', content, flags=re.DOTALL)

    # 3. Replace faculty-grid responsive rule
    content = content.replace('.faculty-grid { grid-template-columns: 1fr; }', '.faculty-lane { gap: 16px; }\n      .faculty-popup { width: 260px; }')

    # 4. Replace faculty HTML
    match = re.search(r'(<section class="dept-section" id="faculty">.*?<h2 class="dept-section__heading">Faculty Profiles</h2>\s*)<div class="faculty-grid">.*?</div>\s*</section>', content, re.DOTALL)
    if match:
        prefix = match.group(1)
        new_section = f'''{prefix}<div class="faculty-lane">
{html}
          </div>
      </section>'''
        content = content[:match.start()] + new_section + content[match.end():]

    # 5. Remove faculty expand JS if present
    content = re.sub(r'\s*// ── Faculty card expand/collapse ──\s*\(function \(\) \{.*?document\.querySelectorAll\(\'\[data-faculty\]\'\).*?\}\)\(\);', '', content, flags=re.DOTALL)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'{dept}: Memory lane with {len(fac_list)} faculty')
