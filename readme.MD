# 🛒 Walmart Sparkathon API - Inventory Intelligence Backend

This is a Django-based backend API for inventory optimization and smart product tagging, built as part of the Walmart Sparkathon challenge. It supports reorder point calculation, product metadata ingestion, and sales trend analysis.

---

## 🚀 Features

- 🔄 Automated Reorder Point & Safety Stock Calculation
- 📦 Product & Inventory Management via Django Admin
- 📈 Sales Trends Integration
- 🧠 Smart Inventory Forecasting (weekly, based on historical patterns)
- 🛠️ Custom Django Management Commands

---

## 🛠️ Setup Instructions

### 📁 1. Clone the Repository

```bash
git clone https://github.com/your-username/walmart-sparkathon-backend.git
cd API/backend
```

### 🧪 2. Create & Activate Virtual Environment

need to create venv1 for extract_data
and venv2 for API

```bash
python -m venv venv
.env\Scriptsctivate      # On Windows
# or
source venv/bin/activate     # On Mac/Linux
```

### 📦 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 🔐 4. Setup Environment Variables

Create a `.env` file in the `API/backend/` directory:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DJ_API_KEY=your-external-api-key  # if applicable
```

---

### 🗃️ 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 👤 6. Create Admin User

```bash
python manage.py createsuperuser
```

---

### ▶️ 7. Run the Server

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) to access the admin dashboard.

---

## 🔧 Management Commands

Run any of the following to automate updates:

```bash
python manage.py update_reorder_points (based on current month and the previous years month data needs to be updated)
python manage.py update_current_stock (will generate synthetic data based on the given inputs)
python manage.py import_inventory(import data from csv files)
python manage.py update_lead_fillfillment_time(updating lead and full filment time based on the shelf life and temprature requirements)
```

---

## 📁 Project Structure

```
API/
  └── backend/
      ├── backend/              # Django settings and URLs
      ├── client/               # Core app (models, views, logic)
      ├── manage.py             # Django entry point
      ├── venv/                 # Virtual environment (ignored)
      └── .env                  # Environment variables (ignored)
extract_data/
  ├── trends_data/             # Processed trend files
  ├── sales_data_batch.csv     # Sales input
  └── extract.py               # Data transformation scripts
frontend/
  └── ...                      # (optional UI or dashboard)
```

---

## ✅ To-Do / Future Improvements

- [ ] Add Agents
- [ ] Agent Comm Setup
- [ ] Frontend
- [ ] Dockerize the backend

---

## 📄 License

This project is built for educational/hackathon purposes. Contact for reuse or extensions.

---

## 👩‍💻 Built With

- [Python 3.12](https://www.python.org/)
- [Django 5.x](https://www.djangoproject.com/)
- [NumPy](https://numpy.org/)
- [dotenv](https://pypi.org/project/python-dotenv/)

---

## ✨ Author

**Gouri Singh Rawat**
