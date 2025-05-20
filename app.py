from flask import Flask, render_template, request, jsonify
from fuzzywuzzy import process

app = Flask(__name__)

# Improved dictionary with more keywords
responses = {
    "hello": "Hi there! How can I help you?",
    "hi": "Hello! What can I do for you?",
    "how are you?": "I'm doing great! How about you?",
    "what are you doing": "Just talking to you and at your service!",
    "what is your name?": "My name is MUJ BOT.",
    "what is your gender?": "I am just a bot, so I have no gender.",
    "age": "I am recently developed by Arnav Rathi and Sanskriti Saxena so I am a new born xD",
    "bye": "Goodbye! Have a nice day!",
    "muj": "MUJ refers to Manipal University Jaipur. It is one of the best universities of Rajasthan situated in outskirts of Jaipur city, 25 kms towards Ajmer. The University was originated in year 2011.",
    "admission": "Admissions start in June. Visit the MUJ's official website for details.",
    "placements": "MUJ has a good placement rate with an average package of about 15 LPA. Top recruiters include Google, Microsoft, TCS and Infosys.",
    "package": "The average placement package in MUJ is about 15 LPA. The highest package offered was 70 LPA offered by Microsoft.",
    "fees": "The fee structure varies by course. The annual fee for B.Tech in CSE is around 2.5 lakh rupees.",
    "library": "The library is open from 6 AM to 11 PM on weekdays and 6 AM to 5 PM on weekends.",
    "okay": "Yess! Should I tell you more?",
    "nice": "Yess! Should I tell you more?",
    "yes": "Great! Ask me something and i'll let you know about it",
    "good": "Nicee! Tell me how can I help you today.",
    "great": "Nicee! Tell me how can I help you today.",
    "fine": "Nicee! Tell me how can I help you today.",
    "nirf ranking": "In the 2024 NIRF rankings, MUJ secured the 64th position in the University category, climbing 37 ranks from the previous year.For the Engineering category, Manipal University Jaipur is ranked 76th by NIRF 2023.",
    "courses": "MUJ offers numerous courses like B.Tech, M.Tech, MBA, and Ph.D. programs in various fields.",
    "canteen": "The MUJ canteen provides a variety of healthy and tasty food options for students.",
    "grading system": "MUJ follows a CGPA-based grading system. The grade points range from 10 (A+) to 0 (F). A minimum CGPA of 5.0 is required to pass a course.",
    "attendance": "You can check your attendance on the MUJ SLCM portal under the 'Attendance' section. Faculty updates it regularly. Students must maintain at least 75% attendance in each subject to be eligible to appear for end-semester exams",
    "exams": "Mid-term exams are usually held in the middle of the semester, and end-term exams take place at the end of the semester. The exact dates are announced by the university.",
    "syllabus": "The syllabus is sent by the faculty as Course Handouts and it is also available in MUJ official website",
    "muj slcm portal": "This is link to the protal: https://mujslcm.jaipur.manipal.edu/",
    "muj official site" : "This is the link to the site: https://jaipur.manipal.edu/",
    "hostel rules": "Hostel gates close at 9:00 AM and students are not allowed to walk inside the hostel after 11:00 PM",
    "fests": "MUJ hosts various fests like 'Oneiros' (Cultural Fest), 'TechIdeate' (Technical Fest), and 'Genesis' (Management Fest).",
    "places to visit near MUJ": "Nearby attractions include Nahargarh Fort, Amber Fort, and Hawa Mahal in Jaipur. Students also visit cafes and malls in the city.",
    "internships": "You can apply through the Training & Placement Cell, LinkedIn, or company websites. MUJ also has industry tie-ups for internship programs.",
    "clubs": "MUJ has multiple student clubs like coding, robotics, music, and dance. There are clubs like ACM, IEEE, yberSpace and Google Developer Student Club (GDSC) that organize coding contests and hackathons. The developers of mine are in Cyberspace and IEEE WIE",
    "medical": "MUJ has an on-campus medical center with doctors available. In case of emergencies, nearby hospitals are also accessible.",
    "transportation": "There are multiple ways you can visit the city. You can get a Cab easily and also you can use Govt. Bus No. 26",
    "scholarship": "MUJ offers various scholarships based on merit, sports, and financial need. Visit the scholarships section on the official website for details.",
    "dining options": "MUJ has multiple food courts, cafes, and a mess. Some popular options include Amul, Nescafé, Pizza Bakers, Dialog, Havmor, Stardom, Lets go Live, Subway, and many more...",
    "study material": "Online study materials are available on the MUJ central portal, Google Classroom, or through faculty-shared resources.",
    "lost and found": "Lost items are usually kept at the security office. You can check there or report a missing item.",
    "sports": "MUJ has facilities for cricket, football, basketball, badminton, and many more. You can register at the sports office.",
    "alumni": "MUJ has an huge active alumni association. You can join the alumni network through the university website and linkedin.",
    "hostel": "MUJ provides well-maintained hostels managed by a firm 'Good Host Spaced'. Hostels are quite specious and consists of various facilities which help students spend their time well inside the premises.",
    "timings": "University runs in 2 shifts for students. 1st shift from 9:00 AM to 1:30 PM. 2nd shift from 1:30 PM to 5:00 PM. Other than classes students can visit university anytime between 9:00 AM to 9:00 PM.",
    "thanks": "Your welcome! You can ask anything, anytime."

}

def get_best_match(user_input):
    """Finds the closest matching question from predefined responses."""
    best_match, score = process.extractOne(user_input, responses.keys())
    
    # Set a higher threshold for better accuracy
    if score > 70:  
        return responses[best_match]
    
    return "Sorry, I don't have information on that. Can you rephrase?"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_message = request.json.get("message", "").lower()
    bot_reply = get_best_match(user_message)
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
