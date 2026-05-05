/**
 * Static search data for MLRIT website
 * This replaces the API calls with static data
 * URLs are relative to the root directory
 */
(function () {
    'use strict';

    var SEARCH_DATA = [
        // Departments
        { title: 'Computer Science and Engineering (CSE)', description: 'Department of Computer Science and Engineering', url: 'departments/cse.html', keywords: 'cse computer science engineering department' },
        { title: 'Electronics and Communication Engineering (ECE)', description: 'Department of Electronics and Communication Engineering', url: 'departments/ece.html', keywords: 'ece electronics communication engineering department' },
        { title: 'Electrical and Electronics Engineering (EEE)', description: 'Department of Electrical and Electronics Engineering', url: 'departments/eee.html', keywords: 'eee electrical electronics engineering department' },
        { title: 'Aeronautical Engineering', description: 'Department of Aeronautical Engineering', url: 'departments/aeronautical.html', keywords: 'aeronautical aerospace engineering department' },
        { title: 'Mechanical Engineering', description: 'Department of Mechanical Engineering', url: 'departments/mechanical.html', keywords: 'mechanical engineering department' },
        { title: 'AI & Machine Learning', description: 'Department of Artificial Intelligence and Machine Learning', url: 'departments/aiml.html', keywords: 'aiml ai ml artificial intelligence machine learning department' },
        { title: 'CSE - Cyber Security', description: 'Computer Science Engineering with Cyber Security specialization', url: 'departments/cse-cs.html', keywords: 'cse cyber security cs specialization' },
        { title: 'CSE - Data Science', description: 'Computer Science Engineering with Data Science specialization', url: 'departments/cse-ds.html', keywords: 'cse data science ds specialization' },
        { title: 'Freshman Engineering', description: 'First year engineering program', url: 'departments/freshman.html', keywords: 'freshman first year engineering' },
        { title: 'MBA Program', description: 'Master of Business Administration', url: 'departments/mba.html', keywords: 'mba master business administration management' },
        { title: 'Undergraduate Programs', description: 'B.Tech programs offered at MLRIT', url: 'departments/ug.html', keywords: 'undergraduate btech programs courses ug' },
        { title: 'Postgraduate Programs', description: 'M.Tech and MBA programs', url: 'departments/pg.html', keywords: 'postgraduate mtech mba programs pg' },
        
        // Placements
        { title: 'Placements', description: 'Placement records and recruiting companies', url: 'placements/placements.html', keywords: 'placements jobs recruitment companies careers' },
        
        // Home sections
        { title: 'MLRIT Home', description: 'Marri Laxman Reddy Institute of Technology homepage', url: 'index.html', keywords: 'home homepage mlrit main' },
        { title: 'About MLRIT', description: 'Learn about Marri Laxman Reddy Institute of Technology', url: 'index.html#about', keywords: 'about mlrit college institute' },
        { title: 'Campus Life', description: 'Student life and campus facilities', url: 'index.html#campus', keywords: 'campus life facilities hostels sports' },
        { title: 'Admissions', description: 'Admission process and eligibility', url: 'index.html#admissions', keywords: 'admissions admission apply eligibility' },
        { title: 'Contact Us', description: 'Get in touch with MLRIT', url: 'index.html#contact', keywords: 'contact address phone email location' },
    ];

    /**
     * Search function that adjusts URLs based on current page location
     * @param {string} query - Search query
     * @param {string} basePath - Base path for URL adjustment ('' for root, '../' for subdirectories)
     * @returns {Array} Search results
     */
    function search(query, basePath) {
        if (!query || !query.trim()) return [];
        
        var q = query.toLowerCase().trim();
        var results = [];
        var base = basePath || '';
        
        SEARCH_DATA.forEach(function(item) {
            var searchText = (item.title + ' ' + item.description + ' ' + item.keywords).toLowerCase();
            if (searchText.indexOf(q) !== -1) {
                results.push({
                    title: item.title,
                    snippet: item.description,
                    url: base + item.url
                });
            }
        });
        
        return results;
    }

    window.StaticSearchData = {
        search: search
    };

})();
