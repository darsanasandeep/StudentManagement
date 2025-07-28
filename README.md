🎓 Student Management System
------------------------------------
1. **🎯Project Title** : Student Management System
2. **✅ Goal** : Build a full-stack web application where admins, teachers, and students can interact with academic data such as attendance, grades, courses, and profiles
3. **🧱 Core Modules & Features** :
   
    1. 🧑‍🏫 **User Management**
        * Admin   | Create/manage teachers and students, assign roles  
        * Teacher | View assigned classes, mark attendance, add grades 
        * Student | View grades, attendance, and profile               

    2. 📚 **Course & Subject Management**
        * Admin creates courses and subjects
        * Teachers are assigned to subjects
        * Students are enrolled in courses
          
    3. ✅ **Attendance Management**
        * Teachers mark daily attendance
        * Students can view their attendance report
          
    4. 📝 **Grades / Marks Module**
        * Teachers upload student marks per subject
        * Students can view results
          
    5. 👤 **Profile Management**
        * All users can view and edit their profiles
        * Admin can update any user's data
      
    6. 📊 **Dashboard & Analytics**
        * Admin sees total students,attendance %, etc
        * Students see personal progress

    7. 🔐 JWT Authentication (Login/Logout with role-based access)
    8. 📂 Secure API with DRF
    9. 📈 Dashboard with Charts and Filters
    10. 🔍 Search & Pagination for data tables
   

🛠 Tech Stack
------------------
| Frontend | Backend | Database         | Auth | Deployment               |
| -------- | ------- | -----------------| ---- | ------------------------ |
| React    | Django  | MySQL / SQLite   | JWT  | Render / Vercel / Heroku |

🧪 Testing
---------------
* Use Postman for API testing
* Use Django’s `TestCase` and React Testing Library for unit tests

🚀 Live Demo
----------------
🌐 View Demo : 
🧪 Demo Credentials: Admin: admin/ admin  , Teacher: vedav@gmail.com / ved@12345 


⚙️ Setup Instructions
--------------------------
1. 🔁 Clone the repository
    git clone https://github.com/your-username/student-management-system.git
    cd student-management-system

2. 📦 Backend Setup (Django) : Backend API runs on http://localhost:8000
    pip install -r requirements.txt
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver

3. 💻 Frontend Setup (React) : Frontend runs on http://localhost:3000
    npm install
    npm start
4. 📁 Project Structure

    student-management-system/
    │
    ├── backend/
    │   ├── core/                  # Django App
    │   ├── media/          
    │   ├── manage.py
    │   └── requirements.txt
    │
    ├── frontend/
    │   ├── src/
    │   ├── public/
    │   └── package.json
    │
    └── README.md

