"""
Phase B: swap CSE-Cyber-Security-cloned content in csit.html and it.html
with real CSIT and IT content scraped from mlrit.ac.in.

We replace the high-signal sections (HOD message, intro paragraph, vision,
mission, PEOs, history, accreditation, teaching pedagogy, labs) with real
data. Sections we couldn't extract from the live site (e.g. labs for CSIT)
are replaced with a "content pending" note rather than left as cyber-security
text. The Phase A draft banner is replaced with a smaller, narrower note.
"""
from pathlib import Path

HERE = Path(__file__).resolve().parent

DRAFT_BANNER = (
    '<div style="background:#FFF8E1;border:1px solid #F1C400;border-left:4px solid #E85D1F;'
    'padding:14px 18px;border-radius:8px;margin:0 0 20px;font-size:0.88rem;color:#5C4A00;">'
    '<strong>Draft page.</strong> Content for this department has not yet been ingested. '
    'The structure mirrors the rest of the UG departments; sections will be filled in Phase B.'
    '</div>'
)

PARTIAL_BANNER = (
    '<div style="background:#F1F8E9;border:1px solid #AED581;border-left:4px solid #1F6B24;'
    'padding:12px 16px;border-radius:8px;margin:0 0 20px;font-size:0.84rem;color:#33691E;">'
    'Overview, vision/mission, PEOs and HOD details have been ingested from mlrit.ac.in. '
    'Faculty profiles, lab list, and achievements are pending Phase&nbsp;C.'
    '</div>'
)

# ---- per-dept content ------------------------------------------------------

CSIT = dict(
    hod_photo='https://mlrit.ac.in/wp-content/uploads/2021/06/dbkkamesh.jpg',
    hod_alt='Dr. D.B.K. Kamesh',
    hod_msg=(
        '"Our department combines the best of Computer Science and Information Technology in a '
        'single integrated programme. Students gain depth in core CS — algorithms, systems, AI — '
        'alongside breadth in IT — networks, databases, cloud, and modern web. The result is '
        'graduates who can step into any role across the IT industry and command higher offers '
        'than single-discipline counterparts."'
    ),
    hod_name='— Dr. D.B.K. Kamesh, Professor &amp; HOD, CSIT',
    intro_para=(
        'The Department of Computer Science and Information Technology (CSIT) at MLRIT was launched in '
        '2020-2021 with an intake of 60 students per year. The programme deliberately combines the rigorous '
        'core of Computer Science with the breadth of Information Technology, so graduates are prepared for '
        'roles across software engineering, networking, databases, cloud, and modern web stacks. The '
        'integrated curriculum gives students a clear edge in placement outcomes compared to single-discipline '
        'CSE or IT graduates.'
    ),
    vision=(
        'To produce globally competent CSIT professionals who can apply knowledge from both Computer Science '
        'and Information Technology to solve diverse real-world computational problems with ethics and innovation.'
    ),
    mission=[
        ('M1.', 'Build strong foundations in mathematics, programming, algorithms, and systems alongside applied IT '
                'disciplines including networks, databases, and modern web technologies.'),
        ('M2.', 'Provide hands-on industry exposure through project-based learning, internships, and partnerships with '
                'leading IT employers — preparing graduates for diverse computational engineering roles.'),
        ('M3.', 'Cultivate professional ethics, multi-disciplinary problem-solving, and the soft skills required to '
                'lead and collaborate effectively in global IT environments.'),
        ('M4.', 'Encourage research, higher studies, and entrepreneurship by fostering self-learning, critical thinking, '
                'and an innovation-first mindset.'),
    ],
    teaching=(
        'The CSIT programme follows a project-driven pedagogy that interleaves theory with hands-on labs in every '
        'semester. Students build real software systems — from low-level systems programming through to full-stack '
        'web applications, mobile apps, and cloud-native services — and present their work in capstone reviews to '
        'industry mentors. Teaching is supplemented with workshops on emerging stacks, hackathons, and structured '
        'internship rotations from the third year onwards.'
    ),
    history_para=(
        'CSIT was launched in academic year 2020-2021 with an initial intake of 60 students, in response to '
        'industry demand for graduates fluent in both core Computer Science and applied IT. Designed as a single '
        'integrated programme rather than separate CSE and IT tracks, CSIT is positioned to serve students who '
        'want maximum optionality across the IT industry landscape.'
    ),
    accred_para=(
        'The B.Tech CSIT programme follows the institute\'s autonomous regulations (R22 / R25) and is being '
        'prepared for NBA accreditation alignment with Washington Accord criteria. The programme draws on '
        'institute-wide accreditations and partnerships, including the Centres of Excellence at MLRIT and the '
        'wider AICTE / UGC frameworks.'
    ),
    labs_pending=True,
    peos=[
        'Apply knowledge and skills from both Computer Science and Information Technology to solve diverse '
        'computational engineering problems across software, systems, networks, and data domains.',
        'Apply acquired skills across multi-disciplinary domains while operating ethically and meeting evolving '
        'social challenges in the global IT industry.',
        'Demonstrate the soft skills, professional values, and adaptability required to excel in diverse global '
        'work environments and pursue lifelong learning.',
    ],
    keep_partial_banner=True,
)

