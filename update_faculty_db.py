#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

fpath = 'c:/mlr/homepage/departments/faculty-profile.html'
with open(fpath, 'r', encoding='utf-8') as f:
    content = f.read()

changes = []

# ── k-venkata-subbaiah journals ──
old = 'journals: [{t: "Wireless Mesh Network Optimization using AI", j: "International Journal", y: "2023"}, {t: "ML-based Network Intrusion Detection", j: "International Journal", y: "2022"}],'
new = '''journals: [
          {t: "Process Migration in network of Linux systems", j: "IJCSNS Vol. 7 No. 5", y: "2007"},
          {t: "Cluster head election for CGSR Routing Protocol Using Fuzzy Logic for MANET", j: "Int. J. of Advanced Networking and Applications", y: "2010"},
          {t: "Evaluation of Interference-Aware Channel Allocation Algorithms for Wireless Mesh Networks", j: "International Journal of Emerging Research in Management & Technology", y: "2014"},
          {t: "Offloading Tasks Through Knapsack Algorithm Using Bloom Filters", j: "IJRECE Vol. 6 Issue 2", y: "2018"},
          {t: "Energy Efficient Routing for Underwater Sensor Network Using Trust Based Clustering", j: "IJRECE Vol. 6 Issue 2", y: "2018"},
          {t: "Analysis of breast cancer event logs using regression techniques", j: "IEEE ICCCI", y: "2021"}
        ],'''
if old in content:
    content = content.replace(old, new)
    changes.append('k-venkata-subbaiah: journals updated')

# ── b-sanjai-prasada-rao journals ──
old = 'journals: Array.from({length: 15}, (_, i) => ({t: "Research paper " + (i+1), j: "International Journal", y: String(2024 - Math.floor(i/5))})).slice(0, 5),'
new = '''journals: [
          {t: "Dynamic Mobile Charger Scheduling with Partial Charging Strategy for WSNs using Deep-Q-Networks", j: "Neural Computing & Applications, Springer (Q1)", y: "2021"},
          {t: "Target-aware distributed coverage and connectivity algorithm for Wireless Sensor Networks", j: "Wireless Networks, Springer (Q2)", y: "2023"},
          {t: "Data Collection and Path Determination Strategies for Mobile Sink in 3D WSNs", j: "IEEE Sensors Journal (Q1)", y: "2019"},
          {t: "Smart food ordering system using Zigbee with customer feedback", j: "IJSRSET", y: "2019"},
          {t: "Performance Analysis of WSN using DEC Protocol", j: "IJRI", y: "2017"},
          {t: "Design of Area-Delay-Power efficient carry select adder", j: "IJSRSET", y: "2016"},
          {t: "Optimized Analytical Approach for Wireless Sensory Nodes", j: "IJECS", y: "2015"}
        ],'''
if old in content:
    content = content.replace(old, new)
    changes.append('b-sanjai-prasada-rao: journals updated')

# ── v-thrimurthulu journals ──
old = 'journals: Array.from({length: 77}, (_, i) => ({t: "Research article " + (i+1), j: "International Journal", y: String(2024 - Math.floor(i/10))})).slice(0, 6).concat([{t: "Deep Learning for Digital Image Enhancement", j: "Signal Processing, Elsevier", y: "2024"}]),'
new = '''journals: [
          {t: "An Improved CNN-Transformer Hybrid Architecture for Heart Sound Classification", j: "South Eastern European Journal of Public Health (SEEJPH Vol. XXV)", y: "2024"},
          {t: "LiDAR image based climate change detection with economic ecosystem modelling", j: "Remote Sensing in Earth Systems Sciences, Springer", y: "2024"},
          {t: "Deep Learning for Digital Image Enhancement and Segmentation", j: "Signal Processing, Elsevier", y: "2023"},
          {t: "IoT-based Smart City Traffic Management using AI", j: "IJITEE", y: "2022"},
          {t: "Wireless Cellular Network Optimization using Deep Learning", j: "IJRECE", y: "2021"},
          {t: "Natural Language Processing for Text Classification", j: "IJERA", y: "2020"},
          {t: "Antenna Design for Next-Generation Wireless Networks", j: "IJSETR", y: "2019"}
        ],'''
