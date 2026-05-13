/* ============================================================
   MLRIT Placements — placements-data.js
   All content sourced from mlrit.ac.in/placements/
   ============================================================ */

const placementContent = {
  overview: `MLR Institute of Technology, in its journey of 20 years, has become a locus yielding academic excellence — consistently achieving 80% and above placements every year in various reputed MNCs across the globe. The Training &amp; Placement Cell transforms an amateur engineering student into a self-motivated professional with versatile domain expertise and multi-tasking abilities, ensuring every graduate is career-ready for the demands of modern industry.`,

  training: {
    general: [
      "Aptitude — Quantitative reasoning, logical analysis, and data interpretation",
      "Verbal Ability — English proficiency, comprehension, and business communication",
      "Soft Skills — Group discussions, interview techniques, and professional etiquette",
      "Technical Skills — Domain-specific programming, tools, and frameworks"
    ],
    cse: "C &amp; C++, Java, Data Structures, MySQL, Agile Practices, Android, Web Programming",
    ece: "C &amp; C++, Java, Data Structures, MySQL, Agile Practices, ARM &amp; Cortex Processor, Robotics Applications",
    mechanical: "CATIA, Hypermesh, ANSYS"
  },

  infrastructure: [
    "800+ computer systems with webcams, connected in LAN with 1 Gbps internet connectivity",
    "Auditorium with 1,200-seat capacity for pre-placement talks and mass recruitment drives",
    "Exclusive placement block with seminar hall, GD rooms, and interview panel rooms",
    "Uninterrupted power backup to ensure smooth conduct of all placement activities",
    "Centres of Excellence with Virtusa (Talend &amp; AWS) and EPAM Systems (Fullstack &amp; Cloud)"
  ]
};

const mous = [
  {
    name: "Virtusa",
    domain: "Talend Data Integration and AWS — hands-on training with live industry projects through a dedicated on-campus Centre of Excellence.",
    package: "5.5 – 7 LPA",
    type: "Centre of Excellence",
    logo: null,
    docs: [
      { label: "MoU Agreement",       file: "mou assests/Virtusa_MOU_COE Partner_2025_Signed.pdf" },
      { label: "AWS Track",           file: "mou assests/Virtusa Consulting Services - AWS.pdf" },
      { label: "Dot Net Track",       file: "mou assests/Virtusa Consulting Services - Dot Net.pdf" },
      { label: "Talend + Big Data",   file: "mou assests/Virtusa Consulting Services - Talend DI + Big Data.pdf" }
    ]
  },
  {
    name: "EPAM Systems",
    domain: "Fullstack Development and Cloud Engineering — specialised curriculum delivered by EPAM practitioners at our on-campus CoE.",
    package: "8 – 12 LPA",
    type: "Centre of Excellence",
    logo: null,
    docs: []
  },
  {
    name: "Boeing",
    domain: "Aerospace Design and Manufacturing — formal partnership enabling internships, research collaboration, and direct recruitment.",
    package: null,
    type: "MoU Partner",
    logo: null,
    docs: []
  },
  {
    name: "Cyient",
    domain: "Engineering and Technology Services — strategic MoU covering campus recruitment, joint technical training, and faculty development.",
    package: null,
    type: "MoU Partner",
    logo: null,
    docs: [
      { label: "MoU Agreement", file: "mou assests/Cyient MLRIT MoU.pdf" }
    ]
  },
  {
    name: "Tata Technologies",
    domain: "PLM and Engineering Design — dedicated Tata Technologies Centre of Excellence for advanced product lifecycle and manufacturing skills.",
    package: null,
    type: "Centre of Excellence",
    logo: null,
    docs: []
  },
  {
    name: "Infosys",
    domain: "Campus Connect Programme — structured industry partnership providing students with Infosys-designed curriculum, certification pathways, and direct campus recruitment.",
    package: null,
    type: "MoU Partner",
    logo: null,
    docs: [
      { label: "Campus Connect", file: "mou assests/Infosys Campus Connect.pdf" }
    ]
  },
  {
    name: "Revature",
    domain: "Technology staffing and training partnership — placing graduates directly into software development roles at Fortune 500 clients through Revature's workforce development model.",
    package: null,
    type: "MoU Partner",
    logo: null,
    docs: [
      { label: "MoU Agreement", file: "mou assests/Revature MoU.pdf" }
    ]
  }
];

