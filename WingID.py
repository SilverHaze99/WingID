import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sqlite3
import os
from PIL import Image, ImageTk
import logging
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LanguageManager:
    def __init__(self):
        self.current_language = 'en'
        self.translations = {
            'en': {
                'title': 'Military Aircraft OSINT Reference Tool',
                'search_frame': 'Aircraft Search',
                'search_label': 'Search:',
                'clear_button': 'Clear',
                'details_frame': 'Aircraft Details',
                'images_frame': 'Aircraft Silhouettes',
                'side_view': 'Side view: No image available',
                'top_view': 'Top view: No image available',
                'no_info': '❌ No information found for aircraft:',
                'db_error': 'Database Error',
                'db_init_failed': 'Failed to initialize database:',
                'app_error': 'Application Error',
                'app_start_failed': 'Failed to start application:',
                'empty_db': 'Empty database detected. Creating sample data...',
                'language_menu': 'Language',
                'theme_menu': 'Theme',
                'light_theme': 'Light',
                'dark_theme': 'Dark',
                'aircraft_info': {
                    'basic_info': '✈️  BASIC INFORMATION:',
                    'platform_base': '    • Platform Base:',
                    'first_flight': '    • First Flight:',
                    'current_status': '    • Current Status:',
                    'operational_role': '🎯  OPERATIONAL ROLE:',
                    'operators': '👥  OPERATORS:',
                    'availability': '📊  AVAILABILITY & RARITY:',
                    'classification': '    • Classification:',
                    'quantity': '    • Quantity in Service:',
                    'detailed_desc': '📋  DETAILED DESCRIPTION:',
                    'last_updated': 'Last updated: Military Aircraft OSINT Database'
                }
            },
            'de': {
                'title': 'Militärflugzeug OSINT Referenz-Tool',
                'search_frame': 'Flugzeug Suche',
                'search_label': 'Suchen:',
                'clear_button': 'Löschen',
                'details_frame': 'Flugzeug Details',
                'images_frame': 'Flugzeug Silhouetten',
                'side_view': 'Seitenansicht: Kein Bild verfügbar',
                'top_view': 'Draufsicht: Kein Bild verfügbar',
                'no_info': '❌ Keine Informationen gefunden für Flugzeug:',
                'db_error': 'Datenbank Fehler',
                'db_init_failed': 'Datenbank Initialisierung fehlgeschlagen:',
                'app_error': 'Anwendungsfehler',
                'app_start_failed': 'Anwendungsstart fehlgeschlagen:',
                'empty_db': 'Leere Datenbank erkannt. Erstelle Beispieldaten...',
                'language_menu': 'Sprache',
                'theme_menu': 'Design',
                'light_theme': 'Hell',
                'dark_theme': 'Dunkel',
                'aircraft_info': {
                    'basic_info': '✈️  GRUNDINFORMATIONEN:',
                    'platform_base': '    • Plattform Basis:',
                    'first_flight': '    • Erstflug:',
                    'current_status': '    • Aktueller Status:',
                    'operational_role': '🎯  OPERATIONELLE ROLLE:',
                    'operators': '👥  BETREIBER:',
                    'availability': '📊  VERFÜGBARKEIT & SELTENHEIT:',
                    'classification': '    • Klassifizierung:',
                    'quantity': '    • Anzahl im Dienst:',
                    'detailed_desc': '📋  DETAILLIERTE BESCHREIBUNG:',
                    'last_updated': 'Zuletzt aktualisiert: Militärflugzeug OSINT Datenbank'
                }
            }
        }
    
    def get_text(self, key):
        """Get translated text for current language"""
        keys = key.split('.')
        text = self.translations[self.current_language]
        for k in keys:
            text = text.get(k, key)
        return text
    
    def set_language(self, lang):
        """Set current language"""
        if lang in self.translations:
            self.current_language = lang


class ThemeManager:
    def __init__(self):
        self.current_theme = 'light'
        self.themes = {
            'light': {
                'bg': '#ffffff',
                'fg': '#000000',
                'select_bg': '#0078d4',
                'select_fg': '#ffffff',
                'entry_bg': '#ffffff',
                'entry_fg': '#000000',
                'text_bg': '#f8f8f8',
                'text_fg': '#000000',
                'frame_bg': '#f0f0f0',
                'button_bg': '#e1e1e1',
                'listbox_bg': '#ffffff',
                'listbox_fg': '#000000'
            },
            'dark': {
                'bg': '#2d2d2d',
                'fg': '#ffffff',
                'select_bg': '#404040',
                'select_fg': '#ffffff',
                'entry_bg': '#404040',
                'entry_fg': '#ffffff',
                'text_bg': '#353535',
                'text_fg': '#ffffff',
                'frame_bg': '#2d2d2d',
                'button_bg': '#404040',
                'listbox_bg': '#353535',
                'listbox_fg': '#ffffff'
            }
        }
    
    def get_colors(self):
        """Get current theme colors"""
        return self.themes[self.current_theme]
    
    def set_theme(self, theme):
        """Set current theme"""
        if theme in self.themes:
            self.current_theme = theme


