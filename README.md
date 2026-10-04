# 🎓 Cloud-Based Digital Certificate Generator

A complete, beginner-friendly cloud computing mini-project that automatically generates professional participation certificates and stores them directly on Google Drive using a modern web interface.

## 🌟 Features
- **Modern Web Interface**: Built using Gradio for a beautiful, responsive UI.
- **Dynamic Generation**: Automatically places names, events, and dates on a professional template.
- **Preview & PDF**: View the certificate live on the web and download it directly as a PDF.
- **Cloud Storage**: Seamlessly integrates with Google Drive in Google Colab to save files to `/content/drive/MyDrive/Generated_Certificates`.
- **Easy Reset**: One-click clear for creating multiple certificates back-to-back.

## 🛠️ Technology Stack
- **Python 3**: Core language
- **Gradio**: Frontend Web UI
- **Pillow (PIL)**: Image generation and text placement
- **ReportLab**: PDF conversion and generation
- **Google Colab & Google Drive API**: Cloud Execution & Storage

---

## 🚀 How to Run the Project (Step-by-Step)

### Option A: Run in Google Colab (Recommended for Viva/Demo)
This is the easiest way to demonstrate "Cloud-Based Execution and Storage".

1. Open your browser and go to [Google Colab](https://colab.research.google.com/).
2. Click on **File > Upload Notebook** and upload the provided `Colab_Certificate_Generator.ipynb` file.
3. Once the notebook opens, click on **Runtime > Run all** (or press `Ctrl+F9`).
4. **Google Drive Prompt**: A popup will appear asking you to connect your Google Drive. Click "Connect to Google Drive", select your Google account, and allow permissions. (This is where the certificates will be saved).
5. Scroll down to the bottom of the notebook. In a few moments, you will see a public URL like:
   `Running on public URL: https://<random-id>.gradio.live`
6. Click that link to open the beautiful web interface.
7. Enter the student details and click **Generate Certificate**.
8. Go to your Google Drive and look for a new folder called `Generated_Certificates`. You will find your PDFs and Images saved there securely in the cloud!

### Option B: Run Locally on Your Computer
If you want to run it on your own Windows/Mac machine without Colab:

1. Open a terminal or command prompt in this project folder.
2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application script:
   ```bash
   python app.py
   ```
4. A local link (usually `http://127.0.0.1:7860`) will appear in the terminal. Open it in your web browser.
5. Your generated certificates will be saved locally in a new folder called `Generated_Certificates` inside this project directory.

## 📝 Cloud Computing Concepts Demonstrated
1. **PaaS (Platform as a Service)**: Using Google Colab as the runtime environment to host the web application.
2. **SaaS (Software as a Service)**: Delivering a ready-to-use application over the internet via the Gradio public link.
3. **Cloud Storage**: Using Google Drive API integration to permanently store generated media off-device.

## 🎨 Application UI Design
The UI features a clean, white background with professional Purple (`#4B0082`) and Gold (`#D4AF37`) accents, providing an elegant and modern look. The UI is completely responsive and works on mobile devices as well.
