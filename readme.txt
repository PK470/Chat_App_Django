Setup Instructions
1. Clone the Repository
Start by cloning this repository to your local machine:
git clone <repository_url>
cd <project_directory>

2. Create a Virtual Environment
Create a virtual environment to isolate the dependencies of this project:

Windows:
python -m venv venv

macOS/Linux:
python3 -m venv venv

3. Activate the Virtual Environment
Activate the virtual environment:

Windows:
venv\Scripts\activate
macOS/Linux:
source venv/bin/activate

4. Install Dependencies
Install all the required dependencies listed in the requirements.txt file:
pip install -r requirements.txt

5. Run the Development Server
Apply the migrations and then run the development server:
python manage.py migrate
python manage.py runserver

6. Access the Application
Once the server is running, open your browser and navigate to:
http://localhost:8000

7. Create an Account
On the homepage, you’ll have the option to create an account.
Sign up using your email (which will serve as the username) and other required details.
8. Start Chatting
Once you have an account, you can start messaging with other users. The application will create a separate chat room for each pair of users, where they can send and receive messages in real-time.



