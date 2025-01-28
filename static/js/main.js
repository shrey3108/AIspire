// Function to get AI insights
async function getInsight() {
    const query = document.getElementById('health-query').value;
    const resultDiv = document.getElementById('insight-result');
    
    if (!query) {
        resultDiv.innerHTML = '<p class="error">Please enter a health challenge to get nature-inspired insights.</p>';
        return;
    }

    // Show loading state
    resultDiv.innerHTML = '<p><i class="fas fa-spinner fa-spin"></i> Analyzing nature\'s wisdom...</p>';

    try {
        const response = await fetch('/api/get_nature_insight', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();

        if (response.ok) {
            // Format and display the response
            resultDiv.innerHTML = `
                <div class="insight-content">
                    <h3><i class="fas fa-leaf"></i> Nature's Solution:</h3>
                    <p>${data.response}</p>
                </div>
            `;
        } else {
            resultDiv.innerHTML = `<p class="error"><i class="fas fa-exclamation-circle"></i> Error: ${data.error}</p>`;
        }
    } catch (error) {
        resultDiv.innerHTML = '<p class="error"><i class="fas fa-exclamation-circle"></i> Failed to get insights. Please try again later.</p>';
    }
}

// Function to show solution details
function showDetails(solutionKey) {
    const card = document.querySelector(`[data-category="${solutionKey}"]`);
    card.classList.toggle('expanded');
}

// Function to vote on community insights
async function voteInsight(index) {
    try {
        const response = await fetch(`/vote_insight/${index}`, {
            method: 'POST'
        });
        const data = await response.json();
        if (response.ok) {
            document.getElementById(`votes-${index}`).textContent = data.votes;
            // Add animation to the vote button
            const btn = document.querySelector(`#votes-${index}`).parentElement;
            btn.classList.add('voted');
            setTimeout(() => btn.classList.remove('voted'), 1000);
        }
    } catch (error) {
        console.error('Error voting:', error);
    }
}

// Initialize charts
async function initializeCharts() {
    try {
        const response = await fetch('/api/visualization_data');
        const data = await response.json();

        // Effectiveness Chart
        new Chart(document.getElementById('effectivenessChart'), {
            type: 'radar',
            data: {
                labels: data.categories,
                datasets: [{
                    label: 'Effectiveness Score',
                    data: data.effectiveness,
                    backgroundColor: 'rgba(44, 119, 68, 0.2)',
                    borderColor: 'rgba(44, 119, 68, 1)',
                    pointBackgroundColor: 'rgba(44, 119, 68, 1)'
                }]
            },
            options: {
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });

        // Cost Chart
        new Chart(document.getElementById('costChart'), {
            type: 'bar',
            data: {
                labels: data.categories,
                datasets: [{
                    label: 'Implementation Cost',
                    data: data.implementation_cost,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });

        // Satisfaction Chart
        new Chart(document.getElementById('satisfactionChart'), {
            type: 'line',
            data: {
                labels: data.categories,
                datasets: [{
                    label: 'User Satisfaction',
                    data: data.user_satisfaction,
                    fill: true,
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    tension: 0.4
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error initializing charts:', error);
    }
}

// Initialize research charts
async function initializeResearchCharts() {
    try {
        const response = await fetch('/api/research_stats');
        const data = await response.json();

        // Publications Growth Chart
        new Chart(document.getElementById('publicationsChart'), {
            type: 'line',
            data: {
                labels: data.publications.labels,
                datasets: [{
                    label: 'Number of Publications',
                    data: data.publications.data,
                    fill: true,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Biomimicry Research Growth'
                    }
                }
            }
        });

        // Success Rates Chart
        new Chart(document.getElementById('successRatesChart'), {
            type: 'radar',
            data: {
                labels: data.success_rates.labels,
                datasets: [{
                    label: 'Success Rate (%)',
                    data: data.success_rates.data,
                    backgroundColor: 'rgba(153, 102, 255, 0.2)',
                    borderColor: 'rgba(153, 102, 255, 1)',
                    pointBackgroundColor: 'rgba(153, 102, 255, 1)'
                }]
            },
            options: {
                responsive: true,
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });

        // Global Impact Chart
        new Chart(document.getElementById('globalImpactChart'), {
            type: 'doughnut',
            data: {
                labels: data.global_impact.labels,
                datasets: [{
                    data: data.global_impact.data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255, 0.8)'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'right'
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error initializing research charts:', error);
    }
}

// Add smooth scrolling for navigation links
document.querySelectorAll('nav a').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        const targetSection = document.querySelector(targetId);
        
        window.scrollTo({
            top: targetSection.offsetTop - 60,
            behavior: 'smooth'
        });
    });
});

// Add animation to solution cards on scroll
const observerOptions = {
    threshold: 0.2
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe all solution cards
document.querySelectorAll('.solution-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    observer.observe(card);
});

// Add animations for case study cards
const caseStudyObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, { threshold: 0.2 });

document.querySelectorAll('.case-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    caseStudyObserver.observe(card);
});

// Initialize all charts when the page loads
document.addEventListener('DOMContentLoaded', () => {
    initializeCharts();
    initializeResearchCharts();
});
