# 📰 News App

A Django-powered News Application with multi-role access (Reader, Journalist, Editor), subscriptions, newsletter distribution, and RESTful API support.

---

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

- **Social Media Integration (Optional)**:  
  - Auto-post approved articles to Twitter/X (via signals or views).

---

## 🏗️ Tech Stack

- **Backend**: Django, Django REST Framework  
- **Database**: MariaDB / MySQL  
- **Frontend**: Django Templates (Bootstrap recommended)  
- **Authentication**: Django built-in + custom roles  
- **Optional Integration**: Twitter API (X)

---

## 🚀 Getting Started

### 🔧 Requirements

- Python 3.8+
- pip / venv
- Docker & Docker Compose (optional)
- MariaDB or MySQL server (or use Docker)

---

### 🖥️ Run Locally (with Virtual Environment)

1. **Clone the repository**
```bash
git clone https://github.com/your-username/news-app.git
cd news-app
