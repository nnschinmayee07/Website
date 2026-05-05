"""
Phase C — refresh faculty grids in aiml.html, cse-cs.html, and cse-ds.html
with the real rosters scraped from
  https://mlrit.ac.in/faculty_categories/cse-aiml/
  https://mlrit.ac.in/faculty_categories/cse-cyber-security/
  https://mlrit.ac.in/faculty_categories/cse-ds/

Reuses the fcard generator from _phase_c_csit_it_faculty.py to keep visual
consistency with csit.html and it.html.
"""
from pathlib import Path
import importlib.util
import sys

HERE = Path(__file__).resolve().parent

# Pull the fcard helpers + regex from the sibling script (avoid duplication)
spec = importlib.util.spec_from_file_location(
    "_p_csit_it", HERE / "_phase_c_csit_it_faculty.py"
)
mod = importlib.util.module_from_spec(spec)
sys.modules["_p_csit_it"] = mod
spec.loader.exec_module(mod)

GRID_RE = mod.GRID_RE
build_grid_inner = mod.build_grid_inner

# ---- rosters ----------------------------------------------------------------

AIML = [
    ("Dr. Kashi Sai Prasad",          "Associate Professor & HOD", "", True),
    ("Dr. K. Varada Rajkumar",        "Professor",            "",  False),
    ("Dr. Penubaka Kiran Kumar Reddy", "Professor",           "",  False),
    ("VS Pavan Kumar",                "Associate Professor",  "",  False),
    ("Bidinamcherla Ammanni",         "Associate Professor",  "",  False),
    ("Dr. Sivakrishna Kondaveeti",    "Associate Professor",  "",  False),
    ("G. Sowmya",                     "Associate Professor",  "",  False),
    ("Singanamala Priyanka",          "Assistant Professor",  "",  False),
    ("Pasupuleti Pavani",             "Assistant Professor",  "",  False),
    ("Remedi Sravani",                "Assistant Professor",  "",  False),
    ("Lakshmi Saritha",               "Assistant Professor",  "",  False),
    ("Komari Biksheswara Rao",        "Assistant Professor",  "",  False),
    ("E. Raghavender",                "Assistant Professor",  "",  False),
    ("Seedarla Sandhya Rani",         "Assistant Professor",  "",  False),
    ("Shaik Gouse Pasha",             "Assistant Professor",  "",  False),
    ("M. Lakshmi Saranya",            "Assistant Professor",  "",  False),
    ("Pottapinjara Babu",             "Assistant Professor",  "",  False),
    ("B. Mamatha",                    "Assistant Professor",  "",  False),
    ("T. Aswani",                     "Assistant Professor",  "",  False),
    ("Ravi Gangadharolla",            "Assistant Professor",  "",  False),
    ("Pacha Swathi",                  "Assistant Professor",  "",  False),
    ("T. Nagini",                     "Assistant Professor",  "",  False),
    ("H. Ramanjineyulu",              "Assistant Professor",  "",  False),
    ("Talari Meena",                  "Assistant Professor",  "",  False),
    ("Nemala Jayasri",                "Assistant Professor",  "",  False),
    ("Gunda Aishwarya",               "Assistant Professor",  "",  False),
    ("P. Lokesh Kumar",               "Assistant Professor",  "",  False),
    ("J. Teja",                       "Assistant Professor",  "",  False),
    ("Mrs. K. Anusha",                "Assistant Professor",  "",  False),
    ("Mr. R. Akhilesh Reddy",         "Assistant Professor",  "",  False),
    ("P. Sai Kumar",                  "Assistant Professor",  "",  False),
    ("Damala Obulesu",                "Assistant Professor",  "",  False),
    ("Bhaskar Mekala",                "Assistant Professor",  "",  False),
    ("Masigari Nagalakshmi",          "Assistant Professor",  "",  False),
    ("Y. Naveen",                     "Assistant Professor",  "",  False),
    ("Kallam Hemanthi",               "Assistant Professor",  "",  False),
    ("Vijay Keerthika",               "Assistant Professor",  "",  False),
    ("G. Umamaheswari",               "Assistant Professor",  "",  False),
    ("K. Jyothsna Reddy",             "Assistant Professor",  "",  False),
]

CSE_CS = [
    ("Dr. P. Subhashini",       "Professor & HOD",     "", True),
    ("Mr. Atluri Srujan",       "Assistant Professor", "", False),
    ("Manisha Kandukuri",       "Assistant Professor", "", False),
    ("Juttu Suresh",            "Assistant Professor", "", False),
    ("K. Shiva Krishna",        "Assistant Professor", "", False),
    ("Bochu Sandhya",           "Assistant Professor", "", False),
    ("Mrs. Swathi Dendi",       "Assistant Professor", "", False),
    ("Mrs. Y. Anjali Satyavati", "Assistant Professor", "", False),
    ("Irfan Bagawan",           "Assistant Professor", "", False),
    ("Kiran Kumar Reddy A.",    "Assistant Professor", "", False),
    ("Ms. Mukku Bhavana",       "Assistant Professor", "", False),
    ("Bolagani Balaji",         "Assistant Professor", "", False),
    ("Ms. D. Tejaswini",        "Assistant Professor", "", False),
    ("Mrs. Ch. Sharonu Pushpa", "Assistant Professor", "", False),
    ("G. Umamaheswari",         "Assistant Professor", "", False),
]

