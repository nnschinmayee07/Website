// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    loadHeader();
    loadFooter();
    loadSearch();
});

function loadHeader() {
    const headerHTML = `
        <!-- Top Header -->
        <header class="top-header">
            <div class="container">
                <div class="logo-section">
                    <a href="../index.html">
                        <img src="https://mlrit.ac.in/wp-content/uploads/2023/01/mlrit-logo-1.jpg" alt="MLRIT Logo" class="logo">
                    </a>
                </div>
                <div class="header-right">
                    <div class="contact-info">
                        <i class="fas fa-phone-alt"></i>
                        <span>Toll Free: <a href="tel:18005724363">1800 572 4363</a></span>
                    </div>
                    <button class="btn-eapcet">EAPCET CODE : MLID</button>
                    <a href="../pages/virtual-tour.html" class="btn-virtual-tour">VIRTUAL TOUR</a>
                    <div class="social-icons">
                        <a href="https://www.facebook.com/Mlrit/" target="_blank"><i class="fab fa-facebook-f"></i></a>
                        <a href="https://www.instagram.com/mlr_institute_of_technology/" target="_blank"><i class="fab fa-instagram"></i></a>
                        <a href="https://twitter.com/mlritin" target="_blank"><i class="fab fa-twitter"></i></a>
                        <a href="https://www.linkedin.com/company/mlrit-institute-of-technology-hyderabad" target="_blank"><i class="fab fa-linkedin-in"></i></a>
                        <a href="https://www.youtube.com/channel/UCAfZfemyTCM-965RZy6QiGA" target="_blank"><i class="fab fa-youtube"></i></a>
                    </div>
                </div>
            </div>
        </header>

        <!-- Black Navigation -->
        <nav class="black-nav">
            <div class="container">
                <ul class="nav-links">
                    <li><a href="../index.html">HOME</a></li>
                    <li><a href="../pages/events.html">EVENTS</a></li>
                    <li><a href="https://alumni.mlrit.ac.in/" target="_blank">ALUMNI</a></li>
                    <li><a href="https://mail.google.com/a/mlrinstitutions.ac.in" target="_blank">COLLEGE EMAIL</a></li>
                    <li><a href="https://lms.mlrit.ac.in/" target="_blank">LMS</a></li>
                    <li><a href="https://portal.vmedulife.com/public/auth/#/login/mlrit-hyderabad" target="_blank">ERP LOGIN</a></li>
                    <li><a href="../pages/scholarships.html">SCHOLARSHIPS</a></li>
                    <li><a href="../pages/contact.html">CONTACT US</a></li>
                    <li><a href="../pages/careers.html">CAREERS</a></li>
                    <li><a href="https://edmit.mlrit.ac.in/" target="_blank">EDMIT – COURSE REGISTRATION</a></li>
                    <li><a href="https://formbuilder.ccavenue.com/live/kotak-mahindra/kmr-educational-society" target="_blank">TRANSPORT FEE PAYMENT</a></li>
                    <li><a href="https://form.qfixonline.com/mlrinfarasture" target="_blank">HOSTEL FEE PAYMENT</a></li>
                </ul>
            </div>
        </nav>

        <!-- Red Navigation -->
        <nav class="red-nav">
            <div class="container">
                <ul class="main-nav">
                    <li><a href="../pages/about-us.html">ABOUT US</a></li>
                    <li class="dropdown">
                        <a href="../pages/departments.html" class="dropdown-toggle">DEPARTMENTS <i class="fas fa-chevron-down"></i></a>
                        <ul class="dropdown-menu">
                            <li><a href="../pages/aeronautical-engineering.html">Aeronautical Engineering</a></li>
                            <li><a href="../pages/computer-science-engineering.html">Computer Science and Engineering</a></li>
                            <li><a href="../pages/cse-cs.html">CSE - Cyber Security</a></li>
                            <li><a href="../pages/cse-ds.html">CSE - Data Science</a></li>
                            <li><a href="../pages/csit.html">Computer Science and Information Technology</a></li>
                            <li><a href="../pages/cse-aiml.html">CSE AI &amp; ML</a></li>
                            <li><a href="../pages/eee.html">Electrical And Electronics Engineering</a></li>
                            <li><a href="../pages/ece.html">Electronics and Communication Engineering</a></li>
                            <li><a href="../pages/freshman.html">Freshman</a></li>
                            <li><a href="../pages/it.html">Information Technology</a></li>
                            <li><a href="../pages/mba.html">Master of Business Administration</a></li>
                            <li><a href="../pages/mechanical-engineering.html">Mechanical Engineering</a></li>
                        </ul>
                    </li>
                    <li><a href="../pages/admissions.html">ADMISSIONS</a></li>
                    <li><a href="../pages/examinations.html">EXAMINATIONS</a></li>
                    <li><a href="../pages/placements.html">PLACEMENTS</a></li>
                    <li><a href="../pages/innovation-cell.html">INNOVATION CELL</a></li>
                    <li><a href="../pages/campus-life.html">CAMPUS LIFE</a></li>
                    <li><a href="../pages/sports.html">SPORTS</a></li>
                    <li><a href="../pages/research.html">RESEARCH</a></li>
                    <li><a href="../pages/iqac.html">IQAC</a></li>
                    <li><a href="https://naac.mlrit.ac.in/" target="_blank">NAAC SSR</a></li>
                    <li><a href="../pages/dcp.html">NBA-DCS</a></li>
                    <li><a href="../pages/chronicles.html" class="chronicles-nav-link">CHRONICLES</a></li>
                </ul>
                <!-- Search icon injected into .top-header by SearchSystem.init() -->
            </div>
        </nav>
    `;

    const headerPlaceholder = document.getElementById('header-placeholder');
    if (headerPlaceholder) {
        headerPlaceholder.innerHTML = headerHTML;
    }
}

