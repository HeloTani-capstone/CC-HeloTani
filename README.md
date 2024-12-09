# HeloTani API Deployment Guide

This guide explains how to run and deploy the HeloTani API locally and on Google Cloud Run.

---

## Run Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/HeloTani-capstone/CC-HeloTani.git
   cd CC-HeloTani
   ```

2. **Run the API**:
   Ensure you have Python installed on your system, then run:
   ```bash
   python api.py
   ```

---

## Deploy to Google Cloud Run

### Prerequisites
- Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install).
- Ensure you have a Google Cloud account and a project set up.

### Steps to Deploy

1. **Authenticate with Google Cloud**:
   Log in to your Google Cloud account:
   ```bash
   gcloud auth login
   ```

2. **Set Up Your GCP Project**:
   Select or create a project in the Google Cloud Console. Then configure the project in your terminal:
   ```bash
   gcloud config set project <your-project-id>
   ```
   Replace `<your-project-id>` with your GCP project ID.

3. **Enable Required APIs**:
   Enable Cloud Run and Container Registry APIs:
   ```bash
   gcloud services enable run.googleapis.com containerregistry.googleapis.com
   ```

4. **Build the Docker Image**:
   Navigate to the project directory and build the Docker image:
   ```bash
   gcloud builds submit --tag gcr.io/<your-project-id>/helotani-api .
   ```
   Replace `<your-project-id>` with your GCP project ID.

5. **Deploy to Cloud Run**:
   Deploy the application to Cloud Run:
   ```bash
   gcloud run deploy helotani-api \
     --image gcr.io/<your-project-id>/helotani-api \
     --platform managed \
     --region <region> \
     --allow-unauthenticated
   ```
   Replace `<your-project-id>` with your GCP project ID and `<region>` with your preferred region (e.g., `us-central1`).

6. **Access Your API**:
   After deployment, you will receive a URL for your API. Use this URL to access your deployed API.

---

### Example
```bash
# Authenticate
gcloud auth login

# Set project
gcloud config set project my-project-id

# Enable APIs
gcloud services enable run.googleapis.com containerregistry.googleapis.com

# Build Docker image
gcloud builds submit --tag gcr.io/my-project-id/helotani-api .

# Deploy to Cloud Run
gcloud run deploy helotani-api \
  --image gcr.io/my-project-id/helotani-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

Feel free to contribute or report any issues in this repository!

