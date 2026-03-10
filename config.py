import os
from dotenv import load_dotenv

load_dotenv()

PEOPLE = [
    "Don L. Scott Jr.",
    "Carl Heastie",
    "Joanna McClinton",
    "Chris Welch",
    "Bobby Joe Champion",
    "Karen Camper",
    "Zellnor Myrie",
    "Jabari Brisport",
    "James Sanders Jr.",
    "Justin Jones",
    "Justin Pearson",
    "Hakeem Jeffries",
    "Lucy McBath",
    "Angela Alsobrooks",
    "Lisa Blunt Rochester",
    "Cory Booker",
    "Raphael Warnock",
    "Karen Bass",
    "Brandon Scott",
    "Brandon Johnson",
    "Andre Dickens",
    "Cherelle Parker",
    "Jim Clyburn",
    "Lateefah Simon",
    "John Horhn",
    "Barbara Lee",
    "Alyia Gaskins",
    "Bennie Thompson",
    "Robin Kelly",
    "Troy Carter",
    "Valerie Foushee",
    "Ayanna Pressley",
    "Shontel Brown",
    "Bonnie Watson Coleman",
    "Steven Horsford",
    "Joyce Beatty",
    "Yvette Clarke",
    "Summer Lee",
    "Gabe Amo",
]

ALIASES = {
    "Brandon Johnson": ["Brandon Johnson Chicago mayor"],
    "Brandon Scott": ["Brandon Scott Baltimore mayor"],
    "Karen Bass": ["Karen Bass Los Angeles mayor"],
    "Barbara Lee": ["Barbara Lee Oakland"],
    "Justin Jones": ["Justin Jones Tennessee representative"],
    "Justin Pearson": ["Justin Pearson Tennessee representative"],
    "Hakeem Jeffries": ["Hakeem Jeffries House Democrats"],
    "Raphael Warnock": ["Raphael Warnock senator Georgia"],
}

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
DIGEST_FROM_EMAIL = os.getenv("DIGEST_FROM_EMAIL", "")
DIGEST_TO_EMAIL = os.getenv("DIGEST_TO_EMAIL", "")        
DIGEST_TO_EMAILS = os.getenv("DIGEST_TO_EMAILS", "")       

DB_PATH = os.getenv("DB_PATH", "watch.db")
LOOKBACK_HOURS = int(os.getenv("LOOKBACK_HOURS", "24"))
MAX_YOUTUBE_RESULTS_PER_PERSON = int(os.getenv("MAX_YOUTUBE_RESULTS_PER_PERSON", "8"))
MAX_NEWS_RESULTS_PER_PERSON = int(os.getenv("MAX_NEWS_RESULTS_PER_PERSON", "5"))
