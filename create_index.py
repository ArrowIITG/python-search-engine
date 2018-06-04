#!/usr/bin/env python
import glob , os , io
import re
import numpy as np
import query
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict , Counter

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

tf = {}
tf_idf_ranking = {}
idf = {}
tf_query = {}
tf_idf_query = {}

def process_query(query_string):
	pattern = re.compile('[\W_]+')
	query_string = pattern.sub(' ' , query_string);
	query_word_list = query_string.split();
	
	query_word_list2 = []

	for word in query_word_list:
		if word not in stop_words:
			word = ps.stem(word)
			query_word_list2.append(word)

	return query_word_list2;
	

def process_files(filenames):
	file_to_terms = {}
	for file in filenames:
		pattern = re.compile('[\W_]+')
		file_to_terms[file] = open(file, 'r').read().lower();
		file_to_terms[file] = pattern.sub(' ',file_to_terms[file])
		file_to_terms[file] = file_to_terms[file].split()
	return file_to_terms

def index_one_file(termlist):
	word_to_pos = {}
	for index , word in enumerate(termlist):
		if word not in stop_words:
			word = ps.stem(word)
			if word in word_to_pos.keys():
				word_to_pos[word].append(index)
			else:
				word_to_pos[word] = [index]
	return word_to_pos;		


def inverted_index(file_to_word_to_pos):
	word_to_file_to_pos = {}

	for file in file_to_word_to_pos:
		sqr_sum = 0
		for word in file_to_word_to_pos[file]:
			x = len(file_to_word_to_pos[file][word])
			# tf[file] = {word : x}
			# sqr_sum += x**2

			if word in word_to_file_to_pos.keys():
				if file in word_to_file_to_pos[word].keys():
					word_to_file_to_pos[word][file].append(file_to_word_to_pos[file][word]);
					t = tf[word][file]
					sqr_sum -= t**2
					sqr_sum += x**2
					tf[word][file] = x
				else:	
					word_to_file_to_pos[word][file] = file_to_word_to_pos[file][word];
					sqr_sum += x**2
					tf[word][file] = x
			else:
				word_to_file_to_pos[word] = { file : file_to_word_to_pos[file][word] }
				sqr_sum += x**2
				tf[word] = {file : x}	

		sqr_sum = sqr_sum**0.5	

		for word in file_to_word_to_pos[file].keys():
			tf[word][file] = np.divide(float(tf[word][file]) , sqr_sum)		

	return word_to_file_to_pos;			

def ranking(word_to_file_to_pos , txtfiles):

	for word in word_to_file_to_pos.keys():
		idf[word] =  np.log2(len(txtfiles)/len(word_to_file_to_pos[word]))
		for file in txtfiles:
			if file in word_to_file_to_pos[word].keys():
				if word in tf_idf_ranking.keys():
					if file in tf_idf_ranking[word].keys():
						tf_idf_ranking[word][file].append(tf[word][file]*idf[word])
					else:
						tf_idf_ranking[word][file] = tf[word][file]*idf[word]	
				else:	
					tf_idf_ranking[word] = {file : tf[word][file]*idf[word]}
			else :
				if word in tf_idf_ranking.keys():
					if file in tf_idf_ranking[word].keys():
						tf_idf_ranking[word][file].append(0)
					else:
						tf_idf_ranking[word][file] = 0	
				else:	
					tf_idf_ranking[word] = {file : 0}				

	for word in word_to_file_to_pos.keys():
		for file in txtfiles:
			print(word , end = " ")
			print(file , end = " ")	
			print(tf_idf_ranking[word][file])		
			

def cosine_similarity(query_word_list , file):
	num = 0
	sqr_sum = 0	
	print(file)

	for word in query_word_list:
		sqr_sum += tf_idf_ranking[word][file]**2

	sqr_sum = sqr_sum**0.5

	for word in query_word_list:
		if sqr_sum == 0:
			test = 0
		else:	
			test = np.divide(float(tf_idf_ranking[word][file]) , sqr_sum)
		num += test*tf_idf_query[word]

	print(num)	

	return num




		

def query_tf_calculation(query_word_list , query_word_list_ans ):
	sqr_sum = 0

	for word in query_word_list:
		cal = 0
		for file in query_word_list_ans:
			if word in tf.keys() and file in tf[word].keys():
				cal += tf[word][file]


		tf_query[word] = cal	
		sqr_sum += cal**2

	sqr_sum = sqr_sum**0.5
		
	for word in query_word_list:
		tf_query[word] = np.divide(float(tf_query[word]) , sqr_sum)

	sqr_sum = 0	

	for word in query_word_list:
		tf_idf_query[word] = tf_query[word]*idf[word]

	for word in query_word_list:
		sqr_sum += tf_idf_query[word]**2

	sqr_sum = sqr_sum**0.5

	for word in query_word_list:
		tf_idf_query[word] = np.divide(float(tf_idf_query[word]) , sqr_sum)	

	cosine_val = []	

	for file in query_word_list_ans:
		cosine_val.append( cosine_similarity(query_word_list , file) )	 

	zipped = list(zip(query_word_list_ans , cosine_val))	

	zipped.sort(key=lambda tup: tup[1], reverse=True)

	return zipped



if __name__ == '__main__':
	txtfiles = []
	os.chdir("./files_to_read")
	for file in glob.glob("*.txt"):
	    txtfiles.append(file)

	file_to_terms = process_files(txtfiles) 

	file_to_word_to_pos = {} 

	for file in file_to_terms:
		file_to_word_to_pos[file] = index_one_file(file_to_terms[file]);


	word_to_file_to_pos = inverted_index(file_to_word_to_pos)

	print(word_to_file_to_pos)

	ranking(word_to_file_to_pos , txtfiles)

	ans = input("Do you want to make query?")

	if ans == 'y':
		print("what type of query do you want ??")
		print("press 1 to make one word query")
		print("press 2 to make free text query")
		print("press 3 to make free text query intersection")
		print("press 4 to make phrase query")

		ans = input("press")
		query_string = input("input string :: ")
		query_word_list = process_query(query_string)
		print(query_word_list)

		if ans == '1':
			query_word_list_ans = query.one_word_query(word_to_file_to_pos , query_string)

		if ans == '2':
			query_word_list_ans = query.free_text_query(word_to_file_to_pos , query_word_list)

		if ans == '3':
			query_word_list_ans = query.free_text_query_intersection(word_to_file_to_pos , query_word_list)	

		if ans == '4':
			query_word_list_ans = query.phrase_query(word_to_file_to_pos , query_word_list)
	

		if ans == '2':
			final_list = query_tf_calculation(query_word_list , query_word_list_ans)
			for key , value in final_list:
				print(key , end = " ")
		else:
			print(query_word_list_ans)					

	
