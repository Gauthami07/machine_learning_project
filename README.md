# Features
1. Personality Prediction: Uses logistic regression to predict personality types based on Big Five traits
2. Resume Parsing: Extracts information from PDF and DOCX resume files
3. Skill Detection: Identifies technical skills from resume content
4. Entity Recognition: Extracts email, phone numbers, and other entities using spaCy NLP
5. GUI Interface: User-friendly Tkinter-based graphical interface
6. Multi-format Support: Handles both PDF and Word document formats

# Prerequisites
Required Python Version :
Python 3.7 or higher

# Dependencies
Install the required packages using pip:
pip install pandas numpy scikit-learn spacy PyPDF2 python-docx
# spaCy Model
Download the English language model for spaCy:
python -m spacy download en_core_web_sm

# Technical features
pandas: Data manipulation and analysis
numpy: Numerical computing
scikit-learn: Machine learning algorithms
spacy: Natural language processing
PyPDF2: PDF file processing
python-docx: Word document processing
tkinter: GUI framework (included with Python)

# Future Enhancements
-Include recruiter dashboard
-Advanced NLP for better resume parsing
-Integration with job matching algorithms
-Database storage for candidate profiles
-Web-based interface
-Batch processing capabilities
-Advanced visualization of results
