# **Google Cloud Setup for User Authentication (OAuth 2.0)**

To allow the script to create and manage Google Slides presentations on your behalf, you must authorize it by creating a local application credential. This is a standard and secure OAuth 2.0 "Desktop App" flow.

**This is a one-time setup.**

### **Step 1: Configure the OAuth Consent Screen**

If this is your first time creating an OAuth credential in this project, you may need to configure the consent screen.

1. Go to the Google Cloud Console APIs & Services: [https://console.cloud.google.com/apis/credentials/consent](https://console.cloud.google.com/apis/credentials/consent)  
2. Select your project.  
3. For **User Type**, choose **Internal** (if everyone using this will be inside your organization) and click **CREATE**.  
4. Fill in the required fields:  
   * **App name:** "Presentation Generation Pipeline"  
   * **User support email:** Your email address  
   * **Developer contact information:** Your email address  
5. Click **SAVE AND CONTINUE** through the remaining steps. You do not need to add scopes here; the script will request them dynamically.

### **Step 2: Create the OAuth 2.0 Client ID**

1. Navigate to the Credentials page in the Google Cloud Console: [https://console.cloud.google.com/apis/credentials](https://console.cloud.google.com/apis/credentials)  
2. Click **\+ CREATE CREDENTIALS** and select **OAuth client ID**.  
3. For **Application type**, select **Desktop app**.  
4. Give it a name (e.g., "Presentation Pipeline Script") and click **CREATE**.  
5. A window will pop up. Click the **DOWNLOAD JSON** button.  
6. **Crucially, move this downloaded file into your project directory and rename it to credentials.json**. This file is sensitive and should not be committed to version control.

### **Step 3: First Run and Authorization**

1. Ensure your .env file is configured correctly per the README.md and .env.example. The GOOGLE\_APPLICATION\_CREDENTIALS variable should point to your new credentials.json file.  
2. If an old token.json file exists in your directory, delete it.  
3. Run the build script:  
   ./run\_build.sh build

4\. Your web browser will automatically open, asking you to log in to your Google account and grant permission for the scopes the application is requesting (Google Drive and Google Slides). 

5\. Log in and click "Allow". 

6\. The script will then proceed. It will create a new `token.json` file in your project directory, which it will use for all future authentications automatically.