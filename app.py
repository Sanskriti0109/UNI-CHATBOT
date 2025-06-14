import google.generativeai as genai
from flask import Flask, request, render_template, jsonify, session
import datetime
import secrets
import re
import random

# Configure the API key
genai.configure(api_key="GEMINI API KEY")

# Use a consistent model name
MODEL_NAME = "gemini-1.5-flash-latest"

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Dictionary to store conversation history for each session
conversation_histories = {}

# Comprehensive MUJ information database
MUJ_INFO = """
ABOUT MANIPAL UNIVERSITY JAIPUR (MUJ):

FOUNDING & LEADERSHIP:
- Founded in 2011 by Dr. Ramdas Pai, founder of the Manipal Education Group
- Chancellor: Dr. K. Ramnarayan
- President: Lt. Gen. M.D. Venkatesh
- Vice Chancellor: Dr. N.N. Sharma

ACCREDITATION & RANKINGS:
- NAAC 'A+' Grade accreditation
- Ranked in 101-150 band in NIRF Engineering Rankings 2023
- QS Asia University Rankings 2024: Ranked in 351-400 band
- Times Higher Education World University Rankings 2024: 1001-1200 band
- 45th in ARIIA Rankings 2021 (Atal Ranking of Institutions on Innovation Achievements)

LOCATION & CAMPUS:
- Located in Dehmi Kalan, near Jaipur, Rajasthan, India
- Spread across 122 acres of land
- State-of-the-art infrastructure with modern classrooms, labs, and sports facilities
- Green campus with solar power generation capabilities
- On-campus residential facilities for students and faculty

ACADEMICS:
- 20+ academic departments across disciplines
- 100+ undergraduate, postgraduate, and doctoral programs
- Schools include Engineering, Management, Design, Hospitality, Sciences, Law, Architecture, and Humanities
- Industry-focused curriculum with emphasis on practical learning
- Credit-based grading system with continuous evaluation

NOTABLE COURSES:
- B.Tech programs in Computer Science, Mechanical, Civil, Electronics, AI & ML, Data Science
- MBA with specializations in Marketing, Finance, HR, Operations
- B.Arch, BBA, BCA, B.Des
- M.Tech, MCA, M.Sc programs
- Ph.D programs across all departments

ADMISSION PROCESS:
- Engineering: JEE Main scores or MU OET (Manipal University Online Entrance Test)
- Management: CAT/MAT/XAT scores or MU Management Entrance Test
- Direct admission based on 12th percentile for some courses
- International admissions through separate process

FEES STRUCTURE (APPROXIMATE):
- B.Tech: ₹2.5-3.5 lakhs per annum
- MBA: ₹4-5 lakhs per annum
- B.Des: ₹2-3 lakhs per annum
- Hostel & Mess: ₹1.2-1.5 lakhs per annum
- One-time registration fee: ₹25,000
- Caution deposit (refundable): ₹10,000

SCHOLARSHIPS:
- Merit-based scholarships up to 100% tuition fee waiver
- Sports scholarships for exceptional athletes
- Financial assistance programs for economically disadvantaged students
- Research scholarships for Ph.D students

PLACEMENTS:
- 500+ companies visit for campus recruitment annually
- Average salary package: ₹6-8 lakhs per annum
- Highest package offered: ₹45 lakhs per annum (2023 batch)
- Key recruiters: Microsoft, Amazon, Deloitte, TCS, Infosys, L&T, KPMG
- 85% placement rate across all disciplines

CAMPUS LIFE:
- 40+ student clubs and societies
- Annual cultural fest "Horizon" and technical fest "Technovation"
- Sports facilities including swimming pool, cricket ground, tennis courts
- Innovation center and incubation hub for startups
- International student exchange programs with universities in USA, UK, Australia

FACILITIES:
- Central library with 100,000+ books and digital resources
- Wi-Fi enabled campus
- 24/7 medical center with ambulance service
- Food courts and cafeterias
- Banking and ATM facilities
- Advanced research labs and workshops
- Transportation facilities connecting to Jaipur city

TRAVEL & TOURISM:
- Nearest airport: Jaipur International Airport (JAI), approximately 30 km from campus
- Nearest railway station: Jaipur Junction Railway Station, approximately 25 km
- Public transportation: Bus services and cabs readily available to/from campus
- Campus shuttle services to Jaipur city available for students

NEARBY ATTRACTIONS:
- Amber Fort (40 km): UNESCO World Heritage site with stunning architecture
- Hawa Mahal (30 km): Iconic "Palace of Winds" in pink sandstone
- City Palace (32 km): Royal residence with museums and gardens
- Jantar Mantar (31 km): UNESCO site with astronomical instruments
- Jal Mahal (28 km): Picturesque palace in Man Sagar Lake
- Nahargarh Fort (35 km): Hilltop fort with panoramic city views
- Albert Hall Museum (29 km): Oldest museum in Rajasthan
- Elefantastic (45 km): Ethical elephant sanctuary
- Chokhi Dhani (12 km): Traditional Rajasthani village experience
- World Trade Park (27 km): Modern shopping mall

LIBRARY & RESOURCES:
- Library timings: 6 AM to 11 PM on weekdays and 6 AM to 5 PM on weekends
- Online resources accessible 24/7
- Specialized research journals and databases
- Study rooms and discussion spaces available

HOSTEL INFORMATION:
- Hostel operator: GOOD HOST SPACES LTD.
- Hostel timings: Gates close at 9:00 AM, no entry allowed after 11:00 PM
- Various room configurations available (single, double, triple occupancy)
- Mess facilities with multiple cuisine options
- In-house laundry and housekeeping services

ONLINE PORTALS:
- MUJ SLCM Portal: https://mujslcm.jaipur.manipal.edu/
- Used for attendance tracking, grade viewing, and course registration
- Students can access academic records and exam schedules

UNIVERSITY TIMINGS:
- Two academic shifts: 9:00 AM to 1:30 PM and 1:30 PM to 5:00 PM
- Campus accessible to students from 9:00 AM to 9:00 PM
- Administrative offices open from 9:00 AM to 5:00 PM on weekdays

EVENTS & FESTS:
- Oneiros: Annual cultural festival featuring performances, competitions, and celebrity appearances
- TechIdeate: Technical festival showcasing innovation and engineering projects
- Genesis: Management festival with business competitions and speakers
- Various department-specific events throughout the academic year

STUDENT CLUBS:
- Technical clubs: ACM, IEEE, CyberSpace, Google Developer Student Club (GDSC)
- Cultural clubs: Music, Dance, Drama, Photography
- Professional clubs: Robotics, Coding, AI/ML, Entrepreneurship
- Sports clubs: Cricket, Football, Basketball, Volleyball

ACADEMIC SYSTEM:
- CGPA-based grading system
- Grade points: A+ (10), A (9), B+ (8), B (7), C+ (6), C (5), D (4), F (0)
- Minimum CGPA of 5.0 required to pass a course
- Semester-based academic calendar with continuous assessment

CONTACT INFORMATION:
- Address: Manipal University Jaipur, Dehmi Kalan, Off Jaipur-Ajmer Expressway, Jaipur, Rajasthan 303007
- Phone: +91-0141-3999100
- Email: info@jaipur.manipal.edu
- Website: www.jaipur.manipal.edu
"""

