import os
import gradio as gr
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A4

# Check if running in Google Colab
IN_COLAB = False
try:
    from google.colab import drive
    IN_COLAB = True
except ImportError:
    pass

# Determine save directory
if IN_COLAB:
    # Mount Google Drive if in Colab
    drive.mount('/content/drive')
    SAVE_DIR = '/content/drive/MyDrive/Generated_Certificates'
else:
    # Save locally if not in Colab
    SAVE_DIR = './Generated_Certificates'

# Ensure the save directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

# Generate a basic template if it doesn't exist
TEMPLATE_PATH = "certificate_template.png"

def create_default_template():
    if not os.path.exists(TEMPLATE_PATH):
        # Create a blank image with white background
        img = Image.new('RGB', (1200, 800), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Draw a gold border
        draw.rectangle([20, 20, 1180, 780], outline="#D4AF37", width=10)
        # Draw a purple inner border
        draw.rectangle([40, 40, 1160, 760], outline="#4B0082", width=5)
        
        # Save the template
        img.save(TEMPLATE_PATH)

create_default_template()

def generate_certificate(student_name, event_name, organizer_name, event_date):
    if not student_name or not event_name or not organizer_name or not event_date:
        return None, None, "❌ Error: All fields are required."
    
    try:
        # Load the template
        img = Image.open(TEMPLATE_PATH)
        draw = ImageDraw.Draw(img)
        
        # Load fonts gracefully (Colab Linux fonts vs Windows fonts)
        try:
            # Try Linux fonts (Google Colab default)
            font_title = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf", 60)
            font_text = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf", 40)
            font_name = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSerif-BoldItalic.ttf", 80)
        except IOError:
            try:
                # Try Windows fonts (Local testing)
                font_title = ImageFont.truetype("arialbd.ttf", 60)
                font_text = ImageFont.truetype("arial.ttf", 40)
                font_name = ImageFont.truetype("ariali.ttf", 80)
            except IOError:
                # Absolute fallback (might look small, but prevents crashing)
                font_title = ImageFont.load_default()
                font_text = ImageFont.load_default()
                font_name = ImageFont.load_default()

        # Certificate Text content
        title = "CERTIFICATE OF PARTICIPATION"
        subtitle = "This is proudly presented to"
        
        # Helper function to center text
        def draw_centered_text(text, y, font, fill):
            # Fallback for older PIL versions
            if hasattr(draw, 'textbbox'):
                bbox = draw.textbbox((0, 0), text, font=font)
                w = bbox[2] - bbox[0]
            else:
                w, h = draw.textsize(text, font=font)
            draw.text(((1200 - w) / 2, y), text, font=font, fill=fill)

        # Draw text onto image
        draw_centered_text(title, 150, font_title, "#4B0082")  # Purple
        draw_centered_text(subtitle, 250, font_text, "#000000")
        
        # Student Name
        draw_centered_text(student_name.upper(), 350, font_name, "#D4AF37") # Gold
        
        body_text = f"for active participation in the event"
        draw_centered_text(body_text, 480, font_text, "#000000")
        
        draw_centered_text(event_name, 550, font_title, "#4B0082")
        
        # Footer details
        footer_text = f"Organized by {organizer_name} on {event_date}"
        draw_centered_text(footer_text, 680, font_text, "#000000")

        # Create safe filenames
        safe_name = student_name.replace(" ", "_").replace("/", "")
        img_filename = f"{safe_name}_certificate.png"
        img_path = os.path.join(SAVE_DIR, img_filename)
        
        # Save Image preview
        img.save(img_path)
        
        # Generate PDF
        pdf_filename = f"{safe_name}_certificate.pdf"
        pdf_path = os.path.join(SAVE_DIR, pdf_filename)
        
        # Create PDF in landscape A4
        c = canvas.Canvas(pdf_path, pagesize=landscape(A4))
        # Draw the image onto the PDF canvas (A4 landscape size is roughly 842 x 595 points)
        c.drawImage(img_path, 0, 0, width=842, height=595)
        c.save()
        
        return img_path, pdf_path, f"✅ Success! Certificate generated and saved to: {SAVE_DIR}"
    
    except Exception as e:
        return None, None, f"❌ Error generating certificate: {str(e)}"

def reset_fields():
    return "", "", "", "", None, None, "Fields have been reset."

# Gradio UI Custom CSS for Professional Look
css = """
.container { max-width: 900px; margin: auto; }
h1 { text-align: center; color: #4B0082; font-family: 'Arial', sans-serif; }
.generate-btn { background-color: #4B0082 !important; color: white !important; font-weight: bold !important; font-size: 16px !important; }
.reset-btn { background-color: #D4AF37 !important; color: white !important; font-weight: bold !important; font-size: 16px !important; }
"""

# Build Gradio UI
with gr.Blocks(css=css, theme=gr.themes.Default(primary_hue="purple", secondary_hue="yellow")) as demo:
    gr.Markdown("# 🎓 Cloud Certificate Generator")
    gr.Markdown("<p style='text-align: center; font-size: 16px; color: #555;'>Generate professional digital certificates automatically and store them securely in the cloud (Google Drive).</p>")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 📝 Enter Details")
            student_name = gr.Textbox(label="Student Name", placeholder="e.g. John Doe")
            event_name = gr.Textbox(label="Event Name", placeholder="e.g. Cloud Computing Workshop")
            organizer_name = gr.Textbox(label="Organizer Name", placeholder="e.g. Tech Club")
            event_date = gr.Textbox(label="Event Date", placeholder="e.g. October 15, 2026")
            
            with gr.Row():
                generate_btn = gr.Button("✨ Generate Certificate", elem_classes="generate-btn")
                reset_btn = gr.Button("🔄 Reset", elem_classes="reset-btn")
            
            status_message = gr.Textbox(label="Status", interactive=False)
            
        with gr.Column(scale=1):
            gr.Markdown("### 👁️ Preview & Download")
            preview_image = gr.Image(label="Certificate Preview", type="filepath")
            download_pdf = gr.File(label="Download PDF Certificate")
            
    # Connect buttons to functions
    generate_btn.click(
        fn=generate_certificate,
        inputs=[student_name, event_name, organizer_name, event_date],
        outputs=[preview_image, download_pdf, status_message]
    )
    
    reset_btn.click(
        fn=reset_fields,
        inputs=[],
        outputs=[student_name, event_name, organizer_name, event_date, preview_image, download_pdf, status_message]
    )

if __name__ == "__main__":
    print(f"Running Certificate Generator... Images will be saved to: {SAVE_DIR}")
    demo.launch(share=True) # Share=True creates a public link (Useful for Colab)
