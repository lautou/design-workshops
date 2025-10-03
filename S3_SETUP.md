# **AWS S3 Setup for Image Hosting**

To resolve the image access issues, we will use an AWS S3 bucket to host the images publicly. This is a standard and robust method that completely bypasses all Google Drive and GCS limitations.

**This is a one-time setup.**

### **Step 1: Create a Public S3 Bucket**

1. Log in to your AWS Management Console and navigate to the S3 service.  
2. Click **Create bucket**.  
3. **Bucket name:** Choose a globally unique name (e.g., your-company-presentation-assets-12345).  
4. **AWS Region:** Select a region.  
5. **Object Ownership:** Select **ACLs enabled**. When prompted, choose **Object writer**. This is required for our script to set permissions on each image it uploads.  
6. **Block Public Access settings for this bucket:**  
   * **UNCHECK** the box for "Block all public access".  
   * Acknowledge the warning that this might make objects public.  
   * Of the four sub-options that appear, ensure the top two regarding ACLs are also **UNCHECKED**:  
     * **UNCHECK** Block public access...through new access control lists (ACLs)  
     * **UNCHECK** Block public access...through any access control lists (ACLs)  
   * The bottom two options regarding policies can remain checked.  
7. Click **Create bucket**.

### **Step 2: Update Environment File (.env)**

Open your .env file and add/update the following lines.

\# \--- AWS S3 Configuration \---  
AWS\_ACCESS\_KEY\_ID="YOUR\_ACCESS\_KEY\_ID\_HERE"  
AWS\_SECRET\_ACCESS\_KEY="YOUR\_SECRET\_ACCESS\_KEY\_HERE"  
S3\_BUCKET\_NAME="your-globally-unique-bucket-name"  
AWS\_REGION="your-bucket-region-e.g.,-us-east-1"

\# \--- Google Drive Configuration (Still Required\!) \---  
\# This is the folder where the FINAL Google Slides presentation will be created.  
OUTPUT\_FOLDER\_ID="YOUR\_GOOGLE\_DRIVE\_FOLDER\_ID\_HERE"

**Important:** The GOOGLE\_APPLICATION\_CREDENTIALS variable is still required for the script to interact with Google Slides and Drive.

### **Step 3: Install New Dependency**

After I provide the updated requirements.txt file, run the following command in your activated virtual environment to install the AWS library:

pip install \-r requirements.txt

Your project is now configured to use AWS S3 for image hosting.