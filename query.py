#!/usr/bin/env python
import re
import numpy 

def one_word_query(word_to_file_to_pos , query_word):
	pattern = re.compile('[\W_]+')
	query_word = pattern.sub(' ' , query_word);
		
	if query_word in word_to_file_to_pos.keys():
		return [filename for filename in word_to_file_to_pos[query_word].keys()]
	else:
		return []

def free_text_query(word_to_file_to_pos , query_word_list):
	query_word_list_ans = []

	for word in query_word_list:
		if word in word_to_file_to_pos.keys():	
			query_word_list_ans += [i for i in word_to_file_to_pos[word].keys()]

	query_word_list_ans = set(query_word_list_ans)

	return query_word_list_ans	

def  intersection_lists(list1 , list2):
	list3 = [value for value in list1 if value in list2]
	return list3

def free_text_query_intersection(word_to_file_to_pos , query_word_list):
	query_word_list_ans = []
	i = 0
	for word in query_word_list:
		tmp = []
		if word in word_to_file_to_pos.keys():	
			tmp = [i for i in word_to_file_to_pos[word].keys()]
			if i != 0 :
				query_word_list_ans = intersection_lists(query_word_list_ans , tmp)
			else:
				query_word_list_ans = tmp
				if query_word_list_ans != []:
					i = 1	

	return query_word_list_ans				


def phrase_query(word_to_file_to_pos , query_word_list):
	query_word_list_ans = free_text_query_intersection(word_to_file_to_pos , query_word_list)

	final_result = []
	result_size = []

	for file in query_word_list_ans:
		i = 0
		for word in query_word_list:
			tmp = []
			array = numpy.array(word_to_file_to_pos[word][file])
			array = array - i
			if i == 0:
				result = array
			else:
				result = numpy.intersect1d(result , array)	
			i = i + 1
		
		if result.size > 0 :
			final_result.append(file)
			result_size.append(result.size)
	
	zipped = list(zip(final_result , result_size))

	zipped.sort(key=lambda tup: tup[1], reverse=True)
	
	final_result = []

	for key , value in zipped:
		final_result.append(key)

	return final_result
