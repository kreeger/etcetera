from heapq import nlargest
from operator import itemgetter

from GChartWrapper import HorizontalBarStack

from etcetera.equipment import models as equipment

def get_top_equipmenttype_graph(
		count,
		the_object,
		from_date=None, until_date=None):
	"""Returns URL string of graph based on top equipment types for checkouts.
	
	Arguments:
	count -- the number of top results you want.
	the_object -- the model/object you're wanting results from (building, ou).
	
	Optional arguments:
	from_date -- the Python datetime.date object of the oldest result.
	until_date -- the Python datetime.date object of the most recent result.
	
	"""
	
	# Create our working objects first
	temp_list = []
	temp_dict = {}
	
	# Get all checkouts
	the_queryset = the_object.checkouts.all()
	# If time period is specified...
	if from_date:
		the_queryset = the_queryset.filter(return_date__gte=from_date)
	if unti_date:
		the_queryset = the_queryset.filter(return_date__lte=until_date)
	
	# For each equipment for each checkout in the queryset...
	for the_checkout in the_queryset:
		for the_equipment in the_checkout.equipment_list.all():
			# Add the equipment's type to the list
			temp_list.append(the_equipment.equipment_type)
	# For each equipment type in the database, count each type of occurring
	# equipment type in our list and add it to a dictionary
	for the_eqtype in equipment.EquipmentType.objects.all():
		temp_dict[the_eqtype] = temp_list.count(the_eqtype)
	
	# Rank the results
	ranked_tuples = nlargest(count, temp_dict.iteritems(), itemgetter(1))
	ranked_data = []
	ranked_labels = []
	for the_tuple in ranked_tuples:
		ranked_labels.append(the_tuple[0])
		ranked_data.append(the_tuple[1])
	
	chart_title = 'Top %i Equipment Types for %s' % (count, the_object.name)
		
	chart = HorizontalBarStack(ranked_data).color('4A0010').axes('xy')
	chart.scale(0, ranked_data[0]).fill('bg','s','65432100').size(650,165)
	
	outlabels = '1:|'
	for item in ranked_labels:
		outstring += unicode(item) + '|'
	url = chart.url + u'&chxl=' + outstring.replace(' ','%20')[:-1]
	url += u'&chxr=0,0,%i,1' % (ranked_data[0],)
	
	return url
	# http://chart.apis.google.com/chart?chxt=x,y&chds=0,7&chd=t:7.0,5.0,4.0,4.0,4.0&chco=4a0010&chs=650x165&cht=bhs&chxl=1:|Data/Video%20Projector|DVD/VCR%20Combo|Computer%20Speaker|Desktop%20Computer|Portable%20P.A.%20System|&chxr=0,0,7,1