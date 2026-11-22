# 📊 ICMLDE 2026 Presentation & Technical Defense Package
**5th Elsevier International Conference on Machine Learning and Data Engineering (ICMLDE 5.0)**  
*27th–28th November 2026 · UPES University, Dehradun, India · Procedia Computer Science*

- **Paper ID:** `857`
- **Accepted Title:** *C-XAI: Benchmarking Explanation Stability, Cross-Explainer Discordance, and Clinical Utility in Healthcare AI*
- **Authors:** Sheela Akshar Sakhi¹ (*Presenter*), Ibbraheem Shaik¹, Settibattini Suhitha¹, Ramya G R²* (*Corresponding Author: `gr_ramya@cb.amrita.edu`*)
- **Affiliation:** Department of Computer Science and Engineering, Amrita School of Computing, Coimbatore, Amrita Vishwa Vidyapeetham, India

---

## 📁 Directory Structure

```
CONF_PRESENTATION/
├── SUBMISSION_READY/              # Final deliverables formatted for conference submission
│   ├── ICMLDE-2026-857.pptx       # Official 12-slide presentation (PPTX format for Google Form)
│   ├── ICMLDE-2026-857.pdf        # Official 12-slide presentation (PDF format)
│   ├── ICMLDE-2026-857_C-XAI_Digital_Poster.pptx # Official 48x24" digital conference poster (PPTX)
│   ├── ICMLDE-2026-857_C-XAI_Digital_Poster.pdf  # Official 48x24" digital conference poster (PDF)
│   ├── ICMLDE-2026-857_Technical_Backup_Presentation.pdf   # 16-slide LaTeX Beamer defense deck
│   ├── ICMLDE-2026-857_Technical_Backup_Documentation.docx # 10-page Elsevier technical defense doc
│   └── ICMLDE-2026-857_Technical_Backup_Documentation.pdf  # 10-page technical defense doc (PDF)
│
├── technical_backup/              # Editable defense sources
│   ├── latex_beamer/              # LaTeX Beamer presentation source (.tex) and output (.pdf)
│   │   ├── C-XAI_Technical_Backup_Presentation.tex
│   │   └── C-XAI_Technical_Backup_Presentation.pdf
│   └── word_documentation/        # Technical defense reference doc (.docx and .pdf)
│       ├── C-XAI_Technical_Backup_Documentation.docx
│       └── C-XAI_Technical_Backup_Documentation.pdf
│
├── scripts/                       # Python automation and build pipelines
│   ├── build_presentation.py      # Generates main 12-slide PPTX and enforces margins
│   ├── build_digital_poster.py    # Generates official 48x24" digital poster PPTX
│   ├── generate_backup_docx.py    # Generates 10-page Word defense document
│   ├── build_technical_backup_presentation.py # Legacy PPTX backup generator
│   ├── fig_discordance_comparison.png         # Vector figure asset for Slide 8 & Poster
│   └── qr_code.png                            # High-res project repository QR code
│
├── templates/                     # Conference templates and backups
│   ├── ICMLDE_2026_Paper_Presentation_Template.pptx          # Populated presentation template
│   ├── ICMLDE_2026_Paper_Presentation_Template_ORIGINAL_BACKUP.pptx # Master template
│   ├── ICMLDE2026_poster_3.pptx                              # Master poster template (48x24 in)
│   └── legacy_pptx_backup.pptx                               # Archived PPTX backup
│
└── previews/                      # High-resolution slide and poster preview renders
    ├── main_presentation/         # Slides 01–12 PNGs
    ├── technical_backup/          # Slides 01–16 PNGs
    └── poster/                    # 7200x3600 Ultra-HD Digital Poster PNG render
```

---

## 🚀 Conference Submission Checklist

### 1. Technical Paper Presentation (Slides)
- **Deadline**: 23/11/2026
- **Google Form**: [Presentation Submission Form](https://docs.google.com/forms/d/e/1FAIpQLSfh2Mu6QyPmb0OVUZB1cHPbCupX9nxbJljttQs_qXmga39SMg/viewform?usp=header)
- **Files to Upload**:
  - `SUBMISSION_READY/ICMLDE-2026-857.pptx`
  - `SUBMISSION_READY/ICMLDE-2026-857.pdf`

### 2. Digital & Physical Conference Poster
- **Deadline**: 23/11/2026
- **Google Form**: [Poster Submission Form](https://docs.google.com/forms/d/e/1FAIpQLSc6Zh2bHTd3tO1tlmq2SvfL5McZpQ_qtc6Z0z0pD8wTZO6A2g/viewform?usp=publish-editor)
- **Format Specs**: Landscape, 48 × 24 in (2:1 aspect ratio, prints at 200% to 96 × 48 in)
- **Typography Specs**: Body text $\ge 24\text{ pt}$ (48 pt when printed), Section headers 32 pt bold
- **Files to Upload**:
  - Required: `SUBMISSION_READY/ICMLDE-2026-857_C-XAI_Digital_Poster.pdf`
  - Recommended: `SUBMISSION_READY/ICMLDE-2026-857_C-XAI_Digital_Poster.pptx`
