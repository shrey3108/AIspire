from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import os
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure Gemini API
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

# Nature-inspired solutions database
nature_solutions = {
    'immune_system': {
        'title': 'Immune System Enhancement',
        'inspiration': 'Mangrove Trees',
        'description': 'Like mangrove trees that filter salt water, our solution focuses on natural body detoxification.',
        'application': 'Natural supplement program inspired by mangrove filtration systems',
        'visualization': 'mangrove_system.jpg'
    },
    'stress_relief': {
        'title': 'Stress Management',
        'inspiration': 'Forest Ecosystems',
        'description': 'Based on forest bathing (Shinrin-yoku) principles, utilizing nature\'s calming effects.',
        'application': 'Biophilic design for stress reduction in urban spaces',
        'visualization': 'forest_therapy.jpg'
    },
    'healing': {
        'title': 'Wound Healing',
        'inspiration': 'Spider Silk',
        'description': 'Inspired by spider silk\'s strength and flexibility for advanced wound care.',
        'application': 'Biomimetic bandages using nature-inspired materials',
        'visualization': 'spider_silk.jpg'
    },
    'sleep_improvement': {
        'title': 'Sleep Enhancement',
        'inspiration': 'Butterfly Chrysalis',
        'description': 'Learning from the metamorphosis process in butterflies for better sleep cycles.',
        'application': 'Natural sleep optimization techniques and environment design',
        'visualization': 'butterfly_sleep.jpg'
    },
    'mental_clarity': {
        'title': 'Mental Focus',
        'inspiration': 'Honeybee Colonies',
        'description': 'Inspired by honeybee communication and collective intelligence.',
        'application': 'Cognitive enhancement techniques based on nature\'s patterns',
        'visualization': 'honeybee_mind.jpg'
    }
}

# Research papers database
research_papers = {
    'lotus_effect': {
        'title': 'Self-Cleaning Surfaces: Learning from the Lotus Leaf',
        'authors': 'Dr. Sarah Chen, Dr. Michael Roberts',
        'year': '2024',
        'key_findings': 'Development of antimicrobial surfaces for medical equipment based on lotus leaf structure',
        'impact': 'Reduced hospital-acquired infections by 47% in trial studies'
    },
    'shark_skin': {
        'title': 'Shark Skin Biomimicry in Medical Devices',
        'authors': 'Dr. James Wilson, Dr. Emily Parker',
        'year': '2023',
        'key_findings': 'New material design reducing bacterial adhesion by 67%',
        'impact': 'Applied in catheter design, reducing infection rates significantly'
    },
    'plant_healing': {
        'title': 'Plant Cell Regeneration Models in Wound Care',
        'authors': 'Dr. Lisa Zhang, Dr. Robert Brown',
        'year': '2024',
        'key_findings': 'Novel hydrogel development mimicking plant cell wall repair',
        'impact': 'Accelerated wound healing by 35% in clinical trials'
    }
}

