
    // ── STANDALONE TAB SWITCHER (runs first, always works) ──
    (function () {
      var tabs = document.querySelectorAll('.dept-tab');
      var panels = document.querySelectorAll('.dept-panel');
      if (!tabs.length || !panels.length) return;
      tabs.forEach(function (tab) {
        tab.addEventListener('click', function (e) {
          e.preventDefault();
          var id = tab.getAttribute('data-tab');
          tabs.forEach(function (t) { t.classList.remove('is-active'); });
          panels.forEach(function (p) { p.classList.remove('is-active'); });
          tab.classList.add('is-active');
          var panel = document.getElementById('panel-' + id);
          if (panel) panel.classList.add('is-active');
        });
      });
    })();


    // Syllabus
    (function () {
      var regulations = {
        r25: {
          label: 'R25',
          fullSyllabus: 'cse-r25.html',
          data: {
            1: { 1: [['A7BS01','Matrices and Calculus'],['A7PH01','Advanced Engineering Physics'],['A7CS01','Programming for Problem Solving'],['A7EE01','Basic Electrical Engineering'],['A7ME01','Computer Aided Engineering Drawing'],['A7PH01L','Advanced Engineering Physics Lab'],['A7CS01L','Programming for Problem Solving Lab'],['A7EE01L','Basic Electrical Engineering Lab'],['A7CS02L','IOT and IT Workshop']],
                 2: [['A7BS02','Ordinary Differential Equations and Vector Calculus'],['A7CH01','Engineering Chemistry'],['A7CS02','Data Structures'],['A7EC01','Electronic Devices and Applications'],['A7EN01','English for Skill Enhancement'],['A7CH01L','Engineering Chemistry Lab'],['A7CS02L','Data Structures Lab'],['A7EN01L','English Communication Skills Lab'],['A7ME02L','Engineering Workshop'],['A7CS03L','Python Programming Lab']] },
            2: { 3: [['A7BS03','Mathematical and Statistical Foundations'],['A7CS03','Computer Organization and Architecture'],['A7CS04','Object Oriented Programming through Java'],['A7CS05','Software Engineering'],['A7CS06','Database Management System'],['A7BS03L','Computational Mathematics Lab'],['A7CS04L','OOP through Java Lab'],['A7CS05L','Software Engineering Lab'],['A7CS06L','DBMS Lab'],['A7CS07','Web Technologies']],
                 4: [['A7BS04','Discrete Mathematics'],['A7CS08','Operating Systems'],['A7CS09','Algorithms Design and Analysis'],['A7CS10','Computer Networks'],['A7CS11','Artificial Intelligence'],['A7CS12','Innovation and Entrepreneurship'],['A7CS08L','Operating Systems Lab'],['A7CS10L','Computer Networks Lab'],['A7CS11L','AI Lab'],['A7CS13','Data Visualization'],['A7MC01','Indian Knowledge System']] },
            3: { 5: [['A7CS14','Machine Learning'],['A7CS15','Automata and Compiler Design'],['A7CS16','Natural Language Processing'],['A7CSPE1','Professional Elective-I'],['A7CSOE1','Open Elective-I'],['A7CS14L','Machine Learning Lab'],['A7CS16L','NLP Lab'],['A7CS15L','Compiler Design Lab'],['A7CS17','Field Based Research Project'],['A7CS18','UI Design (Flutter/Android Studio)']],
                 6: [['A7CS19','Generative AI'],['A7CS20','Deep Learning'],['A7HS01','Business Economics and Financial Analysis'],['A7CSPE2','Professional Elective-II'],['A7CSOE2','Open Elective-II'],['A7CS19L','Generative AI Lab'],['A7CS20L','Deep Learning Lab'],['A7CS21L','Chatbots Lab'],['A7EN02L','English for Employability Skills Lab'],['A7CS22','Prompt Engineering'],['A7MC02','Environmental Science']] },
            4: { 7: [['A7CS23','Reinforcement Learning'],['A7CS24','Data Analytics and Visualization'],['A7HS02','Fundamentals of Management'],['A7CSPE3','Professional Elective-III'],['A7CSPE4','Professional Elective-IV'],['A7CSOE3','Open Elective-III'],['A7CS23L','Reinforcement Learning Lab'],['A7CS24L','Data Analytics Lab'],['A7CS25','Summer Internship']],
                 8: [['A7CSPE5','Professional Elective-V'],['A7CSPE6','Professional Elective-VI'],['A7CS26','Project Work']] }
          }
        },
        r22: {
          label: 'R22',
          fullSyllabus: 'cse-r22.html',
          data: {
            1: { 1: [['22BS01','Mathematics-I'],['22PH01','Engineering Physics'],['22CS01','Programming for Problem Solving (C)'],['22EE01','Basic Electrical Engineering'],['22ME01','Engineering Drawing'],['22PH01L','Physics Lab'],['22CS01L','C Programming Lab'],['22EN01L','English Lab'],['22ME02L','Workshop']],
                 2: [['22BS02','Mathematics-II'],['22CH01','Engineering Chemistry'],['22CS02','Data Structures'],['22EC01','Electronic Devices and Circuits'],['22EN01','English Communication'],['22CH01L','Chemistry Lab'],['22CS02L','DS Lab'],['22CS03L','Python Lab'],['22MC01','Environmental Science']] },
            2: { 3: [['22BS03','Probability and Statistics'],['22CS03','Computer Organization'],['22CS04','OOP through Java'],['22CS05','Discrete Mathematics'],['22CS06','Digital Logic Design'],['22CS04L','Java Lab'],['22CS06L','Digital Lab'],['22BS03L','Statistics Lab']],
                 4: [['22CS07','Database Management Systems'],['22CS08','Operating Systems'],['22CS09','Design and Analysis of Algorithms'],['22CS10','Software Engineering'],['22CS11','Computer Networks'],['22CS07L','DBMS Lab'],['22CS08L','OS Lab'],['22CS11L','CN Lab']] },
            3: { 5: [['22CS12','Compiler Design'],['22CS13','Machine Learning'],['22CS14','Web Technologies'],['22CS15','Information Security'],['22CSPE1','Professional Elective-I'],['22CS13L','ML Lab'],['22CS14L','Web Tech Lab'],['22CS16','Mini Project']],
                 6: [['22CS17','Artificial Intelligence'],['22CS18','Cloud Computing'],['22CS19','Data Mining'],['22CSPE2','Professional Elective-II'],['22CSPE3','Professional Elective-III'],['22CS18L','Cloud Lab'],['22CS20','Seminar']] },
            4: { 7: [['22CS21','Deep Learning'],['22CS22','Big Data Analytics'],['22CSPE4','Professional Elective-IV'],['22CSPE5','Professional Elective-V'],['22CS23','Project Phase-I'],['22CS21L','DL Lab'],['22CS24','Industry Internship']],
                 8: [['22CSPE6','Professional Elective-VI'],['22CS25','Project Phase-II'],['22CS26','Comprehensive Viva']] }
          }
        },
        mlr20: {
          label: 'MLR20',
          fullSyllabus: 'cse-mlr20.html',
          data: {
            1: { 1: [['20BS01','Mathematics-I'],['20PH01','Engineering Physics'],['20CS01','Problem Solving using C'],['20EE01','Basic Electrical Engineering'],['20ME01','Engineering Graphics'],['20PH01L','Physics Lab'],['20CS01L','C Lab'],['20EN01L','English Lab']],
                 2: [['20BS02','Mathematics-II'],['20CH01','Engineering Chemistry'],['20CS02','Data Structures using C'],['20EC01','Basic Electronics'],['20EN01','English'],['20CH01L','Chemistry Lab'],['20CS02L','DS Lab'],['20ME02L','Workshop']] },
            2: { 3: [['20BS03','Mathematics-III'],['20CS03','OOP using Java'],['20CS04','Computer Organization'],['20CS05','Discrete Mathematics'],['20CS06','DBMS'],['20CS03L','Java Lab'],['20CS06L','DBMS Lab'],['20BS03L','Math Lab']],
                 4: [['20CS07','Operating Systems'],['20CS08','DAA'],['20CS09','Computer Networks'],['20CS10','Software Engineering'],['20CS11','Formal Languages and Automata'],['20CS07L','OS Lab'],['20CS09L','CN Lab'],['20CS12','Professional Ethics']] },
            3: { 5: [['20CS13','Compiler Design'],['20CS14','Web Technologies'],['20CS15','Machine Learning'],['20CS16','Information Security'],['20CSPE1','Elective-I'],['20CS15L','ML Lab'],['20CS14L','Web Lab'],['20CS17','Mini Project']],
                 6: [['20CS18','AI'],['20CS19','Cloud Computing'],['20CS20','Data Mining'],['20CSPE2','Elective-II'],['20CSPE3','Elective-III'],['20CS19L','Cloud Lab'],['20CS21','Seminar']] },
            4: { 7: [['20CS22','Big Data'],['20CS23','IoT'],['20CSPE4','Elective-IV'],['20CSPE5','Elective-V'],['20CS24','Project-I'],['20CS23L','IoT Lab'],['20CS25','Internship']],
                 8: [['20CSPE6','Elective-VI'],['20CS26','Project-II'],['20CS27','Comprehensive Viva']] }
          }
        },
        mlr18: {
          label: 'MLR18',
          fullSyllabus: 'cse-mlr18.html',
          data: {
            1: { 1: [['18BS01','Mathematics-I'],['18PH01','Engineering Physics'],['18CS01','Computer Programming (C)'],['18EE01','Basic Electrical Engineering'],['18ME01','Engineering Drawing'],['18PH01L','Physics Lab'],['18CS01L','C Lab'],['18EN01L','English Lab']],
                 2: [['18BS02','Mathematics-II'],['18CH01','Engineering Chemistry'],['18CS02','Data Structures'],['18EC01','Electronic Devices'],['18EN01','English'],['18CH01L','Chemistry Lab'],['18CS02L','DS Lab'],['18ME02L','Workshop']] },
            2: { 3: [['18BS03','Mathematics-III'],['18CS03','OOP (C++)'],['18CS04','Computer Organization'],['18CS05','Discrete Mathematics'],['18CS06','DBMS'],['18CS03L','C++ Lab'],['18CS06L','DBMS Lab']],
                 4: [['18CS07','Operating Systems'],['18CS08','DAA'],['18CS09','Computer Networks'],['18CS10','Software Engineering'],['18CS11','FLAT'],['18CS07L','OS Lab'],['18CS09L','CN Lab']] },
            3: { 5: [['18CS12','Compiler Design'],['18CS13','Web Technologies'],['18CS14','Machine Learning'],['18CS15','Information Security'],['18CSPE1','Elective-I'],['18CS14L','ML Lab'],['18CS13L','Web Lab'],['18CS16','Mini Project']],
                 6: [['18CS17','AI'],['18CS18','Cloud Computing'],['18CS19','Data Mining'],['18CSPE2','Elective-II'],['18CSPE3','Elective-III'],['18CS18L','Cloud Lab'],['18CS20','Seminar']] },
            4: { 7: [['18CS21','Big Data'],['18CS22','IoT'],['18CSPE4','Elective-IV'],['18CSPE5','Elective-V'],['18CS23','Project-I'],['18CS22L','IoT Lab'],['18CS24','Internship']],
                 8: [['18CSPE6','Elective-VI'],['18CS25','Project-II'],['18CS26','Comprehensive Viva']] }
          }
        }
      };
      var syllabusUrls = {
        r25: 'syllabus/pdfs/cse-r25-syllabus.pdf',
        r22: 'syllabus/pdfs/cse-r22-syllabus.pdf',
        mlr20: 'syllabus/pdfs/cse-mlr20-syllabus.pdf',
        mlr18: 'syllabus/pdfs/cse-mlr18-syllabus.pdf'
      };
      var subjectDetails = {
        "Matrices and Calculus": ["Matrices", "Eigen Values and Eigen Vectors", "Single Variable Calculus", "Multivariable Calculus", "Multiple Integrals"],
        "Advanced Engineering Physics": ["Crystallography & Materials Characterization", "Quantum Mechanics", "Quantum Computing", "Magnetic and Dielectric Materials", "Laser and Fibre Optics"],
        "Programming for Problem Solving": ["Overview of C and Selection Structures", "Repetition, Loop Statements and Arrays", "Functions and Pointers", "Strings and User Defined Data Types", "File Handling, Searching and Sorting"],
        "Basic Electrical Engineering": ["D.C. Circuits", "A.C. Circuits", "Transformers", "Electrical Machines", "Electrical Installations"],
        "Computer Aided Engineering Drawing": ["Introduction to Engineering Graphics", "Orthographic Projections", "Projections of Regular Solids", "Development of Surfaces", "Isometric Projections"],
        "Engineering Chemistry": ["Water and Its Treatment", "Electrochemistry and Corrosion", "Energy Sources", "Polymers", "Advanced Functional Materials"],
        "English for Skill Enhancement": ["Perspectives", "Digital Transformation", "Attitude and Gratitude", "Entrepreneurship", "Integrity and Professionalism"],
        "Ordinary Differential Equations and Vector Calculus": ["First Order ODEs", "Higher Order ODEs", "Laplace Transforms", "Vector Differentiation", "Vector Integration"],
        "Data Structures": ["Introduction, Linear Lists, Stacks, Queues", "Trees, Binary Search Trees", "Multi-way Search Trees, Heaps", "Graphs, Sorting Algorithms", "Hashing and Collision Resolution"],
        "Electronic Devices and Applications": ["P-N Junction Diode Characteristics", "Applications of P-N Junction Diode", "Bipolar Junction Transistor and UJT", "Field-Effect Transistor and MOSFET", "Special Purpose Diodes"],
        "Mathematical and Statistical Foundations": ["Random Variables and Probability", "Continuous Distributions and Sampling", "Estimation", "Tests of Hypotheses", "Stochastic Processes and Markov Chains"],
        "Computer Organization and Architecture": ["Boolean Algebra and Logic Gates", "Combinational Logic", "Register Transfer and Micro-operations", "Microprogrammed Control", "I/O and Memory Organization"],
        "Object Oriented Programming through Java": ["OOP Concepts and Java Basics", "Inheritance, Packages and Interfaces", "Exception Handling and Multithreading", "Collections and Java I/O", "Java Networking and JDBC"],
        "Software Engineering": ["Introduction to Software Engineering", "Requirements Engineering", "Design Engineering", "Testing Strategies", "Risk and Quality Management"],
        "Database Management System": ["Database Concepts, ER Model", "Relational Model", "SQL: Queries, Constraints, Triggers", "Transaction Management, Concurrency", "Indexing and File Organization"],
        "Web Technologies": ["HTML5, CSS3, JavaScript", "Server-side Programming", "PHP/Node.js and Databases", "Web Frameworks", "Web Services and APIs"],
        "Discrete Mathematics": ["Mathematical Logic", "Set Theory", "Algebraic Structures", "Elementary Combinatorics", "Graph Theory"],
        "Operating Systems": ["OS Introduction and Structures", "CPU Scheduling, System Models", "Process Synchronization, Deadlocks", "Memory Management, Virtual Memory", "File System Interface and Operations"],
        "Algorithms Design and Analysis": ["Algorithm Analysis, Divide and Conquer", "Disjoint Sets, Heaps, Backtracking", "Dynamic Programming", "Greedy Method, Graph Algorithms", "Branch and Bound, NP-Completeness"],
        "Computer Networks": ["Internet, Protocols, Network Core", "Application Layer, HTTP, DNS", "Transport Layer, TCP, UDP", "Network Layer, Routing", "Link Layer, Error Detection"],
        "Artificial Intelligence": ["Introduction to AI, Problem Solving", "Search Strategies", "Knowledge Representation", "Planning and Acting", "Learning and Expert Systems"],
        "Innovation and Entrepreneurship": ["Foundations of Innovation", "Problem and Customer Identification", "Opportunity Assessment and Prototyping", "Business and Financial Models", "Startups and IPR"],
        "Machine Learning": ["Introduction to ML, Model Performance", "Feature Engineering, PCA, SVD", "Supervised Learning, Regression", "Unsupervised Learning, Clustering", "Ensemble Methods, Neural Networks"],
        "Automata and Compiler Design": ["Finite Automata and Regular Languages", "Context-Free Grammars", "Pushdown Automata", "Lexical Analysis and Parsing", "Code Generation and Optimization"],
        "Natural Language Processing": ["Text Processing and Morphology", "Language Models, N-grams", "Syntax and Parsing", "Semantics and Word Sense", "Machine Translation, Summarization"],
        "Generative AI": ["Introduction to Generative Models", "Variational Autoencoders", "Generative Adversarial Networks", "Transformer Architecture", "Large Language Models and Applications"],
        "Deep Learning": ["Neural Network Fundamentals", "Convolutional Neural Networks", "Recurrent Neural Networks, LSTM", "Attention Mechanisms, Transformers", "Advanced Architectures, GANs"],
        "Reinforcement Learning": ["MDP and Bellman Equations", "Dynamic Programming Methods", "Monte Carlo Methods", "Temporal Difference Learning", "Deep Reinforcement Learning"],
        "Data Analytics and Visualization": ["Introduction to Data Analytics", "Data Preprocessing and Cleaning", "Exploratory Data Analysis", "Statistical Analysis and Modeling", "Visualization Tools and Dashboards"],
        "Mathematical Foundations of Computer Science": ["Propositional and Predicate Logic", "Sets, Relations and Functions", "Graph Theory and Trees", "Algebraic Structures", "Lattices and Boolean Algebra"],
        "Advanced Data Structures": ["Amortized Analysis, Splay Trees", "Red-Black Trees, Skip Lists", "Tries, Suffix Trees", "B-Trees, External Sorting", "Advanced Hashing Techniques"],
        "Advanced Algorithms": ["Approximation Algorithms", "Randomized Algorithms", "Linear Programming", "Network Flow Algorithms", "Computational Geometry"],
        "Advanced Computer Architecture": ["Pipelining and ILP", "Memory Hierarchy Design", "Multiprocessor Systems", "Interconnection Networks", "GPU Architecture"]
      };
      var regPills = document.getElementById('regPills');
      var yearPills = document.getElementById('yearPills');
      var semPillsRow = document.getElementById('semPills');
      var subjectList = document.getElementById('subjectList');
      var fullSyllabusBtn = document.getElementById('fullSyllabusBtn');
      var currentReg = 'r25';
      var selectedYear = null;

      function buildYearPills() {
        var regData = regulations[currentReg].data;
        var years = Object.keys(regData);
        yearPills.innerHTML = '';
        years.forEach(function (y) {
          var p = document.createElement('button');
          p.className = 'pill';
          p.setAttribute('data-year', y);
          p.textContent = 'Year ' + y;
          yearPills.appendChild(p);
        });
        semPillsRow.innerHTML = ''; semPillsRow.style.display = 'none';
        subjectList.classList.remove('is-visible'); subjectList.innerHTML = '';
        fullSyllabusBtn.style.display = 'none';
        selectedYear = null;
      }
      buildYearPills();

      regPills.addEventListener('click', function (e) {
        var btn = e.target.closest('.pill'); if (!btn) return;
        currentReg = btn.getAttribute('data-reg');
        regPills.querySelectorAll('.pill').forEach(function (p) { p.classList.remove('is-active'); });
        btn.classList.add('is-active');
        buildYearPills();
      });

      yearPills.addEventListener('click', function (e) {
        var btn = e.target.closest('.pill'); if (!btn) return;
        var year = parseInt(btn.getAttribute('data-year')); selectedYear = year;
        yearPills.querySelectorAll('.pill').forEach(function (p) { p.classList.remove('is-active'); }); btn.classList.add('is-active');
        var sems = Object.keys(regulations[currentReg].data[year]);
        semPillsRow.innerHTML = '';
        sems.forEach(function (s) {
          var p = document.createElement('button');
          p.className = 'pill';
          p.setAttribute('data-sem', s);
          p.textContent = 'Sem ' + s;
          semPillsRow.appendChild(p);
        });
        semPillsRow.style.display = 'flex';
        subjectList.classList.remove('is-visible'); subjectList.innerHTML = '';
        fullSyllabusBtn.style.display = 'none';
      });

      semPillsRow.addEventListener('click', function (e) {
        var btn = e.target.closest('.pill'); if (!btn || !selectedYear) return;
        var sem = parseInt(btn.getAttribute('data-sem'));
        semPillsRow.querySelectorAll('.pill').forEach(function (p) { p.classList.remove('is-active'); }); btn.classList.add('is-active');
        var subjects = regulations[currentReg].data[selectedYear][sem]; if (!subjects) return;
        var pdfBase = 'syllabus/pdfs/' + currentReg + '/';
        var html = '';
        subjects.forEach(function (sub, i) {
          var code = sub[0]; var name = sub[1];
          var units = subjectDetails[name]; var uh = '';
          if (units && units.length) { uh = '<div class="subject-units"><ol>'; units.forEach(function (u) { uh += '<li>' + u + '</li>'; }); uh += '</ol></div>'; }
          var pdfLink = '<a href="' + pdfBase + code + '.pdf" target="_blank" class="subject-pdf" onclick="event.stopPropagation()">Syllabus PDF</a>';
          html += '<div class="subject-row" onclick="this.classList.toggle(\'is-expanded\')"><span class="subject-code">' + code + '</span><span class="subject-name">' + name + '</span><span class="subject-toggle">&#9654;</span>' + pdfLink + '</div>' + uh;
        });
        subjectList.innerHTML = html;
        subjectList.classList.remove('is-visible'); void subjectList.offsetWidth; subjectList.classList.add('is-visible');

        // Show "View Semester Syllabus" button with dynamic path
        var semPath = 'syllabus/cse/' + currentReg + '/year' + selectedYear + '/sem' + sem + '.html';
        fullSyllabusBtn.innerHTML = '<a href="' + semPath + '" target="_blank" class="syllabus-view-btn">View Semester Syllabus &rarr;</a>';
        fullSyllabusBtn.style.display = 'block';
      });
    })();

    // Publication filter
    (function () {
      var filters = document.getElementById('pubFilters');
      var cards = document.querySelectorAll('.pub-card');
      if (!filters || !cards.length) return;
      filters.addEventListener('click', function (e) {
        var btn = e.target.closest('.pub-filter'); if (!btn) return;
        var year = btn.getAttribute('data-year');
        filters.querySelectorAll('.pub-filter').forEach(function (f) { f.classList.remove('is-active'); }); btn.classList.add('is-active');
        cards.forEach(function (card) {
          var match = (year === 'all' || card.getAttribute('data-pub-year') === year);
          if (match) { card.classList.remove('is-hidden'); card.style.display = 'flex'; }
          else { card.classList.add('is-hidden'); setTimeout(function () { if (card.classList.contains('is-hidden')) card.style.display = 'none'; }, 350); }
        });
      });
    })();

    // Achievement toggle
    (function () {
      document.querySelectorAll('[data-achieve]').forEach(function (card) {
        var toggle = card.querySelector('.achieve-toggle');
        card.addEventListener('click', function () {
          var expanded = card.classList.toggle('is-expanded');
          if (toggle) toggle.textContent = expanded ? 'Read Less' : 'Read More';
        });
      });
    })();

    // FEATURE 4: Faculty hover → filter publications
    (function () {
      var fcards = document.querySelectorAll('.fcard');
      var pubCards = document.querySelectorAll('.pub-card');

      fcards.forEach(function (fcard) {
        var authorName = fcard.getAttribute('data-author');

        fcard.addEventListener('mouseenter', function () {
          var hasMatch = false;
          pubCards.forEach(function (pub) {
            var authorsDiv = pub.querySelector('.pub-card__authors');
            if (authorsDiv && authorsDiv.textContent.indexOf(authorName) !== -1) {
              pub.classList.remove('is-dimmed');
              hasMatch = true;
            } else {
              pub.classList.add('is-dimmed');
            }
          });
          // If no match, don't dim anything
          if (!hasMatch) pubCards.forEach(function (p) { p.classList.remove('is-dimmed'); });
        });

        fcard.addEventListener('mouseleave', function () {
          pubCards.forEach(function (pub) { pub.classList.remove('is-dimmed'); });
        });
      });
    })();
    // Dark sidebar — show items for active tab
    (function () {
      var dsItems = document.querySelectorAll('.ds-item');
      var streak = document.getElementById('navStreak');

      function fireStreak() {
        if (!streak) return;
        streak.classList.remove('is-firing');
        void streak.offsetWidth;
        streak.classList.add('is-firing');
        setTimeout(function () { streak.classList.remove('is-firing'); }, 600);
      }

      function updateSidebar(activeTab) {
        dsItems.forEach(function (item) {
          var show = item.getAttribute('data-ds-tab') === activeTab;
          item.style.display = show ? 'flex' : 'none';
          item.classList.remove('is-active');
        });
        // Activate first visible item
        var first = document.querySelector('.ds-item[data-ds-tab="' + activeTab + '"]');
        if (first) first.classList.add('is-active');
        // Also switch the active tab panel
        document.querySelectorAll('.dept-panel').forEach(function(p){ p.classList.remove('is-active'); });
        document.querySelectorAll('.dept-tab').forEach(function(t){ t.classList.remove('is-active'); });
        var panel = document.getElementById('panel-' + activeTab);
        if (panel) panel.classList.add('is-active');
        var tab = document.querySelector('.dept-tab[data-tab="' + activeTab + '"]');
        if (tab) tab.classList.add('is-active');
      }

      // Hook into tab clicks
      document.querySelectorAll('.dept-tab').forEach(function (tab) {
        tab.addEventListener('click', function (e) {
          e.preventDefault();
          updateSidebar(tab.getAttribute('data-tab'));
          fireStreak();
        });
      });

      // Sidebar item click — mark active + fire streak + scroll to section
      dsItems.forEach(function (item) {
        item.addEventListener('click', function () {
          var tab = item.getAttribute('data-ds-tab');
          var target = item.getAttribute('data-ds-target');
          // Switch to the right tab first
          updateSidebar(tab);
          // Mark this item active
          var siblings = document.querySelectorAll('.ds-item[data-ds-tab="' + tab + '"]');
          siblings.forEach(function (s) { s.classList.remove('is-active'); });
          item.classList.add('is-active');
          fireStreak();
          // Scroll to target — close other accordions, open the right one
          if (target) {
            setTimeout(function () {
              var el = document.getElementById(target);
              if (!el) return;
              // Close all open accordions first
              document.querySelectorAll('.sub-accordion.is-open').forEach(function(a) {
                a.classList.remove('is-open');
              });
              // Open accordion if target is inside one or is the header
              var accordion = el.closest ? el.closest('.sub-accordion') : null;
              if (!accordion && el.parentElement && el.parentElement.classList && el.parentElement.classList.contains('sub-accordion')) {
                accordion = el.parentElement;
              }
              if (accordion) accordion.classList.add('is-open');
              el.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }, 120);
          }
        });
      });

      // Initialize — no scroll, just set sidebar items and panel
      updateSidebar('overview');
      window.scrollTo(0, 0);

    })();

    // Scroll-spy — separate IIFE
    (function () {
      var targets = [];
      document.querySelectorAll('.ds-item[data-ds-target]').forEach(function(item) {
        var id = item.getAttribute('data-ds-target');
        var el = document.getElementById(id);
        if (el) targets.push({ el: el, item: item });
      });
      if (!targets.length) return;
      var spyReady = false;
      setTimeout(function () { spyReady = true; }, 600);
      var observer = new IntersectionObserver(function(entries) {
        if (!spyReady) return;
        entries.forEach(function(entry) {
          if (!entry.isIntersecting) return;
          var matched = targets.find(function(t) { return t.el === entry.target; });
          if (!matched) return;
          // Only update if this item is currently visible in sidebar
          if (matched.item.style.display === 'none') return;
          document.querySelectorAll('.ds-item').forEach(function(i) { i.classList.remove('is-active'); });
          matched.item.classList.add('is-active');
        });
      }, { threshold: 0.3, rootMargin: '-80px 0px -40% 0px' });
      targets.forEach(function(t) { observer.observe(t.el); });
    })();


    // Auto-open accordions when scrolled into view (open only, never force-close)
    (function () {
      var accords = document.querySelectorAll('.sub-accordion');
      if (!accords.length) return;
      var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting && !entry.target.classList.contains('is-open')) {
            entry.target.classList.add('is-open');
          }
        });
      }, { threshold: 0.2 });
      accords.forEach(function (acc) { observer.observe(acc); });
    })();

    // Accordion toggle — header clicks only
    (function () {
      document.querySelectorAll('.sub-accordion__header').forEach(function (header) {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function (e) {
          e.preventDefault();
          e.stopPropagation();
          var accordion = header.closest('.sub-accordion');
          if (!accordion) accordion = header.parentElement;
          if (accordion) {
            var wasOpen = accordion.classList.contains('is-open');
            accordion.classList.toggle('is-open');
            // Scroll into view if opening
            if (!wasOpen) {
              setTimeout(function () {
                accordion.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
              }, 50);
            }
          }
        });
      });
    })();
  