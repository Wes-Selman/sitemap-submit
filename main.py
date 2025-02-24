import logging
from google.cloud import secretmanager
import json
import google.auth
import googleapiclient.discovery
import os
from flask import Flask

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def get_secret(secret_id, project_id, version_id='latest'):
    """Fetch the secret from Google Secret Manager."""
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        response = client.access_secret_version(name=name)
        secret_string = response.payload.data.decode('UTF-8')
        logging.info('Secret retrieved successfully from Secret Manager')
        return secret_string
    except Exception as e:
        logging.error(f'Failed to retrieve secret: {str(e)}')
        raise

def build_service(credentials):
    """Build the Google Search Console API service."""
    try:
        service = googleapiclient.discovery.build('webmasters', 'v3', credentials=credentials)
        logging.info('Google Search Console service built successfully')
        return service
    except Exception as e:
        logging.error(f'Failed to build service: {str(e)}')
        raise

def submit_sitemap(service, site_url, sitemap_url):
    """Submit the sitemap to Google Search Console."""
    try:
        service.sitemaps().submit(siteUrl=site_url, feedpath=sitemap_url).execute()
        logging.info('Sitemap submitted successfully')
        return {'status': 'success', 'message': 'Sitemap submitted successfully.'}
    except Exception as e:
        logging.error(f'Failed to submit sitemap: {str(e)}')
        return {'status': 'error', 'message': str(e)}

@app.route('/')
def main():
    logging.info('Script started')

    # Parameters
    project_id = 'budulup-website'
    secret_id = 'serviceaccount'
    site_url = 'https://www.budulup.com/'
    sitemap_url = 'https://www.budulup.com/sitemap.xml'
    servicedelegate = 'wes@budulup.com'
    SCOPES = ['https://www.googleapis.com/auth/webmasters']

    # Fetch the service account key from Google Secret Manager
    service_account_key = get_secret(secret_id, project_id)
    logging.debug('Client secret obtained')

    # Use ADC for authentication
    credentials, project = google.auth.default(scopes=SCOPES)
    logging.debug('ADC credentials obtained')

    # Build the Google Search Console service
    service = build_service(credentials)

    # Submit the sitemap
    response = submit_sitemap(service, site_url, sitemap_url)
    print(json.dumps(response))

# Print the port number before starting the Flask app
print(f"Starting server on port {int(os.environ.get('PORT', 8000))}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8000)))