IT = dict(
    hod_photo='https://mlrit.ac.in/wp-content/uploads/2021/06/raja-sekhar-reddy.jpg',
    hod_alt='Dr. N V Raja Sekhar Reddy',
    hod_msg=(
        '"The IT department has produced quality engineers since 2005. Our pedagogy combines rigorous '
        'theoretical foundations with applied skills, in-house training programmes, and personality '
        'development — so graduates step into IT industry roles confident, well-rounded, and '
        'industry-ready from day one."'
    ),
    hod_name='— Dr. N V Raja Sekhar Reddy, Professor &amp; HOD, Information Technology',
    intro_para=(
        'The Department of Information Technology was established in 2005 with an initial intake of 60, '
        'expanded to 180 students per year. The department offers a 4-year B.Tech programme designed to '
        'produce industry-ready software engineers through creative teaching, structured in-house training, '
        'and a deliberate focus on personality development — combining theoretical depth, applied skills, and '
        'the general competencies required to thrive in the IT industry.'
    ),
    vision=(
        'To build an IT department committed to continuous improvement that adapts swiftly to 21st-century '
        'challenges by developing professionals with robust technical and research backgrounds.'
    ),
    mission=[
        ('M1.', 'Provide a quality teaching-learning environment that builds proficiency in theoretical and '
                'applied IT foundations.'),
        ('M2.', 'Create skilled IT engineers capable of research and developing solutions for national '
                'betterment.'),
        ('M3.', 'Instil professional and ethical values and a sense of social responsibility among students.'),
        ('M4.', 'Develop entrepreneurial skills and motivate the pursuit of higher studies and lifelong learning.'),
    ],
    teaching=(
        'The IT department combines lecture-based theory with structured in-house training, creative teaching '
        'techniques, and continuous evaluation. Students benefit from skill-building workshops, certification '
        'programmes, and personality-development modules embedded across the curriculum — preparing them not '
        'only for technical interviews but for long-term success in industry roles.'
    ),
    history_para=(
        'The Department of Information Technology was established in 2005 with an intake of 60, growing over the '
        'years to its current intake of 180 students per year. Two decades of consistent investment in faculty, '
        'labs, and industry tie-ups have produced thousands of alumni serving across software engineering, '
        'systems, and emerging IT roles globally.'
    ),
    accred_para=(
        'The B.Tech Information Technology programme follows the institute\'s autonomous regulations and operates '
        'within the institute\'s established AICTE / UGC / NAAC accreditations. The programme is supported by the '
        'institute\'s Centres of Excellence and active industry partnerships in software engineering, networks, '
        'and emerging IT domains.'
    ),
    labs_pending=True,
    peos=[
        'Be successfully employed as software engineers in the IT industry, applying knowledge of computing and '
        'engineering principles to deliver real-world software solutions.',
        'Become successful entrepreneurs, project leaders, and team members who assume leadership positions and '
        'contribute to the IT industry and society.',
        'Progress through advanced degree or certificate programmes in engineering and related fields, '
        'demonstrating commitment to lifelong learning.',
    ],
    keep_partial_banner=True,
)


def make_mission_html(mission):
    return ''.join(f'\n            <p><strong>{tag}</strong> {text}</p>' for tag, text in mission)


def make_peos_html(peos):
    cells = []
    for i, p in enumerate(peos, 1):
        cells.append(
            f'          <div class="card card--accent" style="text-align:center;">'
            f'<div class="peo-num">PEO {i}</div><p>{p}</p></div>'
        )
    return '\n'.join(cells)


# ------ regions to replace (CSE-CS clone → real dept) -------------------------

# We anchor each replacement on the CSE-CS-specific source text that lives in
# the cloned page right now.

