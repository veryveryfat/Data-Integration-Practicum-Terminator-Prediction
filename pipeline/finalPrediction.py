#! /usr/bin/env python

from Bio import SeqIO
from trainModel import Model
import pandas as pd
import pickle
import sys

"""
    This is file takes a GO term and a file name of genome to be tested
    as imput, and gives the final prediction
"""
# Classifier's file name
GO = sys.argv[1]
# The file name of the genome to be predicted (should be .fa file)
genomeFile = sys.argv[2]

fileName = genomeFile.split('/')[-1][:-3]

try:
    model = pickle.load(open('./classifiers/' + GO, "r"))
except IOError:
    print "The classifier of " + sys.argv[1] \
    + "is not existed under the folder ./classifiers."

columns = ['ID', 'Offset', 'Nearby Sequence']
results = pd.DataFrame(columns=columns)

for seq_record in SeqIO.parse(genomeFile, "fasta"):
    i = 0
    count = 0
    sequence = seq_record.seq
    while i + 400 < len(sequence):

        # Print every 16,000 bps are processed
        if i % 16000 == 0:
            print seq_record.id + " has been processed for " + str(i) + " bp"
            print "Currently, " + str(count) + " segments are predicted as TTS"


        currSeq = str(sequence[i:i+400])
        prediction = 0
        
        if "N" not in currSeq:            
            prediction = model.predict(currSeq)
            
            if prediction == 1:
                ## add seq_record.id, offset(i+300), nearby sequence(str(seq_record[i+300:i+400])), to results dataframe
                curDF = [seq_record.id, i+300, str(sequence[i+300:i+400])]
                results.loc[len(results)] = curDF

                count = count + 1
                
        i = i + 50

# Output the prediction result
results.to_csv('./results/' + GO + '_TTS_' + fileName + '.csv')