class AircraftDatabase:
    def __init__(self, language='en'):
        self.language = language
        self.db_file = "airplane_de.db" if language == 'de' else "airplane.db"
        self.conn = None
        self.cursor = None
        self.connect()
        self.initialize_database()

    def connect(self):
        """Establish database connection with error handling"""
        try:
            self.conn = sqlite3.connect(self.db_file)
            self.cursor = self.conn.cursor()
            logger.info(f"Connected to database: {self.db_file}")
        except sqlite3.Error as e:
            logger.error(f"Database connection failed: {e}")
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Safely close database connection"""
        if self.conn:
            try:
                self.conn.close()
                logger.info("Database connection closed")
            except sqlite3.Error as e:
                logger.error(f"Error closing database: {e}")

    def initialize_database(self):
        """Initialize database and add missing fields"""
        try:
            # Create table if it doesn't exist
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS aircraft (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    base TEXT,
                    role TEXT,
                    rarity TEXT,
                    quantity TEXT,
                    operator TEXT,
                    details TEXT,
                    first_flight TEXT,
                    status TEXT
                )
            """)
            self.conn.commit()

            # Add image path columns if they don't exist
            self._add_column_if_not_exists("side_view_path", "TEXT")
            self._add_column_if_not_exists("top_view_path", "TEXT")

            # Check if database is empty and populate with sample data
            self.cursor.execute("SELECT COUNT(*) FROM aircraft")
            if self.cursor.fetchone()[0] == 0:
                logger.info("Empty database detected. Creating sample data...")
                self.create_example_database()

        except sqlite3.Error as e:
            logger.error(f"Database initialization failed: {e}")
            raise

    def _add_column_if_not_exists(self, column_name, column_type):
        """Helper method to safely add columns"""
        try:
            self.cursor.execute(f"ALTER TABLE aircraft ADD COLUMN {column_name} {column_type}")
            self.conn.commit()
            logger.info(f"Added column: {column_name}")
        except sqlite3.OperationalError:
            # Column already exists
            pass

    def create_example_database(self):
        """Create sample database with military aircraft data"""
        if self.language == 'de':
            example_data = [
                ("E-6 Mercury", "Boeing 707-320B", "Strategische Kommunikation und Nuklearkommando (TACAMO)", 
                 "sehr selten", "16 Einheiten", "US Navy", 
                 "Ersetzt die EC-130Q. Dient als fliegendes Kommandozentrum für Nuklearstreitkräfte. Kann 15+ Stunden in der Luft bleiben.", 
                 "1987", "Aktiv", None, None),
                
                ("E-2 Hawkeye", "Grumman Eigenentwicklung", "Trägergestützte Luftraumüberwachung (AEW&C)", 
                 "häufig", "~75 Einheiten (Aktiv)", "US Navy, verschiedene Verbündete", 
                 "Markante rotierende Radarkuppel. Hauptaufgabe ist Luftraumüberwachung von Flugzeugträgern.", 
                 "1960", "Aktiv", None, None),
                 
                ("E-3 Sentry", "Boeing 707-320B", "Luftgestützte Frühwarnung und Kontrolle (AWACS)", 
                 "selten", "~30 Einheiten (USAF)", "USAF, NATO, Saudi-Arabien, andere", 
                 "Große rotierende Radarkuppel oben. Koordiniert Luftoperationen über weite Gebiete.", 
                 "1972", "Aktiv", None, None),
                 
                ("E-4B Nightwatch", "Boeing 747-200B", "Luftgestütztes Kommandozentrum (NAOC)", 
                 "extrem selten", "4 Einheiten", "USAF", 
                 "Doomsday Plane - Fliegendes Pentagon für Krisensituationen. Kann wochenlang in der Luft bleiben.", 
                 "1973", "Aktiv", None, None),
                 
                ("KC-135 Stratotanker", "Boeing 707-80 (Prototyp)", "Luft-zu-Luft Betankung", 
                 "häufig", "~400 Einheiten", "USAF, verschiedene Luftstreitkräfte weltweit", 
                 "Rückgrat strategischer Luftbetankungsoperationen. Ermöglicht globale Reichweite für Kampfflugzeuge.", 
                 "1956", "Aktiv", None, None),
                 
                ("P-8 Poseidon", "Boeing 737-800ERX", "Maritime Aufklärung und U-Boot-Jagd", 
                 "häufig", "140+ Einheiten (alle Betreiber)", "US Navy, Royal Navy, verschiedene Verbündete", 
                 "Ersetzt P-3 Orion. Moderne Avionik für maritime Überwachung und U-Boot-Abwehr.", 
                 "2009", "Aktiv", None, None),
                 
                ("C-130 Hercules", "Lockheed Originaldesign", "Taktischer Transport", 
                 "sehr häufig", "2000+ Einheiten", "USAF und 70+ Länder", 
                 "Arbeitspferd des taktischen Transports. Extrem vielseitig mit zahlreichen Varianten für verschiedene Missionen.", 
                 "1954", "Aktiv", None, None),
                 
                ("B-52 Stratofortress", "Boeing Originaldesign", "Strategischer Bomber", 
                 "selten", "76 Einheiten", "USAF", 
                 "Strategischer Langstreckenbomber. Im Dienst seit 1955, geplant bis in die 2050er Jahre.", 
                 "1952", "Aktiv", None, None)
            ]
        else:
            example_data = [
                ("E-6 Mercury", "Boeing 707-320B", "Strategic Communications and Nuclear Command (TACAMO)", 
                 "very rare", "16 units", "US Navy", 
                 "Replaces the EC-130Q. Serves as a flying command center for nuclear forces. Can remain airborne for 15+ hours.", 
                 "1987", "Active", None, None),
                
                ("E-2 Hawkeye", "Grumman in-house development", "Carrier-based airspace surveillance (AEW&C)", 
                 "common", "~75 units (Active)", "US Navy, various allies", 
                 "Distinctive rotating radar dome. Primary mission is airspace surveillance from aircraft carriers.", 
                 "1960", "Active", None, None),
                 
                ("E-3 Sentry", "Boeing 707-320B", "Airborne early warning and control (AWACS)", 
                 "rare", "~30 units (USAF)", "USAF, NATO, Saudi Arabia, others", 
                 "Large rotating radar dome on top. Coordinates air operations over vast areas.", 
                 "1972", "Active", None, None),
                 
                ("E-4B Nightwatch", "Boeing 747-200B", "Airborne command center (NAOC)", 
                 "extremely rare", "4 units", "USAF", 
                 "Doomsday Plane - Flying Pentagon for crisis situations. Can remain airborne for weeks.", 
                 "1973", "Active", None, None),
                 
                ("KC-135 Stratotanker", "Boeing 707-80 (Prototype)", "Air-to-air refueling", 
                 "common", "~400 units", "USAF, various air forces worldwide", 
                 "Backbone of strategic air refueling operations. Enables global reach for combat aircraft.", 
                 "1956", "Active", None, None),
                 
                ("P-8 Poseidon", "Boeing 737-800ERX", "Maritime reconnaissance and submarine hunting", 
                 "common", "140+ units (all operators)", "US Navy, Royal Navy, various allies", 
                 "Replaces P-3 Orion. Modern avionics for maritime surveillance and anti-submarine warfare.", 
                 "2009", "Active", None, None),
                 
                ("C-130 Hercules", "Lockheed original design", "Tactical transport", 
                 "very common", "2000+ units", "USAF and 70+ countries", 
                 "Workhorse tactical transport. Extremely versatile with numerous variants for different missions.", 
                 "1954", "Active", None, None),
                 
                ("B-52 Stratofortress", "Boeing original design", "Strategic bomber", 
                 "rare", "76 units", "USAF", 
                 "Long-range strategic bomber. In service since 1955, planned to serve until 2050s.", 
                 "1952", "Active", None, None)
            ]

        try:
            self.cursor.executemany("""
                INSERT INTO aircraft (name, base, role, rarity, quantity, operator, details, first_flight, status, side_view_path, top_view_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, example_data)
            self.conn.commit()
            logger.info(f"Created sample database with {len(example_data)} aircraft")
        except sqlite3.Error as e:
            logger.error(f"Failed to create sample data: {e}")
            raise

    def search_aircraft(self, query):
        """Search for aircraft based on input query"""
        try:
            if not query.strip():
                self.cursor.execute("SELECT name FROM aircraft ORDER BY name")
            else:
                query_pattern = f"%{query.lower()}%"
                self.cursor.execute("""
                    SELECT name FROM aircraft 
                    WHERE LOWER(name) LIKE ? OR LOWER(role) LIKE ? OR LOWER(operator) LIKE ?
                    ORDER BY name
                """, (query_pattern, query_pattern, query_pattern))
            
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            logger.error(f"Search failed: {e}")
            return []

    def get_aircraft_info(self, name):
        """Retrieve comprehensive information about an aircraft"""
        try:
            self.cursor.execute("SELECT * FROM aircraft WHERE name = ?", (name,))
            result = self.cursor.fetchone()
            
            if result:
                info = {
                    "base": result[2] or "Unknown",
                    "role": result[3] or "Unknown",
                    "rarity": result[4] or "Unknown",
                    "quantity": result[5] or "Unknown",
                    "operator": result[6] or "Unknown",
                    "details": result[7] or "No details available",
                    "first_flight": result[8] or "Unknown",
                    "status": result[9] or "Unknown",
                    "side_view_path": result[10] if len(result) > 10 else None,
                    "top_view_path": result[11] if len(result) > 11 else None
                }
                return info
            return None
        except sqlite3.Error as e:
            logger.error(f"Failed to retrieve aircraft info: {e}")
            return None

    def __del__(self):
        """Cleanup method"""
        self.close()


class AircraftLookupGUI:
    def __init__(self, root):
        self.root = root
        self.lang_manager = LanguageManager()
        self.theme_manager = ThemeManager()
        
        # Load settings
        self.load_settings()
        
        self.root.title(self.lang_manager.get_text('title'))
        self.root.geometry("1000x750")
        self.root.minsize(800, 600)
        
        # Initialize database with error handling
        try:
            self.db = AircraftDatabase(self.lang_manager.current_language)
        except Exception as e:
            messagebox.showerror(self.lang_manager.get_text('db_error'), 
                               f"{self.lang_manager.get_text('db_init_failed')} {e}")
            self.root.destroy()
            return
        
        # Initialize image references
        self.side_photo = None
        self.top_photo = None
        
        # Create menu
        self.create_menu()
        
        # Create GUI
        self.create_widgets()
        
        # Apply theme
        self.apply_theme()
        
        # Event bindings
        self.search_var.trace('w', self.on_search_change)
        
        # Bind cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_settings(self):
        """Load application settings"""
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    settings = json.load(f)
                    self.lang_manager.set_language(settings.get('language', 'en'))
                    self.theme_manager.set_theme(settings.get('theme', 'light'))
        except Exception as e:
            logger.warning(f"Could not load settings: {e}")

    def save_settings(self):
        """Save application settings"""
        try:
            settings = {
                'language': self.lang_manager.current_language,
                'theme': self.theme_manager.current_theme
            }
            with open('settings.json', 'w') as f:
                json.dump(settings, f)
        except Exception as e:
            logger.warning(f"Could not save settings: {e}")

    def create_menu(self):
        """Create application menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Language menu
        language_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang_manager.get_text('language_menu'), menu=language_menu)
        language_menu.add_command(label="English", command=lambda: self.change_language('en'))
        language_menu.add_command(label="Deutsch", command=lambda: self.change_language('de'))
        
        # Theme menu
        theme_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label=self.lang_manager.get_text('theme_menu'), menu=theme_menu)
        theme_menu.add_command(label=self.lang_manager.get_text('light_theme'), command=lambda: self.change_theme('light'))
        theme_menu.add_command(label=self.lang_manager.get_text('dark_theme'), command=lambda: self.change_theme('dark'))

    def change_language(self, lang):
        """Change application language"""
        if lang != self.lang_manager.current_language:
            self.lang_manager.set_language(lang)
            self.save_settings()
            
            # Reinitialize database with new language
            self.db.close()
            self.db = AircraftDatabase(lang)
            
            # Update GUI text
            self.update_gui_text()
            
            # Refresh search results
            self.update_suggestions(self.db.search_aircraft(""))

    def change_theme(self, theme):
        """Change application theme"""
        if theme != self.theme_manager.current_theme:
            self.theme_manager.set_theme(theme)
            self.save_settings()
            self.apply_theme()

    def apply_theme(self):
        """Apply current theme to all widgets"""
        colors = self.theme_manager.get_colors()
        
        # Configure root
        self.root.configure(bg=colors['bg'])
        
        # Configure style for ttk widgets
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure ttk styles
        style.configure('TFrame', background=colors['bg'])
        style.configure('TLabelFrame', background=colors['bg'], foreground=colors['fg'])
        style.configure('TLabelFrame.Label', background=colors['bg'], foreground=colors['fg'])
        style.configure('TLabel', background=colors['bg'], foreground=colors['fg'])
        style.configure('TButton', background=colors['button_bg'], foreground=colors['fg'])
        style.configure('TEntry', background=colors['entry_bg'], foreground=colors['entry_fg'])
        
        # Configure tk widgets
        if hasattr(self, 'suggestions_listbox'):
            self.suggestions_listbox.configure(
                bg=colors['listbox_bg'], 
                fg=colors['listbox_fg'],
                selectbackground=colors['select_bg'],
                selectforeground=colors['select_fg']
            )
        
        if hasattr(self, 'details_text'):
            self.details_text.configure(
                bg=colors['text_bg'], 
                fg=colors['text_fg'],
                insertbackground=colors['fg']
            )

    def update_gui_text(self):
        """Update all GUI text elements"""
        self.root.title(self.lang_manager.get_text('title'))
        self.search_frame.configure(text=self.lang_manager.get_text('search_frame'))
        self.search_label.configure(text=self.lang_manager.get_text('search_label'))
        self.clear_button.configure(text=self.lang_manager.get_text('clear_button'))
        self.details_frame.configure(text=self.lang_manager.get_text('details_frame'))
        self.images_frame.configure(text=self.lang_manager.get_text('images_frame'))
        
        # Reset image labels
        self.side_view_label.configure(text=self.lang_manager.get_text('side_view'))
        self.top_view_label.configure(text=self.lang_manager.get_text('top_view'))
        
    def create_widgets(self):
        """Create the main GUI widgets"""
        # Main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Search section
        self.search_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.get_text('search_frame'), padding="10")
        self.search_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.search_label = ttk.Label(self.search_frame, text=self.lang_manager.get_text('search_label'))
        self.search_label.grid(row=0, column=0, sticky=tk.W)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.search_frame, textvariable=self.search_var, width=40)
        self.search_entry.grid(row=0, column=1, padx=(10, 0), sticky=(tk.W, tk.E))
        self.search_entry.focus()
        
        # Clear button
        self.clear_button = ttk.Button(self.search_frame, text=self.lang_manager.get_text('clear_button'), command=self.clear_search)
        self.clear_button.grid(row=0, column=2, padx=(5, 0))
        
        # Suggestions list with improved styling
        self.suggestions_frame = ttk.Frame(self.search_frame)
        self.suggestions_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.suggestions_listbox = tk.Listbox(self.suggestions_frame, height=8, font=('Consolas', 10))
        self.suggestions_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.suggestions_listbox.bind('<<ListboxSelect>>', self.on_suggestion_select)
        
        # Scrollbar for suggestions
        suggestions_scrollbar = ttk.Scrollbar(self.suggestions_frame, orient="vertical")
        suggestions_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.suggestions_listbox.config(yscrollcommand=suggestions_scrollbar.set)
        suggestions_scrollbar.config(command=self.suggestions_listbox.yview)
        
        # Details section
        self.details_frame = ttk.LabelFrame(main_frame, text=self.lang_manager.get_text('details_frame'), padding="10")
        self.details_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # Scrollable text area for details
        self.details_text = scrolledtext.ScrolledText(
            self.details_frame, 
            width=90, 
            height=18, 
            wrap=tk.WORD,
            font=('Consolas', 10)
        )
        self.details_text.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Image section
        self.images_frame = ttk.LabelFrame(self.details_frame, text=self.lang_manager.get_text('images_frame'), padding="10")
        self.images_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Side view
        self.side_view_label = ttk.Label(self.images_frame, text=self.lang_manager.get_text('side_view'), 
                                        relief="solid", padding="5")
        self.side_view_label.grid(row=0, column=0, padx=(0, 10), pady=5, sticky=(tk.W, tk.E))
        
        # Top view  
        self.top_view_label = ttk.Label(self.images_frame, text=self.lang_manager.get_text('top_view'), 
                                       relief="solid", padding="5")
        self.top_view_label.grid(row=0, column=1, padx=(10, 0), pady=5, sticky=(tk.W, tk.E))
        
        # Configure grid weights for responsive design
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        self.search_frame.columnconfigure(1, weight=1)
        self.suggestions_frame.columnconfigure(0, weight=1)
        self.details_frame.columnconfigure(0, weight=1)
        self.details_frame.rowconfigure(0, weight=1)
        self.images_frame.columnconfigure(0, weight=1)
        self.images_frame.columnconfigure(1, weight=1)
        
        # Load initial aircraft list
        self.update_suggestions(self.db.search_aircraft(""))
        
    def clear_search(self):
        """Clear the search field and show all aircraft"""
        self.search_var.set("")
        self.search_entry.focus()
        
    def on_search_change(self, *args):
        """Handle search text changes"""
        query = self.search_var.get()
        matches = self.db.search_aircraft(query)
        self.update_suggestions(matches)
        
    def update_suggestions(self, suggestions):
        """Update the suggestions listbox"""
        self.suggestions_listbox.delete(0, tk.END)
        for suggestion in suggestions:
            self.suggestions_listbox.insert(tk.END, suggestion)
        
        # Auto-select first item if there are suggestions
        if suggestions:
            self.suggestions_listbox.selection_set(0)
            
    def on_suggestion_select(self, event):
        """Handle suggestion selection"""
        selection = self.suggestions_listbox.curselection()
        if selection:
            aircraft_name = self.suggestions_listbox.get(selection[0])
            self.show_aircraft_details(aircraft_name)
            
    def load_and_resize_image(self, image_path, size=(250, 120)):
        """Load and resize image with error handling"""
        try:
            if image_path and os.path.exists(image_path):
                image = Image.open(image_path)
                image = image.resize(size, Image.Resampling.LANCZOS)
                return ImageTk.PhotoImage(image)
        except Exception as e:
            logger.warning(f"Failed to load image {image_path}: {e}")
        return None
            
    def show_aircraft_details(self, aircraft_name):
        """Display comprehensive aircraft details and images"""
        info = self.db.get_aircraft_info(aircraft_name)
        if info:
            self.details_text.delete(1.0, tk.END)
            
            # Get translated text elements
            t = self.lang_manager.get_text('aircraft_info')
            
            # Format detailed information
            details = f"""
═══════════════════════════════════════════════════════════════════════════════
                                {aircraft_name.upper()}
═══════════════════════════════════════════════════════════════════════════════

{t['basic_info']}
{t['platform_base']}      {info['base']}
{t['first_flight']}       {info['first_flight']}
{t['current_status']}     {info['status']}

{t['operational_role']}
    {info['role']}

{t['operators']}
    {info['operator']}

{t['availability']}
{t['classification']}     {info['rarity']}
{t['quantity']} {info['quantity']}

{t['detailed_desc']}
    {info['details']}

═══════════════════════════════════════════════════════════════════════════════
{t['last_updated']}
═══════════════════════════════════════════════════════════════════════════════
            """
            
            self.details_text.insert(1.0, details)
            
            # Load and display images
            self.load_aircraft_images(info)
            
        else:
            self.details_text.delete(1.0, tk.END)
            error_msg = f"{self.lang_manager.get_text('no_info')} {aircraft_name}"
            self.details_text.insert(1.0, error_msg)
            self.reset_image_displays()
    
    def load_aircraft_images(self, info):
        """Load aircraft silhouette images"""
        # Side view
        self.side_photo = self.load_and_resize_image(info['side_view_path'])
        if self.side_photo:
            self.side_view_label.config(image=self.side_photo, text="")
        else:
            self.side_view_label.config(image="", text=self.lang_manager.get_text('side_view'))
        
        # Top view
        self.top_photo = self.load_and_resize_image(info['top_view_path'])
        if self.top_photo:
            self.top_view_label.config(image=self.top_photo, text="")
        else:
            self.top_view_label.config(image="", text=self.lang_manager.get_text('top_view'))
    
    def reset_image_displays(self):
        """Reset image displays to default state"""
        self.side_view_label.config(image="", text=self.lang_manager.get_text('side_view'))
        self.top_view_label.config(image="", text=self.lang_manager.get_text('top_view'))
        self.side_photo = None
        self.top_photo = None
    
    def on_closing(self):
        """Handle application closing"""
        try:
            self.save_settings()
            self.db.close()
        except:
            pass
        self.root.destroy()


def main():
    """Main application entry point"""
    try:
        root = tk.Tk()
        app = AircraftLookupGUI(root)
        root.mainloop()
    except Exception as e:
        logger.error(f"Application failed to start: {e}")
        messagebox.showerror("Application Error", f"Failed to start application: {e}")


if __name__ == "__main__":
    main()