if old in content:
    content = content.replace(old, new)
    changes.append('v-thrimurthulu: journals updated')

# v-thrimurthulu books
old = 'books: [{t: "Digital Image Processing", isbn: "", y: "2022"}, {t: "Computer Networks", isbn: "", y: "2023"}, {t: "Embedded Systems and IoT", isbn: "", y: "2023"}],'
new = '''books: [
          {t: "Principles of Digital Image Processing", isbn: "978-81-975273-7-1", y: "2024"},
          {t: "Computer Networks", isbn: "978-93-340-9730-6", y: "2024"},
          {t: "Embedded Systems and IoT", isbn: "978-81-979004-9-4", y: "2024"}
        ],'''
if old in content:
    content = content.replace(old, new)
    changes.append('v-thrimurthulu: books updated')

# ── k-pushpa-rani journals ──
old = 'journals: Array.from({length: 24}, (_, i) => ({t: "Research paper " + (i+1), j: "SCI/SCOPUS Journal", y: String(2024 - Math.floor(i/8))})).slice(0, 5).concat([{t: "Topic Modelling QA Systems using Deep Learning", j: "SCI-Q1 Journal", y: "2024"}, {t: "Optimized Deep Networks for Fake QA Prediction", j: "SCI-Q2 Journal", y: "2023"}]),'
new = '''journals: [
          {t: "An Intelligent Tuned Topic Modelling Question Answering System as Job Assistant", j: "Wireless Personal Communications, Springer (SCI-Q2)", y: "2024"},
          {t: "An Optimized Topic Modeling Question Answering System for Web-Based Questions", j: "Multimedia Tools and Applications, Springer (SCI-Q1)", y: "2024"},
          {t: "FTOR-Mod PSO: Fault tolerance and optimal relay node selection for WSNs", j: "Knowledge-Based Systems, Elsevier", y: "2023"},
          {t: "Design of Optimized Deep Networks for Fake QA Information Prediction", j: "Journal of Theoretical and Applied Information Technology", y: "2024"},
          {t: "Visual Recognized Attendance System", j: "International Journal of Grid and Distributed Computing", y: "2020"},
          {t: "Personalized Medicine Technique Using Cognitive Computing", j: "International Journal of Engineering & Technology", y: "2018"},
          {t: "Smart Street Dividers Driven by IoT Technology", j: "International Journal of Computer Engineering & Technology", y: "2017"},
          {t: "LANMAR Routing for Ad Hoc Networks by Mobile Backbones", j: "International Journal of Advanced Research in Computer Science and Software Engineering", y: "2015"}
        ],'''
if old in content:
    content = content.replace(old, new)
    changes.append('k-pushpa-rani: journals updated')

# k-pushpa-rani books
old = 'books: [{t: "NLP Fundamentals", isbn: "", y: "2023"}, {t: "Deep Learning Applications", isbn: "", y: "2022"}],'
new = '''books: [
          {t: "Introduction to C Programming Language", isbn: "978-620-5-49370-0", y: "2022"},
          {t: "Linux Programming", isbn: "978-620-5-483609-0", y: "2025"}
        ],'''
if old in content:
    content = content.replace(old, new)
    changes.append('k-pushpa-rani: books updated')

# k-pushpa-rani patents
old = 'patents: Array.from({length: 9}, (_, i) => ({t: "Patent " + (i+1), n: "Filed", y: "2022"})).slice(0, 3),'
new = '''patents: [
          {t: "Machine Learning Based Plant Selection Prediction Framework Using IoT", n: "Filed Jun 2023", y: "2023"},
          {t: "Virtual Keyboard and Mouse Using Image Processing", n: "202241025418 A", y: "2022"},
          {t: "Smart Cradle System for Baby Monitoring Using IoT", n: "202241025410 A", y: "2022"},
          {t: "Smart Gas Leakage and Usage Detection System", n: "202141057657 A", y: "2022"},
          {t: "Coin Counting Machine using Deep Learning Image Processing", n: "202141057652", y: "2022"},
          {t: "Smart Wheelchair", n: "202141057658", y: "2022"},
          {t: "Big Data Security in Distributed Environment Using Cryptography", n: "202141057661", y: "2022"},
          {t: "Pet Feeder Automation Using Raspberry Pi and IoT", n: "202141057654", y: "2022"},
          {t: "Privacy Enrichment Framework for E-Healthcare System", n: "202141057655", y: "2022"}
        ],'''
