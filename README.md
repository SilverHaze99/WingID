# WingID - Military Aircraft OSINT Reference Tool

A comprehensive desktop application for military aircraft identification and intelligence gathering, designed for OSINT (Open Source Intelligence) researchers and aviation enthusiasts.

##  Overview

This tool provides a searchable database of military aircraft with detailed specifications, operational information, and visual identification aids. Perfect for aircraft spotters, defense analysts, and anyone interested in military aviation.

## Features

- **Smart Search**: Search by aircraft name, role, or operator
- **Comprehensive Database**: Detailed information including:
  - Platform specifications and base aircraft
  - Operational roles and capabilities
  - Current operators and deployment status
  - Rarity classification and quantity in service
  - First flight dates and current status
- **Visual Identification**: Support for aircraft silhouette images (side and top views)
- **Professional Layout**: Clean, organized interface optimized for reference work
- **Persistent Storage**: SQLite database for reliable data management

##  Quick Start

### Installation

1.  **Clone the repository** (if you are using Git):
    ```bash
    git clone https://github.com/SilverHaze99/WingID
    cd WingID
    ```
2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```
3.  **Activate the virtual environment:**
    * **On Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **On macOS and Linux:**
        ```bash
        source venv/bin/activate
        ```
4.  **Install Required Python Libraries:** Install the necessary libraries using pip within the activated virtual environment:
    ```bash
    pip install Pillow 
    ```
5.  **Download the `airplane.db` file:** This file contains the already a lot of aircrafts. Ensure it is in the same directory as the Python script.

6.  Launch the Script:
   ```bash
    python WingID.py
   ```

### First Launch

The application will automatically:
- Create a new SQLite database (`airplane.db`) if you haven't already done so.
- Populate it with sample military aircraft data
- Launch the GUI interface

## Usage Guide

### Basic Search
1. **Launch the application**
2. **Type in the search box** - search by aircraft name, role, or operator
3. **Select from suggestions** - click on any aircraft in the list
4. **View details** - comprehensive information appears in the details panel

### Advanced Features
- **Clear Search**: Use the "Clear" button to reset search and show all aircraft
- **Auto-Complete**: The search provides real-time suggestions as you type
- **Multi-Field Search**: Search across aircraft names, roles, and operators simultaneously

##  Database Structure

The application uses SQLite with the following schema:

```sql
CREATE TABLE aircraft (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE,
    base TEXT,                 -- Base platform/manufacturer
    role TEXT,                 -- Operational role
    rarity TEXT,              -- Rarity classification
    quantity TEXT,            -- Number in service
    operator TEXT,            -- Operating forces/countries
    details TEXT,             -- Detailed description
    first_flight TEXT,        -- First flight date
    status TEXT,              -- Current operational status
    side_view_path TEXT,      -- Path to side view image
    top_view_path TEXT        -- Path to top-down view image
);
```

## Adding Aircraft Images

To add visual identification aids:

1. **Prepare images** in common formats (PNG, JPG, etc.)
2. **Update database** with image paths:
   ```sql
   UPDATE aircraft 
   SET side_view_path = 'path/to/side_view.png',
       top_view_path = 'path/to/top_view.png'
   WHERE name = 'Aircraft Name';
   ```
3. **Recommended image size**: 250x120 pixels for optimal display

## Sample Data

The application includes sample data for common military aircraft:

- **E-6 Mercury** - Strategic Communications (TACAMO)
- **E-2 Hawkeye** - Carrier-based AEW&C
- **E-3 Sentry** - AWACS
- **E-4B Nightwatch** - Airborne Command Center
- **KC-135 Stratotanker** - Air-to-Air Refueling
- **P-8 Poseidon** - Maritime Reconnaissance
- **C-130 Hercules** - Tactical Transport
- **B-52 Stratofortress** - Strategic Bomber

## Technical Details

### System Requirements
- **OS**: Windows, macOS, Linux
- **Python**: 3.7+
- **RAM**: 256MB minimum
- **Storage**: 50MB+ for application and database

### Dependencies
- `tkinter` - GUI framework (usually included with Python)
- `PIL/Pillow` - Image processing
- `sqlite3` - Database engine (included with Python)

### Architecture
- **Database Layer**: `AircraftDatabase` class handles all data operations
- **GUI Layer**: `AircraftLookupGUI` class manages the user interface
- **Error Handling**: Comprehensive logging and graceful error recovery
- **Resource Management**: Proper cleanup and connection handling

## Customization

### Adding New Aircraft
```python
# Example: Adding a new aircraft entry
new_aircraft = (
    "Aircraft Name",
    "Base Platform", 
    "Operational Role",
    "rarity_level",
    "quantity_info",
    "operators", 
    "detailed_description",
    "first_flight_year",
    "current_status",
    "path/to/side_image.png",
    "path/to/top_image.png"
)

db.cursor.execute("""
    INSERT INTO aircraft (name, base, role, rarity, quantity, operator, details, first_flight, status, side_view_path, top_view_path)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", new_aircraft)
```

### Rarity Classifications
- `extremely rare` - Unique or very limited aircraft (< 5 units)
- `very rare` - Limited production (5-20 units)
- `rare` - Small production run (20-100 units)
- `common` - Standard production (100+ units)
- `very common` - Mass production (1000+ units)

## Troubleshooting

### Common Issues

**Database won't create:**
- Check file permissions in the application directory
- Ensure SQLite3 is properly installed

**Images not displaying:**
- Verify image file paths are correct
- Check image file formats are supported (PNG, JPG, GIF, BMP)
- Ensure Pillow library is installed

**Search not working:**
- Check database connectivity
- Verify sample data was created successfully

### Debug Mode
Enable detailed logging by modifying the logging level:
```python
logging.basicConfig(level=logging.DEBUG)
```

## Contributing

This tool is designed for OSINT research and educational purposes. When adding aircraft data:

1. **Use public sources only** - All information should be from open sources
2. **Verify accuracy** - Cross-reference multiple reliable sources
3. **Respect classifications** - Only include unclassified information
4. **Credit sources** - Document information sources when possible

## Legal Notice

This tool is intended for:
- ✅ Educational purposes
- ✅ Open source intelligence research
- ✅ Aviation enthusiast reference
- ✅ Academic study

**Not intended for:**
- ❌ Classified information handling
- ❌ Operational security violations
- ❌ Unauthorized intelligence collection

## 🚨 Disclaimer

All aircraft information is derived from publicly available sources. Users should verify information independently and comply with all applicable laws and regulations regarding information collection and use.

## Support

For technical issues or feature requests, please refer to the application logs for diagnostic information. The logging system provides detailed information about database operations and error conditions.

---

**Version**: 2.0  
**Last Updated**: 2025  
**License**: MIT  
**Compatibility**: Python 3.7+