CSE_DS = [
    ("Dr. P. Subhashini",          "Professor & HOD",     "", True),
    ("Dr. D.B.K. Kamesh",          "Professor",           "", False),
    ("Dr. Damalla Jyothi",         "Associate Professor", "", False),
    ("Dr. P. Salma Khatoon",       "Associate Professor", "", False),
    ("Dr. Veerasekhar Reddy",      "Associate Professor", "", False),
    ("Arshiya Begum",              "Assistant Professor", "", False),
    ("Tahneyath Ahmed",            "Assistant Professor", "", False),
    ("K. Rani",                    "Assistant Professor", "", False),
    ("Manasaraj",                  "Assistant Professor", "", False),
    ("S. Shakina",                 "Assistant Professor", "", False),
    ("Sravanthi Anumasula",        "Assistant Professor", "", False),
    ("D. Srivalli",                "Assistant Professor", "", False),
    ("D. Gayathri",                "Assistant Professor", "", False),
    ("N. Baby Rani",               "Assistant Professor", "", False),
    ("Dasari Amulya",              "Assistant Professor", "", False),
    ("V. Divya",                   "Assistant Professor", "", False),
    ("Ms. P. Nishitha",            "Assistant Professor", "", False),
    ("A. Nirisha",                 "Assistant Professor", "", False),
    ("S. Anudeep",                 "Assistant Professor", "", False),
    ("Ms. Madhavi Banala",         "Assistant Professor", "", False),
    ("Mrs. Pallavi Mechineni",     "Assistant Professor", "", False),
    ("Bochu Sandhya",              "Assistant Professor", "", False),
    ("Mrs. Swathi Dendi",          "Assistant Professor", "", False),
    ("Mrs. Banoth Rajeshwari",     "Assistant Professor", "", False),
    ("Irfan Bagawan",              "Assistant Professor", "", False),
    ("Kiran Kumar Reddy A.",       "Assistant Professor", "", False),
    ("Bolagani Balaji",            "Assistant Professor", "", False),
    ("Malothu Sindhuja",           "Assistant Professor", "", False),
    ("Hasina Nasrin",              "Assistant Professor", "", False),
    ("Ms. K. Alankruthi",          "Assistant Professor", "", False),
    ("Mrs. B. Ravali Reddy",       "Assistant Professor", "", False),
    ("Mathipogu Ashok Babu",       "Assistant Professor", "", False),
    ("Mrs. K. Srinija",            "Assistant Professor", "", False),
    ("Bhukya Balakrishna",         "Assistant Professor", "", False),
    ("Jangam Nagaraju",            "Assistant Professor", "", False),
    ("Mary Navyatha Govindu",      "Assistant Professor", "", False),
    ("N. Thulasi Chithra",         "Assistant Professor", "", False),
    ("Mrs. S. Parvathi",           "Assistant Professor", "", False),
    ("N. Sandhya",                 "Assistant Professor", "", False),
    ("Mrs. M. Srividya",           "Assistant Professor", "", False),
    ("Ms. D. Neelima Priyadarshini", "Assistant Professor", "", False),
    ("Ms. N. Vijayasri",           "Assistant Professor", "", False),
    ("Rowsonara Begum",            "Assistant Professor", "", False),
    ("Mr. Mohd Anwar Ali",         "Assistant Professor", "", False),
    ("Ms. B. Sushma",              "Assistant Professor", "", False),
    ("Mr. D. Sandeep",             "Assistant Professor", "", False),
    ("S. Navya",                   "Assistant Professor", "", False),
]


def patch(path: Path, roster, dept_slug: str) -> None:
    text = path.read_text(encoding="utf-8")
    new_inner = "\n" + build_grid_inner(roster, dept_slug)
    new_text, count = GRID_RE.subn(
        lambda m: m.group(1) + new_inner + m.group(3), text, count=1
    )
    if count == 0:
        print(f"FAIL: faculty-grid block not located in {path.name}")
        return
    path.write_text(new_text, encoding="utf-8")
    print(f"{path.name}: replaced grid with {len(roster)} faculty cards")


patch(HERE / "aiml.html",   AIML,   "aiml")
patch(HERE / "cse-cs.html", CSE_CS, "cse-cs")
patch(HERE / "cse-ds.html", CSE_DS, "cse-ds")
