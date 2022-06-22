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
- .env file format:
```
USER_EMAIL = < enter IIITH RS API - verified email >
USER_PASSWORD = < enter IIITH RS API - verified password >
API_KEY = < leave blank, will be auto-generated >
BOT_TOKEN = < telegram bot token (secret) >
```

### Usage
While in /src, ... 
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

### Output Directory Structure
```
/
- /src
	- /output
		- /VerticalName
			- /analytics
				- frequency_SensorName.png
				- nans_SensorName.png
				- outlier_SensorName.png
			- SensorName.json
		- /metadata
			- /dead_nodes.json
			- /freq_metadata.json
			- /nans_metadata.json
			- /outlier_metadata.json
	- datadetective.py and other files
	- .env

```