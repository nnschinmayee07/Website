import re, glob

# Department-specific navbar: Home | Undergraduate | Postgraduate | [Dept Name]
dept_info = {
    'cse': ('CSE', 'ug'),
    'ece': ('ECE', 'ug'),
    'eee': ('EEE', 'ug'),
    'mechanical': ('Mechanical', 'ug'),
    'aeronautical': ('Aeronautical', 'ug'),
    'mba': ('MBA', 'pg'),
}

def build_navbar(dept_name, prog_type):
    ug_active = ' style="color:#E85D1F;"' if prog_type == 'ug' else ''
    pg_active = ' style="color:#E85D1F;"' if prog_type == 'pg' else ''

    return f'''  <header class="site-header">
    <div class="masthead">
      <div class="container masthead__inner">
        <a href="../index.html" class="masthead__logo" aria-label="MLRIT Home">
          <img src="../mlrit-logo-transparent.png" alt="MLRIT Logo" />
        </a>
        <div class="masthead__tagline">
          <span>Marri Laxman Reddy Institute of Technology</span>
        </div>
        <a href="#" class="masthead__eapcet">EAPCET CODE : MLID</a>
      </div>
    </div>

    <nav class="main-nav" aria-label="Main navigation">
      <div class="container main-nav__inner">
        <ul class="main-nav__list">
          <li class="main-nav__item">
            <a href="../index.html" class="main-nav__link">Home</a>
          </li>
          <li class="main-nav__item">
            <a href="ug.html" class="main-nav__link"{ug_active}>Undergraduate</a>
          </li>
          <li class="main-nav__item">
            <a href="pg.html" class="main-nav__link"{pg_active}>Postgraduate</a>
          </li>
          <li class="main-nav__item">
            <a href="#" class="main-nav__link" style="color:#18453B; font-weight:700;">{dept_name} Department</a>
          </li>
        </ul>
      </div>
    </nav>
  </header>'''

for dept, (name, prog) in dept_info.items():
    filepath = f'c:/mlr/homepage/departments/{dept}.html'
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the entire header block from <header to </header>
    match = re.search(r'<header class="site-header">.*?</header>', content, re.DOTALL)
    if match:
        old_header = match.group(0)
        new_header = build_navbar(name, prog)
        content = content.replace(old_header, new_header)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'{dept}: navbar updated -> Home | UG | PG | {name}')
    else:
        print(f'{dept}: HEADER NOT FOUND')
