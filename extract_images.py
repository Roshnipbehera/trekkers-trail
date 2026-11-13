import fitz
import os

pdf_path = r"C:\Users\HP\.gemini\antigravity\brain\18f3bdc5-3536-4c61-9e30-e681cc707e17\.user_uploaded\media_1793949964728_1e8e5c3e.pdf"
out_dir = r"C:\Users\HP\.gemini\antigravity\scratch\activity-2\extracted_images"
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print(f"Total pages in PDF: {len(doc)}")

img_count = 0
for pno in range(len(doc)):
    page = doc[pno]
    images = page.get_images(full=True)
    for idx, img in enumerate(images):
        xref = img[0]
        base = doc.extract_image(xref)
        ext = base["ext"]
        img_data = base["image"]
        w, h = base["width"], base["height"]
        filename = f"p{pno+1}_img{idx+1}_{w}x{h}.{ext}"
        filepath = os.path.join(out_dir, filename)
        with open(filepath, "wb") as f:
            f.write(img_data)
        img_count += 1
        print(f"Page {pno+1}: Saved {filename}")

print(f"\nExtracted {img_count} images successfully!")

