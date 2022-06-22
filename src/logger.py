from datetime import datetime

def logthis(message):
	"""
	A small function to log the messages to a file.
	"""

	last_100_lines=[]
	truncate = False

	# append the message to log.txt
	with open('log.txt', 'a') as log:
		log.write("----------------\n")
		log.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
		log.write("\n")
		log.write(message)
		log.write('\n')
	log.close()

	# if log.txt exceeds 2000 lines, truncate it to the latest 100 lines
	with open('log.txt', 'r') as log:
		data=log.readlines()
		if len(data)>2000:
			last_100_lines=data[-100:]
			truncate=True
	log.close()
	if truncate:
		with open('log.txt', 'w') as log:
			for line in last_100_lines:
				log.write(line)
		log.close()
	
		
	