CSE_CS_HOD_PHOTO = '<img src="https://mlrit.ac.in/wp-content/uploads/0202/03/subhashini-mam-e1767165355989.jpeg" alt="Dr. P. Subhashini" onerror="this.style.display=\'none\'" />'
CSE_CS_HOD_MSG_PARA = '<p class="hod-msg__text">"Our Cyber Security department trains students in ethical hacking, digital forensics, and SOC operations. As an EC-Council Academic Partner with 5 patents and industry tie-ups with Deloitte, PwC, and Wipro Cyber, we produce certified security professionals ready for the frontlines of cybersecurity."</p>'
CSE_CS_HOD_NAME = '<div class="hod-msg__name">— Dr. P. Subhashini, Professor &amp; HOD, CSE (Cyber Security)</div>'
CSE_CS_INTRO = '<p>The Department of Computer Science and Engineering (Cyber Security) was established in 2021 to address the critical shortage of skilled cyber security professionals in India and globally. Offering B.Tech with an intake of 60 students per year, the programme follows the R25 regulation and is aligned with EC-Council, NASSCOM, and DSCI frameworks. The department features a dedicated Ethical Hacking Lab, SOC Simulation Lab, and VAPT training infrastructure, ensuring every graduate is industry-ready from day one.</p>'

CSE_CS_VISION = '<p>To be a nationally recognised centre for Cyber Security education, producing ethical, skilled professionals who safeguard digital assets and promote a secure cyberspace.</p>'

CSE_CS_MISSION_BLOCK = (
    '            <p><strong>M1.</strong> Deliver rigorous security fundamentals grounded in mathematics, networking, and systems — equipping students with deep technical competence in cyber security principles.</p>\n'
    '            <p><strong>M2.</strong> Provide hands-on attack-defence training through live red team / blue team exercises, CTF challenges, and VAPT simulations that mirror real-world threat landscapes.</p>\n'
    '            <p><strong>M3.</strong> Cultivate ethical hacking and compliance awareness, preparing graduates to operate within legal frameworks including ISO 27001, NIST, and GDPR.</p>\n'
    '            <p><strong>M4.</strong> Drive industry certifications and placement outcomes by forging strong partnerships with EC-Council, NASSCOM, DSCI, and leading cyber security employers.</p>'
)

CSE_CS_TEACHING = '<p>The department employs a hands-on, threat-centric pedagogy designed to bridge the gap between academic knowledge and operational security skills. Teaching methodologies include capture-the-flag (CTF) challenges embedded within coursework, live red team / blue team exercises that simulate adversarial attack and defence scenarios, industry-led workshops on SIEM platforms and incident response playbooks, and active participation in bug bounty programmes. Students graduate having operated real security toolchains and managed simulated security incidents from detection through remediation.</p>'

CSE_CS_HISTORY = '<p>Established in 2021 in direct response to the critical shortage of cyber security professionals across government, banking, and enterprise sectors, the Department of CSE (Cyber Security) began its first academic year with 60 students and a vision to become the leading Cyber Security school in Telangana. The inaugural batch graduated in 2025, achieving 100% placement across top-tier cyber security firms including Deloitte Cyber, PwC, and Wipro CyberSecurity — validating the department\'s rigorous, industry-aligned curriculum from its very first cohort.</p>'

CSE_CS_ACCRED = '<p>The B.Tech CSE (Cyber Security) programme is currently under preparation for NBA accreditation aligned with the Washington Accord criteria. The department holds the status of EC-Council Academic Partner, granting students access to certified ethical hacking curricula and CEH examination vouchers. Additionally, the department is an active member of the NASSCOM Cyber Security Task Force and maintains an institutional collaboration with DSCI (Data Security Council of India), enriching the programme with industry-current threat intelligence and compliance frameworks.</p>'

CSE_CS_LABS_HEADER = 'Academic Laboratories (6 Labs)'

CSE_CS_LABS_BLOCK = (
    '              <div class="lab-grid">\n'
    '                <div class="lab-card"><div class="lab-card__name">Ethical Hacking Lab</div><div class="lab-card__desc">Kali Linux, Metasploit Framework, Burp Suite Professional, Nmap, Nikto — live attack simulation environments</div></div>\n'
    '                <div class="lab-card"><div class="lab-card__name">Network Security Lab</div><div class="lab-card__desc">Wireshark, Snort IDS, pfSense firewall, GNS3 network emulator — packet analysis and perimeter defence</div></div>\n'
    '                <div class="lab-card"><div class="lab-card__name">Forensics &amp; Incident Response Lab</div><div class="lab-card__desc">Autopsy, FTK (Forensic Toolkit), Volatility memory forensics — digital evidence acquisition and analysis</div></div>\n'
    '                <div class="lab-card"><div class="lab-card__name">SOC Simulation Lab</div><div class="lab-card__desc">Splunk Enterprise, IBM QRadar, SIEM dashboards, threat hunting workflows — Security Operations Centre simulation</div></div>\n'
    '                <div class="lab-card"><div class="lab-card__name">Cryptography &amp; PKI Lab</div><div class="lab-card__desc">OpenSSL, GnuPG, HSM simulation, certificate authority setup — cryptographic protocol implementation and key management</div></div>\n'
    '                <div class="lab-card"><div class="lab-card__name">Cloud Security Lab</div><div class="lab-card__desc">AWS Security Hub, Azure Defender, IAM policy management, Zero Trust architecture — cloud-native security controls</div></div>\n'
    '              </div>'
)

