# 📰 News App

A Django-powered News Application with multi-role access (Reader, Journalist, Editor), subscriptions, newsletter distribution, and RESTful API support.

## 📌 Features

- **Custom User Roles**:  
  - `Reader`: View approved articles and subscribe to journalists.  
  - `Journalist`: Create articles and newsletters.  
  - `Editor`: Approve, edit, or delete content.  

- **Article Management**:  
  - Create, edit, delete, and approve articles.  
  - Workflow with journalist submission and editor approval.

- **Newsletters**:  
  - Journalists can generate newsletters.  
  - Readers get updates based on subscriptions.

- **Subscriptions**:  
  - Readers can subscribe to specific journalists or publishers.

- **RESTful API**:  
  - Get articles based on subscriptions.  
  - API secured with token authentication.

- **Social Media Integration** (Optional):  
  - Auto-post approved articles to Twitter/X (via signals or views).

## 🏗️ Tech Stack

- **Backend**: Django, Django REST Framework  
- **Database**: MariaDB / MySQL  
- **Frontend**: Django Templates (Bootstrap recommended)  
- **Auth**: Django built-in + custom roles  
- **Optional**: Twitter API (X)

## 🎥 API Endpoints

- **Articles**: api/articles/ 


---

## 🚀 Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/your-username/news-app.git
cd news-app
