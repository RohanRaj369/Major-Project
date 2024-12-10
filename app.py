from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
'''
app = Flask(__name__)

ZAP_API_KEY = 'your_zap_api_key'
ZAP_BASE_URL = 'http://localhost:8080'  # Change if ZAP runs on a different host/port

@app.route('/scan', methods=['POST'])
def scan_url():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({"error": "URL is required"}), 400
    
    # Start a new scan
    scan_url = f"{ZAP_BASE_URL}/JSON/ascan/action/scan/"
    params = {
        'url': url,
        'apikey': ZAP_API_KEY
    }
    response = requests.get(scan_url, params=params)
    
    if response.status_code != 200:
        return jsonify({"error": "Failed to start scan"}), 500
    
    scan_id = response.json().get('scan')
    
    # Polling to check scan status
    status_url = f"{ZAP_BASE_URL}/JSON/ascan/view/status/"
    while True:
        status_response = requests.get(status_url, params={'scanId': scan_id, 'apikey': ZAP_API_KEY})
        status = int(status_response.json().get('status', 0))
        if status >= 100:
            break
        time.sleep(5)  # Wait for 5 seconds before checking again

    # Fetch scan results
    result_url = f"{ZAP_BASE_URL}/JSON/core/view/alerts/"
    result_response = requests.get(result_url, params={'baseurl': url, 'apikey': ZAP_API_KEY})
    alerts = result_response.json().get('alerts', [])

    # Generate mitigation suggestions
    mitigations = {
        'SQL Injection': 'Use parameterized queries and validate inputs.',
        'XSS': 'Implement CSP, sanitize user inputs.',
        'CSRF': 'Use anti-CSRF tokens.',
        'Insecure Cookies': 'Enable Secure and HttpOnly flags for cookies.',
    }

    vulnerabilities = [
        {
            "attack": alert.get('name'),
            "risk": alert.get('risk'),
            "description": alert.get('description'),
            "mitigation": mitigations.get(alert.get('name'), "Refer to OWASP guidelines.")
        } for alert in alerts
    ]

    return jsonify({"vulnerabilities": vulnerabilities})
'''

app = Flask(__name__)