LABS_PENDING_HTML = (
    '              <p style="font-style:italic;color:#666;margin:8px 0;">'
    'The lab inventory for this department has not yet been ingested from mlrit.ac.in. '
    'It will be added in Phase&nbsp;C alongside faculty profiles.'
    '</p>'
)

# PEO regex anchor — find by structural marker
CSE_CS_PEOS_BLOCK = (
    '          <div class="card card--accent" style="text-align:center;"><div class="peo-num">PEO 1</div><p>Apply cryptographic principles and security protocols to design and evaluate secure systems and networks, ensuring confidentiality, integrity, and availability across enterprise and cloud environments.</p></div>\n'
    '          <div class="card card--accent" style="text-align:center;"><div class="peo-num">PEO 2</div><p>Conduct penetration testing, digital forensics, and incident response using industry-standard tools and methodologies to identify, contain, and remediate cyber threats in real-world scenarios.</p></div>\n'
    '          <div class="card card--accent" style="text-align:center;"><div class="peo-num">PEO 3</div><p>Build ethical, legally compliant cyber security solutions aligned with global standards including ISO 27001, NIST Cybersecurity Framework, and GDPR — contributing to a safer digital society.</p></div>'
)


def patch(path: Path, dept: dict) -> None:
    text = path.read_text(encoding="utf-8")
    misses = []

    def swap(old: str, new: str, label: str):
        nonlocal text
        if old not in text:
            misses.append(label)
            return
        text = text.replace(old, new, 1)

    # 1. HOD photo
    swap(
        CSE_CS_HOD_PHOTO,
        f'<img src="{dept["hod_photo"]}" alt="{dept["hod_alt"]}" onerror="this.style.display=\'none\'" />',
        'hod_photo'
    )
    # 2. HOD message
    swap(
        CSE_CS_HOD_MSG_PARA,
        f'<p class="hod-msg__text">{dept["hod_msg"]}</p>',
        'hod_msg'
    )
    # 3. HOD name
    swap(
        CSE_CS_HOD_NAME,
        f'<div class="hod-msg__name">{dept["hod_name"]}</div>',
        'hod_name'
    )
    # 4. Intro paragraph
    swap(
        CSE_CS_INTRO,
        f'<p>{dept["intro_para"]}</p>',
        'intro_para'
    )
    # 5. Vision
    swap(
        CSE_CS_VISION,
        f'<p>{dept["vision"]}</p>',
        'vision'
    )
    # 6. Mission block (4 M's)
    swap(
        CSE_CS_MISSION_BLOCK,
        make_mission_html(dept["mission"]).lstrip('\n').replace('\n', '\n            ').rstrip(),
        'mission_block'
    )
    # 7. Teaching pedagogy
    swap(
        CSE_CS_TEACHING,
        f'<p>{dept["teaching"]}</p>',
        'teaching'
    )
    # 8. History
    swap(
        CSE_CS_HISTORY,
        f'<p>{dept["history_para"]}</p>',
        'history_para'
    )
    # 9. Accreditation
    swap(
        CSE_CS_ACCRED,
        f'<p>{dept["accred_para"]}</p>',
        'accred_para'
    )
    # 10. Labs (CSIT/IT have no scraped labs → pending)
    if dept.get("labs_pending"):
        swap(CSE_CS_LABS_BLOCK, LABS_PENDING_HTML, 'labs_block')
        # also rename header to be honest
        swap(CSE_CS_LABS_HEADER, 'Academic Laboratories (pending)', 'labs_header')
    # 11. PEOs (3 cards)
    swap(
        CSE_CS_PEOS_BLOCK,
        make_peos_html(dept["peos"]),
        'peos_block'
    )
    # 12. Replace draft banner with smaller partial banner
    if dept.get("keep_partial_banner"):
        if DRAFT_BANNER in text:
            text = text.replace(DRAFT_BANNER, PARTIAL_BANNER, 1)

    path.write_text(text, encoding="utf-8")
    print(f"{path.name}: ", "OK" if not misses else f"OK with misses → {misses}")


patch(HERE / "csit.html", CSIT)
patch(HERE / "it.html", IT)