# Add conversational responses for greetings and common expressions
CONVERSATIONAL_RESPONSES = {
    "hi": [
        "Hi there! Welcome to the MUJ virtual assistant. How can I help you today?",
        "Hello! I'm MUJ's virtual guide. What would you like to know about our university?",
        "Hey! Great to see you. I can help with any questions about Manipal University Jaipur."
    ],
    "hello": [
        "Hello! How can I assist you with information about Manipal University Jaipur today?",
        "Hi there! I'm here to help with anything you'd like to know about MUJ.",
        "Hello! Welcome to MUJ's virtual assistant. What can I help you discover about our university?"
    ],
    "hey": [
        "Hey there! What would you like to know about Manipal University Jaipur?",
        "Hi! I'm ready to answer your questions about MUJ. What are you curious about?",
        "Hey! Great to connect. How can I help you learn more about MUJ?"
    ],
    "thanks": [
        "You're welcome! Feel free to ask if you have any other questions about MUJ.",
        "Happy to help! Is there anything else you'd like to know about our university?",
        "Glad I could assist! Don't hesitate to reach out if you need more information about MUJ."
    ],
    "thank you": [
        "You're very welcome! I'm here anytime you need information about Manipal University Jaipur.",
        "My pleasure! Feel free to ask more questions about MUJ whenever you need to.",
        "You're welcome! I hope that helps with what you needed to know about our university."
    ],
    "bye": [
        "Goodbye! Feel free to return anytime you have questions about MUJ.",
        "Take care! I'm here 24/7 if you need more information about Manipal University Jaipur.",
        "Bye for now! Wishing you all the best with your MUJ journey."
    ],
    "goodbye": [
        "Goodbye! Thank you for chatting about Manipal University Jaipur. Come back anytime!",
        "Farewell! I'm always here to help with information about MUJ whenever you need it.",
        "Take care! Hope to assist you again soon with any questions about our university."
    ],
    "okay": [
        "Great! What else would you like to know about Manipal University Jaipur?",
        "Perfect! I'm here if you need any more information about MUJ.",
        "Awesome! Any other aspects of MUJ you're curious about?"
    ],
    "ok": [
        "Great! What other questions do you have about MUJ?",
        "Perfect! I'm ready to help with any other information you might need about our university.",
        "Excellent! Is there anything else about Manipal University Jaipur you'd like to explore?"
    ]
}

@app.route('/')
def home():
    if 'session_id' not in session:
        session['session_id'] = secrets.token_hex(8)
        conversation_histories[session['session_id']] = []
    
    return render_template("index.html")