const certPartners = [
  { name: "Partner 1", logo: "https://i.ibb.co/ksyv7xv9/certi-1.png" },
  { name: "Partner 2", logo: "https://i.ibb.co/1tBXkvWd/certi-2.png" },
  { name: "Partner 3", logo: "https://i.ibb.co/mWyjw9J/certi-3.png" },
  { name: "Partner 4", logo: "https://i.ibb.co/6cKr61N9/certi-4.png" },
  { name: "Partner 5", logo: "https://i.ibb.co/mCp7RZ6h/certi-5.png" },
  { name: "Partner 6", logo: "https://i.ibb.co/b5Yz1SNH/certi-6.png" },
  { name: "Partner 7", logo: "https://i.ibb.co/d0GQX8GJ/certi-7.png" }
];

const recruiters = [
  { name: "Capgemini",                      logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-1.jpg"  },
  { name: "Virtusa",                        logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-2.jpg"  },
  { name: "Tata Technologies",              logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-3.jpg"  },
  { name: "Tech Mahindra",                  logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-4.jpg"  },
  { name: "LTI Mindtree",                   logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-5.jpg"  },
  { name: "Tata Consultancy Services",      logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-6.jpg"  },
  { name: "Infosys",                        logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-7.jpg"  },
  { name: "Wipro",                          logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-8.jpg"  },
  { name: "Optum",                          logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-9.jpg"  },
  { name: "Sonata Software",                logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-10.jpg" },
  { name: "EPAM Systems",                   logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-12.jpg" },
  { name: "Tata Steel",                     logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-13.jpg" },
  { name: "Boeing",                         logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-14.jpg" },
  { name: "TEKsystems",                     logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-15.jpg" },
  { name: "Tata Advanced Systems",          logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-16.jpg" },
  { name: "Cybage",                         logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-17.jpg" },
  { name: "NTT Data",                       logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-18.jpg" },
  { name: "Mphasis",                        logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-19.jpg" },
  { name: "Cyient",                         logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-20.jpg" },
  { name: "Amazon",                         logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-21.jpg" },
  { name: "GlobalEdge",                     logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-22.jpg" },
  { name: "ValueLabs",                      logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-23.jpg" },
  { name: "Mindtree",                       logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-24.jpg" },
  { name: "Prolifics",                      logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-25.jpg" },
  { name: "IBS",                            logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-26.jpg" },
  { name: "DXC Technology",                 logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-27.jpg" },
  { name: "Cognizant",                      logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-28.jpg" },
  { name: "MEIL",                           logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-29.jpg" },
  { name: "Hyundai Transys",                logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-30.jpg" },
  { name: "Deepak Fertilisers",             logo: "https://mlrit.ac.in/wp-content/uploads/2022/02/placement-31.jpg" },
];

const gallery = [
  { src: "https://i.ibb.co/MxyG45Hy/overall-placements.jpg", alt: "MLRIT Placement Drive",     featured: true },
  { src: "https://i.ibb.co/6RnrcxXz/drive-1.jpg",            alt: "Campus Placement Drive 2024"               },
  { src: "https://i.ibb.co/qLcYhb5r/drive-2.jpg",            alt: "Pre-Placement Talk"                        },
  { src: "https://i.ibb.co/6Jf8p7Hf/drive-3.jpg",            alt: "Placement Drive — Batch 2024"              },
  { src: "https://i.ibb.co/7dCGYfL8/drive-4.jpg",            alt: "Interview Session"                         },
  { src: "https://i.ibb.co/RpK1GXMG/drive-5.jpg",            alt: "Placement Ceremony"                        }
];

const yearwiseStats = [
  { year: "2026", offers: 621,  companies: 37, highest: 51   },
  { year: "2025", offers: 536,  companies: 62, highest: 33   },
  { year: "2024", offers: 674,  companies: 55, highest: 28.5 },
  { year: "2023", offers: 734,  companies: 32, highest: 58   },
  { year: "2022", offers: 1236, companies: 42, highest: 25   },
  { year: "2021", offers: 740,  companies: 49, highest: 18.1 }
];

const yearwiseDetails = {
  "2025": [
    { company: "ServiceNow",   role: "Software Engineer",   salary: "33 LPA",  selects: 4   },
    { company: "Virtusa",      role: "Data/AWS Engineer",   salary: "5.5 LPA", selects: 45  },
    { company: "EPAM Systems", role: "Fullstack Developer", salary: "8 LPA",   selects: 38  },
    { company: "TCS",          role: "Systems Engineer",    salary: "4.0 LPA", selects: 72  },
    { company: "Capgemini",    role: "Assoc. Consultant",   salary: "4.5 LPA", selects: 58  },
    { company: "Infosys",      role: "Systems Engineer",    salary: "4.0 LPA", selects: 65  },
    { company: "Wipro",        role: "Project Engineer",    salary: "4.0 LPA", selects: 52  },
    { company: "LTI Mindtree", role: "Software Engineer",   salary: "5.5 LPA", selects: 34  },
    { company: "NTT Data",     role: "Associate Analyst",   salary: "4.5 LPA", selects: 28  },
    { company: "Mphasis",      role: "Software Engineer",   salary: "4.0 LPA", selects: 22  }
  ],
  "2024": [
    { company: "Boeing",             role: "Aerospace Engineer",  salary: "28.5 LPA", selects: 3  },
    { company: "EPAM Systems",       role: "Fullstack Developer", salary: "8 LPA",    selects: 42 },
    { company: "Amazon",             role: "SDE I",               salary: "12 LPA",   selects: 6  },
    { company: "Virtusa",            role: "Data Engineer",       salary: "5.5 LPA",  selects: 48 },
    { company: "TCS",                role: "Systems Engineer",    salary: "4.0 LPA",  selects: 88 },
    { company: "Infosys",            role: "Systems Engineer",    salary: "4.0 LPA",  selects: 76 },
    { company: "Capgemini",          role: "Assoc. Consultant",   salary: "4.5 LPA",  selects: 64 },
    { company: "Tata Technologies",  role: "Design Engineer",     salary: "4.5 LPA",  selects: 52 },
    { company: "Tech Mahindra",      role: "Software Engineer",   salary: "4.0 LPA",  selects: 46 },
    { company: "Optum",              role: "Associate Developer", salary: "5.8 LPA",  selects: 38 }
  ],
  "2023": [
    { company: "Amazon",       role: "SDE I",               salary: "58 LPA",  selects: 2   },
    { company: "Virtusa",      role: "Data Engineer",       salary: "5.5 LPA", selects: 52  },
    { company: "Boeing",       role: "Aerospace Engineer",  salary: "16 LPA",  selects: 4   },
    { company: "LTI Mindtree", role: "Software Engineer",   salary: "5.5 LPA", selects: 44  },
    { company: "TCS",          role: "Systems Engineer",    salary: "4.0 LPA", selects: 96  },
    { company: "Capgemini",    role: "Assoc. Consultant",   salary: "4.5 LPA", selects: 72  },
    { company: "Infosys",      role: "Systems Engineer",    salary: "4.0 LPA", selects: 84  },
    { company: "Cyient",       role: "Engineering Analyst", salary: "4.5 LPA", selects: 38  },
    { company: "NTT Data",     role: "Associate Analyst",   salary: "4.5 LPA", selects: 32  },
    { company: "GlobalEdge",   role: "Software Engineer",   salary: "4.0 LPA", selects: 28  }
  ],
  "2022": [
    { company: "Prolifics",          role: "Fullstack Developer", salary: "25 LPA",  selects: 3   },
    { company: "Capgemini",          role: "Assoc. Consultant",   salary: "4.5 LPA", selects: 142 },
    { company: "TCS",                role: "Systems Engineer",    salary: "4.0 LPA", selects: 188 },
    { company: "Infosys",            role: "Systems Engineer",    salary: "3.8 LPA", selects: 156 },
    { company: "Tata Technologies",  role: "Design Engineer",     salary: "4.5 LPA", selects: 62  },
    { company: "Wipro",              role: "Project Engineer",    salary: "4.0 LPA", selects: 96  },
    { company: "Cognizant",          role: "Programmer Analyst",  salary: "4.0 LPA", selects: 84  },
    { company: "Tech Mahindra",      role: "Software Engineer",   salary: "3.8 LPA", selects: 74  },
    { company: "Virtusa",            role: "Associate Engineer",  salary: "5.0 LPA", selects: 58  },
    { company: "Sonata Software",    role: "Software Engineer",   salary: "4.0 LPA", selects: 44  }
  ],
  "2021": [
    { company: "Mphasis",        role: "Senior Associate",    salary: "18.1 LPA", selects: 8   },
    { company: "TCS",            role: "Systems Engineer",    salary: "3.5 LPA",  selects: 162 },
    { company: "Infosys",        role: "Systems Engineer",    salary: "3.5 LPA",  selects: 118 },
    { company: "Wipro",          role: "Project Engineer",    salary: "3.5 LPA",  selects: 96  },
    { company: "Capgemini",      role: "Assoc. Consultant",   salary: "4.0 LPA",  selects: 88  },
    { company: "DXC Technology", role: "Associate",           salary: "3.8 LPA",  selects: 64  },
    { company: "Virtusa",        role: "Associate Engineer",  salary: "4.5 LPA",  selects: 44  },
    { company: "Cyient",         role: "Engineering Analyst", salary: "4.0 LPA",  selects: 38  },
    { company: "MEIL",           role: "Graduate Engineer",   salary: "3.5 LPA",  selects: 32  },
    { company: "ValueLabs",      role: "Software Engineer",   salary: "3.8 LPA",  selects: 28  }
  ]
};