function loadFooter() {
    const footerHTML = `
        <footer class="footer">
            <div class="container">
                <div class="footer-grid">
                    <div class="footer-column">
                        <h3>Contact Information</h3>
                        <p>Official Address:<br>
                        Dundigal V, Survey No. 444, Dundigal, Gandi maisama,<br>
                        Medchal Malkajgiri, Telangana – 500 043, Telangana</p>
                        <p><a href="tel:+919652226061">+91 96522 26061</a></p>
                        <p><a href="mailto:info@mlrinstitutions.ac.in">info@mlrinstitutions.ac.in</a></p>
                        <div class="social-icons" style="margin-top: 20px;">
                            <a href="https://www.facebook.com/Mlrit/" target="_blank"><i class="fab fa-facebook-f"></i></a>
                            <a href="https://www.instagram.com/mlr_institute_of_technology/" target="_blank"><i class="fab fa-instagram"></i></a>
                            <a href="https://twitter.com/mlritin" target="_blank"><i class="fab fa-twitter"></i></a>
                            <a href="https://www.linkedin.com/company/mlrit-institute-of-technology-hyderabad" target="_blank"><i class="fab fa-linkedin-in"></i></a>
                            <a href="https://www.youtube.com/channel/UCAfZfemyTCM-965RZy6QiGA" target="_blank"><i class="fab fa-youtube"></i></a>
                        </div>
                    </div>
                    <div class="footer-column">
                        <h3>Quick Links</h3>
                        <ul>
                            <li><a href="../pages/about-us.html">About Us</a></li>
                            <li><a href="../pages/admissions.html">Admissions</a></li>
                            <li><a href="../pages/campus-life.html">Campus Life</a></li>
                            <li><a href="../pages/examinations.html">Examinations</a></li>
                            <li><a href="../pages/placements.html">Training &amp; Placements</a></li>
                            <li><a href="../pages/sports.html">Sports</a></li>
                        </ul>
                    </div>
                    <div class="footer-column">
                        <h3>Useful Links</h3>
                        <ul>
                            <li><a href="../pages/aicte-approvals.html">AICTE Approvals</a></li>
                            <li><a href="../pages/nirf-ranked-institution.html">NIRF</a></li>
                            <li><a href="../pages/aqar.html">AQAR</a></li>
                            <li><a href="../pages/mandatory-disclosures.html">Mandatory Disclosures</a></li>
                        </ul>
                    </div>
                    <div class="footer-column">
                        <h3>Departments</h3>
                        <ul>
                            <li><a href="../pages/aeronautical-engineering.html">Aeronautical Engineering</a></li>
                            <li><a href="../pages/computer-science-engineering.html">Computer Science &amp; Engineering</a></li>
                            <li><a href="../pages/cse-aiml.html">CSE – AI &amp; ML</a></li>
                            <li><a href="../pages/ece.html">Electronics and Communication Engineering</a></li>
                            <li><a href="../pages/mechanical-engineering.html">Mechanical Engineering</a></li>
                        </ul>
                    </div>
                </div>
                <div class="footer-bottom">
                    <p>Copyright &copy; K M R Educational Society. All Rights reserved</p>
                </div>
            </div>
        </footer>

        <!-- WhatsApp Float Button -->
        <a href="https://wa.me/919652226061" class="whatsapp-float" target="_blank">
            <i class="fab fa-whatsapp"></i>
        </a>

        <!-- Brochure Button -->
        <a href="https://mlrit.ac.in/wp-content/uploads/2024/05/MLRIT_Brochure.pdf" class="brochure-btn" target="_blank">Brochure</a>
    `;

    const footerPlaceholder = document.getElementById('footer-placeholder');
    if (footerPlaceholder) {
        footerPlaceholder.innerHTML = footerHTML;
    }
}