# Function to analyze URL vulnerabilities
def analyze_url(url):
    vulnerabilities = []

    # 1. Unsecured Connection
    if not url.startswith("https://"):
        vulnerabilities.append({
            "attack": "Unsecured Connection",
            "details": "The website does not use HTTPS, making it vulnerable to man-in-the-middle attacks.",
            "mitigation": "Ensure the site uses an SSL/TLS certificate to encrypt communication. "
                          "Redirect all HTTP traffic to HTTPS to enhance security. "
                          "Monitor and renew SSL certificates before expiry.",
            "color": "red"
        })

    try:
        response = requests.get(url, timeout=5)
        headers = response.headers

        # 2. Missing Content Security Policy (CSP)
        if "Content-Security-Policy" not in headers:
            vulnerabilities.append({
                "attack": "Missing Content-Security-Policy",
                "details": "The website does not implement a CSP, leaving it vulnerable to XSS attacks.",
                "mitigation": "Define a Content Security Policy (CSP) header in the server configuration. "
                              "Restrict the sources of scripts and styles using CSP directives. "
                              "Regularly update the CSP to address new threats.",
                "color": "orange"
            })

        # 3. Missing X-Frame-Options
        if "X-Frame-Options" not in headers:
            vulnerabilities.append({
                "attack": "Missing X-Frame-Options",
                "details": "The website does not set X-Frame-Options, making it vulnerable to clickjacking.",
                "mitigation": "Add an 'X-Frame-Options' header with 'DENY' or 'SAMEORIGIN' value in the server settings. "
                              "Test pages to ensure frames are not unexpectedly blocked. "
                              "Consider using the 'Content-Security-Policy: frame-ancestors' directive as a modern alternative.",
                "color": "yellow"
            })

        # 4. Missing X-Content-Type-Options
        if "X-Content-Type-Options" not in headers:
            vulnerabilities.append({
                "attack": "Missing X-Content-Type-Options",
                "details": "The website does not prevent MIME type sniffing.",
                "mitigation": "Configure the server to include 'X-Content-Type-Options: nosniff' in the response headers. "
                              "This ensures browsers interpret files only as their declared type. "
                              "Test headers after deployment to confirm correctness.",
                "color": "blue"
            })

        # 5. Open Redirects
        if "redirect=" in url or "next=" in url:
            vulnerabilities.append({
                "attack": "Open Redirect",
                "details": "The URL may allow open redirects, making it easy to redirect users to malicious sites.",
                "mitigation": "Sanitize and validate redirect parameters by using an allowlist. "
                              "Avoid using user-controlled input for redirect URLs. "
                              "Implement logging and alerts for unusual redirect patterns.",
                "color": "purple"
            })

        # 6. Directory Listing Enabled
        if "Index of" in response.text:
            vulnerabilities.append({
                "attack": "Directory Listing Enabled",
                "details": "The server has directory listing enabled, exposing sensitive files.",
                "mitigation": "Disable directory listing in the web server configuration (e.g., Apache or Nginx). "
                              "Restrict access to sensitive directories using .htaccess or similar methods. "
                              "Audit exposed directories regularly to prevent accidental exposure.",
                "color": "green"
            })

        # 7. SQL Injection
        test_payload = "?id=1' OR '1'='1"
        test_url = url + test_payload
        test_response = requests.get(test_url)
        if "error" in test_response.text.lower():
            vulnerabilities.append({
                "attack": "SQL Injection",
                "details": "The website appears vulnerable to SQL injection attacks.",
                "mitigation": "Use parameterized queries and prepared statements for database operations. "
                              "Avoid using dynamic SQL queries that concatenate user input. "
                              "Regularly scan and test for SQL injection vulnerabilities.",
                "color": "red"
            })

        # 8. Cross-Site Scripting (XSS)
        soup = BeautifulSoup(response.text, "html.parser")
        if soup.find("script"):
            vulnerabilities.append({
                "attack": "Cross-Site Scripting (XSS)",
                "details": "The website allows unescaped scripts, making it vulnerable to XSS.",
                "mitigation": "Sanitize all user inputs and validate them on both client and server sides. "
                              "Use security libraries to encode output before rendering. "
                              "Deploy a strong Content Security Policy to prevent script execution.",
                "color": "orange"
            })

        # 9. Missing Secure Cookies
        if "Set-Cookie" in headers and "Secure" not in headers["Set-Cookie"]:
            vulnerabilities.append({
                "attack": "Missing Secure Cookies",
                "details": "Cookies are not marked as Secure, making them susceptible to theft over HTTP.",
                "mitigation": "Mark all sensitive cookies as 'Secure' to restrict them to HTTPS connections. "
                              "Add the 'HttpOnly' flag to prevent client-side JavaScript from accessing cookies. "
                              "Consider using the 'SameSite' attribute to mitigate cross-site request forgery attacks.",
                "color": "purple"
            })

        # 10. Vulnerable Server Software
        if "Server" in headers:
            server = headers["Server"]
            if "Apache/2.2" in server:
                vulnerabilities.append({
                    "attack": "Vulnerable Server Software",
                    "details": "The server is running an outdated version of Apache, which may have known vulnerabilities.",
                    "mitigation": "Update the server software to the latest stable version. "
                                  "Subscribe to vendor notifications for security patches. "
                                  "Perform routine vulnerability scans to identify outdated components.",
                    "color": "red"
                })

    except requests.RequestException as e:
        vulnerabilities.append({
            "attack": "Connection Error",
            "details": f"Unable to connect to the website: {str(e)}.",
            "mitigation": "Verify the URL and ensure it is accessible from your network. "
                          "Check for DNS or server configuration issues. "
                          "Consider using an alternative endpoint for better results.",
            "color": "gray"
        })

    return vulnerabilities

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form["url"]
        vulnerabilities = analyze_url(url)
        return render_template("index.html", url=url, vulnerabilities=vulnerabilities)
    return render_template("index.html", url=None, vulnerabilities=None)

if __name__ == "__main__":
    app.run(debug=True)