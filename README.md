# DataDetective
A comprehensive data analysis tool for the Smart City Living Lab, SCRC-IIITH.

### Packages Used
- ADTK : A Python package for data analysis and visualization.
- Numpy : A Python package for scientific computing.
- python-telegram-bot : A Python package for Telegram Bot API.
- matplotlib : A Python package for plotting graphs.
- pandas : A Python package for data analysis.
- scikit-learn : A Python package for machine learning.
- alive-progress : A Python package for progress bar.

### Installation
- install dependencies
- `sudo ln -s /path/to/datadetective.py /usr/local/bin/datadetective`
- `sudo chmod 755 /usr/local/bin/datadetective`

### Usage
Usage: datadetective [OPTIONs]...

Options:
-	-h or --help: Print this help message
-	-i or --interactive: Interactive mode
-	-1 or --fetch: If not in interactive mode, fetch data and cache locally
-	-2 or --freq: If not in interactive mode, perform posting frequency analytics
-	-3 or --nan: If not in interactive mode, perform nan posting analytics
-	-4 or --outlier: If not in interactive mode, perform outlier/anomaly analytics
-	-5 or --notif: If not in interactive mode, perform notification analytics
-	-6 or --daily: If not in interactive mode, perform full daily posting routine