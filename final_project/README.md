# RATE THE BATHROOM
#### Video Demo:  <( https://youtu.be/ABvE8E0kkLs )>
#### Description:

Rate the Bathroom is a full-stack web application where users can post reviews of bathrooms, upload images, rate other users’ reviews with stars, like posts, and interact through comments.

The goal of the project is to combine core concepts learned throughout CS50x — such as databases, backend logic, authentication, and frontend interaction — into a single cohesive application with real-world behavior similar to social platforms like Reddit or Twitter.

# 🚀 Features
👤 Authentication

User registration and login

Session-based authentication using Flask sessions

Only logged-in users can post, comment, like, or rate

📝 Reviews

Users can create bathroom reviews with:

Title

Description

Initial star rating

Up to 3 images

Each review has:

Average rating

Like count

Comment count

Review authors can delete their own posts

⭐ Ratings System

Users can rate other people’s reviews from 1 to 5 stars

Review authors cannot rate their own posts

The final average rating includes:

The author’s original rating

All user ratings

Ratings persist and remain highlighted when revisiting a post

❤️ Likes

Users can like and unlike reviews

Likes update dynamically using JavaScript (AJAX)

💬 Comments

Users can add and delete their own comments without refreshing the page

Comments display:

Username

Profile picture

Deleted comments are immediately removed from the DOM

Profile pictures update correctly in real time

👤 Profile Page

Each user has a profile page displaying:

Profile picture

Username

Number of posts

Total likes received

List of their reviews

Users can:

Edit their profile

Change username

Upload a new profile picture

Delete their account

The Edit Profile button only appears for the profile owner

🔗 Navigation

Clicking on:

A profile picture

A username (@username)

Redirects to that user’s profile page

# 🛠 Technologies Used

Python

Flask

SQLite

CS50 SQL Library

HTML / CSS

JavaScript (Fetch API / AJAX)

# 🗂 Project Structure
project/
│
├── app.py                # Main Flask application
├── helpers.py            # Helper functions (login_required, file validation)
├── project.db            # SQLite database
├── README.md             # Project documentation
│
├── static/
│   ├── style.css         # Global styles
│   └── uploads/          # User profile pictures and review images
│       └── default_pfp.png
│
├── templates/
│   ├── layout.html       # Base layout
│   ├── index.html        # Timeline
│   ├── review.html       # Review page
│   ├── rate.html         # Create review page
│   ├── profile.html      # User profile
│   ├── edit_profile.html # Edit profile
│   ├── login.html
│   ├── register.html
│   └── apology.html
│
└── flask_session/        # Session storage

# 🗃 Database Design
Users

id

username

hash

profile_picture

Reviews

id

user_id

title

description

rating (author’s initial rating)

created_at

Review Images

id

review_id

image_path

Ratings

id

user_id

review_id

stars

Likes

id

user_id

review_id

Comments

id

user_id

review_id

content

created_at

# 🧠 Design Decisions
Why AJAX for comments, likes, and ratings?

Using JavaScript with fetch() allows:

Faster interactions

No page reloads

Immediate UI feedback

This mimics real social media behavior and improves user experience.

Why store the author’s rating in the reviews table?

The author’s rating represents the original opinion of the post creator.
User ratings are stored separately, and the final average combines both.

Why SQLite?

SQLite is lightweight, easy to manage, and fully sufficient for a project of this scale while still demonstrating relational database concepts.

# ⚠️ Challenges Faced

Preventing duplicate comments due to repeated fetch calls

Keeping profile pictures consistent across pages

Ensuring deleted comments do not reappear

Handling session data correctly (user_id vs username)

Making star ratings persist after page reload

Each issue was debugged and fixed by refining backend logic and frontend rendering.

# 🌱 Future Improvements

Comment replies (threaded comments)

Search functionality

Pagination for reviews

Notifications

Dark/light theme toggle

# 🏁 Conclusion

Rate the Bathroom demonstrates a complete web application built from scratch using concepts taught in CS50x, including authentication, SQL databases, backend routing, frontend interaction, and real-world debugging.

This project reflects not only technical skills but also iterative problem-solving and design thinking.

# 💙 Thank you, CS50, for the journey. This was CS50.