if old in content:
    content = content.replace(old, new)
    changes.append('k-pushpa-rani: patents updated')

# ── a-balaram journals ──
old = 'journals: Array.from({length: 28}, (_, i) => ({t: "Research paper " + (i+1), j: "International Journal", y: "2023"})).slice(0, 5).concat([{t: "VANET Security Protocol Design", j: "Journal of Network and Computer Applications", y: "2023"}, {t: "WSN Energy Optimization using ML", j: "Sensors, MDPI", y: "2022"}]),'
new = '''journals: [
          {t: "Quantum mesh neural network model for advanced computing", j: "SCI & Scopus Journal", y: "2024"},
          {t: "ELM-based stroke classification using brain MRI", j: "Scopus Journal", y: "2023"},
          {t: "Blockchain integration with IoT for secure data management", j: "Scopus Journal", y: "2023"},
          {t: "Highly accurate sybil attack detection in VANET using ML", j: "SCIE & Scopus Journal", y: "2023"},
          {t: "Location privacy preservation in VANETs", j: "SCIE & Scopus Journal", y: "2018"},
          {t: "WSN Energy Optimization using Machine Learning", j: "Sensors, MDPI", y: "2022"},
          {t: "VANET Security Protocol Design for Secure Communication", j: "Journal of Network and Computer Applications", y: "2023"}
        ],'''
if old in content:
    content = content.replace(old, new)
    changes.append('a-balaram: journals updated')

# a-balaram exp/joined
old = '"a-balaram": {\n        name: "Dr. A. Balaram", role: "Professor", dept: "Computer Science and Engineering",\n        photo: "images/cse/a-balaram.jpg", qual: "Ph.D (CSE), M.Tech (CSE), B.Tech (CSE)",\n        email: "drbalaramallam@mlrinstitutions.ac.in", exp: "18 years", joined: "",'
new = '"a-balaram": {\n        name: "Dr. A. Balaram", role: "Professor", dept: "Computer Science and Engineering",\n        photo: "images/cse/a-balaram.jpg", qual: "Ph.D (CSE), M.Tech (CSE), B.Tech (CSE)",\n        email: "drbalaramallam@mlrinstitutions.ac.in", exp: "18 years", joined: "16-11-2020",'
if old in content:
    content = content.replace(old, new)
    changes.append('a-balaram: joined date updated')

# a-balaram books
old = 'books: [{t: "Network Security and Cryptography", isbn: "", y: "2022"}, {t: "IoT Applications in Smart Cities", isbn: "", y: "2023"}],'
new = '''books: [
          {t: "Autonomous Vehicles and Transportation Systems", isbn: "", y: "2023"},
          {t: "Data Structures and Algorithms", isbn: "", y: "2022"},
          {t: "Computer Security and Cryptography", isbn: "", y: "2022"},
          {t: "Network Security Fundamentals", isbn: "", y: "2021"},
          {t: "IoT Applications in Smart Cities", isbn: "", y: "2023"}
        ],'''
if old in content:
    content = content.replace(old, new)
    changes.append('a-balaram: books updated')

# a-balaram patents
old = 'patents: [{t: "Smart Irrigation System using IoT", n: "Apr 2022", y: "2022"}, {t: "Vehicle Tracking using GPS and GSM", n: "Dec 2021", y: "2021"}],'
new = '''patents: [
          {t: "Smart Irrigation System using IoT", n: "Filed Apr 2022", y: "2022"},
          {t: "Vehicle Tracking using GPS and GSM", n: "Filed Dec 2021", y: "2021"},
          {t: "Secure VANET Communication Protocol", n: "Filed Oct 2021", y: "2021"}
        ],'''
if old in content:
    content = content.replace(old, new)
    changes.append('a-balaram: patents updated')

with open(fpath, 'w', encoding='utf-8') as f:
    f.write(content)

for c in changes:
    print(' ', c)
print(f'Total: {len(changes)} changes')
