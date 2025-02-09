
#newsPod: Daily News Summarizer with Audio

newsPod is a Django-based web application that fetches important news from NewsAPI, summarizes each news article using a Hugging Face Transformers model, and generates a single combined audio file for all the day's news summaries. Users can filter news by category and save articles for later reference.

Features

- News Fetching: Retrieves the latest important news articles via the [NewsAPI](https://newsapi.org/).
- Summarization: Uses the `facebook/bart-large-cnn` model from Hugging Face Transformers to generate concise summaries of each news article.
- Combined Audio Generation: Creates one audio file that combines all the summaries so users can listen to the day's news.
- Category Filtering: By default, displays all news; users can select a specific category (e.g., business, entertainment, health, science, sports, technology) to filter the news.
- Saved News: Allows users to save articles for future reference.

 Demo

If you have a live demo, add the link here. For example:  
[Live Demo](http://your-demo-url.com)

Installation

 1. Clone the Repository

```bash
git clone https://github.com/epsarika/newsPod.git
cd newsPod

2. Create and Activate a Virtual Environment
On Linux/macOS:
python3 -m venv venv
source venv/bin/activate

On Windows:
python -m venv venv
venv\Scripts\activate

3. Install Dependencies
Install the required packages:
pip install -r requirements.txt

Ensure that requirements.txt includes at least:
Django
requests
transformers
gTTS
4. Configure Your NewsAPI Key
In news/views.py, replace the placeholder API key with your actual NewsAPI key:
API_KEY = "3e88d285a5594a4996b16b7e8541be79"

5. Run Migrations and Start the Server
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

Open your browser and navigate to http://127.0.0.1:8000/ to view the app.
Usage
Homepage: Displays summarized news articles along with one combined audio file for all summaries.
Category Selection: Use the dropdown menu to filter news by category (default is "general" for all news).
Audio Playback: Click the audio player to listen to the combined summaries.
Save News: Save individual articles for later reference by clicking the "Save News" button (if implemented).
Project Structure
newsPod/
├── manage.py
├── newsPod/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── news/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── templates/
│   │   └── news/
│   │       ├── home.html
│   │       └── saved_news.html
│   ├── tests.py
│   └── views.py
├── media/              # Audio files are saved here.
└── requirements.txt

Customization
Summarization Model: You can change the summarization model by modifying the pipeline initialization in views.py.
Audio Generation: The app currently uses gTTS. To switch providers or modify settings, update the generate_combined_audio function in views.py.
Styling: Customize the templates and CSS to fit your design needs. Tailwind CSS or custom CSS can be used.
Reference
-Django  
  Official website: [https://www.djangoproject.com/](https://www.djangoproject.com/)   Django is the high-level Python web framework used to build the backend of this application.
- NewsAPI  
 Documentation: [https://newsapi.org/](https://newsapi.org/)  
 Provides access to up-to-date news articles from various sources, which are fetched and processed by the application.
- Hugging Face Transformers
Documentation: [https://huggingface.co/transformers/](https://huggingface.co/transformers/)  
Utilized for the text summarization feature with the `facebook/bart-large-cnn` model to generate concise summaries of news articles.

- gTTS (Google Text-to-Speech)
 PyPI page: [https://pypi.org/project/gTTS/](https://pypi.org/project/gTTS/)  
 Used to convert the combined news summaries into a single audio file.

- Tailwind CSS  
Official website: [https://tailwindcss.com/](https://tailwindcss.com/)  
 (Optional) Used in the frontend for rapid and responsive UI development when using the Tailwind version of the templates.
- Additional Resources 
 - [Python Official Documentation](https://docs.python.org/3/)  
 - [GitHub](https://github.com/) for hosting and version control of the project.
OpenAI  - https://platform.openai.com/
DeepSeek - https://www.deepseek.com/
Claude - https://claude.ai/
Bolt - https://bolt.new/
License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments
NewsAPI for providing up-to-date news data.
Hugging Face Transformers for the summarization model.
gTTS for text-to-speech conversion.