// Load search module on all sub-pages that use page-loader.js.
// Loads CSS + all component scripts in dependency order, then calls SearchSystem.init().
// Pages that already include the scripts directly (chronicles.html, search-results.html)
// are protected by the double-init guard inside SearchSystem.init().
function loadSearch() {
    var BASE = '../';

    // Helper: inject a <link> stylesheet once
    function loadCSS(href) {
        if (document.querySelector('link[href="' + href + '"]')) return;
        var link = document.createElement('link');
        link.rel  = 'stylesheet';
        link.href = href;
        document.head.appendChild(link);
    }

    // Helper: load a script and return a Promise (skips if already loaded)
    function loadScript(src) {
        return new Promise(function (resolve, reject) {
            if (document.querySelector('script[src="' + src + '"]')) { resolve(); return; }
            var s = document.createElement('script');
            s.src     = src;
            s.onload  = resolve;
            s.onerror = reject;
            document.body.appendChild(s);
        });
    }

    // Load CSS immediately (non-blocking)
    loadCSS(BASE + 'modules/search/styles/search.css');

    // Load scripts in dependency order, then init
    loadScript(BASE + 'modules/search/utils/searchEngine.js')
        .then(function () { return loadScript(BASE + 'modules/search/components/SearchOverlay.js'); })
        .then(function () { return loadScript(BASE + 'modules/search/components/SearchInput.js'); })
        .then(function () { return loadScript(BASE + 'modules/search/components/FAQList.js'); })
        .then(function () { return loadScript(BASE + 'modules/search/components/SearchResultsPreview.js'); })
        .then(function () { return loadScript(BASE + 'modules/search/index.js'); })
        .then(function () {
            if (window.SearchSystem) {
                // Double-init guard inside SearchSystem.init() prevents duplicate overlays
                window.SearchSystem.init({
                    basePath:   BASE,
                    apiBase:    '',
                    debounceMs: 300,
                    faqItems:   []
                });
            }
        })
        .catch(function (err) {
            console.warn('[SearchSystem] Failed to load search module:', err);
        });
}
