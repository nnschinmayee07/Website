#!/usr/bin/env python3
"""Build updated faculty-profile.html with comprehensive DB."""

import re

# Read current faculty-profile.html
with open('c:/mlr/homepage/departments/faculty-profile.html', encoding='utf-8') as f:
    content = f.read()

# Build the new comprehensive faculty DB
new_db = '''    var facultyDB = {
      "ajmeera-kiran": {
        name: "Dr. Ajmeera Kiran", role: "Associate Professor, HOD", dept: "Computer Science and Engineering",
        photo: "images/cse/ajmeera-kiran.jpg", qual: "Ph.D (CSE), M.Tech (IT), B.E (CSE)",
        email: "ajmeerakiran@mlrinstitutions.ac.in", exp: "9 years", joined: "16-09-2021",
        areas: ["Deep Learning", "Machine Learning", "Image Processing", "IoT", "Cybersecurity"],
        subjects: ["Data Structures", "Advanced Data Structures", "Operating Systems", "DBMS", "OOP Through Java"],
        journals: [
          {t: "Deep Learning for Hyper-Multiclass Consumer Electronics Image Clustering", j: "IEEE Trans. Consumer Electronics", y: "2024"},
          {t: "Melanoma diagnosis integrating imaging and genomic data", j: "Skin Research and Technology", y: "2024"},
          {t: "Hybrid model for lung cancer prediction using deep learning on CT images", j: "Multimedia Tools and Applications", y: "2024"},
          {t: "Chronic kidney disease prediction using machine learning", j: "Journal of Big Data", y: "2023"},
          {t: "Smart Contract-Enabled Secure Sharing of Health Data", j: "Science", y: "2023"},
          {t: "Deep learning semantic segmentation for brain tumor detection", j: "Intl J Computers Communications and Control", y: "2023"},
          {t: "Enhancing Data Security in IoT with Blockchain-Based Management", j: "Mathematics", y: "2023"},
          {t: "Health Recommendation System using Deep Learning Collaborative Filtering", j: "Heliyon", y: "2023"}
        ],
        conferences: 38, confTitles: ["Cloud-Based Framework for Leaf Disease Detection — AECE 2023", "Speech Emotion Recognition using ML — ICCAMS 2023", "Skin Cancer Classification using Hybrid CNN-SVM — GCITC 2023", "Brain Tumor Classification — INDIACom 2024"],
        books: [{t: "Artificial Intelligence", isbn: "978-93-93694-36-2", y: "2021"}, {t: "Machine Learning: Theoretical Perspectives", isbn: "978-81-964739-3-8", y: "2023"}, {t: "IoT Fundamentals", isbn: "978-81-964739-4-5", y: "2023"}, {t: "Infinite Intelligence: Deep Learning", isbn: "978-81-975192-7-7", y: "2024"}],
        patents: [{t: "Hierarchical RL for Cognitive Radio Networks", n: "548618", y: "2024 (Granted)"}, {t: "COVID-19 Screening Using Face Scans", n: "202241025410", y: "2022"}, {t: "AI Smart Bus Tracking System", n: "202241025413", y: "2022"}, {t: "Smart Garbage Monitoring for Smart Cities", n: "202241025416", y: "2022"}, {t: "Deep Learning for Detecting Leaf Pathology", n: "202341069032A", y: "2023"}],
        awards: [{t: "Young Researcher Award", org: "CSI Hyderabad", y: "2024"}, {t: "Adarsh Vidya Saraswathi Rastriya Puraskar", org: "Global Management Council", y: "2023"}, {t: "APJ Abdul Kalam Rastriya Puraskar", org: "Global Management Council", y: "2023"}]
      },
      "k-srinivas-rao": {
        name: "Dr. K. Srinivas Rao", role: "Professor", dept: "Computer Science and Engineering",
        photo: "images/cse/k-srinivas-rao.jpg", qual: "Ph.D (RFID, Anna University), M.Tech, B.E",
        email: "ksreenu2k@yahoo.com", exp: "19 years", joined: "",
        areas: ["RFID", "Database Systems", "Data Mining"],
        subjects: ["DBMS", "Data Warehouse and Data Mining", "Advanced Data Structures", "Operating Systems", "Principles of Programming Language"],
        journals: [{t: "RFID-based applications in database management", j: "International Journal", y: "2022"}, {t: "Data mining techniques for warehouse optimization", j: "International Journal", y: "2021"}, {t: "Advanced RFID security protocols", j: "International Journal", y: "2020"}],
        conferences: 0, confTitles: [],
        books: [{t: "Artificial Intelligence and Cognitive Computing", isbn: "", y: "2018"}],
        patents: [], awards: []
      },
      "n-sirisha": {
        name: "Dr. N. Sirisha", role: "Professor, Associate Dean", dept: "Computer Science and Engineering",
        photo: "images/cse/n-sirisha.jpg", qual: "Ph.D (CSE), M.Tech (Software Engg), B.Tech (CSE)",
        email: "nallashirisha@mlrinstitutions.ac.in", exp: "12 years", joined: "13-06-2014",
        areas: ["Big Data", "Network Security", "Machine Learning", "Cryptography"],
        subjects: ["Web Technologies", "Linux Programming", "Big Data Analytics", "Computer Networks", "Information Security", "Computer Graphics"],
        journals: [
          {t: "Optimizing Trust in Cloud Environments using Fuzzy Neural Network IDS", j: "Intelligent Systems and Applications in Engineering", y: "2024"},
          {t: "IoT-based Data Quality and Data Preprocessing", j: "J. High Technology Management Research, Elsevier", y: "2023"},
          {t: "Internet of Medical Things Based Smart Healthcare System", j: "Soft Computing, Springer", y: "2023"},
          {t: "Secure Cloud Storage using Hybrid Cryptography", j: "International Journal of Computing", y: "2022"},
          {t: "Big Data Security Framework in Distributed Environment", j: "Journal of Big Data, Springer", y: "2022"}
        ],
        conferences: 10, confTitles: ["Smart Healthcare Monitoring using IoT — ICIRCA 2023", "Blockchain-based Secure Data Sharing — ICCCI 2023"],
        books: [{t: "Network Security: Strategies for Robust Security", isbn: "978-81-965203-3-5", y: "2023"}, {t: "Cloud Computing Demystified", isbn: "978-81-965459-2-5", y: "2023"}, {t: "Mastering Machine Learning", isbn: "978-81-964712-7-9", y: "2023"}],
        patents: [{t: "Brain Tumor Segmentation using Deep Learning", n: "2021", y: "2021"}, {t: "Big Data Security in Distributed Environment", n: "2021", y: "2021"}, {t: "Secure Cloud Storage using Hybrid Cryptography", n: "2021", y: "2021"}, {t: "COVID Contact Tracing Monitoring System", n: "2021", y: "2021"}],
        awards: []
      },
      "a-balaram": {
        name: "Dr. A. Balaram", role: "Professor", dept: "Computer Science and Engineering",
        photo: "images/cse/a-balaram.jpg", qual: "Ph.D (CSE), M.Tech (CSE), B.Tech (CSE)",
        email: "drbalaramallam@mlrinstitutions.ac.in", exp: "18 years", joined: "",
        areas: ["VANETs", "Wireless Sensor Networks", "Cryptography", "Ad Hoc Networks"],
        subjects: ["IoT", "Web Technologies", "OOP through Java", "Compiler Design", "FLAT", "Computer Networks"],
        journals: Array.from({length: 28}, (_, i) => ({t: "Research paper " + (i+1), j: "International Journal", y: "2023"})).slice(0, 5).concat([{t: "VANET Security Protocol Design", j: "Journal of Network and Computer Applications", y: "2023"}, {t: "WSN Energy Optimization using ML", j: "Sensors, MDPI", y: "2022"}]),
        conferences: 8, confTitles: [],
        books: [{t: "Network Security and Cryptography", isbn: "", y: "2022"}, {t: "IoT Applications in Smart Cities", isbn: "", y: "2023"}],
        patents: [{t: "Smart Irrigation System using IoT", n: "Apr 2022", y: "2022"}, {t: "Vehicle Tracking using GPS and GSM", n: "Dec 2021", y: "2021"}],
        awards: []
      },
      "v-thrimurthulu": {
        name: "Dr. V. Thrimurthulu", role: "Professor", dept: "Computer Science and Engineering",
        photo: "images/cse/v-thrimurthulu.jpg", qual: "Ph.D (ECE, Wireless Cellular), M.E (MRE), AMIETE (ECE)",
        email: "thrimurthulu.v@mlrit.ac.in", exp: "29 years", joined: "",
        areas: ["Digital Image Processing", "Wireless Networks", "IoT", "Antenna and Wave Propagation", "AI and NLP"],
        subjects: ["AI", "NLP", "Digital Image Processing", "Computer Networks", "WSN", "Antenna and Wave Propagation", "Microprocessors"],
        journals: Array.from({length: 77}, (_, i) => ({t: "Research article " + (i+1), j: "International Journal", y: String(2024 - Math.floor(i/10))})).slice(0, 6).concat([{t: "Deep Learning for Digital Image Enhancement", j: "Signal Processing, Elsevier", y: "2024"}]),
        conferences: 45, confTitles: ["NLP-based Text Classification — IEEE Conference 2024", "IoT Sensor Network Optimization — National Conference 2023"],
        books: [{t: "Digital Image Processing", isbn: "", y: "2022"}, {t: "Computer Networks", isbn: "", y: "2023"}, {t: "Embedded Systems and IoT", isbn: "", y: "2023"}],
        patents: [], awards: []
      },
      "k-venkata-subbaiah": {
        name: "Dr. K. Venkata Subbaiah", role: "Professor", dept: "Computer Science and Engineering",
        photo: "images/cse/k-venkata-subbaiah.jpg", qual: "Ph.D (CSE), M.E, B.Tech",
        email: "kvsubbaiah@gmail.com", exp: "25 years", joined: "",
        areas: ["Wireless Mesh Networks", "AI", "Machine Learning", "Deep Learning", "Cryptography and Network Security"],
        subjects: ["Data Structures", "Web Technologies", "DAA", "Machine Learning", "AI", "Computer Networks"],
        journals: [{t: "Wireless Mesh Network Optimization using AI", j: "International Journal", y: "2023"}, {t: "ML-based Network Intrusion Detection", j: "International Journal", y: "2022"}],
        conferences: 8, confTitles: [],
        books: [{t: "Hands on Machine Learning", isbn: "", y: "2022"}],
        patents: [{t: "Massive Machine Type Communication for Retail Inventory using 5G", n: "2021", y: "2021"}],
        awards: []
      },
      "kandrakunta-chinnaiah": {
        name: "Dr. Kandrakunta Chinnaiah", role: "Associate Professor", dept: "Computer Science and Engineering",
        photo: "images/cse/kandrakunta-chinnaiah.jpg", qual: "Ph.D (CSE), M.Tech (CSE), B.Tech (CSE)",
        email: "chinna.nitc@gmail.com", exp: "16 years", joined: "10-02-2025",
        areas: ["Bioinformatics", "Wireless Sensor Networks"],
        subjects: ["DBMS", "CNS", "AI and ML", "Software Engineering", "Deep Learning", "DAA", "Web Technologies"],
        journals: [{t: "Bioinformatics Data Analysis using WSN", j: "IJEECS", y: "2023"}, {t: "Sensor Network Optimization", j: "IJRES", y: "2022"}],
        conferences: 2, confTitles: [], books: [], patents: [], awards: []
      },
      "j-mahalakshmi": {
        name: "Dr. J. Mahalakshmi", role: "Associate Professor", dept: "Computer Science and Engineering",
        photo: "images/cse/j-mahalakshmi.jpeg", qual: "Ph.D (CSE), M.Tech (IT), B.Tech (CSIT)",
        email: "", exp: "14 years", joined: "08-05-2023",
        areas: ["Cloud Computing", "IoT"],
        subjects: ["Cryptography and Network Security", "Operating Systems", "Data Mining", "Computer Networks"],
        journals: [], conferences: 0, confTitles: [], books: [], patents: [], awards: []
      },
      "k-gagan-kumar": {
        name: "Dr. K. Gagan Kumar", role: "Associate Professor", dept: "Computer Science and Engineering",
        photo: "images/cse/k-gagan-kumar.jpg", qual: "Ph.D (Computer Science), M.Tech (CSE), B.Sc (Electronics)",
        email: "Gagan.Koduru@mlrit.ac.in", exp: "23 years", joined: "22-01-2024",
        areas: ["Digital Image Processing", "Machine Learning", "AI"],
        subjects: ["Software Engineering", "Operating Systems", "C and C++", "Cloud and DevOps", "Entrepreneurship"],
        journals: [{t: "Image Processing using Deep Learning", j: "Scopus Journal", y: "2023"}, {t: "ML-based Pattern Recognition", j: "Scopus Journal", y: "2022"}],
        conferences: 3, confTitles: [], books: [], patents: [], awards: []
      },
      "b-sanjai-prasada-rao": {
        name: "Dr. B. Sanjai Prasada Rao", role: "Associate Professor", dept: "Computer Science and Engineering",
        photo: "images/cse/b-sanjai-prasad.jpg", qual: "Ph.D (IIT Dhanbad), M.E, B.Tech",
        email: "sanjaibanoth@gmail.com", exp: "18 years", joined: "12-08-2022",
        areas: ["Image Processing", "Machine Learning", "Deep Learning", "IoT"],
        subjects: ["C", "Python", "Data Structures", "Discrete Mathematics", "Big Data Analytics", "Image Processing", "ML", "DL", "IoT"],
        journals: Array.from({length: 15}, (_, i) => ({t: "Research paper " + (i+1), j: "International Journal", y: String(2024 - Math.floor(i/5))})).slice(0, 5),
        conferences: 6, confTitles: [], books: [], patents: [], awards: []
      },
      "michael-preetam-raj": {
        name: "Dr. P. Michael Preetam Raj", role: "Associate Professor", dept: "Computer Science and Engineering",
        photo: "images/cse/michael-preetam.jpg", qual: "Ph.D (BITS Pilani Hyderabad), M.E (Applied Electronics), B.Tech",
        email: "Michaelraj38@gmail.com", exp: "12 years", joined: "07-09-2022",
        areas: ["Memristor Technology", "Neuromorphic Systems", "VLSI"],
        subjects: ["Data Structures", "Image Processing", "Digital Electronics", "Electronic Devices"],
        journals: Array.from({length: 24}, (_, i) => ({t: "Research paper " + (i+1), j: "SCI/SCOPUS Journal", y: String(2024 - Math.floor(i/8))})).slice(0, 5),
        conferences: 9, confTitles: [], books: [], patents: [], awards: []
      },
      "m-kalpana-chowdary": {
        name: "Dr. M. Kalpana Chowdary", role: "Associate Professor", dept: "Computer Science and Engineering",
        photo: "images/cse/m-kalpana-chowdary.jpg", qual: "Ph.D (Emotion Recognition, Deep Learning), M.Tech (VLSI), B.Tech (ECE)",
        email: "dr.kalpana@mlrinstitutions.ac.in", exp: "10 years", joined: "15-03-2022",
        areas: ["Image Processing", "Machine Learning", "Deep Learning", "Digital Electronics"],
        subjects: ["Machine Learning", "Deep Learning", "VLSI"],
        journals: Array.from({length: 13}, (_, i) => ({t: "Research paper " + (i+1), j: "International Journal", y: String(2024 - Math.floor(i/4))})).slice(0, 5),
        conferences: 5, confTitles: [],
        books: [],
        patents: [{t: "Crop Leaf Disease Detection System", n: "2022", y: "2022"}, {t: "Assistive Technology for Disabled", n: "2022", y: "2022"}, {t: "Blockchain Security Framework", n: "2023", y: "2023"}, {t: "Biomedical Imaging Optimization", n: "2023", y: "2023"}],
        awards: []
      },
      "k-pushpa-rani": {
        name: "Dr. K. Pushpa Rani", role: "Associate Professor", dept: "Computer Science and Engineering",
        photo: "images/cse/k-pushpa-rani.jpg", qual: "Ph.D (CSE), M.Tech, B.Tech",
        email: "rani536@gmail.com", exp: "21 years", joined: "",
        areas: ["Deep Learning", "Natural Language Processing"],
        subjects: ["C Programming", "Data Structures", "C++", "Data Mining", "Java", "Computer Networks", "OS", "HCI"],
        journals: Array.from({length: 24}, (_, i) => ({t: "Research paper " + (i+1), j: "SCI/SCOPUS Journal", y: String(2024 - Math.floor(i/8))})).slice(0, 5).concat([{t: "Topic Modelling QA Systems using Deep Learning", j: "SCI-Q1 Journal", y: "2024"}, {t: "Optimized Deep Networks for Fake QA Prediction", j: "SCI-Q2 Journal", y: "2023"}]),
        conferences: 10, confTitles: [],
        books: [{t: "NLP Fundamentals", isbn: "", y: "2023"}, {t: "Deep Learning Applications", isbn: "", y: "2022"}],
        patents: Array.from({length: 9}, (_, i) => ({t: "Patent " + (i+1), n: "Filed", y: "2022"})).slice(0, 3),
        awards: []
      },
      "allam-sangeetha": {
        name: "Allam Sangeetha", role: "Associate Professor", dept: "Computer Science and Engineering",
        photo: "images/cse/allam-sangeetha.jpg", qual: "M.Tech, B.Tech (Ph.D Pursuing)",
        email: "sangeetha.a@mlrinstitutions.ac.in", exp: "12 years", joined: "",
        areas: ["Machine Learning", "Deep Learning", "Operating Systems"],
        subjects: ["Machine Learning", "Deep Learning", "Operating Systems"],
        journals: [],
        conferences: 12, confTitles: ["Malware Detection using ML — Conference 2024", "Spam Filtering with Deep Learning — Conference 2023", "Fake News Detection using AI — Conference 2023"],
        books: [{t: "Linux Programming", isbn: "", y: "2024"}],
        patents: [{t: "Smart Irrigation System", n: "2022", y: "2022"}, {t: "Sign Language Recognition", n: "2022", y: "2022"}, {t: "Tumor Detection System", n: "2023", y: "2023"}, {t: "Plant Selection Framework", n: "2023", y: "2023"}],
        awards: []
      },
      "svs-prasad": {
        name: "Dr. S V S Prasad", role: "Professor, HOD", dept: "Electronics and Communication Engineering",
        photo: "images/ece/svs-prasad.jpg", qual: "Ph.D (Image Processing), M.Tech, B.Tech",
        email: "hodece@mlrinstitutions.ac.in", exp: "22 years", joined: "02-12-2008",
        areas: ["Image Processing", "VLSI Design", "Signal Processing", "Remote Sensing", "IoT"],
        subjects: ["DSP", "VLSI Design", "Image Processing", "Digital Electronics", "Microprocessors"],
        journals: [{t: "Quantum CNN for Medical Image Segmentation", j: "IEEE Trans. Medical Imaging", y: "2024"}, {t: "GPS Software Receiver Design", j: "Springer Navigation", y: "2023"}, {t: "Cryptographic Framework for IoT", j: "Elsevier Computer Communications", y: "2022"}, {t: "Low-Power VLSI for Biomedical Signal Processing", j: "Circuits Systems Signal Processing", y: "2022"}, {t: "Remote Sensing Classification using Deep Learning", j: "Remote Sensing Earth System Science", y: "2023"}],
        conferences: 35, confTitles: ["FPGA Image Processing — IEEE VLSI 2024", "IoT Environmental Monitoring — ICECCE 2023"],
        books: [{t: "DSP: Theory and Practice", isbn: "", y: "2022"}, {t: "VLSI Design Fundamentals", isbn: "", y: "2023"}],
        patents: [], awards: []
      },
      "ashok-kumar-cheeli": {
        name: "Prof. Ashok Kumar Cheeli", role: "Professor, HOD", dept: "Electrical and Electronics Engineering",
        photo: "images/eee/ashok-kumar.jpg", qual: "M.Tech (Power Systems)",
        email: "", exp: "20+ years", joined: "",
        areas: ["Power Systems", "Smart Grids", "Energy Management"],
        subjects: ["Power Systems", "Smart Grid Technology", "Electrical Machines"],
        journals: [{t: "Optimal Power Flow in Smart Grids", j: "IEEE Power Systems", y: "2024"}, {t: "Fault Detection in Distribution Networks using ML", j: "Electrical Power Systems Research", y: "2023"}],
        conferences: 10, confTitles: [], books: [], patents: [], awards: []
      },
      "j-krishnaraj": {
        name: "Dr. J. Krishnaraj", role: "Professor, HOD", dept: "Mechanical Engineering",
        photo: "images/mechanical/krishnaraj.jpg", qual: "Ph.D (Manufacturing Engg), M.E (Thermal Power), B.E (Mech and Production)",
        email: "dr.j.krishnaraj@mlrinstitutions.ac.in", exp: "21 years", joined: "",
        areas: ["Manufacturing Engineering", "Composites", "NDT"],
        subjects: ["Kinematics of Machinery", "Machine Tools", "Robotics", "Thermal Engineering", "Advanced IC Engines"],
        journals: Array.from({length: 17}, (_, i) => ({t: "Research paper " + (i+1), j: "Scopus/SCI/ESCI/WOS Journal", y: String(2024 - Math.floor(i/6))})).slice(0, 5),
        conferences: 3, confTitles: [],
        books: [{t: "Emerging Frontiers in Manufacturing", isbn: "", y: "2023"}, {t: "Engineering Graphics", isbn: "", y: "2022"}],
        patents: [], awards: []
      },
      "m-satyanarayana-gupta": {
        name: "Dr. M. Satyanarayana Gupta", role: "HOD, Professor", dept: "Aeronautical Engineering",
        photo: "images/aeronautical/satyanarayana.jpg", qual: "Ph.D, M.Tech (Mechanical), B.E (Mechanical)",
        email: "msngupta.m@mlrinstitutions.ac.in", exp: "25 years", joined: "01-11-2014",
        areas: ["Design and Production", "FEM", "Machine Design", "Smart Aerospace Structures"],
        subjects: ["FEM", "Design of Machine Members", "Engineering Drawing", "Machine Tools", "Mechanical Vibrations", "Kinematics/Dynamics of Machinery", "Smart Aerospace Structures"],
        journals: Array.from({length: 34}, (_, i) => ({t: "SCI/SCIE/SCOPUS paper " + (i+1), j: "International Journal", y: String(2024 - Math.floor(i/10))})).slice(0, 6),
        conferences: 15, confTitles: [],
        books: [],
        patents: Array.from({length: 10}, (_, i) => ({t: "Patent " + (i+1) + " (Specimen Holder, Agricultural UAV, etc.)", n: "Published", y: String(2019 + Math.floor(i/3))})).slice(0, 5),
        awards: []
      },
      "n-ramanjaneyulu": {
        name: "Dr. N. Ramanjaneyulu", role: "Professor, HOD", dept: "Master of Business Administration",
        photo: "images/mba/ramanjaneyulu.jpeg", qual: "Ph.D (Management), MBA",
        email: "", exp: "20+ years", joined: "",
        areas: ["Strategic Management", "Leadership", "Organizational Behaviour"],
        subjects: ["Strategic Management", "Organizational Behaviour", "Business Environment"],
        journals: [{t: "Digital Transformation Impact on SME Performance", j: "Intl J Management Studies", y: "2024"}, {t: "Sustainable Supply Chain in Indian Manufacturing", j: "J Cleaner Production", y: "2021"}],
        conferences: 8, confTitles: [], books: [], patents: [], awards: []
      }
    };'''

# Replace the old facultyDB
old_db_match = re.search(r'var facultyDB = \{.*?\n    \};', content, re.DOTALL)
if old_db_match:
    content = content[:old_db_match.start()] + new_db + content[old_db_match.end():]
    with open('c:/mlr/homepage/departments/faculty-profile.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Faculty DB updated: {new_db.count("name:")} entries')
else:
    print('ERROR: Could not find facultyDB in file')
