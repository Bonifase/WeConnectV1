def clean_data(data):
	cleaned_data = {}
	for key in data.keys():
		cleaned_data[key] = str(data[key])
	return cleaned_data