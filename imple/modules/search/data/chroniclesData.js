/**
 * MLRIT Chronicles Data (2024-2026)
 * News, achievements, events, and updates from MLRIT
 */
(function () {
    'use strict';

    var CHRONICLES_DATA = [
        // 2026 - Placements & Achievements
        {
            title: 'Record Breaking Campus Placements 2026',
            description: 'MLRIT achieves exceptional placement results with Cognizant (107), Infosys (92), HCL Tech (85), Virtusa (41), and Deloitte (20) recruiting students.',
            date: '2026-02-15',
            category: 'Placements',
            keywords: 'placements 2026 cognizant infosys hcl virtusa deloitte jobs recruitment campus'
        },
        {
            title: 'Students Achievements 2025-26',
            description: 'MLRIT students across departments showcase exceptional performance in academics, sports, and technical competitions.',
            date: '2026-02-24',
            category: 'Achievements',
            keywords: 'students achievements 2025-26 awards recognition excellence'
        },
        {
            title: 'ECE Students Win Smart Bike Project Prize',
            description: 'Electronics and Communication Engineering students receive recognition for innovative Smart Bike project with advanced IoT features.',
            date: '2026-03-13',
            category: 'Achievements',
            keywords: 'ece electronics smart bike iot project innovation award'
        },
        
        // 2025 - Major Events & Placements
        {
            title: 'ZIGNASA 2K25: National Level 24-Hour Hackathon',
            description: 'MLRIT Code Club successfully hosts ZIGNASA 2K25, bringing together innovators, designers, and developers from across India for an intense technological challenge.',
            date: '2025-01-28',
            category: 'Events',
            keywords: 'zignasa hackathon coding competition cse code club national event technology innovation'
        },
        {
            title: 'Campus Placements 2025 - Outstanding Results',
            description: 'MLRIT students secure positions in top companies including Cognizant (65), Global Logic (36), Tech Mahindra (20), Infosys (18), and HCL (16).',
            date: '2025-03-20',
            category: 'Placements',
            keywords: 'placements 2025 cognizant global logic tech mahindra infosys hcl jobs'
        },
        {
            title: 'Microsoft Internship - 51 LPA Package',
            description: 'Sai Loukhya Chundi and Kakumanu Sailatha from Batch 2026 secure prestigious Microsoft internships with 51 LPA package and ₹1.25 Lakh/month stipend.',
            date: '2025-08-15',
            category: 'Placements',
            keywords: 'microsoft internship 51 lpa high package cse students batch 2026'
        },
        {
            title: 'Free Sports Quota Scholarships 2024-25',
            description: 'MLRIT announces free scholarships under Sports Quota for talented athletes, promoting excellence in both academics and sports.',
            date: '2025-07-10',
            category: 'Sports',
            keywords: 'sports quota scholarship free admission athletes cricket badminton volleyball'
        },
        {
            title: 'Faculty Excellence in Research Publications',
            description: 'MLRIT faculty members publish 38 journal papers, present at 14 conferences, contribute 5 book chapters, and file 15 patents.',
            date: '2025-06-05',
            category: 'Research',
            keywords: 'faculty research publications journals conferences patents books academic excellence'
        },
        {
            title: 'NSS Community Service Events 2025',
            description: 'National Service Scheme (NSS) unit organizes multiple community service events focusing on social welfare and environmental conservation.',
            date: '2025-09-21',
            category: 'Events',
            keywords: 'nss national service scheme community service social welfare environment'
        },
        {
            title: 'Wipro Certified Faculty - Mrs. Vijay Keerthika',
            description: 'CSE-AIML faculty Mrs. Vijay Keerthika achieves Wipro TalentNext Java Full Stack certification with 87% score.',
            date: '2025-04-12',
            category: 'Faculty',
            keywords: 'wipro certification faculty java full stack aiml training excellence'
        },
        
        // 2024 - Sports, Rankings & Achievements
        {
            title: 'MLRIT Excels at Two-Day Sports Meet 2024',
            description: 'MLRIT students win overall championships at the inter-collegiate sports meet, showcasing excellence across multiple sporting events.',
            date: '2024-04-16',
            category: 'Sports',
            keywords: 'sports meet 2024 championship volleyball badminton kabaddi basketball cricket athletics'
        },
        {
            title: 'NIRF Rankings 2024 - Engineering Excellence',
            description: 'MLRIT ranked in 201-300 band in NIRF Engineering Category 2024, reflecting consistent academic and research excellence.',
            date: '2024-06-10',
            category: 'Rankings',
            keywords: 'nirf rankings 2024 engineering 201-300 band national ranking excellence'
        },
        {
            title: 'Times Engineering Survey - 6th in Telangana',
            description: 'MLRIT secures 6th position in Telangana according to Times Engineering Survey 2024.',
            date: '2024-07-22',
            category: 'Rankings',
            keywords: 'times survey ranking 6th telangana engineering colleges top'
        },
        {
            title: 'Careers360 AAAA Rating Achievement',
            description: 'MLRIT receives prestigious Four-A (AAAA) accreditation from Careers360, recognizing top engineering college status.',
            date: '2024-08-05',
            category: 'Recognition',
            keywords: 'careers360 aaaa rating four-a accreditation top college recognition'
        },
        {
            title: '19 Students Placed at Eidiko Systems',
            description: 'Batch 2025 students secure positions at Eidiko Systems Integrators with 4.70 LPA package under "Right Education, Bright Placements" initiative.',
            date: '2024-11-18',
            category: 'Placements',
            keywords: 'eidiko placements 19 students batch 2025 4.70 lpa jobs'
        },
        {
            title: 'MLRIT Football Team Wins 1st Place',
            description: 'MLRIT Football Team secures first place at inter-collegiate sports tournament held at St. Peter\'s Engineering College.',
            date: '2024-03-22',
            category: 'Sports',
            keywords: 'football team first place sports tournament championship st peters'
        },
        {
            title: '3 Students Placed at Mehta Hitech Industries',
            description: 'Three students from Batch 2025 join Mehta Hitech Industries, continuing MLRIT\'s strong placement record.',
            date: '2024-12-10',
            category: 'Placements',
            keywords: 'mehta hitech placements 3 students batch 2025 manufacturing jobs'
        },
        {
            title: 'Placement Statistics 2024 - 98% Success Rate',
            description: 'MLRIT achieves 98% placement rate with 963 eligible students and 680 placed, majority from CSE department.',
            date: '2024-05-15',
            category: 'Placements',
            keywords: 'placement statistics 2024 98 percent success rate cse department jobs'
        },
        {
            title: 'EEE Department Placements 2024',
            description: 'Electrical and Electronics Engineering students secure positions in leading companies with competitive packages.',
            date: '2024-05-08',
            category: 'Placements',
            keywords: 'eee electrical electronics placements 2024 engineering jobs'
        },
        {
            title: 'Aeronautical Engineering Research Excellence',
            description: 'Dr. M.V. Narasimha Rao publishes multiple research papers on winglet design and aerodynamics in Science Direct journals.',
            date: '2024-07-15',
            category: 'Research',
            keywords: 'aeronautical research winglet design aerodynamics publications science direct faculty'
        },
        
        // Additional Chronicles
        {
            title: 'R&D Cell Promotes Innovation and Research',
            description: 'MLRIT establishes independent R&D Cell to promote research programs and need-based technology development.',
            date: '2024-09-01',
            category: 'Research',
            keywords: 'r&d research development innovation technology cell programs'
        },
        {
            title: 'AICTE Approval and NAAC Accreditation',
            description: 'MLRIT maintains AICTE approval and NAAC accreditation, ensuring quality education standards.',
            date: '2024-01-20',
            category: 'Accreditation',
            keywords: 'aicte naac accreditation approval quality education standards'
        },
        {
            title: 'NBA Accreditation for Engineering Programs',
            description: 'Multiple engineering programs receive NBA accreditation, validating curriculum quality and industry relevance.',
            date: '2024-02-28',
            category: 'Accreditation',
            keywords: 'nba accreditation engineering programs curriculum quality standards'
        },
        {
            title: 'ARIIA Innovation Ranking Achievement',
            description: 'MLRIT recognized in ARIIA (Atal Ranking of Institutions on Innovation Achievements) for fostering innovation culture.',
            date: '2024-10-12',
            category: 'Rankings',
            keywords: 'ariia innovation ranking atal achievements culture startup'
        },
        {
            title: 'Faculty Development Programs 2024',
            description: 'MLRIT organizes multiple Faculty Development Programs focusing on emerging technologies and pedagogical methods.',
            date: '2024-08-20',
            category: 'Faculty',
            keywords: 'faculty development programs fdp training workshops teaching methods'
        },
        {
            title: 'Industry-Academia Collaboration Initiatives',
            description: 'MLRIT strengthens ties with industry partners through MoUs, guest lectures, and collaborative projects.',
            date: '2024-09-15',
            category: 'Collaboration',
            keywords: 'industry academia collaboration mou partnerships projects internships'
        },
        {
            title: 'Smart Campus Infrastructure Upgrades',
            description: 'MLRIT invests in smart campus infrastructure including Wi-Fi upgrades, digital classrooms, and IoT-enabled facilities.',
            date: '2024-11-05',
            category: 'Infrastructure',
            keywords: 'smart campus infrastructure wifi digital classrooms iot technology upgrades'
        },
        {
            title: 'Student Entrepreneurship Cell Launch',
            description: 'MLRIT launches Entrepreneurship Cell to nurture startup culture and support student entrepreneurs.',
            date: '2024-10-01',
            category: 'Entrepreneurship',
            keywords: 'entrepreneurship cell startup incubation business students innovation'
        },
        {
            title: 'International Collaborations and Exchange Programs',
            description: 'MLRIT establishes international collaborations for student exchange programs and joint research initiatives.',
            date: '2024-12-15',
            category: 'International',
            keywords: 'international collaboration exchange programs global partnerships research'
        },
        {
            title: 'Green Campus Initiative 2024',
            description: 'MLRIT launches comprehensive green campus initiative focusing on sustainability, renewable energy, and environmental conservation.',
            date: '2024-06-05',
            category: 'Environment',
            keywords: 'green campus sustainability environment renewable energy conservation eco-friendly'
        }
    ];

    /**
     * Search chronicles based on query
     * @param {string} query - Search query
     * @returns {Array} Matching chronicles
     */
    function searchChronicles(query) {
        if (!query || !query.trim()) return [];
        
        var q = query.toLowerCase().trim();
        var results = [];
        
        CHRONICLES_DATA.forEach(function(item) {
            var searchText = (item.title + ' ' + item.description + ' ' + item.category + ' ' + item.keywords).toLowerCase();
            if (searchText.indexOf(q) !== -1) {
                results.push({
                    title: item.title,
                    snippet: item.description,
                    date: item.date,
                    category: item.category,
                    url: 'chronicles.html#' + encodeURIComponent(item.title.replace(/\s+/g, '-').toLowerCase())
                });
            }
        });
        
        return results;
    }

    /**
     * Get all chronicles
     * @returns {Array} All chronicles
     */
    function getAllChronicles() {
        return CHRONICLES_DATA.map(function(item) {
            return {
                title: item.title,
                snippet: item.description,
                date: item.date,
                category: item.category,
                url: 'chronicles.html?id=' + encodeURIComponent(item.title.replace(/\s+/g, '-').toLowerCase())
            };
        });
    }

    /**
     * Get chronicles by category
     * @param {string} category - Category name
     * @returns {Array} Chronicles in that category
     */
    function getByCategory(category) {
        return CHRONICLES_DATA.filter(function(item) {
            return item.category.toLowerCase() === category.toLowerCase();
        }).map(function(item) {
            return {
                title: item.title,
                snippet: item.description,
                date: item.date,
                category: item.category,
                url: 'chronicles.html?id=' + encodeURIComponent(item.title.replace(/\s+/g, '-').toLowerCase())
            };
        });
    }

    window.ChroniclesData = {
        search: searchChronicles,
        getAll: getAllChronicles,
        getByCategory: getByCategory,
        data: CHRONICLES_DATA
    };

})();