# Case studies database
case_studies = {
    'hospital_design': {
        'title': 'Biophilic Hospital Design',
        'location': 'Singapore General Hospital',
        'year': '2024',
        'challenge': 'High patient stress levels and slow recovery times in traditional hospital environments',
        'solution': 'Implementation of nature-inspired architecture including: healing gardens, natural light optimization, and biomimetic patterns in interior design',
        'results': [
            '28% reduction in patient stress levels measured through cortisol tests',
            '15% faster recovery times for post-surgery patients',
            '42% improvement in staff satisfaction and reduced burnout',
            'Decreased use of pain medication by 22%'
        ]
    },
    'mental_health': {
        'title': 'Forest-Inspired Therapy Spaces',
        'location': 'Mental Health Center, Stockholm',
        'year': '2023',
        'challenge': 'Traditional therapy environments lacking engagement and showing limited effectiveness for anxiety treatment',
        'solution': 'Creation of forest-mimicking therapeutic spaces using fractal patterns, natural materials, and soundscapes based on forest acoustics',
        'results': [
            '39% increase in therapy session effectiveness',
            '45% improvement in patient mood scores',
            '31% reduction in anxiety levels',
            'Increased patient engagement by 58%'
        ]
    },
    'rehabilitation': {
        'title': 'Coral Reef-Inspired Rehabilitation Center',
        'location': 'Miami Medical Center',
        'year': '2024',
        'challenge': 'Monotonous rehabilitation exercises leading to patient disengagement and slower recovery',
        'solution': 'Development of an interactive rehabilitation space inspired by coral reef ecosystems, featuring dynamic color changes and adaptive exercise patterns',
        'results': [
            '47% increase in patient exercise adherence',
            '33% improvement in rehabilitation outcomes',
            '52% higher patient satisfaction scores',
            'Reduced rehabilitation time by 25%'
        ]
    },
    'pediatric_care': {
        'title': 'Butterfly Garden Pediatric Ward',
        'location': 'Children\'s Hospital, Toronto',
        'year': '2023',
        'challenge': 'Children experiencing high anxiety and stress during hospital stays',
        'solution': 'Creation of a butterfly-inspired healing environment with metamorphosis-themed recovery journey and interactive nature elements',
        'results': [
            '41% decrease in reported anxiety levels',
            '37% reduction in pain medication requirements',
            '63% increase in physical activity during recovery',
            'Improved sleep quality in 78% of patients'
        ]
    },
    'elderly_care': {
        'title': 'Hive-Inspired Senior Living',
        'location': 'Elderly Care Center, Vancouver',
        'year': '2024',
        'challenge': 'Social isolation and reduced mobility in traditional elderly care facilities',
        'solution': 'Implementation of a honeycomb-inspired living space design that promotes natural movement patterns and social interaction',
        'results': [
            '56% increase in social interactions among residents',
            '44% improvement in mobility assessments',
            '39% reduction in depression symptoms',
            'Enhanced cognitive function in 48% of residents'
        ]
    }
}

# Store user submissions (in-memory for demo)
community_insights = []

@app.route('/')
def home():
    return render_template('index.html', 
                         solutions=nature_solutions, 
                         community_insights=community_insights,
                         research_papers=research_papers,
                         case_studies=case_studies)

@app.route('/api/get_nature_insight', methods=['POST'])
def get_nature_insight():
    data = request.json
    query = data.get('query', '')
    
    prompt = f"""Based on biomimicry principles, provide insights about how nature's solutions could be applied to this health challenge: {query}
    Focus on specific examples from nature and their practical applications in healthcare. 
    Include: 
    1. Natural phenomenon
    2. How it works
    3. Potential health applications
    4. Implementation considerations"""
    
    try:
        response = model.generate_content(prompt)
        return jsonify({'response': response.text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/submit_insight', methods=['POST'])
def submit_insight():
    if request.method == 'POST':
        insight = {
            'name': request.form.get('name'),
            'title': request.form.get('title'),
            'inspiration': request.form.get('inspiration'),
            'description': request.form.get('description'),
            'date': datetime.now().strftime("%Y-%m-%d"),
            'votes': 0
        }
        community_insights.append(insight)
        flash('Thank you for sharing your insight!', 'success')
        return redirect(url_for('home'))

@app.route('/vote_insight/<int:index>', methods=['POST'])
def vote_insight(index):
    if 0 <= index < len(community_insights):
        community_insights[index]['votes'] += 1
        return jsonify({'votes': community_insights[index]['votes']})
    return jsonify({'error': 'Invalid insight index'}), 404

@app.route('/api/visualization_data')
def get_visualization_data():
    # Sample data for visualizations
    data = {
        'categories': ['Immune System', 'Stress Relief', 'Healing', 'Sleep', 'Mental Clarity'],
        'effectiveness': [85, 92, 78, 88, 90],
        'implementation_cost': [65, 45, 80, 40, 55],
        'user_satisfaction': [90, 88, 75, 92, 85]
    }
    return jsonify(data)

@app.route('/api/research_stats')
def get_research_stats():
    stats = {
        'publications': {
            'labels': ['2020', '2021', '2022', '2023', '2024'],
            'data': [45, 68, 92, 128, 156]
        },
        'success_rates': {
            'labels': ['Clinical Trials', 'Patient Adoption', 'Hospital Implementation', 'Cost Effectiveness'],
            'data': [78, 85, 72, 90]
        },
        'global_impact': {
            'labels': ['North America', 'Europe', 'Asia', 'Africa', 'South America'],
            'data': [35, 28, 25, 15, 12]
        }
    }
    return jsonify(stats)

if __name__ == '__main__':
    app.run(debug=True)
