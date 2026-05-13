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
    logo: null
  },
  {
    name: "EPAM Systems",
    domain: "Fullstack Development and Cloud Engineering — specialised curriculum delivered by EPAM practitioners at our on-campus CoE.",
    package: "8 – 12 LPA",
    type: "Centre of Excellence",
    logo: null
  },
  {
    name: "Boeing",
    domain: "Aerospace Design and Manufacturing — formal partnership enabling internships, research collaboration, and direct recruitment.",
    package: null,
    type: "MoU Partner",
    logo: null
  },
  {
    name: "Cyient",
    domain: "Engineering and Technology Services — strategic MoU covering campus recruitment, joint technical training, and faculty development.",
    package: null,
    type: "MoU Partner",
    logo: null
  },
  {
    name: "Tata Technologies",
    domain: "PLM and Engineering Design — dedicated Tata Technologies Centre of Excellence for advanced product lifecycle and manufacturing skills.",
    package: null,
    type: "Centre of Excellence",
    logo: null
  }
];

const certPartners = [
  { name: "Partner 1", logo: "assets/logos/certi-1.png" },
  { name: "Partner 2", logo: "assets/logos/certi-2.png" },
  { name: "Partner 3", logo: "assets/logos/certi-3.png" },
  { name: "Partner 4", logo: "assets/logos/certi-4.png" },
  { name: "Partner 5", logo: "assets/logos/certi-5.png" },
  { name: "Partner 6", logo: "assets/logos/certi-6.png" },
  { name: "Partner 7", logo: "assets/logos/certi-7.png" }
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
  { src: "assets/images/overall-placements.jpg", alt: "MLRIT Placement Drive", featured: true  },
  { src: "assets/images/drive-1.jpg",            alt: "Campus Placement Drive 2024"             },
  { src: "assets/images/drive-2.jpg",            alt: "Pre-Placement Talk"                      },
  { src: "assets/images/drive-3.jpg",            alt: "Placement Drive — Batch 2024"            },
  { src: "assets/images/drive-4.jpg",            alt: "Interview Session"                       },
  { src: "assets/images/drive-5.jpg",            alt: "Placement Ceremony"                      },
  { src: "assets/images/placement-1.jpg",        alt: "Placement Activity"                      },
  { src: "assets/images/placement-2.jpg",        alt: "Recruitment Drive"                       },
  { src: "assets/images/placement-3.jpg",        alt: "Campus Recruitment"                      }
];

const yearwiseStats = [
  { year: "2026", offers: 544,  companies: 36, highest: 51   },
  { year: "2025", offers: 536,  companies: 62, highest: 33   },
  { year: "2024", offers: 674,  companies: 55, highest: 28.5 },
  { year: "2023", offers: 734,  companies: 32, highest: 58   },
  { year: "2022", offers: 1236, companies: 42, highest: 25   },
  { year: "2021", offers: 740,  companies: 49, highest: 18.1 }
];
