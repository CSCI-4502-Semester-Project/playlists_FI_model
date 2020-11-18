import configparser
import pandas as pd
import pbjson
import os
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
from collections import defaultdict

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

def load_playlists(root_dir):
    transactions = []

    for user in os.listdir(root_dir):
        path = root_dir + user + '/'
        for index_file in os.listdir(path):
            if index_file.endswith('.INDEX'):
                index = open(path + index_file, 'r')
                lines = index.readlines()
                transaction = [""] * int(lines[0])
                for i, track_id in enumerate(lines[1::]):
                    transaction[i] = track_id
                
                transactions.append(transaction)

    return transactions

if __name__ =='__main__':
    # read the config file
    config = configparser.ConfigParser()

    # try and open it, might try to act sus...
    try:
        config.read('config.ini')
    except:
        try:
            config.read('../config.ini')
        except:
            print('Error, could not find config.ini')
    
    verbose = config['DEFAULT']['Verbose'].lower() == 'true'

    # load the playlists as transactions
    if verbose:
        print('Loading transactions from disk.')
    playlist_transactions = load_playlists(config['model']['PlaylistsDir'])

    # load the transactions into an encoder and get a pandas dataframe
    if verbose:
        print('Encoding transactions')
    te = TransactionEncoder()
    te_ary = te.fit(playlist_transactions).transform(playlist_transactions)
    playlist_df = pd.DataFrame(te_ary, columns=te.columns_)

    # get the support, confidence, and max k values for the itemsets
    min_sup     = float(config['model']['MinSup'])
    max_k       = int(config['model']['ItemsetSize'])

    # run FP Growth algo on the transactions
    if verbose:
        print('Running FP Growth')

    frequent_itemsets = fpgrowth(playlist_df, min_support=min_sup, use_colnames=True, max_len=max_k)
    frequent_itemsets['length'] = frequent_itemsets['itemsets'].apply(lambda x: len(x))
    k_frequent_itemsets = frequent_itemsets[frequent_itemsets['length'] == max_k]

    # create hash table from frequent itemsets
    if verbose:
        print('Creating hash table')

    track_hash = defaultdict(set)
    itemset_list = k_frequent_itemsets['itemsets'].to_list()
    print('Num itemsets %d' % len(itemset_list))
    for fr_set in itemset_list:
        for item in fr_set:
            track_hash[item] = track_hash[item].union(fr_set) # each track points to the set of the union of itemsets the track is in
    
    # dump hash table as 'model'
    if verbose:
        print('Writing model')
    f = open(config['model']['FrequentItemsetsModel'], 'wb+')
    f.truncate(0)
    pbjson.dump(track_hash, f)
    f.close()

    # we are done
    if verbose:
        print('Done')