def preprocess_query(query):
    """Preprocess the query to handle variations in phrasing"""
    # Convert to lowercase for easier matching
    query = query.lower().strip()
    
    # Expand common abbreviations
    query = query.replace("muj", "manipal university jaipur")
    
    # Normalize common phrasings
    query = query.replace("tell me about", "what is")
    query = query.replace("who established", "who founded")
    query = query.replace("when was established", "when was founded")
    
    return query

def is_conversational_query(query):
    """Check if the query is a simple conversational phrase"""
    query = query.lower().strip()
    
    # Check if query matches any conversational keywords
    for key in CONVERSATIONAL_RESPONSES:
        if query == key or query.startswith(key + " ") or query.endswith(" " + key):
            return True, key
    
    return False, None

def get_random_response(key, session_id):
    """Get a semi-random response for conversational queries"""
    import random
    
    # Create a "random" index based on session_id and current hour
    # This makes responses varied but not completely random
    current_hour = datetime.datetime.now().hour
    responses = CONVERSATIONAL_RESPONSES.get(key, CONVERSATIONAL_RESPONSES["hi"])
    
    # Create a predictable but varying index
    index = (hash(session_id) + current_hour) % len(responses)
    return responses[index]

@app.route('/chat', methods=['POST'])
def chat():
    try:
        session_id = session.get('session_id')
        if not session_id or session_id not in conversation_histories:
            session['session_id'] = secrets.token_hex(8)
            conversation_histories[session['session_id']] = []
            session_id = session['session_id']
            
        user_input = request.json.get("message", "")
        print(f"User Input: {user_input}")
        
        # Check if it's a simple conversational query
        is_conversational, conv_key = is_conversational_query(user_input)
        
        if is_conversational and conv_key:
            response_text = get_random_response(conv_key, session_id)
            
            # Update conversation history
            history = conversation_histories[session_id]
            history.append({"role": "user", "parts": [user_input]})
            history.append({"role": "model", "parts": [response_text]})
            conversation_histories[session_id] = history
            
            return jsonify({"response": response_text})
        
        # Continue with normal processing for non-conversational queries
        # Preprocess the query to handle variations
        processed_input = preprocess_query(user_input)
        
        # Get current conversation history
        history = conversation_histories[session_id]
        
        # Create the model
        model = genai.GenerativeModel(
            model_name=MODEL_NAME,
            generation_config={
                "temperature": 0.3,  # Slightly higher for more engaging responses
                "max_output_tokens": 800,
                "top_p": 0.85,
                "top_k": 40
            }
        )
        
        # Create a chat session with existing history
        chat = model.start_chat(history=history)
        
        # Prepare system message with current date/time
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Combine system context with user query
        combined_prompt = f"""
        System: You are the official AI assistant for Manipal University Jaipur (MUJ). 
        Today's date: {current_date}
        Current time: {current_time}
        
        YOUR MUJ INFORMATION DATABASE:
        {MUJ_INFO}
        
        INSTRUCTIONS:
        1. Your primary purpose is to provide accurate information about MUJ.
        2. Always give direct, precise answers using the information provided above.
        3. If a query relates to MUJ but you don't have the exact data, state what you know from the database rather than making up information.
        4. Keep responses concise (2-4 sentences) unless detailed information is specifically requested.
        5. Be engaging and conversational, not just factual.
        6. If asked about dates, fees, or statistics, always use the exact figures from the database.
        7. When asked about "MUJ" or "Manipal Jaipur," understand these refer to Manipal University Jaipur.
        8. Understand variations in how questions might be phrased (e.g., "Who started MUJ" means "Who is the founder of MUJ").
        9. If a query is ambiguous, provide the most relevant information from the database.
        10. Format your response in plain text without excessive formatting.
        11. Add a friendly, conversational tone to your responses instead of being purely factual.
        
        User Query: {processed_input}
        
        IMPORTANT: Answer the query exactly as asked, extracting the relevant information from your database. Don't redirect or deflect if you have the information. Be friendly and personable in your response.
        """
        
        # Send the message with combined context
        response = chat.send_message(combined_prompt)
        
        response_text = response.text
        print(f"API Response: {response_text}")
        
        # Clean up response by removing any "As an AI assistant..." or similar phrases
        response_text = re.sub(r"(Hey there|As an AI assistant|As the official AI assistant for MUJ|Based on my information|According to my database),?\s*[,!]", "", response_text)
        response_text = response_text.strip()
        
        # Update conversation history
        history.append({"role": "user", "parts": [user_input]})
        history.append({"role": "model", "parts": [response_text]})
        conversation_histories[session_id] = history
        
        return jsonify({"response": response_text})
    
    except Exception as e:
        print(f"Error: {str(e)}")
        # More helpful error message for users
        return jsonify({"response": "I'm having trouble processing your request right now. Please try again with a clearer question about MUJ."})

if __name__ == '__main__':
    app.run(debug=True)
