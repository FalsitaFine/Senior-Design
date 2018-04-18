import sklearn.datasets
from sklearn.datasets import load_files
import sklearn.metrics
import sklearn.svm
import sklearn.naive_bayes
import numpy as np
from sklearn.naive_bayes import MultinomialNB
import sklearn.neighbors
from sklearn import svm
import sys, os, glob
from pprint import pprint

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


def ML_Classify(text):
	'''
	test_path = './testing'
	test_files = sklearn.datasets.load_files(test_path, encoding = 'latin1', load_content=True)
	#
	# print(test_files)
	print("test_files")
	print(test_files.data)
	X_test_counts = count_vect.transform(test_files.data)
	print("X_test_counts")
	print(X_test_counts.toarray())
	X_test_tfidf = tfidf_transformer.transform(X_test_counts)
	print("X_test_tfidf")
	print(X_test_tfidf.toarray())
	# print(X_test_counts.shape)
	predicted = svm.predict_proba(X_test_counts)
	#
	print("svm.predict")
	print(svm.predict(X_test_counts))
	print("predicted")
	print(predicted)
	'''

	#count_vect = CountVectorizer()
	#print("train",files)
	X_test_countst = count_vect.transform([text])

	X_test_tfidft = tfidf_transformer.transform(X_test_countst)
	predict_result = svmi.predict_proba(X_test_tfidft)
	print("test = " , svmi.predict_proba(X_test_tfidft))
	print(predict_result.shape)
	#print(predict_result[0][1])
	#print(predict_result.shape[1])
	print(svmi.predict(X_test_countst))
	print(X_test_countst.toarray())

	#for i in range(predict_result.shape[1]):





path = './dataset'
files = sklearn.datasets.load_files(path, encoding = 'latin1', decode_error = 'replace', load_content=True, random_state=3)
# print(files)
count_vect = CountVectorizer()

X_train_counts = count_vect.fit_transform(files.data)

tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
# print(X_train_tfidf)
# print("Target")
# print(files)
# print()
# print((X_train_counts))
svmi = svm.SVC(kernel = 'linear', probability=True)
X = X_train_tfidf
# pprint(files.values())
Y = files["target"]
print("Shapes")
print(X.shape)
print(Y.shape)
h = svmi.fit(X, Y)
print(h)
# print("Now doing test files")

#svm_get = training()
ML_Classify('Do you like to try some medicine for next few weeks?')
ML_Classify('I cought a cold and worn down these days')