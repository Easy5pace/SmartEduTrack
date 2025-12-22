
🎓 SmartEduTrack

Real-Time Student Progress Tracking & Analytics System

SmartEduTrack is a modern, web-based academic monitoring platform designed to improve transparency, communication, and data-driven decision-making in educational institutions. It provides real-time insights into student performance, attendance, and academic trends for students, teachers, parents, and administrators through secure, role-based access.


---

🚀 Key Features

📊 Interactive Dashboards – Visualize academic performance using charts and analytics

🔐 Role-Based Access Control (RBAC) – Secure access for students, teachers, parents, and admins

🧾 Automated Reports – Downloadable progress cards and performance summaries

🔔 Instant Notifications – Alerts for attendance shortages and academic risks

☁️ Cloud-Ready Architecture – Scalable and accessible across devices

📈 District / Institution-Level Analytics – Support administrative decision-making



---

🧠 Motivation

Traditional academic tracking systems rely heavily on manual processes and fragmented tools, resulting in delayed interventions, poor visibility, and limited parent engagement. SmartEduTrack addresses these gaps by offering a centralized, automated, and analytics-driven solution that enables timely academic support and improved educational outcomes.


---

🏗️ System Architecture (Overview)

Users (Student | Teacher | Parent | Admin)
                ↓
        Frontend (HTML, CSS, JS)
                ↓
        Backend (Flask - Python)
                ↓
     Database (MySQL / SQLite)
                ↓
   Analytics & Visualization Layer
        (Chart.js / Plotly)


---

🛠️ Technologies Used

Layer	Technologies

Frontend	HTML5, CSS3, JavaScript
Backend	Python, Flask
Database	MySQL / SQLite
Visualization	Chart.js, Plotly
Hosting	Cloud / Localhost
Version Control	Git, GitHub



---

📂 Project Structure

SmartEduTrack/
│
├── app.py                     # Main Flask application
├── requirements.txt           # Python dependencies
├── README.md                  # Project documentation
│
├── static/
│   ├── css/
│   │   └── style.css          # Stylesheets
│   ├── js/
│   │   └── scripts.js         # Client-side logic
│   └── images/                # Icons and images
│
├── templates/
│   ├── index.html             # Landing page
│   ├── login.html             # Login page
│   ├── dashboard.html         # Dashboard UI
│   └── reports.html           # Reports page
│
├── database/
│   └── smartedutrack.db       # Database file
│
└── docs/
    ├── architecture.png       # System architecture diagram
    └── project_plan.png       # Project timeline infographic


---

⚙️ Installation & Setup

Prerequisites

Python 3.8+

Git

pip


Steps

# Clone the repository
git clone https://github.com/yourusername/SmartEduTrack.git
cd SmartEduTrack

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

Access the app at:
👉 http://127.0.0.1:5000/


---

📊 Example Workflow

1. Teachers upload marks and attendance data


2. System processes and analyzes performance


3. Dashboards update in real time


4. Alerts and reports are generated automatically


5. Parents and admins receive timely insights




---

🔮 Future Enhancements

AI-based performance prediction

Personalized learning recommendations

Mobile application support

LMS integration

Advanced analytics and reporting



---

📚 References

This project is inspired by peer-reviewed research in learning analytics and educational data mining, including works by Siemens & Long (2011), Romero & Ventura (2020), and Verbert et al. (2013).


---

👨‍💻 Contributors

Project Lead: Siddesh Patil

Institution: MIT-ADT University, Pune



---

📜 License

This project is licensed under the MIT License.
You are free to use, modify, and distribute with proper attribution.


---

⭐ Support

If you find this project useful, please ⭐ star the repository and share feedback!

